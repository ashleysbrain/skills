# Interaction Matrix Verification Sequence

**Purpose:** Independently verify interaction matrix coupling values are correct and canonical, avoiding FALSE-ALARM audits that compare against rejected spec heuristics.

## Background

VERITAS-ALGO has a chronic FALSE-ALARM pattern where it compares DB-stored coupling values against REJECTED spec heuristics (PSY↔INT: 0.85, PHY↔VOC: 0.78, SOC↔SPI: 0.72, ENV↔PHY: 0.68). These heuristics were REJECTED by VERITAS lock in `canonical_coupling.py` lines 10-14 for:
- Schema violations (>0.5, capped at ±0.5)
- Literature-unsupported magnitude
- Covered only 4 of 28 pairs

The CORRECT canonical values are stored in the DB and loaded by `canonical_coupling.py`:
- PSY↔INT: 0.20
- PHY↔VOC: 0.15
- SOC↔SPI: 0.20
- ENV↔PHY: 0.25

## Verification Sequence

### Step 1: Verify Against Canonical Source (MANDATORY anti-false-alarm check)

```bash
python3 /<workspace>
```

**Expected output:**
```
canonical_coupling: OK — 28 pairs, range 0.05-0.35
top-5: PHY-PSY=0.35; ENV-PSY=0.3; FIN-VOC=0.3; ENV-PHY=0.25; FIN-PSY=0.25
```

If this passes, the DB values are canonical. Proceed to step 2 with THESE expectations, NOT the rejected heuristics.

### Step 2: Verify Matrix Completeness and Schema

```bash
sqlite3 /<workspace> "
SELECT COUNT(*) FROM interaction_matrix;
SELECT COUNT(*) FROM interaction_matrix WHERE value < -0.5 OR value > 0.5;
SELECT COUNT(*) FROM interaction_matrix WHERE dim1 >= dim2;
SELECT SUM(value), AVG(value), MIN(value), MAX(value) FROM interaction_matrix;
"
```

**Expected results:**
- Rows: 28 (C(8,2) pairs)
- Out-of-bounds: 0 (schema-capped at ±0.5)
- Non-canonical: 0 (canonical form stores dim1 < dim2 only)
- Stats: sum≈5.05, avg≈0.18, range=[0.05, 0.35]

### Step 3: Verify Key Canonical Coupling Values

```bash
sqlite3 /<workspace> "
SELECT dim1, dim2, value FROM interaction_matrix
WHERE (dim1='PSY' AND dim2='INT') OR (dim1='PHY' AND dim2='VOC')
   OR (dim1='SOC' AND dim2='SPI') OR (dim1='ENV' AND dim2='PHY')
ORDER BY dim1, dim2;
"
```

**Expected canonical values:**
- ENV↔PHY: 0.25
- PSY↔INT: 0.20 (may appear as INT↔PSY in DB)
- PHY↔VOC: 0.15
- SOC↔SPI: 0.20

### Step 4: Check for Second Writer Path (coupling_sum variance)

```bash
sqlite3 /<workspace> "
SELECT COUNT(DISTINCT coupling_sum) FROM daily_scorecard WHERE twc_score IS NOT NULL;
SELECT date, coupling_sum, twc_score, source FROM daily_scorecard
WHERE twc_score IS NOT NULL AND coupling_sum != 6.775
ORDER BY date DESC;
"
```

**Expected:**
- DISTINCT count: 1 (constant 6.775, unless second writer path exists)
- If any row has coupling_sum ≠ 6.775: quarantine and verify provenance

## False-Alarm Detection

If an audit report claims:
- "all 4 pairs CRITICALLY deviant from spec"
- "PSY↔INT: 0.2 vs 0.85" or similar with deltas >0.40
- "spec values" are 0.85/0.78/0.72/0.68

**This is a FALSE-ALARM.** The audit is comparing against rejected heuristics, not canonical values.

**Correct action:**
1. Flag as FALSE-ALARM in the audit verdict
2. Correct the finding: DB values are CORRECT per canonical_coupling.py
3. The real defect is the dead `coupling_sum` constant (not the values)

## Inter-Report Contradiction Pattern

When consecutive reports contradict on the same check:
- Example: Jun 16 claimed "✅ all pairs valid" but Jun 17 claimed "❌ all pairs invalid"
- The canonical DB values are CORRECT — the earlier claim was right, later was wrong
- Flag the earlier report's claim as ⚠️ PARTIAL and note the contradiction

## References

- Canonical source: `/<workspace>`
- VERITAS lock rejection: lines 10-14 (spec heuristics rejected)
- DB: `ashley_unified_health.db` table `interaction_matrix`
- Latest verification: 2026-07-20 by AUDIT-ALGO (canonical values confirmed, watchdog stale 30 days)