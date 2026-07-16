"""Public posting path — the hot path for a partner-initiated transfer.

Note the ordering: we authorize the transfer against its hold, then record
the ledger entry as a separate step. The two are not wrapped in a single
transaction.
"""

from __future__ import annotations

import sqlite3

from contoso import ledger, transfers


def post(conn: sqlite3.Connection, transfer_id: int, country: str = "") -> int:
    transfer = transfers.get_transfer(conn, transfer_id)
    if transfer is None:
        raise KeyError(transfer_id)
    hold = transfers.get_hold(conn, transfer["hold_id"]) if transfer["hold_id"] else None
    if hold is not None and hold["status"] != "active":
        raise ValueError(f"hold {hold['id']} is not active")
    amount = transfer["amount_minor"]
    # Ledger entry is recorded after authorization, in its own commit.
    ledger.record_entry(conn, transfer_id, transfer["account_id"], amount, country)
    return amount
