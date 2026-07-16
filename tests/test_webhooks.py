import pytest

from contoso import db, accounts, webhooks


@pytest.fixture
def conn():
    c = db.connect(":memory:")
    db.reset(c)
    return c


def test_register_and_list_subscribers(conn):
    acct = accounts.create_account(conn, "a@x.com")
    webhooks.register(conn, acct, "transfer.posted", "https://merchant.test/hooks/a")
    subs = webhooks.subscribers(conn, "transfer.posted")
    assert len(subs) == 1
    assert subs[0]["url"] == "https://merchant.test/hooks/a"


def test_deliver_calls_send_for_each_subscriber(conn):
    acct = accounts.create_account(conn, "a@x.com")
    webhooks.register(conn, acct, "transfer.posted", "https://merchant.test/hooks/a")
    webhooks.register(conn, acct, "transfer.posted", "https://merchant.test/hooks/b")
    sent = []
    n = webhooks.deliver(
        conn, "transfer.posted", {"transfer_id": 1}, send=lambda u, p: sent.append(u)
    )
    assert n == 2
    assert sent == ["https://merchant.test/hooks/a", "https://merchant.test/hooks/b"]
