# Drift Detection Statistical Validation

Validation patterns for the longitudinal drift detection layer
(`*_longitudinal.py`) in assessment tools. Confirmed 2026-08-13 during
physics/math peer-review validation of the IPIP-NEO-120 drift engine.

**Verdict: the default drift detection methodology does not survive peer review.**
3 critical, 3 high, 3 medium, 1 low issues. The patterns below are reusable
for ANY assessment tool that implements longitudinal drift detection.

---

## Critical Issues (desk-reject level)

### 1. Missing Multiple Comparisons Correction

**The flaw:** `detect_drift()` tests N facets independently (e.g., 30 for
IPIP-NEO) with no family-wise error rate or FDR correction.

**Quantified impact (IPIP-NEO-120, 30 facets):**
- Per-facet false positive rate at threshold 0.5: **0.36**
- Expected false positives per measurement: **10.9**
- P(at least 1 false positive): **1.0000**

**Fix:** Apply Benjamini-Hochberg FDR correction (q=0.05) across all N
facet tests. Bonferroni is overly conservative for correlated facets.

### 2. Threshold Has No Statistical Basis

**The flaw:** Fixed threshold (0.5 on 1-5 Likert) with no connection to
the Standard Error of Measurement (SEM).

**SEM reference (1-5 scale, SD ≈ 1.1 per item):**

| Items/facet | α=0.70 | α=0.75 | α=0.80 |
|-------------|--------|--------|--------|
| 4 (IPIP-120) | 0.602 | 0.550 | 0.492 |
| 10 (IPIP-300) | 0.380 | 0.347 | 0.311 |

Threshold 0.5 against 4-item facets = 0.83-1.02 SEM — within the 95% CI.
A delta of 0.5 cannot distinguish drift from measurement noise.

**Fix:** Replace with paired t-test or Wilcoxon signed-rank test. Report
p-value AND effect size (Cohen's d). Require p < 0.05 AND |d| > 0.3.

### 3. Biased Variance Estimator

**The flaw:** `sum((x - mean) ** 2) / len(x)` — population variance, not
sample variance (missing Bessel's correction `/ (N-1)`).

At default window=3, underestimates by 33% (confirmed via 100k-trial
Monte Carlo: E[pop/samp] = 0.6667 = (n-1)/n). Since critical-slowness
flags trigger when variance > threshold, this bias **suppresses the
exact signal it's designed to detect**.

**Fix:** Use `statistics.variance()` or `numpy.var(x, ddof=1)`.

---

## High Issues (major revision)

### 4. Critical Slowing Metric: Wrong Statistic

Variable named `CSD_VARIANCE_RATIO` but code computes a **mean ratio**
(recent_mean / baseline_mean), not a variance ratio. Scheffer et al.
(2009, *Nature*) predicts four early-warning signals:

1. Increased variance (CV rises)
2. Increased autocorrelation (AR(1) coefficient rises)
3. Increased skewness
4. Decreased return rate (= increased recovery time)

The code captures only #4, mislabeled as variance.

**Fix:** Compute genuine variance ratio AND lag-1 autocorrelation.
Rename mislabeled variables.

### 5. Insufficient Sample Size for Split-Half

n=4 required → halves of 2 → SE(half-mean) = 1.41 → ratio 95% CI ≈ ±2.77.
The warning threshold (1.5) is within noise of 1.0.

| Total n | Half | SE(half-mean) | Ratio CI ≈ |
|---------|------|---------------|-------------|
| 4       | 2    | 1.41          | ±2.77       |
| 10      | 5    | 0.89          | ±1.75       |
| 20      | 10   | 0.63          | ±1.24       |

**Fix:** Require n ≥ 20. Report confidence intervals on all ratios.

### 6. Endpoint Slope Instead of Regression Slope

Trend detection uses `(last - first) / (n-1)` — only 2 of n points.
Should use Theil-Sen estimator or Mann-Kendall trend test.

---

## Medium Issues

### 7. Proportion Tests Without Power

"60% above mean → inflation" is not significant for small fleets:

| n=10 | n=20 | n=50 | n=100 |
|------|------|------|-------|
| p=0.377 | p=0.252 | p=0.101 | **p=0.028** |

**Fix:** Use exact binomial test, require n ≥ 50 for 60% cutoff.

### 8. Undefined Variance Type in Collapse Detection

"Variance < 0.5" doesn't specify across-time, across-dimension, or
across-cohort. **Fix:** Use Levene's test against fleet baseline.

### 9. Inconsistent Slope Thresholds

Different drift classes use different thresholds (0.02, 0.05) with no
justification. Hard-coded values override class constants.

---

## Audit Procedure

When validating ANY longitudinal drift detection module:

1. Count independent tests. If >1 with no correction → severity-1.
2. Express threshold in SEM units. If < 1.96 SEM → severity-1.
3. Check variance estimator. If `/N` not `/(N-1)` → severity-1.
4. For critical slowing: verify it computes variance/autocorrelation,
   not just mean ratio.
5. For split-half: compute SE of half-means. If warning threshold is
   within noise → severity-2.
6. For slope-based detection: check if it uses regression or endpoint.
7. Run Monte Carlo (≥10k trials, fixed seed) to confirm false positive
   rates empirically.

## Files Audited (2026-08-13)

| Component | File | Criticals | Highs |
|-----------|------|-----------|-------|
| Personality drift | `ipip_neo120_longitudinal.py` (3 copies) | 3 | — |
| Critical slowing | `ds-banting-engine/.../cognitive.py` | — | 2 |
| Category drift | `ds-tanaka-engine/.../cognitive.py` | — | 1 |
| Score inflation | `8D360AI/docs/METHODOLOGY.md` §9d | — | 2 |
