# Cron Output File Structure — Observed 2026-08-07

## Context

The V1 skill cycle watchdog documentation previously warned about the cron output directory being inaccessible, assuming that `<agent-home>/cron/output/<job_id>/` might not exist or contain valid files. However, this watchdog session (2026-08-07) demonstrated that the directory **does exist** and contains valid, parseable output files.

## Observed Directory Structure

```
/<workspace>
├── 2026-08-01_07-10-24.md
├── 2026-08-02_03-27-14.md
├── 2026-08-03_03-27-46.md
├── 2026-08-04_03-28-57.md
├── 2026-08-05_03-28-33.md
├── 2026-08-06_03-28-42.md
└── 2026-08-07_03-27-27.md
```

## File Naming Convention

Pattern: `YYYY-MM-DD_HH-MM-SS.md`

The timestamp represents the actual execution time, not just the scheduled time. This is useful for detecting late runs or drift.

## File-Based Extraction Pattern

When session_search results exceed size limits (truncated output), the cron output directory provides a reliable fallback for extracting metrics:

```bash
# Extract JSON monitoring fields from today's output
grep -E "new_skills_recommended|updates_generated|shortfall_label|pipeline_status" \
  <agent-home>/cron/output/c37a1090869d/$(date +%Y-%m-%d)_*.md
```

**Observed working output (2026-08-07):**
```
  "new_skills_recommended": 0,
  "updates_generated": 0,
  "shortfall_label": "philosophical",
  "shortfall_reason": "V1 core + support pair (8d-pattern-awareness + 8d-snapshot-report) assessed as coherent and complete; maintenance-only cycle",
  "pipeline_status": "nominal",
```

## Historical Pattern Extraction

To check consecutive-day patterns (for 3+ day escalation rule):

```bash
# Extract shortfall_label from last 7 days
for f in <agent-home>/cron/output/c37a1090869d/2026-08-*.md; do 
  echo "=== $(basename $f) ==="
  grep -E "new_skills_recommended|updates_generated|shortfall_label" "$f" | tail -2
done
```

**Observed output (Aug 1-7, 2026):**
- All 7 days reported `shortfall_label: "philosophical"`
- All days reported `pipeline_status: "nominal"`
- Updates varied: 2 on Aug 2 and Aug 6, 0 on other days
- New skills: 0 every day

## Distinction: Directory Missing vs. Directory Valid

The skill documentation's warning about "cron output file location inaccessible" conflates two different failure modes:

| Mode | Symptom | What it means |
|------|---------|---------------|
| **Directory doesn't exist** | `test -d <agent-home>/cron/output/c37a1090869d` fails | Cron output location changed, job not configured to write files, or the operator agent version difference |
| **Directory exists but files missing** | Directory present but no file for today's date | Job didn't run, failed silently, or wrote to a different location |
| **Directory exists with valid files** | Directory present + today's timestamp file exists + grep extracts JSON fields | **Normal operation** — file-based extraction is viable |

**Corrective action by mode:**
- Directory doesn't exist → Use session_search as primary extraction method; do not attempt file-based access
- Directory exists but files missing → Investigate job execution (check `hermes cron list`, session_search for today)
- Directory exists with valid files → File-based extraction is available and reliable; prefer it over session_search for speed

## Pattern Observed: 7-Day Philosophical Shortfall Streak

**Date range:** 2026-08-01 through 2026-08-07 (7 consecutive days)

**Consistent pattern across all 7 days:**
- `new_skills_recommended: 0` (every day)
- `updates_generated: 0` (5 of 7 days) or `2` (2 of 7 days)
- `shortfall_label: "philosophical"` (every day)
- `pipeline_status: "nominal"` (every day)
- Shortfall reason consistently references "V1 core + support pair assessed as coherent/complete"

**Watchdog action:**
- Days 1-2: Downgraded to informational (per §R15 routing rule)
- Day 3+: Escalated to target-calibration issue alert (persistent philosophical shortfall with same root cause)

This is the correct escalation pattern per skill-update-engine §R15.

## File Size Baseline (Observed 2026-08)

Typical file size: 145,000–147,000 bytes (142–146 KB)

```
-rw-------@ 1 aw  staff  146615 Aug  7 03:27 2026-08-07_03-27-27.md
-rw-------@ 1 aw  staff  146266 Aug  6 03:28 2026-08-06_03-28-42.md
-rw-------@ 1 aw  staff  145929 Aug  5 03:28 2026-08-05_03-28-33.md
```

**Implication:** If today's file is <100 KB or >200 KB, that may indicate:
- <100 KB: Potential truncation or incomplete execution
- >200 KB: Unusually long output, possible stall or infinite loop

However, file size alone is not conclusive — always verify with structural marker checks.

## Extraction Preference Heuristic

For V1 skill cycle watchdog, use this extraction order:

1. **File-based extraction** (primary): Grep cron output directory for JSON fields — fastest, most reliable when directory exists
2. **session_search with job title** (fallback): Search for "Divinity Health V1 Skill Product Review" — works even if file paths change
3. **session_search with job ID pattern** (last resort): `cron_c37a1090869d_YYYYMMDD` — fragile if naming convention changes

The file-based method should be preferred whenever the directory exists and contains today's file.

## Update to Skill Documentation

The existing pitfall section "Critical pitfall: Cron output file location inaccessible" should be refined to distinguish between:
1. When the directory truly doesn't exist (use session_search)
2. When the directory exists but is empty (investigate job execution)
3. When the directory exists with valid files (file-based extraction is the best option)

The current wording ("this directory does not exist or is not accessible") is too absolute and should be nuanced to reflect the observed reality that the directory often exists and contains valid files.