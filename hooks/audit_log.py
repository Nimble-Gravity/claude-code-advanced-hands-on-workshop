#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""PostToolUse hook: append a structured audit line for every tool call.

Reads tool-call JSON on stdin, writes one JSON line to artifacts/audit.log.
Never blocks (PostToolUse cannot un-ring the bell). Reference implementation
for Day 2 Module 5. Schema: see templates/audit-log-schema.md.

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


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    ti = data.get("tool_input", {})
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "session": data.get("session_id", ""),
        "agent": data.get("agent", "main"),
        "tool": data.get("tool_name", ""),
        "target": ti.get("file_path") or ti.get("command") or "",
        "decision": "allow",
        "approver": None,
    }
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
