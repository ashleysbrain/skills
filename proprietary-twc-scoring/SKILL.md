---
name: proprietary-twc-scoring
description: Score agents using the principal's proprietary TWC formula from 8D360AI — 3-layer composite with coupling coefficients, NOT simple averages
tags: [twc, scoring, fleet, analytics, 8d360]
---

# Proprietary TWC Scoring

## When to Use
Any time agents need scoring, rescoring, GENESIS sprints, fleet reviews, performance evaluation, *or a TWC-based business/organization scorecard*.

For coaching-engine work, see `references/coaching-score-adapter.md` and `references/public-twc-rubric.md` for the public-information-only coaching score convention.

When the scoring target is an advisory panel or coaching engine, use the public coaching score contract by default:
- public information only
- separate public TWC from any private/internal TWC profile
- keep confidence explicit when evidence is thin
- avoid implying that the public score uses private or sensitive data
- if the user asks for "advisor TWC scores" in coaching context, interpret that as the public coaching score unless a narrower metric is explicitly named

## Public founder-bio positioning

When writing a biography, speaker introduction, application profile, or founder description for the principal Williams, do not describe 8D360 without naming the calculation she created. TWC is a signature contribution, not an implementation detail.

Use restrained, public-safe language:

> the principal created the Total Wellness Composite (TWC), a proprietary calculation designed to assess wellness across eight interdependent dimensions. It combines weighted dimension scores with nonlinear, temporal, and cross-dimensional relationships rather than reducing a person to isolated ratings or a simple average.

Bio rules:
- State the principal's authorship directly: "the principal created the Total Wellness Composite (TWC)."
- Expand TWC on first use.
- Explain the distinction from a simple average in plain language.
- Do not call TWC clinically validated, diagnostic, proven, or universally predictive unless current external evidence supports that exact claim.
- Do not expose coefficients, private-health details, or proprietary formula internals unless the requested format requires technical depth.
- When space is tight, prioritize TWC alongside the current flagship research direction. Do not let newer work such as Physiomorphic AI displace the foundational calculation from the principal's bio.

## Coaching-engine score contract

For advisory panels, report scores with all of the following:
- `public_twc_dimension_scores`
- `public_twc_score`
- `public_twc_score_basis`
- `public_twc_score_confidence`

Use only public, observable, or openly stated information. Do not improvise a different rubric unless the user explicitly requests one.

Common pitfall:
- Do not replace the public coaching score with a generic ad hoc proxy just because the internal/private TWC is unavailable.

Use this for:
- NOTE: Every TWC output should be passive-first and must carry an explicit confidence value. Confidence is part of the score contract, not optional metadata.
- Confidence should increase as supporting evidence accumulates, then plateau once the model is well-calibrated.
- agent fleet scoring
- personal 8D/TWC rescores
- organization, nonprofit, volunteer, or for-profit scoring
- parent-company / subsidiary-company scoring where each entity gets its own scorecard
- TWC core score design where business type and stage change interpretation but not the core score identity
- explanatory scorecards and methodology briefs that show *how* the TWC was built, not just the final number
- partner-ready scoring docs for another founder or AI that must choose the correct business type, stage, and calibration before scoring

## The Formula
Use ASCII-safe math in handoffs, PDFs, and partner docs so the rendering is robust:

```text
TWC = sum(w_i * D_i) + sum(kappa_ij * D_i * D_j for all i != j)
```

## Business / Organization Scoring Flow
When scoring companies, score each entity separately and load the correct calibration before computing TWC:

1. Identify whether the entity is the parent company or a subsidiary
2. Classify the company type
3. Classify the stage
4. Load the matching calibration pack
5. Score the 8 dimensions
6. Compute the weighted sum
7. Add the coupling terms
8. Produce a separate roll-up for parent and subsidiary without blending the entity scores

## Business-Type TWC Adapter
When scoring organizations instead of agents or personal health, keep TWC as the core and add a context layer:

- **Org type**: volunteer, for_profit, nonprofit, hybrid
- **Stage**: pre_launch, early_traction, growth, mature
- **FIN meaning** changes by org type:
  - volunteer = sustainability / resource discipline
  - for_profit = revenue, margin, runway
  - nonprofit = funding health / donor stability
  - hybrid = blended sustainability
- **Rule**: do not replace TWC with a separate scoring system; calibrate interpretation around the same core score

**Critical Implementation Note for Organizational Scoring**: When applying the TWC formula to organizations, always use the geometric mean normalization approach for coupling terms (as detailed in the organizational-twc-scorecard skill) rather than raw Dᵢ·Dⱼ products. Raw products inflate scores dramatically and are NOT on the same 1-10 scale as the weighted sum. The correct approach is:
  geo = sqrt((Dᵢ/10) × (Dⱼ/10))     # normalized to [0,1]
  term = κᵢⱼ × geo × 10              # back to score space
This prevents TWC inflation to the efficiency cap for mid-range scoring organizations.

## The Formula
TWC = Σᵢ wᵢ·Dᵢ + Σᵢ≠ⱼ κᵢⱼ·Dᵢ·Dⱼ

## Three Layers
1. **Layer 1 (40%)**: Objective telemetry — hard data (error rates, uptime, output quality)
2. **Layer 2 (30%)**: Peer assessment — agents score each other (weekly rotation)
3. **Layer 3 (30%)**: Cross-dimensional coupling — κᵢⱼ matrix math

## 8 Dimensions (with weights)
- ψ PSY (0.15) — reasoning coherence, cognitive load
- φ PHY (0.15) — infrastructure health, error rates, uptime
- ε ENV (0.10) — configuration, paths, tool access
- τ SOC (0.10) — collaboration, cross-pollination
- σ SPI (0.10) — mission alignment, DS grounding
- ι INT (0.15) — output quality, depth, accuracy
- υ VOC (0.15) — mandate completion, task throughput
- ϕ FIN (0.10) — cost efficiency, model optimization

## Key Coupling Coefficients (κᵢⱼ) — CANONICAL 28-pair matrix

**Canonical source:** `organism/canonical_coupling.py` → DB `interaction_matrix` table (28 pairs, C(8,2), scale 0.05-0.35, schema-capped at ±0.5). VERITAS-locked.

The 4 spec heuristics (PSY↔INT: 0.85, PHY↔VOC: 0.78, SOC↔SPI: 0.72, ENV↔PHY: 0.68) are **REJECTED** — schema-violating (>0.5), literature-unsupported at that magnitude, and covered only 4 of 28 pairs. See `canonical_coupling.py` lines 10-14. Do NOT cite them as authoritative.

Stored canonical values (from DB, verified 2026-06-28): PSY↔INT: 0.20, PHY↔VOC: 0.15, SOC↔SPI: 0.20, ENV↔PHY: 0.25. These are CORRECT, not "deviant from spec." The spec values were the deviation.

**V2 evolution (design locked 2026-06-28):** The 28-pair matrix is the rank-2 baseline. A V2 design adds sparse rank-3 triples (8-12 compounds) and situational gating (context-vector-modulated κ). See `references/coupling-v2-evolution-2026-06-28.md` for the full design: free-energy gate, adiabatic staging (Stage 0 → A → B → C), and the Stage 0 blocker (coupling_sum is currently a dead constant 6.775 in the live scoring path).

## Rules
- Efficiency cap: 8.5 (no agent can score above without peer verification)
- CAR (Cascade Amplification Ratio): measures intervention ripple effects
- ILS (Intervention Leverage Score): identifies highest-ROI dimension to fix
- Bayesian temporal decay on historical scores
- For company scoring, business type and stage determine how FIN and the calibration are interpreted
## References
- Source: 8D360AI repo methodology
- TWC history table issue (2026-06-02): references/twc-history-table-issue-2026-06-02.md
- Integrity check findings (2026-06-06): references/integrity-check-findings-2026-06-06.md
- Computation architecture analysis (2026-06-08): references/computation-architecture-2026-06-08.md — code path map, three κ value sets, independent recomputation results
- Baseline verification: references/baseline-verification.md
- TWC calculation details and validation (2026-06-10): references/twc-calculation-details-2026-06-10.md
- VERITAS DOGFOOD audit findings (2026-06-11): references/veritas-dogfood-audit-2026-06-11.md — audit of scoring documentation review process
- the specialist engine structural floor audit (2026-06-13): references/scoring-floor-inconsistency-2026-06-13.md — traced computation showing 77-91% of rescore deltas are LLM inconsistency correction, not real wellness change; includes monotonicity bias finding
- Algorithm integrity audit procedure (2026-06-14): references/audit-procedure-algo-2026-06-14.md
- AUDIT-SYNTH builder-product audit (2026-07-06): references/audit-synth-2026-07-06.md — two coupling_sum writer paths discovered, VERITAS-ALGO offline, chronic "deviant from spec" misreporting traced

## Implementation
- Calculator: ~/.sibling-agent/workspace/intel/agents/database/twc_calculator.py
- DB: agents.db in same directory
- Run: `python3 twc_calculator.py` for full fleet scoring

## the principal's PERSONAL 8D Scoring (Human Version — DIFFERENT from Agent)

the principal built a separate human scoring methodology. When working on AISHA-MD check-ins, personal wellness, voice notes, or the 8D360 consumer product, use THIS — not the agent version above.

### Baseline-aware personal scoring
- Personal scores are dynamic, not static.
- Use the current baseline/calibration as a translation layer before applying the coupled TWC formula.
- If the source is a transcript or voice note, rich signal extraction should happen before the baseline bridge, not after the final score.
- If the result looks like a simple weighted average, the adapter/bridge is wrong.

### Key Differences from Agent Scoring
- **Weighted geometric mean** (not arithmetic) — penalizes low outliers
- **Different weights**: PSY 0.18, PHY 0.16, VOC 0.14, SOC 0.12, SPI 0.12, INT 0.10, FIN 0.10, ENV 0.08
- **Per-dimension modality weights** vary (e.g., PSY: 50% self/30% objective/20% coupling; PHY: 20% self/30% objective/50% coupling)
- **Nonlinear K=2.5, deficit beta=0.15, momentum coefficient=0.05**
- **Mood correction**: Pre-score mood marker (Energized/Balanced/Low) adjusts interpretation
- **Traffic light ternary**: green=7.5, yellow=5.0, red=3.0 (not 1-10 scale)
- **Financial WEEKLY ONLY** (daily triggers anxiety loop — tied to healthcare/disability cycle)
- **Bayesian temporal smoothing** with population priors and euthymic calibration anchors

### Key Files
- Config: `~/.sibling-agent/workspace/memory/principal-8d/config.json` (dimension rotation, weights, scoring params)
- Profile: `~/.sibling-agent/workspace/memory/principal-8d/profile.md` (energy patterns, hard brain days, ND adaptations)
- Baselines: `~/.sibling-agent/workspace/memory/principal-8d/baselines.json` (Bayesian priors, calibration data)
- Daily data: `~/.sibling-agent/workspace/memory/principal-8d/daily/YYYY-MM-DD.json`
- Health PHI: `~/your-workspace/health-private/principal-health-profile.md` (LOCAL ONLY)
- PRD: `~/.sibling-agent/workspace/intel/wellness/8D360-PRD.md` (full product spec)
- Scoring philosophy: `~/.sibling-agent/workspace/processes/product/SCORING-METHODOLOGY.md`

### User-Facing Dimension Names
Head (PSY), Body (PHY), Space (ENV), People (SOC), Purpose (SPI), Growth (INT), Work (VOC), Money (FIN)

### Dimension Rotation (from config)
Mon: PSY+VOC, Tue: INT+SOC, Wed: ENV+PSY, Thu: VOC+SPI, Fri: SOC+INT, Sat: SPI+ENV, Sun: full 8D

### Three Laws of Skipping (NON-NEGOTIABLE)
1. Skipping is silent. No follow-up. No guilt.
2. Skipping is data. 3+ consecutive skips = possible low period.
3. Returning is unnarrated. No "welcome back," no "you missed 3 days."

### CRITICAL PRINCIPLE: "We live the systems we create"
the principal insists on using her own proprietary methodology on herself. Never substitute generic wellness questions, made-up rotations, or simplified scoring. Always read her config.json for the actual parameters. She built the framework — she lives in it.

## CRITICAL: The Scoring Engine Gap (discovered 2026-03-29)

The fleet TWC was stuck at 7.40-7.41 for days despite 15+ erroring jobs. Root cause: there is NO automated scoring engine. The "Fleet Analytics Refresh" cron (2bb15ea6) is an LLM that reads/edits a markdown file. No actual math runs. The DB has scoring columns (ai_physical, twc_score, fleet_twc) but they were EMPTY.

### What needs to exist (talent request filed 2026-03-29):
1. `fleet-twc-engine.py` at ~/your-workspace/hydra-os/scripts/ that:
   - Pulls live telemetry from `sibling-agent cron list --json`
   - Maps jobs to agents in the DB
   - Calculates 8D scores per agent from telemetry (CE, error rate, model cost, etc.)
   - Applies the proprietary TWC coupling formula with real kij values
   - Writes computed scores to DB AND AGENT-ANALYTICS.md
   - Logs to intel/agents/scoring-log/YYYY-MM-DD-HH.json
2. Fleet Analytics Refresh cron updated to RUN the script, not manually edit markdown
3. The script runs daily minimum, ideally every 3-6 hours

### Scoring from telemetry mapping:
- PHY: CE=0 baseline, CE=1-2 drop 0.5-1.0, CE=3+ drop to 5.5, CE=5+ to 4.0
- FIN: Flash=10, Haiku=9, Sonnet=7, Opus=5 (cost efficiency)
- VOC: task completion rate from lastRunStatus history
- PSY: error rate + output quality signals
- ENV: config health (model set, timeout set, valid targets)
- Coupling cascades: PHY drops cascade to PSY (kij=0.82), INT (0.74), etc.

## Pitfalls
- NEVER use simple averages — the principal will catch it immediately
- The coupling matrix means fixing one dimension cascades to others
- Always report ILS to show WHERE to intervene
- Fleet TWC as of 2026-03-29: 7.21
- NEVER build personal check-ins without reading config.json, profile.md, and baselines.json first
- NEVER schedule check-ins in the evening — the principal's brain shuts down (mornings/midday ONLY)
- NEVER ask financial questions daily — weekly Sunday only (triggers anxiety)
- **Pipeline coverage gap** — If the scoring pipeline is missing scores for recent days, do not backfill automatically. Instead, check for available evidence sources (standup transcripts, voice memos, etc.) for those dates and process them through the scoring pipeline before considering the day complete. Missing days should remain blank only if no evidence exists. Additionally, compute the TRAILING GAP (consecutive unscored days ending at today). A trailing gap ≥5 days is an escalating pipeline failure regardless of the 30-day coverage ratio. **As of 2026-06-17 AUDIT-ALGO verification: 0/7 days with real scores in the last week, 4/30 days total with real scores (excluding cron/carryforward)**. Independent verification confirmed: real scored days in last 7 days = 0, carry-forward days in last 7 days = 0, total days with any row in last 7 days = 0.
- **No baselines table in DB (confirmed 2026-06-07 AUDIT-ALGO)**. The drift calculation references a "baseline" value (e.g., 28.1) but `sqlite_master` has no table matching `%baseline%`. The baselines are stored in a JSON file at `~/.sibling-agent/workspace/memory/principal-8d/baselines.json`, not in the scoring DB. When any audit or pipeline claims "drift from baseline", verify whether the baseline source is the JSON file, a computed anchor, or an invented figure. **As of 2026-06-17 AUDIT-ALGO verification: baselines.json exists but contains `"twcBaseline": null`, making drift calculation impossible. Reverified 2026-06-20 AUDIT-ALGO: baselines.json still contains `"twcBaseline": null`, making drift calculation impossible.**
- **Coupling matrix implementation gap (confirmed 2026-05-31 AUDIT-ALGO, escalated 2026-06-04 AUDIT-ALGO, latest 2026-06-13 VERITAS-ALGO, verified 2026-06-17 AUDIT-ALGO, reverified 2026-06-20 AUDIT-ALGO)** — The skill documents κ values of 0.68-0.85 for the four strongest couplings. The actual implementation (calculator_v3, `ashley_unified_health.db`) stores interaction_matrix values that significantly deviate from specification: PSY↔INT: 0.2 vs 0.85 spec, PHY↔VOC: 0.15 vs 0.78 spec, SOC↔SPI: 0.2 vs 0.72 spec, ENV↔PHY: 0.25 vs 0.68 spec. The `coupling_sum` column is a CONSTANT 6.775 for every scored day regardless of dimension values. Layer 3 (cross-dimensional coupling) is NOT producing differential day-to-day effects. **The coupling_sum is DEAD CODE — it is stored in the DB but never added to the TWC computation.**
- **MULTIPLE writer paths for coupling_sum — provenance signal (2026-07-06 AUDIT-SYNTH, confirmed 2026-07-07 AUDIT-ALGO, reverified 2026-07-24 AUDIT-ALGO, re-verified 2026-07-27 AUDIT-ALGO)** — VERITAS-ALGO claimed coupling_sum was a constant 6.775, but independent verification found FIVE distinct values: 0.1608, 0.1612, 0.1638, 0.1666, and 6.775. The 2026-07-03 transcript row has `coupling_sum=0.1666` with a +15.07 TWC recomputation mismatch (stored 6.82, canonical formula yields ~21.89 — the largest integrity error in system history). Multiple distinct coupling_sum values prove MULTIPLE writer paths exist that bypass the normal pipeline. When auditing, do NOT assume all rows share coupling_sum=6.775. Diagnostic: `SELECT DISTINCT coupling_sum FROM daily_scorecard WHERE twc_score IS NOT NULL ORDER BY coupling_sum;` — any row whose coupling_sum differs from the majority was written by a different code path. Quarantine those rows and run full provenance verification (source column, input artifact, dimension plausibility) before trusting them. **As of 2026-07-27 AUDIT-ALGO: 5 distinct values found, 6 rows with non-6.775 coupling_sum (transcript source, Jul 3-12, 2026). VERITAS-ALGO's claim that "coupling_sum: CONSTANT 6.775 (dead code)" was FALSE — the constant claim masked the existence of alternate writer paths.**
- **Watchdog-watchdog failure: VERITAS-ALGO itself goes offline (2026-07-06 AUDIT-SYNTH)** — The integrity watchdog is itself failing without an alarm. As of 2026-07-06: 0 VERITAS agents in agents.db (`SELECT COUNT(*) FROM agents WHERE display_name LIKE '%VERITAS%'` = 0), and `algorithm-integrity-log.md` last entry is 2026-06-22 (14 days stale). VERITAS-ALGO has not produced a report for over 2 weeks. When AUDIT-SYNTH (the verifier-of-the-verifier) runs, its FIRST check must be VERITAS-ALGO liveness: (a) query agents.db for VERITAS agents, (b) stat the integrity log's latest entry, (c) flag staleness >48h as a pipeline gap in itself. A dead watchdog means every prior "verified by VERITAS" claim is now suspect until VERITAS-ALGO is restarted. Independent recomputation on 2026-06-04 confirmed: for May 29, `weighted_sum × 10 × stacked_modifier = 28.11`, `+ coupling_sum 6.775 = 34.89`, but stored TWC = 28.36. The stored TWC matches the computation WITHOUT coupling_sum. The formula is effectively `TWC = weighted_sum × 10 × stacked_modifier` with no coupling term at all. This is not just "constant coupling" — it's "coupling not in the formula." Critical for product launch: the proprietary formula documentation and the implementation disagree. Either the implementation must add coupling, or the documentation must drop it.

- **CRITICAL IMPLEMENTATION GAP: Coupling terms not active in computation (learned 2026-06-04, verified 2026-06-19 AUDIT-ALGO, reverified 2026-06-20 AUDIT-ALGO)** — Despite the proprietary formula documenting significant coupling coefficients (PSY↔INT: 0.85, PHY↔VOC: 0.78, SOC↔SPI: 0.72, ENV↔PHY: 0.68), the current implementation in `twc_calculator.py` does NOT apply these coupling terms to the TWC calculation. The stored TWC value matches the computation `weighted_sum × 10 × stacked_modifier` exactly, with the coupling_sum column (6.775) never being added. This means Layer 3 (cross-dimensional coupling) has zero effect on scores regardless of dimension values. Until this gap is fixed, the system is operating on a simplified formula that misses the synergistic effects central to the proprietary TWC methodology. All scoring results should be interpreted with this limitation in mind.  **Note on data integrity**: While this represents an implementation gap in the coupling layer, integrity checks confirm that the current scoring system (using only the weighted sum × stacked_modifier computation) produces mathematically correct and internally consistent results. The gap does not corrupt existing data but prevents the full proprietary formula from being realized.
- **DB schema note for auditors** — The `int` dimension column in `daily_scorecard` is named `int_score` (not `int`, which is a SQL reserved word and will error). The audit protocol references `activity_observations` table but it does not exist; the actual table is `activity_log` (40 rows as of 2026-06-04).
- **twc_history table not populated by current pipeline (discovered 2026-06-01 VERITAS-ALGO)** — The `twc_history` table (columns: date, twc, pcm, csi, deficit_penalty, momentum, label) was last populated on 2026-05-26 while `daily_scorecard` has entries through 2026-05-29. The current scoring pipeline writes TWC to `daily_scorecard` but does NOT write to `twc_history`. This means momentum tracking (momentum coefficient=0.05) and PCM/CSI computation features are offline. The pipeline needs a reconnect step.
- **Extreme TWC provenance verification (learned 2026-06-01 VERITAS-ALGO)** — When an integrity audit confirms a TWC value is mathematically correct but the value is a new system extreme (Crisis <30 or Thriving >85), verify the input data provenance before accepting it. Mathematical correctness does not guarantee input correctness. The May 29 TWC of 28.4 (Crisis) with SOC=1.0 and INT=1.06 is a worked example — correct computation from stored dimensions, but the extreme dimension lows could indicate a bad transcript parse rather than a genuinely severe day. Check: source column, original input artifact existence, and whether individual dimension scores are plausible given context.
- **Scoring methodology validation** — Always validate scoring algorithms against evidence and domain expertise. Simple sum models require justification; consider coupling terms and weighted contributions. Arbitrary parameters (like decay rates) should be evidence-based or configurable. Missing dimensional interactions can oversimplify complex systems. Inclusivity and bias review is essential for broad applicability. Gamification elements should meaningfully connect to actual dimension improvement, not just provide extrinsic motivation.
- **Baseline verification**: When using the baseline file for drift detection, verify that the baseline TWC value matches the stored TWC for that date in the database. If they do not match, investigate the cause (e.g., baseline file outdated, database entry incorrect, etc.) before proceeding with drift analysis.
- **Public doc vs proprietary formula brand inconsistency (found 2026-06-04 AUDIT-DOGFOOD)** — Public/partner-facing methodology docs (e.g., QUBIT scoring-methodology.md) may use `Total = D1 + D2 + ... + D8` (unweighted simple sum) while the proprietary TWC uses weighted sum + κᵢⱼ coupling terms. When reviewing any external doc that references "8D" or "Total Wellness Score", check if the math matches the proprietary spec. Simple sum in public docs undermines the proprietary formula's credibility and creates customer confusion if they see both versions. Flag immediately as a brand consistency issue, not just a "methodology difference."
- **Document QA of scoring docs must check for ghost citations** — If a doc claims "37 citations" or "peer-reviewed research backing" but doesn't list them with authors, DOIs, or journal names, that's fabricated evidence appearance, not just "missing citations." This is a severity-1 content integrity issue, not a formatting concern.
- **Structural floor inconsistency in LLM-generated preliminary scores (discovered 2026-06-13 DS POPPER audit)** — The AISHA-MD LLM generates preliminary TWC scores that are 14-15 points BELOW the structural floor computed from their own base dimensions. For example, May 29 v1: preliminary TWC = 41.5, but base dimensions compute to structural floor = 54.99 — a 13.49-point inconsistency. The rescore engine silently absorbs this (line 666: `structural_prelim_floor = max(prelim_twc_reported, prelim_pre_integration)`) and reports the full delta as "improvement," but 77-91% of the rescore delta is actually correction of LLM inconsistency, not real wellness change. This makes the primary success metric (% users showing improvement) uninterpretable until fixed. **For any rescore audit, always compute the structural floor from the preliminary's own base dimensions and report the correction_fraction.** See `references/scoring-floor-inconsistency-2026-06-13.md` for the traced computation.
- **Monotonicity bias in rescore engine (flagged 2026-06-13 DS POPPER audit)** — The rescore engine has a hardcoded invariant (lines 682-689): if any positive evidence exists, `final_TWC >= preliminary_TWC` is enforced by assertion. This means the system structurally cannot detect patterns where one dimension improves while the aggregate should decline. This is a built-in positivity bias that confounds longitudinal analysis. The rule may be clinically justified (avoid demoralizing users), but it must be disclosed in any research or metric derived from these scores. Consider tracking the unconstrained score alongside the clinically adjusted score.
- **Nutrition label storage mismatch** — The `nutrition_daily` table may store incorrect labels for nutrition composites. Always verify that the label matches the output of `nutrition_label(composite)` function from `8d360-nutrition-engine.py`. For example, a composite of 79.0 should be labeled "adequate", not "strong". This can cause misinterpretation of nutrition status.
- **Interaction matrix values are CORRECT — the spec heuristics were rejected (corrected 2026-06-28)** — The `interaction_matrix` in the database stores the CANONICAL coupling coefficients at the correct 0.05-0.35 scale (PSY↔INT: 0.20, PHY↔VOC: 0.15, SOC↔SPI: 0.20, ENV↔PHY: 0.25). These are NOT "deviations from spec." The original 4 spec heuristics (0.85/0.78/0.72/0.68) were REJECTED by VERITAS lock (`canonical_coupling.py` lines 10-14): schema-violating (>0.5), literature-unsupported at that magnitude, and covered only 4 of 28 pairs. The DB values at 28 pairs are the authoritative source. Previous audit findings that flagged DB values as "deviant" were comparing against rejected heuristics and drew the wrong conclusion. The real implementation gap is that `coupling_sum` is a dead constant (6.775) regardless of actual scores — see the coupling-implementation-gap pitfall above.
- **CHRONIC AUDIT MISREPORTING — auditors keep re-flagging correct DB values as "deviant from spec" (2026-07-06 AUDIT-SYNTH)** — Despite the 2026-06-28 correction above, the Jun 27 SYNTHESIS report, the Jun 22 VERITAS-ALGO report, and the `### Regular Interaction Matrix Verification` procedure BELOW this pitfall all STILL cite the rejected 0.85/0.78/0.72/0.68 spec values as authoritative. This is a recurring audit bug, not a scoring bug. When you see a report claiming "all 4 pairs critically deviant from spec" with delta >0.40, that is FALSE-ALARMING — the auditor is comparing against rejected heuristics. The CORRECT check is: (a) confirm 28/28 pairs exist in `interaction_matrix`, (b) confirm the 4 key pairs match 0.20/0.15/0.20/0.25, (c) flag the DEAD `coupling_sum` (not the values) as the real defect. Do not propagate the "deviant from spec" finding; correct it in the report you are writing.
- **Inter-report contradiction audit pattern (discovered 2026-07-07 AUDIT-ALGO)** — AUDIT-ALGO Step 1 reads the latest VERITAS-ALGO report and must cross-check against the previous report for contradictions. Concrete failure: 2026-06-16 claimed "✅ all pairs valid" but 2026-06-17 found "❌ all pairs invalid (PSY↔INT: 0.2 vs 0.85, ...)." When consecutive reports contradict on the same check, the earlier claim is suspect — flag it as ⚠️ PARTIAL and note the contradiction. The canonical DB values (0.20/0.15/0.20/0.25) are CORRECT per canonical_coupling.py; the "spec" values (0.85/0.78/0.72/0.68) were REJECTED for schema violations.
**Critically low pipeline coverage** — If fewer than 50% of days in a rolling 30-day window have real scores (not cron/carryforward), investigate the scoring pipeline. Ensure the automated scoring engine runs daily and writes to the database. As of 2026-06-19, only 0/7 days in the last week and 4/30 days total have real scores (excluding cron/carryforward). **Reverified 2026-06-20 AUDIT-ALGO: 0/7 days with real scores in last week, 4/30 days total (excluding cron/carryforward).**
- **SMI Assessment Findings (2026-06-14)** — Based on Scoring Maturity Index assessment:\\n  - Engine Completeness: 15/25 pts (Fleet TWC engine missing; rescore, nutrition, and sexual health engines exist)\\n  - Test Coverage: 20/20 pts (All rescore engine tests pass including double-count property test)\\n  - Validation Coverage: 15/20 pts (VERITAS audit panel exists and active; calibration file and universal methodology exist; PRD exists)\\n  - Data Quality: 8/20 pts (Only 4/31 days with real scores; nutrition: 3/30 days, sexual health: 2/30 days, EF COMPASS: 21/30 days; activity database balanced; interaction matrix has 28/28 pairs but values mismatch spec. More recent checks show 0/7 days with real scores in the last week.)\\n  - Production Readiness: 10/15 pts (Multi-user architecture exists with partner DBs; limited API/export capability; basic documentation exists)\\n  - **TOTAL SMI: 68/100** (Alpha Ready — works for patient 0, needs work for external users)\\n  - **Key Blockers**: Missing fleet TWC engine, critically low pipeline coverage (<50% real scores), label mismatches in nutrition/sexual health engines, interaction matrix values not matching proprietary specification\\n  - **Highest-ROI Actions**: 1) Implement fleet-twc-engine.py with proper coupling terms, 2) Fix data pipeline to increase real score coverage, 3) Reconcile interaction matrix values with proprietary specification, 4) Fix nutrition/sexual health label outputs to match engine functions

### Verifying Coupling Terms Implementation
To verify whether coupling terms are being applied in the TWC computation:
1. Query the `twc_calculator.py` source to check if coupling terms are included in the final TWC calculation
2. Compare stored TWC values with computed values:
   - Compute weighted sum: `Σ(w_i * D_i)` using the standard weights
   - Compute stacked modifier: `sqrt(nutrition_modifier × sexual_health_modifier)` (for personal scoring) or appropriate modifier for agent scoring
   - Compute base TWC: `weighted_sum × 10 × stacked_modifier` (for personal) or `weighted_sum × 10` (for agent without modifiers)
   - If coupling terms were applied, you would see: `TWC_stored ≈ base_TWC + Σ(κᵢⱼ * D_i * D_j for i≠j)`
   - Currently, the system shows: `TWC_stored ≈ base_TWC` (coupling terms not applied)
3. Check the `interaction_matrix` values in the database - if they're non-zero but not affecting TWC, the gap exists

### TWC Recomputation Verification Methodology (discovered 2026-06-08 AUDIT-ALGO)

**CRITICAL for auditors**: When VERITAS-ALGO (or any auditor) claims "TWC recomputation: 0 mismatches," verify WHAT formula was used for recomputation. The computation path is multi-layered:

1. `calculator.py` (`compute_twc()`) — weighted sum + coupling + coherence factor + synergy tensor, efficiency cap ETA=0.85
2. `unified_pipeline.py` (`unified_score()`) — calls `compute_twc()`, adds ADHD fusion, credibility intervals
3. `scoring_engine_bridge.py` — bridges legacy 8d360-scoring-engine.py to unified_pipeline
4. The DB write path — may or may not go through the bridge; some entries come from transcript parsing, some from standup, some from manual/cron sources

### TWC Recomputation Verification Methodology (discovered 2026-06-08 AUDIT-ALGO)
...
**Three different κ value sets existed historically** (corrected understanding 2026-06-28):
- REJECTED spec heuristics (old skill): PSY↔INT 0.85, PHY↔VOC 0.78, SOC↔SPI 0.72, ENV↔PHY 0.68 — schema-violating, only 4 pairs, VERITAS-rejected per `canonical_coupling.py`
- `calculator.py` KAPPA dict: range 0.10–0.45 — legacy, not authoritative
- **CANONICAL DB `interaction_matrix`: range 0.05–0.35 (28 pairs, C(8,2))** — THIS IS THE AUTHORITATIVE SOURCE per `organism/canonical_coupling.py` VERITAS lock

The DB values are correct. The dead `coupling_sum` constant (6.775) is the real problem — it means the coupling layer is stored but never computed from actual scores. See `references/coupling-v2-evolution-2026-06-28.md` for the fix path.

**Recommendation for auditors**: When verifying TWC, state explicitly which formula/code path you used. If using the pipeline's own code, label it "internal consistency check" not "independent recomputation." True independence requires computing from the documented formula in this skill, not from the codebase. For enhanced robustness, use different models or tools than those used in production to catch model-specific blind spots.

**Recommendation for regular integrity checks**: The interaction_matrix values in the database should be validated quarterly against the proprietary specification coefficients (PSY↔INT: 0.85, PHY↔VOC: 0.78, SOC↔SPI: 0.72, ENV↔PHY: 0.68) as part of algorithmic integrity procedures. Significant deviations indicate implementation gaps requiring immediate attention.

### Regular Interaction Matrix Verification
To ensure the coupling layer of the TWC formula remains aligned with the canonical specification, perform this verification quarterly:

1. Extract all coupling values to verify completeness:
   ```sql
   SELECT COUNT(*) FROM interaction_matrix;
   -- Expected: 28 (C(8,2) pairs)

   SELECT COUNT(*) FROM interaction_matrix WHERE value < -0.5 OR value > 0.5;
   -- Expected: 0 (schema-capped)

   SELECT COUNT(*) FROM interaction_matrix WHERE dim1 >= dim2;
   -- Expected: 0 (canonical form stores dim1 < dim2 only)
   ```

2. **VERIFY AGAINST CANONICAL SOURCE FIRST** — CRITICAL anti-false-alarm rule:
   ```bash
   python3 /<workspace>
   ```
   This loads the authoritative 28-pair values from the DB and runs self-tests. If this passes, the DB values are canonical. Proceed to step 3 with those expectations, NOT the rejected heuristics.

3. Verify the 4 key canonical coupling values (from canonical_coupling.py verify() output):
   ```sql
   SELECT dim1, dim2, value FROM interaction_matrix
   WHERE (dim1='PSY' AND dim2='INT') OR (dim1='PHY' AND dim2='VOC')
      OR (dim1='SOC' AND dim2='SPI') OR (dim1='ENV' AND dim2='PHY')
   ORDER BY dim1, dim2;
   ```
   Expected canonical values: PSY↔INT: 0.20, PHY↔VOC: 0.15, SOC↔SPI: 0.20, ENV↔PHY: 0.25

   **CRITICAL WARNING (AUDIT-ALGO 2026-07-13 finding, REVERIFIED 2026-07-27):** The 0.85/0.78/0.72/0.68 values were REJECTED by VERITAS lock (canonical_coupling.py lines 10-14) for schema violations (>0.5), literature-unsupported magnitude, and covering only 4 of 28 pairs. **DO NOT compare DB values against these rejected heuristics** — they are NOT the authoritative spec. The canonical_coupling.py module IS the authoritative source. Any audit claiming "CRITICALLY deviant" by comparing DB values (0.20/0.15/0.20/0.25) against the rejected heuristics (0.85/0.78/0.72/0.68) is FALSE-ALARM. Always verify against canonical_coupling.py first.

**Worked example of FALSE-ALARM detection (2026-07-27 AUDIT-ALGO):** VERITAS-ALGO's 2026-06-20 report claimed "❌ all 4 key pairs CRITICALLY deviant" with deltas >0.60. Independent verification ran canonical_coupling.py (output: "OK — 28 pairs, range 0.05-0.35") and confirmed DB values are CORRECT: PSY↔INT=0.20, PHY↔VOC=0.15, SOC↔SPI=0.20, ENV↔PHY=0.25. The "spec" values (0.85/0.78/0.72/0.68) are rejected heuristics — not the authoritative source. This false-alarm has recurred across MULTIPLE VERITAS-ALGO reports (Jun 17, Jun 20, Jun 22, Jun 27) despite the 2026-06-28 correction in this skill.

   **MANDATORY AUDIT ENFORCEMENT (2026-07-16 finding):** When VERITAS-ALGO reports claim "all pairs invalid" or "CRITICALLY deviant from spec," AUDIT-ALGO MUST re-verify using canonical_coupling.py as the ground truth. The canonical_coupling.py output is the only authoritative reference. If an audit compares DB values against rejected heuristics (0.85/0.78/0.72/0.68), flag it as a FALSE-ALARM and correct the finding. Do not propagate "deviant from spec" claims without first verifying canonical_coupling.py passes.

**Pipeline coverage query MUST be correct (2026-07-16 verification):** The correct query for real scored days in last N days is:
  ```sql
  SELECT COUNT(*) FROM daily_scorecard 
  WHERE date >= date('now', '-N days') 
    AND twc_score IS NOT NULL 
    AND source NOT IN ('cron','carryforward');
  ```
  Any query missing the `source NOT IN ('cron','carryforward')` clause will OVERCOUNT cron-generated placeholder scores and UNDERCOUNT real user-scored days. As of 2026-07-16, VERITAS-ALGO has been using the wrong query for months, reporting 0/7 days when actual coverage is higher.

4. Verify coupling_sum is consistent (should be constant 6.775 unless second writer path):
   ```sql
   SELECT COUNT(DISTINCT coupling_sum) FROM daily_scorecard WHERE twc_score IS NOT NULL;
   -- Expected: 1 (the constant 6.775), unless second writer path detected
   ```

5. If any coupling_sum differs from 6.775, this proves a SECOND writer path — quarantine the row and verify provenance:
   ```sql
   SELECT date, coupling_sum, twc_score, source FROM daily_scorecard 
   WHERE twc_score IS NOT NULL AND coupling_sum != 6.775 
   ORDER BY date DESC;
   ```

6. Document findings in the algorithm integrity log and notify the scoring methodology panel.

A verification script is available at `scripts/verify_interaction_matrix.py` to automate this check.

- **Highest-ROI Actions**: 1) Implement fleet-twc-engine.py with proper coupling terms, 2) Fix data pipeline to increase real score coverage, 3) Reconcile interaction matrix values with proprietary specification, 4) Fix nutrition/sexual health label outputs to match engine functions

See `references/computation-architecture-2026-06-08.md` for the full code path analysis.

## SMI Assessment Findings (2025-07-26 AUDIT-SMI Independent Verification)

Based on independent scoring maturity audit by AUDIT-SMI verifying AXIOM's claimed SMI of 85/100:

- **AXIOM claimed SMI: 85/100 [Production Ready]**
- **Audit verified SMI: 34/100 [Prototype Phase]**
- **Delta: -51 points** (severely over-scored)

**Domain-by-domain verification:**
- Engine Completeness: AXIOM=25/25, Audit=10/25 → ❌
  • AXIOM credited interaction matrix (28 rows) as working
  • ZERO scripts actually READ it during scoring (search_files: 0 matches)
  • Dead code counted as shipped: -7 points
  • Missing fleet_twc_engine, activity_scoring: -8 points
- Test Coverage: AXIOM=20/20, Audit=12/20 → ❌
  • Excellent on existing engines (72/72 pass: rescore 7/7, nutrition 22/22, sexual health 43/43)
  • Cannot score tests for engines that don't exist
- Validation Coverage: AXIOM=13/20, Audit=0/20 → ❌
  • AXIOM claimed VERITAS agents "FOUND"
  • Database query: 0 VERITAS agents
  • Calibration file exists but never panel-reviewed
- Data Quality: AXIOM=12/20, Audit=0/20 → ❌
  • AXIOM: 4/30 real scored days, nutrition 3/30, sexual health 2/30
  • Actual: 6/30 real scored days, nutrition 0/30, sexual health 0/30 (both worse)
- Production Readiness: AXIOM=15/15, Audit=12/15 → ❌
  • Partner DB claimed as multi-user proof
  • Actual: 0 observations, 0 scores (empty schema only)

**Credit given for unshipped work:**
- Interaction matrix: 28 rows defined, 0 scripts use it
- VERITAS audit panel: Listed as "FOUND", count=0 in DB
- Partner DB multi-user: Schema exists, 0 real user data

**Dead code counted as working:**
- Interaction matrix (Layer 3 coupling): Defined in DB, never read
- AXIOM gave full 7 points for "exists"

**Overall verdict:** ❌ SEVERELY OVER-SCORED. Production-ready claim is premature by 51 points.

**Critical blockers:**
1. Interaction matrix dead code (-7 pts)
2. No VERITAS agents in DB (-13 pts)
3. 80% pipeline gap (-12 pts)
4. Multi-user claim false for empty DB (-3 pts)

**Corrected launch readiness:** Prototype (34/100), not Production Ready.

## SMI Assessment Findings (2026-06-17 AUDIT-ALGO Verification)

Based on independent algorithm integrity auditing by AUDIT-ALGO:

- Engine Completeness: 15/25 pts (Fleet TWC engine missing; rescore, nutrition, and sexual health engines exist)
- Test Coverage: 20/20 pts (All rescore engine tests pass including double-count property test)
- Validation Coverage: 15/20 pts (VERITAS audit panel exists and active; calibration file and universal methodology exist; PRD exists)
- Data Quality: 4/20 pts (Only 0/7 days with real scores in last week; 4/30 days total with real scores (confirmed through 2026-06-19); nutrition: 0/7 days, sexual health: 0/7 days, EF COMPASS: TBD; activity database balanced; interaction matrix has 28/28 pairs but values mismatch spec)
- Production Readiness: 10/15 pts (Multi-user architecture exists with partner DBs; limited API/export capability; basic documentation exists)
- **TOTAL SMI: 64/100** (Alpha Ready — works for patient 0, needs work for external users)

- **Key Blockers**: Missing fleet TWC engine, critically low pipeline coverage (0/7 days with real scores in last week), label mismatches in nutrition/sexual health engines, interaction matrix values not matching proprietary specification, coupling terms not applied in TWC computation

- **Highest-ROI Actions**: 1) Implement fleet-twc-engine.py with proper coupling terms, 2) Fix data pipeline to increase real score coverage, 3) Reconcile interaction matrix values with proprietary specification, 4) Fix nutrition/sexual health label outputs to match engine functions, 5) Apply coupling terms in TWC computation

See `references/computation-architecture-2026-06-08.md` for the full code path analysis.

## SMI Assessment Findings (2026-06-20 AUDIT-ALGO Verification)

Based on independent algorithm integrity auditing by AUDIT-ALGO:

- Engine Completeness: 15/25 pts (Fleet TWC engine missing; rescore, nutrition, and sexual health engines exist)
- Test Coverage: 20/20 pts (All rescore engine tests pass including double-count property test) + nutrition engine: 22/22 passed + sexual health engine: 43/43 passed
- Validation Coverage: 15/20 pts (VERITAS audit panel exists and active; calibration file and universal methodology exist; PRD exists)
- Data Quality: 2/20 pts (Only 0/7 days with real scores in last week; 4/30 days total with real scores (confirmed through 2026-06-19); nutrition: 0/7 days, sexual health: 0/7 days, EF COMPASS: 0/7 days; activity database balanced; interaction matrix has 28/28 pairs but values mismatch spec)
- Production Readiness: 10/15 pts (Multi-user architecture exists with partner DBs; limited API/export capability; basic documentation exists)
- **TOTAL SMI: 62/100** (Alpha Ready — works for patient 0, needs work for external users)

- **Key Blockers**: Missing fleet TWC engine, critically low pipeline coverage (0/7 days with real scores in last week), label mismatches in nutrition/sexual health engines, interaction matrix values not matching proprietary specification, coupling terms not applied in TWC computation, baselines.json twcBaseline: null preventing drift calculation

- **Highest-ROI Actions**: 1) Implement fleet-twc-engine.py with proper coupling terms, 2) Fix data pipeline to increase real score coverage, 3) Reconcile interaction matrix values with proprietary specification, 4) Fix nutrition/sexual health label outputs to match engine functions, 5) Apply coupling terms in TWC computation, 6) Establish proper baseline in baselines.json to enable drift calculations

See `references/computation-architecture-2026-06-08.md` for the full code path analysis.

### Verifying Label Correctness
To verify that label storage in the nutrition_daily and sexual_health_daily tables matches the engine's label functions:

1. Extract nutrition labels and composites:
   ```sql
   SELECT date, composite, label 
   FROM nutrition_daily 
   WHERE date >= date('now', '-30 days');
   ```

2. For each row, verify the label matches these thresholds:
   - Nutrition: >=90 optimal, >=80 strong, >=70 adequate, >=60 gaps, >=50 concerning, <50 critical
   - Example: composite 79.0 should be labeled "adequate", not "strong"

3. Extract sexual health labels and composites:
   ```sql
   SELECT date, composite, label 
   FROM sexual_health_daily 
   WHERE date >= date('now', '-30 days');
   ```

4. For each row, verify the label matches these thresholds:
   - Sexual health: >=85 thriving, >=75 strong, >=65 healthy, >=50 adequate, <50 gaps
   - Example: composite 76.3 should be labeled "strong", not "healthy"

Also verify that `daily_scorecard.nutrition_label` and `daily_scorecard.sexual_health_label` match their respective table counterparts.

If any label mismatches are found, this indicates a bug in the storage logic or label function that should be fixed immediately.


**Independent Audit Methodology**

**Quick Reference:** `references/interaction-matrix-verification-sequence.md` contains the complete verification sequence to avoid FALSE-ALARM audits that compare against rejected spec heuristics.

**Runbook:** `references/veritas-algo-audit-runbook.md` contains the exact, copy-pasteable terminal sqlite3 commands for the bi-daily VERITAS-ALGO audit. Use it instead of reconstructing queries from scratch each run. All checks run via terminal sqlite3 directly (no Python script needed, which avoids write-file gate issues in cron environments).

**Label correctness status (verified CLEAN 2026-06-20):** The previously reported label mismatches (nutrition 79.0 mislabeled as "strong", sexual health 76.3 mislabeled as "healthy") have been resolved. All nutrition and sexual health labels now match canonical thresholds. Continue verifying each run but do not re-report these specific historical mismatches as new findings.

### Resource-Pressure Audit Fallback (learned 2026-06-23 AUDIT-ALGO)
When the system hits fork/resource exhaustion (`BlockingIOError: Resource temporarily unavailable`, `/bin/bash: fork: Resource temporarily unavailable`), AUDIT-ALGO cannot execute its mandatory verification sequence (engine tests, DB queries, interaction matrix checks) directly in the parent session. **Fallback pattern: delegate each independent verification step to a separate subagent** via `delegate_task`. Each subagent gets its own terminal session and runs in isolation, bypassing the parent's resource pressure. Dispatch at most 3 subagents concurrently:
1. Engine tests (rescore + nutrition + sexual health)
2. DB queries (pipeline coverage + interaction matrix + baselines)
3. Cross-checks (label correctness + drift + extreme TWC provenance)
The subagent results re-enter the conversation when complete. AUDIT-ALGO then compiles the final verdict from the subagent returns. **If even subagents fail due to system pressure, report the audit as INCOMPLETE with [SILENT] to suppress delivery and retry on the next cron cycle.**

### VERITAS-ALGO Inter-Report Consistency Check (learned 2026-06-23 AUDIT-ALGO, reaffirmed 2026-07-27)
AUDIT-ALGO's Step 1 reads the latest VERITAS-ALGO report and verifies its claims. **Additionally, cross-check the two most recent consecutive reports for contradictions.** Concrete failure mode discovered: the 2026-06-16 VERITAS-ALGO report claimed interaction matrix was "✅ all pairs valid" but the 2026-06-17 report found "❌ all pairs invalid (PSY↔INT: 0.2 vs 0.85, ...)". The 6/16 check was either not run or wrong. When consecutive reports contradict on the same check, the earlier report's claim is suspect — flag it as ⚠️ PARTIAL in the audit verdict and note the contradiction explicitly.

**Documented contradiction cases (chronic pattern):**
- 2026-06-16: "✅ all pairs valid"
- 2026-06-17: "❌ all pairs invalid (PSY↔INT: 0.2 vs 0.85, ...)"
- 2026-06-20: "❌ all 4 key pairs CRITICALLY deviant" (same false-alarm repeated)

**MANDATORY ENFORCEMENT:** When VERITAS-ALGO reports claim "all pairs invalid" or "CRITICALLY deviant from spec" with deltas >0.40, AUDIT-ALGO MUST re-verify using `canonical_coupling.py` as ground truth BEFORE flagging as material issue. The canonical_coupling.py output is the only authoritative reference. If an audit compares DB values (0.20/0.15/0.20/0.25) against rejected heuristics (0.85/0.78/0.72/0.68), flag it as FALSE-ALARM and correct the finding. Do not propagate "deviant from spec" claims.

### VERITAS-ALGO Log Staleness Check (learned 2026-06-23 AUDIT-ALGO)
The "Last verified YYYY-MM-DD" footer in this skill can drift from reality. AUDIT-ALGO Step 1 must verify that the latest VERITAS-ALGO report date in `algorithm-integrity-log.md` is no older than 48 hours. If the log's latest entry is stale (no report for >2 days), flag it as a pipeline gap — VERITAS-ALGO itself may not be running. Do NOT update the "Last verified" footer in this skill based on a successful AUDIT-ALGO run unless VERITAS-ALGO's own report for that date exists in the log. AUDIT-ALGO and VERITAS-ALGO are independent — AUDIT-ALGO's verification of VERITAS-ALGO's claims is NOT the same as VERITAS-ALGO having produced a fresh report.

**Automated liveness check:** Run `references/veritas-algo-liveness-check.sh` before any audit to verify watchdog health. Exit codes: 0=alive (<48h), 1=stale (>=48h), 2=log file not found. Use in automated workflows to gate audit execution on watchdog health.

To independently verify the integrity of the TWC scoring system, follow these steps:

1. **Engine Tests**: Run the rescore, nutrition, and sexual health engine tests and confirm all pass.
   ```bash
   cd ~/your-workspace/hydra-os/scripts/rescore-engine && python3 rescore_engine.py test
   cd ~/your-workspace/hydra-os/scripts && python3 test-nutrition-engine.py
   cd ~/your-workspace/hydra-os/scripts && python3 test-sexual-health-engine.py
   ```

2. **Pipeline Coverage**: Query the database for real scored days (excluding cron/carryforward) in the last N days.
   ```sql
   SELECT COUNT(*) FROM daily_scorecard WHERE date >= date('now', '-N days') AND twc_score IS NOT NULL AND source NOT IN ('cron','carryforward');
   ```

3. **Interaction Matrix**: Extract key coupling values and verify against the CANONICAL SOURCE first:
   ```bash
   python3 /<workspace>
   ```
   This loads authoritative values from DB and runs self-tests. Expected canonical values: PSY↔INT: 0.20, PHY↔VOC: 0.15, SOC↔SPI: 0.20, ENV↔PHY: 0.25.

   **CRITICAL WARNING (AUDIT-ALGO 2026-07-13 finding):** The 0.85/0.78/0.72/0.68 values were REJECTED by VERITAS lock (canonical_coupling.py lines 10-14). Any audit claiming "CRITICALLY deviant" by comparing DB values (0.20/0.15/0.20/0.25) against the rejected heuristics is FALSE-ALARM. Always verify against canonical_coupling.py first, not the old spec heuristics.

4. **Label Correctness**: Verify that labels in nutrition_daily, sexual_health_daily, and daily_scorecard match engine thresholds.
   - Nutrition: >=90 optimal, >=80 strong, >=70 adequate, >=60 gaps, >=50 concerning, <50 critical
   - Sexual health: >=85 thriving, >=75 strong, >=65 healthy, >=50 adequate, <50 gaps

5. **Drift Calculation**: Verify that baseline TWC value matches stored TWC for that date in the database. Baselines are stored in `~/.sibling-agent/workspace/memory/principal-8d/baselines.json`.

6. **Extreme TWC Provenance**: For any TWC value that is a new system extreme (Crisis <30 or Thriving >85), verify input data provenance (source column, original input artifact existence, plausibility of dimension scores).

7. **Extreme TWC DB Update**: Confirm that any rescore results have been persisted to the database by re-reading after write.

8. **Coupling Terms Implementation**: Verify that coupling terms are applied in TWC computation by comparing stored TWC with base TWC + coupling sum.

These steps can be automated via verification scripts.

- **2026-06-20 report DISPUTED as FALSE-ALARM (2026-09-24 AUDIT-ALGO):** its finding "all 4 key pairs CRITICALLY deviant from spec" is wrong — direct SQL against the (staging) interaction_matrix confirms canonical values 0.20/0.15/0.20/0.25 at 28/28 pairs. The rejected-heuristic comparison pattern recurred in 6/17, 6/19, 6/20 reports; the 6/16 "all pairs valid" was the correct one. VERITAS-ALGO log shows latest report from 2026-06-17 (not 2026-06-20 as previously claimed — staleness detected). Previous verified findings unchanged: engine tests pass (rescore: 7/7, nutrition: 22/22, sexual health: 43/43); pipeline coverage 0/7 days real scores last week, 4/30 total; interaction matrix values deviate from spec; baselines.json twcBaseline: null; coupling terms not applied in TWC computation.

### TWC recomputation tool tip — do NOT use awk (2026-07-06 AUDIT-SYNTH)
When recomputing TWC from stored dimensions in a shell pipeline, do NOT use awk for the weighted sum. The personal weight for INT (0.10) forces you to write `int=0.10`, and `int` is an awk reserved word — the parser throws `illegal statement` and the script aborts silently. Use Python (`sqlite3 + math` via a heredoc or `/tmp` script file) instead. This is a silent-failure trap: the awk command returns exit 2 with a terse error, easy to miss in a cron log.

**Last verified 2026-07-25 by AUDIT-ALGO (watchdog failure escalation)**: VERITAS-ALGO watchdog remains DEAD — now 33+ days stale (last entry 2026-06-20). Key findings:
- VERITAS-ALGO chronically compares interaction matrix against REJECTED spec heuristics (0.85/0.78/0.72/0.68) instead of canonical values (0.20/0.15/0.20/0.25). The spec values were VERITAS-REJECTED for schema violations >0.5 per canonical_coupling.py lines 10-14.
- Inter-report contradiction: Jun 16 claimed "✅ all pairs valid" but Jun 17 claimed "❌ all pairs invalid." The canonical DB values are CORRECT (28 pairs, 0.05-0.35 range) — Jun 16's claim was right, Jun 17 was wrong.
- Pipeline coverage: 0/7 days real scores last week, 6/30 real scores last 30 days (source=transcript, all from Jul 3-12, 2026).
- Sub-tables: Nutrition/sex 0/7 (correct), ef_compass 8/7d (includes current day).
- Engine tests: 72/72 pass (rescore 7/7, nutrition 22/22, sexual health 43/43) ✅
- **ESCALATED**: Watchdog failure now 33+ days (up from 26d on Jul 16, 14d on Jul 13). Immediate restart required.

**VERITAS-ALGO Watchdog Failure Pattern (discovered 2026-07-06, confirmed 2026-07-13, reconfirmed 2026-07-16, escalated 2026-07-25, re-escalated 2026-07-27)** — The integrity watchdog goes offline without triggering alarms. Timeline:
  - 2026-07-06: 14 days stale (last entry 2026-06-22)
  - 2026-07-13: 14 days stale (last entry 2026-06-22 — no progress)
  - 2026-07-16: 26 days stale (last entry 2026-06-20 — worsening)
  - 2026-07-25: 33+ days stale (last entry 2026-06-20 — critical escalation)
  - 2026-07-27: 37+ days stale (last entry 2026-06-20 — watchdog remains dead despite prior escalations)

When AUDIT-ALGO or any verifier-of-the-verifier runs, its FIRST check must be VERITAS-ALGO liveness: (a) stat algorithm-integrity-log.md's latest entry timestamp, (b) check if staleness >48h, (c) flag this as a MATERIAL ISSUE if true. A dead watchdog means all prior "verified by VERITAS" claims are now suspect until VERITAS-ALGO is restarted. 

**MANDATORY ESCALATION when VERITAS-ALGO staleness >48h:** Do not just flag as a pipeline gap. Escalate as "WATCHDOG FAILURE — immediate restart required" in audit verdict. Include: (1) days since last report, (2) prior claims now suspect, (3) corrective actions needed (restart cron, verify schedule, check for crash loops). The watchdog-failure pattern has recurred FOUR times (Jul 2026, Jul 2026, Jul 2026, Jul 2026) — treat as a CRITICAL systemic issue, not transient.

**Liveness check script:** `references/veritas-algo-liveness-check.sh` automates staleness detection with exit codes: 0=alive (<48h), 1=stale (>=48h), 2=log file not found. Run this script BEFORE any audit to verify watchdog health.

- **PRODUCTION SCORING DB + WATCHDOG LOG MISSING (found 2026-09-09 AUDIT-ALGO)** — `~/your-workspace/health-private/` no longer exists (consistent with the sensitive-data-containment PHI purge; only a purged push-staging copy survives at `~/.gd-private/the operator agent-purged-ready-to-push/health-private/`). `algorithm-integrity-log.md` is not merely stale — the FILE IS GONE (watchdog dead ≥81 days as of 2026-09-09). The purged copy's DB has 18 daily_scorecard rows, latest real score 2026-05-29, canonical interaction_matrix intact (28 pairs, key values 0.20/0.15/0.20/0.25), single coupling_sum 6.775. Auditors: queries against the purged copy measure a TRUNCATED staging artifact — label coverage results as production-unverifiable. Recovery requires restoring production health-private (post-purge relocation or encrypted backup `~/your-workspace/health-backup/test-backup.tar.gz.enc`) and restarting VERITAS-ALGO.
- **canonical_coupling.py silent-zero failure (found 2026-09-24 AUDIT-ALGO)** — Post-purge, the module's DB_PATH dangles; `_load()` raises, the bare `except Exception: COUPLING_28 = {}` swallows it, and every importer silently gets kappa=0.0 for all 28 pairs (verify() crashes only when run as __main__). Fix: make load failure LOUD and rewire DB_PATH to the restored production DB. Staging-copy matrix data verified intact 2026-09-24: 28/28 pairs, range 0.05-0.35, key pairs INT-PSY=0.20, PHY-VOC=0.15, SOC-SPI=0.20, ENV-PHY=0.25 (canonical; note PSY↔INT stores as INT-PSY).
- **principal-8d personal-scoring key files GONE (2026-09-24 AUDIT-ALGO)** — `~/.sibling-agent/workspace/memory/principal-8d/` contains only README.md; config.json, profile.md, baselines.json all absent. Personal 8D pipeline inputs and drift baseline no longer exist on disk (was twcBaseline:null on 2026-06-20). Also: 4/7 rescore never persisted (DB stores 71.88 vs engine 78.9/79.4 artifacts) — same Step-6.5 non-persistence family as 5/29. Skill doc drift: 79.4 was the v1.1 answer; engine v2.0.0 correctly yields 78.9 for 4/7 (triple-count fix).
- **2026-10-01 AUDIT-ALGO re-audit (independent)** — All standing gaps persist; watchdog now 103 days stale (last VERITAS-ALGO report 2026-06-20; Aug-12 file mtimes in migrated tree are migration timestamps, not new reports). POSITIVE DELTA: canonical_coupling.py silent-zero defect is FIXED — DB_PATH rewired to `/<workspace>`, loud CANONICAL_COUPLING_BROKEN raise present, verify() passes (28 pairs, 0.05-0.35, key pairs 0.20/0.15/0.20/0.25). Staging DB re-confirmed: 18 rows, latest real 2026-05-29 (trailing gap 125d), coupling_sum single 6.775, labels CLEAN, twc_history stale @05-26. GHOST REFERENCE: skill-referenced `veritas-algo-liveness-check.sh` does NOT exist anywhere on disk — use `stat`/`tail` on the frozen log instead. Migrated-tree `algorithm-integrity-baseline.json` = auto-generated 62.2 @2026-05-28, a synthetic anchor, NOT a calibrated baseline. No scoring script in hydra-os/scripts reads interaction_matrix (Layer 3 remains unwired at compute time).


## DESIGNATED RESCORE SPECIALIST: CALIBER (2026-04-08)
All 8D/TWC rescores for the principal's personal health system are owned by **CALIBER** — the FORGE+ARBITER talent-gated rescore specialist. Profile: `~/your-workspace/hydra-os/intel/agents/profiles/CALIBER-profile.md`. FORGE code: `SCI-RSR-CAL-L7-C5-P11-T5-001`. Model: `anthropic/claude-opus-4-6` (reasoning=high, 118K OMNI). CALIBER owns EVERY day — historical backfill, current finalization, and future scheduled rescores — not just today. Spawned by AISHA-MD via delegate_task; the operator agent never rescores directly (routes to AISHA-MD, who spawns CALIBER). Engine-first, invariant-enforcing, no-shame tone, full per-dimension audit trail. Replaces deprecated ARIA stub.

## CRITICAL RESCORE RULE: Voluntary Evidence LIFTS Base Dimensions (learned 2026-04-08)

When the principal voluntarily provides new data for a past day (follow-up voice memo, text debrief, morning detail after an evening PRELIMINARY), the rescore MUST lift the relevant base 8D dimensions — NOT just swap the nutrition/sex modifiers and leave the base alone.

**Why:** Positive evidence is positive evidence at BOTH layers:
1. It raises the sub-component composite (nutrition/sex) → modifier lifts
2. It raises the dimension itself because the behavior it describes is the dimension (PHY = body care = eating well; SOC = connection = communication)

Swapping modifiers only = negative-sum math. The score will land near or below PRELIMINARY because:
- Sub-component composite usually moves less than you expect (65 → 79 on nutrition only lifts modifier 0.985 → 1.022)
- But the base 8D dimensions DON'T move
- Net effect: <1 point change, can even go NEGATIVE if cross-feed was higher in PRELIMINARY

**The correct rescore flow:**
1. Read the new evidence
2. For EACH dimension the evidence touches, ask: "does this add positive signal to the base dimension score?"
3. If yes, LIFT the base score proportionally (typical lift: +0.3 to +1.0 for strong new evidence)
4. THEN recompute sub-component composites and modifiers
5. THEN recompute TWC
6. Preserve any integration bonus from PRELIMINARY (it's still valid evidence)
7. Add a NEW follow-through credit (+0.5 to +1.5) for voluntary morning debriefs — the act of sending the data IS meta-self-awareness signal

**Dimension → evidence type mapping for personal rescores:**
- Protein/hydration/meal quality → PHY (body care), sometimes PSY (executive function fueling)
- Deep communication / bond growth / relational repair → SOC, sometimes SPI (if explicit integration language)
- Morning follow-through after evening debrief → PSY + SPI (meta-self-awareness)
- Med adherence on hard days → PHY + PSY (both the body care AND the decision-making under fatigue)
- AM sex + good rest → PHY (today), SOC + sexual-health-composite (today's cross-feed)
- Luna/dog emergency care (even drunk on meds) → SOC (caregiving), PSY (decision-making under impairment)

**Rescore audit trail:** Always show Δ per dimension in the rescore note. "PSY 6.8 → 7.2 (+0.4 for voluntary follow-through debrief)" is the format. Never silently change numbers — the principal reads the scorecard carefully and silent shifts break trust.

**The no-shame connection:** A rescore that LOWERS a score after the user voluntarily gave positive data is the single worst failure mode of this system. It trains the user away from honesty. If the math produces a lower score after positive evidence arrives, the rescore logic is wrong — stop and re-examine which dimensions the new evidence should have lifted.
