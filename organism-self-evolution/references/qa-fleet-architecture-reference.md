# QA Fleet Architecture — four-angle immune system (v1.0.0 design + mint record)

Class reference for the QA fleet, per `your-stack/QA-FLEET-ARCHITECTURE.md`
(the canonical doc) and the 2026-08-20 mint session. Kept here so future
sessions don't need to re-derive the fleet from chat history.

## The design law

A single QA angle is a monoculture. All five historical QA failures share one
shape: **the QA organ shared a blind spot with the thing it was checking**
(livelocked loop measured heartbeats not repairs; variance sensor read
variance=0 as healthy; judge's evidence file had no producer; CI ran in a
cloud that never fed local evidence; executor never loaded so nobody
noticed). QA angle diversity must be STRUCTURAL: each angle has its own
evidence source, threshold physics, and declared failure mode.

## The four angles

| Angle | Question | Seat(s) | Evidence | Declared failure mode |
|---|---|---|---|---|
| 1 Technical | is the machine healthy? | Eccles, Deming, Tanenbaum, Lamport, Wenckebach, Hall, Codd, Farr | selftests, CI battery, telemetry, pin diffs, defect-escape rates | measures outputs, not whether the machine serves anyone |
| 2 Scientific | is the reasoning healthy? | Popper (veto), Bernard, van Leeuwenhoek | literature deltas, claim-evidence grading, reproducibility, threshold provenance | internally valid, externally useless |
| 3 Clinical | is the product's health function safe/effective? | **the specialist engine** (minted 08-20) | intervention deltas (pre/post 8D), adverse-signal logs, evidence-grade compliance, BLOCKED_BRAND_CLASSES | over-caution: clearing nothing, shipping nothing |
| 4 Human-experiential | is this healthy FOR the human/company? | **the specialist engine** (minted 08-20); Sloan when B2B exists | interaction telemetry (latency, rework, abandonment), correction-sentiment trend, agency metrics, 8D middle-out delta | user-soothing: comfort over truth (counterweighted by Popper) |

Deming owns synthesis/QA-of-QA (profound knowledge = the four angles); the
fleet-conductor program-manager seat is the specialist engine, project manager the specialist engine.

## Adaptability mechanisms (the immune physics)

1. **Context vector** (DESIGN): organism vital signs per QA cycle from
   measured signals only — bio (load, circadian phase, mint/close rates),
   psycho (volatility, correction sentiment, SKIP/abstention rates), social
   (bus connectivity, cross-harness latency, angle coverage).
2. **Threshold modulation** (Scheffer law): `threshold = base * f(context)`.
   Stressed organism -> MORE sensitive technical QA, GENTLER experiential QA
   (a 2 AM wall of sev-1 alarms is itself a health hazard). Stagnant
   organism -> looser GO thresholds, more adversarial science QA.
3. **Clonal selection**: angles whose findings repeatedly survive appraisal
   scan more often; null angles decay (free-energy law applied to QA itself).
4. **Adaptive memory**: verified defects become pattern-library entries;
   re-exposure = deterministic scan (first exposure expensive, second cheap).

## Process flows

All rides EXISTING flows: FLW-QA-PASS (extended: angle rotation — consecutive
passes must not repeat the same angle pair), FLW-QUEUE (findings -> gap/defect
tasks, context-modulated T), FLW-RESEARCH (QA/health/org-science literature
feeds threshold recalibration), FLW-TELEMETRY (context vector rolls up from
existing events). FLW-QA-FLEET is a composition flow binding it together,
not a new execution lane.

## Mint record (2026-08-20 evening)

- FLW-QA-FLEET registered in `stores/flow-registry.json` (v1.2.0);
  `immune` lane added to `stores/task-taxonomy.json` (v1.1.0).
- ORGANS.json 22 -> 26: Deming, Gantt, Nightingale, Rogers seats added
  (body_system=immune, each with GENOME block incl. 8d= field).
- Idempotent minter: `your-stack/scripts/mint_qa_fleet.py`.
- principal rulings driving this: seat minting AUTONOMOUS ("build it if needed"),
  N>=3 variance law, QA runs 24/7 as ecosystem with program+project managers.
- BUILT vs DESIGN (honest ledger at mint time): angles 1-2 live; Nightingale
  + Rogers seats minted but their maiden scans pending; context vector +
  threshold modulation + clonal scheduling still DESIGN.

## Frontier comparison seeds (arXiv 2026)

From QA-PASS-31 market scan + `audit/FRONTIER-MEMO-2026-08-20.md` (5 papers
post-08-18, 14 arXiv IDs total, all >= 2025): variance-fragility of
self-improvement (GAP-A), skills library drift (GAP-B), anabolic knowledge
loop (GAP-C), verifier-grounded harness optimization (GAP-D). Standing
queries live in `stores/qa-frontier-queries.json` (lane=qa-frontier, 8
queries wired into research_scan_tick via scan_topics — no new crons).
