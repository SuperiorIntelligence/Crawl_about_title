"""اسکیماهای API."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from models.offer import CoffeeType, CrawlReport, ProductOffer, SearchReport


class OfferOut(BaseModel):
    """خروجی یک پیشنهاد برای API/UI."""

    title: str
    coffee_type: CoffeeType = CoffeeType.UNKNOWN
    weight_grams: Optional[float] = None
    price_toman: float
    price_per_gram: Optional[float] = None
    price_per_kg: Optional[float] = None
    url: str
    source: str

    @classmethod
    def from_offer(cls, offer: ProductOffer) -> "OfferOut":
        """تبدیل مدل دامنه به اسکیمای خروجی."""
        return cls(
            title=offer.title,
            coffee_type=offer.coffee_type,
            weight_grams=offer.weight_grams,
            price_toman=offer.price_toman,
            price_per_gram=offer.price_per_gram,
            price_per_kg=offer.price_per_kg,
            url=offer.url,
            source=offer.source,
        )


class RankOut(BaseModel):
    coffee_type: CoffeeType
    winner: Optional[OfferOut] = None
    offers: list[OfferOut] = Field(default_factory=list)


class ReportOut(BaseModel):
    generated_at: datetime
    arabica: RankOut
    robusta: RankOut
    discovered_sources: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)

    @classmethod
    def from_report(cls, report: CrawlReport) -> "ReportOut":
        """تبدیل گزارش قهوه به پاسخ API."""

        def _rank(r):
            return RankOut(
                coffee_type=r.coffee_type,
                winner=OfferOut.from_offer(r.winner) if r.winner else None,
                offers=[OfferOut.from_offer(o) for o in r.offers],
            )

        return cls(
            generated_at=report.generated_at,
            arabica=_rank(report.arabica),
            robusta=_rank(report.robusta),
            discovered_sources=report.discovered_sources,
            errors=report.errors,
        )


class CrawlRequest(BaseModel):
    """درخواست اجرای مجدد Crawl قهوه."""

    demo: bool = False
    discover: bool = True
    use_cache: bool = True


class SearchRequest(BaseModel):
    """درخواست جستجوی عمومی."""

    query: str = Field(min_length=1, max_length=200)
    use_cache: bool = True
    discover_web: bool = True


class SearchReportOut(BaseModel):
    """خروجی جستجوی عمومی."""

    kind: str = "search"
    query: str
    generated_at: datetime
    prefer_unit_price: bool = False
    winner: Optional[OfferOut] = None
    offers: list[OfferOut] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)

    @classmethod
    def from_report(cls, report: SearchReport) -> "SearchReportOut":
        """تبدیل گزارش جستجو به اسکیمای API."""
        return cls(
            query=report.query,
            generated_at=report.generated_at,
            prefer_unit_price=report.prefer_unit_price,
            winner=OfferOut.from_offer(report.winner) if report.winner else None,
            offers=[OfferOut.from_offer(o) for o in report.offers],
            sources=report.sources,
            errors=report.errors,
        )
