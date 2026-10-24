# AUDIT-ALGO Findings — 2026-07-13

## Scope
Independent verification of VERITAS-ALGO's latest report (2026-06-20 12:00:00).

## Critical Findings

### 1. VERITAS-ALGO Chronic False-Alarm Pattern
**Finding:** VERITAS-ALGO repeatedly flags DB interaction_matrix values as "CRITICALLY deviant" by comparing against REJECTED spec heuristics (0.85/0.78/0.72/0.68).

**Root Cause:** The canonical source (`organism/canonical_coupling.py` lines 10-14) VERITAS-REJECTS those heuristics for schema violations (>0.5), literature-unsupported magnitude, and covering only 4 of 28 pairs.

**Correct State:** DB values (0.20/0.15/0.20/0.25) MATCH the canonical source and are CORRECT.

**Evidence:**
```
python3 /<workspace>
# Verify output: 28 pairs, canonical ordering, scale 0.05-0.35, schema-valid ✓
```

**Remediation:** VERITAS-ALGO's comparison logic must be fixed to use canonical values from canonical_coupling.py, not rejected heuristics.

### 2. Coupling Sum Actually Active
**Finding:** VERITAS-ALGO claimed "CONSTANT 6.775 (dead code)" but actual data shows coupling_sum is ACTIVE and non-constant.

**Evidence:**
```sql
SELECT DISTINCT coupling_sum, COUNT(*) as count FROM daily_scorecard 
WHERE coupling_sum IS NOT NULL GROUP BY coupling_sum;
-- Results: 0.1608|2, 0.1612|1, 0.1638|2, 0.1666|1, 6.775|10
```

Recent transcript rows (7/7-7/12) have coupling_sum ~0.16, NOT the constant 6.775.

**Implication:** A SECOND writer path exists and is actively computing non-constant coupling values from dimension scores. This contradicts the "dead code" claim.

### 3. twc_history Table Stale
**Finding:** Last entry 2026-05-26, but daily_scorecard has entries through 2026-07-12.

**Evidence:**
```sql
SELECT date FROM twc_history ORDER BY date DESC LIMIT 1;  -- 2026-05-26
SELECT date FROM daily_scorecard WHERE twc_score IS NOT NULL ORDER BY date DESC LIMIT 1;  -- 2026-07-12
```

**Implication:** No new writes to twc_history in 6+ weeks = broken pipeline segment. Momentum tracking (momentum coefficient=0.05) and PCM/CSI computation features are offline.

### 4. Inter-Report Contradiction
**Finding:** Consecutive VERITAS-ALGO reports contradict on the same check.

**Evidence:**
- 2026-06-16 claimed: "✅ all pairs valid"
- 2026-06-17 claimed: "❌ all pairs invalid (PSY↔INT: 0.2 vs 0.85, ...)"

**Root Cause:** Jun 16 compared against canonical values (correct), Jun 17 compared against rejected heuristics (incorrect).

## Minor Discrepancies

### Pipeline Coverage Under-Reported
**VERITAS Claim:** 0/7 days last week
**Actual:** 4/7 with real transcript scores (7/7, 7/9, 7/10, 7/11, 7/12 all have real scores, source=transcript)

## Verified Correct

### Engine Tests
- Rescore: 7/7 passed ✅
- Nutrition: 22/22 passed ✅
- Sexual health: 43/43 passed ✅

### Interaction Matrix Completeness
- 28/28 pairs present ✅
- Schema-capped (all values in range 0.05-0.35) ✅
- Canonical ordering (dim1 < dim2 for all) ✅

### Sub-table Coverage
- nutrition_daily: 0/7 (matches VERITAS)
- sexual_health_daily: 0/7 (matches VERITAS)
- ef_compass_daily: 6/7 (matches VERITAS)

### Baselines.json
- twcBaseline: null (drift calculation impossible) — matches VERITAS

## Recommendations

1. **Fix VERITAS-ALGO comparison logic:** Use canonical_coupling.py as the authoritative source, not the rejected heuristics
2. **Restart VERITAS-ALGO:** Dead for 14 days (last report 2026-06-22)
3. **Investigate second writer path:** Understand why recent transcript rows have coupling_sum ~0.16 instead of 6.775
4. **Reconnect twc_history pipeline:** Identify why no new writes since 2026-05-26
5. **Correct pipeline coverage reporting:** Use the correct query to avoid under-reporting real scored days

## Audit Verdict
**FAIL** — Chronic false-alarm pattern, coupling_sum actually active (not dead), twc_history pipeline broken.

---
**Auditor:** AUDIT-ALGO (independent algorithm integrity auditor)  
**Date:** 2026-07-13  
**VERITAS-ALGO Report Reviewed:** 2026-06-20 12:00:00