"""مدل‌های دامنه برای پیشنهاد قیمت کالا."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, computed_field


class CoffeeType(str, Enum):
    """برای سازگاری با مسیر قهوه؛ در جستجوی عمومی معمولاً unknown است."""

    ARABICA = "arabica"
    ROBUSTA = "robusta"
    UNKNOWN = "unknown"


class ProductOffer(BaseModel):
    """یک پیشنهاد فروش کالا با قیمت و در صورت وجود وزن."""

    title: str
    coffee_type: CoffeeType = CoffeeType.UNKNOWN
    weight_grams: Optional[float] = Field(default=None, gt=0)
    price_toman: float = Field(gt=0, description="قیمت کل به تومان")
    url: str
    source: str
    currency: str = "IRT"
    scraped_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @computed_field  # type: ignore[prop-decorator]
    @property
    def price_per_gram(self) -> Optional[float]:
        """قیمت به ازای هر گرم؛ اگر وزن نباشد None."""
        if not self.weight_grams:
            return None
        return self.price_toman / self.weight_grams

    @computed_field  # type: ignore[prop-decorator]
    @property
    def price_per_kg(self) -> Optional[float]:
        """قیمت به ازای هر کیلوگرم؛ اگر وزن نباشد None."""
        ppg = self.price_per_gram
        return None if ppg is None else ppg * 1000.0

    def sort_key(self, prefer_unit: bool) -> float:
        """کلید مقایسه: واحد (گرم) یا قیمت کل."""
        if prefer_unit and self.price_per_gram is not None:
            return self.price_per_gram
        return self.price_toman


class RankedResult(BaseModel):
    """نتیجهٔ رتبه‌بندی برای یک نوع قهوه (مسیر قدیمی)."""

    coffee_type: CoffeeType
    winner: Optional[ProductOffer] = None
    offers: list[ProductOffer] = Field(default_factory=list)


class CrawlReport(BaseModel):
    """گزارش مسیر قهوه (عربیکا/روبوستا)."""

    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    arabica: RankedResult
    robusta: RankedResult
    discovered_sources: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class SearchReport(BaseModel):
    """گزارش جستجوی عمومی برای هر کوئری کاربر."""

    query: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    prefer_unit_price: bool = False
    winner: Optional[ProductOffer] = None
    offers: list[ProductOffer] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
