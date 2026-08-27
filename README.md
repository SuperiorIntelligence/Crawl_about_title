# MinPrice — جستجوی کمترین قیمت

ابزار پیدا کردن **ارزان‌ترین پیشنهاد** برای هر کالا در فروشگاه‌های ایرانی، با **لینک مستقیم**.

برای کالاهای وزنی (مثل قهوه/چای) در صورت امکان مقایسه بر اساس **قیمت به ازای گرم** انجام می‌شود، نه فقط قیمت خام بسته.

ریپو: [SuperiorIntelligence/Crawl_about_title](https://github.com/SuperiorIntelligence/Crawl_about_title)

---

## نصب (ویندوز / PowerShell)

```powershell
cd d:\WorkMe\Crawl_about_title
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

قبل از هر دستور اجرا:

```powershell
$env:PYTHONPATH = "src"
$env:PYTHONIOENCODING = "utf-8"
```

---

## اجرا

### ۱) رابط وب + API (پیشنهادی)

```powershell
python -m core.cli serve
```

مرورگر: [http://127.0.0.1:5000](http://127.0.0.1:5000)

عبارت را بنویس (مثلاً `چای`، `گلس سامسونگ`، `لپ تاپ`) و **جستجو** را بزن.

اگر پورت اشغال/مسدود بود:

```powershell
python -m core.cli serve --port 5001
```

> روی بعضی ویندوزها بازهٔ ۸۰۰۰–۸۱۳۴ توسط Hyper-V رزرو است؛ پیش‌فرض اپ **۵۰۰۰** است.

### ۲) جستجو از ترمینال

```powershell
python -m core.cli search "چای"
python -m core.cli search "گلس سامسونگ" --no-cache
```

### ۳) مسیر قدیمی قهوه (عربیکا/روبوستا)

```powershell
# دادهٔ نمونه محلی
python -m core.cli run --demo

# crawl بذر + کشف
python -m core.cli run
python -m core.cli run --no-discover
```

---

## منابع جستجو

| منبع | وضعیت فعلی |
|------|------------|
| دیجی‌کالا | فعال (API) |
| باسلام | فعال (API) |
| دیوار | فعال (API آگهی) |
| ترب | تلاش می‌شود؛ اغلب ضدربات **490** |
| اسنپ | تلاش می‌شود؛ معمولاً **403** |
| اکالا | تلاش می‌شود؛ معمولاً WAF **583** |

در UI زیر نتایج، **منابع موفق** و در صورت نیاز **هشدار منابع** نمایش داده می‌شود.

---

## API

| متد | مسیر | توضیح |
|-----|------|--------|
| `GET` | `/` | رابط وب |
| `GET` | `/api/health` | سلامت سرویس |
| `GET` | `/api/results` | آخرین گزارش ذخیره‌شده |
| `POST` | `/api/search` | جستجوی عمومی — بدنه: `{"query": "چای", "use_cache": true}` |
| `POST` | `/api/crawl` | مسیر قدیمی قهوه — `{"demo": true}` یا زنده |

---

## تست

```powershell
$env:PYTHONPATH = "src"
python -m pytest -q
```

---

## Graphify

برای گراف دانش کد ([Graphify](https://github.com/Graphify-Labs/graphify)):

```powershell
graphify . --code-only
graphify cluster-only .
# بعد از تغییر ساختاری:
graphify . --code-only
```

خروجی در `graphify-out/` (مثل `graph.json` و `GRAPH_REPORT.md`).

---

## ساختار پروژه

```text
src/
  api/           # FastAPI
  core/          # CLI، کش، rate-limit، تنظیمات
  models/        # ProductOffer / SearchReport / CrawlReport
  schemas/       # اسکیمای API
  services/      # search، normalize، crawlers، pipeline
  web/           # قالب Jinja + استاتیک UI
config/settings.yaml
data/fixtures/   # دادهٔ demo
tests/
graphify-out/
```

---

## نسخه‌ها

| نسخه | محتوا |
|------|--------|
| v1 | نرمال‌سازی وزن + بذر + CLI |
| v2 | کشف فروشگاه از وب |
| v3 | rate-limit، کش، API |
| v4 | UI وب |
| بعدی | جستجوی عمومی چندمنبعی (دیجی‌کالا / باسلام / دیوار / …) |

Plane استفاده نمی‌شود؛ تحویل از طریق **GitHub**.

---

## محدودیت‌ها

- بعضی فروشگاه‌ها ربات را مسدود می‌کنند؛ در آن صورت منبع در بخش هشدار می‌آید و بقیه منابع مقایسه می‌شوند.
- آگهی‌های دیوار ممکن است دست‌دوم / نامرتبط باشند؛ همیشه عنوان و لینک را چک کن.
- قیمت‌ها لحظه‌ای‌اند و به موجودی فروشنده وابسته‌اند.
