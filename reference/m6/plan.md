# Technical Plan: API keys expire 30 days after last use

## Restated intent
An API key becomes invalid once 30 days have passed since it was last used.
Using a key resets that 30-day clock. `accounts.py` already implements this
via `is_api_key_valid(conn, token, at=None, ttl_days=30)`, which measures TTL
from `last_used_at`. The job here is to generate tests, from the acceptance
criteria below, that actually prove this behaviour — not to change the
implementation.

## Explicit assumptions
- "Used" means any call that updates `last_used_at` (i.e. `touch_api_key`).
  Tests may call `touch_api_key` directly to simulate use rather than going
  through a full request path.
- Time is UTC via `contoso.models.now()`/`iso()`/`parse()`, consistent with the
  rest of the codebase; tests should pass an explicit `at=` to
  `is_api_key_valid` (or construct timestamps and write them directly via
  `contoso.db`) rather than depending on real wall-clock sleeps.
- A key that has never been used is exempt from this ambiguity: creating a
  key sets `last_used_at` immediately (see `create_api_key`), so every key
  has a `last_used_at` from the moment it exists.
- Exactly-30-days boundary behaviour follows the `<=` in the current
  implementation (30 days ago is still valid; 31 days ago is not) — tests
  should pin this boundary explicitly rather than only testing comfortably
  inside/outside it.

## Implementation steps
1. Write test fixtures that create an account and API key, then manipulate
   `last_used_at` (directly via `contoso.db`, or via `touch_api_key` called
   with a controlled `at`) to simulate "last used N days ago" — `tests/`.
2. Write one test per acceptance criterion below, deriving each test's
   assertion from the criterion's wording, not from re-reading
   `is_api_key_valid`'s implementation.
3. Run `uv run pytest` and confirm all new tests pass against the existing,
   unmodified `is_api_key_valid`.

## Test expectations
Acceptance criteria (each proved by a corresponding test):

- AC1: a key unused for 31 days is invalid — a key whose `last_used_at` is 31
  days before the check time returns `False` from `is_api_key_valid(...)`.
- AC2: a key used 29 days ago is valid — a key whose `last_used_at` is 29
  days before the check time returns `True` from `is_api_key_valid(...)`.
- AC3: using a key resets the 30-day clock — a key that was on track to
  expire, then used again, is valid at a check time that would have made the
  *previous* `last_used_at` invalid (measured from the new use, not the old
  one).

## Risks
- A test can appear to pass while not actually exercising the 30-day expiry
  boundary — verify each criterion is checked by a test that would fail if
  the logic were removed.
- Boundary tests (exactly 30 days) are easy to skip in favor of "clearly
  valid"/"clearly invalid" cases, which would leave the `<=` vs `<` choice in
  `is_api_key_valid` unverified.
