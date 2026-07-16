# Technical Plan: change analytics region bucketing

## Restated intent
Compliance wants finer-grained region buckets in the per-account activity
summary than the current NA/EU/APAC/OTHER split — for example separating
`EU` into `EU-West`/`EU-East`, and giving under-represented countries their
own bucket instead of collapsing into `OTHER`. The output of
`analytics.summary()` should reflect the new buckets; nothing else about the
summary's shape (keys `entries` and `top_regions`) changes.

## Explicit assumptions
- The region-bucketing logic is local to `reporting.py` — it is the module
  that owns "how a ledger entry's country becomes a region" (via
  `bucket_country`) for both the per-account summary and the monthly
  statement, so the new bucket definitions can be added there without
  touching other modules.
- Only the *mapping* from country code to region name changes. The shape of
  `summary()`'s return value (`{"entries": int, "top_regions": {region:
  count}}`) is unchanged, so no caller of `analytics.summary` needs to
  change.
- The new bucket set is additive/finer, not a renumbering — no bucket that
  previously existed disappears, so there is no migration concern for any
  region labels persisted elsewhere (none are, today).
- No historical ledger data needs to be reclassified; the new mapping
  applies going forward to however `summary()` recomputes on each call.
- `posting.py` and `ledger.py` are unaffected — they record raw `country`
  strings on the ledger row and never see a region label, so bucketing
  changes are invisible to the ledger-recording path.

## Implementation steps
1. Add the finer-grained country→region table (e.g. split `DE`/`FR` into
   `EU-West`, add `EU-East` entries for currently-unlisted Eastern European
   codes, and give a couple of previously-`OTHER` countries their own bucket)
   — `reporting.py` (`_REGION`).
2. Update `bucket_country()` to use the new table instead of the current one
   — `reporting.py`; `analytics.summary()` and `reporting.monthly_statement()`
   both call it, so no change is needed at either call site.
3. Update/add unit tests asserting that ledger entries from the newly-split
   countries land in the correct new bucket, and that previously-passing
   bucket assignments (e.g. `US` → `NA`) are unchanged — `tests/`.
4. Spot-check `analytics.summary()` output for an account with a mixed set
   of ledger-entry countries to confirm `top_regions` matches the new
   bucket names.

## Test expectations
- A ledger entry with country `DE` is bucketed as `EU-West` (not the old
  `EU`).
- A ledger entry with country `US` is still bucketed as `NA` (regression
  check — buckets that didn't change should not change).
- `summary()`'s `entries` count is unaffected by the bucketing change (only
  `top_regions` keys/values shift).
- An account with ledger entries from multiple newly-split countries
  produces a `top_regions` dict with one entry per new bucket, counts
  summing to `entries`.

## Risks
- If the new bucket names are typo'd or inconsistent between the table and
  any place that reads bucket names, `top_regions` keys will silently
  fragment (e.g. `EU-west` vs `EU-West`) rather than erroring.
- If compliance expects the finer buckets to also show up in any other
  reporting surface, and this plan does not update one, that surface will
  keep using the coarser regions — flag for review, out of scope as written.
- No test currently pins the exact `_REGION`-style mapping table, so a future
  change could re-coarsen buckets without a test failing unless the new tests
  from step 3 land.
