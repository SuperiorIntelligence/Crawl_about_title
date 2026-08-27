"""کشف فروشگاه‌های مستقل از وب (فراتر از مارکت‌پلیس‌های اصلی)."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import parse_qs, quote_plus, unquote, urlparse, urlunparse

from bs4 import BeautifulSoup

from services.http_fetcher import HttpFetcher

# مارکت‌پلیس‌هایی که جداگانه crawl می‌شوند — اینجا فقط سایت‌های مستقل می‌خواهیم
_SKIP_HOSTS = (
    "digikala.com",
    "basalam.com",
    "divar.ir",
    "torob.com",
    "snapp.market",
    "snapp.express",
    "okala.com",
    "emalls.ir",
    "duckduckgo.com",
    "google.",
    "bing.com",
    "yahoo.com",
    "youtube.",
    "instagram.",
    "facebook.",
    "t.me",
    "telegram.",
    "twitter.",
    "x.com",
    "wikipedia.",
    "aparat.com",
    "linkedin.",
    "pinterest.",
)


def _is_iranian_host(host: str) -> bool:
    host = host.lower().split(":")[0]
    return host.endswith(".ir")


def _skipped_host(host: str) -> bool:
    h = host.lower()
    return any(bad in h for bad in _SKIP_HOSTS)


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


def _unwrap_bing_redirect(href: str) -> str | None:
    if not href or not href.startswith("http"):
        return None
    return href


def build_discovery_queries(user_query: str) -> list[str]:
    """چند کوئری جستجو برای پیدا کردن فروشگاه‌های مستقل."""
    q = user_query.strip()
    return [
        f"{q} خرید",
        f"{q} قیمت",
        f"{q} فروشگاه اینترنتی",
        f"{q} فروش آنلاین",
        f"{q} site:.ir خرید",
        f"خرید {q} از فروشگاه",
    ]


def _collect_links_from_ddg(html: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    urls: list[str] = []
    for a in soup.select("a.result__a, a.result__url"):
        real = _unwrap_ddg_redirect(a.get("href") or "")
        if real:
            urls.append(real)
    if not urls:
        for a in soup.find_all("a", href=True):
            real = _unwrap_ddg_redirect(a.get("href") or "")
            if real:
                urls.append(real)
    return urls


def _collect_links_from_bing(html: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    urls: list[str] = []
    for a in soup.select("li.b_algo h2 a, h2 a"):
        real = _unwrap_bing_redirect(a.get("href") or "")
        if real:
            urls.append(real)
    return urls


def _normalize_seed_url(url: str) -> str:
    """نرمال‌سازی URL کشف‌شده."""
    parsed = urlparse(url)
    # حذف fragment
    return urlunparse((parsed.scheme or "https", parsed.netloc, parsed.path or "/", "", parsed.query, ""))


def discover_web_shops(
    query: str,
    fetcher: HttpFetcher,
    *,
    require_ir_tld: bool = True,
    max_total: int = 20,
    max_per_query: int = 6,
) -> tuple[list[dict[str, Any]], list[str]]:
    """جستجوی وب برای یافتن صفحات/فروشگاه‌های مرتبط با کوئری کاربر."""
    errors: list[str] = []
    discovered: list[dict[str, Any]] = []
    seen_hosts: set[str] = set()
    seen_urls: set[str] = set()

    search_jobs: list[tuple[str, str, Any]] = []
    for q in build_discovery_queries(query):
        search_jobs.append(
            (
                "ddg",
                f"https://html.duckduckgo.com/html/?q={quote_plus(q)}",
                _collect_links_from_ddg,
            )
        )
        search_jobs.append(
            (
                "bing",
                f"https://www.bing.com/search?q={quote_plus(q)}&setlang=fa",
                _collect_links_from_bing,
            )
        )

    for engine, search_url, collector in search_jobs:
        if len(discovered) >= max_total:
            break
        try:
            html = fetcher.get_text(search_url)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"web-discovery/{engine}: {exc}")
            continue

        per_q = 0
        for real in collector(html):
            if len(discovered) >= max_total or per_q >= max_per_query:
                break
            try:
                host = urlparse(real).netloc.lower()
            except Exception:  # noqa: BLE001
                continue
            if not host or _skipped_host(host):
                continue
            if require_ir_tld and not _is_iranian_host(host):
                continue
            # یک بار برای هر دامنه + یک صفحه
            seed_url = _normalize_seed_url(real)
            if seed_url in seen_urls:
                continue
            # اگر همین دامنه را داریم، هنوز صفحهٔ محصول جدا را هم بگیر (حداکثر ۲ از هر دامنه)
            host_count = sum(1 for s in discovered if s.get("host") == host)
            if host_count >= 2:
                continue

            seen_urls.add(seed_url)
            seen_hosts.add(host)
            discovered.append(
                {
                    "name": f"web:{host}",
                    "kind": "html_listing",
                    "enabled": True,
                    "url": seed_url,
                    "host": host,
                    "coffee_hint": None,
                }
            )
            per_q += 1

            # مسیرهای جستجوی رایج روی همان دامنه
            origin = f"{urlparse(seed_url).scheme}://{host}"
            for path in (
                f"/?s={quote_plus(query)}",
                f"/search?q={quote_plus(query)}",
                f"/search/?q={quote_plus(query)}",
            ):
                extra = origin + path
                if extra in seen_urls:
                    continue
                if host_count + 1 >= 2 and path != f"/?s={quote_plus(query)}":
                    break
                seen_urls.add(extra)
                discovered.append(
                    {
                        "name": f"web:{host}",
                        "kind": "html_listing",
                        "enabled": True,
                        "url": extra,
                        "host": host,
                        "coffee_hint": None,
                    }
                )
                break  # فقط یک search URL اضافه کن

    if not discovered:
        errors.append("web-discovery: no independent .ir shops found for query")
    return discovered, errors


# سازگاری با مسیر قدیمی قهوه
def discover_sellers(
    queries: list[str],
    fetcher: HttpFetcher,
    require_ir_tld: bool = True,
    max_results_per_query: int = 8,
) -> tuple[list[dict[str, Any]], list[str]]:
    """کشف فروشگاه برای لیست کوئری‌ها (مسیر قدیمی)."""
    all_seeds: list[dict[str, Any]] = []
    errors: list[str] = []
    for q in queries:
        part, err = discover_web_shops(
            q,
            fetcher,
            require_ir_tld=require_ir_tld,
            max_total=max_results_per_query,
            max_per_query=max_results_per_query,
        )
        all_seeds.extend(part)
        errors.extend(err)
    return all_seeds, errors
