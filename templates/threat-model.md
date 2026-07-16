# Pipeline Threat Model

One row per stage per capability.

| Stage | Action | Untrusted inputs | Reach (creds/repos/env/data) | Blast radius | Likelihood | Impact | Control (prevent/gate/detect/accept) |
|-------|--------|------------------|------------------------------|--------------|------------|--------|--------------------------------------|
| explorer | read | repo, comments, docs | read-only repo | reports poisoned claim as fact | | | |
| implementer | write | plan, artifacts | src/, tests/ | writes hostile code | | | |
| tester | execute | test files, deps | test runner, package scripts | runs arbitrary code | | | |
| ... | | | | | | | |

## Example: Same risk, different ease-of-mitigation

These two rows show why ease-of-mitigation matters for backlog ordering:

**Trivial mitigation** (cheap, high-impact fix):
| tester | conftest.py import-time code execution | test files the implementer wrote | arbitrary Python execution at collection | ledger/filesystem/network access | High | High | **prevent** | Add `conftest.py` to mandatory code review checklist — one-line policy |

**Expensive mitigation** (architecture-level fix):
| tester | conftest.py import-time code execution | test files the implementer wrote | arbitrary Python execution at collection | ledger/filesystem/network access | High | High | **prevent** | Isolate test runner in network-blocked sandbox with import-time hook restrictions — infrastructure change |

Both rows have the same likelihood and impact. The first should rank **much higher** in your backlog because the mitigation is trivial. That's what "ordered by L×I×ease-of-mitigation" means: cheap wins float to the top.

---

## Top 5 hardening backlog (ordered)
Sort by likelihood × impact × ease-of-mitigation. Cheap, high-value fixes rank above expensive ones even if the risk is lower.

1.
2.
3.
4.
5.
