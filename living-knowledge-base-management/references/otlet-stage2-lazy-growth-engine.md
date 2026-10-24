# Otlet System — Stage 2: Lazy Growth Engine (design reference)

**Session:** 2026-08-11. Full design doc: `/<workspace>`.
Companion to `otlet-stage0-seed-design.md` (the pre-launch seed) and
`otlet-system-architecture.md`.

## What Stage 2 solves

Stage 1 (built) ingested a static seed (706 papers, 2,285 concepts, 109 internal
`cites` edges, 0 embeddings). Stage 2 is the **compounding growth** question: as
researchers deposit papers, how does the graph densify, and how do embeddings
spread outward without batch-embedding all 250M+ OpenAlex works?

## The three reusable decisions (these generalize beyond Otlet)

### 1. Co-citation materialization = the compounding mechanism

The graph doesn't just grow — it **densifies**. Three mechanisms, ranked:
- **M1 Join edges** — new user paper cites existing nodes → new `cites` edges land on present nodes.
- **M2 Co-citation** — when user paper U cites both A and B, A and B become co-cited → implicit `co_cited_with(A,B)` edge or embedding-similarity boost. **This is the compound interest.** It densifies the existing graph without adding nodes.
- **M3 Frontier expansion** — U cites paper X not yet in graph → X pulled in lazily.

Grounded math (seed: 706 papers, ~40 refs/paper, 30% overlap with existing):
~20 active researchers takes internal `cites` edges 109 → ~3,000–5,000. Superlinear
in users because each new user's refs can form join edges with every prior user's papers.

### 2. Embedding propagation frontier (BFS rings from ground truth)

User-deposited papers are ground truth. Everything else is an approximation that
upgrades on demand. Embeddings spread outward in confidence-decaying rings:

| Ring | Nodes | Method | Confidence |
|---|---|---|---|
| 0 | User-deposited papers | SPECTER 2 full | 1.00 |
| 1 | Papers a user paper cites | SPECTER 2 real | 1.00 |
| 2 | Papers that cite a user paper | SPECTER 2 if abstract avail, else propagate | 0.85/0.60 |
| 3 | Co-cited siblings | Propagate = mean of shared citers | 0.50 |
| 4 | 2-hop neighborhood | 0.7×half-precision-text + 0.3×neighbor-mean | 0.40 |
| 5+ | Deep frontier | Propagate only; upgrade on query/click | decaying |

Every node carries provenance: `embedding_source`, `embedding_ring`,
`embedding_confidence`, `embedding_model_version`. UI marks propagated embeddings
"approximate." Click/query promotes deep-ring nodes to real embeddings — the graph
heals outward from demand.

**Why propagate at all** (vs. leave NULL): a node with no embedding is invisible
to semantic search and bridge detection. Propagation gives every reachable node
*some* vector so search returns frontier results (marked approximate), bridge
scoring has signal in sparse regions, and UMAP layout has positions instead of
clustering at the origin.

### 3. Priority function + 7-tier trigger taxonomy

Priority drives the background worker queue:
```
priority(node) = 0.35×query_hits + 0.25×degree + 0.20×on_user_path
               + 0.10×staleness − 0.10×distance_penalty(ring)
```
A new user's 1-hop neighborhood always jumps to front (on_user_path=1.0).

Triggers (first two synchronous ≤200ms, rest background):
- **IMMEDIATE** — ingest paper (node+FTS+parse refs, no embed); insert cites edge + bump target query_hits.
- **FAST ASYNC** — new user signup (enqueue ring 0+1 for real embed); semantic-search miss (frontier expand toward query region).
- **NIGHTLY** — frontier crawl (BFS outward, fetch OpenAlex metadata); co-citation materialization (scan 24h new cites edges).
- **WEEKLY** — incremental UMAP re-layout for nodes whose embedding moved > δ.
- **ON-DEMAND** — click/view (lazy detail compute; promote ring ≥3 to embed queue).

Three worker lanes with preemption: P0 real embeddings (ring 0-1) > P1-2 metadata+cocitation > P3-4 free propagation.

## Schema additions (additive, no Stage 1 breakage)

`paper` gains: `embedding_source`, `embedding_ring`, `embedding_confidence`,
`embedding_model_version`, `last_embedded_at`, `query_hits_7d`, `last_clicked_at`.
New tables: `paper_deposit` (user provenance), `enrichment_queue` (persistent
priority queue across worker restarts). New edge type `co_cited_with`.

## Relation to vector-search-scale-planning

This is the **richer version of the T1 (lazy→proactive) threshold** in the
`vector-search-scale-planning` skill. That skill's rule
(`degree≥10 AND queried≥3×/7d → batch embed`) is the flat case. The ring
propagation model adds: approximate embeddings for everything reachable,
provenance tracking, and demand-driven promotion — so the graph is never blind
in sparse regions while still spending real-embedding compute only where humans
look. See that skill's "Embedding Propagation Frontier" section.

## Key pitfalls encoded

- **Don't batch-embed everything.** OpenAlex is 250M+ works. Propagate; upgrade on demand.
- **Don't let propagated embeddings drift.** Confidence decays with ring *and* age; weekly staleness sweep re-propagates ring ≥3 whose neighbors changed.
- **Cap co-citation weight per-citer** to prevent one user inflating a bridge via self-citation spam.
- **Propagation is what makes sparse bridges visible** — real-embedding-only approaches miss weak cross-cluster links that propagated vectors catch.
- **Bump `embedding_model_version` to invalidate** cleanly on model upgrade; queue re-prioritizes ring 0-1 first. No manual migration.
