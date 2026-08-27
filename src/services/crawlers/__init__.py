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
    """استخراج کارت‌های محصول از HTML لیست/جستجو."""
    soup = BeautifulSoup(html, "lxml")
    offers: list[ProductOffer] = []
    seen: set[str] = set()

    link_nodes = soup.select(
        "a[href*='/product/'], a[href*='/products/'], a[href*='/p/'], "
        "a[href*='dkp-'], a[href*='/goods/']"
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
        # رد لینک‌های غیرمحصولی کوتاه
        path = urlparse(url).path or ""
        if path in ("/", "") or path.count("/") < 2:
            if "/p/" not in path and "/product" not in path and "dkp-" not in path:
                continue

        title = " ".join(a.stripped_strings) or a.get("title") or ""
        blob = _closest_text(a)
        if coffee_only:
            if "قهوه" not in blob and "coffee" not in blob.lower() and not coffee_hint:
                continue

        price = parse_price_toman(blob)
        if price is None:
            continue

        # اگر کوئری آمده، حداقل یکی از واژه‌ها در عنوان/متن باشد (سخت‌گیری ملایم)
        if query_tokens:
            blob_l = blob.lower()
            if not any(tok.lower() in blob_l for tok in query_tokens):
                # برای مارکت‌پلیس‌هایی که عنوان در لینک جداست سخت نگیر
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
    return offers


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
