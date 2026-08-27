# Graph Report - Crawl_about_title  (2026-08-27)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 135 nodes · 261 edges · 11 communities (10 shown, 1 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 16 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `52f72797`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- CoffeeType
- main.py
- HttpFetcher
- pipeline.py
- run_crawl
- FileCache
- .price_per_gram
- coffee-price-crawler

## God Nodes (most connected - your core abstractions)
1. `run_crawl()` - 19 edges
2. `ProductOffer` - 18 edges
3. `CoffeeType` - 16 edges
4. `HttpFetcher` - 11 edges
5. `CrawlReport` - 11 edges
6. `FileCache` - 10 edges
7. `ReportOut` - 9 edges
8. `crawl_seed()` - 9 edges
9. `parse_listing_html()` - 9 edges
10. `rank_offers()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `test_rank_picks_best_per_gram()` --uses--> `CoffeeType`  [INFERRED]
  tests/test_normalize_rank.py → src/models/offer.py
- `test_detect_coffee_type()` --uses--> `CoffeeType`  [INFERRED]
  tests/test_normalize_rank.py → src/models/offer.py
- `test_rank_picks_best_per_gram()` --uses--> `ProductOffer`  [INFERRED]
  tests/test_normalize_rank.py → src/models/offer.py
- `test_parse_price_with_separators()` --calls--> `parse_price_toman()`  [EXTRACTED]
  tests/test_normalize_rank.py → src/services/normalize.py
- `test_parse_weight_half_kilo()` --calls--> `parse_weight_grams()`  [EXTRACTED]
  tests/test_normalize_rank.py → src/services/normalize.py

## Import Cycles
- None detected.

## Communities (11 total, 1 thin omitted)

### Community 0 - "CoffeeType"
Cohesion: 0.10
Nodes (29): Enum, CoffeeType, _absolute_url(), crawl_seed(), load_fixture_offers(), parse_listing_html(), Any, Path (+21 more)

### Community 1 - "main.py"
Cohesion: 0.11
Nodes (23): get, HTMLResponse, post, Request, get_results(), health(), home(), post_crawl() (+15 more)

### Community 2 - "HttpFetcher"
Cohesion: 0.13
Nodes (13): RateLimiter, محدودکنندهٔ سادهٔ نرخ درخواست به‌ازای هر host., در صورت نیاز صبر می‌کند تا فاصلهٔ مجاز رعایت شود., discover_sellers(), _is_iranian_host(), Any, کشف فروشگاه‌های قهوهٔ ایرانی از طریق جستجوی وب., جستجوی وب برای یافتن دامنه/صفحات فروش قهوه؛ خروجی seedهای html_listing. (+5 more)

### Community 3 - "pipeline.py"
Cohesion: 0.20
Nodes (14): CrawlReport, ProductOffer, BaseModel, RankedResult, مدل‌های دامنه برای پیشنهاد قیمت قهوه., یک پیشنهاد فروش قهوه با وزن و قیمت قابل‌نرمال‌سازی., نتیجهٔ رتبه‌بندی برای یک نوع قهوه., گزارش کامل یک اجرای Crawl. (+6 more)

### Community 4 - "run_crawl"
Cohesion: 0.19
Nodes (11): command, _print_report(), خروجی CLI برای اجرای Crawl و نمایش برندگان., بالا آوردن API + UI وب., اجرای Crawl و چاپ ارزان‌ترین عربیکا/روبوستا با لینک., run(), serve(), Any (+3 more)

### Community 5 - "FileCache"
Cohesion: 0.23
Nodes (9): FileCache, load_settings(), Any, Path, خواندن تنظیمات YAML پروژه., کش فایل‌محور برای پاسخ‌های HTTP / نتایج., خواندن مقدار کش اگر منقضی نشده باشد., ذخیرهٔ آخرین گزارش در data/results.json. (+1 more)

### Community 6 - ".price_per_gram"
Cohesion: 0.40
Nodes (3): computed_field, قیمت به ازای هر گرم (تومان)., قیمت به ازای هر کیلوگرم (تومان).

## Knowledge Gaps
- **1 isolated node(s):** `coffee-price-crawler`
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_crawl()` connect `run_crawl` to `CoffeeType`, `main.py`, `HttpFetcher`, `pipeline.py`, `FileCache`?**
  _High betweenness centrality (0.196) - this node is a cross-community bridge._
- **Why does `ProductOffer` connect `pipeline.py` to `CoffeeType`, `main.py`, `run_crawl`, `.price_per_gram`?**
  _High betweenness centrality (0.160) - this node is a cross-community bridge._
- **Why does `FileCache` connect `FileCache` to `main.py`, `HttpFetcher`, `pipeline.py`, `run_crawl`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `run_crawl()` (e.g. with `CrawlReport` and `ProductOffer`) actually correct?**
  _`run_crawl()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `ProductOffer` (e.g. with `OfferOut` and `crawl_seed()`) actually correct?**
  _`ProductOffer` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `CoffeeType` (e.g. with `OfferOut` and `RankOut`) actually correct?**
  _`CoffeeType` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `HttpFetcher` (e.g. with `crawl_seed()` and `discover_sellers()`) actually correct?**
  _`HttpFetcher` has 2 INFERRED edges - model-reasoned connections that need verification._