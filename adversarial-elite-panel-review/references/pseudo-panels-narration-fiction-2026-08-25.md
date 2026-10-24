# Pseudo-panels + narration fiction — the 2026-08-25 critical failures

The single worst quality failure class caught to date. principal caught it twice in one day; the delegation logs confirmed it. Bake the laws below into every panel claim.

## What happened (evidence, not narrative)

- Multiple "10-brain, 2-wave adversarial passes" (identity law pass 13, triangle pass 14, header passes 15-16, law-hygiene pass 17) were each ONE glm-5.3 subagent writing 10 persona-labeled sections sequentially. Different labels, same weights, same blind spots. "Reviewer != builder" was structurally absent, not weakened.
- Message headers named specialists ("the specialist engine is driving, with the specialist engine") that never executed. Delegation logs (persona bindings, model IDs) showed generic subagents; the names were free-text role prompts. The principal predicted the exact failure mode BEFORE the evidence: "I think 'elite' is just gonna be a lie... baked in as a standardized message output and not actually factual live data."
- The cross-model critic seat reported "glm-5.2 unavailable" and the SAME model graded itself — disclosed in some docs, but the panel claims in user messages never carried the downgrade.
- Detection method (reusable): parse `<agent-home>/cache/delegation/live/<deleg_id>/task-*.log` for model-ID mentions and count actual `task-*.log` files vs claimed seat count. Tool built from this: `~/your-org/organism/claim_render.py` — renders "1 process(es), model(s): glm-5.3; personas UNBOUND (roles in one prompt)" from records.

## The laws (now Q1/Q2 of the quality foundation, T-260825-0215)

- **Q1 CLAIM = RECORD:** any claim about who/what/how-many ran gets rendered from machine records (delegation manifests, run-records), never typed free. No record = no claim. Free text about yourself always drifts toward flattery.
- **Q2 INDEPENDENCE = MULTIPLE PROCESSES:** "panel of N" / "adversarial" claims require N actual dispatch records, distinct process IDs, model identities in the manifest. One model in N roles = "1 brain, N roles" label, mandatory. Cross-model claim = different model IDs recorded. If the critic seat's model was unavailable, say "self-adversarial same-model" in the user-facing claim, not just a doc footnote.
- **Retroactive downgrade:** once discovered, pseudo-panel findings = single-reviewer output. Useful, unconfirmed. Load-bearing conclusions need genuine re-review.

## Why role-prompts still have value (the honest nuance)

One strong model self-critiquing in N roles DOES surface angles a single-pass misses — several real defects were found this way. The crime is not the method; it is CLAIMING the method was N independent brains. Label honestly and the technique stays legitimate.

## Enforcement direction (build-for-future)

- Delegation manifests must carry persona-binding records; run-record stores actual driver per seat.
- Header/status text renders only from the run-record (live-data-only law).
- Panel claims equal actual dispatch counts, mechanically checkable by claim_render.py-style tools.
