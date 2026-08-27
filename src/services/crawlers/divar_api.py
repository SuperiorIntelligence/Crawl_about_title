"""جستجو در دیوار (آگهی‌های فروش)."""

from __future__ import annotations

from models.offer import ProductOffer
from services.http_fetcher import HttpFetcher
from services.normalize import detect_coffee_type, parse_price_toman, parse_weight_grams


def divar_search(query: str, fetcher: HttpFetcher) -> tuple[list[ProductOffer], list[str]]:
    """جستجوی آگهی در API دیوار."""
    url = "https://api.divar.ir/v8/postlist/w/search"
    body = {
        "json_schema": {"category": {"value": "root"}},
        "query": query,
    }
    try:
        fetcher.rate_limiter.wait("api.divar.ir")
        resp = fetcher.client.post(
            url,
            json=body,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Origin": "https://divar.ir",
                "Referer": "https://divar.ir/",
            },
        )
        resp.raise_for_status()
        payload = resp.json()
    except Exception as exc:  # noqa: BLE001
        return [], [f"divar: {exc}"]

    widgets = payload.get("list_widgets") or []
    offers: list[ProductOffer] = []
    for w in widgets:
        if w.get("widget_type") != "POST_ROW":
            continue
        data = w.get("data") or {}
        title = (data.get("title") or "").strip()
        price_text = data.get("middle_description_text") or ""
        price = parse_price_toman(price_text)
        if not title or price is None:
            continue
        token = (((data.get("action") or {}).get("payload") or {}).get("token")) or ""
        if not token:
            continue
        link = f"https://divar.ir/v/{token}"
        offers.append(
            ProductOffer(
                title=title[:240],
                coffee_type=detect_coffee_type(title),
                weight_grams=parse_weight_grams(title),
                price_toman=price,
                url=link,
                source="divar",
            )
        )
    if not offers:
        return [], ["divar: no priced ads found"]
    return offers, []
