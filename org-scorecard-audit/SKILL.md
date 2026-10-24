---
name: org-scorecard-audit
description: Independent READ-ONLY audit of an organizational TWC scorecard by a second agent/model. Cross-references raw evidence against claimed scores to verify the scorer scored from evidence, not vibes. Runs on a different model than the primary scorer by design.
category: operations
version: 1.0
---

# Organizational TWC Scorecard Audit

Independent READ-ONLY verification of an organizational TWC scorecard. The auditor checks whether the primary scorer (e.g., STRATEGOS) scored from raw evidence or from assumptions, verifies the TWC math, and checks whether any fix agents produced real results.

## When to Use
- A cron job is configured to run an independent audit of the org scorecard
- You need to verify a scorecard produced by another agent/model
- The primary scorer (STRATEGOS or equivalent) has produced output that needs second-opinion verification
- Leadership needs confidence that scores are evidence-based, not inflated

## Core Rules
1. **READ-ONLY**: Never modify scores, never spawn fix agents, never edit files
2. **Different model**: Audits should run on a different model than the primary scorer to catch model-specific blind spots
3. **Evidence-first**: Every dimension score must be independently verified against raw evidence, not just quoted from the report
4. **No credit for plans**: If the scorer gave VOC=7 because "pricing model exists," dispute it. Plans are not execution.
5. **No credit for carry-forward scores**: If dimensions haven't been freshly scored, flag it

## Audit Sequence

### Step 1: Locate the Primary Scorer's Output
Search for the most recent org scorecard output. Check:
- `/<workspace>` for `*org*`, `*scorecard*` files
- `/<workspace>` for scorecard files
- `/<workspace>` for recent memory
- Cron job logs in `/<workspace>`
- Delivery queue: `/<workspace>` (especially failed/ subdirectory)
- Conversation archives: `/<workspace>`
- OpenClaw workspace memory: `/<workspace>` (sometimes contains scorecard summaries)

**If no scorecard exists**: Report "STRATEGOS output not found" as the primary finding. An org scorecard system that isn't producing scorecards is itself a PHY/VOC signal indicating broken feedback loops or missing organizational self-awareness.

### Step 2: Extract Claims
From the scorecard, extract for each dimension:
- The score (1-10)
- The evidence cited
- The root cause diagnosis (if any)
- The fix agent spawned (if any)

### Step 3: Independently Verify Each Dimension

For EACH of the 8 dimensions, gather your OWN evidence and compare:

#### PHY (Operational Health)
```python
# Cron fleet health
import json
with open('/<workspace>') as f:
    states = json.load(f).get('jobs', {})
ok = sum(1 for v in states.values() if v.get('state', {}).get('lastStatus') == 'ok')
err = sum(1 for v in states.values() if v.get('state', {}).get('lastStatus') == 'error')

# Website reachability
# curl -s -o /dev/null -w '%{http_code}' https://divinityscience.com --max-time 10
# curl -s -o /dev/null -w '%{http_code}' https://qubit.divinityscience.com --max-time 10
# HTTP 000 on product subdomain = PHY at most 3.0 regardless of other evidence
```

#### PSY (Leadership/Cognitive Health)
```python
# Founder EF Compass
import sqlite3
db = '/<workspace>'
conn = sqlite3.connect(db)
c = conn.cursor()
c.execute("SELECT date, activation, self_monitoring, compass_overall FROM ef_compass_daily ORDER BY date DESC LIMIT 7")
# Activation < 1.0 = paralysis risk, direct org PSY input
```

#### VOC (Productivity/Market)
- Check PRODUCT-STATUS.md: are products "ready" but never uploaded?
- Check Gumroad/Stripe: any evidence of actual transactions?
- Check git log for shipping activity

#### FIN (Financial)
- $0 revenue = FIN scored on runway/sustainability only, not "revenue architecture"
- Revenue docs from months ago = design documents, not evidence of revenue
- OpenRouter credit exhaustion (402 errors) = direct FIN signal

#### INT (Intellectual)
- Check file modification recency in `intel/your-org/`
- 0 files modified in 30 days = INT stagnation signal
- Papers in perpetual draft (v20+, v30+) without submission = INT is potential, not output

#### ENV, SOC, SPI
- ENV: workspace structure, config freshness, gateway log patterns
- SOC: agent roster count vs. actually functional agents
- SPI: mission clarity, research-to-product coherence

### Step 4: Verify TWC Math

Recompute TWC from the 8 dimension scores using the proprietary formula:
- Weights: PSY=0.15, PHY=0.15, ENV=0.10, SOC=0.10, SPI=0.10, INT=0.15, VOC=0.15, FIN=0.10
- Coupling pairs: PSY-INT=0.85, PHY-VOC=0.78, SOC-SPI=0.72, ENV-PHY=0.68
- Use geometric mean normalization (NOT raw products)
- Apply efficiency cap at 8.5

**Note**: These are the fleet-agent κ values used for ORG scoring. The human personal scoring calculator.py uses MUCH LOWER values (PSY↔INT=0.30, etc.). Make sure you're using the right set for the right context.

**Critical math errors to flag**:
- Raw coupling products used as additive terms (massively inflates TWC)
- Simple average instead of weighted sum
- Missing coupling modifier entirely

### Step 5: Verify Fix Agent Results
If the primary scorer spawned fix agents, check:
- Did FORGE actually fix the infra issue?
- Did the revenue agent produce a real plan or just a document?
- Can you confirm the fix by re-checking the original problem?

### Step 6: Produce Audit Report

```
🔍 ORGANIZATIONAL HEALTH AUDIT — [DATE]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STRATEGOS Report: [timestamp reviewed, or "NOT FOUND"]
STRATEGOS claimed TWC: X.XX [Label]

DIMENSION VERIFICATION:
  PHY: STRATEGOS=X.X, Audit=X.X → ✅/⚠️/❌ [evidence summary]
  PSY: STRATEGOS=X.X, Audit=X.X → ✅/⚠️/❌ [evidence summary]
  ENV: STRATEGOS=X.X, Audit=X.X → ✅/⚠️/❌ [evidence summary]
  SOC: STRATEGOS=X.X, Audit=X.X → ✅/⚠️/❌ [evidence summary]
  SPI: STRATEGOS=X.X, Audit=X.X → ✅/⚠️/❌ [evidence summary]
  INT: STRATEGOS=X.X, Audit=X.X → ✅/⚠️/❌ [evidence summary]
  VOC: STRATEGOS=X.X, Audit=X.X → ✅/⚠️/❌ [evidence summary]
  FIN: STRATEGOS=X.X, Audit=X.X → ✅/⚠️/❌ [evidence summary]

TWC MATH: ✅ Correct / ❌ Error [description]

FIX AGENTS: ✅ Verified / ⚠️ Partial / ❌ Not verified

OVERALL VERDICT: ✅ CLEAN / ⚠️ MINOR DISCREPANCIES / ❌ MATERIAL ISSUES

[If any ❌]: Exact discrepancy and recommended correction.
```

## Scoring Calibration Guide

| Raw Evidence | Score Guidance |
|---|---|
| HTTP 000 on product URL | PHY ≤ 3.0 regardless of other evidence |
| $0 revenue, no Stripe wired | FIN ≤ 3.0 (score runway/sustainability only) |
| Founder activation < 1.0 for 3+ days | PSY ≤ 3.0 (ADHD paralysis signature) |
| 0 products shipped despite "ready" status | VOC ≤ 2.5 (plans without execution) |
| 0 research files modified in 30 days | INT ≤ 4.0 (stagnant intellectual capital) |
| 89%+ enabled fleet erroring | PHY ≤ 3.0, all dims ≤ 4.0 |
| Credits exhausted (402 errors) | FIN ≤ 2.0 (runway = 0) |
| Auth cascade in gateway log | PHY ≤ 2.5 (no working model path) |
| No scorecard system exists (no STRATEGOS cron) | PHY+VOC structural gap, produce independent baseline |
| NEXUS remediation runs but >50% fleet still erroring | PHY ≤ 3.0 (remediation ineffective, root cause unfixed) |
| All OK jobs on free-tier only, nvidia <5% success | FIN=1-2, PHY=2-3 (zero paid access, even free tier failing) |
| Personal TWC 5x+ higher than org TWC | Expected — don't let personal score inflate org scores |
| `search_files` returns 0 for known-existing files | Fall back to Python os.walk() |
| 4+ dimensions overscored by ≥0.5 each | Compound TWC overstatement of 25-30%; recheck each dimension independently |
| BLOCKERS.md stale >60 days | ENV −0.5 to −1.0 regardless of file activity count |
| Gateway `auth mode=none` + security warnings | ENV −0.5 (configuration rot, not just missing features) |
| 295+ model fallback errors in 5000 gateway log lines | PHY/FIN trajectory signal — infra degrading, not stable |
| 35+ enabled jobs with CE≥3 (out of 124) | PHY systemic failure, not transient — 28% of fleet chronically broken |
| Gumroad stores 404 × 2+ while products "ready" 70+ days | VOC ≤ 2.5 (zero execution, not partial) |

## Verdict Definitions
- **✅ CLEAN**: All dimension scores within ±0.5 of audit scores, TWC math correct, evidence cited is accurate
- **⚠️ MINOR DISCREPANCIES**: 1-2 dimensions off by >0.5, or minor math rounding issues, or fix agents partially verified
- **❌ MATERIAL ISSUES**: 3+ dimensions significantly miscalibrated, TWC math error, evidence misrepresented, or scorer gave credit for plans that haven't shipped

## Key Lessons Learned (from 2026-05-27/28 inaugural audits)

1. **STRATEGOS may not exist at all** — on the inaugural run, there was no STRATEGOS cron job configured in jobs.json. The absence of an org scorecard SYSTEM (not just output) is itself a critical PHY/VOC finding. When no scorecard exists, the auditor produces an independent baseline.
2. **`delegate_task` fails when OpenRouter credits are exhausted** — always gather evidence directly via terminal/read_file first; don't rely on subagents. The 402 error confirms FIN crisis.
3. **Personal scorecard ≠ org scorecard** — the principal's daily TWC (67.6/100 "Stable") ran 5x higher than the org TWC (1.35 "Crisis"). This gap is real and expected: personal health and org health are different systems. Don't let the personal score inflate org scores.
4. **Fleet health LATEST.json may not exist** — fall back to jobs-state.json direct parsing.
5. **The 8d-improvement-running-log.md is personal health, not org health** — it tracks the principal's EF compass and nutrition, not DS organizational metrics.
6. **Product subdomain dead (HTTP 000) while parent site live (HTTP 200)** = INT/SPI may have content but PHY/VOC are broken. Don't let the live parent site inflate scores.
7. **Domain health breakdown matters** — when "principal Briefs" has 27 erroring jobs, the executive is flying blind regardless of what other domains show.
8. **All 4 coupling pairs can be DRAG simultaneously** — when the org is in genuine crisis, the coupling modifier becomes large and negative (-1.67), pulling TWC well below the base weighted sum (3.02 → 1.35). This is correct behavior, not a math error.
9. **`daily_scorecard` DB column is `int_score`, not `intel`** — querying `intel` causes `no such column` error. The schema uses `int_score` for the Intellectual dimension.
10. **NEXUS auto-remediation running but ineffective ≠ positive signal** — logs showed "migrated 101 jobs" but 88% still erroring. Root cause (free-tier model failures) wasn't fixed. Don't credit remediation effort as ENV/PHY improvement.
11. **All OK jobs on free-tier only = FIN+PHY dual crisis** — nvidia/nemotron 1/47 OK (2%), z-ai/glm 13/72 OK (18%), llama 24/60 OK (40%). Zero paid model access. Score FIN=1-2, PHY=2-3.
12. **`search_files` may return 0 results for files that exist** — confirmed BLOCKERS.md and revenue files exist via `os.walk()` but search_files found nothing. When search_files is empty but you expect files, fall back to Python `os.walk()`.
13. **STRATEGOS TWC math errors are a real failure mode** — On June 1, 2026, STRATEGOS reported TWC=3.92 (Struggling) when the correct value was 3.24 (Crisis) — a 0.68-point error that changed the classification. Root cause: incorrect coupling computation (likely wrong dampening factor or omitted neutral baseline subtraction). The auditor MUST independently recompute TWC every time using the geometric-mean-normalized formula, not just spot-check a few dimensions. The TWC math verification step (Step 4) is NOT optional.
14. **Compound dimension overscoring compounds** — STRATEGOS overscored 4 dimensions (ENV +0.5, SOC +0.5, VOC +0.5, FIN +1.0). Each individual gap seemed minor, but collectively they produced TWC=3.92 vs audit TWC=2.83 — a 1.09-point (28%) overstatement. When you find 3+ dimensions overscored, the compound TWC error will always be larger than any single dimension error. Flag each one individually AND report the compound effect.
15. **ENV = workspace integrity, not workspace activity** — STRATEGOS scored ENV=4.0 because "76 files modified in 7 days." But: BLOCKERS.md was 69 days stale, gateway ran with `auth mode=none` and `allowInsecureAuth=true`, CF tunnel unconfigured for 35 days. Active file churn does NOT mean healthy configuration. Score ENV on: staleness of blockers, security config freshness, tunnel/auth status, not just file modification counts.
16. **Free-tier degradation trajectory, not static snapshot** — When the org runs on free-tier models AND those models are actively degrading (295 `model fallback decision: candidate_failed` entries in last 5000 gateway log lines), score FIN/PHY on the trajectory, not the current success rate. A 64% OK rate that produced 295 cascading failures in hours is heading to zero, not stable at 64%. The fallback error count is a quantifiable degradation metric.
17. **Chronically failing enabled jobs (CE≥3) as fleet health proxy** — Simple ok/error counts (80 ok / 44 error) look manageable. But 35 of 124 enabled jobs have consecutiveErrors≥3, with one at CE=570. This distinguishes transient failures (random 1-off) from systemic failures (jobs that haven't succeeded in weeks/months). Always report the CE≥3 count alongside the ok/error breakdown.
18. **Gateway model fallback cascade count is a quantitative PHY/FIN signal** — Read the last 5000 lines of `gateway.err.log` and count lines containing `model fallback decision: candidate_failed`. The raw count (295 in one audit) is a concrete, reproducible metric for infrastructure degradation. Compare to `candidate_succeeded` count for a success/fail ratio. This is more diagnostic than fleet-health JSON snapshots which can be stale or inflated with default scores.

## Session-Specific References
See `references/june-1-2026-audit-session.md` for detailed findings from the June 1, 2026 independent audit of STRATEGOS's DS org scorecard, including dimension-by-dimension evidence comparison, TWC math verification, and compound overscoring analysis.

## Verification Checklist (Auditor)
- [ ] Located primary scorer's output and confirmed timestamp
- [ ] Extracted all 8 dimension scores and evidence citations from report
- [ ] Independently verified EACH dimension against raw evidence (not just spot-checked)
- [ ] Independently recomputed TWC math (base sum + coupling modifier + final)
- [ ] Checked compound effect: if 4+ dims overscored, reported compound TWC gap
- [ ] Checked ENV for config rot (stale blockers, auth/security warnings) not just activity
- [ ] Checked FIN for free-tier degradation trajectory, not just static success rate
- [ ] Checked CE≥3 count alongside ok/error breakdown for systemic vs transient failures
- [ ] Checked gateway.err.log fallback cascade count as quantitative PHY/FIN metric
- [ ] Verified fix agent results (if any spawned) against original problem
- [ ] Produced audit report with per-dimension ✅/⚠️/❌ verdicts
- [ ] Overall verdict matches evidence: 3+ ❌ = MATERIAL ISSUES, not MINOR

## Related Skills
- **`organizational-twc-scorecard`**: The skill for GENERATING scorecards (the primary scorer). This audit skill verifies its output.
- **`proprietary-twc-scoring`**: The TWC formula and coupling methodology used by both the scorer and the auditor.
