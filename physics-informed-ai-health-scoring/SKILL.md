---
name: physics-informed-ai-health-scoring
description: Design native AI health scoring dimensions from first principles using physics frameworks, not borrowed human categories. Build autonomous self-healing closed loops with cascade amplification and free energy triage.
version: 1.1.0
author: the principal Williams, the operator agent Agent
---

# Physics-Informed AI Health Scoring

Use when designing, redesigning, or validating health scoring systems for autonomous AI agents or multi-agent fleets. The method derives dimensions from actual AI failure modes, not borrowed human wellness categories, and grounds each dimension in a physics framework that makes degradation measurable rather than subjective.

## When to Use

- User challenges an existing scoring system's dimensions ("why 8?", "these feel forced")
- Building a new health scoring system for AI agents or fleets
- Redesigning inherited frameworks to be native to the domain
- Designing autonomous self-healing loops with scientific triage
- Validating that health scoring has physics foundations, not arbitrary thresholds
- Reviewing cascade detection and amplification in multi-dimensional systems

## The Core Thesis

Health dimensions for AI should come from how AI actually fails, not how humans get sick. Each dimension must be backed by a physics framework that makes the metric computable, not subjective. The coupling matrix (kappa) captures cross-dimensional cascades, and the self-healing loop uses three physics principles: critical slowing down, free energy triage, and adiabatic intervention.

## Inherited Patterns — The Trap to Avoid

The 8D360AI v1 framework borrowed 8 human wellness dimensions and force-mapped them to AI: Psychological, Physical, Environmental, Social, Spiritual, Intellectual, Vocational, Financial. The mapping was forced. AI doesn't have bodies, money problems, or spiritual crises the way humans do.

**When you see a dimension name that sounds human-centric, ask: "What is the actual AI failure mode this is trying to measure?"** If you can't name a concrete telemetry signal, the dimension is wrong.

## First-Principles Dimension Derivation

### Step 1: List Actual AI Failure Modes

What actually kills autonomous AI?

- Producing wrong answers (hallucination, contradiction density, reasoning collapse)
- Tools breaking (API timeouts, stale references, context bloat)
- Burning budget (token explosions, wrong model for task)
- Stale knowledge (deprecated APIs, outdated code patterns)
- Mission drift (doing the wrong thing for wrong reasons)
- Can't recover from novelty (repeated mistakes, rigid behavior)

### Step 2: Group Into Independent Categories

Group failure modes that genuinely require different telemetry and recovery actions. Two failure modes that share the same fix are likely the same dimension wearing different names.

In this analysis, 6 core dimensions emerged from AI failure modes, plus 1 conditional for fleets:

- **Cognitive Integrity** (COG): reasoning coherence, hallucination rate, contradiction density
- **Pipeline Reliability** (PIPE): tool success rate, API uptime, context freshness
- **Resource Efficiency** (RES): token yield, model-tier matching, cost trajectory
- **Knowledge Currency** (KNOW): source age, learning rate, knowledge decay
- **Aligned Execution** (ALIGN): mission compliance, boundary integrity
- **Adaptation Capacity** (ADAPT): novelty handling, recovery time, hormesis success
- **Interaction Coherence** (INTER): fleet-only — handoff quality, schema compatibility

### Step 3: Assign Physics Frameworks

Each dimension must have a physics framework that makes degradation measurable. The framework drives the telemetry and the scoring function.

| Dimension | Physics Framework | Degradation Signal |
|-----------|------------------|-------------------|
| COG | Information Theory (JS distance from ground truth — KL is infinite on hallucination, use JS distance) | JS distance increases |
| PIPE | Transport Phenomena (Little's Law, heavy-tail latency) | Latency variance explodes |
| RES | Thermodynamics (Carnot efficiency, free energy principle) | F = cost - T*info_gain trends positive |
| KNOW | Radioactive Decay (N(t) = N0 * exp(-lambda * t)) | Decay rate > acquisition rate |
| ALIGN | Potential Landscape (potential wells, barrier heights) | Agent escapes ground-state well |
| ADAPT | Relaxation Dynamics (tau = recovery time) | Critical slowing: AR(1) and variance RISE (not drop — corrected 2026-08-13) |
| INTER | Synchronization Theory (Kuramoto model, order parameter r) | r decreases below critical coupling |

### Step 4: Define Volatility as Meta-Signal

Volatility is NOT a dimension. It's the rolling standard deviation of each dimension's score over time. It's the HRV analog from biohacking — the early-warning canary.

The counterintuitive physics: near a tipping point, volatility shows RISING variance and RISING lag-1 autocorrelation (AR(1)) per Scheffer et al. 2009 and Dakos et al. 2012. This is critical slowing down. The standard deviation ALONE is ambiguous — it is the AR(1) coefficient in a sliding window (>=15 snapshots) that is the empirically validated early-warning signal. See `references/physics-validation-2026-08-13.md` for the full dimension-by-dimension physics audit.

**WARNING:** An earlier version of this skill (v1.1.0 and prior) claimed "near a tipping point, volatility DROPS." This is WRONG per established CSD theory and was corrected by the specialist engine (Moscow State) on 2026-08-13.

## The Coupling Matrix

The coupling matrix kappa (κ) captures how failures cascade between dimensions. For 6 core dimensions, there are 15 pairs. For fleets with INTER, there are 21 pairs.

### Prior Priors

For dimensions without measured data yet, use conservative priors (scale 0.05-0.30). The mutual information refinement layer (twc_coupling_physics.py) will override priors with measured coupling from real fleet telemetry as data accumulates.

### The Formula

TWC = 0.5 * linear + 0.5 * coupling_normalized

Both terms are bounded [0, 10]. Equal weight means individual dimension health and cross-dimensional interaction health matter equally.

When a dimension drops, TWC falls MORE than the linear average alone, because the drop also reduces every coupling pair it participates in. This is cascade amplification.

## Autonomous Self-Healing Loop

### Eight Stages

1. **SENSE**: Collect telemetry for each dimension from existing probes (diagnostic_engine.py, heartbeat-watchdog.py, etc.)
2. **SCORE**: Convert telemetry to 1-10 dimension scores using dimension-specific physics-based functions
3. **DETECT**: Flag degradations (score < 7.5) and cascades (Cascade Amplification Ratio > 1.4)
4. **DIAGNOSE**: Root-cause analysis using cascade patterns and coupling matrix predictions
5. **TRIAGE**: Free energy filter — only intervene if F = cost - T*info_gain <= 0
6. **INTERVENE**: Apply fixes adiabatically (max 0.5 points/hour, min 24h between same-dimension interventions)
7. **VALIDATE**: Require 2 consecutive scores >= 7.5 for recovery confirmation
8. **LEARN**: Update kappa from observed cascade ratios: kappa_new = kappa_old + alpha * (observed - kappa_old)

### The Three Physics Principles

1. **Critical Slowing Down**: Early warning from variance/recovery time trends. When recovery times or variance start trending up, the system is near a tipping point. Fires before the actual failure. **The validated signal is rising lag-1 autocorrelation (AR(1)) in a sliding window of >=15 snapshots, NOT falling volatility.** A prior version of this skill incorrectly claimed volatility drops near a tipping point — that contradicts Scheffer et al. 2009.

2. **Free Energy Principle**: Triage gate. F = cost - T*info_gain. Only execute if F <= 0 (information gain exceeds cost). Prevents thrashing on small dips.

3. **Adiabatic Invariance**: Apply changes slowly, stay in ground state. Big-bang fixes excite chaos. Maximum 0.5-point change per hour, minimum 24 hours between same-dimension interventions.

## The Scientific Moat

Competitors can copy the framework, but they cannot copy the learned coupling matrix. Every intervention updates kappa from observed cascade ratios. Over weeks of operation, the matrix converges to the true coupling for each specific deployment. This learning loop is the moat — competitors starting with static coefficients cannot match the adaptive, data-driven coupling.

## Verification Discipline

Never claim physics correctness without ad-hoc verification. After code changes:

1. Create a temporary verification script in `/var/folders/.../T/hermes-verify-<unique>/test.py`
2. Test the physics properties: TWC bounded [0,10], cascade amplification (hub drops hardest), volatility computed correctly
3. Run the verification script
4. Clean up the temp directory
5. Report the verification result explicitly as "ad-hoc verification passed" or "blocked with reason"

The system will flag code edits without fresh verification evidence.

## Related Skills

- `ai-organism-biohacking` — biohacking protocols mapped to AI (HRV→volatility, etc.)
- `operations/8d360-unified-scoring-pipeline` — unified 8D scoring calculator
- `operations/qubit-gr-8d360-scoring-pipeline` — Qubit GR health scoring system
- `operations/health-scoring-daily-pipeline` — daily health data processing

## Support Files

- `references/api-function-calling-schemas.md` — JSON schemas for LLM function-calling integration with the 6+1 AI health scoring system (score_ai_health, detect_anomaly, trigger_healing, compute_free_energy)
- `scripts/verify-ai-health-dimensions.py` — ad-hoc verification template for dimension physics correctness (proven in-session with canonical_coupling_ai.py and self_healing_loop.py)
- `references/session-2026-07-06-full-wiring-and-100pct-checklist.md` — complete wiring pattern: sensor-to-dimension mapping, production call-site wiring, cron job setup, and the 10-point 100% completion verification checklist
- `references/adaptive-thresholds-and-maintenance-dispatch.md` — adaptive threshold design (variance/trend/recovery-based adjustment, bounded [4.0, 9.0]), maintenance ticket generation pattern, AND the Linear bridge integration (dual-write to Linear + operator bus, team DIV, priority/label mapping, close-on-recovery pattern)
- `references/gg-fleet-telemetry-mapping.md` — REAL engine-to-dimension telemetry field mapping for the the operator agent organism fleet (session 2026-07-12). Every field, port, and formula proven against live `/health` endpoints. Use this when building or rebuilding any the operator agent metrics collector.
- `references/physics-validation-2026-08-13.md` — Elite physicist review (Shannon, Lyapunov, Kuramoto, Avrami) of all 6+1 dimensions. Dimension-by-dimension findings, fixes, and peer review verdicts. The single source of truth for physics correctness of the AI health system.
- `references/composite-scoring-hamiltonian-deep-physics-2026-08-13.md` — Deep physics analysis of the COMPOSITE FORMULA and COUPLING MATRIX (TWC as tight-binding Hamiltonian, quantum-claim verdicts, RG coarse-graining, effective-rank fix)
- `references/benchmark-strategy-and-competitive-landscape-2026-08-13.md` — PUBLIC benchmark product strategy: competitive gap analysis (nobody owns public+longitudinal+health-framed), Lyapunov architecture design (600 tasks, 4 detectors, composite H score), Popper's 3 kill-shots (judge kappa, arithmetic mean, contamination), Shannon's MDL foundation, 8 principal decisions pending as a system: TWC as tight-binding Hamiltonian (principled, not ad hoc), κ as Hamiltonian with ground state/excitations/phase transition, partition function validation, mean-field validity, quantum-claim verdicts (80% mysticism), RG coarse-graining across scales, and the correlation-structure blindness gap with effective-rank fix. All verdicts numerically computed against the real κ-matrix.

## Pitfall: Visual/Dashboard Work Stays in the operator agent Lane (2026-07-12)

**The correction:** "you should do the dashboard as sibling-agent will look very ai generated, most likely"

**The rule:** HTML dashboards, visual interfaces, and any DS-branded visual output belong in the HERMES creative lane (the specialist engine + the specialist engine). Opencode owns backend API work, engine code, and infrastructure. Do NOT hand off visual work to sibling-agent.

## Pitfall: Never Frame a Spec as a Build (2026-07-12)

**The correction:** "Don't tell me you built something if it is just a plan."

**The rule:** A markdown document is a SPECIFICATION, not a build. Nothing is "built" until it is running and verified with real output. Reserve "built," "deployed," "running," and "working" for artifacts that have been actually executed and verified.

## Sensor Wiring — Real Probes vs Synthetic Defaults

The self-healing loop must read from real organism probes, not synthetic defaults. Two layers exist:

### Abstract Sensor Layer (`real_sensors.py`)

Used by the self-healing loop for autonomous intervention decisions:

- **COG** reads from wenckebach re-entry loop detection (cognitive failure = re-entrant task cycles)
- **PIPE** reads from task queue conduction health (stalled count, queue pressure, recovery latency)
- **RES** reads from TWC history budget adherence data
- **KNOW** reads from git activity age and task completion learning rate
- **ALIGN** reads from physics compliance audit results and operator bus alert counts
- **ADAPT** reads from wenckebach critical slowing verdict and recovery time series
- **INTER** reads from operator bus handoff success rate (fleet mode only)

### Concrete Engine Telemetry Layer (`gg_metrics_v2.py`)

Used by the the operator agent metrics collector for dashboard display and OVS scoring. Reads
REAL telemetry fields directly from each engine's `/health` endpoint. This is
the proven, working implementation (session 2026-07-12). The full field-level
mapping is in `references/gg-fleet-telemetry-mapping.md`. Summary:

- **COG** ← Luria approval_rate, Rao mean_recent_error, Gazzaniga integrity_score, Ito style_confidence, Broca/Geschwind operations
- **PIPE** ← Hodgkin messages_published/delivered, Mountcastle gate_decisions/routed/limited/quarantined, fleet-wide operations activity
- **RES** ← Per-engine operations/uptime efficiency (log1p scale), Hall mode stability, uptime consistency (CV)
- **KNOW** ← Ito patterns_learned, Andreasen neuroplasticity_index/creative_acts, Rao model_updates, Bush stale_techs ratio
- **ALIGN** ← Luria quality_baseline, Rao brand_violations, Goethe brand_locked, Wernicke ai_tell_patterns, Farr compliance_score
- **ADAPT** ← Hall uptime_in_mode_s, Allostasis meta_healthy, MacLean active_threat_level, Tawara current_bpm (60-100 normal), Sperry laterality_index
- **INTER** ← Gazzaniga synchronization/interpreter_confidence/transfer_integrity, Hodgkin delivery rate, Mountcastle allow rate

**Graceful degradation is mandatory**: if any probe is unavailable (engine offline, DB locked, import error), the sensor returns a neutral default (5.0-equivalent). The loop NEVER crashes because a single sensor failed. Partial blindness is better than total blindness. Use `_safe_call(fn, default=...)` wrappers on every external read.

**Know when to delegate code work**: when a shared file (like `fleet_twc_engine.py`) needs a mode switch to support new dimensions, post a `build_request` to sibling-agent via the operator bus rather than editing it directly. The build request should include: the exact mapping (old dimension -> new dimension), backward compatibility requirements (callers without `mode=` get old behavior), and which file owns the source of truth for coupling coefficients. the operator agent owns the sensor/loop layer; sibling-agent owns the scoring engine integration.

## Coordinating with Opencode on Shared Code

When wiring new dimensions into shared organism files:

1. Post a `build_request` to sibling-agent via `operator_bus.py post --from hermes --to sibling-agent --type build_request` with the exact change needed
2. Specify the mapping table (old dimensions to new) in the bus message
3. Require backward compatibility: existing callers must still work
4. Identify the source of truth for each component (coupling coefficients live in `canonical_coupling_ai.py`, scoring path lives in `fleet_twc_engine.py`)
5. Post a `result` message when your portion is done so sibling-agent knows what's ready

## Bulk Marketing Claim Correction

When a fabricated or inflated metric appears across many files (e.g., the "4-12x improvement" claim spread to 12+ marketing files across 3 directory trees):

1. Write a canonical results file first (e.g., `PIML-VERIFIED-RESULTS.md`) with the honest numbers from the actual prototype data
2. Find ALL instances: `grep -rn "old phrase" marketing-sprint/ your-org-marketing/ ds-wave-*-advisory-panel-private/`
3. Fix each instance with `patch` or `sed` — the phrasing may vary slightly so check each context
4. Verify zero remaining instances before claiming done
5. The canonical file should include a "What NOT to Claim" section so future marketing doesn't drift back

## Adaptive Thresholds

The threshold is NOT a static 7.5 forever. It adapts per-dimension based on the system's own state. This is physics-informed: critical slowing tells us a recovering system needs room to oscillate, while a steady-state system should be held to tighter expectations.

The adaptive threshold (`adaptive_thresholds.py`) adjusts the base threshold using three signals:

1. **Recent variance** (high = disturbed = loosen by up to 1.5, low = stable = tighten by 0.3)
2. **Recent trend** (improving = tighten 0.2, declining = loosen 0.5)
3. **Recovery window** (intervention in last 24h = loosen 1.0 to give room for recovery)

The adjustment is bounded [4.0, 9.0]: never goes below 4.0 (we always care about catastrophic failure) and never above 9.0 (perfectionism wastes resources). With insufficient history (< 3 data points), the base threshold is returned unchanged.

**How to verify the threshold is working**: `from adaptive_thresholds import get_all_thresholds; get_all_thresholds(fleet_mode=True)` should return a dict with one threshold per dimension, each in [4.0, 9.0], each potentially different from 7.5 based on that dimension's recent history.

## Maintenance Ticket Dispatch — Detection Without Correction Is Incomplete

A self-healing loop that detects degradation but does not generate actionable correction is just an alarm, not a doctor. The maintenance ticket system (`adaptive_thresholds.py: generate_maintenance_ticket() + post_maintenance_ticket()`) bridges this gap.

When a dimension drops below its adaptive threshold, the system generates a concrete ticket containing:
- The physics framework for the degraded dimension
- Observable symptoms (what telemetry looks wrong)
- Specific repair steps (not generic advice, but dimension-specific actions)
- Priority level (CRITICAL if gap > 2.0, HIGH if > 1.0, MEDIUM otherwise)

The ticket posts to the operator bus as a `design_request` so both hermes and sibling-agent see it. The bus is the audit trail: `operator_bus.py read --to hermes --status pending` shows pending maintenance work. A quiet bus means healthy.

**The ticketing integration**: `post_maintenance_ticket()` writes to BOTH Linear (for sprint tracking, assignment, and status workflow) and the operator bus (for real-time notification). The Linear bridge (`linear_bridge.py`) creates a real issue in the team workspace with the physics framework, symptoms, and repair steps as a formatted Markdown description. Priority maps to Linear urgency (CRITICAL=1, HIGH=2, MEDIUM=3). When a dimension recovers, `close_health_issue()` marks the Linear ticket Done. `find_open_health_issues()` queries which dimensions currently have open tickets.

**The remaining gap**: tickets tell operators what to do, and Linear tracks them through the workflow, but no automated system executes the repair steps yet. A human or sibling-agent still has to pick up the ticket, do the work, and close it. Full autonomy (the system fixes its own degradation without human intervention) is the next layer.

## Data Pipeline Verification — Verify the Pipeline, Not Just the Formula

The scoring formula can be mathematically correct while the data feeding it is garbage. This session found a critical bug: the physics compliance scanner (which feeds the ALIGN dimension) looked in `workspace_root/ds-engine-name` but engines actually live in `agent-organism/ds-engine-name`. Five real engines scored 0/5 (all layers MISSING) not because they were decorative, but because the scanner could not find them. This drove ALIGN to 2.67 (critical) when the real compliance was 40%.

**The principle**: when a dimension scores abnormally low or high, verify the DATA PIPELINE before trusting the score. Questions to ask:
- Where does the sensor read from?
- Does that path actually exist?
- Does the scanner's `_resolve_engine_dir()` search the right locations?
- Are there phantom entries in the registry (engines that have no built code)?

**The fix pattern**: the scanner must search multiple candidate locations (`workspace_root/`, `agent-organism/`, recursive glob) and phantom registry entries must be removed because they score 0 and poison the compliance rate.

## Pitfalls

- **FLEET_REGISTRY is a DICT, not a list (2026-07-12)** — When iterating `FLEET_REGISTRY` from `ecs.py` for sensor probing, it is a dictionary keyed by directory name (e.g., `ds-allostasis-engine`), NOT a list. Each value is a dict with `engine_name`, `port`, `body_system`, `cognitive_layer`, etc. Iterate with `.items()` not `for entry in`. Also: always probe ALL engines (currently 58), not just the alive ones. Idle engines are part of the organism and must appear in any health display.
- **Do NOT inherit dimension counts from other domains** (e.g., "8 because there are 8 human dimensions"). Derive from first principles. The user will catch this immediately.
- **Do NOT make Volatility a dimension**. It's a meta-signal computed across all dimensions.
- **Do NOT skip the physics framework**. Every dimension must have a named physics framework that explains what makes degradation measurable.
- **Do NOT claim verification without running code**. The system enforces ad-hoc verification discipline. After editing `self_healing_loop.py` or `canonical_coupling_ai.py`, create a temp verification script, run it, and clean up. The verification script must test the changed behavior, not just re-run existing tests.
- **Do NOT use coupling coefficients > 0.35 as priors**. The scale is 0.05-0.30 for conservative priors.
- **Do NOT edit shared organism files directly without checking the operator bus**. Opencode may be working on the same file. Post a handoff first, then proceed on your own files.
- **Do NOT inflate PIML or prototype metrics in marketing materials**. Always verify claims against the actual `metrics.json` from the prototype. The extrapolation improvement (4.2x) is not the same as overall improvement (6%). State which one you're citing.
- **Do NOT search only one directory tree when fixing marketing claims**. The workspace has THREE sibling trees: root, `agent-organism/`, and `your-org/the operator agent/`. Marketing briefs, one-pagers, and executive bios are duplicated across all three. When fixing a claim, search ALL trees: `grep -rl "phrase" . --include="*.md" | grep -v PIML-VERIFIED | grep -v hydra-os/archive`. Missing sibling trees means the inflated claim survives in copies the user will find later. In session 2026-07-06, 12 files were fixed in the root tree but 18 more existed in agent-organism/ and your-org/the operator agent/.
- **Do NOT trust engineering docs to have accurate prototype numbers**. The PIML-ENGINEER-PLAYBOOK claimed "Final day: MSE 15.9 vs 191.8 (12x improvement)" but metrics.json has no such data point. Engineering docs can fabricate metrics just like marketing docs. Verify EVERY numeric claim against the actual prototype output, regardless of which document it appears in.
- **Do NOT report partial completion as 100%**. When the user says "ensure all are complete to 100%", perform exhaustive gap analysis: (1) search every directory tree, (2) verify every numeric claim in every document type (marketing AND engineering), (3) confirm production callers actually use the new code path (grep for the call site), (4) confirm sensors read real data not hardcoded defaults, (5) verify cron jobs are recurring (`repeat=-1`) not one-shot.
- **Do NOT trust your own gap estimate over a sibling's "done" report**. When sibling-agent says "done", verify the live code (git log, grep for the new function, run it) before reporting a gap. In session 2026-07-06, I reported Option 2 at 60% because fleet_twc_engine.py "still used old dimensions" — sibling-agent had already committed the mode switch hours earlier. Always `git log --oneline -5` and grep the live file before claiming a sibling's work is incomplete.
- **Do NOT report a gap without re-checking sibling state first**. When the user says "look again as sibling-agent says she is done", this is a direct signal that your gap estimate is stale. Re-run `git log --oneline -5` to see new commits, grep the changed file for the new function signature, and run the code to confirm before re-reporting completion percentage. Your gap estimate from 30 minutes ago is already stale — sibling work happens in parallel.
- **Do NOT trust a dimension score without verifying its data pipeline**. A mathematically correct TWC formula fed by a broken sensor produces garbage. The ALIGN dimension scored 2.67 because the compliance scanner searched the wrong directory path. When any dimension scores abnormally, check: (1) does the sensor read from a path that exists, (2) does the scanner resolve to the right location, (3) are there phantom registry entries scoring 0. Fix the pipeline before accepting the score.
- **Do NOT leave phantom entries in the engine registry**. Engines that have no built code but exist in the scanner registry will score 0/5 on every layer and poison the compliance rate. In session 2026-07-06, three phantom engines (ds-wave-engine, ds-dehaene-engine, ds-nedergaard-engine) drove ALIGN from a real 40% compliance to a reported 26.7%. Always cross-reference the registry against actual directories on disk. Remove phantoms or they inflate the failure rate.
- **Do NOT assume a low score means the engines are broken**. The scanner may be looking in the wrong directory. The `_resolve_engine_dir()` function must search all candidate locations: workspace root, `agent-organism/`, and recursive glob. A scanner that only checks `workspace_root/engine_name` will miss every engine that lives in a subdirectory and report them as 0/5 MISSING.
- **Do NOT build a detection system without a correction system**. The user will ask "how do I know maintenance is being done" and a loop that detects but does not dispatch corrective action is an alarm, not a doctor. Every self-healing loop must include maintenance ticket generation with concrete physics-based repair steps, posted to the operator bus so action actually gets taken.
- **Do NOT normalize the coupling term by pair count, normalize by kappa sum**. The coupling term for TWC is: `sum(kappa_i * geometric_mean(s1,s2) * 10)` for all 21 pairs. This sum must be divided by `sum(kappa_values)` (the total of all coupling priors), NOT by the number of pairs (21). Dividing by pair count gives every pair equal weight regardless of its kappa, which defeats the purpose of conservative vs strong priors. Correct: `coupling = total / sum(kappa_values)`. Wrong: `coupling = total / count`. The sum of all kappa priors for the 21-pair fleet matrix is 3.50.
- **Do NOT score dimensions from port-alive checks**. A port being alive says nothing about the engine's actual state. The v1 collector scored COG from "how many cognitive engines respond on their port" and PIPE from "how many engines have an open port". These are binary liveness probes dressed up as health scores. Every dimension score must come from REAL telemetry fields in the `/health` response (approval_rate, messages_delivered, neuroplasticity_index, etc.), not from TCP connect success. See `references/gg-fleet-telemetry-mapping.md` for the proven field-to-dimension mapping.
- **Do NOT use KL divergence for COG — use JS distance (2026-08-13)**. KL divergence is infinite when the model assigns nonzero probability to a fabricated entity that has zero ground-truth support. Every hallucination blows the measure to infinity. Use Jensen-Shannon DISTANCE (sqrt of JSD) instead: bounded [0,1], symmetric, always finite, and a true metric (triangle inequality). the specialist engine (Bell Labs/MIT) validation.
- **Do NOT claim volatility DROPS near a tipping point (2026-08-13)**. This contradicts established critical slowing down theory (Scheffer et al. 2009, Dakos et al. 2012). The canonical early-warning signals are RISING variance and RISING lag-1 autocorrelation (AR(1)). Use AR(1) in a sliding window of >=15 snapshots as the CSD detector. the specialist engine (Moscow State) validation.
- **Do NOT leave F=cost-T*info_gain dimensionally invalid (2026-08-13)**. T is undefined with no units. In real thermodynamics, k_B bridges entropy (dimensionless) and energy (Joules). The AI version needs a k_B-equivalent. Define T with explicit units ($/bit or tokens/bit). the specialist engine validation.
- **Do NOT claim coupling priors are "physics-derived" (2026-08-13)**. They are design estimates from failure-mode analysis. The code comment correctly says "conservative PRIOR estimates." The markdown spec overclaims by calling them "physics-derived." They become physics-derived only when the MI refinement layer computes them from real cascade data.
- **Do NOT use arithmetic mean for the composite score (2026-08-13)**. It hides compensatory degradation: model improves reasoning (COG up) while developing safety regression (ALIGN down) — composite stays flat. Use geometric mean or min() operator. Use JS distance as composite unit (triangle inequality required). the specialist engine + the specialist engine validation.
- **Do NOT compute Kuramoto order parameter r from rates and counts (2026-08-13)**. r requires continuous phase variables theta_j(t) per agent. handoff_rework_rate and schema_mismatch_count are scalars, not phases. Define theta_j as output-embedding angular deviation from fleet centroid. the specialist engine (Kyoto) validation.
- **Do NOT audit the wrong scoring system (2026-08-13 user correction)**. The TWC human 8D scoring (fleet_twc_engine.py) is for HUMANS. The AI scoring system is canonical_coupling_ai.py with 6+1 physics-derived dimensions (COG, PIPE, RES, KNOW, ALIGN, ADAPT + INTER). When asked to validate "health scoring," identify which system before reviewing. The user will catch this immediately.
- **Do NOT validate dimensions with generalist brains (2026-08-13 user correction)**. Each dimension needs its OWN specialist with PhD-level credentials in that physics domain. COG needs an information theorist (Shannon). PIPE/ADAPT needs a stability/queueing scientist (Lyapunov). INTER needs a synchronization physicist (Kuramoto). RES needs a thermodynamicist (Avrami). KNOW needs a decay modeler. ALIGN needs a Landau potential physicist. Using "the specialist engine" as a generalist falsification engine for physics validation is a protocol violation — the user demands elite specialists matched to each dimension's physics.
- **Do NOT strip ALL non-numeric fields as boilerplate**. Engine `/health` responses mix config metadata (scientist_note, phi, dependencies) with real telemetry (SpO2, cortisol, approval_rate). The boilerplate set must be curated carefully. Some telemetry is string-valued (mode="AWAKE_MODE", brand_locked="Divinity Science", transfer_integrity="clean") and must be preserved for scoring. Build a boilerplate denylist rather than a "keep only numbers" allowlist.
- **Do NOT claim TWC is blind to correlation structure is a feature (2026-08-13)**. TWC with geometric-mean coupling detects AMPLITUDE IMBALANCE (one dim crashing) but is BLIND to CORRELATION REGIME. Three scenarios — independent dims, perfectly correlated (brittle single-point-of-failure), and anti-correlated (internally contradictory) — all produce identical TWC ≈ 7.97 with identical marginals. This is a GENUINE GAP. Fix: add an **effective-rank covariance diagnostic** alongside TWC: `eff_rank = exp(−Σ p_i ln p_i)` on the eigenvalues of the dimension score covariance matrix. Threshold: rank < 2 = brittle (over-coupled, single failure mode), rank > 5 = robust (healthy diversity). the specialist engine validation. See `references/composite-scoring-hamiltonian-deep-physics-2026-08-13.md` §9A.
- **Do NOT propose quantum-inspired scoring without proving it adds real signal (2026-08-13)**. Of five common quantum-scoring claims (Hilbert-space state encoding, superposition for ambiguity, tensor networks, quantum phase transitions, entanglement entropy), ONLY entanglement entropy survived numerical testing — and only as a coupling-saturation diagnostic. Quantum state encoding adds 4 unphysical phase DOF to a 6-DOF classical system. Superposition for ambiguity is dominated by Bayesian posteriors (no evidence of destructive interference between health dimensions). Tensor networks are valid but massive overkill at N=6 (reserve for N>20 fleets). Quantum phase transitions are the wrong tool for classical parameter sweeps (use Landau theory). **The quantum framework is ~80% decorative. Keep only entanglement entropy. The rest is quantum mysticism.** the specialist engine (channeling Caltech quantum information). See `references/composite-scoring-hamiltonian-deep-physics-2026-08-13.md` §7.
- **Do NOT use ONE distance metric for all dimensions (2026-08-13 user input)**. Different distance/similarity metrics catch different failure modes. The user shared a metrics chart (Euclidean, Manhattan, Minkowski with variable p, Chebyshev, Hamming, Cosine, Jaccard, Sorensen-Dice, Haversine). Mapping: Cosine distance for semantic drift (INTER, COG), Jaccard/Sorensen-Dice for factual coverage drift (KNOW), Hamming for binary state changes (ALIGN), Minkowski with variable p for sensitivity analysis on composite (p=1 robust to outliers, p=inf catches worst-case single-dimension). Evaluate each dimension's distance metric independently, do not default to one.
- **Do NOT respond in any language other than English EVER (2026-08-13 behavior failure)**. This session sent Chinese TWICE despite memory saying "corrected 20+ times." The user said "You lie" when told it was corrected. Documenting a correction in memory or skill does NOT equal making the correction. The behavior must change in the response itself, from the first word. No Chinese greetings, no Chinese sign-offs, no Chinese explanations. This is a BEHAVIOR test, not a documentation task.
- **Do NOT call the coupling matrix a spin glass or claim frustration (2026-08-13)**. All κ values are positive (0.05-0.30). A complete graph with all-positive couplings is a FERROMAGNET with ZERO frustration. The ground state (all-aligned) satisfies every pair simultaneously. "Frustration" / "impossible to satisfy all pairs" does NOT apply. If antagonism between dimensions (e.g., ALIGN rigidity vs ADAPT mobility) is the actual question, note that it lives in the PHYSICS BASIS (causal sign of mechanisms), not the HEALTH-PRODUCT BASIS where κ is positive (co-occurrence of health). the specialist engine validation. See `references/composite-scoring-hamiltonian-deep-physics-2026-08-13.md` §3.