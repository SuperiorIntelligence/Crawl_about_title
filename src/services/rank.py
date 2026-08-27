"""رتبه‌بندی پیشنهادها بر اساس قیمت به ازای گرم."""

from __future__ import annotations

from models.offer import CoffeeType, CrawlReport, ProductOffer, RankedResult


def rank_offers(offers: list[ProductOffer]) -> CrawlReport:
    """جداسازی عربیکا/روبوستا و انتخاب ارزان‌ترین بر اساس قیمت/گرم."""
    arabica = [o for o in offers if o.coffee_type == CoffeeType.ARABICA]
    robusta = [o for o in offers if o.coffee_type == CoffeeType.ROBUSTA]

    def _sorted(items: list[ProductOffer]) -> list[ProductOffer]:
        with_unit = [o for o in items if o.price_per_gram is not None]
        return sorted(with_unit, key=lambda o: o.price_per_gram or 0.0)

    a_sorted = _sorted(arabica)
    r_sorted = _sorted(robusta)
    return CrawlReport(
        arabica=RankedResult(
            coffee_type=CoffeeType.ARABICA,
            winner=a_sorted[0] if a_sorted else None,
            offers=a_sorted,
        ),
        robusta=RankedResult(
            coffee_type=CoffeeType.ROBUSTA,
            winner=r_sorted[0] if r_sorted else None,
            offers=r_sorted,
        ),
    )
