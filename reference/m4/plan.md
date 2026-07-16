# Technical Plan: cache the analytics summary

## Restated intent
`analytics.summary(conn, account_id)` recomputes from every ledger entry on
every call, which is slow for active accounts. Introduce a cache so repeated
calls for the same account do not require a full re-scan of `ledger` when
nothing relevant has changed, while keeping the summary reasonably fresh
after new ledger entries arrive.

This plan intentionally does not choose a caching strategy. Write-through
(update the cache on every posting, in the hot posting path) and cache-aside
with a TTL (compute lazily, cache, expire/invalidate) are both legitimate and
are evaluated separately, against the acceptance criteria below, as a
follow-on comparison.

## Explicit assumptions
- The cache is per `account_id`; there is no requirement to cache anything
  cross-account (e.g. bank-wide aggregates) in this change.
- Callers of `analytics.summary()` are not changed at the call-site level —
  the function keeps its current signature and return shape
  (`{"entries": int, "top_regions": {...}}`); caching is an implementation
  detail behind it.
- Cache state may live in-process (no new persistence table required) unless
  the chosen approach demands otherwise; this plan does not mandate storage.
- The plan commits to a maximum staleness bound once a strategy is chosen
  (write-through: effectively 0; cache-aside: bounded by the TTL). Whichever
  approach is implemented must state its bound explicitly and the tests must
  check against it.
- Cache correctness is judged by observable output equivalence to a full
  recompute, not by internal cache-hit bookkeeping.

## Implementation steps
1. Add a cache lookup at the top of `analytics.summary()` (or an equivalent
   wrapper) that returns a cached result when valid, and falls through to the
   existing recompute logic when not — `analytics.py`.
2. Add the cache write/invalidation hook appropriate to the chosen strategy:
   either update the cache when a ledger entry is recorded (write-through,
   touching `ledger.py`/`posting.py`) or set/refresh a TTL entry on compute
   (cache-aside, contained to `analytics.py`) — files depend on strategy.
3. Ensure the cache does not leak across `account_id`s and does not serve
   stale data across process restarts unless that is an explicitly accepted
   tradeoff for the chosen strategy.
4. Add tests proving no-op cache hits avoid a `ledger` re-scan, and that a
   new ledger entry is reflected within the committed staleness bound —
   `tests/`.

## Test expectations
- AC1: two identical `summary()` calls for the same `account_id`, with no
  new ledger entries recorded in between, return equal results, and the
  second call does not re-scan the `ledger` table (verifiable via a
  query-count/spy on the scan path, not by timing).
- AC2: a new ledger entry recorded for an `account_id` is reflected in
  `summary()`'s output for that `account_id` within the staleness bound the
  implemented strategy commits to (0 for write-through; the stated TTL for
  cache-aside).
- AC3: a ledger entry recorded for a *different* `account_id` does not
  change the cached summary of the `account_id` under test.
- AC4: after the cache is warmed for an `account_id` with zero ledger
  entries, `summary()` still returns `{"entries": 0, "top_regions": {}}`
  (empty state is cacheable, not a special case that bypasses the cache).

## Risks
- **Hot-path blast radius:** `posting.post()` is the public, most frequently
  hit path in the service. Any write-through hook added there that is slow,
  blocking, or can raise, risks slowing or breaking every posting — not just
  analytics reads. This must be measured, not assumed.
- **Staleness:** cache-aside trades hot-path safety for a window in which
  `summary()` can return an outdated count/region breakdown. Whatever bound
  is chosen must be stated in the acceptance criteria and enforced by a test,
  not left as an implicit "should be fast enough."
- Cache invalidation bugs (serving one account's cached data for another, or
  never invalidating) are the most likely production failure of this class of
  change and should be the first thing the critic checks for regardless of
  which strategy is implemented.
