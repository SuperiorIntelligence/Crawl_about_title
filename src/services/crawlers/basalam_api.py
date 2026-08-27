"""جستجو در باسلام."""

from __future__ import annotations

from urllib.parse import quote_plus

import httpx

from models.offer import ProductOffer
from services.http_fetcher import HttpFetcher
from services.normalize import detect_coffee_type, parse_weight_grams


def _to_toman(price: float | int | None) -> float | None:
    if price is None:
        return None
    value = float(price)
    if value <= 0:
        return None
    # API باسلام معمولاً ریال برمی‌گرداند
    return value / 10.0 if value >= 10000 else value


def basalam_search(query: str, fetcher: HttpFetcher) -> tuple[list[ProductOffer], list[str]]:
    """جستجوی کالا در API باسلام."""
    url = (
        "https://search.basalam.com/ai-engine/api/v2.0/product/search"
        f"?q={quote_plus(query)}&from=0&size=24"
    )
    try:
        # از کلاینت موجود استفاده می‌کنیم
        host_wait = fetcher.rate_limiter
        host_wait.wait("search.basalam.com")
        resp = fetcher.client.get(
            url,
            headers={
                "Accept": "application/json",
                "Origin": "https://basalam.com",
                "Referer": "https://basalam.com/",
            },
        )
        resp.raise_for_status()
        payload = resp.json()
    except Exception as exc:  # noqa: BLE001
        return [], [f"basalam: {exc}"]

    products = payload.get("products") or []
    offers: list[ProductOffer] = []
    for p in products:
        title = (p.get("name") or "").strip()
        if not title:
            continue
        price = _to_toman(p.get("price") or p.get("primaryPrice"))
        if price is None:
            continue
        pid = p.get("id")
        link = f"https://basalam.com/p/{pid}" if pid else "https://basalam.com/"
        weight = p.get("weight")
        weight_grams = float(weight) if weight else parse_weight_grams(title)
        offers.append(
            ProductOffer(
                title=title[:240],
                coffee_type=detect_coffee_type(title),
                weight_grams=weight_grams if weight_grams and weight_grams > 0 else None,
                price_toman=price,
                url=link,
                source="basalam",
            )
        )
    if not offers:
        return [], ["basalam: empty product list"]
    return offers, []
