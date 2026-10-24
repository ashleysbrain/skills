# VERITAS-ALGO Integrity Check Procedure

This document outlines the comprehensive integrity check procedure for the 8D360/TWC scoring system, designed to be run every 12 hours as the quality gate for scoring correctness, data cleanliness, and system trustworthiness.

## Procedure Overview

The integrity check consists of eight sequential steps, with the self-referential loop check as the highest priority. Each step builds upon the previous, and critical issues found in early steps may halt the procedure.

### 1. Self-Referential Loop Check (Priority)
**Purpose**: Detect and break feedback loops where scoring system outputs are fed back as behavioral evidence.

**Steps**:
- Query EF tracker `observations` table for evidence containing score-related keywords:
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
- For each result, classify as:
  - **SELF-REFERENTIAL** (must flag): Evidence IS a score number, trend description, or domain comparison
  - **LEGITIMATE** (keep): Evidence describes actual behavior even if mentions scores
- Apply false-positive classification: If observation describes BUILDING, DESIGNING, MAINTAINING, DEBUGGING, or WORKING ON the scoring system, it's legitimate behavioral evidence
- Delete self-referential observations
- Re-run `ef_tracker.py score`
- Sync corrected scores to unified DB using `sync_ef_to_unified.py`
- Record before/after EF COMPASS overall scores for affected dates

### 2. Engine Test Verification
**Purpose**: Ensure scoring engines produce correct outputs given known inputs.

**Steps**:
- Run rescore engine test suite: 
  ```bash
  cd ~/your-workspace/hydra-os/scripts/rescore-engine && python3 rescore_engine.py test
  ```
  All 7 tests must pass.
- (Optional) Run nutrition and sexual health engine tests if available

### 3. Nutrition Engine Validation
**Purpose**: Verify nutrition scoring components are correctly computed and labeled.

**Steps**:
- For the most recent `nutrition_daily` entry:
  - Validate `modifier` matches canonical formula: `0.85 + 0.30 * (composite/100)^2.5` (clamped 0.85-1.15)
  - Validate `label` matches composite thresholds:
    - ≥90 → optimal
    - ≥80 → strong  
    - ≥70 → adequate
    - ≥60 → gaps
    - ≥50 → concerning
    - <50 → critical
- Note: Composite validation against raw inputs requires accessing the original nutrition engine with stored raw inputs (protein_grams, meals_count, water_oz, etc.)

### 4. Sexual Health Engine Validation
**Purpose**: Verify sexual health scoring components are correctly computed and labeled.

**Steps**:
- For the most recent `sexual_health_daily` entry:
  - Validate `modifier` matches canonical formula: `0.85 + 0.30 * (composite/100)^2.5` (clamped 0.88-1.12)
  - Validate `label` matches composite thresholds:
    - ≥85 → thriving
    - ≥75 → strong
    - ≥65 → healthy
    - ≥50 → adequate
    - <50 → gaps
- Note: Composite validation against raw inputs requires accessing the original sexual health engine with stored raw inputs

### 5. Interaction Matrix Validation
**Purpose**: Verify dimensional coupling coefficients are within expected bounds.

**Steps**:
- Query `interaction_matrix` table:
  ```sql
  SELECT dim1, dim2, value FROM interaction_matrix
  ```
- All values should be between 0.05 and 0.35 (inclusive)
- Verify `coupling_sum` in `daily_scorecard` is constant (historically 6.775)

### 6. Pipeline Coverage Check
**Purpose**: Identify gaps in scoring data that may indicate pipeline failures.

**Steps**:
- Query distinct dates from `daily_scorecard`:
  ```sql
  SELECT date FROM daily_scorecard WHERE date IS NOT NULL ORDER BY date
  ```
- Calculate gaps between consecutive dates
- Flag gaps of 7 or more days as potential pipeline failures
- Calculate coverage ratio: (days with scores) / (total days in date range)
- **Critical**: Do not backfill automatically. Instead, for missing dates:
  1. Check for available evidence sources (standup transcripts, voice memos, etc.)
  2. Process them through the scoring pipeline before considering the day complete
  3. Leave blank only if no evidence exists

### 7. Drift Detection
**Purpose**: Identify significant deviations from established baselines.

**Steps**:
- If `algorithm-integrity-baseline.json` exists:
  - Load baseline values (should include TWC and ideally all 8D dimensions)
  - Compare with most recent `daily_scorecard` entry
  - Flag deviations exceeding thresholds (e.g., TWC drift > 5 points)
  - Investigate root causes before accepting new values as valid

### 8. Patient 0 Evidence Audit
**Purpose**: Ensure algorithm development and system work is properly scored as behavioral evidence.

**Steps**:
- Review EF tracker `observations` from past 7 days:
  - Algorithm development work (designing scoring architectures, building agent systems, creating cron jobs, debugging scoring pipelines) SHOULD score as activation/action evidence (contribution 6-8)
  - GitHub commits are ONE channel for evidence - also check for:
    * Cron job creation and management
    * Skill authoring and patching
    * Architecture design sessions
    * Agent profile creation
    * Database schema work
    * Document/technical writing
    * System debugging and incident response
    * Cross-referencing and quality auditing
  - Detect under-scored work: Algorithm-related observations with low Activation/Action/Effort/Focus scores
  - Detect GitHub-only lens: Observations using lack of GitHub commits as sole evidence of low activation

## Key Learnings from Procedure Application

- **Label mismatches**: Nutrition and sexual health labels may be off by one threshold level (e.g., composite 79.0 labeled "strong" instead of "adequate")
- **Pipeline coverage gaps**: Persistent issue requiring evidence-source-driven processing rather than automatic backfill
- **Under-scored algorithm work**: System development activities often not properly credited as behavioral evidence
- **GitHub-only lens**: Over-reliance on commit counts misses other valid evidence channels

## References
- Health Scoring Daily Pipeline skill: Database Integrity Verification Procedure section
- EF COMPASS Self-Referential Loop Prevention (learned 2026-05-27)
- VERITAS-ALGO integrity check findings recorded in algorithm-integrity-log.md