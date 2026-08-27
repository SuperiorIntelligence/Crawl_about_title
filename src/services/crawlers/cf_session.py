"""جلسه HTTP با cloudscraper برای عبور از ضدربات ساده."""

from __future__ import annotations

from typing import Any, Optional

try:
    import cloudscraper
except ImportError:  # pragma: no cover
    cloudscraper = None  # type: ignore


def create_scraper():
    """ساخت scraper شبیه مرورگر؛ اگر cloudscraper نباشد None."""
    if cloudscraper is None:
        return None
    return cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "windows", "mobile": False}
    )


def scraper_get_json(url: str, *, referer: Optional[str] = None, retries: int = 3) -> Any:
    """GET JSON با چند تلاش؛ در شکست Exception می‌اندازد."""
    scraper = create_scraper()
    if scraper is None:
        raise RuntimeError("cloudscraper is not installed")
    headers = {"Accept": "application/json"}
    if referer:
        headers["Referer"] = referer
        # warm-up
        try:
            scraper.get(referer, timeout=25)
        except Exception:  # noqa: BLE001
            pass
    last_err: Exception | None = None
    for _ in range(retries):
        try:
            resp = scraper.get(url, timeout=30, headers=headers)
            if resp.status_code == 200 and "application/json" in (resp.headers.get("content-type") or ""):
                return resp.json()
            if resp.status_code == 200:
                # گاهی بدون content-type درست JSON است
                try:
                    return resp.json()
                except Exception as exc:  # noqa: BLE001
                    last_err = exc
            else:
                last_err = RuntimeError(f"HTTP {resp.status_code}")
        except Exception as exc:  # noqa: BLE001
            last_err = exc
    raise RuntimeError(str(last_err) if last_err else "request failed")
