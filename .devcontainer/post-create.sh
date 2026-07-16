#!/usr/bin/env bash
# Provision the ContosoBank workshop dev container.
# Runs once, in the workspace folder, after the container is created.
set -euo pipefail

echo "==> Installing uv"
if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi
# uv installs to ~/.local/bin; make it available for the rest of this script
export PATH="$HOME/.local/bin:$PATH"

echo "==> Syncing Python dependencies (uv sync)"
uv sync

echo "==> Installing the Claude Code CLI"
if ! command -v claude >/dev/null 2>&1; then
  npm install -g @anthropic-ai/claude-code
fi

echo "==> Installing Claude Code plugins (best-effort; see README for manual steps)"
# Plugin CLI syntax can change between releases; never fail provisioning over it.
install_plugins() {
  claude plugin marketplace add anthropics/claude-plugins-official || return 1
  claude plugin install superpowers@claude-plugins-official || true
  claude plugin marketplace add JuliusBrussee/caveman || true
  claude plugin install caveman@caveman || true
}
if command -v claude >/dev/null 2>&1; then
  install_plugins || echo "    (plugin auto-install skipped — install manually with /plugin, see .devcontainer/README.md)"
else
  echo "    (claude CLI not on PATH yet — install plugins manually after first launch)"
fi

echo "==> Seeding the ContosoBank demo database"
uv run python -m contoso.seed

echo "==> Verifying the sandbox is healthy (uv run pytest)"
uv run pytest -q

cat <<'DONE'

==> Dev container ready.
    - Start the labs:   uv run jupyter lab notebooks/
    - Authenticate Claude Code on first run:  claude   (then follow the login prompt)
    - Day 2 Module 3 Docker sandbox works via the host daemon (docker-outside-of-docker).
DONE
