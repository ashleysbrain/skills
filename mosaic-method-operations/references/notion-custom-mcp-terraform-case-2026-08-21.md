# Notion custom-MCP terraform case (stage 1-2, 2026-08-21) — vendor facts + the two-direction frame

Registry entry `notion-workspace`, advanced `unprobed -> manual-digested`
(brief: `~/your-workspace/technology-registry/BRIEF-NOTION-CUSTOM-MCP.md`;
`tech.manual_digest` event on file). Adversarial 6-seat panel verdicts:
`technology-registry/REVIEW-NOTION-CUSTOM-MCP.md`. Protocol: PROTOCOL-TECH-TERRAFORM.md.

## The frame that matters
Two directions, do not conflate:
- **DIR-A (we -> Notion):** our MCP client calling Notion's hosted MCP —
  ordinary, already live via native client.
- **DIR-B (Notion -> us):** a Notion Custom Agent connects to a DS-HOSTED
  custom MCP bridge; the organism becomes addressable from inside the
  client's Notion. This is the new capability class.

## Source-stamped vendor facts (claimed, not measured)
- Custom MCP connections: **Business/Enterprise plans only**; admin must
  toggle "Enable custom MCP servers" (+ optional approved-only list).
- Auth: OAuth (needs Dynamic Client Registration, else Notion pre-register)
  OR header/bearer. Per-connection, per-agent; NOT shareable across agents.
- Custom server must expose a **publicly reachable URL** (hosted relay/tunnel
  needed for localhost engines).
- MCP connections have read/write but **no trigger capabilities** — pull-only;
  event-driven fans stay on our side of the bridge (anti-cron law preserved).
- Write tools default to per-action confirmation; per-tool enable/disable;
  run-automatically vs always-ask vs always-allow.
- Rate limits: ~180 req/min per user, search 30/min, plus a plan-scaled
  workspace-shared limit.
- `notion-fetch {id: "self"}` returns workspace identity +
  `current_tool_access` plan map — the ideal stage-3 identity/plan probe.
- Unauthenticated `POST https://mcp.notion.com/mcp` returns **401 +
  `www-authenticate: Bearer` + resource_metadata URL** (recorded verbatim;
  use as the no-auth boundary check).

## Options under panel attack (graded in REVIEW file)
OPT-1 read-only Health Cockpit bridge; OPT-2 this-as-terraform-case-#2;
OPT-3 B2B client cockpit product surface; OPT-4 skill loop
(convert-page-to-skill + Research Library sync).

## Hard gates before any build
1. Workspace plan tier (Business/Enterprise?) — principal-confirmed fact required.
2. Public-URL exposure decision (tunnel vs hosted relay) — barrier audit.
3. Two-circulations law: B2C personal data never enters a Notion agent;
   PERSONA zones never write back; write tools stay always-ask in v1.

## Process-flow lesson (minted T-260821-0190)
SaaS-platform features are invisible to a model-ID radar; "understand new
tech quickly" needs changelog/webhook + bus-ping detection inputs,
event-driven — not the 2880m cron bridge (anti-cron law).
