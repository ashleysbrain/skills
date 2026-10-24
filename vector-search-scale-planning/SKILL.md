---
name: vector-search-scale-planning
description: Use when planning vector-search scale transitions.
version: 1.0.0
author: the operator agent
license: MIT
metadata:
  hermes:
    tags: [vector-search, scale-planning, embeddings, FAISS, pgvector, SQLite, ANN, RAG]
    related_skills: [faiss, qdrant-vector-search, chroma, pinecone]
---

# Vector Search Scale Planning

Use this skill when designing, auditing, or planning the growth path of any system that uses embeddings for semantic search, RAG, or knowledge-graph traversal. It provides the concrete numerical thresholds at which the architecture must change, backed by latency and cost calculations.

## When to use

- User asks "when do we need a real database" for an embedding/vector system
- Planning the scale path from MVP (SQLite + brute-force) to production (ANN index)
- Deciding between FAISS sidecar vs Postgres+pgvector vs dedicated vector DB
- Determining when to switch from lazy (on-first-query) to proactive (on-write) embedding
- Budgeting infrastructure cost for a vector search product
- Designing batch-embedding promotion criteria for "stub" nodes
- Reviewing a product spec that says "scales to ~100K nodes" without checking search latency

## Key Insight (state this first)

**The embedding API is never the cost bottleneck.** At $0.02/1M tokens (text-embedding-3-small) or free (local models like SPECTER 2), embedding 1 million documents costs ~$6. The three real walls are:

1. **Brute-force vector scan latency** — O(N) per query with no ANN index
2. **Single-writer lock contention** (SQLite) — saturates at ~50 concurrent writers
3. **RAM for the ANN index** — HNSW/FAISS index must fit in memory; this drives the cost floor

Design around these three, not around embedding API cost.

## The Four-Threshold Framework

### T1. Lazy → Proactive Embedding
- **Trigger:** ~100 active users OR ~5,000 embedded nodes
- **Why:** Lazy embedding puts model inference (~50–200ms) on the query hot path per cold node. Hub nodes (high degree) get hit repeatedly.
- **Batch-embed promotion rule:** `degree ≥ 10 AND queried ≥ 3×/7d AND embedding IS NULL`
- **Priority queue:** `weighted_degree × query_frequency_7d`
- **Nightly cost:** embedding top 1,000 candidates = ~$0.18/month. Negligible.

### T1b. Embedding Propagation Frontier (for graphs too large to batch-embed)

When the corpus dwarfs what users touch (e.g. OpenAlex 250M+ works, only a few
thousand ever queried), batch-embedding everything is wrong even at free API
cost — it wastes compute on nodes nobody will ever retrieve. Use **propagation
from a ground-truth frontier** instead of the flat promotion rule above.

**Model:** treat user-deposited nodes as ring 0 (ground truth, real embeddings).
Spread embeddings outward in confidence-decaying BFS rings:

| Ring | Embedding source | Confidence |
|---|---|---|
| 0 | User-deposited node — real embedding (SPECTER 2 / text-embedding-3) | 1.00 |
| 1 | Nodes the user node points to (cites / references / links) — real | 1.00 |
| 2 | Nodes pointing back at a user node — real if metadata avail, else propagate | 0.85/0.60 |
| 3 | Co-linked siblings (co-cited / co-referenced) — propagate = mean of shared linkers | 0.50 |
| 4 | 2-hop neighborhood — `0.7×half-precision-text + 0.3×neighbor-mean` | 0.40 |
| 5+ | Deep frontier — propagate only; upgrade to real on query/click | decaying |

Every node carries provenance: `embedding_source`, `embedding_ring`,
`embedding_confidence`, `embedding_model_version`. UI marks propagated
embeddings "approximate"; ranking layers down-weight or filter ring ≥ 3 when
precision matters (cite recommendation, RAG context).

**Priority function for the upgrade queue** (generalizes the flat promotion rule):
```
priority(node) = 0.35×query_hits_7d + 0.25×degree + 0.20×on_user_path
               + 0.10×staleness − 0.10×distance_penalty(ring)
```
A node clicked or queried jumps the queue and gets promoted from propagated →
real; its own ring-1 neighbors get re-enqueued. The graph heals outward from
demand.

**Why propagate at all (vs. leave NULL):** a NULL-embedding node is invisible to
semantic search and to any graph algorithm that uses the embedding (clustering,
bridge detection, layout). Propagation gives every reachable node *some* vector
so search returns frontier results (marked approximate) instead of nothing, and
sparse-region cross-cluster links become detectable. This is the mechanism that
makes a graph compound rather than just grow.

**When to use T1b instead of flat T1:** when the corpus is ≥10× the size of the
actively-queried set, or when the graph has a natural "deposited vs. referenced"
distinction (user deposits, citations, links, backlinks). See
`living-knowledge-base-management` → `references/otlet-stage2-lazy-growth-engine.md`
for the worked Otlet/Constellation case.

### T2. SQLite/brute-force → FAISS sidecar OR Postgres+pgvector
- **Trigger:** ~25,000 vectors (latency) OR ~50 concurrent writers (contention)
- **Vector scan ceilings** (SIMD brute-force @ ~300–400K vec/s for 768-dim):
  - 10K vectors: ~25ms (OK)
  - 25K vectors: ~63ms (borderline)
  - 50K vectors: ~125ms (unacceptable for interactive)
  - 100K vectors: ~250ms (dead)
- **ANN alternatives stay flat:** FAISS IVF <5ms, pgvector HNSW <35ms — both to 10M+ vectors
- **Migration path:** FAISS IVF sidecar first (keep SQLite for relational data), then full Postgres+pgvector when write contention or ACID-across-graph-and-vector is needed

### T3. Exact → Approximate Graph Algorithms
- **Trigger:** ~10,000 nodes (for betweenness centrality specifically)
- **Why:** Brandes' algorithm is O(V×E). 10K nodes/30K edges = 10min exact, 30s approximate (k=500 samples). 100K nodes = 28h exact, 8min approximate.
- **Action:** Switch to sampled Brandes, pre-compute nightly, cache results

### T4. Infrastructure Cost Threshold
- **Trigger:** ~$150/month (~50,000 documents with embeddings)
- **Cost driver:** RAM for ANN index. Formula: `dimensions × 4 bytes × N vectors × 3 (HNSW overhead)`
  - 50K × 768 × 4 × 3 = 460MB → fits 4GB VPS ($20/mo)
  - 500K × 768 × 4 × 3 = 4.6GB → needs 16GB instance ($150–400/mo)
  - 1M × 768 × 4 × 3 = 9.2GB → needs 32GB instance ($400+/mo)

## Calculation Formulas

```
Vector search latency (brute-force):
  ms = N_vectors / scan_rate × 1000
  scan_rate ≈ 300–400K vec/s (768-dim, SIMD)

Vector search latency (ANN):
  FAISS IVF: O(√N) probes, typically <5ms
  pgvector HNSW: O(log N), typically <35ms to 10M+

SQLite write contention:
  utilization = (concurrent_writers × writes_per_sec_per_writer × avg_write_ms) / 1000
  < 0.5: healthy | 0.5–0.7: approaching limit | ≥ 1.0: SATURATED

Betweenness centrality timing:
  exact: O(V × E), ~2µs per (V×E) unit
  approximate(k): O(k × E), same rate

HNSW/FAISS RAM budget:
  raw_bytes = dimensions × 4 × N_vectors
  total ≈ raw_bytes × 3 (graph overhead)
  Must fit in RAM or search degrades to disk scan

Embedding API cost:
  cost = N_documents × avg_tokens × price_per_M_tokens / 1e6
  text-embedding-3-small: $0.02/1M tokens, ~300 tokens/doc
  → $6 per 1M documents. Never the bottleneck.
```

## Presentation Format

When writing a scale-transition section into a product/architecture doc:

1. **Lead with the key insight** (embedding API ≠ bottleneck)
2. **Give a TL;DR table** — all thresholds at a glance (trigger, threshold, root cause, action)
3. **For each threshold, show the calculation** — N vs latency/cost table with verdicts (✓/⚠/✗)
4. **Provide a migration checklist** with concrete actions per threshold
5. **Include a scale map** showing the progression

## Migration Decision: FAISS sidecar vs Postgres+pgvector

| Factor | FAISS sidecar | Postgres+pgvector |
|--------|--------------|-------------------|
| Best when | Vector count is the bottleneck, graph is small | Write contention or multi-writer needed |
| Keeps SQLite? | Yes — graph/relational stays | No — full migration |
| ACID across graph+vector? | No (two systems) | Yes |
| Connection pooling | N/A | PgBouncer |
| Effort | Low (add process, export vectors) | Medium (pgloader migration) |
| RAM efficiency | Good (FAISS is optimized) | HNSW uses ~3× raw |

**Recommendation:** Start with FAISS sidecar at 25K vectors. Move to Postgres+pgvector when concurrent writers exceed 50 or ACID consistency across graph+vector is required.

## Browser/visualization wall (parallel constraint)

The frontend has a separate scaling wall independent of the database. Applies to Three.js, D3, or any WebGL/Canvas renderer:

| Nodes in viewport | Strategy | Performance |
|---:|---|---|
| ≤ 10,000 | Render all directly | 60fps |
| 10,000–50,000 | LOD: hide labels, simplify geometry | 30–60fps |
| 50,000–100,000 | LOD clustering + progressive loading | 30fps |
| > 100,000 | Server-side clustering, send clusters not nodes | Mandatory |

## Pitfalls

- Don't trust a schema docstring that says "scales to ~100K nodes" without checking whether that's for *search latency* or just *storage*. Search latency dies at ~25K vectors with brute-force.
- Don't compare brute-force (O(N)) to HNSW (O(log N)) without noting they're fundamentally different complexity classes. The crossover isn't gradual — it's a cliff.
- Don't forget the browser visualization wall. It's a separate constraint from the database. Database can handle 1M nodes but the browser dies at ~50K rendered objects.
- Don't budget around embedding API cost. Budget around RAM for the ANN index. The API cost is rounding error.
- Don't skip the lazy→proactive transition. At ~100 users, hub nodes are hit thousands of times/day and lazy embedding re-pays the inference cost every time.

## Verification

When auditing a scale plan:
- [ ] Does it specify the vector count at which brute-force becomes unacceptable (~25K)?
- [ ] Does it specify the concurrent-writer count at which SQLite saturates (~50)?
- [ ] Does the cost model account for HNSW index RAM, not just embedding API?
- [ ] Is there a lazy→proactive embedding trigger with a concrete promotion rule?
- [ ] If graph algorithms are used (betweenness, centrality), is there an approximate-mode threshold (~10K nodes)?
- [ ] Is the browser/visualization scaling wall addressed separately from the database?

## References

- `references/scale-transition-calculation-patterns.md` — worked examples of the formulas, including the Otlet/Constellation case study (768-dim SPECTER 2, SQLite+FTS5, 3,559 nodes → 500K paper scale plan)
