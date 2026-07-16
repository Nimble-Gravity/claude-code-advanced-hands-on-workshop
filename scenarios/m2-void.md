# Module 2 scenario (ticket B): Void and restore a transfer

**Ticket (as received from the business):**

> Cancelling a transfer outright is too final — support wants a 30-day window
> to restore a voided transfer before it's gone for good.

**Where it lives:** `src/contoso/transfers.py` and the `transfers` table (no
`voided_at` column yet).

**Deliberate gaps to decide, not assume:**
- Does a voided transfer still post, or is posting blocked?
- Do ledger entries against a voided transfer still count in analytics?
- What purges after 30 days, and what triggers the purge?

Use this for Module 2 (planning only, via your `/plan-feature` command). It is
deliberately unrelated to ticket A — your command must handle both without
hardcoding either.
