# کارهای انسان — چک‌لیست کامل راه‌اندازی و استفاده

این فایل مخصوص **کسی است که با این قالب کار می‌کند** (نه Agent).

Agentها نمی‌توانند به‌جای تو این کارها را انجام دهند، چون مربوط به
حساب کاربری، توکن، نصب نرم‌افزار روی سیستم، تأیید push/merge، و پر کردن
اطلاعات واقعی پروژه‌ات هستند.

> نام درست تسک‌ترکر سازمان شما: **Plane**  
> (گاهی اشتباهی «Plain» گفته می‌شود — در این قالب همیشه Plane نوشته شده.)

---

## این فایل کجاست؟

```text
docs/HUMAN-SETUP.md
```

مسیر کامل نمونه:
`d:\WorkMe\Creat_project_use_cursor\docs\HUMAN-SETUP.md`

وقتی قالب را به پروژهٔ جدید کپی می‌کنی، این فایل هم باید داخل `docs/` همان
پروژه باشد تا هر عضو تیم بداند چه کارهایی دستی است.

---

## راهنمای سریع (۳۰ ثانیه)

| اولویت | کار | اجباری؟ |
|---|---|---|
| ۱ | کپی قالب + باز کردن پوشه در Cursor | بله |
| ۲ | پر کردن `AGENTS.md` | بله |
| ۳ | وصل Plane MCP (اگر تسک‌ها در Plane هستند) | توصیه‌شده |
| ۴ | پر کردن `.cursor/rules/plane-tasks.mdc` | اگر Plane داری |
| ۵ | نصب و لاگین `gh` و/یا `glab` | اگر می‌خواهی ریپو از Cursor ساخته شود |
| ۶ | پر کردن بریف/Feature و شروع Workflow | بله |
| ۷ | تأیید قبل از `git push` و merge کردن PR/MR | بله |
| ۸ | نصب Graphify و ساخت گراف | توصیه‌شده برای پروژهٔ واقعی |

جزئیات هر مورد پایین است.

---

## مرحله ۰ — کپی قالب به پروژهٔ جدید

### چه کار کنی
1. یک پوشهٔ خالی برای پروژه بساز (مثلاً `D:\WorkMe\MyProject`).
2. از ریشهٔ این قالب، این‌ها را کپی کن:
   - `.cursor\` (کل پوشه)
   - `AGENTS.md`
   - `prompts\`
   - `memory\`
   - `mcp\`
   - `docs\` (شامل همین فایل)
   - `.gitignore.template`
3. در Cursor: **File → Open Folder** → همان پوشهٔ پروژه.

### چه کار نکنی
- توکن و رمز را داخل فایل‌های git-tracked نگذار.
- لازم نیست همهٔ `README.md` ریشه را کپی کنی (اختیاری است).

### دستور نمونه (PowerShell)
```powershell
$src = "d:\WorkMe\Creat_project_use_cursor"
$dst = "d:\WorkMe\MyProject"
New-Item -ItemType Directory -Path $dst -Force | Out-Null
Set-Location $dst
Copy-Item "$src\.cursor" ".\.cursor" -Recurse
Copy-Item "$src\AGENTS.md" ".\AGENTS.md"
Copy-Item "$src\prompts" ".\prompts" -Recurse
Copy-Item "$src\memory" ".\memory" -Recurse
Copy-Item "$src\mcp" ".\mcp" -Recurse
Copy-Item "$src\docs" ".\docs" -Recurse
Copy-Item "$src\.gitignore.template" ".\.gitignore.template"
```

---

## مرحله ۱ — پر کردن `AGENTS.md` (اجباری)

فایل: ریشهٔ پروژه → `AGENTS.md`

### باید پر کنی
- **Backend** — مثلاً `FastAPI + SQLAlchemy + PostgreSQL`
- **Frontend** — مثلاً `React + Vite + Tailwind` یا `none (API-only)`
- **Infra** — مثلاً `Docker + GitHub Actions` یا `local only`
- **Package manager** — مثلاً `uv` / `pnpm`
- **Git hosting** — `github` یا `gitlab` یا `both`
- **Primary remote** — معمولاً `origin` و بگو به کدام host وصل است
- **Plane project** — اگر از Plane استفاده می‌کنی: نام / identifier / project_id
- **Language conventions** در بخش Coding Style — مثلاً `PEP8 + ruff`

### معمولاً دست نزن
بخش‌های Git Policy، Agents، Workflows، Versioning، Graphify، Continuity —
این‌ها قوانین قالب‌اند.

---

## مرحله ۲ — Plane (تسک‌ترکر) — کار دستی تو

جزئیات فنی بیشتر: `mcp/SETUP.md`  
Agent مربوطه: `.cursor/agents/plane.md`  
پرامت‌های آماده: `prompts/plane-sync-template.md`

### ۲.۱ نصب پیش‌نیاز
```powershell
winget install astral-sh.uv
```
باید دستور `uvx` در ترمینال کار کند.

### ۲.۲ گرفتن توکن Plane
1. وارد `https://plane.ir-ma.ir` شو (یا اینستنس خودتان).
2. Personal Access Token بساز.
3. توکن را جای امن نگه دار — **هرگز commit نکن**.

### ۲.۳ اتصال MCP به Cursor
فایل را باز/بساز:

```text
%USERPROFILE%\.cursor\mcp.json
```

محتوای نمونه:

```json
{
  "mcpServers": {
    "plane": {
      "command": "uvx",
      "args": ["plane-mcp-server", "stdio"],
      "env": {
        "PLANE_API_KEY": "توکن_واقعی_تو",
        "PLANE_WORKSPACE_SLUG": "iran_ma",
        "PLANE_BASE_URL": "https://plane.ir-ma.ir"
      }
    }
  }
}
```

سپس:
1. `Ctrl+Shift+P` → **Reload Window**
2. Settings → **MCP** → سرور `plane` باید سبز/متصل باشد
3. در چت بپرس: «کاربر فعلی Plane را نشان بده»

تست API بدون MCP:
```powershell
curl -H "X-API-Key: YOUR_TOKEN" "https://plane.ir-ma.ir/api/v1/users/me/"
```

### ۲.۴ نگاشت این ریپو به پروژهٔ Plane
فایل: `.cursor/rules/plane-tasks.mdc`

جای این‌ها را با مقدار واقعی پر کن:
- نام پروژه
- `identifier`
- `project_id` (UUID)
- در صورت نیاز UUID ماژول‌ها

بدون این نگاشت، Agent نمی‌داند تسک‌های «همین پروژه» کدام‌اند.

### ۲.۵ بعد از وصل شدن چه می‌توانی بپرسی
- لیست کارهای باز / مانده
- وضعیت هر work item
- ساخت/به‌روز کردن تسک از داخل Cursor

نمونه پرامت‌ها داخل `prompts/plane-sync-template.md` است.

### اگر Plane نمی‌خواهی
این مرحله را رد کن و Taskها را دستی در `prompts/feature-template.md` بنویس.
Linear هم اختیاری است و جایگزین/مکمل Plane است — اجباری نیست.

---

## مرحله ۳ — GitHub و/یا GitLab — کار دستی تو

Agent می‌تواند دستورات را آماده کند، ولی **لاگین حساب** و **تأیید push/merge** مال توست.

### ۳.۱ نصب CLI
```powershell
# GitHub
winget install GitHub.cli
gh auth login

# GitLab
winget install GLab.GLab
glab auth login
```

### ۳.۲ ساخت یا اتصال ریپو
1. فایل `prompts/remote-setup-template.md` را پر کن:
   - Platforms: `github` / `gitlab` / `both`
   - نام ریپو، private/public، ...
2. در Chat به Agent `github` بده تا بسازد/وصل کند.
3. وقتی گفت «قبل از push تأیید می‌خواهم» → diff را ببین → بگو بله/خیر.

### ۳.۳ در طول کار روزمره (همیشه)
طبق قانون قالب:
- Agent روی `main` مستقیم کار نمی‌کند.
- قبل از `git push` **متوقف می‌شود** و از تو تأیید می‌خواهد.
- PR (GitHub) یا MR (GitLab) را باز می‌کند ولی **خودش merge نمی‌کند**.
- **Merge نهایی روی سایت GitHub/GitLab کار خودت است.**

### ۳.۴ هرگز
- توکن/PAT را داخل ریپو commit نکن.
- force-push به main نخواه مگر واقعاً لازم و آگاهانه.

---

## مرحله ۴ — Graphify (توصیه‌شده)

برای اینکه Agent کمتر فایل خام بخواند و توکن کمتری مصرف کند:

```powershell
winget install astral-sh.uv
uv tool install graphifyy
graphify cursor install
```

بعد از اینکه کمی کد واقعی نوشته شد:
```powershell
graphify .
```

بعد از تغییرات ساختاری بزرگ:
```powershell
graphify . --update
```

خروجی در `graphify-out/` می‌آید.  
راهنما: `mcp/SETUP.md` و `.cursor/rules/graphify.mdc`

---

## مرحله ۵ — شروع کار روی محصول (پرامت‌ها)

### پروژهٔ بزرگ / چندنسخه‌ای
1. `prompts/project-brief-template.md` را پر کن (کل ایده).
2. در Chat:

```text
Act as the agents defined in .cursor/agents, starting with roadmap,
follow .cursor/workflows/version-workflow.md step by step for the
project below, and respect AGENTS.md and .cursor/rules.

@prompts/project-brief-template.md
```

3. **حتماً** خروجی `memory/roadmap.md` را بخوان و تأیید کن قبل از کدنویسی.

### یک Feature
1. `prompts/feature-template.md` را پر کن (یا از Plane بکش).
2. `feature-workflow` را اجرا کن.
3. بعد از هر مرحله بگو `ادامه بده` یا اصلاح بخواه.

### باگ
`prompts/bug-template.md` + `bugfix-workflow.md`

### ادامه بعد از چند روز قطعی
فقط بگو:
```text
طبق memory/progress.md ادامه بده. از اول شروع نکن.
```

---

## مرحله ۶ — چیزهایی که همیشه «تأیید انسان» می‌خواهند

این‌ها را Agent نباید خودش تمام کند:

| موضوع | نقش تو |
|---|---|
| `git push` | باید صریحاً بگویی «باشه / تأیید» |
| ساخت ریپوی جدید روی GitHub/GitLab | تأیید قبل از push اول |
| Merge کردن PR/MR | روی سایت خودت Merge کن |
| جلو بردن Current Version بعد از Release | بعد از `release-workflow` صریحاً تأیید کن |
| حذف Branch / remote / repo | فقط با تأیید صریح همین Session |
| گذاشتن توکن در فایل | اصلاً نگذار داخل git |

---

## مرحله ۷ — کامنت فارسی (نیازی به Setup جدا نیست)

این سیاست از قبل در قالب فعال است (`.cursor/rules/coding-style.mdc`):

- Docstring / توضیح‌های مفید → فارسی
- نام تابع و متغیر → انگلیسی
- روی هر خط کامنت نگذار

کار اضافه برای تو: فقط در Review دقت کن Agent این قانون را رعایت کرده باشد.
اگر رعایت نکرد، بگو اصلاح کند.

---

## مرحله ۸ — فایل‌هایی که تو پر می‌کنی در برابر فایل‌هایی که Agent پر می‌کند

### تو پر می‌کنی
| فایل | کی |
|---|---|
| `AGENTS.md` (بخش‌های fill in) | یک‌بار اول پروژه |
| `prompts/project-brief-template.md` | شروع پروژهٔ بزرگ |
| `prompts/feature-template.md` / `bug-template.md` | هر کار (اگر از Plane نکشیدی) |
| `prompts/remote-setup-template.md` | وقتی ریپو می‌سازی |
| `.cursor/rules/plane-tasks.mdc` | نگاشت پروژه Plane |
| `%USERPROFILE%\.cursor\mcp.json` | اتصال Plane/MCP |
| `.gitignore` (از روی template) | یک‌بار |

### Agent پر / آپدیت می‌کند
| فایل | کی |
|---|---|
| `memory/roadmap.md` | بعد از Roadmap |
| `memory/progress.md` | بعد از هر مرحله |
| `memory/decisions.md` | هنگام تصمیم معماری |
| `graphify-out/*` | بعد از `graphify .` (تو دستور را می‌زنی) |

---

## چک‌لیست نهایی قبل از اولین Feature واقعی

- [ ] قالب را در پوشهٔ پروژه کپی کردم و در Cursor باز کردم
- [ ] `AGENTS.md` را پر کردم (استک + git hosting)
- [ ] (اختیاری ولی مهم) Plane MCP وصل است و تست «کاربر فعلی» جواب داد
- [ ] (اگر Plane) `plane-tasks.mdc` را با UUID واقعی پر کردم
- [ ] (اگر ریپو می‌خواهم) `gh` و/یا `glab` لاگین است
- [ ] برای پروژهٔ بزرگ: `project-brief-template.md` پر شده
- [ ] می‌دانم قبل از push باید تأیید بدهم و خودم PR/MR را merge می‌کنم
- [ ] (توصیه) Graphify نصب شده و بعد از اولین کد، `graphify .` زده می‌شود
- [ ] توکن‌ها داخل git نیستند

---

## اگر گیر کردی

| مشکل | کار تو |
|---|---|
| سرور Plane در MCP سبز نیست | Reload Window، چک `uvx`، چک توکن، چک `PLANE_BASE_URL` |
| Agent پروژهٔ اشتباه Plane را می‌بیند | `plane-tasks.mdc` را با UUID درست پر کن |
| قبل از push نایستاد | بگو طبق `git-policy.mdc` متوقف شود و تأیید بخواهد |
| از اول شروع کرد نه از وسط کار | بگو طبق `memory/progress.md` ادامه بدهد |
| نمی‌دانی Workflow کدام است | ببین `docs/README.md` بخش ۸ |

مستند کلی قالب: [`docs/README.md`](./README.md)  
راه‌اندازی فنی MCP/CLI: [`mcp/SETUP.md`](../mcp/SETUP.md)

---

## خلاصه یک جمله‌ای

**تو:** حساب‌ها، توکن‌ها، پر کردن AGENTS/بریف/Plane mapping، تأیید push، و merge نهایی.  
**Agent:** برنامه‌ریزی، طراحی، کدنویسی، تست، آماده‌سازی commit/PR، و Sync با Plane بعد از اینکه تو MCP را وصل کرده باشی.
