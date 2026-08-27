"""API و UI وب برای جستجوی کمترین قیمت."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from core import load_results  # noqa: E402
from schemas import (  # noqa: E402
    CrawlRequest,
    ReportOut,
    SearchReportOut,
    SearchRequest,
)
from services.pipeline import run_crawl  # noqa: E402
from services.search import run_search  # noqa: E402

WEB_DIR = _SRC / "web"
templates = Jinja2Templates(directory=str(WEB_DIR / "templates"))
templates.env.filters["toman"] = lambda n: f"{float(n):,.0f}"

app = FastAPI(
    title="MinPrice Finder",
    description="جستجوی کمترین قیمت برای هر کالا در فروشگاه‌های ایرانی",
    version="0.5.0",
)

static_dir = WEB_DIR / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


def _load_search_view() -> Optional[dict[str, Any]]:
    raw = load_results()
    if not raw:
        return None
    if raw.get("kind") == "search" or "query" in raw:
        try:
            return SearchReportOut.model_validate(raw).model_dump(mode="json")
        except Exception:  # noqa: BLE001
            return raw
    return None


@app.get("/api/health")
def health() -> dict:
    """سلامتی سرویس."""
    return {"status": "ok"}


@app.get("/api/results")
def get_results() -> Optional[dict]:
    """آخرین گزارش ذخیره‌شده."""
    return load_results()


@app.post("/api/search", response_model=SearchReportOut)
def post_search(body: SearchRequest) -> SearchReportOut:
    """جستجوی عمومی کمترین قیمت برای کوئری آزاد."""
    report = run_search(
        body.query,
        use_cache=body.use_cache,
        discover_web=body.discover_web,
    )
    return SearchReportOut.from_report(report)


@app.post("/api/crawl", response_model=ReportOut)
def post_crawl(body: CrawlRequest) -> ReportOut:
    """مسیر قدیمی Crawl قهوه عربیکا/روبوستا."""
    report = run_crawl(
        demo=body.demo,
        discover=body.discover,
        use_cache=body.use_cache,
    )
    return ReportOut.from_report(report)


@app.get("/", response_class=HTMLResponse)
def home(request: Request, q: str = "") -> HTMLResponse:
    """صفحهٔ جستجو و نتایج."""
    report = _load_search_view()
    # اگر ?q= آمده و با آخرین گزارش یکی نیست، فقط فرم را با همان q نشان بده
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "query": q or (report or {}).get("query", ""),
            "report": report,
        },
    )
