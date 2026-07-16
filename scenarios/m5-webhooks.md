# Module 5 scenario: Deliver payment webhooks on transfer.posted

**Ticket (as received from the business):**

> Merchants want a webhook fired when one of their transfers posts. Wire
> `webhooks.deliver` into the posting path.

**Where it lives:** `src/contoso/webhooks.py` (`deliver()` is naive and
synchronous), `src/contoso/posting.py` (the posting path).

**The naive wiring has a real defect for your pipeline to catch:** firing the
webhook synchronously in the posting path (or after the posting commit without
isolation) means a slow or failing merchant endpoint loses postings or
double-delivers on retry. The pipeline must surface this, not force a green
run.

Canned explorer and critic agents are provided under `reference/m5/`.

Use this for Module 5.
