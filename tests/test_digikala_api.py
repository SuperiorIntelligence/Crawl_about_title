from __future__ import annotations

from services.crawlers.digikala_api import digikala_search
from services.http_fetcher import HttpFetcher
from core import RateLimiter


def test_digikala_search_tea_live():
    fetcher = HttpFetcher(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ),
        timeout_sec=25,
        rate_limiter=RateLimiter(0.2),
        use_cache=False,
    )
    try:
        offers, errors = digikala_search("چای", fetcher)
    finally:
        fetcher.close()
    assert not errors or offers, errors
    assert offers, "expected digikala offers for چای"
    assert offers[0].price_toman >= 1000
    assert "digikala.com" in offers[0].url
