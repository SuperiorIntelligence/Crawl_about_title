"""ارکستراسیون Crawl: بذر + کشف + رتبه‌بندی + ذخیره."""

from __future__ import annotations

from typing import Any, Optional

from core import FileCache, RateLimiter, load_settings, save_results
from models.offer import CrawlReport, ProductOffer
from schemas import ReportOut
from services.crawlers import crawl_seed
from services.discovery import discover_sellers
from services.http_fetcher import HttpFetcher
from services.rank import rank_offers


def run_crawl(
    *,
    demo: bool = False,
    discover: bool = True,
    use_cache: bool = True,
    settings: Optional[dict[str, Any]] = None,
) -> CrawlReport:
    """اجرای کامل پایپ‌لاین و برگرداندن گزارش رتبه‌بندی‌شده."""
    cfg = settings or load_settings()
    runtime = cfg.get("runtime", {})
    errors: list[str] = []
    offers: list[ProductOffer] = []
    discovered_sources: list[str] = []

    if demo:
        for seed in cfg.get("seeds", []):
            if seed.get("kind") != "fixture" or not seed.get("enabled", True):
                continue
            part, err = crawl_seed(seed, fetcher=None, demo_only=False, coffee_only=True)
            offers.extend(part)
            errors.extend(err)
            discovered_sources.append(seed.get("name", "fixture"))
        report = rank_offers(offers)
        report.discovered_sources = discovered_sources
        report.errors = errors
        save_results(ReportOut.from_report(report).model_dump(mode="json"))
        return report

    cache = FileCache(ttl_sec=int(runtime.get("cache_ttl_sec", 3600)))
    limiter = RateLimiter(float(runtime.get("rate_limit_per_host_sec", 1.5)))
    fetcher = HttpFetcher(
        user_agent=runtime.get(
            "user_agent",
            "CoffeePriceCrawler/0.4 (+local research)",
        ),
        timeout_sec=float(runtime.get("request_timeout_sec", 25)),
        rate_limiter=limiter,
        cache=cache,
        use_cache=use_cache,
    )

    try:
        seeds = list(cfg.get("seeds", []))
        if discover:
            dcfg = cfg.get("discovery", {})
            extra, derr = discover_sellers(
                queries=list(dcfg.get("queries", [])),
                fetcher=fetcher,
                require_ir_tld=bool(dcfg.get("require_ir_tld", True)),
                max_results_per_query=int(dcfg.get("max_results_per_query", 8)),
            )
            errors.extend(derr)
            seeds.extend(extra)
            discovered_sources.extend(s["name"] for s in extra)

        for seed in seeds:
            part, err = crawl_seed(seed, fetcher=fetcher, demo_only=False, coffee_only=True)
            offers.extend(part)
            errors.extend(err)
            if part or seed.get("kind") == "fixture":
                discovered_sources.append(seed.get("name", "seed"))
    finally:
        fetcher.close()

    report = rank_offers(offers)
    report.discovered_sources = sorted(set(discovered_sources))
    report.errors = errors
    save_results(ReportOut.from_report(report).model_dump(mode="json"))
    return report
