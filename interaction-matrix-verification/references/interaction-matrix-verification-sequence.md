# Interaction Matrix Verification Sequence

Complete copy-pasteable sequence for interaction matrix verification in scoring systems.

## When to Run
During any scoring system audit, especially when verifying Engine Completeness for SMI or checking whether coupling terms actually affect TWC calculations.

## Complete Sequence

### 1. Canonical Source Verification (MANDATORY FIRST STEP)
```bash
python3 /<workspace>
```
This loads authoritative values from DB and runs self-tests. If this passes, the DB values are canonical. Proceed to step 3 with those expectations, NOT the rejected heuristics.

### 2. SQL Verification via Terminal
```bash
sqlite3 /<workspace> "
  SELECT COUNT(*) FROM interaction_matrix;
  SELECT COUNT(*) FROM interaction_matrix WHERE value < -0.5 OR value > 0.5;
  SELECT COUNT(*) FROM interaction_matrix WHERE dim1 >= dim2;
  SELECT dim1, dim2, value FROM interaction_matrix
  WHERE (dim1='PSY' AND dim2='INT') OR (dim1='PHY' AND dim2='VOC')
     OR (dim1='SOC' AND dim2='SPI') OR (dim1='ENV' AND dim2='PHY')
  ORDER BY dim1, dim2;
  SELECT COUNT(DISTINCT coupling_sum) FROM daily_scorecard WHERE twc_score IS NOT NULL;
"
```

Expected results:
- Row count: 28
- Out-of-range count: 0
- Non-canonical form (dim1 >= dim2): 0
- Key pairs: PSY↔INT: 0.20, PHY↔VOC: 0.15, SOC↔SPI: 0.20, ENV↔PHY: 0.25
- Distinct coupling_sum values: 1 (6.775), unless second writer path detected

### 3. DEAD CODE CHECK — Verify Scripts Actually READ the Matrix
```bash
search_files(pattern='interaction_matrix', path='/<workspace>', target='content')
```

- **Result count = 0**: DEAD CODE. The matrix exists but is never used during scoring.
- Credit in audits = 0 for production use, regardless of how well-defined the matrix is.

### 4. If Multiple Coupling Sum Values Found (Second Writer Path)
```bash
sqlite3 /<workspace> "
  SELECT date, coupling_sum, twc_score, source FROM daily_scorecard
  WHERE twc_score IS NOT NULL AND coupling_sum != 6.775
  ORDER BY date DESC;
"
```
Quarantine those rows and run full provenance verification (source column, input artifact, dimension plausibility) before trusting them.

## FALSE-ALARM PATTERN (CRITICAL)

### The Pattern
Auditors compare DB values (0.20/0.15/0.20/0.25) against REJECTED spec heuristics (0.85/0.78/0.72/0.68) and report "CRITICALLY deviant" with deltas >0.60. This is FALSE-ALARM.

### How It Happens
The 0.85/0.78/0.72/0.68 values were REJECTED by VERITAS lock (canonical_coupling.py lines 10-14) for:
- Schema violations (>0.5)
- Literature-unsupported magnitude
- Covering only 4 of 28 pairs

The canonical_coupling.py module IS the authoritative source. The DB values at 28 pairs are CORRECT.

### Detection
If an audit claims "all pairs invalid" or "CRITICALLY deviant from spec" with deltas >0.40, immediately run canonical_coupling.py. If it passes ("OK — 28 pairs, range 0.05-0.35"), the audit is comparing against rejected heuristics.

### Known False-Alarm Cases
- VERITAS-ALGO 2026-06-16: "✅ all pairs valid"
- VERITAS-ALGO 2026-06-17: "❌ all pairs invalid" (contradiction)
- VERITAS-ALGO 2026-06-20: "❌ all 4 key pairs CRITICALLY deviant" (false-alarm repeated)
- Jun 27 SYNTHESIS report: repeated false-alarm

## MANDATORY ENFORCEMENT
When VERITAS-ALGO reports claim "all pairs invalid" or "CRITICALLY deviant from spec," AUDIT-ALGO MUST re-verify using canonical_coupling.py as ground truth. Do NOT propagate "deviant from spec" claims without first verifying canonical_coupling.py passes.

## Graph Task-Level Classification (T-261021-0058)
This sequence is an **edge-level** verification: the matrix is a weighted adjacency matrix over the 8 dimension-nodes, and each of the 28 rows (C(8,2)) is one weighted edge. Step 1 verifies edge weights against the canonical source; step 2 verifies shape/range/canonical form; step 3 verifies **message flow over the edges** (dead code = edges carrying no messages: defined-but-unread); step 4 checks writer-path uniqueness (one aggregation rule — a second coupling_sum value means a second, unordered fold). Vocabulary and onboarding rules: `/<workspace>`.

## History
- 2026-06-28: VERITAS lock applied, spec heuristics rejected
- 2026-07-06: AUDIT-SYNTH discovered chronic audit misreporting
- 2026-07-13: AUDIT-ALGO flagged FALSE-ALARM pattern, warned about repeated misreporting
- 2026-07-16: AUDIT-ALGO added mandatory enforcement rule
- 2026-07-19: AXIOM audit discovered DEAD CODE pattern (28 rows defined, 0 scripts reading)
- 2026-07-26: AUDIT-SMI integrated DEAD CODE detection into verification sequence