# New-Input Two-Brain Evaluation — LittleLearner Case (2026-08-16)

Full worked example of the two-brain pattern now embedded in SKILL.md. Use as the template for any "can we use this new model/tool?" question that arrives mid-plan.

## The trigger
principal screenshot of a LinkedIn post (Jana Zeller, Max Planck ETH): LittleCurriculum (88B-token Grade-5-filtered dataset) + LittleLearner (5B model trained on it, sharp-ish knowledge boundary at 12-year-old level), everything open. Question: "can we use it? what for? how?"

## Extraction prerequisite
The image had to be OCR'd (vision lane rejected the attachment format). Pipeline that worked: PIL upscale 3x + autocontrast → tesseract psm 4 on the raw grayscale (NOT binarized, NOT inverted — 85% white background meant light-mode; psm 11 sparse also worked; psm 3/6 and inverted preprocessing returned zero bytes). Pixel-histogram check first (mean 232, 85% white) told us light-mode before wasting preprocessing passes.

## Brain 1 — Karpathy-mode (technical legs), gated PASS
- Read the consuming engine's SOURCE first (canonical_coupling_ai.py): it takes telemetry dicts (hallucination rates, learning slopes), not weights. This fact drove everything downstream.
- Verdict on the model: boundary is a fuzzy prior, not a wall (Grade-5 readability leaks adult facts); headline finding is scaling-laws-expected, credible not surprising; 5B adequate for their question. The valuable artifact is the controlled unfiltered BASELINE (a real ablation pair).
- Ranked uses: (a) instrument, two-system case study not ablation, publishable only if the composite detects the boundary BLIND; (b) evidence amplifier — NO for the preprint itself (external dependency weakens a reproducibility claim), footnote as controlled-substrate validation post-preprint; (c) demo — skip, reads derivative.
- The one experiment spec: 200 in-boundary / 200 out-of-boundary verifiable facts (Grades 7-9), deterministic exact-match grader, fixed seed; per system x regime: factual_verification_score → COG, confabulation-vs-abstention → COG/KNOW, k-shot slope → ADAPT; feed composite() BLIND (score first, overlay known boundary second). ~400 items on 5B is GPU-cheap, 2-3 days.
- His NO conditions: checkpoints not runnable in <1 day; preprint not drafted; anyone wants to fine-tune (a month, not two weeks); grader not deterministic.
- His risk line: borrowed novelty — our metric riding their model's buzz.

## Brain 2 — Popper-mode (she, falsification), gated PASS
- Premise kill: "can we use it?" is a capability question; the binding constraint is attention. Right question: "what does this displace, and does it out-earn it?" By inspection: no.
- Construct validity: fleet-health instrument on a single frozen checkpoint = "an ECG on a rock: the instrument records; it measures nothing."
- N=2 statistical emptiness; first reviewer asks "why not 20 checkpoints, 5 models?" and honesty costs weeks.
- Frame capture: measuring their boundary with our machinery makes our physics a dependent variable of their filtering methodology. "Identity surrender dressed as evidence."
- Timing: zero spare principal-hour in W1-W8; must break a milestone to fit.
- Legibility: another model + another frame = muddier to funders; harms the 3-inbound kill-shot.
- Her verdict: park. Re-entry condition: qualified inbound demand-pull, nothing less.

## Consolidation (the disjunctive ruling)
1. Park now (Popper wins timing while pre-money).
2. Bank Karpathy's experiment spec verbatim (zero design cost at re-entry).
3. Re-entry = demand-pull OR post-W8 slot (disjunctive, so either unlocks).
4. One free touch: a single related-work citation in the preprint (their calibration-and-abstention direction is our lane).
5. Log 3-line note + persist ruling.

## Why this pattern generalizes
New-model questions arrive daily in AI research; the answer is almost never binary use/don't-use. The pattern produces a three-part asset: a ruling (park/adopt), a banked spec (cheap re-entry), and a re-entry condition (no re-litigation). The brains must be opposite-posture: an enthusiast spec plus an adversary falsify, then a human-grade consolidation.
