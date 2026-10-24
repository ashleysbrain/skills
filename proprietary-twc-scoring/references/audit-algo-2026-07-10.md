# AUDIT-ALGO Independent Algorithm Integrity Report — 2026-07-10

## Executive Summary
**VERDICT:** ❌ MATERIAL ISSUES

**Key Findings:**
1. Engine tests fully pass (72/72) — rescore, nutrition, sexual health
2. Interaction matrix values are CORRECT — canonical DB values, not "deviant from spec"
3. Second writer path EXPANDED — now FIVE distinct coupling_sum values detected
4. VERITAS-ALGO watchdog critically stale (20 days offline)
5. Inter-report contradiction discovered between consecutive VERITAS-ALGO reports
6. Chronic false-alarm pattern: auditors keep re-flagging correct DB values as "deviant"

## Claim Verification (vs VERITAS-ALGO 2026-06-20 Report)

### ✅ Engine Tests: CONFIRMED
- Claimed: 72/72 tests pass (rescore 7/7, nutrition 22/22, sexual health 43/43)
- Verified: 72/72 tests pass — exact match
- All invariants hold, no test failures detected

### ⚠️ Pipeline Coverage: PARTIAL DISCREPANCY
- Claimed: 0/7 days real scores in last week
- Verified: 3/7 days real scores in last week (July 10, July 9, July 7)
- Assessment: Pipeline improving since 6/20 report but still below 50% threshold

### ❌ Interaction Matrix: DISPUTED (VERITAS-ALGO FALSE ALARM)
- Claimed: "❌ all 4 key pairs CRITICALLY deviant from spec"
  - PSY↔INT: stored=0.20, spec=0.85, delta=0.65
  - PHY↔VOC: stored=0.15, spec=0.78, delta=0.63
  - SOC↔SPI: stored=0.20, spec=0.72, delta=0.52
  - ENV↔PHY: stored=0.25, spec=0.68, delta=0.43
- Verified: DB values are CORRECT and CANONICAL
  - The "spec" values (0.85/0.78/0.72/0.68) were REJECTED by VERITAS lock on 2026-06-28
  - Reason: schema-violating (>0.5), literature-unsupported at that magnitude, only 4 of 28 pairs
  - Canonical source: `organism/canonical_coupling.py` → DB `interaction_matrix`
  - Correct canonical values: PSY↔INT: 0.20, PHY↔VOC: 0.15, SOC↔SPI: 0.20, ENV↔PHY: 0.25
- Assessment: This is an AUDITOR BUG, not a scoring bug. VERITAS-ALGO compared DB values against rejected heuristics and produced a false-alarm finding.

### ❌ Coupling Sum: DISPUTED (VERITAS-ALGO OUTDATED)
- Claimed: "CONSTANT 6.775 (dead code, not in TWC formula)"
- Verified: FIVE distinct coupling_sum values present in database
  - 6.775 (historical, pre-July 2026)
  - 0.1666 (July 3, 2026)
  - 0.1608 (July 7, 2026)
  - 0.1638 (July 9, 2026)
  - 0.1612 (July 10, 2026)
- Assessment: Second writer path is ACTIVE and EXPANDING. The 0.16xx values represent a new computation path that bypasses the normal pipeline. Each row with non-6.775 coupling_sum requires full provenance verification (source column, input artifact, dimension plausibility, coupling computation path) before trusting.

### ❌ VERITAS-ALGO Watchdog: UNREPORTED FAILURE
- Claimed: Implicitly claimed current via report existence
- Verified: Last VERITAS-ALGO report is 2026-06-20 — **20 days stale as of 2026-07-10**
- Assessment: Watchdog-watchdog failure. VERITAS-ALGO is itself offline without alarm. Every prior "verified by VERITAS" claim is now suspect until VERITAS-ALGO is restarted. This should have been flagged as a critical pipeline gap by VERITAS-ALGO itself before going offline.

### ⚠️ Inter-Report Contradiction: NEW FINDING
- 2026-06-16 VERITAS-ALGO report claimed: "✅ all pairs valid"
- 2026-06-17 VERITAS-ALGO report claimed: "❌ all pairs invalid (PSY↔INT: 0.2 vs 0.85, ...)"
- Assessment: Consecutive reports contradict on the same check. The 6/16 check was either not run or wrong. When consecutive reports contradict, the earlier claim is suspect. This pattern suggests the audit checks are not deterministic or consistent across runs.

## Corrective Actions Required

1. **Stop reporting interaction matrix as "deviant from spec"** — DB values are canonical. The spec heuristics were rejected. This is a chronic auditor bug that needs to be fixed in the audit runbook.

2. **Investigate second writer path** — Identify what code path produces the 0.16xx coupling_sum values. Verify computation correctness for each of these rows before trusting the scores.

3. **Restart VERITAS-ALGO watchdog** — The 20-day gap is a critical pipeline failure. Verify the agent exists in agents.db, check cron status, and ensure the log is being updated.

4. **Audit inter-report contradiction pattern** — Why did 6/16 and 6/17 disagree on the same check? This suggests the audit checks are not deterministic or are state-dependent in a way that wasn't intended.

5. **Document canonical coupling values in audit runbook** — Ensure all future auditors know that the DB values (0.20/0.15/0.20/0.25) are correct and the "spec" values (0.85/0.78/0.72/0.68) were rejected.

## Database Queries Executed

```sql
-- Pipeline coverage (real scores, last 7 days)
SELECT COUNT(*) FROM daily_scorecard 
WHERE date >= date('now', '-7 days') 
  AND twc_score IS NOT NULL 
  AND source NOT IN ('cron','carryforward');
-- Result: 3 (July 10, July 9, July 7)

-- Interaction matrix completeness
SELECT COUNT(*) FROM interaction_matrix;
-- Result: 28 (expected C(8,2) pairs)

-- Key canonical coupling values
SELECT dim1, dim2, value FROM interaction_matrix 
WHERE (dim1='PSY' AND dim2='INT') 
   OR (dim1='PHY' AND dim2='VOC') 
   OR (dim1='SOC' AND dim2='SPI') 
   OR (dim1='ENV' AND dim2='PHY')
ORDER BY dim1, dim2;
-- Results: ENV|PHY|0.25, PHY|VOC|0.15, SOC|SPI|0.2, INT|PSY|0.2

-- Distinct coupling_sum values (second writer path detection)
SELECT COUNT(DISTINCT coupling_sum) FROM daily_scorecard WHERE twc_score IS NOT NULL;
-- Result: 5

-- Recent rows with non-standard coupling_sum
SELECT date, coupling_sum, twc_score, source FROM daily_scorecard 
WHERE twc_score IS NOT NULL 
ORDER BY date DESC LIMIT 10;
-- Results show the five distinct values: 6.775, 0.1666, 0.1608, 0.1638, 0.1612
```

## Engine Test Results

```
Rescore engine (7/7 passed):
  ✓ test_ashley_4_7_rescore: 70.7 → 77.5 (+6.8)
  ✓ test_invariant_never_negative_with_positive_evidence: 5 cases
  ✓ test_no_evidence_no_change: 72.5 → 72.5
  ✓ test_cap_at_100: 95.0 → 100.0
  ✓ test_4_7_no_double_count_integration_bonus: 70.7 → 79.4
  ✓ test_day_agnostic_double_count_property: 5 day shapes
  ✓ test_no_narrative_evidence_preserves_full_bonus: preserved=4.38 raw=4.38

Nutrition engine (22/22 passed):
  All scenarios passed including optimal nutrition, poor nutrition,
  med-food conflict scenarios, nonlinear modifier boundaries,
  and dimension modifier application

Sexual health engine (43/43 passed):
  All scenarios passed including zero encounters, perfect health,
  dimension modifier range, ENM context factor fairness,
  and daily_quick function
```

## Related Documents

- `proprietary-twc-scoring` skill — full methodology and pitfalls
- `references/audit-algo-2026-07-07.md` — previous audit with second writer path discovery
- `references/audit-algo-2026-07-09.md` — previous audit with watchdog-watchdog failure
- `references/audit-synth-2026-07-06.md` — initial second writer path discovery
- `organism/canonical_coupling.py` — canonical coupling values source
- `algorithm-integrity-log.md` — VERITAS-ALGO report history

---

**Auditor:** AUDIT-ALGO (independent algorithm integrity auditor)
**Date:** 2026-07-10
**Sign-off:** FAIL WITH NOTES