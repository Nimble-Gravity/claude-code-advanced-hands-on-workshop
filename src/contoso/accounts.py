"""Accounts and partner API keys."""

from __future__ import annotations

import secrets as _secrets
import sqlite3
from datetime import timedelta

from contoso import models


def create_account(conn: sqlite3.Connection, email: str) -> int:
    cur = conn.execute(
        "INSERT INTO accounts (email, created_at) VALUES (?, ?)",
        (email, models.iso(models.now())),
    )
    conn.commit()
    return int(cur.lastrowid)


def create_api_key(conn: sqlite3.Connection, account_id: int) -> str:
    token = _secrets.token_hex(16)
    ts = models.iso(models.now())
    conn.execute(
        "INSERT INTO api_keys (account_id, token, created_at, last_used_at)"
        " VALUES (?, ?, ?, ?)",
        (account_id, token, ts, ts),
    )
    conn.commit()
    return token


def touch_api_key(conn: sqlite3.Connection, token: str) -> None:
    conn.execute(
        "UPDATE api_keys SET last_used_at = ? WHERE token = ?",
        (models.iso(models.now()), token),
    )
    conn.commit()


def is_api_key_valid(conn, token, at=None, ttl_days: int = 30) -> bool:
    row = conn.execute(
        "SELECT last_used_at FROM api_keys WHERE token = ?", (token,)
    ).fetchone()
    if row is None:
        return False
    at = at or models.now()
    last_used = models.parse(row["last_used_at"])
    return at - last_used <= timedelta(days=ttl_days)
