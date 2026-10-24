# Unified Search System Architecture (2026-08-11)

Built to fix Popper gap analysis gaps 1-4, 9, 11, 16-18. All modules verified live.

## The Single Search Function

**File:** `unified_search.py`
**API:** `GET /api/research/unified?q=...&limit=15&user_type=auto&enrich=true`

Everything in the Writing Studio calls this ONE endpoint. The old
`/api/research/search-v3` and `/api/research/search` are deprecated.

### Complete Flow (9 steps, mostly deterministic)

```
1. Intent classify (safety_rail.classify_user_intent)     — 0 tokens
   → academic, public, clinical, journalist, student, policy

2. Medical risk detect (safety_rail.detect_medical_intent) — 0 tokens
   → high, moderate, low, none

3. Evidence cache check (evidence_store.get_cached_pool)   — 0 API calls
   → returns cached pool if < 24h old

4. Multi-source search (unified_search._direct_openalex_search)
   → concept-ID filtered if query matches known DS concept
   → full-text fallback for unknown topics
   → 1 API call

5. V3 scoring (search_ab_test._metadata_score_v3)          — 0 tokens
   → IDF weighting + phrase matching + quality floor + dedup

6. Bridge detection (research_bridge_engine.discover_bridges) — 0 tokens

7. Store in evidence DB (evidence_store.store_evidence_pool)
   → dedup by normalized title hash
   → creates cached pool for future queries

8. Enrich (evidence_enrichment)
   → tier_evidence(): strong/established/emerging/theoretical/moderate
   → generate_next_actions(): narrow, recent, contradict, start paper, explore, save
   → generate_pool_summary(): confidence assessment + provenance

9. Apply safety rail disclaimer if medical risk detected
```

## Module Reference

### evidence_store.py
SQLite at `writing-studio/evidence.db`. Tables: papers (deduped by title hash),
search_queries, evidence_pools (cached with TTL), user_feedback (ratings).

Key: `store_paper()` deduplicates across sources — same paper from OpenAlex
and arXiv gets ONE row with `times_seen=2` and the richer metadata kept.

### safety_rail.py
60+ medical keywords + 7 phrase patterns. Risk levels:
- high: 2+ phrase matches OR (1 phrase + 2+ keywords) → full disclaimer
- moderate: 1 phrase OR 3+ keywords → moderate disclaimer
- low: 1-2 keywords → short disclaimer

`classify_user_intent()` routes queries to user types. This determines which
integration layer processes the evidence (academic synthesis vs plain-language
answer vs clinical decision support).

### evidence_enrichment.py
All deterministic, 0 tokens:
- `tier_evidence()`: assigns evidence_tier + evidence_label per paper
- `generate_next_actions()`: returns actionable buttons per result set
- `generate_pool_summary()`: confidence assessment from tier distribution

### unified_search.py
The orchestrator. `_direct_openalex_search()` has a CONCEPT_MAP that maps
known DS phrases to verified OpenAlex concept IDs. Concept-filtered search
(501 results for FEP) vs full-text search (30,392 results including cardiology).
The concept map is the single biggest search quality lever.

## UI Wiring (writing-studio.html)

`hubSearch()` calls `/api/research/unified`. Stores full response in
`window._unifiedSearchResult` for client-side filtering by hubNextAction().

Renders: pool summary header (confidence, tiers, sources, years), safety
disclaimer box (if medical), next-action button bar, paper cards with
evidence tier badges and treatment claim flags.

`hubNextAction(actionStr)` dispatches refine/filter/explore/action buttons.
For "narrow" and "recent only", filters the cached result set client-side
(no new API call). For "contradict" and "explore", triggers a new search.

## What Still Needs Building

1. GAP 20: Unify VERITAS/CRUCIBLE pipeline classes (sibling-agent's lane)
2. GAP 15: NL exploratory on-ramp for non-expert users
3. GAP 6: Robust OpenAlex rate limiting (request queue, not just sleep)
4. Brainstorm endpoint still uses hardcoded arXiv XML, not unified search
5. Pipeline Stage 2 still does its own search, not unified search
