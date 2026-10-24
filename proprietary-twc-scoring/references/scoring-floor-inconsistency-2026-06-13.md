# Scoring Floor Inconsistency — the specialist engine (2026-06-13)

## Context

the specialist engine (Karl Popper methodology specialist) conducted a quality gate review of the
the specialist engine Engine & 8D360 scoring system. This reference captures the specific
finding about structural floor inconsistency in LLM-generated preliminary scores, with
traced computations from real scoring outputs.

---

## The Finding

The AISHA-MD LLM generates preliminary TWC scores that are **14-15 points below the
structural floor** computed from their own base dimensions. The rescore engine silently
absorbs this inconsistency and reports the full delta as "improvement."

This means **77-91% of reported rescore "improvement" is correction of LLM scoring
inconsistency, not actual wellness change.**

---

## Traced Computation: May 29 v1 Rescore

Source: `~/your-workspace/health-private/daily/rescore-result-2026-05-29.json`

### Step 1: Extract preliminary base dimensions

| Dim | Value | Weight |
|-----|-------|--------|
| psy | 7.0 | 0.18 |
| phy | 5.0 | 0.16 |
| env | 5.0 | 0.11 |
| soc | 5.5 | 0.12 |
| spi | 5.0 | 0.10 |
| int | 5.0 | 0.13 |
| voc | 6.5 | 0.11 |
| fin | 5.0 | 0.09 |

### Step 2: Compute weighted sum

```
weighted_sum = 7.0×0.18 + 5.0×0.16 + 5.0×0.11 + 5.5×0.12 + 5.0×0.10 + 5.0×0.13 + 6.5×0.11 + 5.0×0.09
             = 1.26 + 0.80 + 0.55 + 0.66 + 0.50 + 0.65 + 0.715 + 0.45
             = 5.585
```

### Step 3: Compute structural floor

```
weighted_base_100 = 5.585 × 10 = 55.85
stacked_modifier = sqrt(0.985 × 1.0) = 0.992
structural_floor = 55.85 × 0.992 = 55.40
```

### Step 4: Compare

```
preliminary_TWC_reported = 41.5
structural_floor          = 55.40
inconsistency_gap         = 55.40 - 41.5 = 13.90 points
final_TWC                 = 59.1
rescore_delta             = 59.1 - 41.5 = +17.6
correction_fraction       = 13.90 / 17.6 = 79%
```

**79% of the "improvement" was absorbing the LLM's own scoring inconsistency.**

---

## Traced Computation: May 29 v2 Rescore

Source: `~/your-workspace/health-private/daily/rescore-result-2026-05-29-v2.json`

### Preliminary values

Base dimensions: psy=7.5, phy=6.5, env=6.0, soc=7.0, spi=6.5, int=7.0, voc=7.5, fin=5.5
Modifiers: nutrition=1.045, sex=1.0552

```
weighted_sum = 7.5×0.18 + 6.5×0.16 + 6.0×0.11 + 7.0×0.12 + 6.5×0.10 + 7.0×0.13 + 7.5×0.11 + 5.5×0.09
             = 1.35 + 1.04 + 0.66 + 0.84 + 0.65 + 0.91 + 0.825 + 0.495
             = 6.77

weighted_base_100 = 6.77 × 10 = 67.7
stacked_modifier = sqrt(1.045 × 1.0552) = 1.050
structural_floor = 67.7 × 1.050 = 71.09

preliminary_TWC_reported = 56.0
inconsistency_gap = 71.09 - 56.0 = 15.09 points
final_TWC = 72.5
rescore_delta = 72.5 - 56.0 = +16.5
correction_fraction = 15.09 / 16.5 = 91%
```

**91% of the "improvement" was absorbing the LLM's own scoring inconsistency.**

---

## The Rescore Engine Already Knows

The production code (`rescore_engine.py` line 666) handles this silently:

```python
structural_prelim_floor = max(prelim_twc_reported, prelim_pre_integration)
```

This prevents false plausibility-guard alerts but reports the delta from the LLM's
inconsistent preliminary, not the structural floor.

---

## Impact on Primary Success Metric

PRODUCT_THESIS_V1_LOCKED.md defines:
> "Primary metric: % of active users who report measurable improvement in their coached area within 30 days"

If 77-91% of "improvement" is scoring inconsistency correction, this metric cannot
distinguish between:
- User actually improved (real change)
- LLM scored inconsistently yesterday, scored more consistently today (correction artifact)

The metric is uninterpretable until the inconsistency is fixed.

---

## Monotonicity Bias (Related Finding)

The rescore engine also has a hardcoded invariant (lines 682-689):

```python
has_positive_evidence = any(l > 0 for l in base_lifts.values()) or followthrough_credit > 0
if has_positive_evidence and final_twc < prelim_twc_reported:
    raise AssertionError("INVARIANT VIOLATED: positive evidence produced lower TWC")
```

This means the system **cannot detect** patterns where one dimension improves while the
aggregate should decline. Combined with the structural floor inconsistency, the system
has two compounding biases:
1. Preliminary scores are systematically depressed (LLM inconsistency)
2. Rescores are structurally guaranteed to increase when positive evidence exists

The combined effect: rescores almost always show "improvement" regardless of what
actually happened. This is the measurement equivalent of confirmation bias.

---

## Remediation

1. **Fix the LLM prompt** to produce structurally consistent preliminary scores
   (TWC should equal weighted_sum × stacked_modifier ± integration_bonus)
2. **Report deltas from structural floor**, not from LLM-reported preliminary
3. **Add `correction_fraction` field** to rescore output
4. **Flag days where correction_fraction > 50%** as "inconsistent preliminary — delta not interpretable"
5. **Track unconstrained scores** alongside clinically adjusted scores (to handle monotonicity bias)
6. **Disclose both biases** in any research or metric derived from these scores
