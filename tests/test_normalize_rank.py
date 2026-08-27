from __future__ import annotations

from services.normalize import (
    detect_coffee_type,
    parse_price_toman,
    parse_weight_grams,
    price_per_gram,
)
from models.offer import CoffeeType, ProductOffer
from services.rank import rank_offers


def test_parse_weight_persian_grams():
    assert parse_weight_grams("دانه قهوه عربیکا ۲۵۰ گرم") == 250.0


def test_parse_weight_half_kilo():
    assert parse_weight_grams("قهوه نیم کیلو روبوستا") == 500.0


def test_parse_weight_kg():
    assert parse_weight_grams("روبوستا 1 کیلوگرم") == 1000.0


def test_price_per_gram_comparison_example():
    # مثال کاربر: ۲۵۰ گرم / ۱۰۰ هزار در برابر ۵۰۰ گرم / ۱۲۰ هزار
    a = price_per_gram(100_000, 250)  # 400
    b = price_per_gram(120_000, 500)  # 240
    assert b < a


def test_detect_coffee_type():
    assert detect_coffee_type("قهوه عربیکا ویژه") == CoffeeType.ARABICA
    assert detect_coffee_type("Robusta Vietnam") == CoffeeType.ROBUSTA


def test_rank_picks_best_per_gram():
    offers = [
        ProductOffer(
            title="arabica 250",
            coffee_type=CoffeeType.ARABICA,
            weight_grams=250,
            price_toman=100_000,
            url="https://a.ir/1",
            source="t",
        ),
        ProductOffer(
            title="arabica 500",
            coffee_type=CoffeeType.ARABICA,
            weight_grams=500,
            price_toman=120_000,
            url="https://a.ir/2",
            source="t",
        ),
        ProductOffer(
            title="robusta 250",
            coffee_type=CoffeeType.ROBUSTA,
            weight_grams=250,
            price_toman=85_000,
            url="https://a.ir/3",
            source="t",
        ),
    ]
    report = rank_offers(offers)
    assert report.arabica.winner is not None
    assert report.arabica.winner.url == "https://a.ir/2"
    assert report.robusta.winner is not None
    assert report.robusta.winner.url == "https://a.ir/3"


def test_parse_price_with_separators():
    assert parse_price_toman("قیمت ۱۲۰٬۰۰۰ تومان") == 120000.0


def test_parse_price_persian_decimal_sep():
    # جداکنندهٔ رایج ترب: ۱٫۰۵۰٫۰۰۰
    assert parse_price_toman("از ۱٫۰۵۰٫۰۰۰ تومان") == 1_050_000.0
