"""Data layer. All persistence goes through here. SQLite for the sandbox.

This module is intentionally the single chokepoint for storage. If you find
raw sqlite3 connections anywhere else in the codebase, that is a finding.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "contoso.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS holds (
    id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL,
    amount_minor INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL,
    expires_at TEXT,
    FOREIGN KEY (account_id) REFERENCES accounts (id)
);
CREATE TABLE IF NOT EXISTS transfers (
    id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL,
    amount_minor INTEGER NOT NULL,
    hold_id INTEGER,
    created_at TEXT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts (id),
    FOREIGN KEY (hold_id) REFERENCES holds (id)
);
CREATE TABLE IF NOT EXISTS ledger (
    id INTEGER PRIMARY KEY,
    transfer_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    amount_minor INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    country TEXT DEFAULT '',
    FOREIGN KEY (transfer_id) REFERENCES transfers (id),
    FOREIGN KEY (account_id) REFERENCES accounts (id)
);
CREATE TABLE IF NOT EXISTS api_keys (
    id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL,
    token TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL,
    last_used_at TEXT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts (id)
);
CREATE TABLE IF NOT EXISTS webhooks (
    id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL,
    event TEXT NOT NULL,
    url TEXT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts (id)
);
"""


def connect(db_path: "Path | str | None" = None) -> sqlite3.Connection:
    path = str(db_path) if db_path is not None else str(DB_PATH)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    conn.commit()


def reset(conn: sqlite3.Connection) -> None:
    """Drop and recreate. Used by tests and the seed script."""
    conn.executescript(
        "DROP TABLE IF EXISTS webhooks;"
        "DROP TABLE IF EXISTS api_keys;"
        "DROP TABLE IF EXISTS ledger;"
        "DROP TABLE IF EXISTS transfers;"
        "DROP TABLE IF EXISTS holds;"
        "DROP TABLE IF EXISTS accounts;"
    )
    init_schema(conn)
