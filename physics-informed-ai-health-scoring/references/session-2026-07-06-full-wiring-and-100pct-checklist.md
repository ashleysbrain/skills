# Session 2026-07-06: Full Wiring and 100% Completion Checklist

## Context

User asked for Options 2 (adopt 6+1 AI dimensions), 3 (wire self-healing loop to real probes), and 4 (fix PIML marketing claims) to be executed in correct order, then pushed to 100% completion.

## Key Lessons

### 1. Marketing claims live in THREE sibling trees

The workspace has three parallel copies of marketing materials:
- Root: `marketing-sprint/`, `your-org-marketing/`, `ds-wave-*-advisory-panel-private/`
- `agent-organism/`: same directory structure mirrored
- `your-org/the operator agent/`: same directory structure mirrored again

Fixing only the root tree left 18 files in sibling trees still carrying the inflated claim.

**Search command that catches all trees:**
```bash
grep -rl "inflated phrase" . --include="*.md" --include="*.py" \
  | grep -v PIML-VERIFIED | grep -v node_modules | grep -v .git \
  | grep -v hydra-os/archive
```

### 2. Engineering docs can fabricate metrics too

The PIML-ENGINEER-PLAYBOOK.md claimed "Final day: MSE 15.9 vs 191.8 (12x improvement)".
metrics.json has only two data points: total_mse (10.94 vs 11.64 = 6%) and extrapolation_mse (19.22 vs 81.50 = 4.2x).
There is no "final day" breakdown. The 12x number was fabricated.

**Verification rule:** Every numeric claim in any document type (marketing, engineering, advisory) must be traceable to a line in metrics.json. If it is not, remove it.

### 3. Sibling "done" reports need live verification

Opencode committed the mode switch (642cb0e) hours before I checked. I reported Option 2 at 60% based on stale knowledge. The fix: always run `git log --oneline -5` and grep the actual file before claiming a gap.

### 4. Production wiring requires touching the call sites, not just the engine

The mode switch existed in `compute_twc()` but no caller passed `mode='ai'`. The production path still used old dimensions until I wired:
- `fleet_twc_engine.py` line 604: `compute_twc(D, mode="ai")`
- `organism/task-engine-prototype/app.py` line 152: `_fleet.compute_twc(D, mode="ai")`

Human wellness scoring paths (health-private, hydra-os) correctly stay `mode='human'`.

### 5. Sensors must read real data, not hardcoded defaults

sense_align was returning a hardcoded 0.92 compliance rate. After wiring to the real physics_compliance audit, it returned 0.267 (4 of 15 engines pass full 5-layer compliance). That real number triggered the self-healing loop's first genuine critical alert (ALIGN at 2.67).

### 6. Cron jobs need repeat=-1 for recurring

The cronjob tool defaults to one-shot. For an autonomous monitoring loop, set:
- `schedule: "*/15 * * * *"` (every 15 minutes)
- `repeat: -1` (forever)
- `no_agent: true` (script-only, zero token cost)
- `deliver: local` (silent unless critical alert)

### 7. The --execute flag must be tested

Dry-run mode only logs interventions. The --execute flag changes status from "logged" to "queued". Testing it revealed the loop correctly queued a real intervention for ALIGN (soul_file_review + boundary_check + mission_recalibration, F=-4200).

### 8. The --cron flag needs bus posting

The cron mode posts critical alerts to the operator bus so both operators see them. Healthy cycles are silent (noise-aware alarm). Only critical-severity alerts or TWC < 5.0 trigger a bus post.

## Complete 100% Verification Checklist

When the user says "ensure 100% complete":

1. **Exhaustive search** every directory tree for remaining instances
2. **Verify every numeric claim** against metrics.json (not just marketing — engineering docs too)
3. **Confirm production callers** use the new code path (grep for call sites)
4. **Confirm sensors** read real data, not hardcoded defaults
5. **Verify cron jobs** are recurring (repeat=-1), not one-shot
6. **Test --execute flag** produces queued interventions
7. **Test --cron flag** posts alerts to operator bus
8. **Run ad-hoc verification script** covering all changed behavior
9. **Clean up temp files** after verification
10. **Report completion honestly** — if something is at 90%, say 90%
