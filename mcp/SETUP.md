# MCP + CLI Setup — Plane, Linear, Graphify, Git hosts

This file is a one-time, **human** setup guide. Agents reference it; they
don't execute it themselves (connecting MCP servers and installing CLIs
are environment changes, not code changes).

> The task tracker in your org docs is **Plane** (plane.so / self-hosted).
> People sometimes spell it "Plain" — in this template the correct name is
> always **Plane**.

---

## 0. GitHub and/or GitLab (repo hosting — not MCP)

You can host the same project on GitHub, GitLab, or both. The `github`
agent (`.cursor/agents/github.md`) handles both. Use
`prompts/remote-setup-template.md` when creating remotes.

### GitHub CLI (Windows)
```powershell
winget install GitHub.cli
gh auth login
```

### GitLab CLI (Windows)
```powershell
winget install GLab.GLab
glab auth login
# for self-hosted GitLab, set host during login / config
```

### Create / connect a project
Paste a filled `prompts/remote-setup-template.md` into Cursor Chat and ask
the `github` agent to run it. It **must stop before `git push`** and wait
for your yes (see `.cursor/rules/git-policy.mdc`).

Never commit PATs. Prefer `gh` / `glab` login.

---

## 1. Plane MCP (preferred task tracker)

Official docs: [MCP server](https://developers.plane.so/dev-tools/mcp-server) ·
[Tool reference](https://developers.plane.so/dev-tools/mcp-server-tools)

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed so `uvx` is on PATH
- A Plane Personal Access Token (header `X-API-Key`)
- Workspace slug + base URL of your instance

### Recommended: user-global Cursor MCP
Edit `%USERPROFILE%\.cursor\mcp.json` (Windows) or `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "plane": {
      "command": "uvx",
      "args": ["plane-mcp-server", "stdio"],
      "env": {
        "PLANE_API_KEY": "plane_api_YOUR_TOKEN",
        "PLANE_WORKSPACE_SLUG": "iran_ma",
        "PLANE_BASE_URL": "https://plane.ir-ma.ir"
      }
    }
  }
}
```

| Variable | Your instance (from org docs) |
|---|---|
| `PLANE_API_KEY` | Personal Access Token — **never commit this** |
| `PLANE_WORKSPACE_SLUG` | `iran_ma` |
| `PLANE_BASE_URL` | `https://plane.ir-ma.ir` |

Safer variant using OS env (recommended once you set system env vars):

```json
{
  "mcpServers": {
    "plane": {
      "command": "uvx",
      "args": ["plane-mcp-server", "stdio"],
      "env": {
        "PLANE_API_KEY": "${env:PLANE_API_KEY}",
        "PLANE_WORKSPACE_SLUG": "${env:PLANE_WORKSPACE_SLUG}",
        "PLANE_BASE_URL": "${env:PLANE_BASE_URL}"
      }
    }
  }
}
```

Then set in Windows User Environment:
- `PLANE_API_KEY`
- `PLANE_WORKSPACE_SLUG=iran_ma`
- `PLANE_BASE_URL=https://plane.ir-ma.ir`

After saving:
1. `Ctrl+Shift+P` → **Reload Window**
2. Settings → **MCP** → `plane` should show connected/green
3. Ask Agent: «کاربر فعلی Plane را نشان بده» or «لیست پروژه‌های workspace»

### Per-repo mapping
Copy/adjust `.cursor/rules/plane-tasks.mdc` and fill:
- Plane project name, identifier, `project_id`
- Module UUID mappings for folders/services

### Verify API without MCP
```powershell
curl -H "X-API-Key: YOUR_TOKEN" "https://plane.ir-ma.ir/api/v1/users/me/"
```

### Notes
- Rate limit ~60 requests/minute
- Postman collections (if you have them) are for manual API testing; MCP is
  for day-to-day Agent use
- Agent persona: `.cursor/agents/plane.md`
- Prompt pack: `prompts/plane-sync-template.md`

---

## 2. Linear MCP (optional alternative tracker)

Only needed if you still use Linear instead of (or in addition to) Plane.

### Option A — Project-scoped OAuth
Create/edit `.cursor/mcp.json` at the project root (see also
`.cursor/mcp.json.example`):
```json
{
  "mcpServers": {
    "linear": {
      "url": "https://mcp.linear.app/mcp"
    }
  }
}
```
Then: **Cursor Settings → Tools & MCP** → Connect → browser OAuth.

### Option B — Global
Same JSON in `%USERPROFILE%\.cursor\mcp.json`.

### Option C — API key / stdio
```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@linear/mcp"],
      "env": {
        "LINEAR_API_KEY": "${env:LINEAR_API_KEY}"
      }
    }
  }
}
```

---

## 3. Graphify (local knowledge graph, token efficiency)

Graphify (https://github.com/Graphify-Labs/graphify) parses this repo
locally into `graphify-out/`. See `.cursor/rules/graphify.mdc`.

### Install (Windows / PowerShell)
```powershell
winget install astral-sh.uv
uv tool install graphifyy
graphify cursor install
```

### Build / refresh
```powershell
graphify .
graphify . --update
```

Optional MCP:
```powershell
uv tool install "graphifyy[mcp]"
```
```json
{
  "mcpServers": {
    "graphify": {
      "command": "python",
      "args": ["-m", "graphify.serve", "graphify-out/graph.json"]
    }
  }
}
```

---

## Combined example `.cursor/mcp.json`

A project-level file may combine servers (Plane is often configured
**globally** instead so the API key is not in the repo):

```json
{
  "mcpServers": {
    "linear": {
      "url": "https://mcp.linear.app/mcp"
    },
    "graphify": {
      "command": "python",
      "args": ["-m", "graphify.serve", "graphify-out/graph.json"]
    }
  }
}
```

Keep Plane in the **user-global** `mcp.json` with the API key, or use
`${env:...}` references only — never commit a real `PLANE_API_KEY`.
