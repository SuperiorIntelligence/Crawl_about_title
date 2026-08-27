# Release Workflow

```
Resume check → check memory/progress.md for an in-progress task on this
            workflow before starting (see .cursor/rules/continuity.mdc);
            every step below updates memory/progress.md before handing off
Docs      → CHANGELOG updated with all merged features/fixes since last release
Tester    → full test suite run on release branch
Security  → dependency/vulnerability check
Graphify  → graphify . --update (refresh the graph so it reflects the
            released version before the next one starts)
Git (GitHub/GitLab) → branch release/<version>, version bump commit,
            PR and/or MR opened
            STOP — wait for human approval
            (human merges + tags + deploys)
Roadmap   → mark this version "Released" in memory/roadmap.md, move the
            Current Version pointer forward (only after human confirms)
(optional) Plane → move work items for this version's module/cycle to Done,
            comment the version tag
(optional) Linear → same for Linear milestone if that tracker is used
```

## Notes
- No agent creates a git tag or triggers a deploy — those are human actions
  in this template. Automate them later once you trust the pipeline.
- When this template is used with `.cursor/workflows/version-workflow.md`,
  this file is the "close out version vN" step — see
  `.cursor/rules/versioning.mdc` for why the pointer only moves after this
  completes and the human approves.
