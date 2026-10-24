---
name: openresearch
description: Use when ANY research finding, paper, article, web claim, or scan output enters the organism. Enforces the mandatory VERITAS gate (PASS/REVISE/FAIL) before DS O'Keefe consolidation. The canonical chokepoint for scientific-accuracy enforcement — research does not enter the organism's knowledge base without passing VERITAS.
---

# openresearch — Entorhinal Cortex (research-ingest gate)

Body analog: entorhinal cortex — the gateway cortex that gates multimodal
input into the hippocampus (DS O'Keefe, port 8147) for consolidation. This
module is the routing cortex BETWEEN raw research input and consolidation.
Confirmed by hermes R2 (message-bus msg 41): entorhinal is correct vs
parahippocampal (spatial — wrong) and perirhinal (object familiarity — wrong).

This module is source-agnostic. It does not care whether the research came
from a peer-reviewed paper, a web article, a user-supplied claim, a scan
output, or a cron — every external finding enters through the same gate.

## Receptor: OpenResearcher (retrieval layer)

OpenResearcher (GAIR-NLP, Apache-2.0) is vendored at
`vendor/openresearcher/` — an EXTERNAL sensory receptor over the arXiv
corpus (a literature "eye"). It is the retrieval layer this gate
previously lacked: before it, findings had to be supplied by hand; now
the receptor retrieves + synthesizes them automatically, and they still
must pass VERITAS like any other source.

The afferent pathway is `organism/openresearcher_adapter.py`:

    OpenResearcher RAG answer  -->  atomic claims
      --> organism/openresearch_ingest.py  (de-dup + VERITAS + consolidate)
      --> DS O'Keefe (:port)

    # full receptor (Qdrant + Elasticsearch + CUDA embeddings live):
    python3 organism/openresearcher_adapter.py --query "<question>"
    # lite receptor (arXiv-API retrieval + OpenResearcher synthesis; NO Docker/CUDA):
    python3 organism/openresearcher_adapter.py --query "<question>" --lite [--no-critic]
    # bridge-only (ingest any pre-computed finding through the gate):
    python3 organism/openresearcher_adapter.py --answer "<text>" [--citations ...]
    # infra readiness probe:
    python3 organism/openresearcher_adapter.py --preflight-only

The receptor runs under its venv: `vendor/openresearcher/.venv/bin/python`.
Two retrieval backends, same synthesis + same VERITAS gate:
  - **lite** (default on CPU hosts): retrieves real arXiv papers via the
    official arXiv API, synthesizes with OpenResearcher's LLM service layer
    (query_decomposition -> summerize -> self_critic). No Docker/CUDA. Auto-
    activates when the heavy stack is down. arXiv is a CS/physics/math-heavy
    corpus, so non-STEM topics may retrieve little (a corpus property).
  - **heavy**: OpenResearcher's full Qdrant dense+SPLADE + Elasticsearch BM25
    hybrid + bge-reranker. Needs CUDA (a GPU box) — the adiabatic follow-on.

The receptor stack is heavy and Docker/GPU-bound, so it is vendored as a
copy (not a live dependency) and brought online adiabatically. When the
heavy infra is down the adapter auto-falls back to the lite receptor and
exits 0 — it never crashes, and the bridge (`--answer`) stays usable.
LLM credentials are read from `<agent-home>/.env` (LLM/GLM_BASE_URL) — no
key is hardcoded. OpenResearcher findings enter as
`--evidence literature_synthesis`, so unsourced synthesis claims correctly
get VERITAS REVISE (not auto-consolidated).

## Ad-hoc retrieval: OpenAlex API (no-auth, cross-disciplinary)

When the OpenResearcher receptor is unavailable OR the topic is non-STEM
(neuroscience, medicine, social science, interdisciplinary), use the
OpenAlex API directly for paper retrieval. OpenAlex covers 250M+ works
across ALL disciplines, requires no API key, and does not rate-limit like
Semantic Scholar (which 429s after 2-3 rapid calls) or bot-block like
Google Scholar.

```
curl -s --max-time 10 \
  "https://api.openalex.org/works?search=<keywords>&per-page=10" \
  -o /tmp/oalex.json
```

Abstracts are stored as inverted indexes and must be reconstructed to
plain text. Full query patterns, abstract reconstruction code, iterative
narrowing technique, and proven cases are in
`references/openalex-api-reference.md` under the `local-activity-recovery`
skill.

Findings retrieved via OpenAlex should enter the gate as
`--evidence literature_synthesis` (same as OpenResearcher findings), NOT
`--evidence original_data`, because the abstract reconstruction is a
synthesis step, not direct measurement. They must still pass VERITAS.

## Enforcement

The canonical entry point for research ingestion is the CLI wrapper:

    organism/openresearch_ingest.py

Operators (hermes, sibling-agent, sibling-agent, user) MUST route research ingestion
through this wrapper rather than calling veritas_engine.py ad-hoc. The
wrapper is the chokepoint that makes the gate non-bypassable: it runs
de-duplication, the VERITAS gate, verdict routing, and DS O'Keefe
consolidation as one atomic pipeline. Calling veritas_engine.py directly
is NOT research ingestion — it is a raw primitive with no enforcement.

    python3 organism/openresearch_ingest.py \
        --claim "<the claim>" \
        --source "<paper | article | web finding | scan output | user claim>" \
        --evidence <original_data|literature_synthesis|theoretical|mixed> \
        [--no-consolidate] [--quiet]

Because every code path in the organism that ingests research funnels
through this one CLI, an operator cannot quietly consolidate an
unvalidated finding — the wrapper will refuse to encode anything that does
not return VERITAS PASS.

## Workflow (run in order — the wrapper automates steps 1-4)

1. Intake. Accept a research source: any research source (paper, article,
   web finding, scan output, user-supplied claim). Record source,
   timestamp, and the core claim.
2. De-duplicate. Check the claim against existing consolidated knowledge
   in DS O'Keefe (port 8147) via an exact-claim hash tag. If already
   consolidated, stop and report DUPLICATE — do NOT re-run VERITAS (free
   -energy principle: never spend compute re-validating a canonical claim).
3. VERITAS gate (MANDATORY, no exceptions). The wrapper subprocesses
   veritas_engine.py and parses the canonical VERDICT:
   - VERDICT PASS  -> continue to step 4.
   - VERDICT REVISE -> post a revision request to the operator bus
     (--from openresearch --to all --type handoff --subject "REVISE: ...")
     and STOP. Do not consolidate.
   - VERDICT FAIL / SKIP -> reject and STOP. Do not consolidate.
4. Consolidate. Route the PASS'd finding to DS O'Keefe (:port) /encode
     for hippocampal consolidation into long-term knowledge. The wrapper
     tags the trace with a de-dup hash so step 2 catches re-ingestion.
5. Narrate. Route to the specialist engine (:port) for narrative integration when
   the finding feeds writing/production. Optional: the specialist engine (:port) for
   visualization.
6. Handoff. Post an acceptance handoff to the invoking operator via the
   operator bus so the organism knows the finding entered canon.

## Outbound Academic Writing and Conference Submission Pipeline

Research also LEAVES the organism as papers, abstracts, and conference
submissions. These must pass through the same VERITAS gate — but in the
outbound direction. See `references/search-blocked-workaround.md` for the fallback technique
catalog (Startpage curl, Wikipedia REST API, browser direct navigation,
xurl CLI, curl liveness checks for Firecrawl billing-blocks, and the URL
credibility heuristic for recommendations) to use when web_search,
web_extract, Google, Bing, and DuckDuckGo are all blocked. Do NOT narrate
tool failures to the user.

See `references/veritas-academic-writing-pipeline.md`
for the complete outbound pipeline including:
- VERITAS process file locations and 6-stage outbound execution
- Conference abstract pipeline (time-critical workflow)
- Topic generation pattern from organism architecture
- Known conferences, deadlines, and status tracking
- Publication roadmap reconciliation (30-paper tracker)

**Key outbound files:**
- VERITAS Process: `hydra-os/intel/processes/VERITAS-PROCESS.md`
- Organism Roadmap: `agent-organism/docs/ORGANISM-ROADMAP-AND-CONFERENCE-2026.md`
- Publication Roadmap: `hydra-os/intel/academic/PUBLICATION-ROADMAP-30-PAPERS.md`

**Cognitive-science evidence base for pipeline architecture:** Before
proposing structural changes to the draft→review→revise flow, load
`references/cognitive-science-of-expert-writing.md` — the peer-reviewed
evidence (Flower & Hayes, Sommers, Kellogg, Bereiter & Scardamalia, plus
2024–2025 AI-writing studies) showing expert writing is recursive not
single-pass, revision is meaning-first multi-pass, pre-writing synthesis is
the highest-leverage phase, and AI-generated full drafts carry homogenization
and skill-degradation risks. The current single-call-draft pipeline
structurally models the *novice* knowledge-telling pattern; the literature
points toward an interleaved, diagnosis-heavy, synthesis-first architecture.

## SIBLING PROCESS: Crucible (technology pipeline, 2026-08-02)

Veritas has a technology-focused sibling called **Crucible** (Medieval
Latin: vessel of extreme heat testing). Both are research validation
pipelines that share the same 7-stage physics-grounded architecture
but differ in audience, specialist calibration, and adversarial panel
composition.

| Aspect | Veritas | Crucible |
|--------|---------|----------|
| Owner | GG3 (the principal) | Cyber the operator agent (the principal) |
| Audience | Academic, scientific | Technology, entrepreneurs, SBOs |
| Focus | Physiomorphic AI, health science, consciousness | AI engineering, security, mesh/harness, system design |
| Adversarial panel | Popper, Kahneman, Wernicke, 3 domain experts, Machiavelli, Bentham | Popper, Kahneman, Wernicke, security red-team, systems engineer, domain expert, audience proxy, Machiavelli, Bentham |
| Output formats | arXiv, conference abstracts, journal submissions, academic PDFs | arXiv (cs.CR/AI/SE), LinkedIn articles, white papers, blog posts, engineering guides |

Both processes flow through the operator agent engines via the specialist engine routing. Both
share the same citation verification subsystem (no hallucinated
citations, real API calls only). Both enforce engine health gating (no
output if required engines are dead).

Cross-organism collaboration: the principal can input a technology idea into
GG3, which packages and sends via federation (:port) to Cyber the operator agent. Cyber
the operator agent runs it through Crucible and returns the output. The two AIs never
run simultaneously on the same task. The federation is the handshake.
The Crucible CLI implements this directly: `--from-federation` receives,
`--send-federation gg3_veritas` sends back.

**Capitalization rule (user directive 2026-08-02):** Use title case
(Veritas, Crucible) in all documentation and user-facing text. All-caps
(VERITAS) is visually aggressive and has been corrected. Python
constants may remain UPPER_CASE per convention, but docs, skills, and
process names use title case.

See `references/veritas-crucible-dual-pipeline.md` for the complete
7-stage specification of both processes.

## Concrete Implementation (verified 2026-08-03)

Both pipelines are now fully built and verified. `veritas_process.py` (970
lines) and `crucible_process.py` (1,542 lines) in the workspace root are the
working Python implementations of the 7-stage pipelines. Each routes every
stage through real the operator agent engines via HTTP, verifies citations against arXiv +
OpenAlex + Crossref (Crucible also checks GitHub repos), checkpoints state
to disk after each stage, and supports `--resume`. Dependencies: Python
stdlib only (no pip installs).

Crucible additionally supports:
- `--from-federation` / `--send-federation` for GG3 ↔ Cyber the operator agent idea routing
- 5 technology-specific validation rules (code syntax, threat model, impl
  guidance, benchmark methodology, vendor neutrality)
- the principal voice profile loading from `voice.yaml` + standup transcript
  pattern extraction for voice calibration
- arXiv category filtering (cs.CR, cs.AI, cs.SE, cs.DC)
- 9-seat adversarial panel (adds Security/Red Team, Systems Engineering,
  Audience Proxy vs Veritas's 8 seats)

See `references/veritas-process-implementation.md` for the Veritas
implementation reference and `references/crucible-process-implementation.md`
for the Crucible implementation reference (including build verification
results, 10 key differences table, and Docker container port mapping).

```bash
# Full pipeline
python3 veritas_process.py --idea "claim" --evidence-level theoretical --json
# Health check all engines
python3 veritas_process.py --health-check
# Resume after engine recovery
python3 veritas_process.py --resume /tmp/veritas_process_state_<ts>.json
```

## Ownership (scientist names, no codenames)
- the specialist engine (entorhinal) — intake/gate design
- veritas_engine.py (workspace root) — the gate primitive
- organism/openresearch_ingest.py — the enforcement chokepoint (this module)
- DS O'Keefe (:port) — consolidation
- the specialist engine (:port) — narrative
- DS J Eccles — verifier on contradicting claims
- the specialist engine — ECS code for any new canon finding
- the specialist engine (:port) — visualization (optional)

## Hard rules
- NEVER consolidate a finding that has not passed Veritas. No exceptions.
- NEVER bypass de-duplication — re-ingesting a canonical finding is waste.
- NEVER call veritas_engine.py directly for ingestion — route through
  organism/openresearch_ingest.py so the gate cannot be bypassed.
- This is a skill module, not an engine: no port, no heartbeat, no ECS
  code for itself. Invoked on demand by any operator or user.
- **Capitalization (user directive 2026-08-03):** Veritas and Crucible
  are ALWAYS title case in documentation, skills, process names, and
  user-facing text. All-caps (VERITAS) is visually aggressive and has
  been explicitly corrected. Python constants may remain UPPER_CASE per
  convention. This applies to 399 files in the workspace and 112 skill
  files that currently contain "VERITAS" in all-caps — code constants
  stay, docs/skills/user-facing text changes to title case.
- **Domain boundary (learned 2026-08-03):** Building complete organism
  engines (123 engine dirs, ecs.py registry, Dockerfiles, port shifting)
  is OPENCODE's domain (central cortical system / deep code surgery).
  the operator agent owns the process flows, scripts, verification, and operation
  of the pipelines — NOT the infrastructure builds underneath them.
  When the user says "work with sibling-agent" for an organism build, HAND
  OFF via the operator bus. Do not attempt to build 3000+ files of engine
  infrastructure yourself. Post the spec, post the handoff, verify when
  sibling-agent finishes. The user explicitly corrected this: "you do not need
  to build this. You Need to work with open code."
- **Workflow momentum (user directive 2026-08-03):** After receiving
  answers to clarifying questions, IMMEDIATELY move forward into the
  work. Do not pause to ask permission or confirm understanding. The
  user's exact words: "Move forward don't stop to ask me after you've
  received the answers to the questions you ask... ask more questions
  to help your build and immediate move forward when you get your
  answers." This means: ask questions when genuinely needed, then BUILD
  without stopping for sign-off.

## Design Validation Pattern (proven 2026-08-03)

Before writing ANY pipeline code, run a 3-reviewer adversarial gap
analysis on the design spec. This catches structural flaws before they
become code debt.

**Pattern:**
1. Design the full spec (stages, engine routing, panel composition)
2. Dispatch 3 adversarial reviewers: falsifiability (Popper-style),
   operational/engineering (systems architect), human factors (Kahneman)
3. Each reviewer finds gaps with severity ratings (CRITICAL/HIGH/MEDIUM)
4. Write remediation plan BEFORE coding
5. Then build with the fixes baked in

**Proven result:** 37 gaps found before code was written, 7 CRITICAL.
The resulting code (veritas_process.py, crucible_process.py) had crash
recovery, rate limiting, and federation resilience designed in from the
start rather than bolted on after failures.

## Docker Testing Pattern (proven 2026-08-03)

**Key discovery:** Both the operator agent organisms may already be running in Docker
containers via colima, even if Docker.app is not installed. Always check
colima status before assuming Docker is unavailable.

```bash
# Check colima (lightweight Docker daemon for macOS)
colima status 2>/dev/null  # may say "already running"
docker info 2>/dev/null     # if colima is up, this works
docker ps                   # shows running containers
```

**Engine port accessibility:** Docker containers map only specific ports
to the host. Engine ports (9xxx for Cyber the operator agent) may be INTERNAL to the
container only. To test pipelines that route through engines:

1. Run the pipeline script INSIDE the container: `docker cp script.py
   container:/app/ && docker exec container python3 /app/script.py`
2. OR map additional ports in docker-compose.yml
3. The health-check mode (`--health-check`) correctly probes from inside
   the container where all ports are accessible.

**Federation testing:** Both containers respond to GET `/api/federation/
status` (proxied to the federation server). But POST endpoints for
cross-organism handoff require the federation SERVER to be running and
may need implementation. GET 200 does NOT mean POST works.
