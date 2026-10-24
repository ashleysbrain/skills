# Otlet System — Build Status & Implementation Log

## Current State (2026-08-11, post-enrichment Phase 1+2 complete)

The Otlet System is LIVE. API serving on :port. OpenAlex enrichment completed
overnight. DB grew from 748 nodes/1,056 edges (2026-08-07) to 3,559 nodes/6,617
edges (2026-08-11). Constellation product concept documented at
`/<workspace>`.

Next milestone: STAGE 0 seed design — see
`references/otlet-stage0-seed-design.md` for the pre-launch expansion plan
(papers 706→2,200, citations 109→8-12K, concept domains backfilled).

## Files

- `/<workspace>` — full architecture spec
- `/<workspace>` — database schema builder (7 node types, 14 edge types, FTS5 triggers)
- `/<workspace>` — TSC 2026 ingestion scanner
- `/<workspace>` — OpenAlex enrichment pipeline (author matching + works fetch + citations + co-authorship)
- `/<workspace>` — FastAPI backend serving graph data
- `/<workspace>` — Three.js 3D visualization (built by sibling-agent)
- `/<workspace>` — local Three.js library (served from API, not CDN)
- `/<workspace>` — the live database (SQLite, WAL mode)

## Database Stats (2026-08-11, post-enrichment — queried from live DB)

- 3,559 nodes total
  - 706 papers (587 from OpenAlex enrichment, 119 TSC-original; 545 with DOIs, 402 with abstracts, 0 with embeddings)
  - 2,285 concepts (335 have domain/field hierarchy; 1,950 orphans = 85% need backfill)
  - 167 persons (135 matched to OpenAlex IDs, all with ≥1 authored edge)
  - 37 institutions (0 have OpenAlex IDs — gap)
  - 349 venues (348 OA-matched)
  - 15 events (TSC 2026 + 14 plenary sessions)
  - 0 research_labs (not built)
- 6,617 edges across 8 types and 4 layers
  - discusses (concept): 4,901
  - authored (social): 709
  - published_in (bibliographic): 547
  - presented_at (event): 167
  - presented_at_event (event): 119
  - cites (citation): 109 ← critical gap, only 15% coverage
  - affiliated_with (social): 48
  - collaborated_with (social): 17

## API Endpoints (all verified working)

- `GET /health` — status check
- `GET /otlet/stats` — node/edge counts by type
- `GET /otlet/search?q=X` — FTS5 search across all node types
- `GET /otlet/graph?layer=all|concept|social|event|organizational` — JSON graph for Three.js
- `GET /otlet/node/{type}/{id}` — node detail + all connections
- `GET /otlet/event/tsc2026/graph` — TSC 2026 subgraph (301 nodes, 409 links)
- `GET /atlas` — Three.js 3D visualization page
- `GET /three.min.js` — local Three.js library

## Key People Enriched

- Stuart Hameroff: A5051102175 (242 works)
- Giulio Tononi: A5001381023
- Donald Hoffman: A5063001647
- the principal Williams: A5081637205
- Roger Penrose: NOT enriched (rate limited, needs retry)

## What's In Progress

- OpenAlex Phase 2 enrichment (works fetch): blocked by IP-level rate limiting (429).
  Cron job `b05aa1bd1811` runs at 1am/2am/3am to catch throttle reset.
  When complete: ~670 additional papers with abstracts/DOIs, citation edges,
  co-authorship edges.
- 33 people (20%) have no OpenAlex profile — correct, they are independent
  researchers/artists/non-academic presenters.

## What's NOT Built Yet (Phase 2+)

- SPECTER 2 embeddings (semantic paper embeddings, 768-dim)
- UMAP 3D coordinates (layout engine for Google Earth zoom)
- Research lab nodes (no lab data ingested yet)
- Institution collaboration edges (needs cross-ref enrichment)
- Remaining 83 alphabetical-only posters (no photos on website, no names)
- Poster presenter institutions (119/119 still missing affiliations — need OpenAlex completion)

## Opencode Bus Posts

- Bus 1513: Sherman model routing (per-task model selection) — DONE by sibling-agent
- Bus 1523: Otlet Three.js frontend build request (SUPERSEDED by 1524)
- Bus 1524: Updated handoff with corrected status
- Bus 1525: sibling-agent DONE — Atlas built at /<workspace>
- Bus 1526: Previous the operator agent session acknowledged (premature, pre-enrichment)
- Bus 1527: API restarted with enriched data (748 nodes)

## Lessons Learned This Build

1. **35% coverage claimed as "operational" was caught by user.** Adversarial
   audit before claiming done is mandatory. See SKILL.md quality gate section.

2. **OpenAlex rate limits hard at IP level** after ~300 calls. 1s sleep is
   minimum. Overnight cron is the pattern. See `references/openalex-rate-limiting.md`.

3. **Three.js won't load from CDN in restricted browsers.** Serve locally.
   See SKILL.md static-serving pitfall.

4. **SQLite locks when API server + enrichment run concurrently.** WAL mode
   + busy_timeout=30000 is required.

5. **"Build it right not half ass" + "This isn't a race"** — user preference.
   Rate-limited? Wait for reset. Subagent timed out? Run yourself properly.
   Never declare partial work as complete.

## Ingestion Technique (reusable for other conferences)

The TSC scanner uses browser_console JavaScript extraction:
```javascript
// Extract ALL posters via DOM walk — not limited by viewport
const images = document.querySelectorAll('img[alt]');
images.forEach(img => {
    const alt = img.alt.trim();
    let container = img.parentElement;
    for (let i = 0; i < 5 && container; i++) {
        if (container.textContent.includes('Poster #')) break;
        container = container.parentElement;
    }
    // Extract name (from img alt), poster_id (from text), title (from <a>), session (from closest [id^="ps"]')
});
```

The alphabetical poster section (no photos) has ~83 additional titles
without presenter names — these need a different extraction approach
(clicking each title to reveal the presenter page).
