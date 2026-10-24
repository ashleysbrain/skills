# Calculation Spec Template for Evidence-Driven Scoring

Use this as a checklist when writing or reviewing a product spec for a scoring engine.

## Required sections

- **Objective**: what the calculation controls
- **Inputs**: exact variables, sources, and ranges
- **Formulas**: explicit math or pseudocode for each derived metric
- **Thresholds**: what causes state changes
- **Clamps and bounds**: min/max behavior
- **Defaults**: initial constants and priors
- **Update cadence**: when the calculation runs
- **Failure handling**: sparse data, contradictions, stale inputs
- **Acceptance criteria**: how to verify the calculation works

## Minimum formula set

For a daily evidence-led scoring system, include:

- `coverage_score`
- `recency_weight`
- `corroboration_index`
- `source_reliability`
- `field_delta`
- `confidence_update`

## Example structure

```text
Coverage = covered_dimensions / target_dimensions
Recency = exp(-age / half_life)
Corroboration = agreeing_sources / required_sources
Confidence = sigmoid(a*coverage + b*corroboration + c*recency + d*reliability - e*contradiction)
Field delta = evidence_strength * source_reliability * recency * direction
```

## Review test

If the spec can be read without answering "how exactly is this computed?", it is not ready yet.
