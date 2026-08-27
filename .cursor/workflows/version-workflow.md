# Version Workflow (master loop for large projects)

This is the top-level loop that wraps `feature-workflow.md` /
`bugfix-workflow.md` / `release-workflow.md` so a large project gets built
one small, reviewable version at a time instead of all at once. See
`.cursor/rules/versioning.mdc` for the hard rules this enforces.

```
Resume check → check memory/progress.md for an in-progress task before
             starting anything (see .cursor/rules/continuity.mdc); every
             step in this loop, and in the workflows it wraps, updates
             memory/progress.md before handing off
Roadmap    → (first run only) slice the project brief into versions,
             write memory/roadmap.md, set Current Version = v1
             STOP — human reviews/approves the version slicing

┌─ per version (repeat for Current Version only) ───────────────────────┐
│ (optional) Plane  → pull/confirm work items for this version's scope  │
│ (optional) Linear → alternative if Plane is not configured            │
│ For each feature in the version's scope:                              │
│   → run feature-workflow.md fully (through PR/MR + human merge)       │
│ For each bug found along the way:                                     │
│   → run bugfix-workflow.md fully                                      │
│ Once every feature/bug in scope is merged:                            │
│   → run release-workflow.md for this version                         │
│   → Roadmap marks the version "Released" in memory/roadmap.md         │
│   → (optional) Plane  → move version work items to Done               │
│   → (optional) Linear → move milestone issues to Done                 │
│   → Graphify → graphify . --update (refresh the graph for the next    │
│                version, now that this version's code exists)          │
│   STOP — human explicitly approves moving to the next version         │
└─────────────────────────────────────────────────────────────────────┘

Roadmap    → move Current Version pointer to vN+1, confirm/adjust its
             scope from the original brief
             (repeat the block above)
```

## How to run this in Cursor
1. Fill in `prompts/project-brief-template.md` with the whole project idea
   (not just one feature).
2. Say:
   `"Act as the agents defined in .cursor/agents, follow
   .cursor/workflows/version-workflow.md step by step starting with the
   roadmap agent, and respect AGENTS.md and .cursor/rules."`
3. Review the version slicing from `roadmap` before anything else happens —
   this is the most important checkpoint in the whole template, since every
   later step inherits this scope.
4. From there on, each version runs like a normal `feature-workflow.md` /
   `bugfix-workflow.md` cycle per feature, then one `release-workflow.md`
   pass to close the version out.
5. Do not let any agent start version `vN+1` work before `vN` is marked
   "Released" in `memory/roadmap.md` and you've explicitly said to
   continue.

## Stop Conditions
- Same as `feature-workflow.md`/`bugfix-workflow.md`, plus:
- Any agent proposes touching a file/feature that belongs to a version
  other than the Current Version → stop and ask the human before proceeding
  (see `.cursor/rules/versioning.mdc`, rule 2).
- `roadmap` slices a version that still looks too large for one pass of the
  chain (many unrelated features) → ask the human whether to split it
  further before starting implementation.

## Notes
- For a small project that clearly fits in one version, `roadmap` should
  say so explicitly and this workflow collapses to a single pass — you are
  not required to force multiple versions onto a small project.
- This workflow does not replace `feature-workflow.md` /
  `bugfix-workflow.md` / `release-workflow.md` — it sequences them across
  versions instead of running them ad hoc.
