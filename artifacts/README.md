# Artifacts

Each module writes its outputs under its own subdirectory so modules never
collide or depend on each other:

- `m1/` intent.md, plan.md, plan.2.md
- `m2/` plan-search.md, plan-softdelete.md
- `m3/` plan.md (copied from reference), exploration.md, critique.md
- `m4/` plan.md (copied), comparison.md
- `m5/` synthesis.md
- `m6/` plan.md (copied), tests.md, eval-loop.md
- `capstone/` the full packet

This directory is gitignored except this README.
