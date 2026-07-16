"""Populate a demo ContosoBank database. Run: python -m contoso.seed"""

from __future__ import annotations

from datetime import timedelta

from contoso import db, accounts, transfers, ledger, webhooks, models


def main(db_path: "str | None" = None) -> None:
    conn = db.connect(db_path)
    db.reset(conn)
    acct = accounts.create_account(conn, "demo@contosobank.test")
    accounts.create_api_key(conn, acct)
    webhooks.register(conn, acct, "transfer.posted", "https://merchant.test/hooks/demo")

    active_hold = transfers.create_hold(
        conn, acct, 5000, expires_at=models.now() + timedelta(days=1)
    )
    xfer = transfers.create_transfer(conn, acct, 5000, hold_id=active_hold)
    for country in ("US", "US", "DE", "JP", "US", "GB"):
        ledger.record_entry(conn, xfer, acct, 5000, country)

    # An authorization hold that already expired, with a transfer referencing
    # it, so the expiry trap is live on a fresh db.
    expired_hold = transfers.create_hold(
        conn, acct, 2500, expires_at=models.now() - timedelta(days=1)
    )
    expired_xfer = transfers.create_transfer(conn, acct, 2500, hold_id=expired_hold)

    print(
        f"seeded: account={acct} transfer={xfer} ledger_entries=6 "
        f"holds=2 (1 expired, unposted transfer={expired_xfer})"
    )


if __name__ == "__main__":
    main()
