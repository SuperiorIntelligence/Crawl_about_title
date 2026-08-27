# Coffee Price Crawler

پیدا کردن **ارزان‌ترین قهوه عربیکا و روبوستا** از فروشگاه‌های ایرانی وب،
با مقایسهٔ درست بر اساس **قیمت به ازای گرم** (نه قیمت خام بسته)، و دادن **لینک**.

## نصب

```powershell
cd d:\WorkMe\Crawl_about_title
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## اجرا

### حالت Demo (بدون اینترنت — دادهٔ نمونه)

```powershell
$env:PYTHONPATH = "src"
python -m core.cli run --demo
```

در Demo همان مثال تو اعمال می‌شود: بستهٔ ۵۰۰ گرمی ۱۲۰ هزار از ۲۵۰ گرمی ۱۰۰ هزار
**ارزان‌تر** است چون قیمت/گرم کمتر است.

### Crawl زنده (بذر + کشف فروشگاه‌های .ir)

```powershell
$env:PYTHONPATH = "src"
python -m core.cli run
```

گزینه‌ها:
- `--no-discover` — فقط منابع بذر در `config/settings.yaml`
- `--no-cache` — نادیده گرفتن کش

### UI + API

```powershell
$env:PYTHONPATH = "src"
python -m core.cli serve
```

باز کن: http://127.0.0.1:5000

> روی بعضی ویندوزها پورت‌های ۸۰۰۰–۸۱۳۴ رزرو Hyper-V هستند؛ پیش‌فرض اپ **۵۰۰۰** است.

- `GET /` — رابط وب
- `GET /api/results` — آخرین گزارش
- `POST /api/crawl` — اجرای مجدد (`{"demo": true}` یا زنده)

## Graphify

بعد از نصب [Graphify](https://github.com/Graphify-Labs/graphify):

```powershell
graphify .
# پس از تغییر ساختاری:
graphify . --update
```

## ساختار

```
src/
  api/          # FastAPI
  core/         # config, cache, rate-limit, CLI
  models/       # ProductOffer / CrawlReport
  schemas/      # API schemas
  services/     # normalize, rank, discovery, crawlers, pipeline
  web/          # Jinja UI
config/settings.yaml
data/fixtures/
tests/
```

## نسخه‌ها

| نسخه | محتوا |
|------|--------|
| v1 | نرمال‌سازی وزن + بذر + CLI |
| v2 | کشف فروشگاه‌های ایرانی از وب |
| v3 | rate-limit، کش، API |
| v4 | UI وب |

Plane استفاده نمی‌شود؛ تحویل از طریق GitHub.

## محدودیت واقع‌بینانه

سایت‌های بزرگ ممکن است ربات را مسدود کنند؛ در آن صورت خطا در گزارش می‌آید
و منابع قابل‌پارس (از جمله fixture و فروشگاه‌های کشف‌شدهٔ ساده‌تر) مقایسه می‌شوند.
لیست بذر را در `config/settings.yaml` گسترش بده.
