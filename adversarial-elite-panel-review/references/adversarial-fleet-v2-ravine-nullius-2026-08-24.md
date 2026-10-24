# Adversarial Fleet v2 — polymorphic cell + Nullius replay gate (2026-08-24)

principal ruling (verbatim intent): adversarial agents must be elite and FEW (like
the engines); they evolve/adapt to be ANY kind of world-class adversarial
brain; reviews must eventually run on different models/harnesses, so the
group needs an engine leader + orchestrator; the fleet MUST NOT hallucinate
gaps/edits/revisions just because a review was requested — thorough yet
ACCURATE; reasonable feedback flows to the QA fleet for implementation.
Think future processes, not current.

## Fleet shape: 3 organs total (design doc: ADVERSARIAL-FLEET-V2.md)

1. **the specialist engine** (DS-ECS-IMM-13.12.01, orchestrator) — blind-spot law
   (Ravine, Cognition and the Visual Blind Spot, 2002): a reviewer cannot
   self-select the angle they are blind to. Ravine classifies the review
   target, then instantiates the Cell with 2-3 attack angles maximally
   ORTHOGONAL to the target's construction lineage (reviewer != builder,
   the Deming rotation law made mechanical).
2. **The Adversarial Cell** (ONE polymorphic seat) — becomes any
   world-class brain by loading a methodology PROFILE FILE: lamport
   (temporal invariants/atomicity), popper (falsification), deming
   (variation/tampering/systemic-law), tanenbaum (supervision/cold-boot),
   bridgman (operationalism: every metric traced to its measurement),
   saltzer (8-principle security). New capability = one data file, zero
   new seats.
3. **the specialist engine** (DS-ECS-IMM-13.13.01, evidence gate) — nullius in verba:
   every finding carries a machine-replayable evidence pointer and the
   gate replays it BEFORE minting. Types: file_exists, grep, read-only
   cmd (regex-guarded against rm/mv/kill/launchctl/osascript/curl/>),
   sqlite ro query, manifest key. Implementation:
   `~/your-org/organism/nullius_gate.py`. Live test 2026-08-24:
   {filed:3, verified:2, hallucinated:1} — planted phantom-file finding
   caught, real grep + sqlite findings passed.

## The incentive law (kills manufactured findings)

- Reviewer metric = PRECISION (verified/filed), never volume.
- "No defects found" is a FIRST-CLASS verdict — no forced-findings pressure.
- Failed replay = logged hallucination against the profile; precision
  < 0.7 loses dispatch priority (clonal selection on criticism itself);
  3 strikes triggers profile retraining (methodology revision, N>=3 law).
- Both gauge failures alarm: rubber-stamp (qa_meta M4 nullity scan) and
  rubber-hallucinate (precision ledger flat-at-1.0 with zero clean
  verdicts is ALSO suspicious — flag for spot audit).

## Cross-model evolution (the future wiring)

Profiles are model-agnostic BY DESIGN. Today everything runs glm-5.3 elite.
When multi-substrate routing matures, the SAME profile dispatches to a
different substrate (sibling-agent panel, sibling-agent seat, OpenRouter critic —
see cross-model-critic-seat-2026-08-21.md for the proven one-call
OpenRouter mechanism). Ravine keeps a substrate-rotation ledger: the same
surface must never be reviewed twice by the same model+profile combo.
Diversity from substrate rotation, not seat proliferation.

## Feedback routing (one pipeline, no parallel QA)

Verified findings -> FLW-ADV route stage -> existing QA fleet lanes:
Nedergaard (cleanup/debris), Ford (flows), Saltzer (security), Thompson
(isomorphism). Review -> verify -> implement -> confirm. The adversarial
output ENTERS the implementation machine; it never builds its own.

## Panel execution discipline (proven same day, two disjoint 3-brain panels)

- Second pass MUST rotate brains: Popper/Tanenbaum/Luria then
  Lamport/Deming/Bridgman caught entirely disjoint defect sets. Panel 2
  found: daemon worst-case pass time (2820s) exceeding the 900s interval,
  state.json torn-write risk, and a lint lane never wired into the daemon
  — all invisible to panel 1.
- All checks deterministic Python; PASS/FAIL lines pasted with command
  output into `your-stack/audit/QA-PASS-*.md`; battery re-runnable.
- Fix real defects IN-SESSION; the panel report is a diff, not a wish list.
- "Failure" that resolves to correct behavior (lint minting findings
  because the registry legitimately GREW between runs) -> trace to root:
  zero-true-duplicate check, then rerun-to-zero, then annotate.
- Honest gaps stay open and OWNED: e.g. Nedergaard's clearance-rate K is
  claimed in its methodology but measured nowhere (Bridgman catch) —
  queued to the seat's lane, not papered over.
