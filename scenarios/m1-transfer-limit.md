# Module 1 scenario: Transfer-limiting the partner API

**Ticket (as received from the business):**

> ContosoBank's partner endpoints (the posting path and the JSON API) are
> getting hammered by a few misbehaving partners. Add a limit so we can cap
> how much a single caller can move. Ops wants "about 100" as the starting
> cap.

**Where it lives:** `src/contoso/posting.py` (the hot posting path) and the
API surface. `src/contoso/config.py` already defines `TRANSFER_LIMIT = 100`
alongside `THROTTLE_PER_SECOND = 20` and `DEFAULT_WINDOW_SECONDS = 60`.

**This ticket is deliberately underspecified.** Do not resolve the gaps
silently. Record a decision for at least these in your intent doc:

- What is the unit of `TRANSFER_LIMIT = 100` — dollars, a count of transfers,
  per window? (Note the neighbouring `THROTTLE_PER_SECOND`/
  `DEFAULT_WINDOW_SECONDS` imply different units — which one governs? It's
  money this time, so the ambiguity is worse than it looks.)
- Limit per partner API key, or per account?
- Fixed window or sliding window?
- On limit: 429 with `Retry-After`, or queue the transfer?
- Single-node counters, or shared across instances?

Use this for Module 1 (intent + plan only; no code is written in this module).
