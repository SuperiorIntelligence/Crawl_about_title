"""کشف فروشگاه‌های قهوهٔ ایرانی از طریق جستجوی وب."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import parse_qs, quote_plus, unquote, urlparse

from bs4 import BeautifulSoup

from services.http_fetcher import HttpFetcher

_IR_HOST = re.compile(r"(^|\.)ir$", re.IGNORECASE)


def _is_iranian_host(host: str) -> bool:
    host = host.lower().split(":")[0]
    return host.endswith(".ir") or host == "ir"


def _unwrap_ddg_redirect(href: str) -> str | None:
    if not href:
        return None
    if href.startswith("//"):
        href = "https:" + href
    parsed = urlparse(href)
    if "duckduckgo.com" in parsed.netloc and parsed.path.startswith("/l/"):
        qs = parse_qs(parsed.query)
        if "uddg" in qs:
            return unquote(qs["uddg"][0])
    if href.startswith("http"):
        return href
    return None


def discover_sellers(
    queries: list[str],
    fetcher: HttpFetcher,
    require_ir_tld: bool = True,
    max_results_per_query: int = 8,
) -> tuple[list[dict[str, Any]], list[str]]:
    """جستجوی وب برای یافتن دامنه/صفحات فروش قهوه؛ خروجی seedهای html_listing."""
    errors: list[str] = []
    discovered: list[dict[str, Any]] = []
    seen_hosts: set[str] = set()

    for q in queries:
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(q + ' سایت فروش')}"
        try:
            html = fetcher.get_text(url)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"discovery '{q}': {exc}")
            continue

        soup = BeautifulSoup(html, "lxml")
        count = 0
        for a in soup.select("a.result__a, a.result__url, a[href]"):
            href = a.get("href") or ""
            real = _unwrap_ddg_redirect(href)
            if not real:
                continue
            host = urlparse(real).netloc.lower()
            if not host or host in seen_hosts:
                continue
            if require_ir_tld and not _is_iranian_host(host):
                continue
            # فیلتر دامنه‌های عمومی جستجو/شبکه اجتماعی
            if any(
                bad in host
                for bad in (
                    "duckduckgo.",
                    "google.",
                    "bing.",
                    "youtube.",
                    "instagram.",
                    "t.me",
                    "twitter.",
                    "x.com",
                    "wikipedia.",
                )
            ):
                continue
            seen_hosts.add(host)
            discovered.append(
                {
                    "name": f"discovered-{host}",
                    "kind": "html_listing",
                    "enabled": True,
                    "url": real,
                    "coffee_hint": None,
                }
            )
            count += 1
            if count >= max_results_per_query:
                break

    return discovered, errors
