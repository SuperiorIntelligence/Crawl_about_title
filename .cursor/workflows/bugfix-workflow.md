# Bugfix Workflow

Lighter-weight than the feature workflow — no full architecture step unless
the bug reveals a design flaw.

```
Resume check → check memory/progress.md for an in-progress task on this
             workflow before starting (see .cursor/rules/continuity.mdc);
             every step below updates memory/progress.md before handing off
(optional) Plane → find/create work item for the bug (preferred tracker)
Planner    → root cause + minimal fix plan (use Graphify — `graphify query`/
             `graphify explain` — to trace the bug's blast radius before
             guessing which files are involved)
Backend/Frontend → fix (Persian comments only where useful)
Tester     → regression test added (reproduces the bug, then passes)
Reviewer   → review verdict
Git (GitHub/GitLab) → branch (fix/<name>), commit, PR and/or MR opened
             STOP — wait for human approval
(optional) Plane/Linear → comment the PR/MR link, move to In Review
```

## Notes
- If the Planner determines the bug requires an architectural change, escalate
  to the full `feature-workflow.md` (insert an Architect step).
- The regression test must fail on the old code and pass on the fix — verify
  this before handing off to Reviewer.
- A bugfix is not exempt from `.cursor/rules/versioning.mdc`: if fixing it
  properly requires touching a later version's not-yet-built scope, stop and
  ask the human instead of building ahead of the roadmap.
