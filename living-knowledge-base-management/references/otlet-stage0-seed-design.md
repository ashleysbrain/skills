# Otlet System — STAGE 0: Pre-Launch Seed Design

Design for the minimal graph that exists BEFORE any user joins. Derived from
live DB queries (2026-08-11), not estimates. All numbers verified against
`/<workspace>`.

## Ground Truth (queried 2026-08-11)

| Node type | Count | Notes |
|-----------|-------|-------|
| paper | 706 | 587 from OpenAlex enrichment, 119 TSC-original |
| concept | 2,285 | Only 335 (15%) have domain/field hierarchy; 1,950 orphans |
| person | 167 | 135 matched to OpenAlex IDs (all have ≥1 authored edge) |
| institution | 37 | 0 have OpenAlex IDs |
| venue | 349 | 348 already OA-matched |
| event | 15 | TSC 2026 + sessions |
| research_lab | 0 | Not built |
| **Total nodes** | **3,559** | |
| **Total edges** | **6,617** | discusses: 4,901, authored: 709, published_in: 547, presented_at: 167, presented_at_event: 119, cites: 109, affiliated_with: 48, collaborated_with: 17 |

**Critical gaps**: 0 embeddings, 0 layout positions, only 109 cites edges
(15% citation coverage — broken for bridge detection), 85% of concepts lack
domain hierarchy (breaks Z1-Z3 zoom).

## STAGE 0 Targets (3 priorities)

### TARGET 1 — Papers: 706 → ~2,200

Right number for launch. Below 1,500 the graph looks thin; above 3,000 render
cost rises without proportional discovery value.

**Mechanism**: Raise `MAX_WORKS` in `openalex_enrichment.py` from 5 → 15 for
the 135 matched authors. Yields ~2,025 works, dedup against existing 587 →
~1,438 new papers, ~2,144 total.

**API cost**: 135 `/works` queries (authors already matched, no author search
needed). At 1s/call = ~2.5 min.

### TARGET 2 — Citation densification: 109 → 8,000-12,000 cites edges

The citation graph is the product's spine (bridge detection, citation
candidates). Currently 15% coverage — broken.

**Mechanism**: For ~2,000 papers, resolve `referenced_works` against an
expanded pull of hub papers (~500 most-cited references across the corpus not
yet in DB). Pull those 500, then resolve all refs → expect 8,000-12,000
internal cites edges.

**API cost**: ~200 batched works fetches.

### TARGET 3 — Concept hierarchy: backfill domains on 1,950 orphans

Only 335/2,285 concepts have `domain` — breaks the Z1-Z3 zoom hierarchy.

**Mechanism**: OpenAlex `/concepts` lookup for each orphan → assign
domain/field/subfield + parent.

**API cost**: ~1,950 calls at 1s = ~32 min. Adds ~700 new concepts from
expanded papers → ~3,000 concepts total, ~95% with domain.

### Side pulls (trivial)

- 37 institutions → OpenAlex IDs (37 calls)
- 349 venues already OA-matched (done)

## STAGE 0 Final Totals

~2,200 papers | ~3,000 concepts | 167 persons | ~60 institutions | ~400 venues |
~18,000-25,000 edges. Matches architecture spec band (3,000-7,000 nodes,
15,000-50,000 edges).

**Total API budget**: ~2,300 OpenAlex calls, ~40 min wall-clock at polite-pool
rate (1s sleep).

## Pre-Compute (before any user joins)

These MUST exist in the graph at launch — they're prerequisites for core
features:

1. **SPECTER 2 embeddings** for all ~2,200 papers + ~3,000 concepts — required
   for search (F1 universal search) and layout. ~5,200 forward passes (~10 min GPU).
2. **UMAP 3D + d3-force layout** — required for initial Z1-Z5 render. One batch
   job (~15 min).
3. **Concept domain hierarchy** (Target 3) — required for zoom navigation.
4. **Citation edges** (Target 2) — required for bridge detection (F4) and
   citation candidates (F5).
5. **FTS5 indexes** — already auto-built via triggers (done).

## Lazy Compute (on user query, NOT pre-materialized)

These are computed per-request to avoid pre-computing N² or O(edges) structures:

1. **Citation candidate ranking** (F5) — per-pair scoring on demand
2. **Traversals beyond 2-hop neighborhoods** — BFS at query time
3. **Non-TSC author disambiguation** — resolve when encountered via search
4. **Cross-disciplinary bridge scoring** — on filtered subgraph, not global
5. **Co-authorship graph for new (non-seed) authors** — expand on demand

## The Pre-Compute / Lazy Decision Rule

When deciding whether to pre-compute a graph property at seed time:

- **Pre-compute if**: it's O(nodes) or O(edges) to build, AND it's needed for
  the first render/search/layout. (embeddings, layout positions, hierarchy,
  citation edges)
- **Lazy compute if**: it's O(N²) pairwise, OR it's query-specific (ranking,
  bridge scoring, neighborhood expansion), OR it involves entities not yet in
  the graph (new authors, user-added papers).

The seed exists to make the graph *navigable* on first load. Everything that
makes it *useful for a specific question* is computed when the question is asked.
