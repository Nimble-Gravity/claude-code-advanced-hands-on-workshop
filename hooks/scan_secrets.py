#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""PreToolUse hook: block file writes that contain secret-like strings.

Reads tool-call JSON on stdin, inspects EVERY string about to be written
(Write.content, Edit.new_string, and each MultiEdit edits[].new_string), and
exits 2 if any matches a secret pattern. Reference implementation for Day 2
Module 5. In production this hook is the integration point for the bank's real
scanning tooling; the hook is the plumbing, not the scanner.

On a block it appends a `deny` line to artifacts/audit.log so that blocked
attempts appear in the audit trail. A PreToolUse denial stops the tool call,
so the PostToolUse audit hook never sees it; without this line a blocked
attempt would leave no evidence, which defeats the Module 5 audit story.

Set the AUDIT_LOG environment variable to redirect logging to a scratch
path (used by the notebook's grounding/demo cells so they do not pollute
the participant's own artifacts/audit.log).
"""
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

LOG = Path(os.environ["AUDIT_LOG"]) if os.environ.get("AUDIT_LOG") else (
    Path(__file__).parent.parent / "artifacts" / "audit.log"
)

PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),                 # AWS access key id
    re.compile(r"sk-[A-Za-z0-9]{20,}"),              # generic secret key
    re.compile(r"-----BEGIN (RSA |EC )?PRIVATE KEY"),# private key block
    re.compile(r"(?i)(password|passwd|secret)\s*[:=]\s*['\"][^'\"]{6,}"),
]


def candidate_strings(ti: dict):
    """Every string a write tool could carry, across Write/Edit/MultiEdit."""
    if isinstance(ti.get("content"), str):
        yield ti["content"]
    if isinstance(ti.get("new_string"), str):
        yield ti["new_string"]
    for edit in ti.get("edits", []) or []:
        if isinstance(edit, dict) and isinstance(edit.get("new_string"), str):
            yield edit["new_string"]


def audit_deny(data: dict, reason: str) -> None:
    ti = data.get("tool_input", {})
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "session": data.get("session_id", ""),
        "agent": data.get("agent", "main"),
        "tool": data.get("tool_name", ""),
        "target": ti.get("file_path") or ti.get("notebook_path") or "",
        "decision": "deny",
        "approver": None,
        "reason": reason,
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
        return 0
    ti = data.get("tool_input", {})
    for text in candidate_strings(ti):
        for pat in PATTERNS:
            if pat.search(text):
                reason = f"secret pattern {pat.pattern!r}"
                print(f"BLOCKED: content matches {reason}", file=sys.stderr)
                audit_deny(data, reason)
                return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
