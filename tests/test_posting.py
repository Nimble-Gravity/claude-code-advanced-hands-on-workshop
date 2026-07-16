import pytest

from contoso import db, accounts, transfers, ledger, posting


@pytest.fixture
def conn():
    c = db.connect(":memory:")
    db.reset(c)
    return c


def test_post_returns_amount_and_records_ledger_entry(conn):
    acct = accounts.create_account(conn, "a@x.com")
    hold = transfers.create_hold(conn, acct, 1000)
    xfer = transfers.create_transfer(conn, acct, 1000, hold_id=hold)
    assert posting.post(conn, xfer) == 1000
    assert ledger.count_entries(conn, acct) == 1


def test_post_unknown_transfer_raises(conn):
    with pytest.raises(KeyError):
        posting.post(conn, 999)


def test_post_still_succeeds_for_expired_hold(conn):
    # Trap: post() reads hold.status but never hold.expires_at, so an expired
    # hold still posts exactly like an active one.
    from datetime import timedelta

    from contoso import models

    acct = accounts.create_account(conn, "a@x.com")
    hold = transfers.create_hold(
        conn, acct, 750, expires_at=models.now() - timedelta(days=1)
    )
    xfer = transfers.create_transfer(conn, acct, 750, hold_id=hold)
    assert posting.post(conn, xfer) == 750
    assert ledger.count_entries(conn, acct) == 1
