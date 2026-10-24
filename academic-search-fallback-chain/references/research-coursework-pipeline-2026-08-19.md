# Research-to-Coursework Pipeline — session build record + binding steering

Session 2026-08-19, Workstream 2 (picked up from Telegram). Canonical doc:
`/<workspace>`.
Tools (all in `/<workspace>`, each with a
live-verified `--selftest`):

| Tool | Role | Selftest proof |
|---|---|---|
| `live_market_signals.py` | 5 free-tier market/news connectors, honest live/blocked/error envelope | HN+RePEc live, S2 throttled-live, GDELT unproven, PatentsView blocked-no-key |
| `synergy_composer.py` | deterministic cross-field scoring (novelty/evidence/market/impact/feasibility, principal-tunable weights) | 36 combos, determinism PASS, weight-sensitivity PASS |
| `brainstorm_seeder.py` | composer -> brainstorm seeds; `--decide BS_ID` = star = the ONLY topic->course path | seed->decide->draft chain PASS |

## principal steering (binding, 2026-08-19)

1. **Algorithm output feeds a DECISION LAYER, never auto-production.**
   The composer seeds brainstorm candidates; a human/star decision is the
   single door from "ranked combination" to "course we build". Auto-minting
   drafts from algorithm output was wrong and was reverted the same day.
2. **Evidence tiering is absolute:** course CONTENT may cite only
   peer-reviewed literature (OpenAlex `type:article`). News/community
   signals (HN, GDELT) may move the market/attention SCORE only — they are
   demand indicators, never content, never citations. "Absolutely
   scientifically accurate and proven" = peer-reviewed or it does not
   appear in the course.

## Why the tiering is enforced in code, not convention

- Composer pools query OpenAlex with `type:article` baked into the URL —
  downstream stages cannot accidentally pull preprints.
- Each seeded brainstorm row carries `content_tier` and `demand_tier` fields
  in `notes` JSON, so the constraint travels with the data.
- The seeder's `decide()` function is the only INSERT path into coursework
  drafts; there is no batch/auto mint function anymore.

## Cross-field scoring mechanics (deterministic, no LLM)

- Novelty = concept-Jaccard distance between the two papers x exponential
  recency decay (tau=3y).
- Evidence = log10(1+citations)/4 proxy; the true VERITAS A/B/C grade is a
  LABELED SLOT (neutral 0.5) — never assert a grade without the panel run.
- Impact = labeled panel slot (rubric 1-5, 2+ independent reads) — same rule.
- Weights are principal-tunable JSON (`--weights path`); selftest proves a slider
  change reranks the top pick (weight-sensitivity check).
