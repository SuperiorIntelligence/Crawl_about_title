# AGENTS.md — Project Brain

Every agent MUST read this file before doing any work. It is the single
source of truth for architecture, style, and process rules on this project.

## 1. Tech Stack
- Backend: `Python 3.11+ / FastAPI + httpx + BeautifulSoup + Pydantic`
- Frontend: `Jinja2 templates served by FastAPI (no separate SPA)`
- Infra: `local only (optional Docker later)`
- Package manager: `pip` (`requirements.txt`)
- Git hosting: `github`
- Primary remote name: `origin` (GitHub)
- Plane project (if using Plane): `n/a — not used for this project`

## 2. Folder Structure
```
src/
  api/         # route handlers
  services/    # business logic
  models/      # ORM / data models
  schemas/     # request/response validation
  core/        # config, security, startup
tests/
docs/
graphify-out/  # Graphify knowledge graph (graph.json, GRAPH_REPORT.md) — see §11
```
Agents must not invent a different top-level layout. If a change to the
structure is needed, the **architect** agent proposes it in `docs/adr/` and
waits for human approval before any other agent adopts it.

## 3. Coding Style
- Language conventions: `PEP8 + ruff` (Python)
- Naming: `snake_case` for Python, `camelCase` for JS/TS, `PascalCase` for classes/components.
- Every public function/endpoint needs a **Persian** docstring/JSDoc
  (purpose, params, return). Identifiers stay English.
- Add Persian inline comments only for non-obvious logic — never comment
  every line. See `.cursor/rules/coding-style.mdc`.
- No commented-out dead code in commits.

## 4. Branch Strategy
- `main` — always deployable, protected.
- `feature/<short-name>` — one feature per branch.
- `fix/<short-name>` — bug fixes.
- `release/<version>` — release stabilization.
- Hosting may be **GitHub**, **GitLab**, or **both** — see Git hosting in
  §1 and `prompts/remote-setup-template.md`. GitHub uses Pull Requests;
  GitLab uses Merge Requests. Same safety rules apply to both.

## 5. Git Policy (hard rule, applies to every agent)
- Never push directly to `main` / `master`.
- Always work on a feature/fix branch.
- Always open a Pull Request (GitHub) and/or Merge Request (GitLab)
  instead of merging directly.
- Always **stop and ask for human approval** before: `git push`, `merge`,
  `delete branch`, creating remotes/repos (`gh`/`glab`), or any destructive
  command.
- Commit messages follow Conventional Commits: `feat:`, `fix:`, `docs:`,
  `refactor:`, `test:`, `chore:`.
- Details: `.cursor/rules/git-policy.mdc` and `.cursor/agents/github.md`
  (handles both GitHub and GitLab).

## 6. Review Policy
- No PR is merged without the **reviewer** agent's checklist passing.
- Security-sensitive code (auth, payments, secrets) additionally requires the **security** agent's sign-off.

## 7. Definition of Done
A task is only "done" when:
1. Code implements the acceptance criteria from the Plane work item
   (preferred) or Linear issue / filled prompt template.
2. Tests exist and pass.
3. Docs are updated (`docs/` or README).
4. Reviewer has approved.
5. PR (GitHub) and/or MR (GitLab) is opened (not merged) and waiting for
   human approval.

## 8. Agents Available in This Project
| Agent | File | Responsibility |
|---|---|---|
| Roadmap | `.cursor/agents/roadmap.md` | Slices a large project brief into shippable versions (v1, v2, ...) |
| Planner | `.cursor/agents/planner.md` | Turns a request into an implementation plan |
| Architect | `.cursor/agents/architect.md` | System/API/DB design, no code |
| Backend | `.cursor/agents/backend.md` | Server-side implementation |
| Frontend | `.cursor/agents/frontend.md` | Client-side implementation |
| Tester | `.cursor/agents/tester.md` | Writes/updates tests |
| Reviewer | `.cursor/agents/reviewer.md` | Code review, no edits |
| Security | `.cursor/agents/security.md` | Security review |
| Docs | `.cursor/agents/docs.md` | Documentation |
| GitHub | `.cursor/agents/github.md` | Git remotes on GitHub and/or GitLab (repo create, branch, PR/MR) |
| Plane | `.cursor/agents/plane.md` | Preferred task tracker via Plane MCP (pull/push work items) |
| Linear | `.cursor/agents/linear.md` | Optional alternative tracker via Linear MCP |

## 9. Workflows
See `.cursor/workflows/`. Every feature/bugfix/release MUST follow the
matching workflow file step by step, in order. No skipping steps. For a
large project, `version-workflow.md` is the top-level loop that sequences
`feature-workflow.md` / `bugfix-workflow.md` / `release-workflow.md` across
versions — see §11.

## 10. Decision Log
Any non-trivial architectural decision must be appended to
`memory/decisions.md` with date, decision, and reasoning.

## 11. Versioning Strategy (for large projects)
Large projects are broken into shippable **versions** so Cursor works on a
scope it can reliably hold in context, instead of the whole project at once.
This is a hard rule — see `.cursor/rules/versioning.mdc`.

- `memory/roadmap.md` is the source of truth: it lists all versions, each
  one's scope/acceptance criteria, and a **Current Version** pointer.
- Only the Current Version may be implemented right now. Anything else
  gets flagged, not silently built.
- `.cursor/agents/roadmap.md` (the **Roadmap** agent) creates/updates this
  file — start any large project by filling in
  `prompts/project-brief-template.md` and running
  `.cursor/workflows/version-workflow.md`.
- A version only becomes "Released" after `release-workflow.md` completes
  and the human explicitly approves — only then does the Roadmap agent move
  the Current Version pointer forward.
- Small projects can skip this entirely and just use `feature-workflow.md`
  directly — `roadmap` will say so explicitly if one version is enough.

## 12. Knowledge Graph (Graphify) — token efficiency
This project uses [Graphify](https://github.com/Graphify-Labs/graphify) to
maintain a local, deterministic knowledge graph of the codebase in
`graphify-out/` (git-tracked, except `cost.json`). This is a hard rule —
see `.cursor/rules/graphify.mdc`.

- Every agent must prefer `graphify query "..."` / `graphify explain "..."`
  / `graphify path "A" "B"` (or the equivalent MCP tools, if the Graphify
  MCP server is configured — see `mcp/SETUP.md`) over grepping/reading raw
  files for "how is this connected" questions.
- `graphify-out/GRAPH_REPORT.md` is the first thing to read for a broad
  architecture overview (god nodes, communities, surprising connections).
- Rebuild with `graphify . --update` after structural changes (new/removed
  files, renamed public APIs) — cheap, local, AST-only, no LLM cost for
  code.
- Why this matters: on a large repo, an agent that opens 15–60 files per
  prompt to "figure out the codebase" burns tens of thousands of tokens on
  retrieval alone. A ~10–15k-token `GRAPH_REPORT.md` plus 2-3 scoped
  `graphify query` calls replaces most of that, and keeps Cursor's
  understanding of the *whole* project consistent across sessions instead
  of re-derived (and sometimes re-guessed) every time.

## 13. MCP Servers Used in This Project
Configured in user-global and/or project `.cursor/mcp.json` (see
`mcp/SETUP.md` and `.cursor/mcp.json.example`):
- **Plane** (`uvx plane-mcp-server`, preferred task tracker) — only the
  `plane` agent calls Plane tools directly. Instance example from org
  docs: workspace `iran_ma`, base URL `https://plane.ir-ma.ir`. Keep the
  API key in env / local mcp.json — never commit it.
- **Linear** (`https://mcp.linear.app/mcp`) — optional alternative issue
  tracking. Only the `linear` agent calls Linear tools directly.
- **Graphify** (optional, `python -m graphify.serve graphify-out/graph.json`)
  — exposes `query_graph` / `get_node` / `get_neighbors` / `shortest_path`
  as MCP tools, as an alternative to shelling out to the `graphify` CLI.

Add any project-specific MCP server here as it's introduced, with a one-line
note on which agent(s) are allowed to use it.

## 14. Resuming Work Across Sessions (Continuity)
Coding tasks here can span multiple Cursor sessions — the human may close
Cursor mid-task, or start a fresh chat days later. This is a hard rule —
see `.cursor/rules/continuity.mdc`.

- `memory/progress.md` is the source of truth for in-flight task/step
  state: which workflow is running, which agent/step is current, the git
  branch, a step-status checklist, and free-text resume notes.
- `.cursor/rules/continuity.mdc` is the hard rule that keeps it updated —
  every agent reads it first thing in any session (right after this file)
  and updates it at every handoff, including right before a STOP point.
- Why this matters: on a multi-day task, or a task picked back up in a
  brand-new chat, nothing should be lost or need re-explaining — the next
  session (any agent persona) should be able to read `memory/progress.md`
  and continue from the exact step where the previous session stopped,
  instead of restarting the workflow or guessing at prior state.
- This complements, but does not replace, `memory/roadmap.md` (§11,
  version-level state) and `graphify-out/` (§12, codebase-structure state)
  — three sibling mechanisms, each keeping a different kind of context
  small and current across sessions.
