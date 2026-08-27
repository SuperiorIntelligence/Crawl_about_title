"""واکشی پیشنهادها از API عمومی دیجی‌کالا."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote_plus

from models.offer import ProductOffer
from services.http_fetcher import HttpFetcher
from services.normalize import detect_coffee_type, parse_weight_grams


def _to_toman(selling_price: float | int | None) -> float | None:
    """قیمت API دیجی‌کالا معمولاً به ریال است → تومان."""
    if selling_price is None:
        return None
    value = float(selling_price)
    if value <= 0:
        return None
    return value / 10.0


def digikala_search(query: str, fetcher: HttpFetcher, page: int = 1) -> tuple[list[ProductOffer], list[str]]:
    """جستجوی کالا در API دیجی‌کالا و تبدیل به ProductOffer."""
    errors: list[str] = []
    url = f"https://api.digikala.com/v1/search/?q={quote_plus(query)}&page={page}"
    try:
        payload: dict[str, Any] = fetcher.get_json(url)
    except Exception as exc:  # noqa: BLE001
        return [], [f"digikala: {exc}"]

    products = ((payload.get("data") or {}).get("products")) or []
    offers: list[ProductOffer] = []
    for p in products:
        title = (p.get("title_fa") or p.get("title_en") or "").strip()
        if not title:
            continue
        dv = p.get("default_variant") or {}
        price = _to_toman((dv.get("price") or {}).get("selling_price"))
        if price is None:
            continue
        uri = ((p.get("url") or {}).get("uri")) or f"/product/dkp-{p.get('id')}/"
        link = "https://www.digikala.com" + uri
        weight = parse_weight_grams(title)
        offers.append(
            ProductOffer(
                title=title[:240],
                coffee_type=detect_coffee_type(title),
                weight_grams=weight,
                price_toman=price,
                url=link,
                source="digikala",
            )
        )
    if not offers:
        errors.append("digikala: empty product list")
    return offers, errors
