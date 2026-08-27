"""تلاش برای جستجو در اسنپ‌مارکت / اکالا (اغلب ضدربات یا SPA بدون API عمومی)."""

from __future__ import annotations

from urllib.parse import quote_plus

from services.crawlers.cf_session import create_scraper


def snapp_search(query: str) -> tuple[list, list[str]]:
    """تلاش برای API/صفحه اسنپ؛ در صورت عدم دسترسی پیام خطا برمی‌گرداند."""
    scraper = create_scraper()
    if scraper is None:
        return [], ["snapp: cloudscraper missing"]
    q = quote_plus(query)
    urls = [
        f"https://api.snapp.market/v1/search?q={q}",
        f"https://snapp.market/api/v1/search?q={q}",
    ]
    for url in urls:
        try:
            resp = scraper.get(url, timeout=25, headers={"Accept": "application/json"})
            ctype = resp.headers.get("content-type") or ""
            if resp.status_code == 200 and "json" in ctype:
                data = resp.json()
                # اگر ساختار ناشناخته بود، فعلاً خالی
                products = data.get("products") or data.get("results") or data.get("items") or []
                if products:
                    # پارس حداقلی در صورت وجود
                    from models.offer import ProductOffer
                    from services.normalize import detect_coffee_type, parse_weight_grams

                    offers = []
                    for p in products:
                        title = (p.get("title") or p.get("name") or "").strip()
                        price = p.get("price") or p.get("selling_price")
                        if not title or not price:
                            continue
                        offers.append(
                            ProductOffer(
                                title=title[:240],
                                coffee_type=detect_coffee_type(title),
                                weight_grams=parse_weight_grams(title),
                                price_toman=float(price),
                                url=p.get("url") or "https://snapp.market/",
                                source="snapp",
                            )
                        )
                    if offers:
                        return offers, []
            if resp.status_code in (403, 429, 490, 583):
                return [], [f"snapp: blocked (HTTP {resp.status_code}) — نیاز به مرورگر/لاگین"]
        except Exception as exc:  # noqa: BLE001
            last = exc
            continue
    return [], ["snapp: no public searchable API from this environment"]


def okala_search(query: str) -> tuple[list, list[str]]:
    """تلاش برای API اکالا؛ در عمل معمولاً WAF بلاک می‌کند."""
    scraper = create_scraper()
    if scraper is None:
        return [], ["okala: cloudscraper missing"]
    q = quote_plus(query)
    urls = [
        f"https://api.okala.com/api/Search/Products?searchTerm={q}",
        f"https://www.okala.com/api/search?q={q}",
    ]
    for url in urls:
        try:
            resp = scraper.get(url, timeout=25, headers={"Accept": "application/json"})
            ctype = resp.headers.get("content-type") or ""
            if resp.status_code == 200 and "json" in ctype:
                data = resp.json()
                products = data.get("products") or data.get("items") or data.get("data") or []
                if isinstance(products, dict):
                    products = products.get("products") or products.get("items") or []
                if products:
                    from models.offer import ProductOffer
                    from services.normalize import detect_coffee_type, parse_weight_grams

                    offers = []
                    for p in products:
                        title = (p.get("title") or p.get("name") or "").strip()
                        price = p.get("price") or p.get("sellingPrice") or p.get("selling_price")
                        if not title or not price:
                            continue
                        offers.append(
                            ProductOffer(
                                title=title[:240],
                                coffee_type=detect_coffee_type(title),
                                weight_grams=parse_weight_grams(title),
                                price_toman=float(price),
                                url=p.get("url") or "https://www.okala.com/",
                                source="okala",
                            )
                        )
                    if offers:
                        return offers, []
            if resp.status_code in (403, 429, 490, 583):
                return [], [f"okala: blocked (HTTP {resp.status_code}) — WAF/ضدربات"]
        except Exception:  # noqa: BLE001
            continue
    return [], ["okala: no public searchable API from this environment"]
