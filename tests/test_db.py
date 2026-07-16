from contoso import db


def test_reset_creates_all_tables():
    conn = db.connect(":memory:")
    db.reset(conn)
    names = {
        row["name"]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
    }
    assert {"accounts", "transfers", "holds", "ledger", "api_keys", "webhooks"} <= names


def test_connect_enables_foreign_keys():
    conn = db.connect(":memory:")
    assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1
