# Sandbox for Day 2 Module 3: sandboxed test execution.
# Minimal image, non-root user, no secrets baked in. Network egress is
# controlled at run time (see run-sandbox.sh), not here.
#
# Dependencies are installed from the lockfile at BUILD time into an
# image-resident venv (/opt/venv). Nothing is fetched at run time, so the
# container works under `--network none`. The worktree is mounted read-only at
# run time; pytest's `pythonpath = ["src"]` (from the mounted pyproject.toml)
# puts the worktree's source ahead of the baked copy, so tests run against the
# agent's code under test, not the code baked into the image.
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN useradd -m -u 1000 sandbox

# Bake deps from the lockfile into /opt/venv. Copy only what uv needs to
# resolve and build the project so this layer caches well.
WORKDIR /opt/app
COPY pyproject.toml uv.lock ./
COPY src ./src
COPY tests ./tests
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
RUN uv sync --frozen --no-editable

# No bytecode writes to the read-only mount; keep the pytest cache off disk.
ENV PYTHONDONTWRITEBYTECODE=1

USER sandbox
WORKDIR /work
# Run pytest straight from the baked venv (no uv, no network at run time).
ENTRYPOINT ["/opt/venv/bin/pytest", "-q", "-p", "no:cacheprovider"]
