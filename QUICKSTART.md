# Quickstart

## Option A — Dev Container (recommended)

Open the `claude-code-workshop` folder in VS Code and choose **Reopen in Container**.
Everything below is set up for you: uv + deps, the Claude Code CLI + plugins,
`gh`, and the `docker` CLI wired to the host daemon for the Day 2 sandbox. See
`.devcontainer/README.md`.

Then authenticate Claude Code (`claude`) and start the labs:

```bash
uv run jupyter lab notebooks/
```

## Option B — Local

```bash
uv sync
uv run pytest
uv run python -m contoso.seed
uv run jupyter lab notebooks/
```

Then open any module in `notebooks/day1/` or `notebooks/day2/` — each module is
self-contained, so you can start with whichever one you like.

## Module 5 preflight (Agent Teams)

Day 1 Module 5 uses the experimental **Agent Teams** feature. It needs Claude
Code **v2.1.32 or newer** (`claude --version` to check; upgrade with
`claude update` or your installer). The required env flag
`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` already ships in this repo's
`.claude/settings.json` — no action needed, but note that without it (or on an
older CLI) Claude quietly falls back to subagents and the module's team run
won't measure what it should. The notebook's preflight cell checks all of this.
