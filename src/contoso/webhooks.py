"""Payment webhook registration and delivery.

deliver() is deliberately naive: it sends synchronously and in order to a
merchant's callback URL, with no timeout, retry, failure isolation, or
signature. Making it robust is a workshop exercise.
"""

from __future__ import annotations

import sqlite3


def register(conn: sqlite3.Connection, account_id: int, event: str, url: str) -> int:
    cur = conn.execute(
        "INSERT INTO webhooks (account_id, event, url) VALUES (?, ?, ?)",
        (account_id, event, url),
    )
    conn.commit()
    return int(cur.lastrowid)


def subscribers(conn: sqlite3.Connection, event: str) -> list:
    return conn.execute(
        "SELECT * FROM webhooks WHERE event = ?", (event,)
    ).fetchall()


def _noop_send(url: str, payload: dict) -> None:
    pass


def deliver(conn: sqlite3.Connection, event: str, payload: dict, send=None) -> int:
    send = send or _noop_send
    n = 0
    for sub in subscribers(conn, event):
        send(sub["url"], payload)  # synchronous, no isolation
        n += 1
    return n
