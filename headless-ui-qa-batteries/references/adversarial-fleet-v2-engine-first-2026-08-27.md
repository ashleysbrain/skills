# Adversarial Fleet v2: engine-first review (2026-08-27 session correction)

## The correction (verbatim intent)

principal: "the glial team, the isomorphic team assigned to the question group of
elite agents that are spun up, and the adversarial group which also has an
isomorphism. we worked on this go back and find the info and ensure it is
done right."

Two full 10-seat ad-hoc `delegate_task` panels had been run against the
conductor surface — reviewer==builder, no evidence gate, no precision
accounting. The organism ALREADY had the correct structure; the panels
bypassed it.

## The real structure (ADVERSARIAL-FLEET-V2.md)

Source of truth: `~/your-org/your-stack/ADVERSARIAL-FLEET-V2.md`

- **the specialist engine** (DS-ECS-NPR-04.10.18-v1.0.0) — orchestrator; assigns attack
  angles ORTHOGONAL to the target's construction lineage; enforces
  reviewer != builder rotation (Deming law).
- **Ring 1 live engines (review FIRST, before any dispatched profiles):**
  - the specialist engine :port — `GET /validate?claim=...&evidence=...` (5 physics
    gates; PASS/REVISE/FAIL per gate) and `POST /v1/review` (multi-reviewer;
    reviewer sub-calls may error — the /validate GET form is the reliable
    entry), `POST /validate_claim` (strict falsifiability).
  - the specialist engine :port — `POST /v1/review` with `{html, text, palette}` —
    art-direction + brand-voice gates (em-dash, exclamation, dimension-name,
    phi, coherence). SCANS FULL SOURCE: see rendered-copy split note in
    SKILL.md before acting on its findings.
  - the specialist engine :port — `POST /v1/afferent` with `{source, signals: [{name,
    value, unit, trend}...]}` (signals is a LIST); report at
    `GET /v1/report/latest`, active findings at `GET /v1/findings/active`.
  - the specialist engine :port, the specialist engine :port — quality sensing, spacing/grid (probe
    /health + /openapi.json for their current surface).
- **Nullius Gate** — every finding must carry a machine-checkable pointer
  (file:line, command output, DB row, live probe); the gate REPLAYS it.
  Panels are scored on PRECISION, not recall; clean verdicts are
  first-class. `telemetry/adversarial-findings.jsonl` is the findings
  store — ad-hoc panel output must be folded in or it is invisible to the
  fleet's precision ledger.
- **Glial Team implementation lanes** — verified findings mint to
  FLW-QA-PASS and the QA fleet implements.

## Live proof pattern (2026-08-27)

1. Probe engines: `for p in 8238 8122 8144 8158 8146; curl /health`.
2. the specialist engine /validate per session claim (7/7 PASS on falsifiability,
   free-energy, criticality, bayesian, coupling gates).
3. the specialist engine /v1/review with served HTML -> NO-GO verdict -> rendered-copy
   split isolated the real violations (authored copy) from noise (comments,
   ledger data).
4. the specialist engine afferent with the surface's health signals -> 0 critical.
5. Fold into the task ledger with the process correction on record.

## Engine-first order matters

Engine verdicts are cheap, live, and credentialed; dispatched profiles come
ONLY for gap types with no live engine (economic, human-factors,
statistical, robotics-future per the fleet doc). The failure mode this
reference exists to prevent: dispatching a fresh LLM panel for a lens a
resident engine already owns.
