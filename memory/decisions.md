# Decision Log

Append every non-trivial architectural or process decision here.
Format:

```
## YYYY-MM-DD — <short title>
Decision: ...
Reasoning: ...
Made by: <agent/human>
```

---

## 2026-08-02 — Plane as preferred tracker; GitHub+GitLab; Persian comments
Decision: Use **Plane** (self-hosted `plane.ir-ma.ir`, workspace `iran_ma`)
as the preferred product backlog via MCP; keep Linear as optional.
Extend the git agent to create/connect remotes on **GitHub and/or GitLab**
(PR and MR). Require **Persian** docstrings/comments for non-obvious code
only (identifiers remain English).
Reasoning: Human org already runs Plane + documented MCP setup; dual git
hosts match real delivery; Persian comments improve readability for the
team without line-by-line noise.
Made by: human + template update

## 2026-08-27 — Coffee crawler: GitHub only, no Plane; search-discovery model
Decision: For **Iranian Coffee Price Crawler**, do **not** use Plane (or
Linear). Track work via `memory/roadmap.md` + `memory/progress.md` and
ship through **GitHub** PRs only. Interpret “crawl the whole internet” as
**systematic discovery of Iranian coffee sellers via web search + product
crawling**, not unbounded scraping of every host on earth. Proposed stack
for v1 (pending human confirm in `AGENTS.md`): Python 3.11+, CLI-first,
httpx/playwright as needed, pytest; Graphify required for agent context.
Reasoning: Human explicitly chose GitHub and rejected Plane; literal
whole-web crawl is infeasible and legally/fragile; discovery+seed adapters
still meets the goal of finding best Arabica/Robusta prices with links and
per-gram normalization.
Made by: human + roadmap
