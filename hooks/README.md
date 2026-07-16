# hooks/

Reference control-plane hooks for Day 2 Module 5 (uv single-file scripts).

- `protect_paths.py`  PreToolUse: block Write/Edit to protected paths (`.env`,
  `.claude/settings.json`, `hooks/`, CI dirs); self-logs a `deny` line.
- `scan_secrets.py`   PreToolUse: block writes containing secret-like strings;
  self-logs a `deny` line.
- `audit_log.py`      PostToolUse: append an `allow` line for every tool call.
- `block_test_failures.py`  Stop: refuse to end the session while tests fail.

A PreToolUse denial never reaches PostToolUse, so the two Pre hooks self-log
their denials — otherwise blocked attempts would leave no audit trail. Wire
them in `.claude/settings.json` (Module 5 exercise). All four write/read
`artifacts/audit.log`.
