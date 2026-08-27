"""جستجوی عمومی کمترین قیمت: مارکت‌پلیس‌ها + کشف وب‌سایت‌های مستقل."""

from __future__ import annotations

from typing import Any, Optional

from core import FileCache, RateLimiter, load_settings, save_results
from models.offer import ProductOffer, SearchReport
from schemas import SearchReportOut
from services.crawlers import crawl_seed
from services.crawlers.basalam_api import basalam_search
from services.crawlers.digikala_api import digikala_search
from services.crawlers.divar_api import divar_search
from services.crawlers.snapp_okala import okala_search, snapp_search
from services.crawlers.torob_api import torob_search
from services.discovery import discover_web_shops
from services.http_fetcher import HttpFetcher
from services.normalize import looks_like_unit_goods

_BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)


def rank_general(offers: list[ProductOffer], *, prefer_unit: bool) -> list[ProductOffer]:
    """مرتب‌سازی پیشنهادها از ارزان به گران."""
    usable = [o for o in offers if o.price_toman > 0]
    if prefer_unit:
        with_unit = [o for o in usable if o.price_per_gram is not None]
        if len(with_unit) >= 2:
            return sorted(with_unit, key=lambda o: o.sort_key(True))
    return sorted(usable, key=lambda o: o.sort_key(False))


def run_search(
    query: str,
    *,
    use_cache: bool = True,
    discover_web: bool = True,
    settings: Optional[dict[str, Any]] = None,
) -> SearchReport:
    """جستجو در مارکت‌پلیس‌ها + کشف و crawl سایت‌های مستقل از وب."""
    q = (query or "").strip()
    if not q:
        return SearchReport(query="", errors=["query is empty"])

    cfg = settings or load_settings()
    runtime = cfg.get("runtime", {})
    dcfg = cfg.get("discovery", {})
    errors: list[str] = []
    offers: list[ProductOffer] = []
    sources: list[str] = []

    cache = FileCache(ttl_sec=int(runtime.get("cache_ttl_sec", 3600)))
    limiter = RateLimiter(float(runtime.get("rate_limit_per_host_sec", 1.0)))
    fetcher = HttpFetcher(
        user_agent=runtime.get("user_agent") or _BROWSER_UA,
        timeout_sec=float(runtime.get("request_timeout_sec", 25)),
        rate_limiter=limiter,
        cache=cache,
        use_cache=use_cache,
    )

    def _merge(name: str, part: list[ProductOffer], err: list[str]) -> None:
        offers.extend(part)
        errors.extend(err)
        if part:
            sources.append(name)

    try:
        # ۱) مارکت‌پلیس‌های اصلی
        _merge("digikala", *digikala_search(q, fetcher))
        _merge("basalam", *basalam_search(q, fetcher))
        _merge("divar", *divar_search(q, fetcher))
        _merge("torob", *torob_search(q))
        _merge("snapp", *snapp_search(q))
        _merge("okala", *okala_search(q))

        # ۲) کشف وب‌سایت‌های مستقل (خارج از ترب/دیجی‌کالا/…)
        if discover_web:
            seeds, derr = discover_web_shops(
                q,
                fetcher,
                require_ir_tld=bool(dcfg.get("require_ir_tld", True)),
                max_total=int(dcfg.get("max_web_seeds", 18)),
                max_per_query=int(dcfg.get("max_results_per_query", 6)),
            )
            errors.extend(derr)
            web_hits = 0
            for seed in seeds:
                part, err = crawl_seed(
                    seed,
                    fetcher=fetcher,
                    coffee_only=False,
                    query=q,
                )
                # خطاهای تکراری هر دامنه را خلاصه نگه دار
                for e in err:
                    if "no parseable" not in e:
                        errors.append(e)
                if part:
                    offers.extend(part)
                    web_hits += len(part)
            if web_hits:
                sources.append("web-discovery")
            elif seeds:
                errors.append(
                    f"web-discovery: visited {len(seeds)} independent pages, "
                    "none yielded parseable prices"
                )
    finally:
        fetcher.close()

    dedup: dict[str, ProductOffer] = {}
    for o in offers:
        prev = dedup.get(o.url)
        if prev is None or o.price_toman < prev.price_toman:
            dedup[o.url] = o
    ranked = rank_general(list(dedup.values()), prefer_unit=looks_like_unit_goods(q))

    report = SearchReport(
        query=q,
        prefer_unit_price=looks_like_unit_goods(q),
        winner=ranked[0] if ranked else None,
        offers=ranked,
        sources=sources,
        errors=errors,
    )
    save_results(SearchReportOut.from_report(report).model_dump(mode="json"))
    return report
