# PENDING SKILL.md EDITS — pass 23 / MCP production (2026-08-18, hermes)

Background-curator patch was blocked by the _read_before_write guard
(known quirk: dedup skill_view never counts toward it; new-file writes
pass). Apply these hunks to SKILL.md in a foreground/curator pass.

## Hunk 1 — Package map: add MCP adapter line

Insert after the `stores/task-ledger.db` bullet (before the
PROCESS-FLOWS.md bullet):

```
- `adapters/mcp/` — the gates as stdio MCP tools (8 incl. mosaic_dispatch
  WHO+WHICH join). Registered in hermes config + sibling-agent.jsonc with
  ABSOLUTE paths — tilde does NOT expand in MCP subprocess spawn. Anti-rot:
  `python3 adapters/mcp/mcp_roundtrip_test.py` runs in CI every push.
  Roadmap: docs/MCP-PRODUCTION-ROADMAP.md; session detail:
  references/mcp-production-2026-08-18.md.
```

## Hunk 2 — CI discipline section: machine-state independence + cron sweep hazard

Replace the first sentence of the CI discipline section:

OLD:
```
Gate battery + store-manifest integrity + surgical chain-ok on every
push.
```

NEW:
```
Gate battery + store-manifest integrity + surgical chain-ok + MCP
round-trip on every push. CI tests must be MACHINE-STATE INDEPENDENT:
assert the contract with branch-correct invariants (dispatch GO when
the technology-registry exists; fail-stop REFUSE naming the registry
when it doesn't — both correct), never hardcode GO (run 32174366797
died to that). The overnight-volley cron commits ANY dirty working tree
in its bus-intake tick — commit promptly after VERIFY or in-flight edits
land in the cron's commit and fail ITS run first (observed run
32174241976).
```

## Hunk 3 — References list: add session detail pointer

Append to the References section:

```
- `references/mcp-production-2026-08-18.md` — MCP server production
  wiring: market findings, pydantic-core ABI fix, era-safe negotiation,
  dual-harness registration, CI round-trip gate.
```
