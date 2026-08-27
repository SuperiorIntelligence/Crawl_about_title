from __future__ import annotations

from services.pipeline import run_crawl


def test_demo_pipeline_finds_winners():
    report = run_crawl(demo=True, discover=False)
    assert report.arabica.winner is not None
    assert report.robusta.winner is not None
    # ۵۰۰ گرم / ۱۲۰ هزار باید از ۲۵۰ / ۱۰۰ هزار ارزان‌تر باشد
    assert report.arabica.winner.weight_grams == 500
    assert "example.ir/arabica-500" in report.arabica.winner.url
