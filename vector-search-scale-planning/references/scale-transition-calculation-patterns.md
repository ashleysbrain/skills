# Scale Transition Calculation Patterns

Worked examples of the formulas from the main skill, using the Otlet/Constellation
knowledge-graph system as a case study.

## Case Study: Otlet/Constellation

- 7 node types (paper, concept, person, institution, lab, event, venue)
- 768-dim SPECTER 2 embeddings (float32)
- SQLite + FTS5 backend, Three.js WebGL frontend
- Current state: 3,559 nodes, 6,617 edges, 706 papers, 0 embeddings
- Target: scale to 500K papers

## Worked Example 1: Vector Search Latency

sqlite-vec stores 768-dim vectors and scans with SIMD at ~400K vec/s.

```
At 706 papers:    706 / 400,000 × 1000 = 1.8ms   ✓
At 10K papers:    10,000 / 400,000 × 1000 = 25ms  ✓
At 25K papers:    25,000 / 400,000 × 1000 = 63ms  ⚠ Borderline
At 50K papers:    50,000 / 400,000 × 1000 = 125ms ✗ Unacceptable
At 100K papers:   100,000 / 400,000 × 1000 = 250ms ✗ Dead
```

FAISS IVF with sqrt(N) probes:
```
At 100K:  √100,000 = 316 probes → <1ms
At 1M:    √1,000,000 = 1000 probes → ~1.25ms
```

pgvector HNSW (O(log N)):
```
At 100K:  ~29ms
At 1M:    ~34ms
At 10M:   ~48ms
```

**Crossover:** SQLite brute-force dies at ~25K vectors. ANN stays flat forever.

## Worked Example 2: SQLite Write Contention

Single ingestion cron writes papers + edges. Avg transaction = 5ms.

```
1 writer, 2 w/s:   utilization = (1 × 2 × 5) / 1000 = 0.01  ✓
5 writers, 10 w/s:  utilization = (5 × 10 × 5) / 1000 = 0.25  ✓
20 writers, 40 w/s: utilization = (20 × 40 × 5) / 1000 = 0.40  ✓ OK
50 writers, 100 w/s: utilization = (50 × 100 × 5) / 1000 = 0.50 ⚠ Limit
100 writers, 200 w/s: utilization = (100 × 200 × 5) / 1000 = 1.00 ✗ SATURATED
```

**Ceiling:** ~50 concurrent writers before SQLITE_BUSY errors.

## Worked Example 3: Betweenness Centrality

Bridge Discovery Engine uses NetworkX betweenness_centrality (Brandes, O(V×E)).
~2µs per (V×E) operation unit.

```
3,559 nodes, 6,617 edges:
  exact: 3,559 × 6,617 × 2µs = 47s      ✓ Feasible
  approx(k=500): 500 × 6,617 × 2µs = 6.6s ✓ Fast

10,000 nodes, 30,000 edges:
  exact: 10,000 × 30,000 × 2µs = 600s (10min) ⚠ Slow
  approx(k=500): 500 × 30,000 × 2µs = 30s    ✓ Fast

50,000 nodes, 200,000 edges:
  exact: 50,000 × 200,000 × 2µs = 20,000s (5.5h) ✗ Infeasible
  approx(k=500): 500 × 200,000 × 2µs = 200s (3.3min) ⚠ Slow but OK nightly
```

**Crossover:** Switch to approximate at ~10,000 nodes.

## Worked Example 4: HNSW RAM Budget

768-dim × 4 bytes × N × 3 (HNSW graph overhead):

```
50K papers:   768 × 4 × 50,000 × 3 = 460MB    → 4GB VPS ($20/mo)
100K papers:  768 × 4 × 100,000 × 3 = 922MB   → 4GB VPS ($20/mo)
500K papers:  768 × 4 × 500,000 × 3 = 4.6GB   → 16GB instance ($150-400/mo)
1M papers:    768 × 4 × 1,000,000 × 3 = 9.2GB → 32GB instance ($400+/mo)
```

**Cost trigger:** ~$150/mo at 500K papers, driven entirely by RAM.

## Worked Example 5: Embedding API Cost

text-embedding-3-small: $0.02/1M tokens. Average paper: ~300 tokens.

```
706 papers:   706 × 300 × $0.02 / 1e6 = $0.004
10K papers:   10,000 × 300 × $0.02 / 1e6 = $0.06
100K papers:  100,000 × 300 × $0.02 / 1e6 = $0.60
1M papers:    1,000,000 × 300 × $0.02 / 1e6 = $6.00
```

**Verdict:** Never the bottleneck. 1M papers costs less than lunch.

## Worked Example 6: Batch Embedding Promotion

Otlet has 2,285 concepts. The top ~200 have degree ≥ 10 and cover ~80% of
`discusses` edges. These are the hub nodes worth proactively embedding.

Promotion criteria: `degree ≥ 10 AND queried ≥ 3×/7d AND embedding IS NULL`

Priority: `weighted_degree × query_frequency_7d`

Nightly batch: embed top 1,000 candidates.
Cost: 1,000 × 300 tokens × $0.02 / 1e6 = $0.006/night = $0.18/month.

## Generalization Notes

These formulas work for any embedding dimensionality. Adjust:
- `dimensions` in the RAM budget (1536 for OpenAI ada, 768 for SPECTER 2, 384 for MiniLM)
- `scan_rate` for different SIMD implementations (sqlite-vec ~300-400K, numpy ~50-100K)
- `avg_tokens` for the embedding cost (varies by document type)
- `avg_write_ms` for different databases (SQLite ~5ms, Postgres ~2-3ms with WAL)

The thresholds (25K vectors, 50 writers, 10K graph nodes) are complexity-class
boundaries, not hardware-dependent. They hold across hardware generations.
