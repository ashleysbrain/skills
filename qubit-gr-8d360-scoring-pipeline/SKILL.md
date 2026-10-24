---
name: qubit-gr-8d360-scoring-pipeline
description: Build and maintain the Qubit GR / 8D360 universal health scoring system — personal scoring for the principal (middle-out MVP) and universal platform for all users. Covers expert panels, experience databases, scoring calibration, and the talent gate process for scoring work.
tags: [qubit-gr, 8d360, scoring, health, wellness, calibration, expert-panel, experience-database]
version: 1.0
---

# Qubit GR 8D360 Scoring Pipeline

## When to Use
- Building or updating 8D360 scoring algorithms, calibrations, or formulas
- Designing a new condition-specific subscore or sidecar metric (for example ADHD / executive-function support scoring)
- Designing *diagnosis-gated* condition subscores that are optional, measure current burden/impairment rather than diagnosis presence, and stay separate from proxy/functioning scores
- Spawning expert panel agents to review scoring science
- Building the experience/activity database
- Designing a universal **activity ontology** and master score system that ranks human actions by measurable health impact across all 8 dimensions
- Creating or updating a **master database of human activities** with evidence-weighted scoring, personalization, and versioned rules as science evolves
- Defining how to score common daily actions such as water intake, bathing/hygiene, nutrition, outdoor exposure, physical activity, sleep support, social behaviors, spiritual practices, and recovery behaviors
- Working on the principal's personal scoring (middle-out MVP)
- Generalizing scoring for other users
- ANY scoring calibration work — NEVER do this solo, always with expert panel

## Critical Rules (Learned 2026-03-31)

### 1. Personal Health Data → AISHA-MD, NEVER AISHA
Any personal health/lifestyle data from the principal (meals, sleep, exercise, intimate activity, mood, hydration, pain, etc.) ALWAYS routes to AISHA-MD. AISHA is fleet lead. AISHA-MD is personal health. They are different.

### 2. Scoring Calibrations NEVER Solo
the principal explicitly said: scoring algorithms need a full expert panel — mathematicians, physicists, psychologists, biologists, etc. I built calibrations alone and was corrected. Always:
- File talent request through FORGE+ARBITER
- Spawn specialists with unique domain expertise
- Get panel consensus before any calibration goes to production
- Current panel: 19 agents (7 original + 12 expanded)

### 3. No "Dr." Prefix on AI Agents
AI agents must never be confused with real medical providers. Use codenames only (CIRCADIA, REUPTAKE, EIGENSTATE, etc.)

### 4. Full 17-Section Profiles Required
Every agent spawned needs the full master profile treatment — 17 sections, 10 personality variations, registered in agent_personas DB table, filled by specialist agents (FORGE skeleton → 8 specialists fill). Not skeleton profiles.

### 4b. Spawn-to-calibration gate
If a scoring blueprint, calibration pack, or implementation spec introduces new scoring agents, the sequence must be explicit:
1. define the task family or scoring lane
2. choose the base model or operating mode
3. assign role and persona
4. set credential targets / bands
5. verify process familiarity
6. verify evidence-domain familiarity
7. record spawned_by and spawned_at
8. register the agent
9. mark calibration authorization
10. only then calibrate or score

A draft roster, profile stub, or unregistered agent does not count as calibration-ready.

### 5. Qubit GR Content Must Be Universal
Remove ALL personal/the principal-specific references from Qubit GR platform docs. No ADHD/BP2 mentions, no personal baselines, no climbing. The platform adapts to ANY human. the principal's personal scoring is separate (health-private/ directory).

### 5b. Personal-condition fields belong in a separate personalization layer
If a draft business-scoring doc contains diagnosis-specific or operator-specific fields (for example ADHD, BP2, chronic pain, or personal medication timing), move them out of the core business score and into a separate operator/personalization layer or personal-health lane. The core business score must describe the company, not the founder or user profile. This separation also applies when converting narrative methodology into an implementation spec: core model = business only; personalization = bounded overlay; personal health = separate system.

### 5c. Cross-domain bridge summaries
When business scoring must interconnect with human 8D or AI 8D systems, accept only summarized bridge inputs at the boundary:
- overall score
- confidence
- trend
- provenance hash

Never route raw human health details or raw AI internals into the business core. The core may use the bridge summary as an advisory modifier only; all detailed records remain in their own private stores.

### 5c. Cross-domain bridge summaries
When business scoring must interconnect with human 8D or AI 8D systems, accept only summarized bridge inputs at the boundary:
- overall score
- confidence
- trend
- provenance hash

Never route raw human health details or raw AI internals into the business core. The core may use the bridge summary as an advisory modifier only; all detailed records remain in their own private stores.

### 5d. Canonical architecture companion
When the bridge layer is introduced or revised, create or update the canonical interconnect architecture note in the repo and mirror the same boundary rules into Obsidian notes and MOCs so the source of truth stays aligned across systems.

### 6. QA Mandatory on External Content
ALL external-facing content goes through QA per WRITING-WORKFLOW.md. Zero AI telltales, zero em dashes, human voice only.

### 7. Analytics on Everything
Every task, delegation, QA review, spawn — logged in agents.db tables (task_analytics, delegation_tracking, talent_gate_log, qa_tracking, daily_productivity).

## Key Files
- Health profile: ~/your-workspace/health-private/principal-health-profile.md (LOCAL ONLY)
- Calibration: ~/your-workspace/hydra-os/memory/principal-8d/calibration.json (DRAFT — needs panel review)
- Transcript analyzer: ~/your-workspace/hydra-os/scripts/transcript-analyzer.py
- Experience DB schema: ~/your-workspace/hydra-os/products/qubit-gr/database/schema.sql
- Experience DB seed: ~/your-workspace/hydra-os/products/qubit-gr/database/seed.sql
- Scoring methodology paper: ~/your-workspace/hydra-os/products/qubit-gr/research/SCORING-METHODOLOGY-UNIVERSAL.md
- 8D360 PRD: ~/.sibling-agent/workspace/intel/wellness/8D360-PRD.md
- Config: ~/your-workspace/hydra-os/memory/principal-8d/config.json
- Expert panel assignments: ~/.sibling-agent/workspace/intel/agents/talent-requests/processed/8D360-PANEL-ASSIGNMENTS-2026-03-31.md
- Expanded panel: ~/.sibling-agent/workspace/intel/agents/talent-requests/processed/QUBIT-GR-EXPANDED-PANEL-2026-03-31.md

## Maslow 7-Tier Mapping
1. Physiological → PHY
2. Safety → ENV + FIN
3. Love & Belonging → SOC
4. Esteem → VOC + INT
5. Cognitive → INT + PSY
6. Aesthetic → ENV + SPI
7. Self-Actualization → SPI + PSY

## Cron Deduplication Rule
Before creating ANY new cron, check ALL existing crons in both the operator agent and OpenClaw. the principal caught duplicate audit crons on 2026-03-31. SENTINEL is THE single daily audit. Don't duplicate its work.

## Category Scoring Implementation Pattern (Added 2026-04-01)

New categories (beyond core 8D) follow this physics-based modular pattern:
1. **Panel functions**: Each panel (3-6 per category) is a separate function returning 0-100
2. **Composite**: Weighted sum of panel scores (weights from LIBRA validation)
3. **Modifier function**: Maps 0-100 composite → 0.85-1.15 multiplier range
4. **apply_to_dimensions()**: Multiplies base 8D360 dimension scores by the modifier, clamped 0-100
5. **daily_quick()**: Function accepting minimal user inputs → full composite output

**Implemented engines:**
- `8d360-nutrition-engine.py` — 7 panels: protein, meal timing, meal frequency, glycemic, hydration, gut, med-food. Affects PHY, PSY, INT, VOC. Mod range: 0.85-1.15.
- `8d360-sexual-health-engine.py` — 6 panels: satisfaction, bonding, somatic, regulation, communication, diversity. Includes ENM/CNM fairness adjustment. Affects SOC, PHY, PSY. Mod range: 0.88-1.12.
- `8d360-category-workflow-template.py` — 7-step template for any future category.

## Universal Scoring Contract (Added 2026-05-25)

When designing any new subscore or calibration pack, use a *person-specific, interaction-aware* architecture:

- **Patient 0 is a product-design reference, not a universal calibration anchor.** Use it as the prototype and worked example, not the default for everyone else.
- **Each human gets their own calibration profile.** Thresholds, priors, and interpretation layers should be versioned per person.
- **Separate the layers.** Keep raw evidence, canonical score, confidence/uncertainty, normalized display score, and interaction terms distinct.
- **Model synergy explicitly.** Positive and negative cross-dimension effects should be represented as named interaction rules, not hidden inside the base score.
- **Use bounded cross-feed.** A domain can influence multiple dimensions, but the effect must be explicit, capped, and justified by evidence.
- **Avoid one-size-fits-all baselines.** A worked example can inspire the design, but it should not become a universal anchor.
- **Confidence is mandatory for every TWC and standalone score.** Always emit a first-class confidence value alongside the score, even when the score is stable.
- **Confidence should generally increase as supporting data accumulates.** More passive evidence, better source agreement, recency, and baseline fit should raise confidence until it plateaus; sparse, stale, or conflicting evidence should lower it.
- **Passive-first, manual-light by default.** Scores should compute from background evidence first and only ask for micro-check-ins when confidence is too low or the data are contradictory.

## Universal Activity Master Database Pattern (Added 2026-05-26)

When the task is to build a master activity scoring database for all human actions, apply these rules:

- **Score the activity, not the marketing claim.** Use physiological or behavioral impact, not buzzword status. Example: regular water should not be outranked by alkaline water unless evidence supports a specific indication.
- **Use measurable units.** Every activity needs a unit (minutes, repetitions, ounces, servings, exposures, sessions, etc.) and a dose-response rule.
- **Rank by expected health impact.** The highest scores should go to behaviors with the strongest expected benefit, not the most trendy or emotionally appealing behaviors.
- **Personalize by baseline and context.** A user with a dehydration risk, athletic load, dietary restriction, disability, or culture-specific constraint should get a different weight than a generic user.
- **Prevent double counting.** If two activities contribute to the same outcome, use overlap tags and bounded interaction terms.
- **Keep a game layer separate from the truth layer.** The score should motivate behavior change, but the underlying health-impact score must remain scientifically defensible.
- **Version every rule.** Science evolves; the activity catalog, evidence grades, and scoring formulas must all be versioned and re-runnable.
- **Start with the highest-impact behaviors first.** Seed the ontology with the strongest universal levers: sleep, movement, diet quality, hydration, stress regulation, outdoor exposure, and social connection.
- **Add low-level daily actions as subordinate nodes.** Water intake, bathing, oral care, meal timing, sunlight, walking, stretching, meditation, prayer, and cleaning behaviors should roll up into broader categories rather than being scored in isolation with inflated importance.
- **Use evidence grades.** Each activity must carry STRONG / MODERATE / WEAK evidence labeling and a short rationale.
- **Track staleness.** If science changes or evidence becomes mixed, mark the rule as provisional until reviewed.
- **Store intent separately from effect.** A “healthy-sounding” action is not automatically high value if outcome evidence is weak.

## Evidence-Linked Schema Pattern (Added 2026-05-26)

When the work is moving from scoring philosophy into database schema or implementation specs, use this structure:

- **Separate truth from presentation.** Keep `base_impact_score` as the evidence-grounded scientific layer and `display_score` as the user-facing motivational layer.
- **Link every rule to sources.** Use versioned source records, topic records, and rule-to-source join tables so any score can be traced back to its evidence.
- **Version the rule itself, not just the source.** A rule change should produce a new score version with timestamps, status, and reason for change.
- **Model interactions explicitly.** Overlap, synergy, and suppression must live in a dedicated interaction table or matrix instead of being hidden inside the base formula.
- **Personalization belongs in a bounded overlay.** User-specific modifiers should never rewrite the underlying scientific rule; they should only adjust the displayed or contextual score within caps.
- **Track update cycles.** Every science refresh should be logged as an update cycle with topics reviewed, sources added, rules changed, and stale rules flagged.
- **Keep aliases separate from canonical activities.** Map synonyms, product names, and marketing terms to a canonical activity so the ontology stays clean.
- **Prefer deterministic math plus auditable SQL.** The schema should support reproducible rescoring, historical replay, and regression checks as science updates.
- **Design for future science drift.** If a source becomes outdated or evidence changes, the database should preserve historical truth while allowing the active rule to evolve.


## ADHD / Executive Function Subscore Pattern (Added after patient-0 draft)

When designing a new ADHD / executive-function subscore, use a **profile-first, score-second** approach:

### Intake flow
1. Ask a short onboarding set to identify the user's presentation profile.
2. Allow multiple tags instead of forcing one label.
3. Use the profile only to adapt weights and interpretation, not to diagnose.

### Recommended profile tags
- inattentive-leaning
- hyperactive/impulsive-leaning
- combined
- activation-dominant
- time-blindness-dominant
- emotional-regulation-sensitive
- hyperfocus/transition-sensitive
- sleep-sensitive

### Daily scoring domains
Use 8 ADHD-specific domains:
1. Initiation
2. Sustained attention
3. Working memory / organization
4. Time awareness
5. Transitions
6. Impulse control
7. Emotion regulation
8. Sleep-context sensitivity

### Math pattern
- Map each response to a friction value `F_d` in `[0, 10]`
- Convert to support score `S_d = 10 - F_d`
- Compute `ADHD_Score = clamp(Σ(w_d * S_d), 0, 10)`
- Keep weights bounded and sum to 1.0
- Adapt weights by profile, but do not let any weight fall below 0.03 or above 0.25

### Confidence and smoothing
- Report confidence separately from the score
- Also compute 7-day EWMA trend and 30-day baseline
- If intake is sparse or inconsistent, mark the result provisional

### Integration rule
- Treat the ADHD score as a **sidecar** to TWC/8D, not a duplicate of PSY/INT/VOC
- Do not reuse evidence already counted in other subscores
- If coupled into TWC later, use only a small bounded modifier so it cannot dominate core dimensions
- The ADHD score should explain *why* other dimensions changed, not silently create multiple score shifts

### Safety rule
- No diagnosis language
- No claim that the score replaces a clinician
- Keep the framing practical, non-shaming, and support-oriented

**ENM/CNM fairness rule**: Sexual health scoring does NOT penalize or reward number of partners. ENM context factor evaluates only communication quality and jealousy management. Partner count is neutral.

## Score-to-Modifier Physics
The modifier function uses this pattern:
```
mod = clamp(lo, hi, center + range * ((composite/100) - 0.50))
```
Where center = (lo+hi)/2 and range = (hi-lo)/2. A 50/100 composite = 1.0x multiplier (no change). Above 50 boosts dimensions. Below 50 reduces them.

## Data Pipeline Gap (Critical Issue)
- Daily data pipeline severely broken: only 4/30 days have real scores in the last 30 days (per SMI 2026-06-07)
- Nutrition coverage: only 3/30 days
- Sexual health coverage: only 2/30 days
- EF COMPASS coverage: 21/30 days (relatively better)
- This represents a severe data gap that must be addressed immediately

## Verification and Auditing Best Practices (Added 2026-06-14)

When assessing scoring system maturity or verifying SMI-like claims, use these verification techniques:

### Engine Completeness Verification
- Don't just check if engine files exist - verify they're >500 bytes (to avoid stubs)
- Check if engines are actually imported/called in the main scoring pipeline
- For interaction matrices: verify scripts actually READ the matrix during scoring, not just that it's defined in DB
- Count actual working engines vs. defined/planned ones

**DEAD CODE DETECTION (learned 2026-07-19 AXIOM audit):**
A database table or data structure can be FULLY POPULATED yet produce ZERO effect in production if no scoring script actually reads it. AXIOM gave full credit (28/28 rows) for interaction matrix existence, but search_files showed ZERO scripts using 'interaction_matrix' pattern. This is DEAD CODE — defined but never called. Verification pattern:
1. Check if the structure EXISTS in DB/FS (e.g., `SELECT COUNT(*) FROM interaction_matrix`)
2. Search codebase for READ usage: `search_files(pattern='<structure_name>', path='/scripts', target='content')`
3. Zero matches = dead code, credit = 0, regardless of how well-defined the structure is
4. Example from 2026-07-19: 28 pairs defined, 0 scripts reading them = -7 SMI points for Engine Completeness

### Test Coverage Verification
- Actually RUN test suites, don't just check for test file existence
- Verify tests are meaningful and cover core functionality
- Check if OTHER engines that should have tests actually DO have test functions
- Distinctly count test PASSES vs just presence of test code

### Validation Coverage Verification
- Verify VERITAS/audit agents actually EXIST in agent database with appropriate non-Anthropic models
- Check calibration files for independent review/validation stamps (not just existence)
- Verify universal methodology documents are actively USED in scoring computations
- Look for evidence of independent panel review/sign-off

### Data Quality Verification
- Count REAL scored days (exclude cron/carryforward placeholders)
- Verify each data source table has actual entries for recent days
- Check activity database for balanced dimension coverage (no zero-count dimensions)
- Verify evidence richness across all scoring components

### Production Readiness Verification
- For multi-user claims: check partner databases for actual observations/scores (not just schema)
- For API/export claims: verify actual working endpoints/scripts exist and are used
- Check for real-world usage evidence, not just architectural plans
- Validate deployment/maintenance procedures with actual evidence

## Panel-Per-Algorithm Architecture (Built 2026-04-05)

Every scoring algorithm gets a dedicated SME team with domain experts + mathematician + physicist + ethicist. Plus an independent AUDIT PANEL on a DIFFERENT AI MODEL.

### Existing Teams (fully or partially staffed)
- **Sexual Health Panel (FULLY STAFFED):** EROS, TANTRA, KINSEY, BONDING + LIBRA-SX, FLUX-SX, ETHOS-SX + panel variants (EROS-SX, TANTRA-SX, BONDING-SX)
- **Nutrition Panel:** LIBRA-NUT, FLUX-NUT, ETHOS-NUT (led by HALO)
- **Specialized:** CIRCADIA (circadian), REUPTAKE (addiction)

### Teams Needing Spawn (14 agents via FORGE+ARBITER talent gate)
- **8D Core/TWC Panel:** LIBRA-8D, FLUX-8D, ETHOS-8D (math/physics/ethics for nonlinear mapping, geometric mean, PCM, CSI, deficit penalty)
- **Kink Panel:** LIBRA-KNK, FLUX-KNK, ETHOS-KNK (KAE curves, biomechanics, consent ethics)
- **Database/Schema Panel (added 2026-04-06):** LIBRA-DB, FLUX-DB, ETHOS-DB (schema math validation, physical plausibility of derived metrics, data minimization + retention ethics)
- **EF COMPASS Panel:** COGNOS (neuropsychologist), LIBRA-EF, FLUX-EF, ETHOS-EF (evidence weighting, pharmacokinetics, clinical safety)
- **VERITAS Audit Panel (NON-ANTHROPIC ONLY, SPAWNED 2026-05-XX):** VERITAS-MATH (Gemini), VERITAS-PHYS (Gemini), VERITAS-STAT (Qwen), VERITAS-ETHICS (DeepSeek)

### ✅ VERITAS Audit Panel Status (Updated 2026-05-31)
The 4-discipline algorithmic audit panel (VERITAS-MATH/PHYS/STAT/ETHICS on non-Anthropic models) NOW EXISTS in agents.db and is actively producing integrity reports. Verify current status with:
```
sqlite3 ~/.sibling-agent/workspace/intel/agents/database/agents.db "SELECT code, display_name, primary_model FROM agents WHERE display_name IN ('VERITAS-MATH','VERITAS-PHYS','VERITAS-STAT','VERITAS-ETHICS')"
```
Returns four rows showing the panel is active with appropriate non-Anthropic models.

The panel is producing regular VERITAS-ALGO INTEGRITY REPORT entries in the algorithm integrity log, confirming active validation coverage.

### Regular Integrity Check Procedure (Bi-daily)
Following the VERITAS-ALGO audit protocol, this procedure should be run every 12 hours to ensure algorithmic integrity.

**Quick reference:** The `proprietary-twc-scoring` skill has a copy-pasteable runbook at `references/veritas-algo-audit-runbook.md` with the exact terminal sqlite3 commands for each step. Use it instead of reconstructing queries each run.

1. **Self-referential loop check** (PRIORITY): 
   - Query EF tracker observations for evidence that references scores rather than behavior:
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
   - For each result, classify as:
     - **SELF-REFERENTIAL** (must flag): Evidence IS a score number, a trend description, or a domain comparison. Examples: "Activation at 0.7 — new tracking low", "COMPASS Activation at 1.0 for two weeks", "Activation score drifted from 2.5 to 1.7"
     - **LEGITIMATE** (keep): Evidence describes actual BEHAVIOR even if it mentions scores. Examples: "deliberately structures sub-3-minute commitments to reduce activation barrier", "started working on algorithms before 5 AM"
   - **Apply false-positive classification rule**: If observation describes BUILDING, DESIGNING, MAINTAINING, DEBUGGING, or WORKING ON the scoring system, it's legitimate behavioral evidence — do not flag as self-referential
   - If self-referential observations found: delete them, re-run `ef_tracker.py score`, sync corrected scores to unified health DB, and report before/after scores

2. **Engine test verification**: 
   - Run all test suites and verify they pass:
     ```bash
     cd ~/your-workspace/hydra-os/scripts/rescore-engine && python3 rescore_engine.py test
     cd ~/your-workspace/hydra-os/scripts && python3 test-nutrition-engine.py
     cd ~/your-workspace/hydra-os/scripts && python3 test-sexual-health-engine.py
     ```
   - All tests must pass. If any fail, STOP and report — do not proceed with other integrity checks.

3. **Data integrity validation**:
   - **Modifier staleness**: Verify nutrition_modifier and sexual_health_modifier match canonical formula `0.85 + 0.30 * (composite/100)^2.5` (clamped to 0.85-1.15 for nutrition, 0.88-1.12 for sexual health in daily_scorecard)
   - **TWC recomputation**: For each day with stored TWC, verify `stored_twc ≈ [sum(w_i * D_i) + sum(kappa_ij * D_i * D_j for all i != j)] × sqrt(nutrition_modifier × sexual_health_modifier)` using personal weights (PSY 0.18, PHY 0.16, ENV 0.08, SOC 0.12, SPI 0.12, INT 0.10, VOC 0.14, FIN 0.10) and coupling coefficients (PSY↔INT: 0.85, PHY↔VOC: 0.78, SOC↔SPI: 0.72, ENV↔PHY: 0.68). **Note**: In the agent fleet system, coupling terms are currently not active in the computation (known gap), so verification should use only the weighted sum portion for fleet scores. For the principal's personal scoring (middle-out MVP), the full formula with coupling terms should be used.
   - **Interaction matrix validation**: Verify that the interaction_matrix values in the database match the proprietary specification coefficients for key couplings (PSY↔INT: 0.85, PHY↔VOC: 0.78, SOC↔SPI: 0.72, ENV↔PHY: 0.68). Significant deviations indicate implementation gaps that must be addressed.
   - **Pipeline coverage**: Check for 7-day gaps in daily_scorecard and ef_compass_daily entries (gap indicates data availability issue, not necessarily corruption)
   - **Phantom TWC**: Check for TWC values on carryforward rows without legitimate 8D data
   - **EF COMPASS sync**: Verify column order and natural capacity scaling (divide EF tracker natural_capacity_raw by 10 before inserting)

4. **Patient 0 evidence audit**: 
   - Review activation/action observations for:
     - Algorithm development work counting as activation evidence (designing scoring architectures, building agent systems, creating cron jobs, debugging scoring pipelines)
     - Broad evidence lens beyond GitHub commits (agent design, conversation-based system building, document creation, cron creation, skill authoring, architecture decisions)
     - Distinguishing deliberate rest from activation failure (protected recovery days should score activation at 4-5, not 1-2)
     - Proper classification of system work vs score reference

5. **Drift detection**: When algorithm-integrity-baseline.json exists, compare latest scores against baseline values and flag significant deviations.

6. **Integrity logging**: Record findings in `algorithm-integrity-log.md` using the standard format:
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
   Log to: `~/your-workspace/health-private/algorithm-integrity-log.md`

20. **Extreme TWC provenance verification** (when TWC is new system extreme):
   - If integrity audit confirms a TWC value is mathematically correct but the value is a new system extreme (Crisis <30 or Thriving >85):
     - Verify the `source` column in daily_scorecard
     - Verify original input data (transcript, check-in, etc.) still exists and matches
     - Flag for human review if value falls in Crisis (<30) or Thriving (>85) tier
     - Mathematical correctness does not guarantee input correctness — extreme values may indicate bad data parse rather than genuine extreme day

21. **Scoring methodology validation** — Always validate scoring algorithms against evidence and domain expertise. Simple sum models require justification; consider coupling terms and weighted contributions. Arbitrary parameters (like decay rates) should be evidence-based or configurable. Missing dimensional interactions can oversimplify complex systems. Inclusivity and bias review is essential for broad applicability. Gamification elements should meaningfully connect to actual dimension improvement, not just provide extrinsic motivation.

## References
- Health Scoring Daily Pipeline skill: Database Integrity Verification Procedure section
- EF COMPASS Self-Referential Loop Prevention (learned 2026-05-27)
- VERITAS-ALGO integrity check findings recorded in algorithm-integrity-log.md
- VERITAS-ALGO integrity check procedure (2026-06-10): references/integrity-check-procedure-2026-06-10.md
- Interaction matrix findings (2026-06-13): references/interaction-matrix-findings-2026-06-13.md
- XP/coherence multiplier population stress test (2026-07-07): references/xp-coherence-stress-test-2026-07-07.md — Monte Carlo technique for validating formula gaps at scale. Worked example: the 4.7x coherence gap claim did not replicate under 50K-user simulation (actual 3.48x worst case). Always Monte Carlo test flagged gaps before accepting as blockers.
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
Classify each result:
- **SELF-REFERENTIAL** (must flag): Evidence IS a score number, trend description, or domain comparison
- **LEGITIMATE** (keep): Evidence describes actual behavior even if mentions scores
Apply false-positive classification rule: if observation describes BUILDING, DESIGNING, MAINTAINING, DEBUGGING, or WORKING ON the scoring system, it's legitimate behavioral evidence

#### 2. Engine test verification
```bash
cd ~/your-workspace/hydra-os/scripts/rescore-engine && python3 rescore_engine.py test
# All 7 tests must pass
cd ~/your-workspace/hydra-os/scripts && python3 test-nutrition-engine.py
cd ~/your-workspace/hydra-os/scripts && python3 test-sexual-health-engine.py
```

#### 3. Data integrity validation
- **Pipeline coverage**: Check for 7-day gaps in daily_scorecard and ef_compass_daily entries
- **Modifier staleness**: Verify nutrition_modifier and sexual_health_modifier match canonical formula
- **TWC recomputation**: Validate stored TWC matches computed value from 8D dimensions × stacked modifier
- **Phantom TWC**: Check for TWC values on carryforward rows without legitimate 8D data

#### 4. Patient 0 evidence audit
Review activation/action observations for:
- Algorithm development work counting as activation evidence
- Broad evidence lens beyond GitHub commits (cron creation, skill authoring, architecture work)
- Distinguishing deliberate rest from activation failure
- Proper classification of system work vs score reference

#### 5. Drift detection
When algorithm-integrity-baseline.json exists:
- Compare latest scores against baseline values
- Flag significant deviations requiring investigation

### Audit Protocol (the principal's standing rule: different AI model verifies calculations)
1. VERITAS-MATH re-derives every formula from first principles on Gemini, compares to engine output
2. VERITAS-PHYS checks all boundaries and physical plausibility on Gemini
3. VERITAS-STAT validates weighting, confidence intervals, trend calculations on Qwen
4. VERITAS-ETHICS reviews modifiers, thresholds, alerts for bias on DeepSeek
5. No formula goes to production without audit sign-off
6. Audit schedule: on any formula change, weekly spot-check during GENESIS, monthly full audit

### Activation Protocol
When ANY scoring calculation work begins, the relevant panel MUST be activated:
- 8D/TWC changes → HALO + CIRCADIA + LIBRA-8D + FLUX-8D + ETHOS-8D, then VERITAS audit
- Nutrition changes → HALO + LIBRA-NUT + FLUX-NUT + ETHOS-NUT, then VERITAS audit
- Sexual health changes → full SX panel (EROS/TANTRA/KINSEY/BONDING + triads), then VERITAS audit
- Kink changes → KINSEY + EROS + LIBRA-KNK + FLUX-KNK + ETHOS-KNK, then VERITAS audit
- EF COMPASS changes → AISHA-MD + COGNOS + LIBRA-EF + FLUX-EF + ETHOS-EF, then VERITAS audit
- Cross-system integration → FORGE + HALO + NEXUS + all affected engine teams, then full VERITAS audit

### Blueprint Document
Full ecosystem blueprint with vault structure, team architecture, security model:
`~/your-workspace/health-private/SCORING-ECOSYSTEM-BLUEPRINT.md` (and PDF version)

## Persona Variation Assignment (Built 2026-04-05)

Every agent activated for a task gets a persona variation assigned by ARBITER:
- V1: Analytical (formula derivation) | V2: Builder (code implementation) | V3: Skeptical (audit/review)
- V4: Systems thinker (integration) | V5: Cautious (clinical safety) | V6: Teacher (documentation)
- V7: Scholar (research) | V8: Pragmatist (hotfix) | V9: Designer (UX) | V10: Philosopher (ethics)

Logged in task_analytics. SENTINEL flags unassigned tasks. Part of GENESIS Phase 9 audit.

## Unified Health Database Architecture (Built 2026-04-05)

**ashley_unified_health.db** — FORGE-built, 8 tables:
- daily_scorecard (35 cols: 8D base+final, TWC, all modifiers, mood, energy)
- nutrition_daily (7 sub-scores + composite + raw inputs)
- sexual_health_daily (6 sub-scores + composite)
- kink_daily (5 sub-scores + per-dimension modifiers)
- ef_compass_daily (7 domains current+natural + overall)
- dimension_trends (7d/30d rolling averages)
- alerts (clinical/wellness alerts by severity)
- twc_history (full TWC decomposition)

**ashley_ef_tracker.db** — 6 tables: observations, domain_scores, health_factors, interventions, score_history, complementarity_map. CLI: ef_tracker.py (add/batch/score/status).

**Multi-user:** Partner databases use identical schemas with swapped complementarity columns. Architecture supports N users with zero schema changes. Vault folders are 05-Partners/[username]/, not hardcoded to the principal.

## Obsidian Visualization Layer — Option C Hybrid (Built 2026-04-05)

Vault: ~/Qubit-Health-Vault/ (LOCAL ONLY, .nosync, never iCloud)
Sync: obsidian-sync.py pulls DB→Obsidian daily notes (one-directional, DB is source of truth)
Plugins: Dataview, Charts, Tracker, Templater, Calendar, Kanban, Excalidraw (all local-only)
Security: FileVault + optional encrypted APFS sparse image + obsidian-encrypt plugin for sensitive notes
Cron: 7:45 AM daily syncs scores into 02-Daily/ notes with YAML frontmatter for Dataview queries

## Daily Scoring Pipeline (Standing Automation)

7:30 AM — AISHA-MD cron (e1b0a2a2845b): extract EF observations from standups, recalculate scores, sync to unified DB, deliver FULL scorecard to the principal with ALL sub-dimensions
7:45 AM — Obsidian sync cron (99978c4f68b3): pull DB data into vault daily notes
Saturday 7 PM — GENESIS full sprint

the principal NEVER asks for her scores. They arrive automatically every morning. If she has to ask, the system is broken.

## Unified Pipeline Architecture (Phase 1 built 2026-05-27)

### Problem: 6 Independent Scoring Systems
Before unification, six separate scripts each computed their own TWC with different formulas:
- `transcript-analyzer.py` — linear weights + nonlinear K=2.5
- `8d360-scoring-engine.py` — stock-and-flow, EWMA, cascade, PCM, CSI (2214 lines)
- `8d360-nutrition-engine.py` — 0-100 composite → TWC modifier
- `rescore_engine.py` — its own TWC computation
- `rescore_and_report.py` — weighted sum TWC
- `scoring_pipeline.py` (old) — basic dimension → TWC without autonomous layer

None called calculator.py. All had different weights, different coupling (or none), different TWC math.

### Solution: Input Adapter Layer + Confidence Merger
```
Check-in (conf 1.0) ─┐
Nutrition (conf 0.7) ─┤→ Merger (highest confidence wins per field) → calculator.py → TWC
Transcript (conf 0.4)┘   ↓                                          ↓
                ConfidentInputBundle                              Credibility Interval
                (per-field confidence)                            (±uncertainty on TWC)
```

### New Files (all in products/principal-8d-tracker/)
- `unified_pipeline.py` — SINGLE entry point for all scoring. Only file that calls calculator.py.
- `input_adapters/__init__.py` — ConfidentValue, ConfidentInputBundle, baselines (ASHLEY_BASELINES), merger, credibility intervals
- `input_adapters/transcript_adapter.py` — Standup text → calculator.py fields with 0.4-0.7 confidence, regex signal extraction
- `input_adapters/nutrition_adapter.py` — Nutrition 0-100 → PhysicalInput + cascades to INT/VOC/PSY
- `input_adapters/checkin_adapter.py` — Check-in answers → calculator.py fields with 1.0 confidence
- `scoring_pipeline.py` — OLD, replaced by unified_pipeline.py

### Confidence Tiers
- 1.0 = direct measurement (check-in answer, sensor data)
- 0.7 = strong inference (transcript keyword matching with context)
- 0.4 = weak inference (keyword presence, no context)
- 0.2 = baseline default (no evidence, using personal baseline)
- 0.0 = no data at all

### Merger Logic
Highest confidence wins per field, independently. When two sources provide the same field, the one with higher confidence replaces the other. On tie, incumbent wins. Result: every field has the best-available evidence with provenance tracking.

### Credibility Interval
```
uncertainty = 0.02 + 0.33 * (1 - coverage) * (1 - avg_confidence)
TWC range = [max(0, twc - uncertainty), min(0.85, twc + uncertainty)]
```
Not a statistical confidence interval (no repeated measurements). A credibility assessment: "given input quality, true TWC is likely within this range."

### Key Bug Found and Fixed (2026-05-27)
Old pipeline wrote flat TWC=0.50 for 8 days (May 18-25) WITHOUT any dimension scores. The AISHA-MD scoring cron was inserting placeholder TWC values without running compute_twc(). Fixed by: deleting orphan TWC records, backfilling correct TWC from dimension scores, creating atomic scoring guard (never writes TWC without dimensions).

### 5-Phase Unification Plan Status
- **Phase 1:** Input adapter layer ✅ (built 2026-05-27)
- **Phase 2:** Wire calculator.py as sole TWC source ❌ (legacy scripts still compute independently)
- **Phase 3:** Reconnect operational layer (stock-and-flow, EWMA, cascade, PCM, CSI) ❌
- **Phase 4:** ADHD EF Compass v3 with sigmoid curves ✅ (built earlier)
- **Phase 5:** Review cron (specialist agents audit unified system) ❌

### Usage
```bash
cd ~/your-workspace/hydra-os/products/principal-8d-tracker
python3 unified_pipeline.py --full           # full autonomous run
python3 unified_pipeline.py --transcript /path/to/transcript.md
python3 unified_pipeline.py --text "raw transcript text here"
python3 unified_pipeline.py --date 2026-05-27
```

## Behavioral Physics Engine (Diviq) — Nightly Self-Healing

The behavioral physics engine is a layered equation stack (8 layers: observation, latent state, history, geometry, distribution, dynamics, regime, policy) that replaces flat score tracking with a full trajectory engine. It is NOT a separate codebase yet — it exists as specification documents.

**Dedicated specialist:** PULSAR (`INTP-5w4-PHYS-01`). Only escalate when the math lane needs physics/dynamical systems expertise.

- See `references/behavioral-physics-engine-spec-corpus.md` for the full file inventory, cross-document coherence check checklist, implementation gap status, and known drift patterns.
- See `references/algorithm-ecosystem-registry.md` for the condensed algorithm ecosystem reference: 29+ algorithms across 9 mathematical domains, their locations, status (LIVE/DEV/SPEC), key equations, implementation gaps, file map, and external advisor context. Use this when building advisor reviews, scientific briefs, or technical handoff documents so you present the full ecosystem rather than just the prototype in front of you.

**Key pitfall:** HTML presentation files drift from their MD source specs. Always compare pill/tag counts and equation renderings in HTML against the canonical MD spec. The 2026-06-03 audit found the hero section had 7 pills instead of 8 (missing Distribution Geometry).

## Pitfalls
1. Built scoring calibrations solo — the principal corrected: needs expert panel with mathematicians, physicists, biologists, psychologists
2. Used "Dr." prefix on AI agents — the principal corrected: never, these aren't real doctors
3. Standup transcript had the principal's words bleeding into the principal's scores — fixed with proper speaker separation
4. Created duplicate NEXUS audit cron that overlapped SENTINEL — removed, consolidated into SENTINEL
5. Post-standup cron ran 3x (9/10/11 AM) — wasteful, changed to 1x at 10 AM
6. Filed talent requests but didn't actually spawn through FORGE+ARBITER — paperwork ≠ execution
7. Skeleton profiles instead of full 17-section master profiles — the principal caught it, needs proper process
8. Personal health data routed through AISHA instead of AISHA-MD — must always go to AISHA-MD
9. NEVER just call attention to broken things, missing data, or recalculation needs — fix them always
10. NEVER build databases yourself (AISHA). Delegate ALL DB architecture to FORGE (CTO). Three attempts failed before learning this.
11. NEVER use Anthropic models for database creation/population — the principal's standing rule. Use FORGE on capable model, or execute_code with Python sqlite3 directly.
12. Free models (Qwen free tier) cannot reliably build complex schemas — wrong constraints, missing columns. Always use FORGE on a capable model for DB work.
13. Split subagent tasks: combined "read all files + build DB + populate" tasks TIMEOUT. Pattern: (a) FORGE builds schema, (b) separate execute_code populates data.
14. Schema CHECK constraints must match REAL data shapes. Read actual JSON files before defining constraints — the source field had ('transcript','checkin','manual') but real data used 'scorecard_json'. Had to ALTER TABLE after first load.
15. Subagent terminal approval blocks cause timeouts even with auto-approve user setting. When this happens, do work via execute_code in main session.
16. the principal wants ALL scores visible daily WITHOUT ASKING. Every number, every sub-dimension, every day. The daily cron must deliver the COMPLETE scorecard.
17. **Never write TWC without dimension scores.** The old pipeline inserted flat TWC=0.50 placeholders for 8 days with zero dimension data. Always use unified_pipeline.py which writes dimensions + TWC atomically.
18. **Six legacy scripts still compute their own TWC independently** (transcript-analyzer.py, 8d360-scoring-engine.py, 8d360-nutrition-engine.py, rescore_engine.py, rescore_and_report.py, old scoring_pipeline.py). Phase 2 of the unification plan must rewire these to call unified_pipeline.py instead. Until then, scores may differ across systems.
19. **Critically low pipeline coverage** — If fewer than 50% of days in a rolling 30-day window have real scores (not cron/carryforward), the scoring pipeline is broken and must be fixed immediately. This prevents accurate trend analysis and rescore processing.
20. **Interaction matrix values deviating from proprietary specification** — If key coupling coefficients (PSY↔INT, PHY↔VOC, SOC↔SPI, ENV↔PHY) deviate by more than 0.30 from the proprietary specification (0.85, 0.78, 0.72, 0.68 respectively), it indicates a fundamental error in the coupling matrix implementation or data pipeline requiring urgent attention.
19. **Critically low pipeline coverage** — If fewer than 50% of days in a rolling 30-day window have real scores (not cron/carryforward), the scoring pipeline is broken and must be fixed immediately. This prevents accurate trend analysis and rescore processing.
20. **Interaction matrix values deviating from proprietary specification** — If key coupling coefficients (PSY↔INT, PHY↔VOC, SOC↔SPI, ENV↔PHY) deviate by more than 0.30 from the proprietary specification (0.85, 0.78, 0.72, 0.68 respectively), it indicates a fundamental error in the coupling matrix implementation or data pipeline requiring urgent attention.

- **Interaction matrix values severely deviant** — The interaction matrix values in the database are significantly below the proprietary specification (PSY↔INT: 0.2 vs 0.85, PHY↔VOC: 0.15 vs 0.78, SOC↔SPI: 0.2 vs 0.72, ENV↔PHY: 0.25 vs 0.68). This indicates a fundamental error in the coupling matrix implementation or data pipeline. Urgent action is required to reconcile the interaction matrix values with the proprietary specification.

- **Critically low pipeline coverage** — Only 4/30 days in the last 30 days have real scores (not cron/carryforward). This prevents accurate trend analysis and rescore processing. The scoring pipeline must be fixed immediately.

## Self-referential scoring loop prevention
When extracting EF observations, never include observations that reference scores, trends, or domain values as these create feedback loops. Only include actual behavioral evidence. Examples of self-referential evidence to avoid: "Activation at 0.7 — new tracking low", "COMPASS Activation at 1.0 for two weeks", "X score drifted from A to B".
\n\n**False-positive classification rule (learned 2026-06-01 VERITAS-ALGO audit):** When keyword patterns flag observations containing "scoring", "domain", "COMPASS", "subscores", "TWC" etc., check whether the observation describes BUILDING, DESIGNING, MAINTAINING, DEBUGGING, or WORKING ON the scoring system. These are legitimate behavioral evidence — the subject is the person's action on the system, not the system's output about the person. A useful heuristic: if you could replace the scoring keyword with "database" or "spreadsheet" and the sentence still describes productive work, it's legitimate. Only flag observations where the subject IS a score value, trend, or system-produced metric.\n\n**Critical application:** During integrity checks, always apply this rule to avoid misclassifying legitimate algorithm work, system building, or debugging efforts as self-referential evidence. This prevents incorrectly purging valid activation/action observations that reference the scoring system as part of legitimate work on the system.\n21. **Scoring methodology validation** — Always validate scoring algorithms against evidence and domain expertise. Simple sum models require justification; consider coupling terms and weighted contributions. Arbitrary parameters (like decay rates) should be evidence-based or configurable. Missing dimensional interactions can oversimplify complex systems. Inclusivity and bias review is essential for broad applicability. Gamification elements should meaningfully connect to actual dimension improvement, not just provide extrinsic motivation.\n\n### Evidence Source Diversity Audit\n\nWhen conducting Patient 0 evidence audits (as outlined in the VERITAS-ALGO integrity check procedure), be vigilant about over-reliance on GitHub commits as a proxy for activation/action evidence. In the June 7, 2026 integrity check, 16 observations were flagged by the pattern `evidence_text LIKE '%no github commits%'` — indicating a potential narrow evidence lens.\n\n**Always apply the false-positive classification rule**: Check whether observations mentioning GitHub (or lack thereof) describe BUILDING, DESIGNING, MAINTAINING, DEBUGGING, or WORKING ON the scoring system. Examples of legitimate work that might not show in GitHub commits:\n- Agent design and architecture sessions\n- Cron job creation and management\n- Skill authoring and patching\n- Conversation-based system building\n- Document creation and technical writing\n- System debugging and incident response\n- Cross-referencing and quality auditing\n- Algorithm development work (which counts as activation evidence for patient 0)\n\nOnly flag observations where the subject IS a score value, trend, or system-produced metric — not observations about where work does or doesn't appear in version control.
**False-positive classification rule (learned 2026-06-01 VERITAS-ALGO audit):** When keyword patterns flag observations containing "scoring", "domain", "COMPASS", "subscores", "TWC" etc., check whether the observation describes BUILDING, DESIGNING, MAINTAINING, DEBUGGING, or WORKING ON the scoring system. These are legitimate behavioral evidence — the subject is the person's action on the system, not the system's output about the person. A useful heuristic: if you could replace the scoring keyword with "database" or "spreadsheet" and the sentence still describes productive work, it's legitimate. Only flag observations where the subject IS a score value, trend, or system-produced metric.

**Critical application:** During integrity checks, always apply this rule to avoid misclassifying legitimate algorithm work, system building, or debugging efforts as self-referential evidence. This prevents incorrectly purging valid activation/action observations that reference the scoring system as part of legitimate work on the system.
21. **Scoring methodology validation** — Always validate scoring algorithms against evidence and domain expertise. Simple sum models require justification; consider coupling terms and weighted contributions. Arbitrary parameters (like decay rates) should be evidence-based or configurable. Missing dimensional interactions can oversimplify complex systems. Inclusivity and bias review is essential for broad applicability. Gamification elements should meaningfully connect to actual dimension improvement, not just provide extrinsic motivation.
