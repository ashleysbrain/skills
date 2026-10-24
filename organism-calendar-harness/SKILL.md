---
name: organism-calendar-harness
category: software-development
description: Use when working on the Organism Calendar Harness in the operator agent Ops.
version: 1.0.0
---

# Organism Calendar Harness

The temporal mesh layer for the the operator agent Ops Platform. Visualizes AI/human task work across time with dual-lane rendering. Built after 3 adversarial review passes (32 gaps found and addressed).

## Architecture

**Read-aggregation layer. NOT source of truth.** Pulls from existing systems, renders unified timeline, writes back to sources that support it.

### Components

| Component | File | Owner | Port |
|-----------|------|-------|------|
| Calendar Engine JS | `gg3-ops/html/calendar-engine.js` (566 lines) | hermes | served by proxy |
| Standalone Page | `gg3-ops/html/organism-calendar.html` (84 lines) | hermes | :9300 |
| the operator agent Ops Tab | `gg3-ops/html/gg-ops-platform.html` (ws-calendar) | hermes | :9300 |
| Calendar API | `gg3-ops/gg3_gateway.py` (endpoints) | sibling-agent | :port |
| Calendar DB | `gg3-ops/organism_calendar.db` | sibling-agent | - |
| Source Adapters | in gg3_gateway.py (Cron, Engine, Pipeline, Writing) | sibling-agent | - |

### API Endpoints (on :port)

- `GET /api/calendar/mesh?days=30&silo=gg3` — unified timeline (returns `dedupe_stats` + `dynamics_macro` since bus #5972)
- `GET /api/calendar/day/:date` — day view with computed lanes
- `GET /api/calendar/health` — adapter health status
- `GET /api/calendar/brief?format=text` — daily summary for Telegram
- `GET /api/calendar/changes?since=ISO8601` — status-only diff
- `GET /api/calendar/handshakes?limit=100&item_ref=` — cross-layer exchange log (info/opportunities/gaps)
- `POST /api/calendar/handshake` — log a cross-layer exchange (422 on unknown layer/wrong type; layer vocab: source|mesh|triangle|surface|ceo)
- `POST /api/calendar/items` — create manual item
- `PATCH /api/calendar/items/:id` — update/reschedule
- `DELETE /api/calendar/items/:id` — remove

### Cockpit Layer (bus #5972, 2026-08-28 — drawers are cockpits)

- Every drawer opens action surfaces: writing->Writing Studio (:port/), research->Research Studio (:port/, same app — verified via pipeline_api dashboard docstring), review->Flow (Conductor :port/?task=), task->inline Live Status (15s refresh). Map overridable via `init({surfaces})` — this is the TEMPLATE contract for the future calendar system.
- Cross-adapter dedupe in mesh(): norm(title)+date+ref key; never merges across dates; keeper = richest then edit authority (manual > bus > mosaic > writing > posting > publication > github > pipeline > cron > engine); losers recorded in `merged_from`.
- Dynamics per item (micro) and per view (macro) derived SERVER-SIDE from structure via `dynamics_gate.derive` (mastermind/synergy/symbiosis/entourage, honest zero "none"). Bus from/to are carrier semantics, NOT co-dispatched specialists (fold D2 — false-synergy bug caught by battery).
- Handshake logging: every source->mesh adapter pull logs info+opportunities+gaps (throttled 10min on identical full signatures); every cockpit surface-open logs mesh->surface. Missing deep-link contracts surface as GAPs, never fabricated URLs.
- Design doc + volley record: `organism/CALENDAR-COCKPIT-DESIGN-T-260828.md`; battery: `test_calendar_cockpit.py` (33 checks).

### Lane Computation (dynamic, at render time)

```
if status in (blocked, needs_input, awaiting_review) -> human
if type in (deadline, meeting, external_event) -> human
if route == 'human' -> human
if free_energy > 0.7 -> human
else -> ai
```

### Engine Init Pattern

```javascript
OrganismCalendar.init({
  container: 'elementId',
  apiBase: 'http://localhost:port',
  siloScope: 'gg3',       // all, gg3, gg-live, writing, infrastructure
  theme: 'ops',            // ops, writing, standalone
  popout: 'organism-calendar.html?silo=gg3',
  defaultView: 'week'      // day, week, month, year, multiyear
});
```

## Design Principles (from adversarial review)

1. Calendar NEVER owns source data (read-aggregation only)
2. Lane computed at render time, never stored
3. Each adapter has 3s timeout, failed sources show stale cache
4. Cron expansion only for day/week views, density counts for month/year
5. Self-maintenance: health cron every 5min, governance proposals to bus
6. No new process: lives inside existing gg3_gateway.py
7. Engine has mock data fallback when API unreachable
8. Day view uses dedicated /day endpoint (more accurate lanes)

## Known Issues

1. Silo filter too strict on mesh endpoint (sibling-agent fixing msg 1603)
2. Cron recurring definitions not yet populating in mesh response
3. Engine has fallback mechanisms for both issues

## Maintenance

### Adding a new source (sibling-agent lane)
1. Create adapter class implementing: pull(), health(), write_back()
2. Register in adapter registry dict in gg3_gateway.py
3. Add to health monitoring loop

### Adapter inventory (2026-08-18, organism_calendar.py)
| Source | Reads | What it surfaces |
|--------|-------|------------------|
| cron | <agent-home>/cron/jobs.json | 52 recurring harness jobs |
| engine | :port /api/metrics | engine fleet alerts (69 engines) |
| pipeline | :port /api/pipelines/runs | writing pipeline runs |
| writing | :port /api/drafts | draft stages (down when :port auth/off) |
| publication | publication_deadlines.db | CFP/grant deadlines + placeholders |
| posting | writing-studio/calendar_mesh.db | scheduled posts + posting_memory (canonical per bus 2125) |
| mosaic | ~/your-org/your-stack/stores/task-ledger.db | cross-harness the OS ledger open tasks (all 3 harnesses) |
| bus | message-bus.db | pending inter-harness messages (newest 50) |
| notion | Notion API | shared pages (warn when 0 shared) |
| manual | organism_calendar.db calendar_items | hand/UI-created items |

Lane rules for adapters: pending posts route=human (principal approval); posting_memory status=completed milestone; mosaic actor_class=human or P-* assignee -> human; bus design_request/approval_request -> human.

### Adding a new surface (hermes lane)
1. Include `calendar-engine.js` via script tag
2. Create container div
3. Call `OrganismCalendar.init({...})`

### Self-maintenance
- Health cron every 5 min: check adapters, log metrics, flag anomalies
- 3 retries with backoff on failure, then disable + notify bus
- Auto-archive items >90 days
- Governance proposals for schema drift, performance, new sources
