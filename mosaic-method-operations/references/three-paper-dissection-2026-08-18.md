# Three-Paper Dissection — ScienceFlow + Replica + AutoResearchEval
(Session 2026-08-18, relayed by the principal. Full texts fetched via curl fallback;
facts below verified from PDF text extraction, not abstracts. Veritas verdicts:
all three ASK — held for principal on claim consolidation; engineering adoption
proceeded on independently verifiable mechanics. Canonical dissection doc:
`~/Desktop/INTELLIGENT-OS/your-stack/RESEARCH-DISSECTION-3PAPERS.md`.)

## Paper mechanics (what each actually is)

### ScienceFlow (arXiv 2608.14354) — EXECUTION CONTROL layer
- Long-horizon autoresearch agent; SOTA 70.22% Any-Medal, full MLE-bench, 24h budget.
- Recoverable executable states: workspace checkpoints every segment boundary.
- ESTRA re-anchoring: at each boundary choose CONTINUE live trajectory vs
  REDIRECT from archived checkpoint (dead-end recovery, not forward-only).
- Evidence-aware execution controller SEPARATE from route selection:
  admission verdicts RUN_NOW / OBSERVE_THEN_RUN / PENDING / REPLAN judged
  against live resources Rt, remaining budget Bt, validated progress.
- Online review + replan at observation boundaries (liveness, log growth,
  metric history, artifacts, checkpoints, remaining budget).
- ADOPTED in-package: gates/scienceflow_admission.py (verdict rides every
  dispatch record, persisted in dispatch.db) + gates/estra_reanchor.py
  (volley tick checkpoint/decide). Flows 11-12, T-260818-0073 closed.

### Replica / Faraday (arXiv 2608.13331) — REWARD + TRAINING layer
- 242 replication tasks from 100 papers (figures redacted → reproduce).
- Auto-generated per-task RUBRIC judges: low noise, validated against expert
  human rankings → usable as reward signal without human-in-loop.
- Faraday = Qwen3.6-27B post-trained with turn-level GRPO credit.
- Coding-agents-as-tools (CAT): small orchestrator model + Codex/Claude as
  executor tools. Beats Claude Opus 4.8 on 73% in-dist, GPT-5.5 60% held-out.
- Thesis: orchestration + rubric reward + turn credit > raw model size.

### AutoResearchEval (arXiv 2608.13417) — EVALUATION layer
- 36 long-horizon tasks, 7 frontier models. "Beyond final scores."
- Rule-based WITHIN-RUN metrics (deterministic from verifier outcomes +
  trajectory signals, NO LLM judgment): C1 Solution Framing, C2 Execution,
  C3 Feedback Control.
- M-metrics: controlled with-vs-without experience comparisons; reuse spans
  -0.013 to +0.145 — CAN MISLEAD. Must measure, not assume.
- Findings: agents = engineering optimizers (novelty rare); run-to-run
  variance high; HARNESS DESIGN measurably affects stability (direct external
  validation of the Mosaic methodology thesis).

## The one-system digest
Execution control (ScienceFlow) + reward/training (Replica) + evaluation
(ARE) = the three layers of a self-improving agent OS. We had parts of the
first; the other two were absent.

## G1-G9 gap table (grep-verified against the live package, 2026-08-18)
| # | Paper | Gap | Ledger task |
|---|-------|-----|-------------|
| G1 | Replica | no rubric judges anywhere | T-260818-0078 |
| G2 | ARE | volley logs completion, not capability (C1/C2/C3) | T-260818-0079 |
| G3 | ARE | experience reuse unmeasured | T-260818-0080 |
| G4 | ARE | no harness A/B comparison mode | T-260818-0081 |
| G5 | Replica | dispatch decides, never executes (CAT lane) | T-260818-0082 |
| G6 | Replica | no turn-level credit assignment | T-260818-0083 |
| G7 | Replica | no training lane (the specialist engine) | T-260818-0084 |
| G8 | Replica | no self-eval task generation (redaction method) | T-260818-0085 |
| G9 | ARE | no agent run-to-run variance telemetry | T-260818-0086 |

## Build order (dependency-first, physics-gated)
- Phase 1 (measurement): G1 rubric judge → G2 within-run metrics → G9 stability
- Phase 2 (leverage): G5 CAT execution → G4 harness A/B → G3 experience reuse
- Phase 3 (elite goal): G8 task space → G6 turn credit → G7 the specialist engine training
  = closed loop: registry → probe → rubric-eval → train → fleet slot, zero
  external benchmark dependence.

## Session pitfalls encoded nearby
- Fresh-clone CI check: schema changes must land in CREATE TABLE + migration
  path, never only ALTER on the local DB (CI run 32140653231 died to this).
- Absence of telemetry signal is NOT healthy signal — stale-evidence flag
  before trusting trend decisions (ESTRA fix, ARE lesson applied).
- Backfill provenance: honest ts + "backfilled" label, never fabricated history.
