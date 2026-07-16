from datetime import timedelta

import pytest

from contoso import db, accounts
from contoso.models import now


@pytest.fixture
def conn():
    c = db.connect(":memory:")
    db.reset(c)
    return c


def test_new_key_is_valid(conn):
    acct = accounts.create_account(conn, "a@x.com")
    token = accounts.create_api_key(conn, acct)
    assert accounts.is_api_key_valid(conn, token) is True


def test_key_expires_30_days_after_last_use(conn):
    acct = accounts.create_account(conn, "a@x.com")
    token = accounts.create_api_key(conn, acct)
    future = now() + timedelta(days=31)
    assert accounts.is_api_key_valid(conn, token, at=future) is False


def test_touch_extends_validity(conn):
    acct = accounts.create_account(conn, "a@x.com")
    token = accounts.create_api_key(conn, acct)
    accounts.touch_api_key(conn, token)
    near = now() + timedelta(days=29)
    assert accounts.is_api_key_valid(conn, token, at=near) is True
