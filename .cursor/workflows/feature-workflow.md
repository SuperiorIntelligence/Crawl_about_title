# Feature Workflow

Use this exact sequence for any new feature. Do not skip steps.

```
-1. Resume check     → check memory/progress.md for an in-progress task on
                        this workflow before starting (see
                        .cursor/rules/continuity.mdc); every step below
                        updates memory/progress.md before handing off
0. Scope check       → confirm this feature belongs to the Current Version
                        in memory/roadmap.md (see .cursor/rules/versioning.mdc)
(optional) Plane     → preferred: pull/create work item via plane agent
                        (see .cursor/agents/plane.md + plane-tasks.mdc)
(optional) Linear    → alternative tracker if Plane is not configured
Planner               → implementation plan
Architect             → design (API/DB/folders) — consult the Graphify
                        graph (.cursor/rules/graphify.mdc) instead of
                        reading the whole codebase to understand it
Backend and/or Frontend → implementation (Persian docstrings/comments
                        where useful — .cursor/rules/coding-style.mdc)
Tester                → tests written + passing
Reviewer              → review verdict
Security              → only if auth/secrets/payments/input-handling touched
Docs                  → docs updated (+ note "run graphify . --update" if
                        the change is structural)
Git (GitHub/GitLab)   → branch, commit, PR and/or MR opened
                        STOP — wait for human approval before push
Git                   → push + PR/MR ready for merge (human merges)
(optional) Plane/Linear → comment PR/MR link, move work item to In Review
```

## How to run this in Cursor
1. Open Cursor Chat/Composer in this repo.
2. Paste the feature request (or a Plane/Linear work item — see
   `.cursor/agents/plane.md` / `.cursor/agents/linear.md`).
3. Say: `"Act as the agents defined in .cursor/agents, follow .cursor/workflows/feature-workflow.md step by step for this task, and respect AGENTS.md and .cursor/rules."`
4. Let each step complete before moving to the next — review the output of
   each agent stage before telling Cursor to continue to the next one.
5. At the Git step, Cursor must stop before `git push`. Review the diff,
   then explicitly approve. Remotes may be GitHub, GitLab, or both.

## Stop Conditions
- Any agent hits ambiguity → stop and ask the human.
- The feature is not in the Current Version's scope (`memory/roadmap.md`) →
  stop and ask whether to pull it forward on purpose, per
  `.cursor/rules/versioning.mdc`.
- Reviewer verdict is "Request Changes" → loop back to Backend/Frontend.
- Security verdict is "Block" → loop back to Backend/Frontend, cannot
  proceed to Git step until resolved.
