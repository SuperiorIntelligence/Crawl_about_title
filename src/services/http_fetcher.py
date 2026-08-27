"""کلاینت HTTP با rate-limit و کش و هدر شبیه مرورگر."""

from __future__ import annotations

from typing import Any, Optional
from urllib.parse import urlparse

import httpx

from core import FileCache, RateLimiter


class HttpFetcher:
    """واکشی HTML/JSON با احترام به rate limit و کش محلی."""

    def __init__(
        self,
        user_agent: str,
        timeout_sec: float,
        rate_limiter: RateLimiter,
        cache: Optional[FileCache] = None,
        use_cache: bool = True,
    ) -> None:
        self.user_agent = user_agent
        self.timeout_sec = timeout_sec
        self.rate_limiter = rate_limiter
        self.cache = cache
        self.use_cache = use_cache
        self._client = httpx.Client(
            headers={
                "User-Agent": user_agent,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "fa-IR,fa;q=0.9,en;q=0.8",
                "Cache-Control": "no-cache",
            },
            follow_redirects=True,
            timeout=timeout_sec,
        )

    @property
    def client(self) -> httpx.Client:
        """دسترسی به کلاینت httpx برای آداپترهای API."""
        return self._client

    def get_text(self, url: str) -> str:
        """متن پاسخ را برمی‌گرداند؛ از کش استفاده می‌کند اگر فعال باشد."""
        if self.use_cache and self.cache:
            cached = self.cache.get(url)
            if isinstance(cached, str):
                return cached

        host = urlparse(url).netloc
        self.rate_limiter.wait(host)
        resp = self._client.get(url)
        resp.raise_for_status()
        text = resp.text
        if self.use_cache and self.cache:
            self.cache.set(url, text)
        return text

    def get_json(self, url: str) -> Any:
        """پاسخ JSON را برمی‌گرداند (با کش)."""
        if self.use_cache and self.cache:
            cached = self.cache.get("json:" + url)
            if cached is not None:
                return cached
        host = urlparse(url).netloc
        self.rate_limiter.wait(host)
        resp = self._client.get(url, headers={"Accept": "application/json"})
        resp.raise_for_status()
        data = resp.json()
        if self.use_cache and self.cache:
            self.cache.set("json:" + url, data)
        return data

    def close(self) -> None:
        """بستن کلاینت HTTP."""
        self._client.close()
