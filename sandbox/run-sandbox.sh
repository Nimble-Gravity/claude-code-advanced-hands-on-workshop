#!/usr/bin/env bash
# Run the test suite inside the sandbox with the four boundaries enforced.
#
#   --network none        : default-deny egress (Network boundary)
#   --read-only + tmpfs   : filesystem locked except an explicit scratch dir
#   -v "$PWD":/work        : mount only the worktree
#   --env-file /dev/null   : no host environment leaks in (Secrets boundary)
#
# Day 2 Module 3: run this, then run the three planted attack tests, then
# confirm the legitimate suite still passes.
set -euo pipefail

IMAGE="contoso-sandbox"

docker build -t "$IMAGE" -f sandbox/Dockerfile . >/dev/null

docker run --rm \
  --network none \
  --read-only \
  --tmpfs /tmp \
  -v "$PWD":/work:ro \
  -v "$PWD/artifacts":/work/artifacts:rw \
  --env-file /dev/null \
  "$IMAGE" "$@"
