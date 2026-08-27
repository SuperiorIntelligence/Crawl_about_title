# Linear Sync Prompts (copy/paste, requires the Linear MCP connector)

See `mcp/SETUP.md` to connect Linear first, and `.cursor/agents/linear.md`
for the full behavior/rules of this persona.

## Pull an issue into a task
```
Act as the linear agent from .cursor/agents/linear.md. Fetch Linear issue
<ID or URL> via the Linear MCP tools, convert it into a structured task,
and hand off to planner.
```

## Pull a whole project/milestone into version-workflow
```
Act as the linear agent, then the roadmap agent. List all issues in Linear
project/milestone <name or ID> via MCP, summarize them into a project
brief matching prompts/project-brief-template.md, then follow
.cursor/workflows/version-workflow.md.
```

## Sync a PR back to Linear
```
Act as the linear agent. The PR for issue <ID> was just opened at <PR URL>.
Comment that link on the Linear issue and move it to "In Review".
```

## Close out a released version in Linear
```
Act as the roadmap agent, then the linear agent. Version <vX> was just
released (release-workflow.md completed). Mark it "Released" in
memory/roadmap.md, then move every issue in that version's Linear
milestone to "Done" and comment the version tag on each.
```

## Just ask what's available (sanity check after setup)
```
List every MCP tool you currently have available for Linear, with a
one-line description of each.
```
