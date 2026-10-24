---
name: health-data-pipeline-maintenance
description: Maintain and enhance automated personal health data collection and processing systems, including cron job management, script modifications for data capture, and pipeline fixes for health tracking systems like the principal's 8D/TWC scoring.
category: health
version: 1.0
---

# Health Data Pipeline Maintenance

Maintain and enhance automated personal health data collection and processing systems, including cron job management, script modifications for data capture, and pipeline fixes for health tracking systems like the principal's 8D/TWC scoring.

## When to Use
- User reports issues with automated health data collection (missing data, stalled pipelines)
- Cron jobs related to health tracking are failing or missing
- Need to add new data sources or evidence types to health tracking systems
- A passive-first sidecar score or subscore must flow into an existing TWC / daily scorecard / dashboard automatically
- The sidecar score also needs a visible breakdown block in API/CLI/dashboard output (for example, base score, sidecar score, normalized value, blend ratio, delta, fused total, confidence, evidence coverage, prompt policy, and staleness)
- You need to add an additive autonomous overlay layer without rewriting the core TWC math
- You need to keep the core scorer unchanged while exposing new metadata via thin wrappers and presentation layers
- Health scoring systems show stale or missing data
- User wants to improve validity or completeness of health tracking data

## Standard Procedure

### 1. Diagnose System Issues
- Check cron job status: `sibling-agent cron list`
- Identify failed or missing jobs related to health tracking
- Examine diagnostic output for authentication, model availability, or script errors
- Verify data sources exist and are being updated (transcripts, standup drafts, etc.)
- Check evidence balance in EF COMPASS system (behavioral_observation vs self_report vs third_party)

### 2. Fix Cron Job Authentication Issues
- For failed cron jobs due to model authentication:
  - `sibling-agent cron edit [JOB_ID] --model [AVAILABLE_MODEL]`
  - Common fixes: update expired/llm-vendor/glm-5 models to google/gemini-2.5-pro or similar
  - Verify fix by checking next run status

### 3. Recreate Missing Critical Cron Jobs
- Identify missing jobs from documentation or system requirements
- Use `sibling-agent cron add` with appropriate parameters:
  - `--name` descriptive name
  - `--agent main` (typically)
  - `--session isolated`
  - `--model [WORKING_MODEL]`
  - `--cron "[SCHEDULE_EXPRESSION]"`
  - `--tz America/Chicago`
  - `--message "[COMMAND_TO_EXECUTE]"`
  - `--no-deliver` (for background processing)
- Example for post-standup transcript analysis:
  ```bash
  sibling-agent cron add --name "Post-Standup Transcript Analysis" --agent main --session isolated --model google/gemini-2.5-pro --cron "0 9,10,11 * * *" --tz America/Chicago --message "python3 /path/to/script.py" --no-deliver
  ```

### 4. Enhance Data Capture in Processing Scripts
- Identify key processing scripts (e.g., daily-standup-processor.py)
- Add data capture mechanisms:
  - Transcript saving: Save standup transcripts to standardized location
  - Evidence generation: Create self-report prompts or other evidence files
  - Modify script processing pipeline to include new capture steps
- Example additions to daily-standup-processor.py:
  ```python
  # Add transcript saving
  transcript_path = Path.home() / "your-workspace" / "standups" / f"{date_str}-transcript.md"
  shutil.copy(standup_file, transcript_path)
  
  # Add EF prompt generation
  self.generate_ef_prompts()  # Method to create daily self-report prompt files
  ```

### 5. Implement Evidence Diversification
- For EF COMPASS system lacking self_report/third_party_observation:
  - Prefer passive telemetry and activity-derived evidence first when it can cover the signal
  - Create structured micro check-ins instead of long daily prompt files when the goal is user retention
  - Generate brief, adaptive prompts only when confidence is low or passive coverage is sparse
  - Design ADHD-friendly, brief prompts (1-2 sentence responses) if manual input is required
  - Map prompts to EF domains with appropriate weights (typically 2.0 for self_report)
  - When a new passive sidecar score must affect an existing composite score, add a backward-compatible fusion stage rather than duplicating the core scorer, and verify dashboards/API consumers still work when the sidecar payload is absent
  - Instructions for scoring: 0-10 scale based on self-assessment rubrics
  - Instructions for scoring: 0-10 scale based on self-assessment rubrics

### 6. Document Changes and Maintain Running Log
- Update improvement running log with:
  - Timestamp of intervention
  - Diagnostic findings
  - Changes made (cron fixes, script modifications, etc.)
  - Evidence summary (what was verified)
  - Open questions/review needs
  - Next run priorities
- Follow format:
  ```
  ## Current Update
  [Timestamp and findings]
  
  ## Running List Update
  **Update #[N] — [TIMESTAMP]** — [Summary]. Cumulative update count: [N].
  
  ## Proposed Scoring/Tracking Changes
  [Numbered list of changes with priority, description, mapping, and rationale]
  
  ## Evidence Summary
  [Bullet points of verified facts]
  
  ## Open Questions / Review Needs
  [Numbered list of questions needing expert review]
  
  ## Next Run Priorities
  [Numbered list of immediate next steps]
  ```

## Validation Checks
After implementing changes:
- Verify cron jobs show "next run" times and no immediate errors
- Confirm new data files are being created in expected locations
- Check that processing scripts complete without errors
- Validate that new evidence types are being collected and scored
- Confirm the overlay metadata reaches API responses, CLI output, and dashboard payloads
- Run the relevant unit tests plus a smoke request to the wrapper endpoint
- Review running log for completeness and accuracy

## Domain-Specific Notes for the principal's 8D/TWC System
- Transcript-based 8D scoring requires: standup draft → transcript analysis → 8D360 conversion
- EF COMPASS requires balanced evidence types: behavioral_observation (weight 3.0), self_report (weight 2.0), third_party_observation (weight 2.0), stated_belief (weight 1.0)
- HealthKit pipeline provides objective PHY data for sleep_cascade rule and reduces self-report reliance
- Calibration.json must go through expert panel review before scoring rule changes
- All PHI must remain LOCAL ONLY - never transmitted outside ~/your-workspace/health-private/
- Cron job authentication issues commonly occur with expired/llm-vendor/glm-5 models; fix by updating to allowed models from sibling-agent.json allowlist (e.g., openrouter/google/gemma-3-27b-it:free, openrouter/meta-llama/llama-3.3-70b-instruct:free)
- Specific cron jobs for the principal's 8D system: 
  * Standup Preparation (ID: 4fe4e0f4-f204-49cd-b89c-f45beeff2491) - runs at 7:00 AM CT
  * Post-Standup Transcript Analysis (ID: a6cf3acb-a89d-4dd2-afb2-09968ff6fd70) - runs at 9/10/11 AM CT
- Transcript capture can be implemented in daily-standup-processor.py by saving standup drafts to ~/your-workspace/standups/YYYY-MM-DD-transcript.md
- EF COMPASS evidence often lacks self_report and third_party_observation; consider adding structured self-report prompts in standup processing
- HealthKit data pipeline has been broken since March 2026 - investigate iOS Shortcut and healthkit-pull.py script
- Calibration.json has remained DRAFT since March 31, 2026 pending expert panel validation

## Orphan Record Antipattern (learned 2026-05-27)

### Symptom
TWC (or any composite score) in the database shows identical flat values (e.g., 0.5000) across many consecutive days, while dimension scores may be correct or entirely missing.

### Root Cause
A cron job writes composite output records (TWC) daily as placeholders WITHOUT first computing from input records (dimension scores). The compute step was either skipped or disconnected from the write step. Result: fake data that looks real.

### Diagnosis
```sql
-- Find dates with TWC but no dimension scores (orphans)
SELECT t.date FROM twc_scores t
LEFT JOIN dimension_scores d ON t.date = d.date
WHERE d.date IS NULL;

-- Check for suspiciously flat TWC values
SELECT date, twc_final FROM twc_scores
GROUP BY twc_final HAVING COUNT(*) > 3;
```

### Fix Pattern
1. **Delete orphans**: Remove TWC records for dates with no dimension scores
2. **Backfill**: For dates WITH dimension scores, recompute TWC using `compute_twc()` and replace
3. **Atomic pipeline guard**: Create a `scoring_pipeline.py` that computes dimensions AND TWC in a single transaction, never one without the other
4. **Update cron**: Point the scoring cron at the atomic pipeline script instead of manual DB writes
5. **Validate**: Run `python3 scoring_pipeline.py --validate` to check for new orphans

### Atomic Pipeline Script
Located at `products/principal-8d-tracker/scoring_pipeline.py`:
- `compute_and_store_atomic(date)` — computes all 8D + TWC together, never writes TWC without dimensions
- `--validate` — checks for orphan TWC records
- `--fix` — deletes orphan records
- All DB operations are in a single transaction with rollback on failure

### Prevention Rule
**NEVER allow a cron to write composite scores (TWC) without simultaneously writing the component scores (dimensions) they derive from.** If no input data exists, report "no data" rather than inserting placeholder values.

## Autonomous 8D Scoring Pipeline (principal-8d-tracker)

The autonomous scoring pipeline lives at `products/principal-8d-tracker/` and computes scores without manual check-ins by fusing multiple evidence sources.

### Architecture (10 steps, in order)

1. **Gather evidence** — Pull latest check-in answers (daily/weekly/monthly) from `checkin.py`
2. **Build inputs** — `build_inputs_from_answers()` maps answers → calculator.py dataclasses
3. **Score 8 dimensions** — Each dimension scored by its `score_*()` function from `calculator.py`
4. **Compute TWC** — `compute_twc(scores)` applies coupling matrix + coherence + synergy tensor
5. **ADHD fusion** — `adhd_fusion.py:build_adhd_fusion(base_twc)` reads passive ADHD payload, blends 88% base + 12% ADHD normalized score
6. **Support subscores** — `support_subscores.py:build_support_subscores()` computes nutrition, sexual, ADHD, EF proxy scores with cross-dimensional cascades and anti-double-counting
7. **Autonomous overlay** — `autonomous_overlay.py:build_twc_overlay()` computes confidence, evidence coverage, freshness, prompt policy, staleness, source mode
8. **Determine final score** — If ADHD fusion available, use fused TWC; otherwise use base TWC
9. **Store atomically** — Dimensions + TWC in single transaction (never one without other)
10. **Write artifact** — `scoring_export.py:write_scoring_artifact()` writes downstream JSON

### Key Files

- `scoring_pipeline.py` — Full autonomous pipeline script with `--full`, `--validate`, `--fix` flags
- `calculator.py` — Canonical TWC algorithm (coupling matrix, coherence factor, synergy tensor)
- `adhd_fusion.py` — ADHD passive payload → 88/12 fusion with confidence/coverage
- `support_subscores.py` — Cross-dimensional cascade scoring (nutrition, sexual, ADHD, EF)
- `autonomous_overlay.py` — Confidence, coverage, freshness, prompt policy, evidence mix entropy
- `checkin.py` — Check-in answer storage and input building
- `models.py` — SQLAlchemy models (TWCRecord, DimensionScoreRecord, CheckinRecord)
- `api.py` — FastAPI endpoints with full autonomous stack (`/scores/today`, `/dashboard`)

### Autonomous Overlay Metrics

- **Confidence**: 0-1 composite of profile confidence, freshness, evidence coverage
- **Evidence coverage**: Weighted blend of profile, passive, and support quality
- **Freshness**: Time-decay from last profile update
- **Source mode**: `passive_only`, `checkin_only`, or `autonomous_fused`
- **Prompt policy**: Whether the principal needs micro-check-in based on coverage/confidence thresholds
- **Evidence mix entropy**: Shannon entropy of normalized evidence sources (skewed/mixed/balanced)

### Score Modes

- `checkin_only` — No ADHD payload available, base TWC only
- `autonomous_fused` — ADHD fusion active, fused TWC = 0.88 * base + 0.12 * ADHD_norm

### Cron Integration

The AISHA-MD daily scoring cron (e1b0a2a2845b) runs:
```
python3 products/principal-8d-tracker/scoring_pipeline.py --full
python3 products/principal-8d-tracker/scoring_pipeline.py --validate
```

### Dependencies

Requires `sqlalchemy` package. Install: `python3 -m pip install sqlalchemy --break-system-packages`

### ADHD EF Compass v3 Integration (parallel system)

The ADHD EF Compass v3 (`adhd_ef_compass_v3.py`) with sigmoid response curves is a SEPARATE system from the autonomous pipeline above. It feeds behavioral signals through a fusion layer (`adhd_signal_fusion.py`) that maps ADHD domains to calculator.py input fields across 7 of 8 TWC dimensions. This system is built but not yet wired into the scoring_pipeline.py flow — it currently runs as standalone test profiles. To activate: integrate the fusion layer output as an additional evidence source in step 2 of the pipeline.

### Overlap Warning

Three skills cover similar territory:
- **This skill** (`health-data-pipeline-maintenance`) — pipeline fixes, orphan antipattern, autonomous architecture
- **`health-scoring-daily-pipeline`** — transcript-based scoring, nutrition/sexual health, EF COMPASS (different DB at health-private/)
- **`transcript-scoring-pipeline-diagnostics`** — transcript-to-score data flow diagnostics

The autonomous pipeline (principal-8d-tracker) and the transcript pipeline (health-private/) are TWO SEPARATE scoring systems. The autonomous one uses `wellness.db` in the tracker directory; the transcript one uses `ashley_unified_health.db` in health-private/. Do not confuse them.

### score_from_evidence.py — Production DB Writer (FIXED 2026-05-28)

`~/your-workspace/health-private/score_from_evidence.py` is the script that ACTUALLY writes 8D/TWC to `ashley_unified_health.db`. It was discovered (2026-05-28) that it had its own simple linear TWC formula (`twc = sum(dim × weight) × 10`) instead of using `calculator.py` with the coupling matrix, coherence, and synergy tensor. The fix: `compute_twc()` now imports from `calculator.py` and delegates to the real engine, with automatic fallback to simple arithmetic if calculator.py is unavailable.

**Key details of the fix:**
- Dimension order mapping: dims_10 keys (psy,phy,env,soc,spi,int,voc,fin) → calculator canonical order (PSY=0,PHY=1,INT=2,SOC=3,SPI=4,VOC=5,FIN=6,ENV=7)
- Scale: 1-10 input → 0-ETA (0-0.85) for calculator → scaled back to 0-100 for DB
- New DB columns added via auto-migration: `coherence` (REAL), `synergy` (REAL), `coupling_sum` (REAL), `score_engine` (TEXT)
- Scores written after fix include `score_engine='calculator_v3'`; pre-fix rows have `score_engine=NULL`
- The `_ensure_db_columns()` function in score_from_evidence.py handles ALTER TABLE migration automatically on first write

**Diagnostic pattern for this class of bug:** If any scoring script has its own inline math instead of importing the canonical engine, that's a "dual-implementation gap." The canonical engines are:
- TWC math: `calculator.py` in `products/principal-8d-tracker/`
- Nutrition: `8d360-nutrition-engine.py` in `scripts/`
- Sexual health: `8d360-sexual-health-engine.py` in `scripts/`
- Rescore: `rescore_engine.py` in `scripts/rescore-engine/`
- Any script that duplicates formulas inline instead of importing these is suspect.

## Safety Requirements
- Never use `python3 -c "..."` for DB operations in cron (approval blocks in unattended sessions)
- Always write DB scripts to temp file first, then execute
- Health data (PHI) stays LOCAL ONLY at `~/your-workspace/health-private/` with 700/600 permissions
- Never push health data to GitHub, cloud, API calls, or cron prompts
- Verify speaker attribution in transcripts before trusting transcript-derived scores
- Health scoring math MUST go through deterministic engines - never hand-compute
- **Canonical nutrition engine:** `~/your-workspace/hydra-os/scripts/8d360-nutrition-engine.py` (FORGE-audited v1.1+). All nutrition scoring (protein, meal frequency, hydration, composite, modifier, label) MUST import from this engine. The 2026-05-27 audit found 22-point score inflation from a script that duplicated formulas instead of importing the engine. NEVER copy nutrition formulas inline.
- **Partial-day scoring:** The canonical engine has `compute_nutrition_composite_partial(hour_of_day, **kwargs)` that scales protein/meals/hydration targets by time of day. Use for midday check-ins and real-time food logging. End-of-day final scoring must use full `compute_nutrition_composite()`. Food photo helper script at `~/your-workspace/health-private/daily/food_photo_to_nutrition.py` (v2.0+) uses partial scoring automatically.
- **Canonical rescore engine:** `~/your-workspace/hydra-os/scripts/rescore-engine/rescore_engine.py`. All TWC rescores must go through this engine, never hand-computed (see `rescore-engine-usage` skill).