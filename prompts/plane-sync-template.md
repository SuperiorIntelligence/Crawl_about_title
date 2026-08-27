# Plane Sync Prompts (copy/paste — requires Plane MCP)

The product is **Plane** (plane.so / self-hosted). See `mcp/SETUP.md` and
`.cursor/agents/plane.md`.

## Pull a work item into a task
```
Act as the plane agent from .cursor/agents/plane.md. Fetch Plane work item
<readable id or UUID> via MCP, convert it into a structured task, and hand
off to planner.
```

## List what is left to do
```
Act as the plane agent. List open work items for this repo's Plane project
(see .cursor/rules/plane-tasks.mdc). Group by state: Backlog / In Progress /
In Review / Done. Summarize what is left and what is blocked.
```

## Sync a PR/MR back to Plane
```
Act as the plane agent. The PR/MR for work item <id> was opened at <URL>.
Comment that link on the Plane work item and move it to the appropriate
In Review state for this workspace.
```

## Close out a released version in Plane
```
Act as the roadmap agent, then the plane agent. Version <vX> was just
released. Mark it Released in memory/roadmap.md (after human confirmation),
then move every work item for that version's module/cycle to Done and
comment the version tag.
```

## Sanity check after MCP setup
```
List every MCP tool you currently have available for Plane, with a one-line
description of each. Then retrieve the current Plane user.
```
