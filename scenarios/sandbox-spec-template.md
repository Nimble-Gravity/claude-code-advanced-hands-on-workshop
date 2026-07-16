# Sandbox Specification (Day 2 Module 3)

Fill this in whether you build the sandbox or design it. If your environment
blocks Docker, this document IS the exercise deliverable.

## Chosen isolation tier
<hardened container / gVisor / MicroVM> and one sentence of why, tied to
ContosoBank's risk posture.

## The four boundaries

### Network
Default deny egress. Enumerate the exact allowed destinations (package cache?)
and nothing else.

### Filesystem
Worktree mounted how; dependencies read-only; scratch dir where. No home dir,
no shared mounts.

### Secrets
What the sandbox gets (answer should be: nothing, or synthetic credentials).
Real secrets never enter an environment that runs agent-generated code.

### Dependencies
Install source: internal proxy or lockfile only. An agent that can add an
arbitrary package has network egress with extra steps.

## Verification tests you would run
1. Attempt outbound HTTP (e.g. POST an API key or ledger batch to an
   external URL) from inside a test. Expect: blocked (`--network none`).
2. Open `sandbox/planted_secret.txt` and dump `os.environ` from inside a
   test. Expect: file unreadable / environment empty of host secrets. (Not
   `~/.ssh` or `.env` — neither exists in the image, so probing them fails
   for the wrong reason and never exercises the boundary.)
3. Attempt to write into an *existing* read-only directory outside the
   worktree, e.g. `/etc/contoso-escape-test.txt`. Expect: `EROFS`
   ("read-only file system") — not a made-up path like `/opt/evil/x`, which
   fails with `ENOENT` for the wrong reason and never reaches the boundary.
4. Run the legitimate suite. Expect: still green, by its own reported test
   count — don't assume a fixed number.
