# Notion Team-Idea Ingestion — Verified Prerequisites (2026-08-18)

Class of task: absorb team input living in a SaaS workspace (Notion) into
the the OS task ledger. Everything below was measured live; nothing is
inferred.

## The share-wall (durable Notion platform behavior)
An internal integration token can be fully valid and still see NOTHING:
- `GET /v1/users/me` → 200, correct bot + workspace
- `POST /v1/search` → 200 with `"results": []` (empty list, not an error)
- `GET /v1/pages/{id}` → 404 `object_not_found`, message names OUR
  integration ("Make sure the relevant pages and databases are shared
  with your integration ...")

That signature = empty page-connection grant set. Notion requires each
page tree to be manually connected: open page → ••• → Connections →
select the integration (children inherit). Only a workspace owner can do
it; there is NO admin-console bypass (the Enterprise "connection
settings" console governs which connections members may install, not
page grants). Source: developers.notion.com/docs/authorization, fetched
live during the session.

Diagnostic rule: the 404 naming your integration is PROOF the token is
valid and pointed at the right workspace — do not re-audit credentials
once seen.

## ntn CLI quirks
- Search requires an explicit method flag: `ntn api v1/search -X POST`.
  Bare `ntn api v1/search` → 400 invalid_request_url.
- Headless env: `export NOTION_API_TOKEN=$NOTION_API_KEY` and
  `NOTION_KEYRING=0` (keyring fallback file ~/.config/notion/auth.json
  holds the same token).

## Recovering page IDs when the API sees nothing
Chrome profile `Sessions/*Tabs` snapshot files hold recently open URLs:
`strings "<profile>/Sessions/"* | grep -i notion.so` — yields page IDs
and the `spaceId` (confirm it matches the token's workspace_id from
users/me). Probes against recovered IDs confirm "exists but unshared"
via the 404 text above.

## MCP parallel pipe (independent failure class)
`@notionhq/notion-mcp-server` reads its token from env `NOTION_TOKEN`
(check `npx notion-mcp-server --help`). the operator agent config needs:
```yaml
  notion:
    args: [-y, '@notionhq/notion-mcp-server@2.2.1']
    command: npx
    enabled: true
    env:
      NOTION_TOKEN: $NOTION_API_KEY
```
Two gotchas: (1) a running server keeps its OLD environment until the
gateway restarts — re-verify the MCP path after restart, not before;
(2) concurrent `hermes config` CLI writes + manual python edits can
double-write duplicate `env:` keys — always re-parse the YAML after any
config write and dedupe.

Second-order fault rule: when one pipe is blocked, audit sibling pipes
for independently-broken paths that would re-confirm the blocker AFTER
the primary fix lands (the tokenless MCP server would have kept reading
"zero pages" even after the page grant).

## Unlock watcher pattern
Background loop polling the known page IDs every 20s:
`curl -s -o /dev/null -w '%{http_code}' .../v1/pages/{id}` → first 200
fires ingestion. Log every ~15 polls; exit on unlock. Keeps the principal's
one manual action (the Connections click) from blocking the session.

## Framing law (Bichat verdict, gated PASS 2026-08-18, verbatim)
"the operator agent conflated where the fix is performed (Notion's UI) with whose
action it is (ours, administratively)." When reporting a blocker on a
vendor boundary, state BOTH: the boundary lives on the vendor's server,
but crossing it is our side's administrative action. "The break is on
X's side" reads as a defect accusation and invites the principal's correct
rebuttal when nothing on X's side malfunctions.

## Gate battery reminder
No GNU `timeout` on macOS — see SKILL.md CI discipline section.
