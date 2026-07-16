# Module 4 scenario: Cache the activity summary

**Ticket (as received from the business):**

> The per-account activity summary is recomputed from every ledger entry on
> every request and it's slow for active accounts. Cache it.

**Where it lives:** `src/contoso/analytics.py` `summary()` (recomputes from
all ledger entries each call); entries arrive via `src/contoso/posting.py`.

**Two legitimate approaches — you will run both and compare:**
- **Write-through:** update a cached summary on every posting (hot path).
- **Cache-aside + TTL:** compute lazily, cache with a short TTL / invalidation.

A canned plan + acceptance criteria are provided at `reference/m4/plan.md`;
copy it to `artifacts/m4/plan.md` and feed it to both approaches.

Use this for Module 4.
