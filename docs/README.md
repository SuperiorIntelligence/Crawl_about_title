# مستندات کامل cursor-ai-starter

این فایل راهنمای کامل استفاده از قالب Multi-Agent برای پروژه‌های Cursor است.
مخاطب: کسی که تازه این قالب را می‌بیند و می‌خواهد بداند هر فایل برای چیست،
چطور پروژه را راه‌اندازی کند، و چطور کار روزمره را جلو ببرد.

> **کارهای اجباری/دستی انسان (توکن، لاگین، تأیید push، پر کردن AGENTS و Plane):**  
> **[`HUMAN-SETUP.md`](./HUMAN-SETUP.md)** — اول این را بخوان اگر می‌خواهی بدانی خودت باید چه‌کار کنی.

> نسخهٔ خلاصه‌تر و نصب‌محور در ریشهٔ پروژه: [`README.md`](../README.md)

---

## فهرست

1. [این قالب چیست؟](#1-این-قالب-چیست)
2. [محدودیت واقعی Cursor (مهم)](#2-محدودیت-واقعی-cursor-مهم)
3. [ساختار پوشه‌ها و نقش هر فایل](#3-ساختار-پوشه‌ها-و-نقش-هر-فایل)
4. [نصب روی پروژهٔ جدید](#4-نصب-روی-پروژهٔ-جدید)
5. [راه‌اندازی اولیه (یک‌بار)](#5-راه‌اندازی-اولیه-یکبار)
6. [سه لایهٔ حافظهٔ پروژه](#6-سه-لایهٔ-حافظهٔ-پروژه)
7. [Agentها و مسئولیت‌ها](#7-agentها-و-مسئولیتها)
8. [Workflowها — کدام را کی اجرا کنی](#8-workflowها--کدام-را-کی-اجرا-کنی)
9. [چطور کار را شروع کنی (روزمره)](#9-چطور-کار-را-شروع-کنی-روزمره)
10. [نسخه‌بندی پروژه‌های بزرگ](#10-نسخه‌بندی-پروژه‌های-بزرگ)
11. [ادامه کار بعد از قطع Session](#11-ادامه-کار-بعد-از-قطع-session)
12. [GitHub، Branch و Pull Request](#12-github-branch-و-pull-request)
13. [Graphify (کاهش توکن و درک بهتر کد)](#13-graphify-کاهش-توکن-و-درک-بهتر-کد)
14. [Linear با MCP (اختیاری)](#14-linear-با-mcp-اختیاری)
15. [قوانین سخت (Rules)](#15-قوانین-سخت-rules)
16. [چک‌لیست سریع شروع](#16-چکلیست-سریع-شروع)
17. [عیب‌یابی رایج](#17-عیبیابی-رایج)

---

## 1. این قالب چیست؟

`cursor-ai-starter` یک **قالب فرآیند** است، نه یک اپلیکیشن آماده.

کاری که انجام می‌دهد:

- برای Cursor چند **نقش (Agent Persona)** تعریف می‌کند: Planner، Architect،
  Backend، Frontend، Tester، Reviewer، Security، Docs، GitHub، Roadmap، Linear.
- ترتیب کار را با **Workflow** مشخص می‌کند (Feature / Bugfix / Release / Version).
- با **Rules** قوانین سخت را همیشه به Context اضافه می‌کند (Git، نسخه‌بندی، Graphify، Continuity).
- با فایل‌های `memory/` وضعیت پروژه را بین Sessionهای مختلف زنده نگه می‌دارد.

هدف نهایی: روی پروژه‌های واقعی و حتی بزرگ، Cursor کنترل‌شده، قابل‌بازبینی و قابل‌ادامه کار کند —
نه اینکه یک‌جا کل پروژه را «حدس بزند» و خراب کند.

---

## 2. محدودیت واقعی Cursor (مهم)

Cursor برخلاف بعضی ابزارها، **به‌صورت خودکار بین Agentها سوییچ نمی‌کند**.

| نوع فایل | رفتار واقعی در Cursor |
|---|---|
| `.cursor/rules/*.mdc` با `alwaysApply: true` | خودکار همیشه به Context اضافه می‌شود |
| `.cursor/agents/*.md` | فایل Prompt است؛ باید با `@` یا دستور متنی به آن ارجاع بدهی |
| `.cursor/workflows/*.md` | همین‌طور؛ تو می‌گویی کدام Workflow را قدم‌به‌قدم دنبال کند |

پس «نقش عوض کردن» را خودت با یک جملهٔ شروع مثل این کنترل می‌کنی:

```text
Act as the agents defined in .cursor/agents, follow
.cursor/workflows/feature-workflow.md step by step,
and respect AGENTS.md and .cursor/rules.
```

بعد از هر مرحله خروجی را بخوان و بگو `ادامه بده` یا اصلاح بخواه.

---

## 3. ساختار پوشه‌ها و نقش هر فایل

```text
پروژه/
├── AGENTS.md                 مغز پروژه — استک، قوانین، لیست Agentها
├── README.md                 خلاصهٔ نصب و معرفی قالب
├── .gitignore.template       پیشنهاد Ignore برای Graphify و اسرار
│
├── .cursor/
│   ├── rules/                قوانین همیشه‌فعال (native Cursor)
│   │   ├── project.mdc
│   │   ├── git-policy.mdc
│   │   ├── coding-style.mdc
│   │   ├── versioning.mdc
│   │   ├── graphify.mdc
│   │   └── continuity.mdc
│   ├── agents/               تعریف نقش هر Agent
│   │   ├── roadmap.md
│   │   ├── planner.md
│   │   ├── architect.md
│   │   ├── backend.md
│   │   ├── frontend.md
│   │   ├── tester.md
│   │   ├── reviewer.md
│   │   ├── security.md
│   │   ├── docs.md
│   │   ├── github.md
│   │   └── linear.md
│   └── workflows/            ترتیب مراحل کار
│       ├── version-workflow.md
│       ├── feature-workflow.md
│       ├── bugfix-workflow.md
│       └── release-workflow.md
│
├── prompts/                  قالب‌هایی که خودت پر می‌کنی
│   ├── project-brief-template.md
│   ├── feature-template.md
│   ├── bug-template.md
│   └── linear-sync-template.md
│
├── memory/                   حافظهٔ زندهٔ پروژه بین Sessionها
│   ├── roadmap.md            نسخه‌ها + Current Version
│   ├── progress.md           وضعیت دقیق مرحلهٔ جاری
│   └── decisions.md          لاگ تصمیم‌های معماری
│
├── mcp/
│   └── SETUP.md              راهنمای Plane / Linear / Graphify / git CLIs
│
├── docs/
│   └── README.md             همین فایل
│
└── graphify-out/             بعد از اجرای graphify . ساخته می‌شود
    ├── graph.json
    ├── GRAPH_REPORT.md
    └── graph.html
```

### نقش فایل‌های کلیدی (خلاصه)

| فایل | کی پر می‌شود؟ | کی می‌خواند؟ |
|---|---|---|
| `AGENTS.md` | تو، یک‌بار در شروع پروژه | همهٔ Agentها قبل از هر کار |
| `prompts/project-brief-template.md` | تو، برای پروژهٔ بزرگ | Agent `roadmap` |
| `prompts/feature-template.md` | تو، برای هر Feature | Agent `planner` |
| `memory/roadmap.md` | Agent `roadmap` | همه، برای Scope نسخه |
| `memory/progress.md` | همهٔ Agentها بعد از هر مرحله | همه، در شروع هر Session |
| `memory/decisions.md` | Architect / انسان هنگام تصمیم مهم | Planner / Architect |
| `.cursor/rules/*` | از قبل آماده | Cursor خودکار |

---

## 4. نصب روی پروژهٔ جدید

### ویندوز (PowerShell)

```powershell
$src = "d:\WorkMe\Creat_project_use_cursor"   # مسیر این قالب
$dst = "d:\WorkMe\My-New-Project"             # مسیر پروژهٔ جدید

New-Item -ItemType Directory -Path $dst -Force | Out-Null
Set-Location $dst

Copy-Item "$src\.cursor" ".\.cursor" -Recurse
Copy-Item "$src\AGENTS.md" ".\AGENTS.md"
Copy-Item "$src\prompts" ".\prompts" -Recurse
Copy-Item "$src\memory" ".\memory" -Recurse
Copy-Item "$src\mcp" ".\mcp" -Recurse
Copy-Item "$src\.gitignore.template" ".\.gitignore.template"
# اختیاری: Copy-Item "$src\docs" ".\docs" -Recurse
```

### چه چیزهایی را حتماً کپی کن

- `.cursor\` (کل پوشه)
- `AGENTS.md`
- `prompts\`
- `memory\`
- `mcp\`
- `.gitignore.template`

`README.md` ریشه و `docs\` اختیاری‌اند (برای انسان)، ولی برای کار Agentها ضروری نیستند.

بعد: در Cursor برو **File → Open Folder** و پوشهٔ پروژهٔ جدید را باز کن.

---

## 5. راه‌اندازی اولیه (یک‌بار)

### ۵.۱ پر کردن `AGENTS.md`

بخش‌های `<fill in>` را با استک واقعی پر کن، مثلاً:

```text
Backend: FastAPI + SQLAlchemy + PostgreSQL
Frontend: React + Vite + TailwindCSS
Infra: Docker, docker-compose, GitHub Actions
Package manager: uv (backend) / pnpm (frontend)
```

بدون این، Agentها استک را حدس می‌زنند.

### ۵.۲ آماده‌سازی GitHub (اگر می‌خواهی PR داشته باشی)

قالب خودش Repo روی GitHub نمی‌سازد. یک‌بار دستی:

1. در github.com یک Repository خالی بساز.
2. در پوشهٔ پروژه:

```powershell
git init
git remote add origin https://github.com/USERNAME/REPO.git
git add .
git commit -m "chore: initial commit from cursor-ai-starter"
git branch -M main
git push -u origin main
```

از این به بعد `origin` همان یک آدرس ثابت است. برای هر Feature فقط **Branch جدید** ساخته می‌شود، نه origin جدید.

### ۵.۳ Graphify (پیشنهادی برای پروژهٔ واقعی)

```powershell
winget install astral-sh.uv
uv tool install graphifyy
graphify cursor install
# بعد از اینکه کمی کد واقعی نوشته شد:
graphify .
```

جزئیات بیشتر: [`mcp/SETUP.md`](../mcp/SETUP.md)

### ۵.۴ Linear (کاملاً اختیاری)

اگر تیم نداری و Taskها را خودت در `prompts/` می‌نویسی، نیازی به Linear نیست.
اگر خواستی وصل کنی: همان `mcp/SETUP.md`.

---

## 6. سه لایهٔ حافظهٔ پروژه

این سه مکانیزم مکمل هم هستند:

| لایه | فایل | چه چیزی را نگه می‌دارد |
|---|---|---|
| نسخه (Version) | `memory/roadmap.md` | v1/v2/...، Scope، Current Version |
| مرحلهٔ جاری (Task/Step) | `memory/progress.md` | کدام Workflow، کدام Agent، کدام Branch |
| ساختار کد | `graphify-out/` | نقشهٔ ارتباط فایل‌ها/توابع/کلاس‌ها |

تصمیم‌های معماری هم جداگانه در `memory/decisions.md` لاگ می‌شوند.

---

## 7. Agentها و مسئولیت‌ها

| Agent | کار | کد می‌نویسد؟ |
|---|---|---|
| **Roadmap** | پروژهٔ بزرگ را به نسخه‌ها می‌شکند | خیر (فقط `memory/roadmap.md`) |
| **Planner** | پلن پیاده‌سازی | خیر |
| **Architect** | طراحی API/DB/پوشه‌ها | خیر |
| **Backend** | پیاده‌سازی سرور | بله |
| **Frontend** | پیاده‌سازی UI | بله |
| **Tester** | تست می‌نویسد و اجرا می‌کند | فقط تست |
| **Reviewer** | بررسی کد، فقط گزارش | خیر |
| **Security** | بررسی امنیتی | خیر |
| **Docs** | به‌روزرسانی مستندات | بله (docs) |
| **GitHub** | ساخت/اتصال ریپو روی GitHub و/یا GitLab، branch، push، PR/MR | خیر (فقط git/CLI) |
| **Plane** | تسک‌ترکر ترجیحی — کشیدن/به‌روزکردن work item از Plane MCP | خیر |
| **Linear** | جایگزین اختیاری Plane | خیر |

قانون کلی: هر Agent فقط داخل Scope خودش کار می‌کند. اگر چیزی مبهم بود، حدس نمی‌زند — از تو می‌پرسد.

---

## 8. Workflowها — کدام را کی اجرا کنی

| Workflow | کی استفاده شود |
|---|---|
| `version-workflow.md` | شروع پروژهٔ بزرگ / چندنسخه‌ای |
| `feature-workflow.md` | هر Feature داخل یک نسخه (یا پروژهٔ کوچک) |
| `bugfix-workflow.md` | باگ — سبک‌تر از Feature |
| `release-workflow.md` | بستن یک نسخه و آماده‌سازی Release |

### ترتیب معمول Feature

```text
Resume check (memory/progress.md)
→ Scope check (Current Version)
→ (اختیاری، ترجیحی) Plane
→ (اختیاری) Linear
→ Planner
→ Architect  (+ Graphify query)
→ Backend و/یا Frontend  (کامنت/Docstring فارسی در جاهای مفید)
→ Tester
→ Reviewer
→ Security (اگر auth/secrets/payments باشد)
→ Docs
→ Git (GitHub و/یا GitLab)  → STOP قبل از push → بعد از تأیید تو: push + PR/MR
→ (اختیاری) Plane/Linear sync
```

هر مرحله باید `memory/progress.md` را به‌روز کند.

---

## 8.1 GitHub و GitLab — ساخت/اتصال پروژه

Agent `github` (فایل `.cursor/agents/github.md`) هر دو پلتفرم را پشتیبانی می‌کند.

1. یک‌بار CLI را نصب و لاگین کن: `gh auth login` و/یا `glab auth login`
2. قالب `prompts/remote-setup-template.md` را پر کن (platform: github / gitlab / both)
3. در Chat از Agent بخواه ریپو را بسازد/وصل کند — **قبل از اولین push می‌ایستد**
4. GitHub → Pull Request ؛ GitLab → Merge Request ؛ قوانین ایمنی یکی است

جزئیات: `mcp/SETUP.md` بخش ۰ و `.cursor/rules/git-policy.mdc`

---

## 8.2 Plane (تسک‌ترکر — گاهی اشتباهی «Plain» گفته می‌شود)

محصول واقعی **Plane** است (`https://plane.ir-ma.ir`، workspace نمونه: `iran_ma`).

- Agent: `.cursor/agents/plane.md`
- Rule: `.cursor/rules/plane-tasks.mdc` (UUID پروژه/ماژول را خودت پر کن)
- پرامت‌ها: `prompts/plane-sync-template.md`
- راه‌اندازی MCP: `mcp/SETUP.md` بخش ۱

با Plane می‌توانی ببینی چه تسکی مانده، در چه state است، و Agent وضعیت را بعد از PR/MR به‌روز کند.

---

## 8.3 کامنت فارسی در کد

طبق `.cursor/rules/coding-style.mdc` و `AGENTS.md` §3:

- Docstring/JSDoc و توضیح‌های غیرواضح → **فارسی**
- نام تابع/متغیر/کلاس → **انگلیسی**
- روی هر خط کامنت نگذار؛ فقط جاهای مفید

---

## 9. چطور کار را شروع کنی (روزمره)

### الف) پروژهٔ کوچک / یک Feature

1. `prompts/feature-template.md` را پر کن.
2. در Chat بگو:

```text
Act as the agents defined in .cursor/agents, follow
.cursor/workflows/feature-workflow.md step by step for the request below,
and respect AGENTS.md and .cursor/rules.

<متن feature-template پر شده>
```

3. بعد از هر مرحله: بخوان → بگو `ادامه بده` یا اصلاح بخواه.
4. در مرحلهٔ GitHub قبل از push تأیید بده.

### ب) پروژهٔ بزرگ / چندنسخه‌ای

1. `prompts/project-brief-template.md` را با **کل ایده** پر کن
   (لازم نیست خودت نسخه‌بندی کنی؛ Roadmap این کار را می‌کند).
2. در Chat بگو:

```text
Act as the agents defined in .cursor/agents, starting with roadmap,
follow .cursor/workflows/version-workflow.md step by step for the
project below, and respect AGENTS.md and .cursor/rules.

<متن project-brief پر شده>
```

3. خروجی `memory/roadmap.md` را **قبل از هر کدنویسی** بررسی و تأیید کن.
4. بعد برای هر Feature داخل نسخهٔ جاری، همان مسیر Feature Workflow را برو.
5. وقتی Scope نسخه تمام شد → `release-workflow.md`.

### ج) ادامه بعد از قطع کار

فقط بنویس:

```text
ادامه بده
```

Agent باید اول `memory/progress.md` را بخواند و از همان مرحلهٔ ثبت‌شده ادامه دهد.

---

## 10. نسخه‌بندی پروژه‌های بزرگ

### چرا؟

اگر کل پروژهٔ بزرگ را یک‌جا به Cursor بدهی:

- Context پر می‌شود
- تغییرات ناهماهنگ زیاد می‌شود
- Review واقعی سخت می‌شود

راه‌حل: شکستن به نسخه‌های کوچک و قابل‌نمایش (`v1`, `v2`, ...).

### قوانین سخت (`.cursor/rules/versioning.mdc`)

1. فقط **Current Version** پیاده‌سازی می‌شود.
2. درخواست مال نسخهٔ بعدی؟ → متوقف شو و از انسان بپرس.
3. نسخه فقط بعد از `release-workflow` + تأیید انسان «Released» می‌شود.
4. نشانگر Current Version را هیچ Agentی خودسر جلو نمی‌برد.
5. یک Branch/PR نباید Scope دو نسخه را قاطی کند.

### نقش تو

- بریف را بنویس
- تقسیم‌بندی Roadmap را تأیید کن
- بگو کی به نسخهٔ بعد برویم

---

## 11. ادامه کار بعد از قطع Session

فایل زنده: `memory/progress.md`  
قانون: `.cursor/rules/continuity.mdc` (`alwaysApply: true`)

داخل `progress.md` می‌بینی:

- عنوان Feature/Bugfix
- Workflow در حال اجرا
- نام Branch
- چک‌لیست مراحل (Done / In Progress / Pending / Skipped)
- Resume Notes (آخرین کار + قدم بعدی)

اگر فایل با واقعیت Repo تناقض داشت، Agent باید بپرسد نه حدس بزند.
وقتی کار کامل merge شد، بخش Active پاک می‌شود و یک خط به Recently Completed اضافه می‌شود.

---

## 12. GitHub، Branch و Pull Request

### مفاهیم (با هم قاطی نکن)

| مفهوم | معنی | چند بار؟ |
|---|---|---|
| `origin` | آدرس Remote گیت‌هاب | یک‌بار در کل پروژه |
| `main` | شاخهٔ پایدار تحویل‌دادنی | همیشه یکی |
| `feature/...` یا `fix/...` | شاخهٔ موقت برای یک کار | برای هر Feature/Bug یک‌بار |

### رفتار اجباری Agent GitHub

طبق `.cursor/rules/git-policy.mdc`:

1. مستقیم روی `main` کار نمی‌کند.
2. Branch می‌سازد → commit می‌کند.
3. **قبل از `git push` می‌ایستد و تأیید می‌خواهد.**
4. بعد از تأیید: push + باز کردن PR.
5. **خودش PR را merge نمی‌کند** — merge کار انسان است.

### جریان ساده

```text
main ──●───────────────●  (بعد از merge دستی تو)
        \             /
         feature/x ──●── PR باز شد، منتظر تو
```

---

## 13. Graphify (کاهش توکن و درک بهتر کد)

منبع: [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify)

### ایده

به‌جای اینکه Agent برای هر سؤال ۲۰ تا ۶۰ فایل خام باز کند، یک Knowledge Graph محلی
از پروژه ساخته می‌شود و Agent اول از آن Query می‌گیرد.

### خروجی

```text
graphify-out/
├── graph.json        دادهٔ کامل گراف
├── GRAPH_REPORT.md   خلاصه برای Agentها (god nodes، communities، ...)
└── graph.html        نمای بصری برای انسان
```

### دستورات مهم

```powershell
graphify .              # ساخت اولیه
graphify . --update     # بعد از تغییر ساختاری
graphify query "..."    # سؤال از گراف
graphify explain "Name"
graphify path "A" "B"
```

قانون `.cursor/rules/graphify.mdc` همهٔ Agentها را مجبور می‌کند قبل از Grep/خواندن زیاد فایل،
اول از گراف استفاده کنند. بعد از تغییرات ساختاری باید گراف را تازه کنی.

---

## 14. Plane با MCP (ترجیحی) و Linear (اختیاری)

نام درست محصول تسک‌ترکر: **Plane** (گاهی اشتباهی Plain گفته می‌شود).

### Plane — کارهایی که خودت باید یک‌بار انجام بدهی
1. `uv` را نصب کن تا `uvx` در PATH باشد.
2. از Plane یک Personal Access Token بگیر.
3. در `%USERPROFILE%\.cursor\mcp.json` سرور `plane` را طبق `mcp/SETUP.md` اضافه کن
   (`PLANE_BASE_URL=https://plane.ir-ma.ir`, `PLANE_WORKSPACE_SLUG=iran_ma`).
4. Cursor را Reload کن و در Settings → MCP وصل‌بودن `plane` را ببین.
5. فایل `.cursor/rules/plane-tasks.mdc` را باز کن و `project_id` / نام پروژه /
   UUID ماژول‌ها را برای **همین ریپو** پر کن.

بعد از آن Agent `plane` می‌تواند work item بکشد، وضعیت را عوض کند و لیست
کارهای مانده را نشان بدهد (`prompts/plane-sync-template.md`).

### Linear
فقط اگر هنوز از Linear استفاده می‌کنی لازم است — همان مراحل قبلی OAuth در
`mcp/SETUP.md`. اگر فقط Plane داری، Linear را نادیده بگیر.

---

## 15. قوانین سخت (Rules)

این فایل‌ها با `alwaysApply: true` همیشه فعال‌اند:

| Rule | کار |
|---|---|
| `project.mdc` | اول `AGENTS.md` را بخوان؛ داخل Scope بمان |
| `git-policy.mdc` | بدون تأیید، push/merge/حذف Branch ممنوع |
| `versioning.mdc` | فقط Current Version |
| `graphify.mdc` | اول گراف، بعد فایل خام |
| `continuity.mdc` | اول `progress.md`، بعد هر کار جدید |
| `coding-style.mdc` | سبک کدنویسی روی فایل‌های کد |

تغییر این فایل‌ها فقط با درخواست صریح انسان مجاز است.

---

## 16. چک‌لیست سریع شروع

- [ ] پوشه‌های لازم از قالب را به پروژهٔ جدید کپی کردم
- [ ] پروژه را در Cursor با Open Folder باز کردم
- [ ] `AGENTS.md` را با استک واقعی پر کردم
- [ ] (اختیاری) Git remote را به Repo خالی وصل کردم
- [ ] (اختیاری) Graphify را نصب و یک‌بار اجرا کردم
- [ ] برای پروژهٔ بزرگ: `project-brief-template.md` را پر کردم و `version-workflow` را شروع کردم
- [ ] برای کار کوچک: `feature-template.md` را پر کردم و `feature-workflow` را شروع کردم
- [ ] بعد از هر مرحله خروجی را خواندم و `ادامه بده` گفتم
- [ ] قبل از push تأیید دادم
- [ ] خودم PR را در GitHub merge کردم

---

## 17. عیب‌یابی رایج

### Agent از اول شروع کرد، نه از جایی که قطع شده بود
- `memory/progress.md` را باز کن؛ آیا مرحلهٔ درست ثبت شده؟
- در چت جدید صریحاً بگو: «طبق `memory/progress.md` ادامه بده، از اول شروع نکن.»

### قبل از push نایستاد
- به `.cursor/rules/git-policy.mdc` ارجاع بده و بگو: «طبق git-policy متوقف شو و تأیید بخواه.»

### چیزهایی از نسخهٔ بعدی را ساخت
- بگو متوقف شود و `memory/roadmap.md` را چک کند؛ فقط Current Version مجاز است.

### Graphify چیزی پیدا نمی‌کند
- اول `graphify .` را اجرا کرده باشی؟
- بعد از تغییرات بزرگ: `graphify . --update` یا در صورت نیاز `graphify . --force`.

### Linear کار نمی‌کند
- اختیاری است. اگر وصل نیست، Task را دستی در `feature-template.md` بنویس.

### PowerShell دستور `/graphify .` را اشتباه می‌فهمد
- از `graphify .` بدون اسلش ابتدایی استفاده کن.

---

## پیام‌های آمادهٔ کپی‌پیست

### شروع پروژهٔ بزرگ
```text
Act as the agents defined in .cursor/agents, starting with roadmap,
follow .cursor/workflows/version-workflow.md step by step for the
project below, and respect AGENTS.md and .cursor/rules.

@prompts/project-brief-template.md
```

### شروع یک Feature
```text
Act as the agents defined in .cursor/agents, follow
.cursor/workflows/feature-workflow.md step by step for the request below,
and respect AGENTS.md and .cursor/rules.

@prompts/feature-template.md
```

### شروع Bugfix
```text
Act as the agents defined in .cursor/agents, follow
.cursor/workflows/bugfix-workflow.md step by step for the bug below,
and respect AGENTS.md and .cursor/rules.

@prompts/bug-template.md
```

### ادامه بعد از وقفه
```text
طبق memory/progress.md و .cursor/rules/continuity.mdc از همان مرحلهٔ ثبت‌شده ادامه بده.
از اول شروع نکن مگر اینکه خودم بگویم.
```

### بستن یک نسخه
```text
Act as the agents defined in .cursor/agents, follow
.cursor/workflows/release-workflow.md step by step for version vX,
and respect AGENTS.md and .cursor/rules.
```

---

## جمع‌بندی یک‌خطی

1. قالب را کپی کن → `AGENTS.md` را پر کن.  
2. ایدهٔ بزرگ را در `project-brief-template.md` بنویس → Roadmap نسخه‌بندی کند.  
3. هر Feature را با `feature-workflow` جلو ببر.  
4. قبل از push تأیید بده؛ خودت PR را merge کن.  
5. Graphify را بعد از کد واقعی بساز و بعد از تغییرات ساختاری آپدیت کن.  
6. اگر کار قطع شد، فقط بگو «ادامه بده» — `memory/progress.md` مسیر را نگه می‌دارد.

اگر جایی از این مستند با رفتار واقعی فایل‌های قالب تناقض داشت، فایل‌های داخل
`.cursor/` و `AGENTS.md` منبع حقیقت‌اند؛ این سند فقط راهنمای انسان است.
