"""نرمال‌سازی وزن/قیمت و تشخیص نوع قهوه."""

from __future__ import annotations

import re
from typing import Optional

from models.offer import CoffeeType

_DIGIT_MAP = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")

_WEIGHT_PATTERNS = [
    re.compile(
        r"(?P<n>\d+(?:[.,]\d+)?)\s*(?:گرم(?:ی)?|gr|g)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?P<n>\d+(?:[.,]\d+)?)\s*(?:کیلوگرم|کیلو|kg|kilo)\b",
        re.IGNORECASE,
    ),
    re.compile(r"نیم\s*کیلو", re.IGNORECASE),
]

# قیمت‌های رایج ایرانی با جداکنندهٔ هزارگان ٫٬,
_PRICE_EXPLICIT = re.compile(
    r"(?:از\s*)?(?P<n>\d{1,3}(?:[٬,٫']\d{3})+|\d{4,})\s*(?:تومان|تومن)\b",
    re.IGNORECASE,
)
_PRICE_LOOSE = re.compile(
    r"(?P<n>\d{1,3}(?:[٬,٫']\d{3})+)\s*(?:تومان|تومن|ریال)?",
    re.IGNORECASE,
)


def normalize_digits(text: str) -> str:
    """تبدیل ارقام فارسی/عربی به لاتین."""
    return text.translate(_DIGIT_MAP)


def _to_number(num: str) -> float:
    cleaned = (
        num.replace("٬", "")
        .replace("٫", "")
        .replace(",", "")
        .replace("'", "")
        .replace(" ", "")
    )
    return float(cleaned)


def parse_weight_grams(text: str) -> Optional[float]:
    """استخراج وزن بسته به گرم از عنوان/توضیح."""
    t = normalize_digits(text)
    if re.search(r"نیم\s*کیلو", t, re.IGNORECASE):
        return 500.0
    for pattern in _WEIGHT_PATTERNS:
        m = pattern.search(t)
        if not m:
            continue
        if "نیم" in pattern.pattern:
            return 500.0
        raw = m.group("n").replace(",", ".")
        value = float(raw)
        token = m.group(0).lower()
        if any(x in token for x in ("کیلو", "kg", "kilo")):
            return value * 1000.0
        return value
    return None


def parse_price_toman(text: str) -> Optional[float]:
    """استخراج قیمت به تومان؛ جداکنندهٔ فارسی هزارگان را درست هندل می‌کند."""
    t = normalize_digits(text)
    candidates: list[float] = []

    for pattern in (_PRICE_EXPLICIT, _PRICE_LOOSE):
        for m in pattern.finditer(t):
            chunk = m.group(0)
            try:
                value = _to_number(m.group("n"))
            except ValueError:
                continue
            if "ریال" in chunk:
                value = value / 10.0
            if value >= 1000:
                candidates.append(value)

    if not candidates:
        return None
    return max(candidates)


def detect_coffee_type(text: str, hint: Optional[str] = None) -> CoffeeType:
    """تشخیص عربیکا/روبوستا از متن یا hint."""
    if hint:
        h = hint.lower().strip()
        if h in ("arabica", "عربیکا"):
            return CoffeeType.ARABICA
        if h in ("robusta", "روبوستا"):
            return CoffeeType.ROBUSTA
    arabica = ("عربیک" in text) or ("آرابیکا" in text) or ("arabica" in text.lower())
    robusta = ("روبوست" in text) or ("robusta" in text.lower())
    if arabica and not robusta:
        return CoffeeType.ARABICA
    if robusta and not arabica:
        return CoffeeType.ROBUSTA
    return CoffeeType.UNKNOWN


def looks_like_unit_goods(query: str) -> bool:
    """آیا کوئری شبیه کالای وزنی (مثل قهوه) است تا قیمت/گرم اولویت بگیرد."""
    q = query.lower()
    keys = ("قهوه", "coffee", "چای", "برنج", "شکر", "آرد", "حبوبات", "گرم", "کیلو")
    return any(k in q for k in keys)


def price_per_gram(price_toman: float, weight_grams: float) -> float:
    """محاسبهٔ قیمت واحد به ازای گرم."""
    if weight_grams <= 0:
        raise ValueError("weight_grams must be > 0")
    return price_toman / weight_grams
