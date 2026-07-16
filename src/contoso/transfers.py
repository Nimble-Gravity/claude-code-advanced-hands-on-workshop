"""Create and look up transfers and their authorization holds.

A transfer moves money from a partner's account; it is authorized by a hold
before it can post (see posting.py). Transfers are keyed by transfer_id.
"""

from __future__ import annotations

import sqlite3

from contoso import models


def create_hold(
    conn: sqlite3.Connection,
    account_id: int,
    amount_minor: int,
    status: str = "active",
    expires_at=None,
) -> int:
    cur = conn.execute(
        "INSERT INTO holds (account_id, amount_minor, status, created_at, expires_at)"
        " VALUES (?, ?, ?, ?, ?)",
        (
            account_id,
            amount_minor,
            status,
            models.iso(models.now()),
            models.iso(expires_at) if expires_at else None,
        ),
    )
    conn.commit()
    return int(cur.lastrowid)


def get_hold(conn: sqlite3.Connection, hold_id: int) -> "sqlite3.Row | None":
    return conn.execute(
        "SELECT * FROM holds WHERE id = ?", (hold_id,)
    ).fetchone()


def create_transfer(
    conn: sqlite3.Connection,
    account_id: int,
    amount_minor: int,
    hold_id: int | None = None,
) -> int:
    cur = conn.execute(
        "INSERT INTO transfers (account_id, amount_minor, hold_id, created_at)"
        " VALUES (?, ?, ?, ?)",
        (account_id, amount_minor, hold_id, models.iso(models.now())),
    )
    conn.commit()
    return int(cur.lastrowid)


def get_transfer(conn: sqlite3.Connection, transfer_id: int) -> "sqlite3.Row | None":
    return conn.execute(
        "SELECT * FROM transfers WHERE id = ?", (transfer_id,)
    ).fetchone()
