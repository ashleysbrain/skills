# Public TWC Rubric Note

This note captures the coaching-engine variant of TWC scoring.

## What changed

For coaching/advisory panels, TWC is not computed from private or sensitive data. It is a *public-information-only proxy*.

## Required fields

- `public_twc_dimension_scores` — eight public proxy dimensions
- `public_twc_score` — public composite score
- `public_twc_score_basis` — short note on public evidence used
- `public_twc_score_confidence` — confidence in the public evidence

## Scoring guardrails

- Use only public, observable, or openly stated information.
- Do not infer private, medical, financial, or sensitive facts.
- Keep a separate internal/private score only if the project explicitly maintains one.
- Treat low evidence as low confidence, not invented certainty.

## Coaching-engine interpretation

When docs or responses say "score" in the coaching-engine context, prefer:
- public TWC score
- coaching score
- health state

Avoid implying that the public score is the same as a private/internal assessment.