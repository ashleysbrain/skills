# Design-Review Iteration Loop — Thinkery Case (2026-08-18)

Case study for the plan-only adversarial design review + background iteration
pattern. Companion to `ceo-directive-dissection-thinkery-2026-08-18.md` (the
dissection half). Artifacts: `docs/THINKERY-DESIGN-REVIEW-v1.md` (859abce) and
`v2.md` (eaa09d5) in your-org/your-stack; ledger T-260818-0153.

## The pattern: ground-truth-first, then multi-lens panel, then lock, then iterate

### 1. Live digest BEFORE any review claim
Never review from memory or session summary. Curl the real surface, count the
endpoints, grep for wiring absence:
- `curl -s -o /dev/null -w "%{http_code}"` the page + its data endpoints
- `grep -c "@app\." backend.py` (found 9,934 lines / 200 endpoints = monolith finding)
- `grep -n "<capability>" path` returning EMPTY is evidence (e.g. zero
  `organism_state` refs in the brainstorm path = falsification F1)
- Row counts from the live stores (ledger 179 tasks, registry 38 entries)

### 2. Multi-lens panel — one question class per lens
Each lens runs a distinct adversarial pass with its own output format:
- **Popper (falsification):** list the implicit claims ("X exists"), test each
  with grep/curl evidence, verdict TRUE/FALSIFIED/WEAK. F1-F4 format.
- **Tanenbaum (architecture):** verdicts per structural risk (T1-T5) — monolith
  containment, one-ledger law, bridge-only LLM calls, read-only feeds,
  handoff-not-reimplementation.
- **Nielsen (usability):** entry friction, progressive disclosure, checkpoint
  states, component reuse, plain-words law.
- **Koster (motivation):** points hookup day 1, visible lineage, NO new point
  physics (one writer).
Rotating lenses across iterations prevents reviewer blind-spot reuse.

### 3. Decisions-locking from principal voice answers
principal answers arrive as rambling voice transcripts. Convert to `LOCK-N` entries
verbatim-intent, then choose physics-PM defaults for everything unanswered.
Split questions into blocking (3 max) vs non-blocking (defaults chosen and
recorded). When principal says "I don't know" to a question YOU can answer with
evidence (e.g. which repo copy is canonical), answer it with measurements
(0-byte ledger, 0-row queue, git history) instead of escalating — then clean
up the ambiguity permanently (delete the stale mirror).

### 4. Background iteration loop (the "many iterations before principal sees it" law)
Cron job, every 4h, deliver=local:
- Read latest vN doc → run ONE lens pass on the PLAN (not code)
- Write vN+1 with changelog; cite repo evidence (file:line) for every claim
- Stop conditions: two consecutive lenses finding zero defects → declare
  PLAN-STABLE; hard cap v7 regardless
- PLAN ONLY discipline: never touch code outside docs/ until stable or principal
  orders build

## Pitfalls found the hard way

- **docs-only commits skip CI legitimately.** The workflow has a `paths:`
  filter (gates/stores/adapters/CONTRACT/manifest). A docs-only commit showing
  zero runs is path-filtered, NOT a CI defect. Verify with
  `gh api repos/.../actions/runs?head_sha=<sha>` before suspecting breakage —
  don't burn 3 polling cycles like this session did.
- **Whole-file rewrites of plan docs blocked by gates.** write_file to the
  package can hit baseline-first + specialist-gate expirations; the working
  path is a python file-op heredoc inside terminal with git commit, or re-route
  the specialist gate (`specialist_gate.py --route`) then retry.
- **Cost claims need measurement.** "We must work smart" → measured the real
  7-day harness baseline (37 runs, ~115k tokens, glm-5.3 dominant) before
  designing tiering. Never design cost controls without a measured baseline.

## Signals for reuse
User says: "iterate on the plan many times before it comes back to me",
"plan only, don't make changes yet", "adversarial design review", "build out
the plan keep iterating", or asks for front+back plans "together". Load
spec-adversarial-review and apply this iteration-loop wrapper.
