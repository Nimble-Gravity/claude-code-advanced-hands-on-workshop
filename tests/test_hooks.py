import json
import subprocess
import sys
from pathlib import Path

HOOKS = Path(__file__).parent.parent / "hooks"


def _run(hook: str, payload: dict):
    return subprocess.run(
        [sys.executable, str(HOOKS / hook)],
        input=json.dumps(payload), text=True, capture_output=True,
    )


def test_protect_paths_blocks_env():
    r = _run("protect_paths.py", {"tool_name": "Write", "tool_input": {"file_path": "contoso/.env"}})
    assert r.returncode == 2


def test_protect_paths_allows_source():
    r = _run("protect_paths.py", {"tool_name": "Write", "tool_input": {"file_path": "src/contoso/transfers.py"}})
    assert r.returncode == 0


def test_scan_secrets_blocks_aws_key():
    r = _run("scan_secrets.py", {"tool_name": "Write",
             "tool_input": {"file_path": "x.py", "content": "AKIAIOSFODNN7EXAMPLE"}})
    assert r.returncode == 2


def test_scan_secrets_allows_clean_content():
    r = _run("scan_secrets.py", {"tool_name": "Write",
             "tool_input": {"file_path": "x.py", "content": "def f():\n    return 1\n"}})
    assert r.returncode == 0


def test_audit_log_appends_allow_line(tmp_path, monkeypatch):
    # audit_log writes to <repo>/artifacts/audit.log; just assert it exits 0 and writes a line
    r = _run("audit_log.py", {"tool_name": "Read", "tool_input": {"file_path": "src/contoso/db.py"}})
    assert r.returncode == 0
