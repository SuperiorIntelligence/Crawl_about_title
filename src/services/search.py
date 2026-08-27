"""جستجوی عمومی کمترین قیمت از چند مارکت‌پلیس ایرانی."""

from __future__ import annotations

from typing import Any, Optional

from core import FileCache, RateLimiter, load_settings, save_results
from models.offer import ProductOffer, SearchReport
from schemas import SearchReportOut
from services.crawlers.basalam_api import basalam_search
from services.crawlers.digikala_api import digikala_search
from services.crawlers.divar_api import divar_search
from services.crawlers.snapp_okala import okala_search, snapp_search
from services.crawlers.torob_api import torob_search
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
    settings: Optional[dict[str, Any]] = None,
) -> SearchReport:
    """جستجو در دیجی‌کالا، باسلام، دیوار، ترب، اسنپ، اکالا."""
    q = (query or "").strip()
    if not q:
        return SearchReport(query="", errors=["query is empty"])

    cfg = settings or load_settings()
    runtime = cfg.get("runtime", {})
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
        _merge("digikala", *digikala_search(q, fetcher))
        _merge("basalam", *basalam_search(q, fetcher))
        _merge("divar", *divar_search(q, fetcher))
        _merge("torob", *torob_search(q))
        _merge("snapp", *snapp_search(q))
        _merge("okala", *okala_search(q))
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
