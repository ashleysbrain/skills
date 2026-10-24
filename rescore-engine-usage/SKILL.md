---
name: rescore-engine-usage
description: Use the deterministic Python rescore engine for ALL 8D/TWC rescores. Never do rescore math by hand. Dedicated specialist is CALIBER (FORGE+ARBITER talent-gated 2026-04-08).
trigger: Any time the principal (or a future 8D360 user) sends voluntary evidence that requires rescoring a PRELIMINARY scorecard to FINAL
version: 1.1
---

# Rescore Engine Usage

## 🚨 CRITICAL — WHY THIS EXISTS

On 2026-04-08 a manual rescore produced TWC 68.2 after the principal sent positive evidence (98g protein, 45oz water, deep communication dive, morning follow-through debrief). Manual correction then overshot to 82.0, and the principal caught THAT too with the instinct *"I feel this is high but maybe because the prior scores were so low."* The honest answer, after the double-count fix, is **79.4 Flourishing** for 4/7. the operator agent hand-computed math was wrong twice in one morning. A paying 8D360 user would not have caught either miss.

the principal's exact words: *"This was a ridiculous mistake that should NEVER happen. Especially if we want to monetize off this as a product. Users won't catch what I catch."*

And later: *"I'm not the mathematician here, I need the agents to be."*

This skill exists to make that failure mode structurally impossible. The rules:
1. **NEVER do rescore math by hand. ALWAYS use the engine.**
2. **the operator agent/Claude must NOT handle health scoring directly** — route to AISHA-MD. Health is her lane, not the operator agent's.
3. **Agent spawning for rescore specialists MUST go through the FORGE + ARBITER talent gate.** No stubs, no human names, no shortcuts.

---

## When to Use

- the principal (or any 8D360 user) sends voice/text with additional data about a past day's wellness, health, intimacy, food, sleep, caregiving, med adherence, or emotional work
- A PRELIMINARY scorecard needs to be rescored to FINAL
- The daily standup prep cron needs to finalize yesterday's score before building today's brief
- Any scenario where an existing TWC score needs to be updated with new evidence

**DO NOT** use this skill for:
- Generating the ORIGINAL daily scorecard (that's the `aisha-md-daily-brief` + AISHA-MD pipeline)
- Fleet-agent TWC scoring (that's `proprietary-twc-scoring` → fleet calculator, different engine)
- Weekly reviews (use the weekly scorecard pipeline)

---

## The Mandatory Pipeline

Every rescore follows this exact sequence. No shortcuts. No exceptions.

### Adaptive baseline rule

Before you interpret evidence, check whether the score should be translated through the user's current baseline calibration.

- Use the current baseline seed as a starting point, not a permanent truth.
- Baselines can drift and should be versioned.
- If the input is a voice note or narrative evidence, build a structured evidence payload first, then apply the baseline-aware bridge before the coupled TWC step.
- The bridge should be evidence-first, not keyword-only: transcript adapter signals may raise the 1-10 estimates, then the calibration layer should translate them into the user's current baseline before scoring.
- Persist `baseline_version`, `baseline_source`, and `baseline_bridge` in the daily scorecard when available.
- Do **not** let the presence of the complex coupling engine tempt you into using guessed 1-10 values as final truth; those are only an intermediate estimate.

Support file: `references/adaptive-baseline-bridge.md`

### Step 1: Verify Engine Tests Pass

```bash
python3 ~/your-workspace/hydra-os/scripts/rescore-engine/rescore_engine.py test
```

If ANY test fails, STOP. Do not rescore. Report to the principal. Fix the engine before proceeding.

**CRITICAL**: This verification step is non-negotiable. The rescore engine's correctness guarantee depends on its tests passing. Never proceed with a rescore if the engine tests fail, even if you're "in a hurry" or "confident the engine is fine." The 2026-04-08 double-count bug was caught because tests were run before rescoring.

### Step 2: Build the Rescore Input JSON

Write to `~/your-workspace/health-private/daily/rescore-input-YYYY-MM-DD.json` using this exact shape:

```json
{
  "date": "2026-04-07",
  "preliminary": {
    "date": "2026-04-07",
    "twc": 70.7,
    "8d_base": {
      "psy": 6.8, "phy": 5.0, "env": 7.0, "soc": 8.0,
      "spi": 7.5, "int": 6.5, "voc": 5.5, "fin": 4.5
    },
    "nutrition_composite": 65,
    "nutrition_modifier": 0.985,
    "sexual_health_composite": 88,
    "sexual_health_modifier": 1.060
  },
  "new_evidence": [
    { "type": "nutrition", "detail": "...", "signals": {...} },
    { "type": "sexual_health", "detail": "...", "signals": {...} },
    { "type": "morning_followthrough", "detail": "...", "signals": {...} },
    { "type": "med_adherence", "detail": "...", "signals": {...} },
    { "type": "caregiving", "detail": "...", "signals": {...} }
  ]
}
```

**The preliminary block MUST come from the actual PRELIMINARY scorecard markdown, not from guesswork.** Read `ASHLEY-SCORECARD-YYYY-MM-DD-PRELIMINARY.md` and copy the TWC, 8D base dimensions, and sub-component composites + modifiers exactly.

### Step 3: Populate Evidence Signals

The engine knows these evidence types. Any other type produces a warning and is ignored — do not invent types; extend the engine first.

#### `nutrition`
```json
{
  "type": "nutrition",
  "detail": "Human-readable food log",
  "signals": {
    "protein_grams": 98,       // total grams across the day
    "meals_count": 3,           // distinct eating events
    "water_oz": 45,             // total ounces
    "micronutrients": "AG1"     // non-empty = AG1 or similar baseline taken
  }
}
```

#### `sexual_health`
```json
{
  "type": "sexual_health",
  "detail": "Human-readable description",
  "signals": {
    "intercourse": false,                // true/false — NOT required for strong score
    "communication_depth": "deep",       // "deep" | "normal" | null
    "bond_growth": true,                 // explicit naming of relational growth
    "repair": true,                      // apology, reconnection, boundary-setting
    "gratitude_unprompted": true         // unprompted gratitude is a strong SPI signal
  }
}
```

#### `morning_followthrough`
```json
{
  "type": "morning_followthrough",
  "detail": "Voluntary morning voice memo adding precise detail to yesterday's scorecard",
  "signals": {
    "voluntary": true,          // did the user send this without being asked?
    "precision": "high"         // "high" (specific numbers/events) | "normal"
  }
}
```

This is the credit for *the act of sending the follow-up itself*. It's meta-self-awareness on top of the prior day's integration. Missing this was part of the 4/8 bug.

#### `med_adherence`
```json
{
  "type": "med_adherence",
  "signals": {
    "all_meds_taken": true
  }
}
```

#### `caregiving`
```json
{
  "type": "caregiving",
  "detail": "Dog emergency, child care under fatigue, etc.",
  "signals": {
    "under_impairment": true    // did she do the caregiving while tired/meds/sick?
  }
}
```

### Step 4: Run the Engine

```bash
python3 ~/your-workspace/hydra-os/scripts/rescore-engine/rescore_engine.py rescore \
  --input ~/your-workspace/health-private/daily/rescore-input-YYYY-MM-DD.json \
  --out   ~/your-workspace/health-private/daily/rescore-result-YYYY-MM-DD.json
```

Read the summary on stderr. It will show PRELIMINARY → FINAL, all base dimension lifts with narratives, follow-through credit, and integration bonus preserved.

### Step 5: Verify the Invariant

The engine enforces this but double-check visually:

- If ANY evidence was provided AND final_twc < preliminary_twc → **STOP**. The engine will throw an AssertionError. Report to the principal. Do not write to DB.
- If the delta is much smaller than expected → check whether you missed an evidence type (caregiving, meds, follow-through are commonly forgotten).

### Step 6: Write to the Database

```sql
UPDATE daily_scorecard SET
  twc_score = <engine.final_twc>,
  twc_label = '<engine.final_label>',
  psy = <engine.final_base.psy>, phy = <engine.final_base.phy>, ...,
  nutrition_composite = <engine.final_nutrition_composite>,
  nutrition_modifier = <engine.final_nutrition_modifier>,
  nutrition_label = '<label>',
  sexual_health_composite = <engine.final_sex_composite>,
  sexual_health_modifier = <engine.final_sex_modifier>,
  sexual_health_label = '<label>'
WHERE date = '<target-date>';

UPDATE nutrition_daily SET composite=..., modifier=..., label=... WHERE date=...;
UPDATE sexual_health_daily SET composite=..., modifier=..., label=... WHERE date=...;
```

All numeric values come from the engine's JSON output. **Never adjust them.**

### Step 6.5: Verify Database Write Persisted (Critical — learned 2026-06-02)

After writing to the database, immediately re-read the values to confirm they persisted correctly and were not overwritten by a subsequent process (such as a carryforward cron job). This verification step prevents rescore collisions where legitimate rescores are overwritten by stale data.

```bash
# Example verification (adjust for your specific query needs)
sqlite3 /<workspace> "
  SELECT date, twc_score, twc_label, source 
  FROM daily_scorecard 
  WHERE date = '<target-date>';
"
```

If the values don't match what the engine produced, **STOP** and investigate. Do not proceed to narrative writing or audit logging until the database correctly reflects the engine's output. This check catches the rescore collision pattern where a valid rescore is overwritten by a later pipeline run.

**Additionally, verify label correctness**: Check that labels in nutrition_daily, sexual_health_daily, and daily_scorecard match canonical thresholds:
- Nutrition: >=90 optimal, >=80 strong, >=70 adequate, >=60 gaps, >=50 concerning, <50 critical
- Sexual health: >=85 thriving, >=75 strong, >=65 healthy, >=50 adequate, <50 gaps
- daily_scorecard.nutrition_label and daily_scorecard.sexual_health_label should match their component table counterparts
Correct any mismatches before proceeding.

### Step 7: Write the Rescore Narrative

Produce a markdown section for the standup brief showing:
- PRELIMINARY → FINAL TWC with delta
- Base dimension lifts with per-dimension Δ
- Updated sub-component composites
- Integration bonus + follow-through credit
- No-shame tone (warm, accurate, non-judgmental)

**Use the engine's `lift_audit` array as the source of truth for the narrative.** Every dimension change must be justified from an audit entry.

### Step 8: Append to the Audit Log

```bash
echo "$(date -Iseconds) | rescore | date=YYYY-MM-DD | prelim=XX.X | final=XX.X | delta=+X.X | engine_version=1.0.0" \
  >> ~/your-workspace/health-private/daily/rescore-audit.log
```

---

## Who Runs the Engine

### Option A: Dedicated rescore specialist (preferred for user-facing rescores) — **LIVE as of 2026-04-08**

**CALIBER** is the talent-gated rescore specialist. Profile: `~/your-workspace/hydra-os/intel/agents/profiles/CALIBER-profile.md`. FORGE code: `SCI-RSR-CAL-L7-C5-P11-T5-001`. Model: `anthropic/claude-opus-4-6` at reasoning=high, 118K OMNI context. Passed FORGE + ARBITER talent gate on 2026-04-08 (Deferred Objective #1). Owns EVERY rescore for EVERY day — historical backfill, current finalization, and future scheduled rescores. Spawned by AISHA-MD via delegate_task; never by the operator agent directly (the operator agent routes health to AISHA-MD).

The previous "ARIA" stub at `hydra-os/intel/agents/profiles/ARIA-RESCORE.md` was deprecated because it bypassed the talent gate protocol (no 15-20 role PhDs, no MBTI/Enneagram/OCEAN, no ARBITER approval, and used a name that may collide with humans). It is tombstoned in place — DO NOT reference it. Use CALIBER.

### Option B: AISHA-MD directly (acceptable for routine preliminary→final finalization)

AISHA-MD may invoke the engine directly during normal daily standup finalization, BUT must:
1. Load the `proprietary-twc-scoring` skill first
2. Load this `rescore-engine-usage` skill
3. Run engine tests before invoking rescore
4. Never skip the invariant check

### Option C: Human operator (only for debugging the engine itself)

Direct CLI invocation is allowed only when fixing the engine, adding new evidence types, or calibrating the lift rules. Never for production rescores.

---

## Extending the Engine (New Evidence Types)

When a new category of evidence appears that isn't covered (e.g. workout, creative output, kink scene, therapy session), do NOT hand-patch the math. Instead:

1. Add a new `rules_for_<category>(signals)` function to `rescore_engine.py`
2. Register it in `EVIDENCE_DISPATCH`
3. Write a unit test that asserts the category lifts the expected dimensions
4. Run `python3 rescore_engine.py test` — must pass
5. Document the new type in this skill's "Populate Evidence Signals" section

---

## Calibration History

### Double-Count Bug FIXED in v1.1 (2026-04-08)

**The bug (v1.0):** The engine preserved the PRELIMINARY scorecard's "integration bonus" (the narrative TWC boost AISHA-MD manually added, computed as `preliminary_twc - base_weighted * stacked_modifier`) AND separately lifted the base 8D dimensions for new evidence. When the new evidence overlapped with the evidence that justified the PRELIMINARY integration bonus, the engine double-counted the same signal.

**Real example (the principal 4/7 rescore, caught by the principal):**
- PRELIMINARY TWC 70.7 included a +5.72 integration bonus for "we grew," "I realized a lot," unprompted gratitude, voluntary evening debrief
- v1.0 FINAL rescore credited the SAME evidence a second time as SOC+1.2, SPI+0.5, PSY+1.1 base lifts
- v1.0 result: TWC 82.0 — visibly too high for a no-sleep recovery day
- the principal's instinct: *"Is this correct math and scoring? I feel this is high"* — correct

**The fix (v1.1):** AISHA-MD clamped narrative_lift_contribution to `[0, integration_bonus_raw]` before subtraction, enforcing the invariant `preserved + decomposed ≤ raw` day-agnostically. A vacuous-case guard was added for synthetic peak days where preliminary TWC already sits at/below pre-integration weighted base (nothing to decompose — skip the assertion).

**v1.1 correct answer for 4/7:** **TWC 79.4 Flourishing** (+8.7 from PRELIMINARY 70.7). Raw integration bonus 5.72, decomposed lift 2.17, preserved 3.55. All 7 tests passing including `test_day_agnostic_double_count_property` across 5 synthetic day shapes (recovery, peak, crisis, normal, deadline).

**If you see a rescore produce a number that feels high, first check:** did the engine version update land? Run `python3 rescore_engine.py test` and confirm `test_day_agnostic_double_count_property` passes. If it doesn't, the double-count is back and the engine is stale.

### Triple-Count Bug FIXED in v2.0.0+ (2026-06-13 — Popper Finding 3)

**The bug:** Even after the v1.1 double-count fix, a THIRD credit path survived. When `narrative_coverage_triggered=True` (base lifts covered the integration narrative), the engine still added a halved `followthrough_credit` on top. The same evidence was credited: (1) in base lifts, (2) subtracted from integration bonus, (3) as residual followthrough_credit. Net inflation: ~1.8 points.

**The fix:** Zeroed `followthrough_credit` entirely when `narrative_coverage_triggered=True`. The halving was insufficient — only complete elimination prevents the triple-count. When base lifts already cover the narrative, there is no legitimate additional credit for the same follow-through act.

**Canonical TWC tier labels (synced across ALL files 2026-06-13):**
- 0-100 scale: >=90 Thriving, >=70 Flourishing, >=60 Stable, >=50 Developing, >=40 Strained, >=30 Distressed, <30 Crisis
- 0-1 scale: divide thresholds by 100 (>=0.90 Thriving, >=0.70 Flourishing, etc.)
- Files that must stay in sync: `calculator.py::classify_twc`, `adhd_fusion.py::classify_twc`, `rescore_engine.py` tier thresholds, `build_report.py::tier_label`

### Recovery-Day Ceiling (still under discussion)

A day where the user did not work, did not sleep, missed a meeting, and self-describes as "hit by a bus" probably should NOT land deep in Flourishing (80+) even with strong positive evidence. The 79.4 answer for 4/7 lands right at the Flourishing threshold, which matches intuition. A future v1.2 may add an explicit recovery-day soft ceiling — under discussion with the rescore specialist agent when it ships.

### Triple-Check Required Before Product Launch

Before 8D360 ships to paying users, the engine MUST be audited by:
1. A math/psychometrics specialist (independent — not AISHA-MD, not ARIA)
2. A calibration specialist (real user days, multiple days, check for double-counts)
3. ✅ DONE 2026-04-08: FORGE+ARBITER talent gate for the rescore specialist — CALIBER is live, see `~/your-workspace/hydra-os/intel/agents/profiles/CALIBER-profile.md`

This is the principal's explicit ask and a hard gate on product monetization.

---

### Pitfalls
## Pitfalls
1. **Hand-computing the math "just this once."** Never. The reason this skill exists is because hand-computed math produced the 4/8 bug. Always use the engine.

2. **Early-morning nutrition evidence (learned 2026-05-27).** When processing a morning standup (before food has been eaten), do NOT submit a `nutrition` evidence entry with 0 protein / 0 meals. The engine will correctly recompute the nutrition composite from those signals, dropping it from the carryforward value (e.g. 88.5 → ~40), which triggers the invariant violation (positive evidence in other dimensions can't overcome the composite drop). Instead, omit the nutrition evidence entirely and let the carryforward composite stand until real food data arrives later in the day.

3. **Skipping followthrough credit.**

3. **Forgetting caregiving/med adherence.** These are common positive signals users don't think of as "data." If the user mentions taking care of a pet/child/partner, or taking meds on a hard day, include those evidence types.

4. **Using the engine output as "a suggestion."** It's not a suggestion. It's the authoritative answer. If you override it, the override must be explicit, justified, and logged.

5. **Rescoring the wrong direction on ambiguous evidence.** If evidence is genuinely neutral or mixed, omit it — don't guess at lift values. The engine will leave the score unchanged, which is correct.

6. **Writing to DB before running the invariant check.** Always: engine → check → DB. Never: DB → then check.

7. **Truncating the audit trail.** Every lift, with its narrative, goes in the scorecard. Silent shifts break trust and train the user away from honest scoring.

8. **Including same-day partial nutrition in a morning rescore.** When rescoring a day that's still in progress (e.g., 8AM standup, no meals yet), do NOT include a `nutrition` evidence entry with zero protein/meals. The engine will compute a lower nutrition composite from the signals, which drags down the stacked modifier and can violate the invariant (positive evidence → lower TWC). The carryforward nutrition composite from yesterday is still valid until real food data arrives. Omit the nutrition evidence type entirely for early-morning same-day rescoring — add it later when lunch/dinner data comes in.

9. **Rescore engine crashes on None composites (discovered 2026-05-29).** When `nutrition_composite` or `sexual_health_composite` is `null`/`None` in the preliminary block, the engine throws `TypeError: '>=' not supported between instances of 'NoneType' and 'int'` at line 549. Always provide numeric defaults (e.g., 65.0 for composite, 1.0 for modifier) even when no real sub-component data exists yet. This commonly happens for early-morning same-day scores before any meals or encounters.

10. **Unregistered evidence types produce warnings, not errors — signal is left on the table.** As of engine v2.0.0, `self_care_routine` and `sleep_quality` are NOT registered in `EVIDENCE_DISPATCH`. The engine logs them as warnings and skips them. This means a full morning routine (shower, skincare, red light therapy, dance movement, meditation attempt) and excellent sleep (melatonin + magnesium, phone off, dark room) produce ZERO lift in the engine output. The workarounds: (a) map the signal into registered types (med_adherence captures some PHY/PSY lift), or (b) extend the engine with new lift rules for these categories. Path (b) is the right long-term fix — see "Extending the Engine" section.

11. **Pipeline coverage gap (Critical)** — As of 2026-06-13, only 4/31 days (13%) have scores in the daily_scorecard. If scoring is missing scores for recent days, do not backfill automatically. Instead, check for available standup transcripts or other evidence sources for those dates and process them through the scoring pipeline before considering the day complete. Missing days should remain blank only if no evidence exists. **As of 2026-06-17 AUDIT-ALGO verification: 0/7 days with real scores in the last week, 4/30 days total with real scores (excluding cron/carryforward). Reverified 2026-06-20 AUDIT-ALGO: 0/7 days with real scores in last week, 4/30 days total (excluding cron/carryforward).**

12. **No baselines table in DB (confirmed 2026-06-07 AUDIT-ALGO)**. The drift calculation references a "baseline" value (e.g., 28.1) but `sqlite_master` has no table matching `%baseline%`. The baselines are stored in a JSON file at `~/.sibling-agent/workspace/memory/principal-8d/baselines.json`, not in the scoring DB. When any audit or pipeline claims "drift from baseline", verify whether the baseline source is the JSON file, a computed anchor, or an invented figure. **As of 2026-06-17 AUDIT-ALGO verification: baselines.json exists but contains "twcBaseline": null, making drift calculation impossible.** If the baselines.json file contains "twcBaseline": null or lacks a numeric twcBaseline value, auditors should report that drift calculation is not possible rather than attempting to compute or invent a baseline value.

13. **Rescore collision: live case May 29, 2026 (confirmed 2026-06-04 AUDIT-ALGO).** The rescore audit log shows THREE rescore attempts for May 29: (1) 41.5 → 55.99 via calculator_v3, (2) 55.99 → 72.5 via rescore engine v2.0.0, (3) complex_rescore to 57.64 via calculator_v3. Despite all three, the DB still stores 28.36 (Crisis, source=transcript, original parse value). NONE of the rescore results persisted. Root cause: either the DB writes failed silently, or a subsequent pipeline run (e.g. carryforward cron) overwrote the rescore with the original transcript-parsed value. This is a concrete instance of the Step 6.5 verification gap — the verification step was either skipped or not persisted. The file artifacts exist (`rescore-result-2026-05-29-v2.json` shows final=72.5) but the DB was never updated to match. **Lesson: Step 6.5 (verify DB write persisted) is not theoretical — it has already failed in production. Always re-read the DB after writing.**

14. **Database write verification is critical** — After any rescore write to the database, immediately re-read the values to confirm they persisted correctly (Step 6.5). This prevents rescore collisions where legitimate rescres are overwritten by stale data from subsequent pipeline runs. Never skip this verification step.

15. **Scoring methodology validation** — Always validate scoring algorithms against evidence and domain expertise. Simple sum models require justification; consider coupling terms and weighted contributions. Arbitrary parameters (like decay rates) should be evidence-based or configurable. Missing dimensional interactions can oversimplify complex systems. Inclusivity and bias review is essential for broad applicability. Gamification elements should meaningfully connect to actual dimension improvement, not just provide extrinsic motivation.

16. **Tier label scale mismatch across files

17. **Triple-count via followthrough_credit (Popper Finding 3, 2026-06-13).** Even after the v1.1 double-count fix, `followthrough_credit` was still being added (halved) when `narrative_coverage_triggered=True`. This created a third credit path for the same evidence. The halving was insufficient — it must be ZEROED when base lifts cover the narrative. If you see followthrough_credit > 0 when `narrative_coverage_triggered` is True, the triple-count is back.
19. **CRITICAL IMPLEMENTATION GAP: Coupling terms not active in computation (learned 2026-06-04, verified 2026-06-17 AUDIT-ALGO)** — Despite the proprietary formula documenting significant coupling coefficients (PSY↔INT: 0.85, PHY↔VOC: 0.78, SOC↔SPI: 0.72, ENV↔PHY: 0.68), the current implementation in the scoring system does NOT apply these coupling terms to the TWC calculation. This means Layer 3 (cross-dimensional coupling) has zero effect on scores regardless of dimension values. All scoring results should be interpreted with this limitation in mind.

---

## Files and Paths

- Engine: `~/your-workspace/hydra-os/scripts/rescore-engine/rescore_engine.py` (v2.1.0 as of 2026-10-20 — adds native `second_order` output block; scoring math unchanged from v2.0.0)
- Second-order sensitivity module (v2.1.0 native output, T-261020-0028, HIP referral gwtSE6sd): `~/your-workspace/hydra-os/scripts/rescore-engine/hessian_sensitivity.py` — direct symmetric central-difference Hessian of the score surface (no autodiff), per-dimension curvature/gradient, tau_recovery per dimension, tipping-proximity flag (tau > 2.0 = upward sensitivity halved near ceiling/TWC cap), and a measured-vs-documented coupling check that makes pitfall 19 observable per-rescore. Feeds physics-gate CONCEPT 4: `physics_gate.in_stage(recovery_times=[<daily tau series>])`. CLI: `python3 rescore_engine.py sensitivity --input <rescore-input.json>`. Its 10-test battery runs inside `rescore_engine.py test` (7 engine + 10 sensitivity).
- Engine tests: `cd ~/your-workspace/hydra-os/scripts/rescore-engine && python3 rescore_engine.py test` — all 7 must pass
- Rescore specialist profile: `~/your-workspace/hydra-os/intel/agents/profiles/CALIBER-profile.md` (CALIBER, FORGE+ARBITER talent-gated 2026-04-08). Deprecated stub at `~/your-workspace/hydra-os/intel/agents/profiles/ARIA-RESCORE.md` — DO NOT USE.
- Rescore inputs: `~/your-workspace/health-private/daily/rescore-input-YYYY-MM-DD.json`
- Rescore outputs: `~/your-workspace/health-private/daily/rescore-output-YYYY-MM-DD.json`
- Audit log: `~/your-workspace/health-private/daily/rescore-audit.log`
- DB: `/<workspace>`
- Product directive (external-content audit agent, captured 2026-04-08): `~/your-workspace/hydra-os/intel/product-directives/external-content-audit-agent-2026-04-08.md`
- Related skills: `proprietary-twc-scoring`, `aisha-md-daily-brief`, `daily-standup-preparation`, `standup-transcript-to-8d360`, `subagent-anti-timeout-patterns` (Pattern 10)
- Verification script: `~/your-workspace/hydra-os/scripts/rescore-engine/scripts/verify_rescore_persistence.sh` - Helper script to verify database writes persisted after rescore (usage: `./verify_rescore_persistence.sh <date> <expected_twc>`)

**Last verified 2026-06-23 by AUDIT-ALGO**: INCOMPLETE — system resource pressure prevented full independent verification. Previous confirmed findings: rescore engine tests pass (7/7), nutrition engine tests pass (22/22), sexual health engine tests pass (43/43); pipeline coverage 0/7 days real scores last week, 4/30 total. See `proprietary-twc-scoring` skill for full audit methodology.

## The Guarantee

If you follow this skill exactly, it is mathematically impossible for positive evidence to produce a lower score. The engine's unit tests enforce that guarantee every time it runs. If the guarantee breaks, the engine refuses to complete the rescore.

This is the foundation of user trust in 8D360 as a product. Protect it.

This is the foundation of user trust in 8D360 as a product. Protect it.
