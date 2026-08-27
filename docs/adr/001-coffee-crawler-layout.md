# ADR 001 — Coffee crawler package layout

Date: 2026-08-27  
Status: Accepted (human asked to deliver full v1–v4 project)

## Decision
Keep the AGENTS.md top-level layout (`src/api`, `src/services`, `src/models`,
`src/schemas`, `src/core`, `tests/`). Put crawler adapters under
`src/services/crawlers/` and static UI under `src/web/` (templates/static)
served by FastAPI — no separate frontend app for v4.

## Reasoning
Matches existing folder contract; one Python process for CLI + API + UI
keeps the first deliverable demable without inventing a second stack.
