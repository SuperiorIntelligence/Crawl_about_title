# Work Progress (Continuity)

## Active Task
Version: v1–v4 code complete
Feature/Bugfix title: Iranian Coffee Price Crawler
Source workflow: version-workflow (all versions implemented per human request)
Git branch: `feature/coffee-price-crawler`

### Step Status
| Step | Status |
|---|---|
| Plane | Skipped |
| Implementation v1–v4 | Done |
| Tester | Done (8 passed) |
| Graphify | Done (`graphify . --code-only`) |
| Reviewer | Pending human |
| GitHub commit/push/PR | Pending human approval |

### Resume Notes
- General search UI at `/` — POST `/api/search` with `{query}`.
- Demo button removed. Restart `python -m core.cli serve` (port 5000).
- Price parser fixed for Persian `٫` thousand separators.

## Recently Completed
```
- 2026-08-27 — Coffee crawler v1–v4 on feature/coffee-price-crawler; tests green
```
