# nimble gravity

## Advanced Claude Code Workshop

A two-day hands-on workshop teaching advanced Claude Code techniques: agentic
workflows, multi-agent orchestration, planning, evaluation, and enterprise
governance. You'll practice these concepts on ContosoBank, a realistic sandbox
bank service with real-world constraints - transfers, analytics, webhooks, API
key management - so the patterns transfer directly to production codebases.

**Day 1:** Build the core agentic pipeline (intent → plan → explore → critique →
implement → test). **Day 2:** Govern that pipeline with threat modeling,
permissions, sandboxing, hooks, and prompt injection defense.

## Workshop Schedule

**2 Days, 9:00 AM – 4:30 PM**

### Day 1 — Agents, Pipelines, and Agentic Architecture

| Time | Block |
| --- | --- |
| 9:00 AM – 9:15 AM | Open |
| 9:15 AM – 10:05 AM | M1 — Intent to Pipeline |
| 10:05 AM – 10:50 AM | M2 — Execution Harness |
| 10:50 AM – 11:05 AM | ☕ Break |
| 11:05 AM – 12:00 PM | M3 — Subagents |
| 12:00 PM – 12:45 PM | 🍽 Lunch |
| 12:45 PM – 1:35 PM | M4 — Worktrees |
| 1:35 PM – 2:25 PM | M5 — Agent Teams |
| 2:25 PM – 2:40 PM | ☕ Break |
| 2:40 PM – 3:25 PM | M6 — Evaluation Loops |
| 3:25 PM – 3:30 PM | Capstone setup |
| 3:30 PM – 4:25 PM | Capstone (work) |
| 4:25 PM – 4:45 PM | Capstone readout & close |

### Day 2 — Control, Security, and Enterprise-Readiness

| Time | Block |
| --- | --- |
| 9:00 AM – 9:15 AM | Open |
| 9:15 AM – 10:05 AM | M1 — Threat Model |
| 10:05 AM – 10:50 AM | M2 — Permission Modeling |
| 10:50 AM – 11:05 AM | ☕ Break |
| 11:05 AM – 12:00 PM | M3 — Sandboxing |
| 12:00 PM – 12:45 PM | 🍽 Lunch |
| 12:45 PM – 1:30 PM | M4 — Bounded Workflows |
| 1:30 PM – 2:20 PM | M5 — Hooks as Control Plane |
| 2:20 PM – 2:35 PM | ☕ Break |
| 2:35 PM – 3:30 PM | M6 — Prompt Injection |
| 3:30 PM – 3:35 PM | Capstone setup |
| 3:35 PM – 4:25 PM | Capstone (work) |
| 4:25 PM – 4:45 PM | Capstone readout & workshop close |

## Agenda

### Day 1 — Building the Pipeline

Notebooks: `notebooks/day1/`

| Module | Focus | Ticket |
|---|---|---|
| 1 | Intent + plan, no code | `scenarios/m1-transfer-limit.md` |
| 2 | Planning via a `/plan-feature` command | `scenarios/m2-search.md`, `scenarios/m2-void.md` |
| 3 | Explore + critique before touching code | `scenarios/m3-explore-analytics.md` |
| 4 | Compare two implementation approaches | `scenarios/m4-cache-analytics.md` |
| 5 | Full pipeline: implement, catch a real defect | `scenarios/m5-webhooks.md` |
| 6 | Tests generated from acceptance criteria | `scenarios/m6-key-ttl.md` |
| Capstone | Unseen ticket, full pipeline | `scenarios/capstone-expiring-holds.md` |

### Day 2 — Governing the Pipeline

Notebooks: `notebooks/day2/`. Modules 1, 2, and 5 apply a security lens to
Day 1's own tickets and canned inputs (see `reference/day2/`); modules 3, 4,
6, and the capstone have their own tickets.

| Module | Focus | Ticket / reference |
|---|---|---|
| 1 | Threat-model the pipeline itself | `templates/threat-model.md`, `reference/day2/m1/pipeline.md` |
| 2 | Permission modeling for agents/subagents | `reference/day2/m2/agents/` |
| 3 | Sandboxed test execution (Docker) | `sandbox/`, `scenarios/sandbox-spec-template.md` |
| 4 | A ticket the pipeline must refuse to force-green | `scenarios/d2-m4-impossible.md` |
| 5 | Hooks as a control plane | `hooks/` |
| 6 | Running the pipeline over a poisoned tree | `scenarios/d2-m6-add-analytics-field.md` |
| Capstone | Signed/expiring webhooks + adversarial acceptance | `scenarios/d2-capstone-signed-webhooks.md`, `scenarios/d2-capstone-adversarial.md` |

## How the workshop is structured

Each day is **six independent module labs plus a capstone**. Unlike a single
end-to-end pipeline that you build up module by module, each module here is
fully self-contained:

- its own ticket in `scenarios/`
- its own canned inputs (plans, agents) in `reference/`, where the module
  needs one
- its own output directory, `artifacts/m<N>/` (Day 1) or `artifacts/day2/m<N>/`
  (Day 2)

That means you can start on any module cold, in any order, without having
completed the others first. If you only have time for Module 4, you can jump
straight there — you don't need Module 1's or Module 2's artifacts to do it.

## The pipeline spine

Several modules exercise stages of the same underlying pipeline shape:

```
intent → plan → explore → critique → implement → test → synthesize
```

Each stage's contract is defined once, domain-neutrally, so it can be reused
across modules and scenarios:

- `templates/intent.md`, `templates/plan.md` — the artifact shapes every
  stage reads and writes.
- `starter-agents/*.skeleton.md` — read-only explorer/critic, and
  implementer/tester/synthesizer skeletons you complete during the modules
  that need them (see the `# TODO (Module N)` markers in each file).

The key difference from a typical pipeline exercise: here, no module depends
on another module's artifacts to run. Each module hands you what it needs
(a ticket, and where relevant a canned reference plan/agent) so the pipeline
stages can be practiced and evaluated in isolation.

## Quick start

See `QUICKSTART.md` for the dev-container option (recommended — comes with
`uv`, Python, the Claude Code CLI, `gh`, and Docker preconfigured, so you can
skip the local Python setup below entirely).

### Python environment setup (local)

Requires Python 3.11+ and [`uv`](https://docs.astral.sh/uv/) — uv manages
both, so you don't need to pre-install a matching Python yourself.

1. **Install uv** (skip if already installed):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh   # macOS/Linux
   # or: pipx install uv / brew install uv
   ```

2. **Sync the environment.** This creates a `.venv/` in the repo root and
   installs everything pinned in `uv.lock` (pytest, JupyterLab, and the
   sandbox's own dependencies) — no manual `pip install` needed:

   ```bash
   uv sync
   ```

3. **Verify the sandbox works** and seed its demo data:

   ```bash
   uv run pytest                      # expect green
   uv run python -m contoso.seed
   ```

4. **Launch JupyterLab inside the synced environment:**

   ```bash
   uv run jupyter lab notebooks/
   ```

   `uv run` executes Jupyter using `.venv/`, so the notebooks already see the
   `contoso` package and its dependencies — no separate kernel install step
   needed. If you instead open the notebooks from an IDE (e.g. VS Code) rather
   than `uv run jupyter lab`, point its Jupyter/Python interpreter at
   `.venv/bin/python` so it picks up the same environment.

Then open any module's notebook under `notebooks/day1/` or `notebooks/day2/`
— they don't need to be run in order. Day 2 Module 3's primary exercise needs
Docker; see `sandbox/README.md` for the no-Docker fallback.

**Troubleshooting:** if a notebook can't import `contoso`, confirm you're
running it via `uv run jupyter lab` (or the `.venv` interpreter) rather than a
system/global Jupyter install. If `uv sync` fails on the Python version, run
`uv python install 3.11` first, then re-run `uv sync`.

## Repo layout

- `src/contoso/`, `tests/` — the sandbox service itself (see the top-level
  `CLAUDE.md` for its conventions).
- `templates/` — domain-neutral artifact shapes (intent, plan, Day 2 threat
  model).
- `starter-agents/` — skeleton subagents to complete during the labs.
- `scenarios/` — one ticket per module, each deliberately scoped and, where
  noted, deliberately underspecified. `d2-*` scenarios are Day 2's.
- `reference/` — canned inputs (plans, agents) for modules that provide them;
  Day 1's live at the top level (`m1/`, `m3/`, ...), Day 2's under `day2/`.
- `sandbox/` — Docker infra for Day 2 Module 3's isolated test execution.
- `hooks/` — reference PreToolUse/PostToolUse/Stop hooks for Day 2 Module 5.
- `.claude/` — settings baseline; `agents/` and `commands/` are where your
  completed subagents and slash commands go.
- `artifacts/` — gitignored working output per module; only this README is
  tracked.
