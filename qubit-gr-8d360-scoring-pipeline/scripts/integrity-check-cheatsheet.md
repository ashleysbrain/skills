# Integrity Check Cheat Sheet

Quick reference for performing the VERITAS-ALGO integrity check.

## Procedure Summary
Run every 12 hours to ensure algorithmic integrity.

### 1. Self-Referential Loop Check (PRIORITY)
- Query observations for score/COMPASS/domain/etc. terms
- Classify as self-referential OR legitimate (apply false-positive rule)
- If self-referential found: delete, re-score, sync, report

### 2. Engine Test Verification
- `cd ~/your-workspace/hydra-os/scripts/rescore-engine && python3 rescore_engine.py test` (7/7 must pass)
- `cd ~/your-workspace/hydra-os/scripts && python3 test-nutrition-engine.py` (must pass)
- `cd ~/your-workspace/hydra-os/scripts && python3 test-sexual-health-engine.py` (must pass)
- STOP if any test fails

### 3. Data Integrity Validation
#### Modifier Staleness
- Nutrition: modifier = 0.85 + 0.30*(composite/100)^2.5 [clamped 0.85-1.15]
- Sexual health: modifier = 0.85 + 0.30*(composite/100)^2.5 [clamped 0.88-1.12]
- Tolerance: ±0.005

#### TWC Recomputation
- Base TWC = (psy*0.18 + phy*0.16 + env*0.11 + soc*0.12 + spi*0.10 + int*0.13 + voc*0.11 + fin*0.09) * 10
- Stacked modifier = sqrt(nutrition_modifier * sexual_health_modifier)
- Expected TWC = base_twc * stacked_modifier
- Tolerance: ±0.2

#### Interaction Matrix
- PSY↔INT: 0.85 ±0.10
- PHY↔VOC: 0.78 ±0.10
- SOC↔SPI: 0.72 ±0.10
- ENV↔PHY: 0.68 ±0.10

#### Pipeline Coverage
- No 7+ day gaps in TWC scores
- Process evidence for missing days
- Target: >80% coverage in last 60 days

#### Phantom TWC
- NULL TWC on carryforward rows without 8D data
- Investigate sourced rows with missing 8D data

### 4. Patient 0 Evidence Audit
- Algorithm work = activation evidence
- Broad evidence lens beyond GitHub commits
- Distinguish deliberate rest from activation failure
- Apply false-positive rule to GitHub observations

### 5. Drift Detection
- Compare latest TWC to baseline in algorithm-integrity-baseline.json
- Investigate if |drift| > 1.0 points
- Note: >3 points = significant, >5 points = critical

### 6. Integrity Logging
Record to ~/your-workspace/health-private/algorithm-integrity-log.md:
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

## Action Guide by Verdict
- ✅ CLEAN: Continue regular monitoring
- ⚠️ MINOR ISSUES: Investigate & fix, schedule for maintenance
- ❌ MATERIAL ISSUES: Investigate immediately, implement fixes ASAP, consider pausing operations

## Critical Thresholds
- Pipeline coverage: <50% = critical, 50-70% = major
- Drift: >3 points = significant, >5 points = critical
- Interaction matrix: >0.20 = major, >0.30 = critical
- Engine tests: ANY failure = critical
- Self-referential loops: ANY detection = critical