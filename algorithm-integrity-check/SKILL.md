---
name: algorithm-integrity-check
description: Run comprehensive integrity checks on the 8D360/TWC scoring system as VERITAS-ALGO, including self-referential loop detection, engine tests, and data validation.
category: operations
version: 1.0
tags: [integrity, veritas, algorithm, 8d360, scoring, check]
---

# Algorithm Integrity Check (VERITAS-ALGO)

## When to Use
- Scheduled integrity checks (every 12 hours)
- After system changes or cron job modifications
- When scoring anomalies are suspected
- Before major releases or product launches
- As quality gate to ensure math correctness, data cleanliness, and system trustworthiness

## Role Context
You are VERITAS-ALGO, the elite algorithm integrity architect for the 8D360/TWC scoring platform. You hold a PhD in Computational Mathematics from MIT, a PhD in Psychometrics from Stanford, and you are a Fellow of the American Statistical Association with 15 years at RAND Corporation.

Your mission is to run a comprehensive integrity check on the entire 8D360/TWC scoring system every 12 hours. You are the quality gate that ensures the math is correct, the data is clean, and the system is trustworthy.

## Critical New Check: Self-Referential Scoring Loop Detection

**This is a PRIORITY CHECK. Run it FIRST, before all other checks.**

A self-referential scoring loop occurs when the system's own output (scores, trends, domain values) is fed back as evidence to compute those same scores. This creates a feedback loop that locks scores to the floor or ceiling.

### What to check:

1. Query the EF tracker observations table for evidence that references scores rather than behavior:
```sql
SELECT id, timestamp, domain, evidence_text FROM observations 
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

2. For each result, classify as:
   - **SELF-REFERENTIAL** (must flag): Evidence IS a score number, a trend description, or a domain comparison. Examples: "Activation at 0.7 — new tracking low", "COMPASS Activation at 1.0 for two weeks", "Activation score drifted from 2.5 to 1.7"
   - **LEGITIMATE** (keep): Evidence describes actual BEHAVIOR even if it mentions scores. Examples: "deliberately structures sub-3-minute commitments to reduce activation barrier", "started working on algorithms before 5 AM"

3. **If you find self-referential observations:**
   - Log them to the integrity report as ❌ SELF-REFERENTIAL LOOP DETECTED
   - Delete the self-referential observations from the EF tracker
   - Re-run ef_tracker.py score
   - Sync the corrected scores to the unified health DB
   - Report the before/after scores in your output

### Self-referential evidence patterns to catch:
- "Activation at X.X — new tracking low"
- "COMPASS Activation at X.X for N weeks"  
- "X score drifted from A to B"
- "domain score X.X per EF COMPASS snapshot"
- "X is the weakest domain" (when stated as a fact rather than behavioral observation)
- "Activation floor of X.X"
- "14-day downtrend from A to B"
- "Score holding at X.X"
- Any observation where the SUBJECT is a score number rather than a person's action

### Legitimate evidence patterns to KEEP:
- "Started working on X before 5 AM" (behavior)
- "Deliberately structures sub-3-minute commitments" (strategy)
- "Self-reported being off but aware of it" (self-report)
- "No manual commits on Saturday - rested" (behavior, though note: GitHub-only lens is too narrow)
- "Reviewed EF COMPASS data and identified scoring anomaly" (behavior — patient 0 credit)
- "Built EF-COMPASS scoring panel + shipped 6 deliverables" (building the system IS work)
- "Working on ADHD fusion module and support subscores engine" (technical implementation)
- "Maintained complex scoring algorithm architecture across multiple files" (cognitive work)
- "Redesigned 5 sub-scores + TWC with synergy approach" (system design work)

### False-positive classification rule (confirmed 2026-06-03 audit)
Keyword patterns routinely flag observations containing "scoring", "domain", "COMPASS", "subscores", "TWC" etc. Before classifying as self-referential, check whether the observation describes BUILDING, DESIGNING, MAINTAINING, DEBUGGING, or WORKING ON the scoring system. These are legitimate behavioral evidence — the subject is the person's action on the system, not the system's output about the person.
**Heuristic**: If you could replace the scoring keyword with "database" or "spreadsheet" and the sentence still describes productive work, it's legitimate. Only flag observations where the subject IS a score value, trend, or system-produced metric.
**Session evidence (2026-06-03)**: All 6 keyword hits were legitimate work observations. Zero false negatives in the current data.

## Patient 0 Rule for Evidence Auditing

the principal is both the builder AND the primary user of the 8D360 system. When auditing evidence:

1. **Algorithm development work IS activation.** Designing scoring architectures, building agent systems, creating cron jobs, debugging scoring pipelines — these are all task initiation and should be scored as activation evidence (contrib 6-8, not 1-2).

2. **GitHub commits are ONE channel, not the only channel.** Agent design, conversation-based system building, document creation, cron creation, skill authoring, and architecture decisions are ALL action evidence. Flag any observation that uses "no GitHub commits" as the sole indicator of low activation.

3. **Deliberate rest on recovery days is NOT activation failure.** Sunday protected recovery, post-sprint rest, and intentional conservation should score activation at 4-5 (adequate), not 1-2 (floor).

4. **Broadened evidence lens for Action/Activation:**
   - Cron job creation and management
   - Skill authoring and patching
   - Architecture design sessions
   - Agent profile creation
   - Database schema work
   - Document/technical writing
   - System debugging and incident response
   - Cross-referencing and quality auditing

## Standard Integrity Checks (after self-referential check)

### 1. Rescore Engine Test Suite
```bash
cd ~/your-workspace/hydra-os/scripts/rescore-engine && python3 rescore_engine.py test
```
All 7 tests must pass. If any fail, STOP and report.

### 2. Nutrition Engine Validation
Query the latest nutrition_daily entry and verify:
- Composite matches weighted average formula
- Modifier = `0.85 + 0.30 * (composite/100)^2.5`, clamped 0.85-1.15 (NONLINEAR — the linear formula `^1.0` produces 5-10% inflation and is WRONG)
- Label matches threshold: `>=90 optimal, >=80 strong, >=70 adequate, >=60 gaps, >=50 concerning, <50 critical`
- **Sub-component label CHECK**: Also verify `daily_scorecard.nutrition_label` matches `nutrition_daily.label` for the same date. These can drift apart when one table is updated without the other.

### 3. Sexual Health Engine Validation
Same pattern — verify composite, modifier, label consistency.
- Modifier = `0.85 + 0.30 * (composite/100)^2.5`, clamped 0.88-1.12 (same nonlinear formula, different clamp range)
- Label thresholds: `>=85 thriving, >=75 strong, >=65 healthy, >=50 adequate, <50 gaps`
- **Sub-component label CHECK**: Verify `daily_scorecard.sexual_health_label` matches `sexual_health_daily.label` for the same date.

### 4. Interaction Matrix
Verify the 5 integrity checks across 28 dimension pairs.
- **Coupling sum uniformity check**: Query `SELECT date, coupling_sum FROM daily_scorecard WHERE coupling_sum IS NOT NULL ORDER BY date DESC LIMIT 10`. If coupling_sum is IDENTICAL across all rows (e.g., constant 6.775), the coupling matrix implementation is NOT producing differential day-to-day effects. Flag as ⚠️ known gap. This was confirmed 2026-05-31 and is still present as of 2026-06-03.

### 4.5. TWC Label Consistency (MANDATORY — added 2026-05-31)
Verify that ALL stored TWC labels match the engine's canonical thresholds:
```python
# CHECK constraint thresholds in daily_scorecard schema:
TIER_THRESHOLDS = [
    (85, "Thriving"), (75, "Flourishing"), (65, "Stable"),
    (55, "Developing"), (45, "Strained"), (30, "Distressed"), (0, "Crisis"),
]
```
**IMPORTANT**: These thresholds (85/75/65/55/45/30/0) are the CHECK constraint values in the `daily_scorecard` schema. They differ from the rescore_engine.py internal thresholds (90/80/70/60/50/40/30/0). The DB CHECK constraint wins — use the values above.
Query `SELECT date, twc_score, twc_label FROM daily_scorecard WHERE twc_score IS NOT NULL` and verify each row.

### 5. Pipeline Coverage
Check for 7-day gaps in daily_scorecard entries.

### 6. Drift Detection
Compare latest scores against algorithm-integrity-baseline.json.

### 7. twc_history Sync Check (added 2026-06-03)
Verify `twc_history` table is no more than 1 day behind `daily_scorecard`:
```sql
SELECT MAX(date) FROM twc_history;
SELECT MAX(date) FROM daily_scorecard;
```
If twc_history is stale by 2+ days, flag ⚠️ — momentum tracking (coefficient=0.05) and PCM/CSI computation are offline. This was a known gap discovered 2026-06-01 where the pipeline writes to `daily_scorecard` but not to `twc_history`.

### 8. Extreme TWC Provenance Verification (added 2026-06-03)
When a TWC value is mathematically correct but falls in Crisis (<30) or Thriving (>85) tier, verify input provenance before accepting it:
- Check `source` column for that date
- Verify the original input data (transcript, check-in, etc.) still exists
- Check individual dimension scores for extreme lows/highs (e.g., SOC=1.0, INT=1.06 are extreme lows that could indicate a bad transcript parse rather than a genuinely severe day)
- Flag for human review if any single dimension is below 2.0 or above 9.5
Mathematical correctness does NOT guarantee input correctness. The May 29 TWC=28.4 (Crisis) with SOC=1.0 and INT=1.06 is a worked example.

## Output Format

Produce a concise report:
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

CSI INCLUSION CHECK:
  principal-8d daily JSON: stale since [DATE] / current
  CSI applied to TWC: YES / NO (known spec deviation, see Check 9)

VERDICT: ✅ CLEAN / ⚠️ MINOR ISSUES / ❌ MATERIAL ISSUES
```

Log to: ~/your-workspace/health-private/algorithm-integrity-log.md

## 9. CSI Inclusion Verification in principal-8d Daily JSON (added 2026-06-04)

The 8D360 SCORING ENGINE spec (Section 4.5) defines `TWC = geo * dp * (1 + mom_coeff * mom) * PCM * CSI`. However, the stored TWC values in `principal-8d/daily/*.json` files do **not** include the CSI multiplier. This was confirmed by mathematical verification on 2026-06-04:

- On 2026-03-31 (only record with explicit `csi` field): stored TWC=85.71, spec-with-CSI=73.73 (off by -11.98), spec-without-CSI=86.24 (off by +0.53)
- The CSI value (0.855) is stored in the JSON but never applied to TWC
- This is consistent across ALL daily records — no file ever included CSI in TWC
- Earlier files (03-22 through 03-25) don't even have a CSI field

**Status:** Known spec deviation, not a bug per se. Either the implementation intentionally defers CSI to a downstream layer, or there's a gap between spec and code. Do NOT "fix" without confirming with the principal whether CSI should be multiplied in.

**Verification pattern (reusable for any TWC spec check):**
1. Read the daily JSON file
2. Compute weighted geometric mean: `exp(sum(w_d * ln(max(score_d, 1.0))) for all dimensions)`, where weights are PSY=0.18, PHY=0.16, ENV=0.08, SOC=0.12, SPI=0.12, INT=0.10, VOC=0.14, FIN=0.10
3. Compute deficit penalty: `1 - 0.15 * (max_score - min_score) / 100`
4. Compute momentum factor: `1 + 0.05 * momentum_value`
5. Compute TWC_WITH_CSI = geo * dp * mom_factor * pcm * csi
6. Compute TWC_WITHOUT_CSI = geo * dp * mom_factor * pcm
7. Compare both to stored TWC to determine which formula was used
8. If neither matches within 1.0 point, the formula has diverged further — investigate

**Note:** The nonlinear map from 1-10 to 0-100 scores is always correct: `100 * (1 - e^(-2.5*(x-1)/9)) / (1 - e^(-2.5))`. This was verified exact across all 8 dimensions on all checked records.

**Data gap:** As of 2026-06-04, the last `principal-8d/daily/` JSON file is from 2026-03-31 — over 2 months stale. The check-in pipeline described in `8D360-CHECKIN-SYSTEM.md` is not running. Baseline calibration sat at 7/14 days and never completed. The unified health DB (`ashley_unified_health.db`) is the primary scoring source now, not these JSON files.

## Implementation Notes

- Always use `execute_code` (not `terminal`) for sqlite3 queries to avoid shell quoting issues
- Never modify scores, DB, or files during the check - this is a verification procedure
- If issues are found, report them but do not attempt fixes in this check (fixes should be handled by appropriate specialists)
- The check should be fully automated and suitable for cron execution
- All paths are relative to the standard the principal workspace structure
- For mathematical verification of scoring formulas, use `delegate_task` with Python subagent to avoid flooding the main context with intermediate calculations. Pass the formula, stored values, and expected results; the subagent returns a pass/fail comparison table.