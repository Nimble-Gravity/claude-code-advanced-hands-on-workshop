# Module 5 · Sample team run (facilitator fallback)

For attendees whose environment can't run Agent Teams (Claude Code older than
v2.1.32, or org policy blocking the experimental flag), this directory holds a
recorded run they can study for Parts A and B of the exercise. Parts C and D
still run live for everyone — the subagent baseline needs no flag.

## Facilitator: record this before the workshop

1. From the repo root, with the flag active (it ships in `.claude/settings.json`),
   run Part A of the module exactly as the notebook describes.
2. Capture into this directory:
   - `team-transcript.txt` — terminal capture of the lead session (`script` or
     tmux `capture-pane` both work)
   - `inboxes/` — copy of `~/.claude/teams/<team-name>/inboxes/*.json` taken
     right after the team reaches its decision
   - `cost.txt` — the `/cost` output for the team run
3. Repeat Part B (agreeable skeptic) and capture `inboxes-flipped/` the same
   way, so the debate-collapse diff is visible in the recording too.

Keep captures raw. The point is that attendees can see real teammate-to-
teammate mailbox traffic — an edited transcript defeats it.

**Nothing in this directory is committed yet** — if you're reading this at the
workshop and it's still empty, fall back to running Part A as a front-of-room
demo instead.
