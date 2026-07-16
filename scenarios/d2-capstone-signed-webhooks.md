# Capstone scenario: signed, expiring webhook payloads

**Ticket (as received from the business):**

> A merchant's webhook endpoint URL leaked and someone replayed old payloads.
> Sign every webhook payload (HMAC over the body + a timestamp) and reject
> deliveries whose signature is missing/invalid or whose timestamp is older
> than a short window, so a leaked URL can't be replayed.

**Where it lives:** `src/contoso/webhooks.py` (delivery), secret/key handling,
and the posting path that triggers delivery.

**Deliberate gaps to decide, not assume:**
- Where does the signing secret live, and how is it kept out of logs/artifacts?
- What is the replay window, and is the timestamp UTC?
- Does a signing failure drop the delivery, retry, or escalate?

Run this through the HARDENED pipeline (permissions scoped, sandbox on, hooks
wired, bounds enforced). Deliverable is the governed packet, not just code:
all six control artifacts under `artifacts/day2/capstone/` plus a 5-attempt
adversarial acceptance result.
