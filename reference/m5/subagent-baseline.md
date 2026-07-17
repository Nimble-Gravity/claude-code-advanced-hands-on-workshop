# Module 5 · Subagent baseline (the control run)

This is the **subagent** version of the Module 5 ticket — the control group you
compare the agent team against. Run it in a **fresh** Claude Code session (so
`/cost` measures only this run), from the repo root.

Paste the prompt below verbatim. It uses classic subagents (Module 3): workers
with their own context that report **back to you** — no shared task list, no
peer-to-peer messages, one coordinator owning all state.

---

## The prompt

```text
Work scenarios/m5-webhooks.md using subagents only — no agent team.

1. In parallel, launch two read-only subagents:
   - one using the explorer agent definition in reference/m5/explorer.md,
     to map how webhooks.deliver() would be wired into posting.post()
   - one using the critic agent definition in reference/m5/critic.md,
     to attack the naive synchronous wiring for failure modes
2. When both report back, decide whether any implementation should proceed.
   If the critic's blocker stands (slow/failing merchant endpoint blocks or
   fails the posting; retry double-delivers transfer.posted), do NOT wire the
   call in.
3. Write your decision to artifacts/m5/subagent-run.md as:
   - Decision: SHIP / REVISE / ESCALATE
   - Evidence: the specific failure modes, citing files
   - What would make ESCALATE become SHIP

Do not edit any source files unless the critic clears the approach.
```

## Record your numbers

When the run finishes, run `/cost` in the same session and append to
`artifacts/m5/subagent-run.md`:

```text
## Measurements
- Total tokens (from /cost):
- Wall clock (rough):
- Final decision:
```

## What to expect

Same correct answer as the team — an ESCALATE-shaped "don't wire it inline
without isolating delivery" — at a fraction of the tokens. The explorer and
critic never talk to each other; you (one context) integrate their reports.
That's the trade the module measures: no debate, much cheaper.
