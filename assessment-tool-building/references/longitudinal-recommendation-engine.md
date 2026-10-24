# Longitudinal Tracking + Recommendation Engine

When a one-shot test result is not enough — the organism needs to track
personality/health measurements over time, detect drift, and generate
ongoing adaptive recommendations.

## When to Build This Layer

- The tool measures something stable but slowly changing (personality, health status, team dynamics)
- The organism needs to adapt its behavior based on the measurement over weeks/months
- One-shot results would become stale
- The user explicitly asks for "long-running" or "ongoing" recommendations

## Architecture

```
*_longitudinal.py
├── save_measurement(subject, results)    # append to timeline (adiabatic: never overwrite)
├── load_timeline(subject)                # load all past measurements
├── detect_drift(timeline, window=3)      # critical slowing detection
├── generate_recommendations(results, timeline)  # ongoing directives
└── explain_calculation(results)          # full item->facet->domain transparency
```

Storage: JSON files in `longitudinal_store/{subject}_timeline.json`.

## Drift Detection (Physics: Critical Slowing Down)

Compare the latest measurement to the mean of the previous N measurements.
A facet is "drifting" if:
- `|latest_score - previous_mean| >= 0.5` (the score shifted significantly)
- AND the shift is consistent (not a one-measurement spike)

A facet shows "critical slowing" if:
- Variance across repeated measurements > 0.5 (measurements are becoming scattered)

Critical slowing means the person is near a tipping point — the organism
should treat their current traits as provisional and watch for emerging
patterns.

## Recommendation Engine

Each recommendation has these mandatory fields:

```python
{
    "id": "O-H1",                    # stable ID for tracking
    "title": "Feed intellectual curiosity",  # human-readable
    "directive": "Surface research...",      # what the organism should DO
    "metric": "engagement_with_novel_content",  # trackable metric name
    "frequency": "weekly",           # how often to apply
    "duration": "ongoing",           # NOT one-shot. "ongoing" or "until_stabilized"
    "trigger": "O high (4.79/5)",    # why this activated
}
```

### Recommendation Levels

1. **Domain-level**: triggered by high/low domain scores (>=3.5 or <=2.5)
2. **Facet-level overrides**: specific facets that deviate from their domain
   (e.g., high Assertiveness within mid-range Extraversion)
3. **Drift-informed**: generated when longitudinal drift is detected,
   telling the organism to recalibrate

### Stability Assessment

Combine within-test variance + cross-test drift into a 0-100 score.

IMPORTANT (learned 2026-08-06): The initial weights below were too
aggressive. A realistic varied profile with 8 ambiguous facets, 0 unstable,
adiabatic OK was scoring 0/100 because 8*3=24 + other penalties exceeded 100.
The penalty multipliers and the lack of a cap on ambiguous-facet penalties
made the score meaningless. Use the CORRECTED weights:

```
stability = 100
         - (unstable_facets_in_test * 5)        # was *10, too harsh
         - min(ambiguous_facets * 2, 30)        # was *3 uncapped; cap at 30
         - (15 if non-adiabatic)                # was -20
         - (drift_count * 3)                    # was *5
```

With these weights: a realistic profile scores 75-90. A uniform
"all same response" profile SHOULD score low (30 or below) because it is
genuinely non-adiabatic. But a real human answering honestly should never
hit 0 unless they literally pressed one button the entire test.

| Score | Verdict |
|-------|---------|
| >= 80 | HIGH: directives can be trusted |
| >= 60 | MODERATE: directives are provisional |
| >= 40 | LOW: retake recommended |
| < 40 | CRITICAL: do not generate directives |

## Calculation Transparency

`explain_calculation()` produces a full audit chain for every score:

```
Domain Openness (3.50)
  = mean of facet means [4.0, 5.0, 3.0, 3.5, 4.0, 1.5]
  = 3.50
  -> percentile 73.4%

  Facet O1 Imagination (4.0)
    = mean of item scores [5.0, 4.0, 3.0, 4.0]
    Item I097 [+]: "Have a vivid imagination." response=5 -> score=5.0 (forward)
    Item I098 [+]: "Enjoy wild flights of fantasy." response=4 -> score=4.0 (forward)
    Item I099 [+]: "Love to daydream." response=3 -> score=3.0 (forward)
    Item I100 [+]: "Like to get lost in thought." response=4 -> score=4.0 (forward)
```

This lets the user (and auditors) verify every number traces back to raw responses.

## Design Philosophy Compliance

Every recommendation output includes:
```python
"design_notes": {
    "physics_basis": "Each recommendation derives from facet scores and drift analysis...",
    "not_consciousness": "These are behavioral adaptation directives, not claims about awareness, identity, or internal experience.",
}
```

Never use the word "self-model" or claim the tool measures consciousness.
It measures behavioral tendencies. Period.

## Verified Build

Built 2026-08-06 for IPIP-NEO-120:
- `gigi3/organism/tools/ipip_neo120/ipip_neo120_longitudinal.py` (~25K chars)
- 4 new API endpoints on :port (recommendations, explanation, timeline, drift)
- 16 recommendation templates across 5 domains (all `duration: ongoing`)
- 13 trackable metrics defined
- Drift detection with critical-slowing flags
- Full lifecycle tested with synthetic profiles
