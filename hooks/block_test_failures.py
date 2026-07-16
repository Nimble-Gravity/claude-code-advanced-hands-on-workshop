#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Stop hook: refuse to end the session while tests fail.

Guards against infinite loops via stop_hook_active. Exit 2 tells Claude to
keep working; exit 0 allows the stop. Bonus reference for Day 2 Module 5.
"""
import json
import subprocess
import sys


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    if data.get("stop_hook_active"):
        return 0  # already re-invoked once; allow stop to avoid a loop
    result = subprocess.run(
        ["uv", "run", "pytest", "-q"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print("Tests are failing. Fix them before ending the session.",
              file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
