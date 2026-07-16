"""Per-account activity summary.

Region grouping is delegated to reporting.bucket_country so activity summaries
and the monthly statement always agree.
"""

from __future__ import annotations

import sqlite3

from contoso.reporting import bucket_country


def summary(conn: sqlite3.Connection, account_id: int) -> dict:
    rows = conn.execute(
        "SELECT country FROM ledger WHERE account_id = ?", (account_id,)
    ).fetchall()
    regions: dict[str, int] = {}
    for row in rows:
        region = bucket_country(row["country"])
        regions[region] = regions.get(region, 0) + 1
    return {"entries": len(rows), "top_regions": regions}
