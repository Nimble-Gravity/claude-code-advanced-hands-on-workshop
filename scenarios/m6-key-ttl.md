# Module 6 scenario: Partner API key expiry

**Ticket (as received from the business):**

> Partner API keys should expire 30 days after their last use. `accounts.py`
> already has `is_api_key_valid(...)`; we need tests that actually prove
> expiry works before we trust it.

**Where it lives:** `src/contoso/accounts.py` (`is_api_key_valid` measures TTL
from `last_used_at`; the `created_at` column exists but is not read for
expiry).

**Your job is to generate tests from acceptance criteria, not from the code.**
A canned plan with acceptance criteria is at `reference/m6/plan.md`; copy it to
`artifacts/m6/plan.md`.

Use this for Module 6.
