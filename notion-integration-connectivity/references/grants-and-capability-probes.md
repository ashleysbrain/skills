# Notion Grants, Blindness, and Capability Probes (2026-08-18)

## Grant model — why auth works but nothing is visible
- An integration can return 200 on `/v1/users/me` and still see ZERO pages: pages must be shared with it (page ••• menu → Connections → select integration). Connect the ROOT page once; children inherit. Reversible from the same menu.
- A "blind" bot still sees the workspace member list; only page access is empty.
- Enterprise admin connection-settings path is a dead end: plan-gated, governs member installs, not page grants.
- A missing grant can sit unnoticed for days (observed: 4-day blind window 08-14 to 08-18) when monitoring only checks liveness.

## Capability probe (not liveness)
- Visibility health check = `GET /v1/search?page_size=1` expecting 200 AND ≥1 result. `users/me` 200 proves nothing about page access.

## Evidence discipline
- 404 response bodies are CANNED: byte-identical for valid-but-unshared IDs and random garbage UUIDs. A 404 never proves page existence or non-existence.
- Page IDs from browser session snapshots go stale (workspace copies/branches). Re-census via `/v1/search` after the grant lands; treat snapshot IDs as hints only.

## Token + config wiring
- the operator agent `mcp_servers` env interpolation accepts ONLY the braced form `${VAR}`; unbraced `$VAR` passes through as a literal string (interpolation regex in mcp_tool.py). Silently fatal — lint configs for unbraced forms at load time.
- Token lives in `<agent-home>/.env` only; never on a command line (background pollers leak it into `ps` output). Load it inside scripts.
- Verify MCP server restarts by FUNCTION (live 200 through the server), never by reading env from process listings (proven unreliable on macOS).
