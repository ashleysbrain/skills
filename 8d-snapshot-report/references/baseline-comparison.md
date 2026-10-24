# Baseline Comparison Layer

This reference sharpens how snapshot reports compare the current state to a baseline.

## Baseline choice
Use the most truthful baseline available:
1. User-stated baseline
2. Most recent comparable note or check-in
3. Rolling summary of prior entries
4. No baseline if nothing comparable exists

## Baseline strength
Label the baseline quality explicitly:
- Strong: same metric, similar conditions, recent, repeatable
- Moderate: mostly comparable but not identical
- Weak: sparse, old, or mismatched conditions
- None: no comparable prior point

## Comparison order
When comparing current state to baseline, report in this order:
1. Current snapshot
2. Baseline used
3. Direction of change
4. Stability or drift
5. Magnitude, only if supported
6. Confidence
7. Safe next step

## Comparison rules
- Compare like with like only
- Do not claim a trend from one point
- Do not invent magnitude or percentages
- Separate change from confidence
- Keep the comparison narrow and honest
- If the baseline is weak, say that instead of smoothing it over

## Change labels
Use plain labels:
- better
- worse
- same
- unclear
- mixed

If different dimensions move in different directions, say so.
Do not force one grand narrative.

## Trend rules
Trend language is allowed only when there are at least 3 comparable points or a clearly repeated pattern.
Even then, keep the claim modest:
- improving
- declining
- stable
- fluctuating

Avoid stronger language unless the evidence is very clear.

## Confidence rules
Confidence should reflect both data quality and baseline quality.
Typical guidance:
- High: repeated, comparable, recent evidence
- Medium: partial but useful comparison
- Low: thin, mixed, or weak baseline

Low confidence is acceptable and often the most honest answer.

## Anti-overclaim checklist
Before shipping a snapshot report, ask:
- Did I name the baseline?
- Did I label its quality?
- Did I avoid trend claims from a single point?
- Did I keep the comparison honest if conditions changed?
- Did I avoid invented numbers?
- Did I give one safe next step?

## Output note
This layer is for public-facing reviewability.
It should improve transparency, not expose hidden scoring or private calibration logic.
