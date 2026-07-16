# Audit log schema

Each line the PostToolUse hook appends to artifacts/audit.log is one JSON
object. Design the schema so "show me every agent action on this repo in
March and who approved the gated ones" is a trivial query.

Required fields:
- ts:        ISO 8601 timestamp
- session:   session id
- agent:     role (explorer / implementer / tester / critic / synthesizer / main)
- tool:      tool name (Bash / Write / Edit / Read / ...)
- target:    file path or command
- decision:  allow / deny / gated
- approver:  human id when decision == gated, else null
