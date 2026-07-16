# Capstone scenario: Expiring authorization holds

**Ticket (as received from the business):**

> Authorization holds already carry an expiry. After a hold expires, a
> transfer referencing it must not post. This must interact correctly with
> the posting path and with how analytics/statements treat postings against
> an expired hold.

**Where it lives:** the `holds` table already has an `expires_at` column
(`src/contoso/db.py`, `src/contoso/models.py`); `posting.post` does not check
it; `analytics.py`/`reporting.py` aggregate ledger entries regardless.

**Deliberate gaps to decide, not assume:**
- Is expiry checked at posting time, by a sweep, or both? UTC anchor?
- Do ledger entries against an already-expired hold still count in analytics?
- Where does the "is this hold expired?" rule live so posting and analytics
  agree (avoid two sources of truth)?

Unseen ticket — run the whole pipeline on it. Use for the Day 1 capstone.
