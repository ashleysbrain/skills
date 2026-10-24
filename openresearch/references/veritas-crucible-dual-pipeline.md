# Veritas + Crucible: Dual Research Validation Pipelines

## Overview

Two sibling processes sharing the same 7-stage physics-grounded
architecture but calibrated for different audiences and domains.

**Veritas** (Latin: truth) — academic/scientific research validation.
Owner: GG3 (the principal). Audience: academic, scientific, consciousness
research community.

**Crucible** (Medieval Latin: vessel of extreme heat testing) —
technology research validation. Owner: Cyber the operator agent (the principal). Audience:
technology leaders, entrepreneurs, small business owners, security
professionals.

## The 7 Stages (Both Processes)

### Stage 0: Evidence Level Gate

Before any writing or research begins, classify the evidence level:

| Level | Weight | Veritas Language | Crucible Language |
|-------|--------|-----------------|-------------------|
| Original Data | 1.0 | "our data show", "we found" | "our benchmarks show", "we measured" |
| Literature Synthesis | 0.6 | "converging evidence suggests" | "industry research indicates" |
| Theoretical | 0.3 | "we propose", "future work should test" | "we propose this architecture" |
| Mixed | 0.7 | "partially supported by our data" | "supported by testing and research" |

Rule: "demonstrates" at Literature Synthesis or Theoretical level = automatic flag.

### Stage 1: Intake and Topic Refinement

Human inputs idea ONE time. Process asks clarifying questions internally.

1. Human submits raw idea
2. the specialist engine routes to the specialist engine for topic expansion
3. the specialist engine generates 3-5 refined topic angles
4. the specialist engine checks against prior publications (dedup)
5. the specialist engine checks for novelty
6. If duplicate: STOP, report, suggest novel angle
7. If novel: proceed

Human touchpoint: ONE. They see refined topics and pick one. Then the
process runs autonomously until output.

### Stage 2: Research and Evidence Gathering

1. the specialist engine routes to OpenResearcher for literature search
2. Sources: arXiv API, OpenAlex API, Crossref, Semantic Scholar
3. DS O'Keefe (:port) checks against consolidated knowledge (dedup)
4. Each finding enters the physics gate (Stage 3)
5. the specialist engine checks for real-time developments
6. the specialist engine monitors confidence levels

Citation verification (CRITICAL):
- Every citation verified against 2+ sources
- Citations come ONLY from real API calls, never LLM-generated
- DOI must resolve to real publication
- Citation log: source API, query, timestamp, DOI, verification status
- Rate limiting: 1 req/3s for arXiv, exponential backoff for others

### Stage 3: Physics Gate (Veritas/Crucible Engine)

Four complementary physics approaches on the same data:

1. **Free Energy (Friston):** Is the claim surprising? F = cost - T*info_gain
2. **Coupling (Kuramoto):** Do validation perspectives cohere?
3. **Critical Slowing Down:** Are reviewers converging or diverging?
4. **Bayesian:** How does evidence shift belief?

Verdict: PASS / REVISE / FAIL. the specialist engine issues the verdict.

Engine route: the specialist engine, the specialist engine, the specialist engine, the specialist engine, the specialist engine.

### Stage 4: Drafting

1. the specialist engine routes to domain specialist
2. Specialist drafts following evidence-level classification
3. the specialist engine (:port) applies voice, removes AI telltales
4. the specialist engine (:port) designs figures/diagrams
5. the specialist engine (:port) renders output

### Stage 5: Adversarial Panel Review

**Consecutive, not in concert.** Each reviewer builds on the previous.

Veritas panel (8 seats): Popper, Kahneman, Wernicke, 3 domain specialists,
Machiavelli, Bentham.

Crucible panel (9 seats): Popper, Kahneman, Wernicke, security/adversarial
specialist, systems engineering specialist, domain expert, the specialist engine,
audience proxy (entrepreneur/SBO perspective), the specialist engine.

Scoring: Floor 7.0/10 for abstracts, 8.0/10 for keynotes. Dissent
requirement: no PASS above 8.0 unless 2+ reviewers scored below 6.0.

### Stage 6: Revision (Internal Loop)

If any seat returns REVISE:
1. Revision goes back through the specialist engine to drafting specialist
2. Specialist revises
3. Returns to the seat that flagged it
4. Loops until that seat passes or the draft fails

Human touchpoint: ZERO during this loop.

### Stage 7: QA and Output

1. the specialist engine (:port) checks visual quality
2. the specialist engine runs final AI telltale scan
3. Format check for target venue
4. the specialist engine (:port) packages for delivery

Multi-format output from one validated research output:
- arXiv LaTeX source
- Conference abstract (word-limited)
- Journal submission
- LinkedIn article
- Technical blog post
- Twitter/X thread
- Presentation slides
- White paper (Crucible)
- Code repository with examples (Crucible)

## Engine Routing Map

### Veritas (GG3, port 8300 block)

| Stage | Primary | Port | Supporting |
|-------|---------|------|------------|
| 0 | the specialist engine | - | the specialist engine |
| 1 | the specialist engine | 8108 | the specialist engine (8126), the specialist engine (8127) |
| 2 | OpenResearcher | - | DS O'Keefe (8147), the specialist engine (8105) |
| 3 | the specialist engine | 8095 | the specialist engine (8010), the specialist engine (8095), the specialist engine |
| 4 | Domain specialist | varies | the specialist engine (8124), the specialist engine (8120), the specialist engine (8121) |
| 5 | the specialist engine | 8238 | the specialist engine, domain experts, the specialist engine, the specialist engine |
| 7 | the specialist engine | 8122 | the specialist engine, the specialist engine, the specialist engine (8092) |

### Crucible (Cyber the operator agent, port 9000/8400 block)

Same stages, ports shifted +1000 (Andreasen 9108, Ito 9126, etc.).

## Engine Health Gating

Before each stage, check ALL required engines alive (GET /health on each
port). If ANY dead: PAUSE, trigger auto-repair, wait for recovery. If
recovery fails: ALERT human (only mid-process human contact). Process
cannot resume until ALL required engines alive.

Enforced by the specialist engine running pre-stage health checks.

## Cross-Organism Collaboration

GG3 inputs technology idea -> federation (:port) -> Cyber the operator agent runs
Crucible -> output returns via federation -> both the principal and the principal see
result.

Federation cleansing strips scripts, event handlers, javascript: URLs.
Data types limited to: research_note, workflow, process_flow.

## Human-AI Iteration Minimization

Human touches process exactly TWICE:
1. Input: submit idea (system may ask 1-3 clarifying questions)
2. Output: review final output

Between touchpoints: AI iterates internally. Adversarial panels,
revisions, citation verification. All without human involvement.

Exception: dead engine that cannot be auto-repaired triggers human alert.

## the principal Learning Loop

3-stage voice evolution:
1. Baseline: voice.yaml (INTJ, technical tone, Creator archetype)
2. Pattern recognition: the specialist engine identifies preferred structures from
   accumulated Crucible outputs
3. Deep learning: LinkedIn content ingested, published work enters corpus,
   system matches the principal's actual published voice

## Gaps Identified (2026-08-02)

1. Federation server :port conflict with the specialist engine (sibling-agent owns fix)
2. Cyber the operator agent engines not verified running on 9000 port block
3. the principal LinkedIn not connected (start with standup transcripts)
4. Docker twin built but engine port probing needs fixing
5. Citation API rate limiting at scale (50+ papers/month)
6. ~~Process state checkpointing for crash recovery~~ **RESOLVED 2026-08-03** — `veritas_process.py` implements per-stage checkpointing to `/tmp/veritas_process_state_<ts>.json` with `--resume` support. See `references/veritas-process-implementation.md`.
