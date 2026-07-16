"""
API key expiry tests — criteria-derived, not code-derived.

Each test traces explicitly to an acceptance criterion from artifacts/m6/plan.md.
Tests manipulate last_used_at (the column that actually drives expiry behavior)
and verify is_api_key_valid's response, not created_at (which is never read).
"""

import pytest
from datetime import timedelta
import contoso.db as db
import contoso.accounts as accounts
from contoso.models import now, iso, parse


@pytest.fixture
def conn():
    """Fresh in-memory DB per test."""
    c = db.connect(":memory:")
    db.reset(c)
    return c


@pytest.fixture
def acct_and_key(conn):
    """Account and API key ready for last_used_at manipulation."""
    acct = accounts.create_account(conn, "test@example.com")
    tok = accounts.create_api_key(conn, acct)
    return conn, acct, tok


def test_ac1_key_invalid_at_31_days(acct_and_key):
    """AC1: a key unused for 31 days is invalid.

    Derives from: "a key whose last_used_at is 31 days before the check time
    returns False from is_api_key_valid(...)"
    """
    conn, acct, tok = acct_and_key
    check_time = now()
    # Compute 31 days before check time as ISO string.
    old_time = iso(check_time - timedelta(days=31))

    # Manipulate last_used_at directly to 31 days ago.
    conn.execute("UPDATE api_keys SET last_used_at = ? WHERE token = ?",
                 (old_time, tok))
    conn.commit()

    # Assert the criterion: key should be invalid.
    assert accounts.is_api_key_valid(conn, tok, at=check_time) is False


def test_ac2_key_valid_at_29_days(acct_and_key):
    """AC2: a key used 29 days ago is valid.

    Derives from: "a key whose last_used_at is 29 days before the check time
    returns True from is_api_key_valid(...)"
    """
    conn, acct, tok = acct_and_key
    check_time = now()
    recent_time = iso(check_time - timedelta(days=29))

    # Set last_used_at to 29 days ago.
    conn.execute("UPDATE api_keys SET last_used_at = ? WHERE token = ?",
                 (recent_time, tok))
    conn.commit()

    # Assert the criterion: key should be valid.
    assert accounts.is_api_key_valid(conn, tok, at=check_time) is True


def test_ac3_use_resets_window(acct_and_key):
    """AC3: using a key resets the 30-day clock.

    Derives from: "a key that was on track to expire, then used again,
    is valid at a check time that would have made the previous last_used_at
    invalid (measured from the new use, not the old one)"
    """
    conn, acct, tok = acct_and_key

    # Set key to 31 days old (would be invalid if checked now).
    old_time = iso(now() - timedelta(days=31))
    conn.execute("UPDATE api_keys SET last_used_at = ? WHERE token = ?",
                 (old_time, tok))
    conn.commit()

    # Verify key is currently invalid from old timestamp.
    assert accounts.is_api_key_valid(conn, tok) is False

    # Use the key now (resets the clock to now).
    accounts.touch_api_key(conn, tok)

    # Key should now be valid even though the old timestamp was 31 days ago.
    # This proves the reset worked — we measure from the new use, not the old one.
    assert accounts.is_api_key_valid(conn, tok) is True


def test_boundary_exactly_30_days(acct_and_key):
    """Boundary: exactly 30 days after last use should still be valid.

    The implementation uses <=, so 30 days is the last valid moment.
    Verify both sides: 30 days is valid, 31 days is not.
    """
    conn, acct, tok = acct_and_key
    check_time = now()

    # Set last_used_at to exactly 30 days before check.
    exactly_30_ago = iso(check_time - timedelta(days=30))
    conn.execute("UPDATE api_keys SET last_used_at = ? WHERE token = ?",
                 (exactly_30_ago, tok))
    conn.commit()

    # At 30 days, should still be valid (this tests the <= boundary).
    assert accounts.is_api_key_valid(conn, tok, at=check_time) is True

    # At 30 days + 1 second, should be invalid.
    check_time_plus_1 = check_time + timedelta(seconds=1)
    assert accounts.is_api_key_valid(conn, tok, at=check_time_plus_1) is False
