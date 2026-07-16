# Quickstart

## Option A — Dev Container (recommended)

Open this folder in VS Code and choose **Reopen in Container** (or open the
top-level `advanced-claude-code.code-workspace`). Everything below is set up for
you: uv + deps, the Claude Code CLI + plugins, `gh`, and the `docker` CLI wired
to the host daemon for the Day 2 sandbox. See `.devcontainer/README.md`.

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
