---
name: interaction-matrix-verification
description: Verify interaction matrices are actually used in scoring.
tags: [interaction-matrix, coupling-matrix, scoring, verification, dead-code, canonical-coupling]
---

# Interaction Matrix Verification

## When to Use
When verifying that an interaction/coupling matrix in a scoring system is actually working, not just defined in a database. The critical distinction: a matrix can be fully populated yet produce zero effect in production if no scoring script reads it.

## The DEAD CODE Pattern
A database table or data structure can be FULLY POPULATED yet produce ZERO effect in production if no scoring script actually reads it. AXIOM gave full credit (28/28 rows) for interaction matrix existence, but search_files showed ZERO scripts using 'interaction_matrix' pattern. This is DEAD CODE — defined but never called.

**Verification principle:** Check if the structure EXISTS in DB/FS (e.g., `SELECT COUNT(*) FROM interaction_matrix`) AND verify scripts actually READ it during scoring. Zero matches = dead code, credit = 0, regardless of how well-defined the structure is.

## Verification Sequence

### Step 1: Verify Against Canonical Source First (CRITICAL)
The canonical_coupling.py module is the authoritative source. Run it before comparing DB values:
```bash
python3 /<workspace>
```
This loads authoritative values from DB and runs self-tests. If this passes, the DB values are canonical.

### Step 2: Verify Completeness
```sql
SELECT COUNT(*) FROM interaction_matrix;
-- Expected: 28 (C(8,2) pairs)

SELECT COUNT(*) FROM interaction_matrix WHERE value < -0.5 OR value > 0.5;
-- Expected: 0 (schema-capped)
```

### Step 3: Verify Key Canonical Coupling Values
```sql
SELECT dim1, dim2, value FROM interaction_matrix
WHERE (dim1='PSY' AND dim2='INT') OR (dim1='PHY' AND dim2='VOC')
   OR (dim1='SOC' AND dim2='SPI') OR (dim1='ENV' AND dim2='PHY')
ORDER BY dim1, dim2;
```
Expected canonical values: PSY↔INT: 0.20, PHY↔VOC: 0.15, SOC↔SPI: 0.20, ENV↔PHY: 0.25

**CRITICAL WARNING:** The 0.85/0.78/0.72/0.68 values were REJECTED by VERITAS lock for schema violations (>0.5), literature-unsupported magnitude, and covering only 4 of 28 pairs. Do NOT compare DB values against these rejected heuristics.

### Step 4: DEAD CODE CHECK — Verify Scripts Actually READ the Matrix
```bash
search_files(pattern='interaction_matrix', path='/scripts', target='content')
```
- If result count = 0: DEAD CODE. The matrix exists but is never used during scoring.
- Credit in audits = 0 for production use, regardless of how well-structured the matrix is.

### Step 5: Verify Coupling Sum Consistency
```sql
SELECT COUNT(DISTINCT coupling_sum) FROM daily_scorecard WHERE twc_score IS NOT NULL;
-- Expected: 1 (the constant 6.775), unless second writer path detected
```
If more than one distinct value exists, this proves MULTIPLE writer paths.

## Verification Script
Use the automated script:
```bash
scripts/verify_interaction_matrix.py
```

## False-Alarm Prevention (Critical)
When you see a report claiming "all pairs invalid" or "CRITICALLY deviant from spec" with deltas >0.40, the auditor is likely comparing DB values (0.20/0.15/0.20/0.25) against the rejected heuristics (0.85/0.78/0.72/0.68). This is FALSE-ALARM. Always verify against canonical_coupling.py first.

**MANDATORY ENFORCEMENT:** When VERITAS-ALGO reports claim "all pairs invalid" or "CRITICALLY deviant from spec" with deltas >0.40, AUDIT-ALGO MUST re-verify using canonical_coupling.py as ground truth. The canonical_coupling.py output is the only authoritative reference.

## Example False-Alarm (2026-07-27)
VERITAS-ALGO's 2026-06-20 report claimed "❌ all 4 key pairs CRITICALLY deviant" with deltas >0.60. Independent verification ran canonical_coupling.py (output: "OK — 28 pairs, range 0.05-0.35") and confirmed DB values are CORRECT. The "spec" values were rejected heuristics — not the authoritative source.

## Graph Vocabulary (message-passing view) — added T-261021-0058
The interaction matrix is a weighted adjacency matrix over the 8 dimension-nodes; each of the 28 rows (C(8,2)) is one weighted edge. Canonical primer: `/<workspace>` (source: Distill 2021, DOI 10.23915/distill.00033).
- This verification is an **edge-level** graph task: each coupling edge is checked individually, never just the matrix shape.
- **Dead code = connectivity without message flow**: an edge exists only if messages (scoring reads) traverse it. Population without readers is topology with no traffic.
- **Frozen matrix = static topology**: edge weights that never re-estimate (topology as photograph, not process — QA-MICRO-REVIEW-1).
- **Permutation invariance**: verification semantics must not depend on dimension ordering (pairs are canonicalized dim1 < dim2 for exactly this reason).

## References
- Canonical source verification: `organism/canonical_coupling.py`
- Verification sequence reference: `references/interaction-matrix-verification-sequence.md`