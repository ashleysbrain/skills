# Bridge Engine v2 — Graph-Based Cross-Disciplinary Discovery

**Created:** 2026-08-11
**Spec location:** `organism/docs/constellation/BRIDGE-ENGINE-SPEC.md`
**Reference impl:** `organism/docs/constellation/bridge_engine.py` (runnable, self-tests pass)

## What changed (v1 → v2)

The original `research_bridge_engine.py` used a 3-factor score (entanglement,
novelty, impact) on raw OpenAlex API co-occurrence counts. No graph, no
communities, no embeddings, no centrality.

v2 is a full heterogeneous-graph pipeline with four scoring factors powered
by sampled Brandes centrality. This is Constellation's core moat.

## The five-stage pipeline

```
NIGHTLY (batch):          QUERY-TIME:
1. Ingest & Embed         3. Candidate Generation (concept-κ triples)
2. Community Detection    4. Bridge Scoring (4-factor geometric mean)
   + Sampled Brandes      5. Rank & Emit (MMR diversity)
```

All expensive work (embedding, Louvain, centrality) is precomputed nightly.
Query-time is pure lookup + scoring: < 50ms per seed paper.

## Sampled Brandes with inter-community filter (key algorithmic innovation)

Standard betweenness centrality is O(V·E) — infeasible on million-node
graphs. **Sampled Brandes** (Brandes & Pich 2007) estimates it by running
single-source accumulation from only k≪V random source nodes. O(k·E).
Unbiased estimator, error scales O(1/√k). k=500 default gives ±0.045 CI.

**The twist for bridge detection:** modify the back-propagation step to
only accumulate dependency when `comm(v) != comm(w)` — i.e., only count
shortest paths that CROSS community boundaries. This yields
**inter-community betweenness (IBC)** — a node's centrality specifically
as a bridge between disciplines, not as a hub within one.

Run this on the concept subgraph only (~10⁴ nodes), not the full paper
graph. Seconds per nightly run.

Full pseudocode in the spec (§3.2). Python implementation in
`bridge_engine.py` function `sampled_brandes_intercommunity()`.

## Four-factor Bridge Score (geometric mean)

```
B = (S_κ^α1 · Φ^α2 · 𝒩^α3 · Δ_cite^α4) ^ (1/Σα)
```

Geometric mean (not arithmetic) because a zero on any factor kills the
bridge — it must be simultaneously central, surprising, novel, AND
citation-absent.

Default exponents: α = (1.0, 0.7, 0.6, 0.8).

### Factor 1 — S_κ: Structural centrality (sampled Brandes IBC)
Normalized inter-community betweenness of the bridge concept. High IBC =
concept sits on many shortest paths between different communities.

### Factor 2 — Φ: Surprise (Goldilocks gap) — THE MOAT
Gaussian bell centered at cosine_sim=0.35, σ=0.15. Peaks in the middle
band — semantically adjacent enough to be meaningful, distant enough that
a human wouldn't find it by browsing. Explicitly DOWNWEIGHTS high
similarity (sim≈0.9 → Φ→0, "too obvious"). This is what pure similarity
search cannot do — it optimizes for sim→1. The bridge engine optimizes
for the gap nobody else looks in.

### Factor 3 — 𝒩: Novelty (temporal acceleration)
Recent (12-month) cross-field co-mention frequency ÷ 5-year baseline.
Clipped to [0,3]. >1 = bridge is forming.

### Factor 4 — Δ_citation: Citation-graph absence ("nobody noticed")
1.0 if no citation path ≤3 exists between the two papers. 0.0 if they
already cite each other directly or through one intermediary. Maximal
when the citation graph is silent — the discoverable condition.

## Walk-through: neuroscience ↔ quantum physics

Seed: "Predictive coding in cortical microcircuits" (neuroscience)
Bridge concept: "Bayesian Inference" (IBC=0.91 — highest cross-community
centrality; it's the only concept appearing in BOTH communities)
Target: "Quantum Bayes theorem and subjective probability" (quantum)
- sim = 0.37 → Φ = 0.96 (Goldilocks band)
- No citation path → Δ_cite = 1.0
- 𝒩 = 2.1 (accelerating)
- B = 0.93

No keyword overlap. No citation path. Cosine sim below typical thresholds.
Only the bridge engine surfaces it.

## Relation to existing code

| Old function (v1)        | New role (v2)                                      |
|--------------------------|----------------------------------------------------|
| compute_entanglement     | subsumed by S_κ (IBC) — was a proxy for centrality |
| compute_novelty          | becomes Factor 3 𝒩, unchanged in spirit             |
| compute_impact           | folded into Δ_citation + 𝒩                         |
| compute_bridge_score     | geometric mean retained, expanded 3→4 factors      |
| compute_percolation      | auxiliary signal (field maturity), not in core score|
| compute_health_proximity | auxiliary signal, feeds explanation layer           |

## Implementation order (7 steps)

1. Graph builder (SQLite + NetworkX + OpenAlex ingest)
2. Community detection (Louvain via python-louvain)
3. Sampled Brandes (implement + validate against exact on 10k subgraph)
4. Candidate generator (τ_mention parameterized)
5. Scoring (4 factors, config-driven exponents)
6. FAISS integration (ANN cosine for surprise factor at scale)
7. MMR + explanation emitter

Each step independently testable against existing DS_FIELD_CONCEPTS pairs.
