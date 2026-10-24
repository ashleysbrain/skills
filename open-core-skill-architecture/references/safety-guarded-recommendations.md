# Safety-Guarded Recommendations

This reference shows how to interpret signals and produce accurate recommendations without exposing private algorithms.

## Signal interpretation order
1. Facts in the source material
2. Change versus baseline
3. Confidence / completeness of evidence
4. Safety or escalation flags
5. Recommendation

## Simple public heuristic
Use a reviewable heuristic for the public layer:

`recommendation_score = (signal_strength × confidence) / (friction + 1) - risk_penalty`

Interpretation:
- `signal_strength` = how strong or repeated the signal is
- `confidence` = how complete and reliable the evidence is
- `friction` = how hard the recommended action is to carry out
- `risk_penalty` = how much caution the situation requires

## Output shape
- What the signal says
- What it likely means
- One recommended action
- One support action, if useful
- One escalation condition

## Boundary rule
- Public docs may explain the signal order and the recommendation shape
- Private scoring tables, calibrated weights, and hidden thresholds stay out of the open layer
- If the evidence is thin, say so plainly instead of pretending certainty

## Pitfall
- Do not convert the heuristic into a rigid promise; it is a guide for interpretability, not a replacement for specialist judgment.