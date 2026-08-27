# Remote Setup Template (GitHub and/or GitLab)

Copy, fill in, and paste into Cursor Chat when you want this project
created/connected on GitHub, GitLab, or both.

```
Platforms:          <github | gitlab | both>
Primary remote:     <github | gitlab>   # becomes "origin"
Repo name:
Visibility:         <private | public>
Description:
GitHub org/user:    <optional>
GitLab namespace/group: <optional>
GitLab host URL:    <https://gitlab.com or self-hosted URL>
Existing local git?: <yes | no>
```

Then say to Cursor:
> Act as the `github` agent from `.cursor/agents/github.md`, follow
> `prompts/remote-setup-template.md` and `.cursor/rules/git-policy.mdc`.
> Create/connect the remote(s) above. Stop and ask before any `git push`.

## Notes
- Install CLIs once on your machine if missing:
  - GitHub: `winget install GitHub.cli` then `gh auth login`
  - GitLab: `winget install GLab.GLab` (or see https://gitlab.com/gitlab-org/cli)
    then `glab auth login`
- Never put PATs into committed files. Prefer `gh` / `glab` auth login.
- If both platforms are selected, the agent uses `origin` for Primary and
  a second remote named `github` or `gitlab` for the other host.
