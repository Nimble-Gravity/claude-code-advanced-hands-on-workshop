# sandbox/

Infrastructure for Day 2 Module 3 (sandboxed test execution).

- `Dockerfile`         minimal, non-root, no baked secrets
- `run-sandbox.sh`     runs the suite with the four boundaries enforced
- `planted_secret.txt` a concrete secret for the escape test to target

## Primary exercise (requires Docker)

```bash
./sandbox/run-sandbox.sh
```

Runs `pytest` inside a container with network disabled, a read-only filesystem
except a scratch tmpfs and the `artifacts/` mount, only the worktree mounted,
and no host environment inherited.

Then have your implementer produce a test file that (a) attempts an outbound
HTTP call (e.g. POSTing api-key or ledger data to an external URL), (b) attempts
to read `sandbox/planted_secret.txt` and dump `os.environ` (not `~/.ssh` or
`.env` — neither exists in the image, so probing them fails for the wrong
reason and never exercises the Secrets boundary), and (c) attempts to write
into an *existing* read-only directory, e.g. `/etc/contoso-escape-test.txt`
(not a made-up path like `/opt/evil/x` — a missing parent directory fails
with `ENOENT` before the write ever reaches the read-only-filesystem check;
only a write into a real existing directory fails with the `EROFS` that
actually proves the boundary). Run the suite again and record in
`artifacts/day2/m3/sandbox-verification.md` what was blocked, allowed, or
partially blocked, then confirm the legitimate suite still passes (compare
its own reported test count — don't assume a fixed number).

## Fallback (no Docker)

Do not build; design. Fill in `scenarios/sandbox-spec-template.md` for ContosoBank,
then attack your own spec: list the three most likely ways an agent-generated
payload defeats it, and patch the spec.
