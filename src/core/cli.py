"""خروجی CLI برای اجرای Crawl و نمایش برندگان."""

from __future__ import annotations

import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

# اطمینان از import پکیج‌های src وقتی به‌صورت اسکریپت اجرا می‌شود
_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

# ویندوز: خروجی UTF-8 تا متن فارسی در کنسول نشکند
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

from schemas import ReportOut  # noqa: E402
from services.pipeline import run_crawl  # noqa: E402

app = typer.Typer(add_completion=False, no_args_is_help=True)
console = Console(force_terminal=True, emoji=False)


def _print_report(report) -> None:
    out = ReportOut.from_report(report)
    for label, block in (("Arabica", out.arabica), ("Robusta", out.robusta)):
        console.rule(f"[bold]{label}[/bold]")
        if not block.winner:
            console.print("[yellow]No offers found[/yellow]")
            continue
        w = block.winner
        console.print(f"[green]Winner:[/green] {w.title}")
        console.print(
            f"weight: {w.weight_grams:g} g | total: {w.price_toman:,.0f} Toman | "
            f"per-gram: {w.price_per_gram:,.1f}"
        )
        console.print(f"link: {w.url}")
        console.print(f"source: {w.source}")

        table = Table(title=f"{label} ranking (cheapest first)")
        table.add_column("#")
        table.add_column("title")
        table.add_column("g")
        table.add_column("per-g")
        table.add_column("url")
        for i, o in enumerate(block.offers[:15], start=1):
            table.add_row(
                str(i),
                o.title[:40],
                f"{o.weight_grams:g}",
                f"{o.price_per_gram:,.1f}",
                o.url[:60],
            )
        console.print(table)

    if out.discovered_sources:
        console.print("\n[cyan]sources:[/cyan] " + ", ".join(out.discovered_sources))
    if out.errors:
        console.print("\n[red]errors / warnings:[/red]")
        for e in out.errors:
            console.print(f" - {e}")


@app.command("search")
def search_cmd(
    query: str = typer.Argument(..., help="عبارت کالا، مثلاً لپ تاپ یا گلس"),
    no_cache: bool = typer.Option(False, "--no-cache"),
) -> None:
    """جستجوی عمومی کمترین قیمت برای هر کالا."""
    from services.search import run_search

    report = run_search(query, use_cache=not no_cache)
    if not report.winner:
        console.print("[yellow]No offers found[/yellow]")
        for e in report.errors:
            console.print(f" - {e}")
        raise typer.Exit(code=1)
    w = report.winner
    console.print(f"[green]Winner:[/green] {w.title}")
    console.print(f"price: {w.price_toman:,.0f} Toman | link: {w.url}")
    console.print(f"source: {w.source}")


@app.command("run")
def run(
    demo: bool = typer.Option(
        False,
        "--demo",
        help="فقط دادهٔ نمونهٔ محلی (بدون شبکه)",
    ),
    no_discover: bool = typer.Option(
        False,
        "--no-discover",
        help="کشف خودکار فروشگاه از وب را خاموش کن",
    ),
    no_cache: bool = typer.Option(
        False,
        "--no-cache",
        help="کش HTTP را نادیده بگیر",
    ),
) -> None:
    """اجرای Crawl و چاپ ارزان‌ترین عربیکا/روبوستا با لینک."""
    report = run_crawl(
        demo=demo,
        discover=not no_discover,
        use_cache=not no_cache,
    )
    _print_report(report)


@app.command("serve")
def serve(
    host: str = "127.0.0.1",
    port: int = 5000,
) -> None:
    """بالا آوردن API + UI وب (پیش‌فرض پورت 5000 — روی ویندوز 8000 اغلب رزرو است)."""
    import uvicorn

    uvicorn.run("api.main:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    app()
