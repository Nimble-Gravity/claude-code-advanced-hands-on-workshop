#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""PreToolUse hook: block writes to protected paths.

Reads the tool-call JSON on stdin. If the tool is about to write or edit a
protected path (config, credentials, CI definitions, the hooks directory
itself), exit 2 to block. Exit 0 to allow.

Register in .claude/settings.json under PreToolUse with matcher "Write|Edit"
(that matcher also covers MultiEdit, whose file_path is read here too).
This is a reference implementation for Day 2 Module 5. Extend the list.

Why the hooks directory is on the list: an agent that can edit the hooks can
remove the control plane. That line is not optional.

On a block it appends a `deny` line to artifacts/audit.log. A PreToolUse
denial stops the call before PostToolUse runs, so without this the blocked
attempt would leave no audit evidence.

Set the AUDIT_LOG environment variable to redirect logging to a scratch
path (used by the notebook's grounding/demo cells so they do not pollute
the participant's own artifacts/audit.log).
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

LOG = Path(os.environ["AUDIT_LOG"]) if os.environ.get("AUDIT_LOG") else (
    Path(__file__).parent.parent / "artifacts" / "audit.log"
)

PROTECTED = (
    ".env",
    ".claude/settings.json",
    "hooks/",
    ".github/",
    ".gitlab-ci",
)


def audit_deny(data: dict, path: str, needle: str) -> None:
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "session": data.get("session_id", ""),
        "agent": data.get("agent", "main"),
        "tool": data.get("tool_name", ""),
        "target": path,
        "decision": "deny",
        "approver": None,
        "reason": f"protected path (matched '{needle}')",
    }
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOG.open("a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass  # never let audit failure crash the control hook


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0  # nothing to inspect; do not block on parse failure
    ti = data.get("tool_input", {})
    path = str(ti.get("file_path") or ti.get("notebook_path") or "")
    for needle in PROTECTED:
        if needle in path:
            print(f"BLOCKED: write to protected path '{path}' (matched '{needle}')",
                  file=sys.stderr)
            audit_deny(data, path, needle)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
