"""آداپترهای Crawl و پارس HTML عمومی برای هر کالا."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from core import ROOT
from models.offer import CoffeeType, ProductOffer
from services.http_fetcher import HttpFetcher
from services.normalize import detect_coffee_type, parse_price_toman, parse_weight_grams


def load_fixture_offers(path: str | Path) -> list[ProductOffer]:
    """خواندن پیشنهادهای نمونه از JSON."""
    p = ROOT / path if not Path(path).is_absolute() else Path(path)
    raw = json.loads(p.read_text(encoding="utf-8"))
    offers: list[ProductOffer] = []
    for row in raw:
        offers.append(
            ProductOffer(
                title=row["title"],
                coffee_type=CoffeeType(row.get("coffee_type", "unknown")),
                weight_grams=float(row["weight_grams"]) if row.get("weight_grams") else None,
                price_toman=float(row["price_toman"]),
                url=row["url"],
                source=row.get("source", "fixture"),
            )
        )
    return offers


def _absolute_url(base: str, href: Optional[str]) -> Optional[str]:
    if not href:
        return None
    if href.startswith("#") or href.startswith("javascript:"):
        return None
    return urljoin(base, href)


def _closest_text(node) -> str:
    title = " ".join(node.stripped_strings) if node else ""
    parts = [title]
    cur = node
    for _ in range(4):
        if cur is None:
            break
        parts.append(" ".join(cur.stripped_strings))
        cur = cur.parent
    return " ".join(parts)


def parse_listing_html(
    html: str,
    page_url: str,
    source_name: str,
    *,
    coffee_hint: Optional[str] = None,
    coffee_only: bool = False,
    query: Optional[str] = None,
) -> list[ProductOffer]:
    """استخراج کارت‌های محصول از HTML لیست/جستجو یا صفحهٔ محصول."""
    soup = BeautifulSoup(html, "lxml")
    offers: list[ProductOffer] = []
    seen: set[str] = set()

    link_nodes = soup.select(
        "a[href*='/product/'], a[href*='/products/'], a[href*='/product-'], "
        "a[href*='/p/'], a[href*='dkp-'], a[href*='/goods/'], "
        "a[href*='/shop/'], a[href*='/item/']"
    )
    if not link_nodes:
        link_nodes = soup.find_all("a", href=True)

    query_tokens = []
    if query:
        query_tokens = [t for t in query.strip().split() if len(t) > 1]

    for a in link_nodes:
        href = a.get("href")
        url = _absolute_url(page_url, href)
        if not url or url in seen:
            continue
        path = urlparse(url).path or ""
        if path in ("/", "") or path.count("/") < 2:
            if not any(x in path for x in ("/p/", "/product", "dkp-", "/item/", "/shop/")):
                continue

        title = " ".join(a.stripped_strings) or a.get("title") or ""
        blob = _closest_text(a)
        if coffee_only:
            if "قهوه" not in blob and "coffee" not in blob.lower() and not coffee_hint:
                continue

        price = parse_price_toman(blob)
        if price is None:
            continue

        if query_tokens:
            blob_l = blob.lower()
            if not any(tok.lower() in blob_l for tok in query_tokens):
                if len(title) < 3:
                    continue

        weight = parse_weight_grams(blob)
        ctype = detect_coffee_type(blob, hint=coffee_hint)
        if coffee_only and ctype == CoffeeType.UNKNOWN:
            continue

        seen.add(url)
        offers.append(
            ProductOffer(
                title=(title[:220] or f"item@{urlparse(url).netloc}"),
                coffee_type=ctype,
                weight_grams=weight,
                price_toman=price,
                url=url,
                source=source_name,
            )
        )
        if len(offers) >= 50:
            break

    # اگر کارت پیدا نشد، خود صفحه را به‌عنوان یک پیشنهاد امتحان کن (schema.org / متن)
    if not offers:
        page_offer = _parse_single_page_offer(
            soup, page_url=page_url, source_name=source_name, query=query
        )
        if page_offer:
            offers.append(page_offer)
    return offers


def _parse_single_page_offer(
    soup: BeautifulSoup,
    *,
    page_url: str,
    source_name: str,
    query: Optional[str],
) -> Optional[ProductOffer]:
    """استخراج یک قیمت از صفحهٔ تکی (محصول مستقل)."""
    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
    h1 = soup.find("h1")
    if h1:
        title = " ".join(h1.stripped_strings) or title

    # schema.org
    price = None
    for meta in soup.select('[itemprop="price"], meta[property="product:price:amount"]'):
        content = meta.get("content") or meta.get_text(" ", strip=True)
        if content:
            try:
                # اگر عدد خام لاتین باشد
                raw = content.replace(",", "").strip()
                value = float(raw)
                price = value / 10.0 if value >= 100_000_000 else value
                if price < 1000:
                    price = None
                    continue
                break
            except ValueError:
                price = parse_price_toman(content)
                if price:
                    break

    text = " ".join(soup.stripped_strings)[:4000]
    if price is None:
        price = parse_price_toman(text)
    if price is None:
        return None

    if query:
        tokens = [t for t in query.split() if len(t) > 1]
        blob = f"{title} {text[:800]}".lower()
        if tokens and not any(t.lower() in blob for t in tokens):
            return None

    return ProductOffer(
        title=(title[:220] or f"page@{urlparse(page_url).netloc}"),
        coffee_type=detect_coffee_type(title or text[:200]),
        weight_grams=parse_weight_grams(f"{title} {text[:500]}"),
        price_toman=price,
        url=page_url,
        source=source_name,
    )


def crawl_seed(
    seed: dict[str, Any],
    fetcher: Optional[HttpFetcher],
    demo_only: bool = False,
    *,
    coffee_only: bool = True,
    query: Optional[str] = None,
) -> tuple[list[ProductOffer], list[str]]:
    """اجرای یک منبع بذر."""
    errors: list[str] = []
    name = seed.get("name", "unknown")
    if not seed.get("enabled", True):
        return [], errors

    kind = seed.get("kind")
    if kind == "fixture":
        try:
            return load_fixture_offers(seed["path"]), errors
        except Exception as exc:  # noqa: BLE001
            return [], [f"{name}: fixture error: {exc}"]

    if demo_only:
        return [], errors

    if kind != "html_listing":
        return [], [f"{name}: unsupported kind {kind}"]

    if fetcher is None:
        return [], [f"{name}: fetcher missing"]

    url = seed["url"]
    try:
        html = fetcher.get_text(url)
        offers = parse_listing_html(
            html,
            page_url=url,
            source_name=name,
            coffee_hint=seed.get("coffee_hint"),
            coffee_only=coffee_only,
            query=query,
        )
        if not offers:
            errors.append(f"{name}: no parseable offers (site may block bots)")
        return offers, errors
    except Exception as exc:  # noqa: BLE001
        return [], [f"{name}: {exc}"]
