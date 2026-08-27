# Project Roadmap

Maintained by the `roadmap` agent. Human approval required for "Released".

---

## Project: Iranian Coffee Price Crawler

### Vision
ابزار Crawl برای یافتن ارزان‌ترین قهوه عربیکا/روبوستا در فروشگاه‌های ایرانی وب،
با نرمال‌سازی وزن (قیمت/گرم) و لینک مستقیم.

### Versions
| Version | Goal (one sentence) | Depends on | Status |
|---|---|---|---|
| v1 | هسته + نرمال‌سازی وزن + بذر + CLI | - | Implemented (awaiting release approve) |
| v2 | کشف خودکار فروشگاه‌های .ir | v1 | Implemented (awaiting release approve) |
| v3 | rate-limit، کش، API | v2 | Implemented (awaiting release approve) |
| v4 | UI وب | v3 | Implemented (awaiting release approve) |

### Current Version
v4 (code complete on `feature/coffee-price-crawler`; mark Released after human merge)

### v1 — هستهٔ Crawl و مقایسهٔ واحد
Scope: models, normalize, seed crawlers, CLI — **done in code**
Acceptance Criteria:
- [x] CLI crawl
- [x] Arabica/Robusta ranking
- [x] per-gram comparison
- [x] winner link
- [x] unit tests

### v2 — کشف فروشگاه از وب
Scope: DuckDuckGo HTML discovery for `.ir` sellers — **done in code**

### v3 — پایدارسازی و API
Scope: RateLimiter, FileCache, FastAPI `/api/*` — **done in code**

### v4 — UI وب
Scope: Jinja UI at `/` — **done in code**

Plane: not used
Git hosting: GitHub

---

## Version History
```
(empty — awaiting human release approval after PR merge)
```
