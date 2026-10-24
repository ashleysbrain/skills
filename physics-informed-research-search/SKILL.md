---
name: physics-informed-research-search
category: software-development
description: Build token-efficient research search using physics models.
version: 1.0.0
---

# Physics-Informed Research Search

Use when designing, building, or maintaining the research search engine that
powers the Writing Studio's literature discovery, evidence gathering, and
cross-field bridge detection.

## CRITICAL: Shared Engine, Not Siloed Pipelines (user-locked 2026-08-11)

The search engine is ONE engine. It is NOT siloed between VERITAS and CRUCIBLE.
The user determines the output format at runtime. The search engine is
format-agnostic. Pipeline steps activate or skip based on the user's chosen output.

```
User input: idea + context (format, audience, depth)
           ↓
    SHARED SEARCH ENGINE (token-efficient, physics-informed)
           ↓
    RANKED EVIDENCE POOL (strongest sources, bridge connections)
           ↓
    USER PICKS OUTPUT FORMAT (paper, spec, brief, analysis, etc.)
           ↓
    CONDITIONAL PIPELINE STEPS (stages adapt to output type)
```

**User directive (2026-08-11):** "the processes should not be siloed they
should just have different steps but both be able to produce outputs with a
focus of either science/academia or technology."

**User directive (2026-08-11):** output formats are NOT limited to two types.
Any format the user needs for that particular search.

**NOTE (2026-08-11 update):** The pipeline has 16 stages, not 8. The UI
PIPELINE_STAGES constant must match the actual veritas_process.py code.
See `references/unified-search-architecture.md` in the
`research-writing-studio-interface` skill for the full 16-stage list.

## The Four-Layer Search Architecture

Designed through sequential mastermind passes with four DS specialists.
Each layer answers a different question. They are NOT competitors. They
stack as layers in a single engine.

```
Layer 4: TURING (pattern formation)        → WHERE are the relevant clusters?
Layer 3: HELMHOLTZ (unconscious inference) → WHICH paper in each cluster to read?
Layer 2: KREBS (metabolic economy)         → HOW DEEPLY to extract from each?
Layer 1: RAO (active inference)            → WHEN to stop (confidence threshold)?
```

### Layer 4 — Turing: Reaction-Diffusion Pattern Formation

**Scientist:** Alan Turing (Manchester, Princeton). "Chemical Basis of
Morphogenesis" (1952). Reaction-diffusion equations produce complex spatial
patterns from homogeneous starting conditions via local activation and
long-range inhibition.

**Principle:** Don't rank papers one by one. Define two opposing forces
across the citation landscape and let relevant clusters EMERGE.

- **Activator (A):** semantic similarity x citation inflow x bridge potential x recency
- **Inhibitor (I):** redundancy suppression (long-range, diffuses faster than activator)
- **Dynamics:** iterate A and I across citation-graph Laplacian until pattern stabilizes
- **Result:** clusters of high-activation papers separated by gaps; bridges = edges between clusters

**Token advantage:** reads only ONE paper per cluster (the center), not all
members. ~1200-2000 tokens for 5-8 clusters.

**User-adjustable:** beta (inhibitor strength) controls cluster selectivity.

### Layer 3 — Helmholtz: Unconscious Inference + Weber-Fechner

**Scientist:** Hermann von Helmholtz (Berlin). Weber-Fechner law, unconscious
inference (1860), nerve conduction velocity, conservation of energy (1847).

**Three laws applied to search:**

1. **Weber-Fechner ranking:** perceived intensity scales logarithmically.
   S = alpha*log(1+citations) + beta*log(1+recency) + gamma*log(1+bridge).
   A paper with 3 citations can outrank one with 500 if recent and cross-field.

2. **Unconscious prior construction:** before spending tokens, infer field
   structure from OpenAlex concept graph. Allocates sampling budget
   proportionally across discovered fields.

3. **Signal detection cutoff:** d-prime score determines relevance threshold.
   d'(paper) = (relevance_score - mean_noise) / std_noise. User-adjustable
   beta cutoff controls sensitivity.

### Layer 2 — Krebs: Graded Metabolic Extraction

**Scientist:** Hans Krebs (Sheffield, Oxford). Citric acid cycle (1937).
Nobel Prize 1953.

**Three principles:**

1. **Evidence compounding (citric acid cycle):** one paper yields five
   metabolites (direct claims, references, methodology, counterarguments,
   bridge connections). 3 deeply metabolized papers outperform 15 shallow reads.

2. **Graded extraction (glycolysis, Krebs, oxidative phosphorylation):**
   - Glycolysis pass: titles + metadata only (~2 tokens/paper, 50 papers)
   - Krebs pass: abstracts only (~100 tokens/paper, 10-15 papers)
   - Oxidative pass: full text (~500-2000 tokens/paper, 3-5 papers)

3. **Allosteric feedback inhibition:** when a claim's confidence exceeds
   threshold, STOP searching for more evidence on it. Reallocate to
   under-fueled claims.

### Layer 1 — Rao: Active Inference Stopping

**Scientist:** the specialist engine (predictive comparison engine).

**Principle:** search is active perception. Each sample maximizes expected
information gain per token. Stop when marginal information gain drops below
token cost.

E(s) = InformationGain(s) - lambda x TokenCost(s)

User-adjustable lambda (cost sensitivity) and max_iterations (gap-fill depth).

## User-Adjustable Parameters (all three exposed in UI)

| Parameter | Symbol | What it controls | Default |
|-----------|--------|-----------------|---------|
| Sensitivity | beta | How selective the engine is | 0.5 |
| Cost sensitivity | lambda | Token savings vs thoroughness | 0.5 |
| Max depth | iterations | Gap-fill cycles to run | 2 |

## Cross-Field Bridge Detection (v2 — graph-based, 2026-08-11)

**Design spec:** `organism/docs/constellation/BRIDGE-ENGINE-SPEC.md`
**Reference impl:** `organism/docs/constellation/bridge_engine.py` (runnable, self-tests pass)
**Full writeup:** `references/bridge-engine-v2-graph-design.md`

### v1 → v2 upgrade (2026-08-11)

The original `research_bridge_engine.py` (v1) used a 3-factor score
(entanglement/novelty/impact) on raw OpenAlex API co-occurrence counts —
no graph, no communities, no embeddings, no centrality. v2 is a full
heterogeneous-graph pipeline with sampled Brandes centrality and four
scoring factors. It is Constellation's core moat.

### The five-stage pipeline

```
NIGHTLY (batch):          QUERY-TIME:
1. Ingest & Embed         3. Candidate Generation (concept-κ triples)
2. Community Detect       4. Bridge Scoring (4-factor geometric mean)
   + Sampled Brandes      5. Rank & Emit (MMR diversity)
```

All expensive work precomputed nightly. Query-time < 50ms per seed.

### Sampled Brandes with inter-community filter

Standard betweenness is O(V·E). **Sampled Brandes** (Brandes & Pich 2007)
estimates from k≪V random sources: O(k·E), unbiased, error O(1/√k).
k=500 default → ±0.045 CI. Run on concept subgraph only (~10⁴ nodes).

**Key innovation:** modify back-propagation to only accumulate delta when
`comm(v) != comm(w)`. Yields **inter-community betweenness (IBC)** — a
concept's centrality as a bridge BETWEEN disciplines. This is Factor 1.

### Four-factor Bridge Score (geometric mean)

```
B = (S_κ^α1 · Φ^α2 · 𝒩^α3 · Δ_cite^α4) ^ (1/Σα)
```

1. **S_κ** — normalized IBC (sampled Brandes, inter-community)
2. **Φ — Surprise (THE MOAT):** Gaussian bell centered at cosine_sim=0.35.
   Explicitly DOWNWEIGHTS high similarity. Pure similarity search optimizes
   for sim→1; the bridge engine optimizes for the gap nobody looks in.
3. **𝒩** — temporal acceleration: recent cross-field co-mention ÷ baseline
4. **Δ_citation** — citation-graph absence: 1.0 if no citation path ≤3 exists

### Canonical example: neuroscience ↔ quantum physics

"Predictive coding in cortical microcircuits" → Bayesian Inference (IBC=0.91)
→ "Quantum Bayes theorem." sim=0.37 (Goldilocks), no citation path,
accelerating 2.1×. Score B=0.93. No keyword overlap, no citation path, sim
below typical thresholds — only the bridge engine surfaces it.

API (unchanged): GET /api/research/bridges, GET /api/research/trending-bridges

The old v1 physics-models framing (quantum tunneling, percolation, Markov
blanket) is superseded. `compute_entanglement` → S_κ, `compute_novelty` →
𝒩, `compute_impact` → Δ_citation. Percolation and health proximity remain
as auxiliary explanation-layer signals.

## Publication Readiness Scoring

**File:** `publication_readiness_engine.py`

Six axes, each 0-100, with venue-adaptive weights:
1. Citation health (grounding, density, recency)
2. Structural integrity (section balance, claim density, EC ratio)
3. Venue fit (adaptive thresholds per venue preset)
4. AI detection risk (burstiness, TTR, predictable phrases)
5. Argument strength (claim verbs, rebuttals, hedging)
6. Voice authenticity (em-dashes, AI vocab, hedge density)

Venue presets: Nature, arXiv, NeurIPS, Blog, Grant.

API: POST /api/publication/readiness, GET /api/publication/venues

## A/B Test Results (2026-08-11 — TESTED, NOT THEORIZED)

An A/B test was run comparing the current pipeline search vs the title-first
v2 methodology across 3 queries. **The results overturned the premise.**

### What the test showed

| Metric | Baseline (current) | V2 (title-first) |
|--------|-------------------|-----------------|
| Titles harvested | 15 | 23-27 |
| Abstracts read | 2-3 | 5 |
| Token cost | ~250 | ~600-750 |
| Search time | ~23s | ~23s |
| Paper quality | 2010-2017, stale | 2024-2026, current |

### The premise was wrong

The entire four-layer architecture was designed to solve a TOKEN WASTE problem
that DOES NOT EXIST. The baseline pipeline only reads 2-3 abstracts per search
because most API results don't include abstracts. The "25 abstracts at 6500
tokens" scenario that motivated the design was never the actual behavior.

### What actually works

The v2 metadata scoring DOES improve result quality through:
1. **Recency weighting** — surfaces 2024-2026 papers that citation-count ranking buries
2. **Title overlap scoring** — finds papers directly on-topic regardless of citation count
3. **Log-scaled citations (Weber-Fechner)** — prevents old high-cite papers from dominating

The token savings DO NOT MATERIALIZE in practice. The real gain is QUALITY.

### What does NOT work

- **Clustering via title keywords** is too crude — most "clusters" have 1 paper.
  Real argument clustering needs semantic similarity, not keyword overlap.
- **Token budget optimization** as a design goal is misplaced when the baseline
  already reads only 2-3 abstracts.

### Honest lesson (user correction 2026-08-11)

> "how does this make it better or are you just telling me it is better to
> shut me up and get me to tell you to proceed?"

The user correctly identified that four brainstorming passes produced the same
idea in four costumes. The lesson: **A/B test before claiming improvement.
The token savings story was theater. The real improvement (recency-weighted
result quality) only emerged from running the actual comparison.**

## Intelligent Topic Discovery (2026-08-11 — SELF-EXPANDING SEARCH)

**File:** `intelligent_search.py`
**API:** `GET /api/topics/intelligent?max_concepts=12`

The hardcoded concept list approach (even with 20 verified fields) is still
a silo. Research publishes 2,000+ papers daily. A fixed menu cannot capture that.

### The co-occurrence discovery approach

Instead of hardcoding fields, the engine DISCOVERS them dynamically:

1. Start with 3 DS seed concepts (FEP, interoception, predictive coding)
2. Search OpenAlex for recent papers matching each seed
3. Extract concept tags from every paper found (co-occurrence analysis)
4. Rank discovered concepts by bridge potential (how many seeds connect to each)
5. Fetch trending papers for top-ranked concepts
6. Include globally trending papers (all fields, no seed filter)

From 3 seeds, the engine discovered 70+ connected fields that nobody hardcoded:
psychology, epistemology, Bayesian probability, allostasis, N400, adaptive
behavior, philosophy of language, clinical psychology, autism research, etc.

### OpenAlex API for co-occurrence

```python
# Search recent papers by text query
url = ("https://api.openalex.org/works"
       "?search=%s&filter=publication_year:2024|2025"
       "&per-page=5&select=id,title,concepts") % seed_query

# Each paper has concept[] tags with scores
for concept in paper["concepts"]:
    name = concept["display_name"]
    cid = concept["id"].split("/")[-1]
    score = concept["score"]  # filter > 0.4 for meaningful relevance
```

### Rate limiting (CRITICAL)

OpenAlex returns HTTP 429 when hit too fast. The engine needs:
- Exponential backoff retry in `_fetch_json()` (1s, 2s, 3s)
- `time.sleep(0.3)` between concept fetches in Phase 2
- Cache results so the UI doesn't re-discover on every page load

### UI wiring

`loadResearchHub()` in writing-studio.html calls `/api/topics/intelligent`
first. Falls back to cached `/api/topics` if the intelligent endpoint fails
or returns < 3 topics. Shows "INTELLIGENT DISCOVERY" header when active.

### Pitfall: concept level filtering

Broad concepts (Level 0 in OpenAlex hierarchy) have millions of papers and
return all-time most-cited papers, not recent work. Examples:
- "Computer science" = 176M works → returns papers from 2009
- "Psychology" = 39M works → same problem

The score > 0.4 filter in `discover_concepts()` helps but doesn't fully solve
this. For truly recent papers, use `from_publication_date` filter (but note:
combined with concept_id filter, this can return 0 results on some concepts
due to OpenAlex indexing delays).

### Commits

- `d8ed855` — intelligent_search.py + /api/topics/intelligent endpoint
- `41dfc22` — Writing Studio UI wired to intelligent discovery

## Popper Gap Analysis (2026-08-11 — 20 gaps, 9 CRITICAL)

the specialist engine traced every process flow through REAL CODE and falsified the
architecture claims. Full details: `references/popper-gap-analysis-and-public-architecture.md`

### The 3 gaps that BLOCK public rollout

1. **No Medical Safety Rail (GAP 9):** public users WILL ask medical
   questions. System answers with zero safety check. Legal liability.
2. **No Evidence Persistence (GAP 11):** every search starts from scratch.
   100 users = 100 redundant API calls = OpenAlex rate-limits everyone.
3. **No Exploratory Flow (GAP 15):** non-experts land on the page, see
   academic field names, and leave. No NL on-ramp.

### The 3 gaps that make the CURRENT system mediocre

4. **Three Disconnected Searches (GAP 1-3):** brainstorm uses hardcoded
   arXiv XML (THE SILO), search-v3 uses OpenAlex only, pipeline Stage 2
   does its own search. Nothing shares data.
5. **Dead-End Flows (GAP 16):** search results have no next actions.
   No "save to library", "find contradictions", "build on this."
6. **Split-Brain VERITAS/CRUCIBLE (GAP 20):** identical 8 stages coded
   as separate codebases. Bug fixes don't propagate. This is the root
   cause of siloing. The user confirmed: "didn't we change how the
   process flows if it is veritas or crucible it is almost the same
   process just different gates."

### Split-Brain Diagnosis (the real architectural debt)

The two "pipelines" share IDENTICAL 8 stages with different GATES:

| Stage | VERITAS | CRUCIBLE |
|-------|---------|----------|
| 0 | Evidence Gate | Evidence Gate + Tech Rules |
| 1 | Topic Refinement | Topic Refinement (same) |
| 2 | Research Gathering | Research Gathering (same) |
| 3 | Physics Gate | Crucible Physics Gate (same engine, different thresholds) |
| 4 | Drafting | Drafting (same) |
| 5 | Adversarial Panel | Adversarial Panel (different seats) |
| 6 | Revision Loop | Revision Loop (same) |
| 7 | QA + Output | QA + Output (same) |

Fix: ONE pipeline class with configurable gates per output format.

### Recommended Build Priority

1. Unify pipelines (GAP 20) — root cause of siloing
2. Connect discovery → search → pipeline (GAP 1-3)
3. Evidence persistence (GAP 11)
4. Medical safety rail (GAP 9)
5. Exploratory flow (GAP 15)

## Public Rollout: Sherrington Integration Architecture

When opening search to everyday people, the evidence spine stays SHARED
and integration layers ADAPT per user type. Every user sees the same
underlying evidence through their specific lens.

Six flows needed: citizen health, professional/clinician, student/learner,
journalist/fact-checker, academic researcher, policy maker.

The critical rule: **no integration layer may originate information.**
Every fact traces back to the shared evidence spine. Layers translate
and package — they never create. Full architecture in
`references/popper-gap-analysis-and-public-architecture.md`.

## Implementation Status (2026-08-11 — ALL 12 GAPS FIXED)

### Completed modules
- `evidence_store.py` — SQLite evidence persistence with cross-source dedup, cached pools, user feedback table (GAP 11, 12, 13)
- `unified_search.py` — THE single search function: cache check → concept-filtered search → V3 score → bridge detect → store (GAP 1-3, 4)
- `safety_rail.py` — medical intent detection, risk levels, auto-disclaimers, user intent classification, NL translation, exploratory starters (GAP 9, 15)
- `evidence_enrichment.py` — evidence tiers, next-step actions, pool summary with provenance (GAP 16, 17, 18)
- `research_bridge_engine.py` — physics-based bridge detection, tested with live data
- `publication_readiness_engine.py` — 6-axis scoring, tested
- `search_ab_test.py` — V3 scoring (IDF + phrase + quality floor + dedup), A/B tested
- `intelligent_search.py` — self-expanding co-occurrence discovery via group_by (GAP 6 fixed with 2hr cache)
- API: `GET /api/research/unified` — live endpoint with safety rail + enrichment + evidence store
- API: `POST /api/pipeline/run?pipeline=veritas|crucible` — unified pipeline runner (GAP 20)
- API: `GET /api/research/exploratory` — plain-language topic starters for non-experts (GAP 15)
- API: `GET /api/research/translate` — NL-to-science translation (GAP 15)
- UI: Research Hub fully wired to `/api/research/unified` (commit e4f0c2a)
- UI: Compose page unified — output format cards replace pipeline toggle (commit efbf8b4)
- UI: Dashboard unified — single pipeline health row, not two (commit 92ec593)
- Opencode: pipeline return shapes confirmed identical, consensus on all 3 questions (msg #1805-1807)

## Concept-ID Detection for Search Quality (CRITICAL FIX, REVISED 2026-08-12)

**The problem:** OpenAlex full-text search for "free energy principle consciousness"
returns dementia and cardiology papers because it matches "energy" literally.
Full-text search treats the query as bag-of-words, not as scientific concepts.

**The WRONG fix (original 2026-08-11, proven broken 2026-08-12):**
concept-filtered search ONLY — `filter=concepts.id:C33553690&sort=cited_by_count:desc`.
This returns the most-cited papers in the ENTIRE concept field, not the most
relevant to the query. "sleep neuroscience" (concept C90856448) returned
"Gammarus species from Xinjiang" (15,793 citations) and "WHO Classification
of Tumors" — completely irrelevant papers that happen to be tagged with the
neuroscience concept and have the most citations.

**The CORRECT fix:** use BOTH full-text search AND concept filter together,
sorted by relevance score, NOT citation count:

```python
CONCEPT_MAP = {
    "free energy principle": "C33553690",
    "free energy": "C33553690",
    "active inference": "C33553690",
    "interoception": "C2908550385",
    "predictive coding": "C2778061373",
    "consciousness": "C71688214",
    "neuroscience": "C90856448",
    "sleep": "C8689300",
    "memory consolidation": "C2986327255",
    "markov blanket": "C33884282",
    "attention": "C121332964",
    "decision making": "C14904185",
    "reinforcement learning": "C154945302",
    "deep learning": "C201016680",
    "bayesian": "C19939987",
    "entropy": "C2996917470",
    "information theory": "C1900190",
    # ... always VERIFY before hardcoding
}
concept_id = None
for phrase, cid in CONCEPT_MAP.items():
    if phrase in query_lower:
        concept_id = cid; break

encoded = urllib.parse.quote(query)
if concept_id:
    # CORRECT: search=text AND filter=concept, sorted by relevance
    url = ("https://api.openalex.org/works?search=%s"
           "&filter=concepts.id:%s,publication_year:2020|2021|2022|2023|2024|2025"
           "&sort=relevance_score:desc&per-page=%d"
           "&select=id,title,cited_by_count,publication_date,doi,concepts,"
           "primary_location,authorships,relevance_score"
           ) % (encoded, concept_id, limit)
else:
    # Fallback: full-text only for unknown topics
    url = ("https://api.openalex.org/works?search=%s"
           "&filter=publication_year:2020|2021|2022|2023|2024|2025"
           "&sort=relevance_score:desc&per-page=%d"
           "&select=id,title,cited_by_count,publication_date,doi,concepts,"
           "primary_location,authorships,relevance_score"
           ) % (encoded, limit)
```

**CRITICAL PITFALL (live-tested 2026-08-12):**
- `filter=concepts.id:X` WITHOUT a `search=` parameter returns the most-cited
  papers in that concept field — garbage for any specific query.
- `sort=cited_by_count:desc` returns the most-cited papers regardless of
  relevance. NEVER use this for research discovery.
- Always combine: `search=query` + `filter=concepts.id:X` + `sort=relevance_score:desc`.
- When changing the search algorithm, CLEAR the evidence cache
  (`DELETE FROM evidence_pools` in writing-studio/evidence.db) — stale cache
  will serve the old garbage results even after code is fixed.

**Pitfall:** the concept map must start empty and be populated ONLY with
curl-verified IDs. Inventing IDs from memory produces 404s (see Pitfall #2).

## Unified Search Endpoint (GAP 1-3 FIX)

**API:** `GET /api/research/unified?q=...&limit=15&user_type=auto&enrich=true`

Complete flow (all deterministic except the fallback search):
1. Classify intent (academic/public/clinical/journalist/student) — 0 tokens
2. Detect medical risk — 0 tokens
3. Check evidence cache (SQLite) — 0 API calls if hit
4. Multi-source search (concept-ID filtered) — 1 API call
5. V3 scoring (IDF + recency + quality floor) — 0 tokens
6. Bridge detection — 0 tokens
7. Store in evidence DB (dedup + feedback table)
8. Enrich: evidence tiers + next actions + pool summary
9. Apply safety rail disclaimer if medical

Returns: `{papers[], pool_summary{}, next_actions[], safety{}, user_type, intent}`

## Evidence Persistence Layer (GAP 11 FIX)

**File:** `evidence_store.py`, **DB:** `writing-studio/evidence.db`

Tables:
- `papers` — deduped by normalized title hash, tracks times_seen across sources
- `search_queries` — every query logged with user_type + intent
- `evidence_pools` — cached result sets with TTL (default 24h)
- `user_feedback` — rating + action per paper (ranking improvement foundation)

Key functions: `store_paper()`, `store_evidence_pool()`, `get_cached_pool()`,
`record_feedback()`, `get_stats()`

## Medical Safety Rail (GAP 9 FIX)

**File:** `safety_rail.py`

- Keyword set: 60+ medical terms (treatment, supplement, pregnancy, cortisol, etc.)
- Phrase patterns: "should i take", "is it safe to", "does X work for Y"
- Risk levels: high (2+ phrase matches), moderate (1 phrase or 2+ keywords),
  low (1 keyword), none
- Disclaimers generated per risk level — never medical advice
- `classify_user_intent()` routes to: academic, public, clinical, journalist,
  student, policy — each gets different integration layer

## Evidence Enrichment (GAP 16, 17, 18 FIX)

**File:** `evidence_enrichment.py`

1. **Evidence tiers:** strong (100+ cites, good venue), established (50+ cites),
   emerging (recent, low cites), theoretical (model keywords), moderate
2. **Next actions:** narrow, recent-only, find-opposing, start-paper,
   explore-related, save-to-library
3. **Pool summary:** confidence assessment (high/moderate/emerging/theoretical),
   tier breakdown, source diversity, year range, provenance chain

### UI Wiring Details (commit e4f0c2a — FULLY WIRED TO UNIFIED SEARCH)

### Research Hub Search (`hubSearch` in writing-studio.html)
Now calls `/api/research/unified?q=...&limit=15` (NOT the old search-v3).
Transforms `d.papers[]` into `renderHubResults()` shape with new fields:
`_evidence_tier`, `_evidence_label`, `_treatment_relevance`, `v3_score`.
Stores the FULL response in `window._unifiedSearchResult` for next-action handlers.

**Pitfall:** hubNextAction() needs access to the full result object (for client-side
filtering like "narrow to strong only"). Store `window._unifiedSearchResult = d` in
hubSearch() before rendering, then read from it in hubNextAction(). Without this,
the refine/filter actions have no data to filter.

**Pool summary rendering:** The header above results shows confidence level
(color-coded: sage=high, ochre=emerging, starlight-dim=moderate), tier breakdown
bar (colored chips), source count, year range, and cache indicator.
**Safety disclaimer:** red/amber box for medical queries, with risk level badge.
**Next-action buttons:** 6 types (refine, action, explore), each calling
hubNextAction(actionStr) which JSON-parses the action and dispatches.

### Publication Readiness (`runPublicationReadiness`)
Venue selector dropdown (arXiv, Nature, NeurIPS, Blog, Grant) in draft editor
below the Writing Audit panel. Calls `POST /api/publication/readiness`.
Renders: overall score (color-coded), 6 axis bars with summaries,
top rejection risks with severity color coding.

### Cross-Field Bridge Discoveries (in `loadResearchHub`)
Fetches `/api/research/trending-bridges` and appends below trending topics.
**CRITICAL:** The API returns `topics[]` (not `results[]`). Each topic has
`best_bridge` (object with `target_field`, `entanglement`), `percolation`,
`health_proximity`, `trend_score`, `trending_papers[]`. Iterating
`results` instead of `topics` silently returns 0 bridges.

## V3 Scoring Algorithm (A/B TESTED 2026-08-11)

**File:** `search_ab_test.py`, function `_metadata_score_v3()`
**API:** `GET /api/research/search-v3?q=...&limit=...&cost_sensitivity=...`

Five components, each addressing a failure mode found in testing:

### 1. Quality Floor (noise filter)
A paper must meet ONE of: citations > 5, OR (year >= 2024 AND title relevance > 0.5),
OR recognized quality venue. Filters book chapter numbers, keyword-stuffed titles.

### 2. IDF-Weighted Term Matching
Rare terms (interoception: 0.9) dominate common terms (system: 0.2). Ensures
discriminating query terms matter more than generic ones.

### 3. N-gram Phrase Matching
"Free energy principle" as a trigram = 0.30. "Artificial intelligence" as a
bigram = 0.20. Prevents generic-keyword papers from outranking specific-concept papers.

### 4. Recency Weighting (the proven real value)
Linear decay over 15 years. This is what ACTUALLY improves results.

### 5. Semantic Dedup Penalty
Jaccard title similarity > 0.6 triggers penalty. Prevents duplicate surveys.

See `references/v3-scoring-algorithm.md` for full details and A/B test results.

## Organism-Aware Architecture (user correction 2026-08-11, repeated 18x)

**User directive:** "understand we have the entire the operator agent organism and mosaic os
to work with for functionality and sending information through"

The search engine must NOT be a standalone Python script. It must flow THROUGH
the the operator agent organism like a nerve signal flows through the body. The organism has
82 specialist engines, the specialist engine (thalamocortical routing), the specialist engine
(cardiovascular message circulation), the specialist engine (quality gates), and the
operator bus connecting hermes and sibling-agent.

### The three-silos problem (diagnosed 2026-08-11)

Three separate systems were built that don't talk to each other:

1. **Discovery** (`intelligent_search.py`): finds connected fields, but output
   doesn't feed into search.
2. **Search** (`optimized_research_search`): finds papers for a query, but
   doesn't feed into the pipeline.
3. **Pipeline** (`VeritasPipeline` stages 0-7.5): Stage 2 does its OWN search
   instead of using the search system. The brainstorm endpoint calls the
   pipeline directly without using intelligent discovery.

### The correct unified flow

```
USER INPUT: idea + output format
     ↓
STAGE -1: DISCOVERY (intelligent_search.py group_by)
     → discovers connected research fields from DS seeds
     → 3 OpenAlex API calls, 0 tokens
     ↓
STAGE 0: EVIDENCE GATHERING (optimized_research_search)
     → multi-source search (arXiv + S2 + Crossref + PubMed + OpenAlex)
     → uses discovered fields as search targets, not just query string
     → RRF fusion + V3 re-rank
     → 5 API calls, 0 tokens
     ↓
STAGE 0.5: BRIDGE DETECTION (research_bridge_engine.py)
     → which field pairs have unexpected connections
     → 0 tokens (deterministic)
     ↓
STAGE 1+: CONDITIONAL PIPELINE
     → output format determines which stages activate
     → VERITAS for academic, CRUCIBLE for tech, custom for anything else
     → uses evidence pool from Stage 0, not its own search
```

**Lane split:** sibling-agent owns the pipeline integration (Stage 2 should call
`optimized_research_search` instead of its own search). the operator agent owns the API
unification + UI wiring.

### OpenAlex group_by optimization (discovered 2026-08-11)

The biggest API cost reduction: use `group_by` to discover ALL co-occurring
concepts in a SINGLE API call per seed concept.

```python
# ONE call returns concept distribution across ALL papers with that concept
url = ("https://api.openalex.org/works"
       "?filter=concepts.id:C33553690,publication_year:2024|2025"
       "&group_by=concepts.id&per-page=25")
# Returns: [{key: concept_id, key_display_name: "Cognitive science", count: 250}, ...]
```

This collapsed the discovery phase from 19 API calls to 4 (3 seeds + 1 global
trending). The group_by endpoint returns co-occurrence counts directly — no
need to read individual papers to extract concept tags.

### "Use PhD persona brains, not generalist" (user correction 2026-08-11)

**User directive:** "don't do this with a generalist brain... you need to have
a best in the world brain with elite university credentials. the multidigit phd
personas we used to work on???? you haven't been using those,.,... shame on you"

When designing algorithms or making architectural decisions, route through DS
Sherman to the appropriate specialist engine (the specialist engine for optimization,
the specialist engine for perception theory, the specialist engine for pattern formation, etc.).
Building as a generalist is a protocol violation. The specialist gate
(`specialist_gate.py --route`) must fire before any design or build work.

## Pitfalls

1. **Don't treat the four layers as competing approaches.** They are
   stacked layers, not alternatives. Building only one gives partial results.

2. **NEVER fabricate API concept IDs.** In the desiloing fix (2026-08-11),
   I invented 14 out of 22 OpenAlex concept IDs from memory. ALL 14 returned
   HTTP 404. The remaining valid IDs resolved to WRONG concepts
   (C154945302 resolved to "Artificial intelligence" with 36M works, not
   "Multi-agent systems"; C71924100 resolved to "Medicine", not "Ecology").
   ALWAYS verify before hardcoding:
   ```
   curl "https://api.openalex.org/concepts?search=TOPIC&per-page=1&select=id,display_name,works_count"
   ```
   Then confirm display_name matches your intent AND works_count is in a
   reasonable range (not 36M for a niche concept). Hardcode ONLY verified IDs.

3. **Topic recommendation silos are a recurring failure.** The topics endpoint
   was siloed because field_queries only covered 8 DS-specific concept IDs
   (FEP, predictive coding, interoception, consciousness, multi-agent,
   adversarial ML, complex systems, LLMs). The user flagged "still very
   siloed" and was right. Fix: expand to 20 fields across physics, biology,
   medicine, environmental science, social sciences, materials, and DS core.
   DS fields are the STARTING POINT for bridge detection, not the BOUNDARY
   of discovery. Bump `_TOPICS_VERSION` whenever field_queries changes to
   invalidate stale cache.

4. **Bridge co-occurrence counts need normalization.** Raw co-occurrence
   between large fields (Psychology x Neuroscience) will always be high.
   Use entanglement score (observed/expected).

4. **The output format is NOT the search's concern.** Search finds evidence.
   The pipeline decides format. Never couple search logic to output format.

5. **Token budget is a USER decision.** The three adjustable parameters
   (beta, lambda, max_depth) must be exposed in the UI, not hidden.

6. **NEVER claim "better" without an A/B test.** Four brainstorming passes
   (Rao, Krebs, Helmholtz, Turing) all claimed superiority over each other
   and over the baseline. The A/B test revealed the token-savings premise
   was wrong — the baseline already reads only 2-3 abstracts. The real
   improvement was result quality (recency weighting), which only emerged
   from running the actual comparison. The user caught this: "how does
   this make it better or are you just telling me it is better to shut me
   up." Design first is fine, but TEST before claiming anything works.

7. **The "four specialist passes" pattern is a fluff trap.** Producing the
   same algorithm wearing different science vocabulary (perception,
   metabolism, inference, morphogenesis) is not multiple approaches — it
   is one idea in four costumes. When the user says "do another pass with
   a different brain," they want a GENUINELY different perspective, not
   the same ranking algorithm renamed.

8. **OpenAlex `primary_location` can be None.** Both `_bridge_papers()`
   and `get_trending_with_bridge_data()` crashed when OpenAlex returned
   `null` for `primary_location` (common for preprints). Always use
   defensive extraction: `loc = w.get("primary_location") or {}` then
   `isinstance(loc, dict)` check before `.get("source")`.

9. **"Do another pass" = RUN THE SYSTEM, check OUTPUT, fix via ROUTING.**
   When specialist is RUNNING: WAIT. Do NOT produce parallel answers.
   Never write specialist content on timeout. Never produce the same
   deliverable a specialist is currently working on.

10. **Never assume the API response key structure.** When wiring an endpoint
    to the UI, ALWAYS curl the endpoint first and inspect the actual JSON
    keys before writing the JS that parses it. The trending-bridges endpoint
    returns `topics[]` not `results[]`. The search-v3 endpoint returns
    `top_papers[]` not `papers[]`. Silently iterating the wrong key returns
    an empty array with no error — the UI shows nothing and you don't know
    why. Pattern: `curl -s http://localhost:port/api/X | python3 -m json.tool`
    before writing the `renderX()` function.

11. **"Build right... dont go fast" means verify in the browser, not just**
    **in the API.** API tests confirm the endpoint works. They do NOT confirm
    the JS function correctly parses the response, renders the DOM, or
    handles the select/button lifecycle. After wiring UI: restart server,
    curl every endpoint to confirm real data shapes, AND run a Puppeteer/
    browser test to confirm the rendered output exists in the DOM. The user
    corrected when asked to rush: "build right... dont go fast."

12. **NEVER hardcode a fixed list of concept IDs as the discovery boundary.**
    Even 20 verified fields across all sciences is still a silo. Research
    publishes 2,000+ papers daily. Use the co-occurrence discovery engine
    (`intelligent_search.py`) instead: start from DS seeds, discover
    connected fields dynamically from what researchers are actually
    publishing. The user flagged "this search is still too narrow with only
    20 fields and isn't intelligent searching."

13. **OpenAlex rate limiting (429) is aggressive and silent.** When fetching
    multiple concept IDs in sequence, add `time.sleep(0.3)` between calls
    AND implement exponential backoff retry in the fetch function. Without
    both, the API silently returns 429s that get swallowed by try/except
    blocks, producing 0 results with no error message. Pattern: always log
    the actual HTTP status, never blanket-catch without logging.

    **SOLVED (2026-08-11): 4-layer protection built.** See
    `references/rate-limit-protection.md` in the
    `research-writing-studio-interface` skill for the full architecture:
    Layer 1 token-bucket limiter (8/s per API), Layer 2 semantic concept-ID
    cache, Layer 3 Semantic Scholar failover, Layer 4 nightly prewarm cron.
    Rate limiter verified: burst of 10 then 0.13s spacing (8/s steady).

10. **Exact betweenness is infeasible at scale.** O(V·E) on a million-node
    graph is ~10¹³ ops. Use **sampled Brandes** (Brandes & Pich 2007):
    O(k·E) from k random sources, unbiased, error O(1/√k). k=500 is
    sufficient for ranking bridge vertices. Never reach for exact Brandes
    on a graph with > ~10⁴ nodes.

11. **Standard betweenness finds hubs, not bridges.** A high-betweenness
    node may just be a popular hub within one community. For bridge
    detection you must use **inter-community betweenness**: modify the
    back-propagation to only accumulate delta when `comm(v) != comm(w)`.
    Without this filter, the centrality score rewards the wrong nodes.

12. **Pure cosine similarity cannot find bridges — it downranks them.**
    The whole point of a bridge is that it connects distant papers (sim≈0.35).
    If you rank candidates by sim alone, you reproduce nearest-neighbor
    search and miss every bridge. The Surprise factor (Φ) is a Gaussian
    that PEAKS at sim=0.35 and explicitly penalizes sim→1. This is the
    moat: optimize for the gap, not for similarity.

13. **Run centrality on the concept subgraph, not the full paper graph.**
    The concept subgraph is ~10⁴ nodes; sampled Brandes runs in seconds.
    The full paper graph is 10⁶+ nodes and wastes compute. Papers get
    their bridge score via the concepts they mention — they don't need
    their own centrality.

14. **VERITAS and CRUCIBLE are ONE pipeline with different gates, NOT two
    pipelines.** The user confirmed this explicitly: "didn't we change how the
    process flows if it is veritas or crucible it is almost the same process
    just different gates." The codebase still has them as separate classes
    (VeritasPipeline, CruciblePipeline) with identical stages duplicated.
    This is a split-brain lesion — bug fixes don't propagate, evidence isn't
    shared. The fix is ONE pipeline class with configurable gate thresholds
    per output format. NEVER design or build them as separate systems.
    The pipeline has 16 stages (0-7.5 with half-steps), NOT 8. Count
    `def stage*` methods before writing any UI stage list.

15. **When the user flags a redundant UI section, DELETE it — do not relocate.**
    The user said "why is there an entire section under this then that also
    lists writing outputs?" I initially moved the catalog to the TOP of the
    page as a "primary selector." Wrong. The catalog was redundant with the
    Document Type dropdown. One selector wins (the one already wired to the
    backend). Delete the other entirely (HTML + JS renderer + event handlers
    + switchView call). Never create a third "unified" version.

15. **Process flows end at display, not at action.** Every search result is
    a dead end. The user gets cards and then... nothing. No "save to library",
    no "start paper from this", no "find contradictions", no "build on this
    evidence." Research is ITERATIVE — the system treats it as one-shot. Every
    result card needs contextual next actions that continue the flow.

16. **No evidence persistence = scale failure.** Every search fetches papers
    fresh from APIs. With 100 users, that's 100 redundant calls to OpenAlex
    for the same topic. The API rate-limits everyone. Store results in SQLite
    with a TTL. Cross-query deduplication. The system should REMEMBER what
    it found.

17. **Public rollout requires a medical safety rail (non-negotiable).** Public
    users WILL ask medical questions. The system WILL answer without any
    safety check. This is legal and ethical liability on day one. The safety
    rail is rule-based (keyword detection + static disclaimer template), costs
    0 tokens, and must be ALWAYS ON for citizen-flow queries.

18. **Every branch in a tiering/classification function MUST assign all output
    keys.** `evidence_enrichment.py` tier_evidence() crashed the server because
    the `established` tier branch (citations >= 50) set `evidence_label` but
    forgot to set `evidence_tier`. The provenance dict then referenced
    `paper["evidence_tier"]` which raised KeyError. Pattern: after any
    if/elif/else classifier, every branch must set ALL output keys, OR set a
    default before the chain. Test with `curl` after restart to catch it.

19. **The split-brain shows in the UI, not just the backend.** Even after
    unifying the API runner (`_run_pipeline_async`), the user STILL saw "2
    processes" because the dashboard HTML had two pipe-health rows (Veritas +
    Crucible) and the compose page had two pipeline selector cards. The user
    had to say "i still see 2 processes in my ui" (repeated 25 times) before
    we found the dashboard dual-row. Lesson: when removing a split, trace EVERY
    layer — backend runner, API endpoint, UI selector cards, dashboard health
    bars, hero description text, JS state variables. A split at any layer
    re-creates the appearance of two systems. Search for ALL of:
    `pipe-health-name`, `pipe-selector`, `PIPELINE_STAGES.*crucible`,
    `selectedPipeline`, `data-pipeline=`. Replace with a single unified
    format selector (paper/spec/analysis) that maps to pipeline behind the scenes.

20. **_utc() definition order crash.** `pipeline_api.py` called
    `_recover_orphaned_runs()` at module load (line 104), but `_utc()` was
    defined at line 223. NameError on every startup. AND the function body used
    `datetime.datetime.now(datetime.timezone.utc)` but the file imports
    `from datetime import datetime, timezone` — so the correct call is
    `datetime.now(timezone.utc)`. Pattern: when moving a helper function above
    its caller, check the import style matches the function body. This was a
    pre-existing bug that only surfaced after a restart with orphaned runs in
    the pipeline_runs.db. Fix: move `_utc()` definition above
    `_recover_orphaned_runs()` and match the import style.

21. **The dashboard hero description carries legacy "two pipelines" language.**
    After unifying pipelines, the hero text still said "Two research pipelines
    grounded in a living knowledge base." The user sees this immediately on
    page load. When removing a split, grep for ALL user-visible text that
    references the old architecture: hero descriptions, labels, tooltips,
    placeholder text, alt text, aria-labels.

22. **Pipeline name case mismatch silently breaks every run.** (2026-08-12)
    `run_unified_pipeline()` passed `pipeline="Veritas"` (capital V) to
    `_run_pipeline_async()` which checked `if pipeline == "veritas"` (lowercase).
    Every unified pipeline run crashed instantly with `ValueError: Unknown
    pipeline: Veritas`. The `/api/veritas/run` and `/api/crucible/run` endpoints
    had the same mismatch. Fix: normalize ALL pipeline names to lowercase
    before routing — `pipeline_lower = pipeline.lower()` — and use that
    everywhere downstream (run_id prefix, _runs dict key, async args, poll_url).
    This is the #1 class of bug when unifying two previously-separate code paths:
    string identity is case-sensitive and no test catches it until you run the
    actual endpoint live.

23. **Brainstorm evidence is destroyed at the handoff to pipeline.** (2026-08-12)
    `launchFromAngle()` flattened the seed+angle into a plain string and called
    `newDraft()`. Research principles, live papers, physics scores — all lost.
    The pipeline then re-searched from scratch. Fix: add `pre_gathered_evidence`
    + `search_terms` fields to the run request model, package the angle's
    evidence into those fields, and launch the pipeline directly (not via draft
    creation alone). The pipeline must be wired to consume pre-gathered evidence
    (engine-level, sibling-agent lane).

## References

- `references/four-layer-search-architecture.md` — full design from four specialist passes
- `references/v3-scoring-algorithm.md` — A/B tested v3 scoring: IDF, phrase matching, quality floor, recency weighting. Includes test results and honest assessment of what works vs what doesn't.
- `references/bridge-engine-v2-graph-design.md` — graph-based bridge detection v2: five-stage pipeline, sampled Brandes with inter-community filter, four-factor geometric-mean score (S_κ/Φ/𝒩/Δ_cite), neuroscience↔quantum walk-through, v1→v2 migration map.
- `references/intelligent-search-design.md` — self-expanding co-occurrence discovery engine. No hardcoded concept IDs. Discovers 70+ fields from 3 seeds via OpenAlex concept tags.
- `references/organism-search-architecture.md` — the three-silos diagnosis, correct unified flow (discovery→search→bridge→conditional pipeline), OpenAlex group_by optimization, organism infrastructure map, and PhD persona brain routing pattern.
- `references/popper-gap-analysis-and-public-architecture.md` — 20-gap falsification audit of all process flows. Split-brain VERITAS/CRUCIBLE diagnosis. Public rollout Sherrington integration architecture (6 user flows, shared evidence spine, medical safety rail).
- `references/unified-search-system-architecture.md` — the 9-step unified search flow (safety rail → cache → concept-filtered search → V3 score → bridge detect → evidence store → enrich → disclaimer). Module reference for evidence_store.py, safety_rail.py, evidence_enrichment.py, unified_search.py. UI wiring details for hubSearch() + hubNextAction().
