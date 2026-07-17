# Agents

Completed subagents live here. Copy a skeleton from `starter-agents/`, drop the
`.skeleton` suffix, and fill in the `# TODO` sections. Target filenames:
`explorer.md`, `critic.md`, `implementer.md`, `tester.md`, `synthesizer.md`.
The `tools:` frontmatter line is the role's capability whitelist — keep the
read-only agents read-only.

Three definitions ship pre-built for Module 5's agent team: `shipit.md`,
`skeptic.md`, and `merchant.md`. They double as **teammate types** — spawn a
teammate "using the skeptic agent type" and the definition's body becomes part
of that teammate's system prompt, with its `tools:` line still enforced. Module
5's Part B asks you to edit `skeptic.md`; restore it afterwards (`git checkout
-- .claude/agents/skeptic.md`).
