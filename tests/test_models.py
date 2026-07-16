from datetime import datetime, timezone

from contoso.models import Hold, now, iso, parse


def test_now_is_utc_aware():
    assert now().tzinfo is not None


def test_iso_roundtrip():
    dt = datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
    assert parse(iso(dt)) == dt


def test_hold_defaults():
    hold = Hold(id=1, account_id=1, amount_minor=500)
    assert hold.expires_at is None
