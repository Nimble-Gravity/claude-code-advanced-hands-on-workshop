from contoso import db, seed


def test_seed_populates(tmp_path):
    path = tmp_path / "t.db"
    seed.main(str(path))
    conn = db.connect(str(path))
    assert conn.execute("SELECT COUNT(*) FROM transfers").fetchone()[0] >= 1
    assert conn.execute("SELECT COUNT(*) FROM ledger").fetchone()[0] >= 1
    assert conn.execute("SELECT COUNT(*) FROM holds").fetchone()[0] >= 1


def test_seed_includes_an_expired_hold(tmp_path):
    path = tmp_path / "t.db"
    seed.main(str(path))
    conn = db.connect(str(path))
    from contoso import models

    expired = conn.execute(
        "SELECT COUNT(*) FROM holds WHERE expires_at < ?", (models.iso(models.now()),)
    ).fetchone()[0]
    assert expired >= 1
