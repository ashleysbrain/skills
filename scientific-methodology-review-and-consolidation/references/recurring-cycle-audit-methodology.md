# Recurring Methodology Quality Gate — Cycle Audit Methodology

For recurring quality-gate cron jobs (e.g., the specialist engine `bb2fc380f91d`, every 4h), use this cycle-over-cycle methodology. The goal: each cycle builds on the last rather than starting from scratch, and persistent findings get escalated until resolved.

## Cycle Audit Sequence

### Step 1: Read previous cycle output
```bash
# Find the most recent output file for the cron job
ls -t <agent-home>/cron/output/<JOB_ID>/*.md | head -1
```
Extract: every numbered finding, its severity, its VETO status, and the integrity score table.

### Step 2: Verify each finding's resolution status
For each finding from the previous cycle, run the specific diagnostic to check if it was fixed. **Do not assume resolution — verify.**

### Step 3: Compute the fix rate
`fix_rate = findings_resolved / total_findings`. If fix_rate = 0%, that itself is a finding (organism is not addressing flagged issues). Track this across cycles.

### Step 4: Scan for new artifacts since last cycle
```bash
find ~/your-workspace <agent-home> -maxdepth 6 -type f -newermt "<LAST_CYCLE_TIME>" \( -name "*.md" -o -name "*.py" -o -name "*.json" \) | grep -viE "node_modules|\.git/|__pycache__"
```
Check for: new manuscripts, new engine code, new reference files, updated integrity logs.

### Step 5: Escalate findings that worsened
If a finding from the previous cycle has new evidence showing it's worse (e.g., single-level problem becomes two-level problem), escalate the severity and expand the VETO.

### Step 6: Check agent pipeline status
Verify whether upstream agents (Garfield/Pearl/Simon/Asimov or equivalent search/causal/synthesis/writing pipeline) produced output this cycle. A stalled pipeline is itself a finding.

### Step 7: Compute integrity score with deltas
Score each dimension, compare to previous cycle, compute delta. A declining score is a signal that the organism is backsliding.

## Diagnostic Query Bank

Verified queries for common the specialist engine finding types. Run these each cycle to check status.

### Dead coupling code (coupling_sum constancy)
```python
import sqlite3
conn = sqlite3.connect('~/your-workspace/health-private/ashley_unified_health.db')
c = conn.cursor()
c.execute("SELECT MIN(coupling_sum), MAX(coupling_sum), COUNT(DISTINCT coupling_sum) FROM daily_scorecard WHERE coupling_sum IS NOT NULL")
r = c.fetchone()
print(f"FIXED: coupling varies [{r[0]}, {r[1]}]" if r[2] > 1 else f"STILL DEAD CODE: coupling={r[0]} constant")
```

### Interaction matrix values vs spec
```sql
-- Spec: PSY↔INT=0.85, PHY↔VOC=0.78, SOC↔SPI=0.72, ENV↔PHY=0.68
-- If actual values are 60-80% below spec → placeholder values, not scientific coefficients
SELECT dim1, dim2, value FROM interaction_matrix ORDER BY value DESC LIMIT 5;
```

### Label threshold reconciliation
Check if engine test failures persist:
```bash
tail -30 ~/your-workspace/health-private/algorithm-integrity-log.md | grep -E "LABEL MISMATCH|PASS|FAIL"
```

### Kuramoto RNG seeding (reproducibility)
```bash
# Check production model (not tests) for seed
grep -n "seed\|np.random" <engine_path>/src/kuramoto/model.py
# If np.random used without seed and noise_std > 0 → non-reproducible
```

### Scale-free network falsifiability
```bash
# Check if proper KS goodness-of-fit replaced the -0.7 correlation heuristic
grep -n "0.7\|ks_test\|KS\|powerlaw\|clauset" <engine_path>/src/entropy/scale_free.py
```

### Pipeline coverage
```sql
SELECT COUNT(*) FROM daily_scorecard WHERE twc_score IS NOT NULL AND date >= date('now', '-30 days');
-- If < 50% of days scored → underpowered for longitudinal claims
```

### Marketing gate bypass (Check 9)
```bash
# Scan for new external-facing documents since last cycle
find ~/your-workspace -maxdepth 6 -type f -newermt "<LAST_CYCLE_TIME>" \
  \( -name "*one-pager*" -o -name "*positioning*" -o -name "*social-media*" \
     -o -name "*marketing*" -o -name "*brief*" -o -name "*investor*" \) \
  | grep -viE "node_modules|\.git/"

# For each document found, cross-reference claims against audit findings:
# 1. Extract performance claims → check against metrics.json (Check 2)
# 2. Extract "cannot X" claims → check for bounded ≠ safe (Check 8)
# 3. Extract named techniques → grep codebase (Check 3)
# 4. Extract coupling/interaction claims → check DB coupling_sum (Finding 6/8)
# 5. Check for "no hedging" voice instructions (compounds all violations)
#
# Build violation catalog: document_line × claim_text × violated_check × evidence
# Issue categorical VETO if multiple claims violate multiple triggers.
```

## Finding Escalation Framework

| Condition | Action |
|-----------|--------|
| Finding unresolved for 1 cycle | Note "unchanged" in status table |
| Finding unresolved for 3+ cycles | Escalate severity by one level |
| Finding unresolved for 5+ cycles | Add to "persistent failure" list; flag to director as process breakdown |
| Finding worsens (new evidence) | Escalate severity; expand VETO scope |
| Finding resolved | Verify with diagnostic query; note "RESOLVED" with cycle |
| Finding's broken claims appear in external-facing materials | Issue categorical VETO on those materials; flag as integrity crisis |
| Marketing materials instruct removing scientific hedging | Flag as compounding violation; add to voice-guide audit checklist |

## Integrity Scoring Rubric (7 Dimensions)

| Dimension | What It Measures | Score Guide |
|-----------|-----------------|-------------|
| Falsifiability | Can claims be refuted by observation? | 10=every claim has a falsification condition; <5=core claims unfalsifiable |
| Reproducibility | Same inputs → same outputs? | 10=fully seeded/deterministic; <5=active non-determinism in production |
| Bias detection | Are known biases accounted for? | 10=independent calibration verified; <5=internal QA inflation uncorrected |
| Transparency | Are limitations honestly disclosed? | 10=all gaps documented; <5=gaps hidden or implied resolved |
| FAIR compliance | Findable, Accessible, Interoperable, Reusable? | 10=full reproducibility package; <5=no seed/code/data availability |
| Ethical compliance | IRB, consent, COI, demographic bias? | 10=full ethical review; <5=missing IRB/consent/bias review |
| **Overall** | **Weighted mean** | **Publication threshold: 7.0** |

## VETO Trigger Management

Maintain a numbered list of active VETO triggers. Each trigger has:
- Finding number it derives from
- Scope (what outputs are blocked)
- Lift condition (what must be true to remove)

When a finding escalates, expand the corresponding VETO's scope. When a finding resolves, verify and lift the VETO.

**Categorical VETO on document sets:** When a finding reveals that multiple claims from a single document or document set (e.g., an entire marketing-sprint directory) each violate different VETO triggers, issue a categorical VETO on the ENTIRE document set rather than individual claim-level vetoes. This prevents the "whack-a-mole" problem where one claim is fixed but twelve others from the same voice guide remain. The lift condition for a categorical VETO must include a voice-guide or process audit, not just individual claim fixes.

## Worked Example: 2026-06-13 Cycles

### 13:40 Cycle
7 findings from prior cycle. Fix rate: 0%. One finding escalated (coupling matrix dead code → interaction matrix placeholder values, two-level failure). Overall integrity score declined 5.5→5.0. Four active VETO triggers (expanded from 3).

### 17:38 Cycle
8 prior findings still unresolved (0% fix rate). Two new findings: Finding 9 (marketing sprint violated ALL 4 active VETO triggers — 12 catalogued violations across 3 investor/public-facing documents), Finding 10 (research synthesis partially unstuck pipeline but is aspirational framework, not validated results). Overall integrity score declined 5.0→4.5. Five active VETO triggers (expanded from 4). NEW categorical VETO on entire marketing-sprint directory.

Key lesson: the most dangerous finding was not a new methodological flaw — it was the organism packaging existing unresolved flaws into external-facing marketing materials. Twelve claims in investor and social-media documents mapped directly to unresolved audit findings. The quality gate had been covering manuscripts and code, but marketing materials bypassed it entirely. See Check 9 in the parent SKILL.md and `references/marketing-claim-violation-detection.md`.
