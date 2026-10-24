---
name: notion-integration-connectivity
description: "Use when wiring Notion API access or fixing Notion 401s."
version: 1.0.1
category: productivity
author: hermes
license: MIT
tags: [Notion, API, authentication, ntn, troubleshooting]
related_skills: ["notion"]
trigger:
  - Connecting an agent or CLI to a Notion workspace for the first time
  - Notion API returns 401 unauthorized
  - Notion API authenticates but search returns zero results
  - Installing or scripting the ntn CLI
  - User pastes a Notion integration token or asks how to connect Notion
---

# Notion Integration Connectivity

## When to Use

- First-time wiring of any agent, CLI, or MCP server to a Notion workspace.
- Notion API returns 401, or authenticates but sees zero pages.
- Installing the `ntn` CLI or scripting against the Notion API.

Credential wiring, permission-model diagnosis, and CLI setup for Notion API
access. Verified live 2026-08-14 (macOS, Notion-Version 2025-09-03, ntn 0.22.1).
The bundled `notion` skill covers general API usage; THIS skill covers getting
connected and diagnosing the two classic failure states.

## Diagnosis chain (the two failure states)

State 1 — **401 unauthorized** (e.g. from an MCP Notion server):
the stored token is invalid/stale. Re-wire credentials (below).

State 2 — **authenticated but search returns 0 results**:
`ntn api v1/users` (or GET /v1/users) succeeds and lists workspace users,
but search returns empty with no error. This is Notion's permission model:
an integration sees NOTHING until pages are explicitly shared with it.
No API call can self-share pages — a human must do it in the Notion UI.

Probe order: check auth with `/v1/users` first, THEN interpret search results.
A valid token + empty search = permissions, not a bug.

## Credential storage points (set all of them)

1. `<agent-home>/.env`:
   `NOTION_API_KEY`, `NOTION_API_TOKEN` (ntn reads this), `NOTION_KEYRING=0`
   (disables OS-keychain prompts for headless use).
2. `~/.config/notion/auth.json`: `{"token": "ntn_..."}` — ntn file-based creds.
3. Any MCP Notion server config in the operator agent — a stale token here keeps returning
   401 even after (1) and (2) are fixed.

## Sharing pages with the integration (human UI step)

Documented Notion behavior (label: not yet user-confirmed in our workspace):
page-level connection lives under the **Share button popup → Connections**
area (older guidance says ••• → Connect to; users report it missing there).
Broad alternative (admin): workspace Settings → Connections → integration →
"All pages" access. If the Share popup shows no connections area at all,
suspect (a) insufficient page rights, or (b) integration created in a
different workspace than the target pages (check the workspace selector at
notion.so/my-integrations) — fix = recreate integration in the right
workspace and re-wire the token in all three storage points.

## ntn CLI install and quirks

- Install: `curl -fsSL https://ntn.dev | bash` — can complete WITHOUT placing
  a working `ntn` on PATH. Verified fallback: `npm install -global ntn`
  (needs Node 22+). Check `npm prefix -g`; the binary lands in that bin dir,
  which is often NOT on the default PATH — prepend it in subprocess env.
- Meaningful ntn exit codes: rc 4 = no workspace selected (no creds),
  rc 5 = inline input parse error. ntn 0.22.1 has no `--json -` stdin piping;
  for scripted queries use direct curl with headers: `Authorization: Bearer
  $TOKEN`, `Notion-Version: 2025-09-03`, `Content-Type: application/json`.

## References

- `references/connection-session-2026-08-14.md` — full session detail:
  machine-specific env facts, exact probe transcripts, storage commands.
