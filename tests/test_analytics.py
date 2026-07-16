import pytest

from contoso import db, accounts, transfers, ledger, reporting, analytics


@pytest.fixture
def conn():
    c = db.connect(":memory:")
    db.reset(c)
    return c


def test_bucket_country_maps_to_region():
    assert reporting.bucket_country("US") == "NA"
    assert reporting.bucket_country("DE") == "EU"
    assert reporting.bucket_country("ZZ") == "OTHER"


def test_summary_counts_and_buckets(conn):
    acct = accounts.create_account(conn, "a@x.com")
    hold = transfers.create_hold(conn, acct, 1000)
    xfer = transfers.create_transfer(conn, acct, 1000, hold_id=hold)
    ledger.record_entry(conn, xfer, acct, 1000, "US")
    ledger.record_entry(conn, xfer, acct, 1000, "DE")
    ledger.record_entry(conn, xfer, acct, 1000, "US")
    s = analytics.summary(conn, acct)
    assert s["entries"] == 3
    assert s["top_regions"] == {"NA": 2, "EU": 1}


def test_monthly_statement_uses_same_buckets(conn):
    acct = accounts.create_account(conn, "a@x.com")
    hold = transfers.create_hold(conn, acct, 1000)
    xfer = transfers.create_transfer(conn, acct, 1000, hold_id=hold)
    ledger.record_entry(conn, xfer, acct, 1000, "US")
    assert reporting.monthly_statement(conn) == {"NA": 1}
