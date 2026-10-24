# AUDIT-ALGO Report: 2026-07-12

**Auditor**: AUDIT-ALGO (Independent Algorithm Integrity Auditor)  
**VERITAS-ALGO Report Reviewed**: 2026-06-20 12:00:00 (22 days stale)  
**Audit Status**: PASS WITH NOTES

## Executive Summary

VERITAS-ALGO itself is OFFLINE — the integrity watchdog has not produced a report for 22 days (last entry 2026-06-20). This is a watchdog-watchdog failure: the system designed to catch scoring problems is itself failing without alarm. When the primary auditor is stale, all prior "verified by VERITAS" claims are now suspect until VERITAS-ALGO is restarted.

Engine tests are CLEAN (72/72 pass). Pipeline coverage has IMPROVED to 4/7 days since June 20 but remains below the 50% threshold. The interaction matrix contains CORRECT canonical values — VERITAS-ALGO's chronic "deviant from spec" false-alarm is an AUDITOR BUG, not a scoring bug.

## Findings

### ✅ CONFIRMED: Engine Tests Pass
- Rescore engine: 7/7 tests pass
- Nutrition engine: 22/22 tests pass
- Sexual health engine: 43/43 tests pass
- **Total**: 72/72 tests pass

### ⚠️ PARTIAL: Pipeline Coverage
- **VERITAS-ALGO claimed**: 0/7 days (stale data from June 20)
- **AUDIT-ALGO verified**: 4/7 days with real scores in last week
- **Days scored**: July 11, July 10, July 9, July 7
- **Status**: IMPROVING but still below 50% threshold
- **Last real score date**: 2026-07-11
- **Real scored days (30d)**: 5/30
- **Carry-forward days (7d)**: 0

### ⚠️ PARTIAL: Interaction Matrix Claims
- **VERITAS-ALGO claimed**: "all 4 key pairs CRITICALLY deviant"
  - PSY↔INT: stored=0.20, spec=0.85, delta=0.65
  - PHY↔VOC: stored=0.15, spec=0.78, delta=0.63
  - SOC↔SPI: stored=0.20, spec=0.72, delta=0.52
  - ENV↔PHY: stored=0.25, spec=0.68, delta=0.43
- **AUDIT-ALGO verified**: DB values are CORRECT
  - PSY↔INT: 0.20 (canonical)
  - PHY↔VOC: 0.15 (canonical)
  - SOC↔SPI: 0.20 (canonical)
  - ENV↔PHY: 0.25 (canonical)
- **Root cause**: VERITAS-ALGO compared DB values against REJECTED heuristics (0.85/0.78/0.72/0.68)
- **Note**: These spec values were REJECTED for schema violations (>0.5), literature-unsupported magnitude, and covering only 4 of 28 pairs

### ✅ CONFIRMED: Interaction Matrix Completeness
- Total pairs: 28/28 (C(8,2) = 28, correct)
- Out-of-bounds values: 0 (schema-capped at ±0.5)
- Non-canonical pairs: 0 (all stored with dim1 < dim2)
- Matrix stats: sum=5.05, avg=0.180, range=[0.05, 0.35]

### ⚠️ EXPANDED: Second Writer Path for Coupling Sum
- **Previously known**: 2 distinct coupling_sum values (6.775 historical, 0.1666 July 3)
- **Now discovered**: 6 distinct values
  - 6.775 (historical constant)
  - 0.1666 (July 3)
  - 0.1608 (July 7)
  - 0.1638 (July 9)
  - 0.1612 (July 10)
  - 0.1608 (July 11)
- **Implication**: Multiple active writer paths bypass the normal pipeline
- **Risk**: These rows require full provenance verification before trusting (source column, input artifact, dimension plausibility, coupling computation path)

### ❌ CRITICAL: VERITAS-ALGO Watchdog Failure
- **Last VERITAS-ALGO report**: 2026-06-20 12:00:00 (22 days old)
- **Expected frequency**: Bi-daily
- **Staleness**: 22 days without report (critical threshold is 48 hours)
- **Impact**: Every prior "verified by VERITAS" claim is now suspect
- **Recommendation**: Restart VERITAS-ALGO immediately

## Inter-Report Contradictions Found

### 2026-06-16 vs 2026-06-17
- **6/16**: "✅ all pairs valid"
- **6/17**: "❌ all pairs invalid (PSY↔INT: 0.2 vs 0.85, ...)"
- **Contradiction**: Same check, opposite results
- **Interpretation**: Earlier claim (6/16) was suspect — either not run or wrong

### Chronic False-Alarm Pattern
- **Jun 27 SYNTHESIS**: "deviant from spec"
- **Jun 22 VERITAS-ALGO**: "CRITICALLY deviant"
- **Jun 20 VERITAS-ALGO**: "CRITICALLY deviant"
- **Reality**: DB values are CORRECT per canonical_coupling.py
- **Root cause**: All compared against REJECTED heuristics, not canonical values
- **This is an AUDITOR BUG, not a scoring bug**

## Corrective Actions Recommended

1. **Restart VERITAS-ALGO** — The watchdog is dead, recent audit coverage is zero. This is the highest priority.

2. **Fix VERITAS-ALGO's interaction matrix check** — The check must compare against canonical values (0.20/0.15/0.20/0.25), not rejected heuristics (0.85/0.78/0.72/0.68).

3. **Investigate 0.16xx coupling_sum rows** — The 6 rows with non-constant coupling_sum values require full provenance verification:
   - Verify source column is accurate
   - Verify input artifact exists and is valid
   - Verify dimension scores are plausible given context
   - Verify coupling computation path (which code path produced these values)

4. **Address sub-table coverage gap** — nutrition_daily and sexual_health_daily have no recent entries (0/7 days). Investigate why these tables are not being populated.

5. **Audit previous VERITAS-ALGO reports** — Since the watchdog was offline for 22 days and has a history of false-alarms, all claims from the last 6 months should be independently re-verified.

## Appendix: Audit Queries

```sql
-- Pipeline coverage
SELECT COUNT(*) FROM daily_scorecard WHERE date >= date('now', '-7 days') AND twc_score IS NOT NULL AND source NOT IN ('cron','carryforward');
SELECT COUNT(*) FROM daily_scorecard WHERE date >= date('now', '-30 days') AND twc_score IS NOT NULL AND source NOT IN ('cron','carryforward');
SELECT date FROM daily_scorecard WHERE twc_score IS NOT NULL AND source NOT IN ('cron','carryforward') ORDER BY date DESC LIMIT 1;

-- Interaction matrix
SELECT COUNT(*) FROM interaction_matrix;
SELECT dim1, dim2, value FROM interaction_matrix WHERE (dim1='PSY' AND dim2='INT') OR (dim1='PHY' AND dim2='VOC') OR (dim1='SOC' AND dim2='SPI') OR (dim1='ENV' AND dim2='PHY') ORDER BY dim1, dim2;

-- Coupling sum writer paths
SELECT COUNT(DISTINCT coupling_sum) FROM daily_scorecard WHERE twc_score IS NOT NULL;
SELECT date, coupling_sum, twc_score, source FROM daily_scorecard WHERE twc_score IS NOT NULL AND coupling_sum != 6.775 ORDER BY date DESC;
```

## Related Documents

- `proprietary-twc-scoring` skill (updated with 2026-07-12 findings)
- `references/audit-algo-2026-07-10.md` (previous AUDIT-ALGO report)
- `references/audit-synth-2026-07-06.md` (discovery of second writer path)