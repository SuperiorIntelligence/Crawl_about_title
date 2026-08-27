"""جستجو در ترب (با cloudscraper؛ گاهی ضدربات بلاک می‌کند)."""

from __future__ import annotations

from urllib.parse import quote_plus

from models.offer import ProductOffer
from services.crawlers.cf_session import scraper_get_json
from services.normalize import detect_coffee_type, parse_price_toman, parse_weight_grams


def _price_from_torob(item: dict) -> float | None:
    # فیلدهای رایج ترب
    for key in ("price", "min_price", "price_text", "price1"):
        val = item.get(key)
        if val is None:
            continue
        if isinstance(val, (int, float)):
            # اغلب تومان است
            return float(val) if val > 0 else None
        if isinstance(val, str):
            parsed = parse_price_toman(val)
            if parsed:
                return parsed
    return None


def torob_search(query: str) -> tuple[list[ProductOffer], list[str]]:
    """جستجوی کالا در API ترب."""
    url = (
        "https://api.torob.com/v4/base-product/search/"
        f"?query={quote_plus(query)}&page=0"
    )
    try:
        payload = scraper_get_json(url, referer="https://torob.com/", retries=3)
    except Exception as exc:  # noqa: BLE001
        return [], [f"torob: blocked/unavailable ({exc})"]

    results = payload.get("results") or []
    offers: list[ProductOffer] = []
    for item in results:
        title = (item.get("name1") or item.get("name") or item.get("title") or "").strip()
        if not title:
            continue
        price = _price_from_torob(item)
        if price is None:
            continue
        link = item.get("web_client_absolute_url") or item.get("absolute_url") or item.get("url")
        if link and link.startswith("/"):
            link = "https://torob.com" + link
        if not link:
            key = item.get("random_key") or item.get("prk")
            link = f"https://torob.com/p/{key}/" if key else "https://torob.com/"
        offers.append(
            ProductOffer(
                title=title[:240],
                coffee_type=detect_coffee_type(title),
                weight_grams=parse_weight_grams(title),
                price_toman=float(price),
                url=link,
                source="torob",
            )
        )
    if not offers:
        return [], ["torob: empty results"]
    return offers, []
