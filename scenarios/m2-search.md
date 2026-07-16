# Module 2 scenario (ticket A): Transfer search

**Ticket (as received from the business):**

> Account holders with hundreds of transfers can't find anything. Add a way
> to search an account's transfers by amount and reference (`transfer_id`).

**Where it lives:** `src/contoso/transfers.py` (transfer storage/lookup). No
search exists yet.

**Deliberate gaps to decide, not assume:**
- Exact match, range match on amount, or full-text on reference?
- Search `amount_minor` only, or `hold_id`/reference too?
- Scope to the owning account only?

Use this for Module 2 (planning only, via your `/plan-feature` command).
