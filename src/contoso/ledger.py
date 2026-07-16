"""Ledger entry recording and counting. Append-only record of posted transfers."""

from __future__ import annotations

import sqlite3

from contoso import models


def record_entry(
    conn: sqlite3.Connection,
    transfer_id: int,
    account_id: int,
    amount_minor: int,
    country: str = "",
) -> None:
    conn.execute(
        "INSERT INTO ledger (transfer_id, account_id, amount_minor, created_at, country)"
        " VALUES (?, ?, ?, ?, ?)",
        (transfer_id, account_id, amount_minor, models.iso(models.now()), country),
    )
    conn.commit()


def count_entries(conn: sqlite3.Connection, account_id: int) -> int:
    row = conn.execute(
        "SELECT COUNT(*) AS n FROM ledger WHERE account_id = ?", (account_id,)
    ).fetchone()
    return int(row["n"])
