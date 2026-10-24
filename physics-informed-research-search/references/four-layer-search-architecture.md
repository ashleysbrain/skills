# Four-Layer Search Architecture — Full Design

From sequential mastermind passes (2026-08-11) with four DS specialists.
Each specialist was routed through Sherman and given the previous pass to
build on. The result is a stacked architecture, not four competing approaches.

## Design Session Context

User directive: "come up with a better search method for our needs. do
research and figure out a better algorithm using physics or another science"

User directive: "we need to come up with or copy an innovative search
algorithm/methodology so the ai can search through using as few of tokens
as possible while navigating through information and finding the best answer"

User directive on architecture: "the processes should not be siloed they
should just have different steps but both be able to produce outputs with a
focus of either science/academia or technology"

User directive on output: NOT limited to two formats. Any output the user
needs for that particular search.

User directive on parameters: sensitivity, cost, and max depth should all
be USER ADJUSTABLE.

## Layer 4: Turing (Pattern Formation)

### The Insight

Every search tool ranks papers one by one using sequential decisions. Turing
showed in 1952 that complex patterns can EMERGE from two opposing forces
acting across a space, without any decision-maker.

### The Equation

```
dA/dt = DA * laplacian(A) + A^2/(I+epsilon) - mu*A
dI/dt = DI * laplacian(I) + A^2 - nu*I

where:
  DA < DI  (inhibitor diffuses faster — LOCAL ACTIVATION, LONG-RANGE INHIBITION)
  laplacian = citation-graph Laplacian operator
  mu, nu = decay rates
  epsilon = small constant to prevent division by zero
```

### Applied to Search

- Nodes = papers from multi-source search (OpenAlex, arXiv, S2, Crossref)
- Graph edges = co-citation and co-cited relationships
- Activator field initialized from: semantic similarity x citation velocity x bridge potential
- Inhibitor field starts at zero, grows where activator is high (redundancy suppression)
- Iterate until pattern stabilizes (typically 5-15 iterations)
- Extract connected components of high-activation nodes = clusters
- Each cluster = one argument/perspective
- Edges between clusters = BRIDGES (novel research opportunities)

### Why It Works

- No order dependence (all nodes evaluated simultaneously)
- No greedy traps (a paper irrelevant in isolation may be inside a relevant cluster)
- Natural clustering (no manual grouping needed)
- Automatic redundancy removal (inhibitor suppresses duplicate findings)
- Reads only cluster centers (1 abstract per cluster, not per member)

### Token Cost

~1200-2000 tokens for 5-8 clusters. Lowest of all four approaches.

## Layer 3: Helmholtz (Unconscious Inference)

### Three Laws

**1. Weber-Fechner Ranking:**

```
S(paper) = alpha * log(1 + citations) 
         + beta  * log(1 + recency_weight) 
         + gamma * log(1 + bridge_score)
```

A paper with 3 citations that is recent and cross-field can outrank a paper
with 500 citations that is old and siloed. No tool on the market does this.

**2. Unconscious Prior Construction:**

Before spending tokens, compute field structure from OpenAlex concept API:

```
P(field_structure | query) from concept graph
  = multi-field probability distribution

Example: "interoception prediction error" maps to:
  40% neuroscience, 25% clinical psychology, 15% philosophy, 20% other

Sampling budget allocated proportionally:
  40% of abstract-fetches from neuroscience sources
  25% from psychology
  15% from philosophy
```

**3. Signal Detection Cutoff:**

```
d'(paper) = (relevance_score - mean_noise) / std_noise

Decision rule:
  d' > beta_cutoff → SAMPLE (read the abstract)
  d' < beta_cutoff → REJECT (skip, save tokens)
```

User-adjustable beta cutoff: low = sensitive (more papers, more tokens),
high = selective (fewer papers, fewer tokens).

### Posterior Correction

After reading abstracts, LLM updates field beliefs:
"Based on what I read, this is actually 60% computational neuroscience,
20% pharmacology. Philosophy is absent."

Remaining budget reallocated to CORRECTED proportions. Loop max_depth times.

## Layer 2: Krebs (Metabolic Economy)

### Three Principles

**1. Evidence Compounding (Citric Acid Cycle):**

One paper yields five metabolites:
1. Direct claims (fuel for the argument)
2. Paper's references (new sources — citation graph expansion)
3. Methodology (reusable for user's own work)
4. Counterarguments (fuel for rebuttal section)
5. Bridge connections (cross-field links)

3 deeply metabolized papers outperform 15 shallowly read ones.

**2. Graded Extraction:**

```
Glycolysis pass  → 50 papers, titles + metadata only     → ~100 total tokens
Krebs pass       → 10-15 papers, abstracts only           → ~1000-1500 tokens  
Oxidative pass   → 3-5 papers, full text if available     → ~1500-3000 tokens
```

User controls where the budget goes. Quick scan stops at glycolysis.
Deep dive goes to oxidative phosphorylation.

**3. Allosteric Feedback Inhibition:**

```
for each claim c in the argument:
    if confidence(c) > confidence_threshold:
        stop searching for evidence on c
        reallocate budget to claims with confidence < threshold
```

The engine knows when to stop because the claims tell it.

## Layer 1: Rao (Active Inference)

### The Principle

Search is active perception. Each sample maximizes expected information gain
per token cost.

```
E(s) = InformationGain(s) - lambda * TokenCost(s)

where:
  E(s) = expected value of sampling source s
  InformationGain(s) = KL divergence between posterior and prior
  TokenCost(s) = tokens required to read source s
  lambda = user-adjustable cost sensitivity
```

### The Cycle

```
Phase 1: PRIOR CONSTRUCTION (0 tokens)
   Query → concept graph from OpenAlex (titles + metadata only)
   
Phase 2: SALIENCE MAPPING (0 tokens)
   Compute expected information gain per paper
   
Phase 3: ACTIVE SAMPLING (tokens spent)
   Pull abstracts for top-K salient papers only (K=3-5)
   
Phase 4: BELIEF UPDATE + GAP TARGETING (tokens spent)
   LLM: "I'm confident about X. I know nothing about Y."
   Gap Y becomes new query → back to Phase 1
   Max iterations = user-adjustable
```

## Token Comparison Table

| Method | Papers touched | Abstracts read by LLM | Tokens | Quality |
|--------|---------------|----------------------|--------|---------|
| Current pipeline | 25 | 25 | ~6500 | Good |
| Rao alone | 5-8 | 5-8 | ~1500 | Good (might miss connections) |
| Krebs alone | 50→3-5 | 10-15 | ~2500-4000 | Better (metabolite extraction) |
| Helmholtz alone | 8-15 | 8-12 | ~2000-3500 | Better (multi-field proportional) |
| **Four-layer stack** | **50→clusters→centers** | **5-8 (one per cluster)** | **~1200-2500** | **Best (all four insights combined)** |

## Implementation Files

- `research_bridge_engine.py` — bridge detection (quantum tunneling, percolation, health proximity)
- `publication_readiness_engine.py` — six-axis scoring with venue presets
- `pipeline_api.py` — 4 new API endpoints: /api/research/bridges, /api/research/trending-bridges, /api/publication/readiness, /api/publication/venues

## Mastermind Synergy

Telegram the operator agent identified the same siloing problem independently (msg #1778).
Opencode fixed the pipeline-side field-agnostic search (msg #1780).
the operator agent built the bridge + publication readiness engines (msg #1777, #1781).
Opencode confirmed Stage 0.5 Bridge Discovery integration is their lane.

## Publishable Contribution

"Reaction-Diffusion Search: Turing Patterns in Citation Networks for
Token-Efficient Literature Discovery"

Novel contributions:
1. First use of reaction-diffusion dynamics for document ranking
2. Emergent clustering without LLM calls
3. Bridge detection as natural consequence of Turing instability
4. Weber-Fechner log-scale salience (vs raw citation count everywhere else)
5. Proportional multi-field sampling from inferred prior
