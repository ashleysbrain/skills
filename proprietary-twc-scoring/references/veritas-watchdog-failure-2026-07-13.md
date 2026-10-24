# VERITAS-ALGO Watchdog Failure — 2026-07-13 AUDIT-ALGO Finding

## Summary
VERITAS-ALGO, the primary integrity watchdog for the TWC scoring system, stopped producing reports on 2026-06-22 and has not run for 14 days as of 2026-07-13. This represents a MATERIAL ISSUE — a dead watchdog means all prior "verified by VERITAS" claims are now suspect.

## Critical Finding: Chronic Misreporting of Corrected Data

### The Error Pattern
VERITAS-ALGO repeatedly flagged canonical interaction matrix values as "deviant from spec" by comparing against REJECTED heuristics:

**Rejected spec heuristics (WRONG):**
- PSY↔INT: 0.85
- PHY↔VOC: 0.78
- SOC↔SPI: 0.72
- ENV↔PHY: 0.68

These values were REJECTED by VERITAS lock on 2026-06-28 (`organism/canonical_coupling.py` lines 10-14) for:
- Schema violations (>0.5 exceeds cap)
- Literature-unsupported magnitude at those levels
- Only covering 4 of 28 C(8,2) pairs

**Canonical DB values (CORRECT):**
- PSY↔INT: 0.20 (stored as INT↔PSY due to canonical dim1<dim2 form)
- PHY↔VOC: 0.15
- SOC↔SPI: 0.20
- ENV↔PHY: 0.25

Full matrix: 28 pairs, C(8,2), range [0.05, 0.35], sum=5.05, avg=0.180

### Inter-Report Contradiction
- **Jun 16 report**: "✅ all pairs valid" — CORRECT assessment
- **Jun 17 report**: "❌ all pairs invalid (PSY↔INT: 0.2 vs 0.85, ...)" — WRONG assessment

When consecutive reports contradict on the same check, the earlier claim is suspect, but in this case the earlier (Jun 16) was correct and Jun 17 was wrong.

## Correct Auditor Verification Procedure

When verifying interaction matrix integrity:

```sql
-- 1. Verify completeness: 28 pairs (C(8,2))
SELECT COUNT(*) FROM interaction_matrix;  -- Expected: 28

-- 2. Verify no out-of-bounds values (capped at ±0.5)
SELECT COUNT(*) FROM interaction_matrix WHERE value < -0.5 OR value > 0.5;  -- Expected: 0

-- 3. Verify canonical form (dim1 < dim2 only)
SELECT COUNT(*) FROM interaction_matrix WHERE dim1 >= dim2;  -- Expected: 0

-- 4. Verify 4 key canonical pairs (NOT the rejected spec heuristics)
SELECT dim1, dim2, value FROM interaction_matrix 
WHERE (dim1='ENV' AND dim2='PHY') OR (dim1='PHY' AND dim2='VOC') 
   OR (dim1='SOC' AND dim2='SPI') OR (dim1='INT' AND dim2='PSY')
ORDER BY dim1, dim2;
-- Expected: ENV↔PHY: 0.25, PHY↔VOC: 0.15, SOC↔SPI: 0.2, INT↔PSY: 0.2

-- 5. Verify coupling_sum is constant (dead code detector)
SELECT COUNT(DISTINCT coupling_sum) FROM daily_scorecard WHERE twc_score IS NOT NULL;
-- Expected: 1 (the constant 6.775) unless second writer path detected
```

## Watchdog Liveness Check (MANDATORY for any verifier)

Before trusting any VERITAS-ALGO claim, verify the watchdog is alive:

```bash
# Check latest log entry timestamp
stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" /<workspace>

# Or read last 5 lines
tail -5 /<workspace>
```

**Staleness threshold**: >48 hours without a new entry = VERITAS-ALGO is dead = MATERIAL ISSUE.

## Real Pipeline Status (Jul 13, 2026)

 contrary to VERITAS's Jun 20 claim of "0/7 days":

```
REAL scored days (7d): 5/7
Real scored days (30d): 6/30
Last real score date: 2026-07-12
Rows in last 10 days: 6 (trailing gap: 4 days)

Sub-table coverage:
- nutrition_daily: 0/7 days
- sexual_health_daily: 0/7 days
- ef_compass_daily: 6/7 days

Engine tests: 72/72 PASS
- Rescore: 7/7
- Nutrition: 22/22
- Sexual health: 43/43
```

## Corrective Actions Required

1. **Restart VERITAS-ALGO** — The watchdog must resume regular reporting (target: bi-daily)
2. **Fix spec-comparison logic** — Update VERITAS-ALGO to compare against canonical DB values (0.20/0.15/0.20/0.25), not the rejected heuristics
3. **Audit previous VERITAS-ALGO reports** — Any claim of "deviant from spec" with delta >0.40 is suspect and needs re-verification
4. **Document the canonical source** — Point to `organism/canonical_coupling.py` as the authoritative spec, not the old heuristics

## References

- Canonical coupling spec: `organism/canonical_coupling.py` lines 10-14
- DB source: `ashley_unified_health.db` → `interaction_matrix` table
- VERITAS lock date: 2026-06-28
- Audit-ALGO discovery: 2026-07-13