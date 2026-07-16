"""Monthly statement reporting. Owns the canonical country -> region bucketing
used for AML geo-reporting.
"""

from __future__ import annotations

import sqlite3

_REGION = {
    "US": "NA", "CA": "NA", "MX": "NA",
    "DE": "EU", "FR": "EU", "GB": "EU", "ES": "EU",
    "JP": "APAC", "AU": "APAC", "IN": "APAC",
}


def bucket_country(country_code: str) -> str:
    return _REGION.get(country_code, "OTHER")


def monthly_statement(conn: sqlite3.Connection) -> dict:
    counts: dict[str, int] = {}
    for row in conn.execute("SELECT country FROM ledger"):
        region = bucket_country(row["country"])
        counts[region] = counts.get(region, 0) + 1
    return counts
