# Detailed Integrity Check Procedure

This document provides an expanded version of the VERITAS-ALGO integrity check procedure with additional context and guidance.

## Overview
The VERITAS-ALGO integrity check should be performed every 12 hours to ensure algorithmic integrity of the 8D360/TWC scoring system. This procedure combines self-referential loop prevention, engine testing, data validation, and patient-specific auditing.

## Detailed Procedure

### 1. Self-Referential Loop Check (PRIORITY)
**Purpose**: Prevent feedback loops where system outputs are used as inputs, causing scores to lock to floor/ceiling.

**Steps**:
1. Query the EF tracker observations table for evidence containing score-related terms:
   ```sql
   SELECT id, timestamp, domain, evidence_text 
   FROM observations 
   WHERE evidence_text LIKE '%score%' 
      OR evidence_text LIKE '%COMPASS%' 
      OR evidence_text LIKE '%domain%'
      OR evidence_text LIKE '%floor%' 
      OR evidence_text LIKE '%downtrend%'
      OR evidence_text LIKE '%drift%'
      OR evidence_text LIKE '%per EF%'
      OR evidence_text LIKE '%tracking low%'
      OR evidence_text LIKE '%weakest domain%'
   ```
2. For each result, classify using the false-positive classification rule:
   - **SELF-REFERENTIAL** (must flag): Evidence IS a score number, trend description, or domain comparison
     - Examples: "Activation at 0.7 — new tracking low", "COMPASS Activation at 1.0 for two weeks", "Activation score drifted from 2.5 to 1.7"
   - **LEGITIMATE** (keep): Evidence describes actual BEHAVIOR even if it mentions scores
     - Examples: "deliberately structures sub-3-minute commitments to reduce activation barrier", "started working on algorithms before 5 AM"
   - **False-positive rule**: If observation describes BUILDING, DESIGNING, MAINTAINING, DEBUGGING, or WORKING ON the scoring system, it's legitimate behavioral evidence — do not flag as self-referential
3. If self-referential observations found:
   - Log them to the integrity report as ❌ SELF-REFERENTIAL LOOP DETECTED
   - Delete the self-referential observations from the EF tracker
   - Re-run `ef_tracker.py score`
   - Sync corrected scores to unified health DB
   - Report before/after scores in your output

### 2. Engine Test Verification
**Purpose**: Ensure all scoring engines are functioning correctly before trusting their output.

**Steps**:
1. Run rescore engine tests:
   ```bash
   cd ~/your-workspace/hydra-os/scripts/rescore-engine && python3 rescore_engine.py test
   ```
   - All 7 tests must pass
2. Run nutrition engine tests:
   ```bash
   cd ~/your-workspace/hydra-os/scripts && python3 test-nutrition-engine.py
   ```
3. Run sexual health engine tests:
   ```bash
   cd ~/your-workspace/hydra-os/scripts && python3 test-sexual-health-engine.py
   ```
4. If any test fails, STOP and report — do not proceed with other integrity checks

### 3. Data Integrity Validation
**Purpose**: Verify that stored data matches expected values from canonical formulas.

#### Modifier Staleness Check
**Purpose**: Ensure nutrition and sexual health modifiers are computed correctly from composites.

**Steps**:
1. For nutrition: Verify `modifier = 0.85 + 0.30 * (composite/100)^2.5`, clamped to 0.85-1.15
2. For sexual health: Verify `modifier = 0.85 + 0.30 * (composite/100)^2.5`, clamped to 0.88-1.12
3. For any mismatches >0.005, recompute from composite and update both tables

#### TWC Recomputation Check
**Purpose**: Ensure stored TWC matches computed value from 8D dimensions.

**Steps**:
1. For each day with stored TWC:
   - Skip if any 8D dimension is NULL
   - Get stored modifier values (use 1.0 if NULL)
   - Compute base TWC: `(psy*0.18 + phy*0.16 + env*0.11 + soc*0.12 + spi*0.10 + int*0.13 + voc*0.11 + fin*0.09) * 10`
   - Compute stacked modifier: `sqrt(nutrition_modifier * sexual_health_modifier)`
   - Compute expected TWC: `base_twc * stacked_modifier`
   - If |stored - expected| > 0.2, flag as mismatch
2. For mismatches, recompute from corrected modifiers and update TWC

#### Interaction Matrix Validation
**Purpose**: Ensure coupling coefficients match proprietary specification.

**Steps**:
1. Extract key coupling values:
   ```sql
   SELECT dim1, dim2, value 
   FROM interaction_matrix 
   WHERE (dim1='PSY' AND dim2='INT') OR (dim1='INT' AND dim2='PSY')
      OR (dim1='PHY' AND dim2='VOC') OR (dim1='VOC' AND dim2='PHY')
      OR (dim1='SOC' AND dim2='SPI') OR (dim1='SPI' AND dim2='SOC')
      OR (dim1='ENV' AND dim2='PHY') OR (dim1='PHY' AND dim2='ENV');
   ```
2. Compare to specification:
   - PSY↔INT/INT↔PSY: Expected 0.85
   - PHY↔VOC/VOC↔PHY: Expected 0.78
   - SOC↔SPI/SPI↔SOC: Expected 0.72
   - ENV↔PHY/PHY↔ENV: Expected 0.68
3. Flag any deviation >0.10 as implementation gap

#### Pipeline Coverage Check
**Purpose**: Ensure sufficient data coverage for reliable scoring.

**Steps**:
1. Check for 7+ day gaps in daily_scorecard TWC scores
2. If gaps exist, investigate and process available evidence sources
3. Missing days should remain blank only if no evidence exists
4. Calculate percentage of days with real scores in last 60 days
5. If <50%, investigate scoring pipeline issues

#### Phantom TWC Check
**Purpose**: Remove TWC scores not backed by legitimate 8D data.

**Steps**:
1. Check for TWC values on carryforward rows without legitimate 8D data
2. NULL out phantom TWC unless 8D values are legitimate for that date
3. Investigate rows with source set but missing 8D data

### 4. Patient 0 Evidence Audit
**Purpose**: Ensure the principal's algorithm work is properly counted as activation evidence.

**Steps**:
1. Review activation/action observations for:
   - Algorithm development work counting as activation evidence
   - Broad evidence lens beyond GitHub commits
   - Distinguishing deliberate rest from activation failure
   - Proper classification of system work vs score reference
2. Apply false-positive classification to GitHub observations
3. Ensure algorithm building, company-building, and scoring-methodology work count as real daily activity

### 5. Drift Detection
**Purpose**: Detect significant changes in scoring system behavior over time.

**Steps**:
1. When algorithm-integrity-baseline.json exists:
   - Compare latest TWC score against baseline value
   - Flag significant deviations (>1.0 points) for investigation
2. Consider volatility adjustment: if stdev >15, trends may be noise

### 6. Integrity Logging
**Purpose**: Record findings in a standardized format for tracking and trending.

**Steps**:
1. Record findings in `algorithm-integrity-log.md` using the standard format:
   ```
   VERITAS-ALGO INTEGRITY REPORT — [DATE TIME]
   ================================================

   SELF-REFERENTIAL LOOP CHECK:
     Observations scanned: N
     Self-referential found: N ❌
     Deleted: N
     Score corrections: [before] → [after]

   ENGINE TESTS:
     Rescore engine: ✅ 7/7 / ❌ N failures
     Nutrition engine: ✅ / ❌
     Sexual health engine: ✅ / ❌

   DATA INTEGRITY:
     Pipeline coverage: N/N days
     Drift from baseline: +X.X / -X.X
     Interaction matrix: ✅ all pairs valid / ❌

   PATIENT 0 AUDIT:
     Activation observations reviewed: N
     Under-scored work detected: Y/N
     GitHub-only lens detected: Y/N

   VERDICT: ✅ CLEAN / ⚠️ MINOR ISSUES / ❌ MATERIAL ISSUES
   ```
2. Log to: `~/your-workspace/health-private/algorithm-integrity-log.md`

## Interpretation Guide
See `scripts/interpret-integrity-results.md` for guidance on interpreting results and determining appropriate actions.

## Frequency
This procedure should be run every 12 hours (bi-daily) as part of the VERITAS-ALGO audit protocol.

## Automation Considerations
While this procedure can be manual, consider automating repetitive components:
- Database queries can be scripted
- Engine test verification can be automated
- Report generation can be templated
However, the self-referential loop check and patient 0 audit benefit from human judgment.

## References
- VERITAS-ALGO audit protocol
- Health Scoring Daily Pipeline skill: Database Integrity Verification Procedure section
- EF COMPASS Self-Referential Loop Prevention (learned 2026-05-27)
- Proprietary TWC Scoring skill: Coupling matrix implementation gap