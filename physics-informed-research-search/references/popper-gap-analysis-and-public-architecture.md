# Popper Gap Analysis + Public Rollout Architecture

## Session: 2026-08-11

the specialist engine conducted a rigorous falsification audit of the entire research
system, tracing every process flow through REAL CODE. 20 gaps found.

## The 3 Blocking Gaps (prevent public rollout)

### GAP 9: No Medical Safety Rail
A parent WILL ask "should I take ashwagandha while pregnant." The system
WILL answer. Zero safety rail exists. Legal liability on day one.

Fix: intent classifier detects health/medical queries. Rule-based safety
rail adds disclaimer. 0 tokens (keyword detection + static template).

### GAP 11: No Evidence Persistence
Papers are fetched fresh every search. Nothing stored in SQLite. 100 users
searching the same topic = 100 redundant OpenAlex API calls = rate limit
blocks everyone.

Fix: cache search results in a papers table. TTL-based expiry. Cross-query
deduplication. 0 additional token cost.

### GAP 15: No Exploratory Flow
Non-expert users land on the Studio and see "Cognitive Science, Predictive
Coding, N400." They leave. There's no on-ramp for someone who doesn't
already know the vocabulary.

Fix: guided entry points ("I want to understand stress", "I'm researching
sleep"). Natural language input box, not academic query box.

## The 3 Critical Process-Flow Gaps (affect the principal now)

### GAP 1-3: Three Disconnected Search Implementations
Three independent search systems that don't share data:

1. `/api/brainstorm` — hardcoded arXiv XML + S2 fallback. Hardcoded
   categories (q-bio.NC for veritas). THIS IS THE SILO that sibling-agent
   fixed in research_discovery.py but the brainstorm endpoint STILL has.
2. `/api/research/search-v3` — OpenAlex only with V3 IDF scoring.
3. `veritas_process.py` Stage 2 — `optimized_research_search` (5 sources +
   RRF). The best one, but the pipeline doesn't use it.

Fix: ONE unified search function. All three callers use it.

### GAP 16: Dead-End Flows
Every search result is a dead end. No "save to library", no "start paper
from this", no "find more like this", no "what contradicts this", no "build
on this evidence". The flow STOPS at display.

Fix: every result card needs contextual next actions.

### GAP 20: Split-Brain (VERITAS/CRUCIBLE)
The two pipelines share IDENTICAL 8 stages with different GATES. But they
are coded as separate codebases. Bug fixes in one don't propagate. Evidence
gathered by one isn't visible to the other. This is a corpus callosum lesion.

VERITAS Stage 0 = Evidence Gate | CRUCIBLE Stage 0 = Evidence Gate + Tech Rules
VERITAS Stage 3 = Physics Gate   | CRUCIBLE Stage 3 = Crucible Physics Gate
All other stages are structurally identical.

Fix: ONE pipeline class with configurable gates per output format.

## Public Rollout Architecture (Sherrington Integration Model)

The evidence spine is SHARED. Integration layers ADAPT. Every user type
sees the same underlying evidence, filtered through their specific lens.

```
                    THE SHARED EVIDENCE SPINE
                    (one pool, built once, served to all)
                              |
         +--------------------+---------------------+
         v                    v                     v
    INTEGRATION           INTEGRATION          INTEGRATION
    LAYER:                LAYER:               LAYER:
    Researcher            Clinician            Citizen
         |                    |                     |
         v                    v                     v
    Full methodology     Clinical              Plain-language
    + raw data           decision support     answer + safety rail
    + future work        + contraindications  + evidence tiers
                         + drug interactions  + "talk to your doctor"
```

### The critical rule
No integration layer may originate information. Every fact, every claim,
every evidence tag must trace back to the shared evidence spine. The layers
translate and package — they never create.

### Six Process Flows for Public Users

| Flow | User Type | Input Shape | Output Shape | Safety Rail |
|------|-----------|-------------|--------------|-------------|
| 1 | Citizen health | NL question | Plain answer + tiers | Medical rail ALWAYS ON |
| 2 | Professional | Clinical query | GRADE scoring + CI | "Evidence support, not Rx" |
| 3 | Student/Learner | Concept question | Concept ladder + prereqs | None (conceptual) |
| 4 | Journalist | Verification query | Provenance chain + replication status | Source attribution |
| 5 | Academic | Research query | Full pipeline output | None (expert) |
| 6 | Policy maker | Impact query | Population-level evidence + cost-benefit | Regulatory context |

### Token cost by flow
All flows draw from the SAME evidence spine (0 tokens for search, already
built). The integration layer cost varies:
- Citizen: ~500 tokens (translation + actionability)
- Clinician: ~200 tokens (GRADE formatting)
- Academic: ~2000+ tokens (full pipeline stages 3-7)
- Student: ~300 tokens (concept ladder)
- Journalist: ~200 tokens (provenance formatting)

### New Components Needed for Public

| Component | Purpose | Cost | Priority |
|-----------|---------|------|----------|
| Intent Classifier | Route to correct integration layer | 0 tokens | P0 |
| NL-to-Science Translator | Map everyday language to concepts | ~200 tokens | P0 |
| Evidence Tier Engine | Tag strong/emerging/theoretical/contested | 0 tokens | P1 |
| Contradiction Detector | Surface opposing findings | 0 tokens | P1 |
| GRADE Quality Scorer | Clinical evidence evaluation | 0 tokens | P2 |
| Literacy Adapter | Inline definitions, reading level | 0 tokens | P2 |

## Recommended Build Priority (Popper)

1. **Unify the pipelines** (GAP 20) — merge VERITAS/CRUCIBLE into one
   configurable pipeline. Eliminates root cause of siloing.
2. **Connect discovery → search → pipeline** (GAP 1-3) — one search
   function everything calls.
3. **Add evidence persistence** (GAP 11) — store results in SQLite.
4. **Medical safety rail** (GAP 9) — required before any public user.
5. **Exploratory flow** (GAP 15) — guided entry for non-experts.
