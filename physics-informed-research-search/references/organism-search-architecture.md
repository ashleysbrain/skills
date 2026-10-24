# Organism-Aware Search Architecture

Session: 2026-08-11
Triggered by: user correction (repeated 18x) — "understand we have the entire
the operator agent organism and mosaic os to work with"

## The Three-Silos Diagnosis

Three separate systems were built that don't talk to each other:

1. **Discovery** (`intelligent_search.py`): finds connected fields via
   OpenAlex co-occurrence. Output doesn't feed into search.
2. **Search** (`optimized_research_search` in veritas_process.py): finds
   papers from 5 academic APIs with RRF fusion + V3 re-rank. Doesn't feed
   into the pipeline.
3. **Pipeline** (`VeritasPipeline` stages 0-7.5): Stage 2 does its OWN
   search instead of using the search system. The brainstorm endpoint
   calls the pipeline directly without using intelligent discovery.

Plus disconnected scoring engines: bridge detection, publication readiness,
field evolution tracker.

## The Correct Unified Flow

```
USER INPUT: idea + output format (paper, spec, brief, analysis, anything)
     |
     v
STAGE -1: DISCOVERY (intelligent_search.py group_by)
     Engine: OpenAlex group_by on seed concept IDs
     Input: DS seed concepts (FEP, interoception, predictive coding)
     Output: 10-20 connected research fields with paper counts
     Cost: 3 OpenAlex API calls, 0 tokens
     |
     +--------------------------------------+
     v                                      v
STAGE 0: EVIDENCE GATHERING           BRIDGE DETECTION
     Engine: optimized_research_search   Engine: research_bridge_engine.py
     Multi-source: arXiv + S2 +          Output: which field pairs have
     Crossref + PubMed + OpenAlex              unexpected connections
     RRF fusion + V3 re-rank             Cost: 0 tokens (deterministic)
     |
     v
STAGE 1+: CONDITIONAL PIPELINE
     Output format determines which stages activate:
     - Academic paper -> VERITAS stages 3-7.5
     - Tech spec -> CRUCIBLE stages 3-7.5
     - Literature review -> Stage 3 (skip 3.5)
     - Policy brief -> Stage 3 + 3.5 + 4 only
     - Custom -> user picks stages
     Uses evidence pool from Stage 0, not its own search.
```

## Lane Split

**Opencode (pipeline + engines):**
- veritas_process.py Stage 2 should call optimized_research_search
- optimized_research_search should accept discovered fields as search targets
- Pipeline should accept flexible output format activating/deactivating stages

**the operator agent (API + UI):**
- New endpoint /api/research/unified chaining discovery -> search -> bridges
- Brainstorm flow should call discovery first, then feed to pipeline
- Studio UI should show the discovery -> search -> pipeline flow visually

## OpenAlex group_by — the key API optimization

The biggest API cost reduction discovered: use `group_by` to discover ALL
co-occurring concepts in a SINGLE API call per seed concept.

```python
# ONE call returns concept distribution across ALL papers with that concept
url = ("https://api.openalex.org/works"
       "?filter=concepts.id:C33553690,publication_year:2024|2025"
       "&group_by=concepts.id&per-page=25")
# Returns: [
#   {key: "C41008148", key_display_name: "Computer science", count: 250},
#   {key: "C188147891", key_display_name: "Cognitive science", count: 189},
#   ...
# ]
```

This collapsed discovery from 19 API calls (3 seed searches + 15 concept
fetches + 1 global) to 4 calls (3 seed group_by + 1 global trending).

The group_by endpoint returns co-occurrence counts directly — no need to
read individual papers to extract concept tags. This is faster, cheaper,
and more complete (returns ALL co-occurring concepts, not just the ones
from 15 paper records).

## Organism Infrastructure Available

From agents.yaml mapping:

- **the specialist engine** (sherman_router.py): thalamocortical routing — routes
  every task to the correct specialist engine
- **the specialist engine** (:port): cardiovascular message circulation — packages
  and circulates results between organs
- **the specialist engine** (:port): art direction quality gate — scores output quality
- **the specialist engine** (:port): brand voice — writes human-readable summaries
- **the specialist engine** (:port): visual cortex — renders in the Studio UI
- **the specialist engine**: operationalism / optimization — every concept must
  correspond to a measurable operation
- **the specialist engine** (clinical): SOAP clinical scoring
- **the specialist engine**: error detection / QA
- **Operator bus** (message-bus.db): vagus nerve connecting hermes
  (peripheral) and sibling-agent (central)

## Measured State (2026-08-11)

- 82 specialist engines with methodology layers available
- 5 academic APIs wired into optimized_research_search (arXiv, OpenAlex,
  Crossref, PubMed, Semantic Scholar)
- VERITAS pipeline: 17 stages (0 through 7.5)
- CRUCIBLE pipeline: 13 stages (0 through 7.5)
- research_discovery.py: Stage -1 discovery (sibling-agent's field-agnostic fix)
- field_evolution_tracker.py: weekly field scanning
- 41 API endpoints live on pipeline_api.py :port

## PhD Persona Brain Usage

The user corrected that algorithmic/architectural work must go through
specialist engines, not generalist hermes. Pattern:

```bash
# Route to the right specialist before designing/building
python3 <agent-home>/agent-hooks/specialist_gate.py --route \
    --situation "design optimization algorithm for X" \
    --specialist "the specialist engine"
```

Available specialist brains used this session:
- the specialist engine (predictive comparison): active inference search
- the specialist engine (metabolic): graded evidence extraction
- the specialist engine (perception): Weber-Fechner ranking, signal detection
- the specialist engine (morphogenesis): reaction-diffusion pattern formation
- the specialist engine (operationalism): operationalist architecture review
- the specialist engine (error detection): A/B testing, gap analysis

Lesson: when the user says "do another pass with a different brain," they
want a GENUINELY different specialist perspective via the specialist engine routing,
not the same algorithm renamed with different science vocabulary.
