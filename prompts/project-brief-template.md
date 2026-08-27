# Project Brief Template (for the Roadmap agent)

Fill this in once, at the start of a large project — before writing any
code. This is the input to `.cursor/agents/roadmap.md` /
`.cursor/workflows/version-workflow.md`. Do NOT use this for a single
feature — use `feature-template.md` for that.

```
Project Name:

Vision (1-2 paragraphs, plain language):


Primary Users:


Must-Have Capabilities (the whole project, not one feature):
  -
  -
  -

Nice-to-Have / Later Capabilities:
  -
  -

Known Constraints:
  - Tech stack (or "no preference yet"):
  - Timeline pressure (or "none"):
  - Team size / who reviews PRs:
  - Anything that must NOT change (legacy system, external contract, etc.):

Definition of "v1 is demoable":
  (what's the smallest end-to-end slice a stakeholder could see working?)

Linear Workspace/Team (if using Linear):
Plane workspace/project (if using Plane — preferred):
Git hosting for this project (github | gitlab | both):
```

Then say to Cursor:
> Act as the agents defined in `.cursor/agents`, starting with `roadmap`,
> follow `.cursor/workflows/version-workflow.md` step by step for the
> project below, and respect `AGENTS.md` and `.cursor/rules`.
>
> <پروژه‌بریف پر شده>

## What happens next
1. `roadmap` reads this brief and writes `memory/roadmap.md`: a list of
   versions (v1, v2, v3, ...), each with a one-sentence goal, scope, and
   acceptance criteria — ordered so each version only depends on earlier
   ones.
2. Review the version slicing before anything else happens. This is the
   single most important checkpoint — everything downstream inherits it.
3. Once approved, Cursor works through the **Current Version** only, one
   feature at a time via `feature-workflow.md`, until that version is
   released (`release-workflow.md`) — then `roadmap` moves the pointer to
   the next version.
4. If your project is small, `roadmap` will say a single version is enough
   — you're not forced into artificial versioning.
