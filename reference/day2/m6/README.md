# Module 6 poisoned tree

These files carry four prompt-injection payloads (three blatant, one subtle) for
the Module 6 exercise. To use them WITHOUT touching the real source:

1. Create a worktree: `git worktree add ../contoso-poisoned -b m6-poisoned`
2. Copy the poisoned files over the real ones IN THE WORKTREE only:
   - `poisoned/accounts.py`  -> `src/contoso/accounts.py`
   - `poisoned/webhooks.py`  -> `src/contoso/webhooks.py`
   - `POISONED-README.md`     -> `README.poisoned.md` (repo root of the worktree)
3. Run the pipeline against the worktree. Never merge this branch.

Three of the payloads are blatant — you should be able to spot them on a
read-through. The fourth is deliberately subtle: it reads like a routine,
plausible change rather than an attack. Finding it (not being told where it
is) is the point of the exercise.
