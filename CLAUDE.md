# ContosoBank Sandbox Service

Training sandbox modeled on a small partner-API bank: money movement + account
activity reporting. Used in the Advanced Claude Code workshop, Day 1 and
Day 2.

## Conventions

- Source lives in `src/contoso/`. Tests live in `tests/`.
- Run tests with `uv run pytest`.
- All persistence goes through `contoso.db`. No raw sqlite3 connections elsewhere.
- Counts and IDs are integers. Amounts are integer minor units (cents).
  Timestamps are UTC ISO-8601 strings via `contoso.models.now()` / `iso()` /
  `parse()`.

## Layout

- `transfers.py` create/look up transfers and authorization holds;
  `posting.py` public posting path (authorize + record a ledger entry).
- `ledger.py` ledger entry recording/counting; `analytics.py` per-account
  activity summary.
- `reporting.py` monthly statement and the canonical country→region bucketing.
- `accounts.py` accounts and partner API keys (TTL from last use).
- `webhooks.py` payment webhook registration and delivery.
- `config.py` runtime constants.

## Recording example notebook runs

When running through a `notebooks/day*/moduleN_*.ipynb` end-to-end, save
proof of a successful run under `notebooks/examples/<module_name>/run-<date>.md`
(e.g. `notebooks/examples/module1_intent/run-2026-07-13.md`). One file per
run, date in filename so repeat runs don't collide.

Log must demonstrate execution succeeded **without leaking the solution**:

- Cell-by-cell stdout for setup/grounding cells (safe — no answers in them).
- Artifact metadata only for anything the participant writes by hand
  (intent docs, plans, code): word/line counts and a sha256 hash, never
  the file's actual prose/code.
- Self-check / verification cell output in full (checklists, gap matrices,
  pass/fail tables) — these reflect back structure, not the answer itself.
- A short "Result" section summarizing what passed/failed.
- A "Notes / anomalies" section for anything that broke, was skipped, or
  needs facilitator attention (env issues, cells not executable in this
  environment, optional steps not run).

Never copy the actual `artifacts/**` file contents into `notebooks/examples/`.
The point is a facilitator can verify a module runs cleanly without the
example doubling as a published answer key.
