# VERITAS-ALGO Bi-Daily Audit Runbook

Condensed, copy-pasteable command sequence for the recurring integrity audit.
Run every 12 hours. All commands use terminal sqlite3 directly (no Python script needed,
which avoids write-file gate issues in cron environments).

## Step 0: Watchdog Liveness Check (MANDATORY before any other verification)

Before running any verification checks, verify that VERITAS-ALGO itself has been running regularly.

```bash
# Check latest log entry timestamp (staleness >48h = watchdog dead)
stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" /<workspace>

# Or read last 5 lines to see timestamps manually
tail -5 /<workspace>
```

**Staleness threshold:** If the latest entry is older than 48 hours, VERITAS-ALGO is dead and this must be flagged as a MATERIAL ISSUE in the audit report. A dead watchdog means all prior "verified by VERITAS" claims are now suspect.

## Step 1: Engine Tests (run in parallel)

```bash
cd ~/your-workspace/hydra-os/scripts/rescore-engine && python3 rescore_engine.py test
cd ~/your-workspace/hydra-os/scripts && python3 test-nutrition-engine.py
cd ~/your-workspace/hydra-os/scripts && python3 test-sexual-health-engine.py
```
Expected: rescore 7/7, nutrition 22/22, sexual health 43/43. If ANY fail, STOP.

## Step 2: Self-Referential Loop Check (EF tracker)

```bash
sqlite3 /<workspace> "
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
   OR evidence_text LIKE '%Activation at %'
   OR evidence_text LIKE '%score drifted%'
   OR evidence_text LIKE '%Score holding at%';"
```
Classify each hit. Apply false-positive rule: if observation describes BUILDING/DESIGNING/
MAINTAINING/DEBUGGING/WORKING ON the scoring system, it's legitimate. Only flag entries
where the subject IS a score number, trend, or system-produced metric.

## Step 3: Pipeline Coverage

```bash
DB=/<workspace>

# Real scores last 7 days
sqlite3 $DB "SELECT COUNT(*) FROM daily_scorecard WHERE twc_score IS NOT NULL AND source NOT IN ('cron','carryforward') AND date >= date('now','-7 days');"
# Real scores last 30 days
sqlite3 $DB "SELECT COUNT(*) FROM daily_scorecard WHERE twc_score IS NOT NULL AND source NOT IN ('cron','carryforward') AND date >= date('now','-30 days');"
# Last real score date
sqlite3 $DB "SELECT date FROM daily_scorecard WHERE twc_score IS NOT NULL AND source NOT IN ('cron','carryforward') ORDER BY date DESC LIMIT 1;"
# Trailing gap (rows in last 10 days)
sqlite3 $DB "SELECT date, twc_score, source FROM daily_scorecard WHERE date >= date('now','-10 days') ORDER BY date DESC;"
```
Flag: 0/7 = CRITICAL. Trailing gap >=5 days = escalating failure.

## Step 4: Interaction Matrix (canonical values verification)

**CRITICAL:** The canonical DB values are AUTHORITATIVE per `organism/canonical_coupling.py` VERITAS lock (2026-06-28). The old spec heuristics (0.85/0.78/0.72/0.68) were REJECTED for schema violations >0.5. Do NOT compare against them.

```bash
sqlite3 $DB "
SELECT dim1 || '<->' || dim2 as pair, value,
  CASE
    WHEN (dim1='INT' AND dim2='PSY') THEN 0.20
    WHEN (dim1='PHY' AND dim2='VOC') THEN 0.15
    WHEN (dim1='SOC' AND dim2='SPI') THEN 0.20
    WHEN (dim1='ENV' AND dim2='PHY') THEN 0.25
    ELSE NULL END as canonical,
  ROUND(value - (CASE
    WHEN (dim1='INT' AND dim2='PSY') THEN 0.20
    WHEN (dim1='PHY' AND dim2='VOC') THEN 0.15
    WHEN (dim1='SOC' AND dim2='SPI') THEN 0.20
    WHEN (dim1='ENV' AND dim2='PHY') THEN 0.25
    ELSE NULL END), 3) as delta
FROM interaction_matrix
WHERE (dim1='INT' AND dim2='PSY')
   OR (dim1='PHY' AND dim2='VOC')
   OR (dim1='SOC' AND dim2='SPI')
   OR (dim1='ENV' AND dim2='PHY');"
```
Expected: delta = 0.000 (canonical values are correct). If delta != 0, investigate data corruption.

**Additional checks:**
```bash
# Matrix completeness: should be 28 pairs (C(8,2))
sqlite3 $DB "SELECT COUNT(*) FROM interaction_matrix;"

# Out-of-bounds check: should be 0 (capped at ±0.5)
sqlite3 $DB "SELECT COUNT(*) FROM interaction_matrix WHERE value < -0.5 OR value > 0.5;"

# Canonical form check: should be 0 (dim1 < dim2 only)
sqlite3 $DB "SELECT COUNT(*) FROM interaction_matrix WHERE dim1 >= dim2;"

# Matrix statistics: sum should be ~5.05, avg ~0.180, range [0.05, 0.35]
sqlite3 $DB "SELECT SUM(value), AVG(value), MIN(value), MAX(value) FROM interaction_matrix;"
```

## Step 5: Modifier Staleness

```bash
# Nutrition
sqlite3 $DB "SELECT date, nutrition_composite, nutrition_modifier FROM daily_scorecard WHERE nutrition_composite IS NOT NULL ORDER BY date DESC LIMIT 10;"
# Sexual health
sqlite3 $DB "SELECT date, sexual_health_composite, sexual_health_modifier FROM daily_scorecard WHERE sexual_health_composite IS NOT NULL ORDER BY date DESC LIMIT 10;"
```
Verify: modifier = 0.85 + 0.30 * (composite/100)^2.5, clamped [0.85, 1.15].
Flag: delta >0.005 = stale.

## Step 6: TWC Recomputation

```bash
sqlite3 $DB "SELECT date, twc_score, psy, phy, env, soc, spi, int_score, voc, fin, nutrition_modifier, sexual_health_modifier FROM daily_scorecard WHERE twc_score IS NOT NULL ORDER BY date DESC LIMIT 10;"
```
Recompute: weighted = PSY*0.18 + PHY*0.16 + ENV*0.08 + SOC*0.12 + SPI*0.12 + INT*0.10 + VOC*0.14 + FIN*0.10
Then: computed = weighted * 10 * sqrt(nutrition_modifier * sexual_health_modifier)
Flag: delta >0.2 = mismatch.

## Step 7: Other Checks

```bash
# Phantom TWC (carryforward rows with TWC but all 8D NULL)
sqlite3 $DB "SELECT date, twc_score, source FROM daily_scorecard WHERE source IN ('cron','carryforward') AND twc_score IS NOT NULL ORDER BY date DESC LIMIT 20;"

# Coupling sum constancy (dead code check)
sqlite3 $DB "SELECT DISTINCT coupling_sum FROM daily_scorecard WHERE coupling_sum IS NOT NULL;"
# Flag: if <=2 distinct values = constant = Layer 3 dead

# twc_history freshness
sqlite3 $DB "SELECT MAX(date) FROM twc_history;"
sqlite3 $DB "SELECT MAX(date) FROM daily_scorecard;"

# Label correctness
sqlite3 $DB "SELECT date, composite, label FROM nutrition_daily WHERE date >= date('now','-30 days');"
sqlite3 $DB "SELECT date, composite, label FROM sexual_health_daily WHERE date >= date('now','-30 days');"
# Nutrition thresholds: >=90 optimal, >=80 strong, >=70 adequate, >=60 gaps, >=50 concerning, <50 critical
# Sexual health thresholds: >=85 thriving, >=75 strong, >=65 healthy, >=50 adequate, <50 gaps
```

## Step 8: Baselines

Read `~/.sibling-agent/workspace/memory/principal-8d/baselines.json` and check `twcBaseline`.
If null, drift calculation is impossible. Flag as blocker.

## Step 9: Assemble Report and Log

Append to `~/your-workspace/health-private/algorithm-integrity-log.md` using the
standard VERITAS-ALGO report format (see SKILL.md Output Format section).

## Historical Findings (as of 2026-06-20)

Persistent issues across 5+ consecutive verifications (not transient):
- Pipeline coverage: 0/7 days real scores (trailing gap >=10 days)
- Interaction matrix: all 4 key couplings deviate 0.43-0.65 from spec
- Coupling terms: dead code (constant 6.775, never added to TWC)
- twcBaseline: null
- twc_history: stale (not being populated by current pipeline)

Resolved issues (confirmed clean 2026-06-20):
- Label correctness: ALL nutrition and sexual health labels now match canonical thresholds
- Self-referential loops: 0 found (prevention working)
- Modifier staleness: 0 stale (all within tolerance)
- Phantom TWC: 0 found
