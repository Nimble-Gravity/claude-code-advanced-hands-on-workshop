# REFERENCE (redacted) — Intent doc, Module 1 (rate limiting)

> This is a **bar to compare against, not an answer to copy.** Sections are
> shown with the *kind* of content that belongs in each; the hardest decisions
> are deliberately left as `[you decide]` so you still have to do the thinking.
> A strong intent doc is concrete where this one is blank.

## Feature
One paragraph: what the feature does in plain language. (Public API callers —
the posting endpoint and the JSON API — get capped at "about 100" requests
so a few abusive partners can no longer degrade the service for everyone
else.)

## Explicitly does NOT do
- Does not change `THROTTLE_PER_SECOND` or `DEFAULT_WINDOW_SECONDS` semantics
  for any other subsystem — those constants are reused here, not redefined.
- Does not add an admin override or allowlist for trusted callers. `[confirm:
  needed before rollout, or fast-follow?]`
- Does not apply to internal/service-to-service calls, only the public
  posting and JSON API surface.

## Decisions (the underspecified points, decided)
| point | decision | rationale |
| --- | --- | --- |
| unit of `TRANSFER_LIMIT = 100` | `[you decide: is 100 per-second, matching THROTTLE_PER_SECOND=20's neighbourhood, or per-window, matching DEFAULT_WINDOW_SECONDS=60?]` | `config.py` mixes per-second and per-window units — pick one |
| scope | `[you decide: per partner API key, or per account?]` | posting callers may be anonymous (no key); JSON API callers usually have one |
| window type | `[you decide: fixed window or sliding window?]` | fixed is simpler to reason about; sliding is fairer at window edges |
| on-limit behaviour | `[you decide: 429 with Retry-After, or queue the transfer?]` | affects client contract and whether callers need new retry logic |
| counter scope | single-node counters for the sandbox `[confirm: acceptable, or must this design for a shared/multi-instance counter store now?]` | no shared cache exists in this codebase today |

## Acceptance criteria (each a pass/fail statement about observable state)
- AC1: a caller that has not exceeded the limit within the current window
  receives a normal response (the transfer posts / JSON API responds 2xx).
- AC2: a caller that exceeds the decided limit within the decided window
  receives the decided on-limit response (e.g. 429) instead of a normal
  response, for every request beyond the limit until the window resets.
- AC3: `[you write: once the window resets (or the sliding window has aged
  out enough requests), the same caller can succeed again without any
  manual reset]`
- AC4 (scope check): a second caller under a different identity (partner
  API key/account, per the scope decision) is not affected by the first
  caller exceeding their limit.

## Open questions (what you could NOT decide, and who must)
- Is 100 meant as a hard cap ops can raise later, or a value they expect you
  to tune based on the unit decision above? Ops should confirm once the unit
  is picked.
- Does exceeding the limit need to be observable to ops (a metric/log line),
  or is returning 429 sufficient for v1?
