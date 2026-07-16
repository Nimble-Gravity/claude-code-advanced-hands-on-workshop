import pytest

from contoso import db
from contoso import accounts, transfers


@pytest.fixture
def conn():
    c = db.connect(":memory:")
    db.reset(c)
    return c


def test_create_and_get_transfer(conn):
    acct = accounts.create_account(conn, "a@x.com")
    hold = transfers.create_hold(conn, acct, 1000)
    xfer = transfers.create_transfer(conn, acct, 1000, hold_id=hold)
    row = transfers.get_transfer(conn, xfer)
    assert row["amount_minor"] == 1000
    assert row["hold_id"] == hold


def test_get_missing_transfer_returns_none(conn):
    assert transfers.get_transfer(conn, 999) is None


def test_create_and_get_hold(conn):
    acct = accounts.create_account(conn, "a@x.com")
    hold = transfers.create_hold(conn, acct, 500, status="active")
    row = transfers.get_hold(conn, hold)
    assert row["amount_minor"] == 500
    assert row["status"] == "active"
