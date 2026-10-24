# Notion Connection Session — 2026-08-14

Full session detail backing `notion-integration-connectivity`. Context: wiring
the Divinity Science organism into Notion (HQ + the specialist engine pages) for elite
agent-brain orchestration. Connection itself ended blocked on the human UI
step (sharing pages with the integration); everything below the UI step was
live-verified.

## Machine environment (verified)

- Node: `/<workspace>` v22.23.1, npm 10.9.8.
- `npm prefix -g` = `/<workspace>` → global installs land in `~/.local/bin`.
- `~/.local/bin` NOT on default session PATH. All ntn subprocess calls need:
  `env = dict(os.environ, PATH="/<workspace>:"+os.environ["PATH"])`.
- `ntn` 0.22.1 via `npm install -global ntn` after the curl installer
  (`curl -fsSL https://ntn.dev | bash`) produced no working binary.

## Probe transcript (sequence that worked)

1. MCP `API_get_self` → 401 "API token is invalid" (stale mcp-notion token).
2. `ntn` absent everywhere → npm install → verified `ntn 0.22.1`.
3. `ntn api v1/users` with `NOTION_API_TOKEN` + `NOTION_KEYRING=0` env →
   rc 0, workspace users listed (the principal Williams, Angela McGrady, ...) —
   token valid, workspace = divinityscience.com team space.
4. Search for "Divinity Science HQ", "the specialist engine", etc. → 0 results each.
5. Raw curl `POST /v1/search` with `{"page_size":100}` → `results: []`,
   `has_more: false` → confirmed: no pages shared with integration.
6. Blocked on human UI step (user could not find Connections in ••• menu;
   guided to Share button popup route; session ended before confirmation).

## Credential commands executed (working)

```bash
# <agent-home>/.env (append)
NOTION_API_KEY=ntn_...
NOTION_API_TOKEN=ntn_...
NOTION_KEYRING=0

# ~/.config/notion/auth.json
{"token": "ntn_..."}

# probe
export NOTION_API_TOKEN=... NOTION_KEYRING=0
ntn api v1/users
curl -s -X POST https://api.notion.com/v1/search \
  -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H "Notion-Version: 2025-09-03" -H "Content-Type: application/json" \
  -d '{"page_size": 100}'
```

## ntn CLI failure modes observed

- `ntn api v1/search` with NO body → non-JSON error output, not scriptable.
- `--json -` stdin flag → "unexpected argument '--json'" (rc 2). Not supported.
- rc 4 = "No workspace selected" (no credentials found).
- rc 5 = inline request input parse error.

## Unresolved at session end

- Page sharing UI step: user reported Connections not findable in ••• menu.
  Guided to Share-button route (documented, not confirmed in our workspace).
  Next session: re-probe search FIRST; if results > 0, sharing succeeded and
  the HQ/Space population work can proceed.
- The the operator agent mcp-notion server config still holds the stale token — needs the
  new token wired wherever that server's env is configured.
