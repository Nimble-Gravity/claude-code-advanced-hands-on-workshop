"""Domain models. Counts and IDs are integers. Amounts are integer minor units
(cents) — never floats. Timestamps are UTC ISO strings.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class Account:
    id: int
    email: str


@dataclass
class Hold:
    id: int
    account_id: int
    amount_minor: int
    status: str = "active"
    # Day 1 capstone (expiring holds) cares about this. Nothing consumes it yet.
    expires_at: datetime | None = None


@dataclass
class Transfer:
    id: int
    account_id: int
    amount_minor: int
    hold_id: int | None = None


@dataclass
class LedgerEntry:
    id: int
    transfer_id: int
    account_id: int
    amount_minor: int
    country: str = ""


@dataclass
class ApiKey:
    id: int
    account_id: int
    token: str
    # TTL is measured from last_used_at. created_at is kept but NOT used for expiry.
    created_at: datetime | None = None
    last_used_at: datetime | None = None


@dataclass
class Webhook:
    id: int
    account_id: int
    event: str
    url: str


def now() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat()


def parse(s: str) -> datetime:
    return datetime.fromisoformat(s)
