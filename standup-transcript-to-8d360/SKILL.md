---
name: standup-transcript-to-8d360
description: Process the principal's daily standup transcripts into 8D360 wellness scores, daily responsibilities, and midday check-in updates. Two-speaker separation mandatory.
tags: [standup, 8d360, scoring, aisha-md, transcript, wellness]
version: 2.0
---

# Standup Transcript to 8D360 Scoring Pipeline

## 🔄 MANDATORY: Any New Transcript = Re-Score the Day (locked 2026-04-06)

When ANY new source of evidence lands for a day that's already been scored — a fresh transcript, audio file, weekly vision doc, voice note, retroactive debrief, late-logged supplement/meal/exercise data — you MUST re-score the entire day immediately. Scores are a running estimate, not a historical lock.

**Trigger conditions:**
- New `standups/YYYY-MM-DD-transcript.md` or `weekly-vision-YYYY-MM-DD.md` lands
- the principal reports additional data retroactively (voice note, text, voice call)
- Any supplement, meal, exercise, intimacy, or sleep data logged late
- Any wearable data imports for the date

**Required action:**
1. Re-read ALL source materials for that day (transcripts, vision docs, existing scores, audio if available)
2. Re-score every dimension (PSY, PHY, ENV, SOC, SPI, INT, VOC, FIN)
3. Re-score every sub-component (nutrition, sexual health, kink, EF COMPASS)
4. Re-compute TWC with the new numbers
5. UPSERT the daily_scorecard row (update by date)
6. UPSERT the twc_history row
7. Send the principal the updated scorecard with a diff showing what changed and why
8. Never silently re-score without sending the principal the updated numbers

**MANDATORY evidence search before any (re-)score** — ALWAYS check BOTH locations before scoring a day. Missing one caused a full-tier under-scoring of 4/5 (70.7 Stable vs actual 75.0 Flourishing):

```bash
# BOTH of these must be checked for every scoring run:
ls ~/your-workspace/health-private/standups/YYYY-MM-DD-transcript.md
ls ~/your-workspace/hydra-os/memory/principal-8d/weekly-vision-YYYY-MM-DD.md
# Plus any audio files, voice notes, and retroactive chat data
```

The `standups/` transcript (from the principal↔the principal standup voice note) and the `weekly-vision-*` doc (from Sunday vision debrief) are DIFFERENT source materials with DIFFERENT signal. The weekly vision doc typically contains 3-5x the richness of the standup transcript — boundary work, relationship processing, fleet wins, infrastructure drains, FIN conversations. Never score from transcript alone when a weekly vision doc exists for the same date.

**DB source field CHECK constraint:** `daily_scorecard.source` only accepts specific values (`'transcript'`, `'manual'`, etc.) — DO NOT try to use `'transcript+weekly_vision'` or other combined values, they will reject. Use `'transcript'` and note the merged evidence in the rationale field instead. Schema gap flagged for HELION's Qubit-GR rebuild.

**Never** leave a day scored on incomplete evidence when new evidence exists.

### Adjacent-day rescore requirement (learned 2026-04-07)

When voluntary debrief evidence lands retroactively, you often need to rescore MORE than just the target day:

- **Morning-after voice memos** that debrief the PREVIOUS day → rescore the previous day, AND verify today's auto-generated 7:33 AM scorecard didn't lock in stale "trending down" language from the old data
- **Evening debriefs** covering the current day → rescore today AND check that today's 7:33 AM pre-standup brief didn't already ship a prediction based on yesterday's incomplete data

**The automated 7:33 AM scorecards are built BEFORE any voluntary debrief lands** — they're predictions based on the prior day. When the principal sends a debrief later, both the scored day AND any auto-scorecards generated from stale assumptions need to be replaced.

Check for `ASHLEY-SCORECARD-YYYY-MM-DD-*.md` files in `~/your-workspace/health-private/daily/` — if any are older than the new evidence, regenerate them with the RESCORE suffix and UPSERT the DB rows.

### NO-SHAME language audit before delivery (learned 2026-04-07)

Before sending ANY scorecard to the principal, grep the output for banned phrases:
```bash
grep -iE "declining|trending down|downward|regression|slipping|concerning|flagged|watch out|be careful|warning|feeding.*problem" <scorecard>.md
```

If ANY hit, rewrite before delivery. The automated scoring engine WILL produce "trending down" text — you must intercept it.

The DB schema has `sexual_health_label` including `'concerning'` as an allowed value. This is OK to store internally for CHECK constraint compliance, but NEVER display it to the principal in that wording. Translate to neutral framing in the user-facing output.

### DB schema gotchas (learned 2026-04-07)

`daily_scorecard` table has:
- NO `rationale` column — don't try to INSERT one (will error "no column named rationale")
- `source` field CHECK constraint only accepts: `'transcript'`, `'checkin'`, `'manual'`, `'scorecard_json'`, `'cron'`, `'standup'`, `'8d_daily'` — NOT combined values like `'transcript+weekly_vision'`
- PRIMARY KEY is `date`, use `ON CONFLICT(date) DO UPDATE SET ...` for upserts
- `int_score` is the column name (not `int` which is a reserved word)

Working upsert template:
```sql
INSERT INTO daily_scorecard (date, twc_score, twc_label, psy, phy, env, soc, spi, int_score, voc, fin, mood, source)
VALUES ('YYYY-MM-DD', 71.0, 'Stable', 6.5, 5.0, 7.5, 8.0, 7.5, 6.5, 5.5, 4.5, 'mood-tag', 'transcript')
ON CONFLICT(date) DO UPDATE SET
  twc_score=excluded.twc_score, twc_label=excluded.twc_label,
  psy=excluded.psy, phy=excluded.phy, env=excluded.env, soc=excluded.soc,
  spi=excluded.spi, int_score=excluded.int_score, voc=excluded.voc, fin=excluded.fin,
  mood=excluded.mood, source=excluded.source;
```

---

## When to Use
- Processing the principal's daily standup transcript
- Running midday check-ins when the principal reports personal data
- Updating 8D360 scores from real-time user data
- Any time the principal sends personal health/wellness data (ALWAYS route to AISHA-MD, never AISHA)
- Any time later same-day evidence arrives and the provisional personal scorecard needs to be replaced with a final day score

## Critical Rules

1. **Personal health data → AISHA-MD ONLY.** Never AISHA. Never any other agent.
2. **ASHLEY'S DAILY CARD IS ASHLEY ONLY.** Never include the principal's action items, tasks, appointments, or to-dos in the principal's scorecard or daily card. the principal's items are his business. The card the principal sees should contain ONLY her tasks and her scores. Extracting the principal's items "for context" is crossing the firewall. This was violated 2026-05-27 and corrected.
3. **Speaker separation:** the principal speaks first. the principal's section starts at her transition phrase — known variants include "Ok for me...", "back to me", "for me, the principal", or a "## ASHLEY" header. ONLY the principal's words scored. CRITICAL: "For me, the principal" / "For me, the principal was my part" is the SAME PATTERN as "Ok for me" — the principal addressing herself by name to start her section. It is NOT the principal addressing the principal. When in doubt, ASK the principal before scoring rather than guess wrong. Misattributing the principal's gratitude/apology/business excitement to the principal contaminates her scores and breaks trust. Confirmed wrong-direction parse 2026-04-07.

### Ownership correction for mixed standup notes
- If the user later says that some numbered items are not theirs, discard those items and rebuild the list from scratch using only confirmed user-owned items.
- Do not treat transcript position or numbering as ownership.
- Leave uncertain items unassigned rather than guessing.
- Reference: `references/ownership-correction-pattern.md`

3. **Transcript cap:** No dimension hits 10.0 from transcript keywords alone. Cap at 9.0.
4. **SOC base override:** the principal's social base is 6.0 not 5.0. Low social volume is chosen, not deficit.
5. **All data saved to health-private/** (local only, chmod 600, never GitHub).
6. **Show actual scores.** When the principal asks about scores, compute and display the full scorecard. Don't just describe changes narratively.
7. **Personal vs system separation.** If the user asks for personal scores, show the principal-only numbers first and keep fleet/system health summaries out of the personal scorecard unless explicitly requested.

## Cron Architecture (no duplicates — audit before creating)

| Time | Job | What It Does |
|------|-----|-------------|
| 7:00 AM | SENTINEL Compliance Sweep | Single daily audit: journals, talent gate, data integrity, QA coverage |
| 7:15 AM | Standup Prep | Pulls git accomplishments, deadlines, blockers. Delivers PDF BEFORE standup. |
| 10 AM | Post-Standup | Checks for new transcript. If found: runs analyzer, generates responsibilities PDF, delivers scores. ONE run, goes [SILENT] if no transcript or already processed. |

## Transcript Analyzer

Two scripts can be used to process standup/pre-standup briefs into scores:

**Important baseline rule:** scores are not static. The active calibration can change over time, and the pipeline should carry baseline metadata forward so later evidence can rescore the same day cleanly.

1. **`score_from_evidence.py`** (preferred for standup/pre-standup briefs):
   ```bash
   python3 /<workspace> --date TODAY --source standup --text "<brief_content>"
   ```

2. **`transcript-analyzer.py`** (original tool, still valid):
   ```bash
   python3 ~/your-workspace/hydra-os/scripts/transcript-analyzer.py <transcript.md> --summary
   ```

Calibration for transcript-analyzer: `~/your-workspace/hydra-os/memory/principal-8d/calibration.json`

### Transcript path locations (there are multiple — check the one the cron points at)

- `~/your-workspace/standups/YYYY-MM-DD-transcript.md` ← 10 AM post-standup cron reads THIS path
- `~/your-workspace/health-private/standups/YYYY-MM-DD-transcript.md` ← used by some health workflows
- `~/your-workspace/hydra-os/memory/principal-8d/weekly-vision-YYYY-MM-DD.md` ← Sunday vision doc

The 10 AM post-standup cron specifically uses `~/your-workspace/standups/`. Don't waste time searching `health-private/standups/` if that's not where the cron is pointed — follow the cron prompt exactly.

## Daily Responsibilities PDF Generation

The 10 AM post-standup job generates a responsibilities PDF. Logic: use `/tmp/gen_daily_pdf.py` if it exists, otherwise write it fresh.

**`/tmp/gen_daily_pdf.py` is ephemeral** (VM restart wipes `/tmp/`). Each cron run should be prepared to write it fresh. A working implementation lives in the skill's scripts/ folder (see `scripts/gen_daily_pdf.py`) — copy that to `/tmp/` if missing rather than rewriting from scratch.

Usage: `python3 /tmp/gen_daily_pdf.py <input.md> <output.pdf>`

**Styling contract (amber/sienna palette):**
- Primary color: `#A0522D` (sienna) for H1, H3
- Accent: `#D2691E` (chocolate/amber) for borders, blockquote rules, table headers
- Background: `#fdf8f2` (warm cream)
- Table rows: `#FFF8DC` / `#FAEBD7` zebra
- Font: Georgia/Palatino serif for body, Helvetica Neue for headings
- H2: uppercase, amber gradient background, sienna left border
- Checklist items render as ☐ / ☑ (not `- [ ]`)
- Page footer: "AISHA-MD · Daily Responsibilities · page N of M" in sienna

The generator is a minimal markdown→HTML converter (NOT a full markdown library) tailored to the responsibilities template format: H1/H2/H3, blockquotes, `- [ ]`/`- [x]` checklists, plain `- ` lists, pipe tables with `|---|` separator, `**bold**`, `*italic*`, `` `code` ``, `~~strike~~`, and `---` horizontal rules. That covers everything the responsibilities template uses.

## Midday Check-In Updates

When the principal sends personal data during the day (meals, activity, mood, etc.):
1. Log raw data to `~/your-workspace/health-private/daily/YYYY-MM-DD-*.json`
2. Compute adjusted scores from morning baseline + new evidence
3. Show the FULL scorecard with MORNING → ADJ → NOW → TRAFFIC LIGHT for each dimension
4. Include evidence citations for every adjustment
5. chmod 600 all health-private files

### Partial-Day standup baseline workflow

When the evidence is a same-day standup voice note and later-day evidence has *not* arrived yet:
1. Parse the principal's section only, using the speaker split rules above.
2. Create a *preliminary* scorecard for the current date instead of waiting for nutrition or sexual-health completion.
3. Save both a machine-readable raw artifact and a human-readable preliminary markdown file in `health-private/daily/`.
4. Update the lightweight daily overview file so the top-line TWC matches the preliminary standup score.
5. Keep nutrition, sexual health, kink, and EF deltas explicitly pending unless the voice note actually contains those signals.
6. Mark the output as provisional/preliminary so later evidence can trigger a full re-score without ambiguity.
7. Preserve the patient-0 rule: algorithm/company/scoring-method work counts as real activity, and mission-aligned positive-health work can lift PSY/SPI more than a generic productivity day.
8. If lunch, dinner, hydration, intimacy, or follow-up details arrive later the same day, treat the earlier result as provisional and rescore the full day.

This pattern is useful whenever the principal does a quick morning or midday debrief, then sends more data later in the day.

### Scoring Categories Beyond Basic 8D
- **Sexual Health:** Cross-dimensional (PHY+PSY+SOC+SPI). 5 components: Physical Intensity, Neurochemical Impact, Emotional Connection, Frequency Health, Recovery & Safety. Panel: EROS, TANTRA, KINSEY, BONDING. Score physical activity properly — 5 vigorous sessions = 75-200 min cardio equivalent.
- **Nutrition:** Cross-dimensional (PHY+PSY+INT+ENV). Components: inflammation index, brain-health index, medication interaction, hydration. Panel: ENTERIC, NOURISH, SYNTH, HARVEST, GLYCAN. Always flag Latuda 350+ cal dinner reminder.

## Agent Spawning for New Scoring Categories

When a scoring gap is identified (like sexual health or nutrition), the process is:
1. File talent request through FORGE+ARBITER
2. Check existing fleet for transferable expertise (e.g., GD fleet for sexual psych)
3. Spawn new science agents with full profiles (17 sections, 10 personalities, DB+personas)
4. Log everything in analytics tables (delegation_tracking, talent_gate_log, task_analytics)
5. FIREWALL: GD knowledge transfers to DS/QH, but GD branding stays separate

## Solo Standup / Direct Voice Note Workflow (added 2026-05-29)

This workflow now assumes the transcript adapter and adaptive baseline bridge are part of the live path. The job of the adapter is to extract richer evidence from the note; the job of the bridge is to translate that evidence through the principal's evolving baseline before the calculator runs.

When the principal sends a voice note directly in chat (not as a transcript file) and it's a solo standup (no the principal), the pipeline is different:

### Why this needs special handling
The automated `score_from_evidence.py --text` parser is a blunt instrument — it assigns flat 5.0s to most dimensions and produces very low TWC (e.g., 41.5 for a morning with rich positive evidence). It cannot capture compound self-care routines, mission-aligned work, or patient-0 signal. You must manually set base dimensions from evidence.

### Workflow
1. **Parse the voice note text** — no transcript file to read, no speaker separation needed
2. **Extract ALL evidence categories** present in the voice note:
   - Self-care routine (shower, red light, skincare, meditation) → PHY, ENV
   - Physical activity (sex, dance, exercise) → PHY, SOC, sexual health composite
   - Nutrition (bone broth, coffee, meals) → nutrition composite
   - Med adherence → PHY, PSY
   - Executive function (proactive rescheduling, planning, laundry) → PSY, VOC, ENV
   - Mission-aligned work (scoring system, methodology) → INT, VOC, SPI (patient-0 rule)
   - Forward planning (brainstorm prep) → PSY, SPI
   - Cannabis resupply → FIN (maintaining medical baseline)
3. **Set base dimensions manually from evidence** — do NOT trust the automated scorer output. Typical ranges for a good morning routine:
   - PSY: 7.0-8.0 (voluntary debrief + proactive planning + med adherence)
   - PHY: 6.0-7.5 (sex + red light + dance + nutrition + self-care stack)
   - ENV: 5.5-6.5 (self-care routine + chores planned)
   - SOC: 6.5-8.0 (intimacy + connection signals; base is 6.0 not 5.0)
   - SPI: 6.0-7.5 (mission-aligned work counts double for patient-0)
   - INT: 6.5-8.0 (scoring methodology = deep intellectual work)
   - VOC: 6.5-8.0 (meeting management + system work)
   - FIN: 5.0-6.0 (planned budget, nothing negative)
4. **Compute TWC** using the calculator: write a temp `/tmp/compute_twc.py` that imports `compute_twc` from `score_from_evidence.py` and passes the manual dims + any sub-component composites. The `-c` inline flag has shell escaping issues.

   - For live transcript/voice-note scoring, prefer the transcript adapter + adaptive baseline bridge path instead of treating the manual dims as final truth.
5. **Write to DB** with `UPDATE daily_scorecard SET ... WHERE date = ?` (row likely exists from the automated scorer's first pass).
6. **Append to rescore audit log** at `~/your-workspace/health-private/daily/rescore-audit.log`.
7. **Deliver the scorecard** to the principal with full dimension breakdown, sub-components, evidence citations, and Δ from yesterday.

### Sub-component handling for early morning
- **Nutrition composite:** If only coffee/bone broth consumed (no meals yet), use a carryforward or conservative default (e.g., 65). Do NOT pass 0 protein/0 meals to the rescore engine — it will crash or tank the score.
- **Sexual health composite:** If morning intimacy is reported, set to 70-75 (healthy) and compute modifier from the canonical formula.

### Rescore engine limitation
The rescore engine crashes (`TypeError: '>=' not supported between instances of 'NoneType' and 'int'`) when `nutrition_composite` or `sexual_health_composite` is None in the preliminary block. Always provide numeric defaults (e.g., 65.0 / 1.0) even if the real data is pending.

### Calculator Engine Architecture (added 2026-05-29)

**This is the core knowledge the principal expects you to have.** The system has TWO scoring paths, and you must use the complex one:

**Baseline calibration update:** the complex engine still needs a baseline-aware translation layer. Treat calibration as versioned and evolving; do not freeze the user's first-week or first-day numbers as a permanent anchor.

#### The Complex Engine (calculator.py)
Located at: `/<workspace>`

Each dimension has its own scientific algorithm:
- Ψ Psychological: Quantum Cognition (valence, coherence, energy, stability)
- P Physical: Prigogine Thermodynamics (recovery, kinetic output, entropy index)
- In Intellectual: Shannon Information Theory (info input, processing, knowledge entropy, cognitive efficiency)
- So Social: Kuramoto Model (network density, interaction force, support balance, conflict friction)
- Sp Spiritual: Consciousness Science (consciousness coherence, purpose field, values alignment, transcendent energy)
- Vo Vocational: Flow Theory (work force, flow balance, career momentum, growth energy)
- Fi Financial: Prospect Theory (cash flow, resilience, growth potential, equilibrium distance)
- En Environmental: Attention Restoration Theory (conductivity, atmosphere, nature gradient)

These algorithms take detailed quantitative dataclass inputs (e.g., `PhysicalInput(sleep_hours=2.0, exercise_min=25, ...)`) and produce 0-0.85 scores.

#### The TWC Formula (28-pair coupling matrix)
```
TWC = η × μ_D × C × (1 + 0.5 × S)

where:
  η = 0.85 (efficiency cap / ETA)
  μ_D = mean of 8 dimension scores (scaled to 0-ETA range)
  C = 1 - σ_D/μ_D (coherence factor — penalizes imbalance)
  S = (1/28) × Σ κ_ij × D_i × D_j (synergy tensor from 28 coupling pairs)
```

The coupling coefficients (κ_ij) are in `calculator.py`'s `KAPPA` dict. The strongest pairs:
- Ψ↔So: 0.40 (head drives social)
- In↔Vo: 0.45 (growth drives work)
- Vo↔Fi: 0.35 (work drives money)
- Ψ↔Vo: 0.35 (head drives work)
- Ψ↔In: 0.30 (head drives growth)

#### How score_from_evidence.py bridges the gap
You do NOT need to populate calculator.py's raw dataclass inputs. `score_from_evidence.compute_twc()` does the bridging:

1. Takes 1-10 scale dimension scores (e.g., `{"psy": 8.0, "phy": 6.2, ...}`)
2. Scales each to 0-ETA range: `(val/10) × 0.85`
3. Creates `DimensionScore` objects with the scaled values
4. Calls `calculator.py`'s `compute_twc()` — this runs the FULL coupling matrix + coherence + synergy
5. Scales the result back to 0-100: `result.twc_final / ETA × 100`
6. Applies nutrition modifier: `0.85 + 0.30 × (composite/100)`
7. Applies sexual health modifier: `0.88 + 0.24 × (composite/100)`
8. Combined modifier: geometric mean of both
9. Final TWC = base × combined_modifier

**This IS the complex scoring.** The coupling matrix, coherence factor, and synergy tensor are all engaged. It is NOT a simple weighted average.

#### What to show in the scorecard
the principal expects to see:
- All 8 dimensions with evidence citations
- The TWC computation breakdown: μ_D, C (coherence), S (synergy), κ sum
- The TWC formula with actual numbers
- Nutrition and sexual health composites with modifiers
- Key coupling cascades (which dimension pairs are lifting or dragging)
- The engine label: `calculator_v3`

#### The `--text` flag pitfall
Running `python3 score_from_evidence.py --text "..."` uses an internal LLM/scorer that sets flat dimensions and produces VERY low TWC (e.g., 41.5 for a morning with rich positive evidence). It does NOT capture compound self-care routines, mission-aligned work, or patient-0 signal. **Never trust its output as the final score.** Use it only as a starting point, then manually set dimensions from evidence and call `compute_twc()` directly.

---

## Pitfalls

1. **the principal's words bleeding into the principal's scores.** Always verify speaker boundaries.

1a. **SUBSTANCE SPEAKER ATTRIBUTION — CRITICAL (locked 2026-04-08).** Any mention of "not going to smoke," "staying sober," "sobriety," "had mushrooms," "microdosing," "not smoking today," or any other substance-related statement MUST be attributed to the correct speaker BEFORE being logged to any scoring table. Mis-attributing the principal's sobriety intention to the principal happened 2026-04-08 and broke her trust — the principal's cannabis use is her MEDICAL BASELINE, not a variable, and framing her as "pursuing sobriety" is a serious no-shame-rule violation. Default assumption: if a substance statement is ambiguous, it is NOT the principal modifying her cannabis baseline (because cannabis IS her baseline — like AG1 or alkaline water). the principal microdoses mushrooms daily and sometimes smokes; the principal does mushrooms only occasionally, not daily. See `aisha-md-daily-brief` skill "CANNABIS IS ASHLEY'S MEDICAL BASELINE" section for the full rule.
2. **Underselling physical activity.** Vigorous intimacy = real cardio. Score it.
3. **VOC/INT inflating from keywords.** Cap at 9.0. Diminishing returns after 5 accomplishments.
4. **Duplicate crons.** ALWAYS audit existing crons before creating. SENTINEL owns daily audit.
5. **"Will fix" instead of fixing.** Fix NOW, same message.
6. **Latuda meal timing.** 350+ cal dinner reminder when logging daytime nutrition.
7. **Saying scores changed without showing them.** Always display the full scorecard table.
8. **Talent gate skipped.** Every agent needs: DB registration, 10 persona variations in agent_personas, full profile, analytics logged. Check ALL of these, don't assume.
9. **Using simple/weighted-average scoring instead of the full coupling engine.** the principal WILL catch this immediately. The correct path is: manually set 1-10 dims from evidence → call `score_from_evidence.compute_twc()` which internally delegates to `calculator.py`'s full 28-pair κ coupling matrix + coherence C + synergy S + formula TWC = η × μ × C × (1+0.5×S). The `--text` flag on `score_from_evidence.py` does NOT produce coupled scores. If your scorecard doesn't show coherence, synergy, and coupling_sum, you used the wrong path. Fixed 2026-05-29 after the principal caught simple scoring being delivered.
