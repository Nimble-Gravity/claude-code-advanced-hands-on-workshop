# Dev Container

A ready-to-go environment for the ContosoBank workshop (Day 1 + Day 2). Open the
`claude-code-workshop` folder in VS Code and choose **Reopen in Container**, or open
the top-level `advanced-claude-code.code-workspace` and reopen its ContosoBank root in
the container.

## What's included

- Python 3.12 + [uv](https://docs.astral.sh/uv/) (deps synced on create)
- Node LTS and the **Claude Code CLI** (`@anthropic-ai/claude-code`)
- `gh` CLI
- **docker-outside-of-docker** — the `docker` CLI plus the host's Docker socket,
  so the Day 2 Module 3 sandbox exercise runs against the host daemon (no
  Docker-in-Docker)
- Claude Code plugins (best-effort auto-install): `superpowers` and `caveman`
- VS Code: Python + Jupyter extensions; port 8888 forwarded for JupyterLab

The workspace is bind-mounted at the **same absolute path** inside the container
as on the host (`workspaceMount` in `devcontainer.json`). That alignment is what
lets `sandbox/run-sandbox.sh`'s `-v "$PWD":/work` mount resolve correctly when the
container talks to the host Docker daemon.

## First run

On create, `post-create.sh` installs uv, syncs deps, installs the Claude Code CLI,
attempts the plugin installs, seeds the demo DB, and runs the test suite as a
health check.

1. **Authenticate Claude Code** (not baked into the image — no secrets shipped):
   ```bash
   claude
   ```
   Follow the login / API-key prompt on first launch.
2. **Start the labs:**
   ```bash
   uv run jupyter lab notebooks/
   ```

## Plugins — manual fallback

If the best-effort auto-install was skipped (plugin CLI syntax drifts between
releases), install them from inside Claude Code:

```
/plugin marketplace add anthropics/claude-plugins-official
/plugin install superpowers@claude-plugins-official
/plugin marketplace add JuliusBrussee/caveman
/plugin install caveman@caveman
```

## Day 2 Module 3 (Docker sandbox)

With docker-outside-of-docker the Docker path works in the container:

```bash
./sandbox/run-sandbox.sh
```

If your setup mounts the workspace at a different path than the host (so the
`-v "$PWD":/work` bind fails), use the no-Docker fallback documented in
`sandbox/README.md` — fill `scenarios/sandbox-spec-template.md` and self-attack
the spec.
