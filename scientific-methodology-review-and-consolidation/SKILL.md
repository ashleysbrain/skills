---
name: scientific-methodology-review-and-consolidation
description: Multi-specialist scientific methodology review plus implementation-spec consolidation.
triggers:
  - User asks for a science review, methodology review, or expert-panel critique of a research draft
  - User asks for a cybersecurity review, cyber-risk critique, or security/compliance panel synthesis
  - A document mixes scientific claims, UX/product behavior, and algorithm or measurement design
  - A draft needs review from multiple specialist lenses before it becomes an implementation-ready spec
  - A position, paradigm, or field-introduction manuscript needs novelty positioning, prior-art depth audit, or citation completeness review (load Checks 10-14 from references)
  - User asks to reconcile or tighten a research methodology into a deterministic, engineerable version
  - A recurring improvement cycle is needed for a scoring/tracking system, especially where updates must be logged over time and reviewed by multiple experts
applies_to:
  - Research methodology drafts
  - Academic manuscripts (position papers, paradigm proposals, field-introduction papers)
  - Product-science hybrid documents
  - Measurement / scoring / personalization specs
  - Cybersecurity risk and governance reviews
  - Multi-expert review workflows
---

# Scientific Methodology Review and Consolidation

## Purpose

Use this workflow when a draft needs two things at once:
1. a rigorous expert-lens review of scientific, operational, and UX risks
2. a rewritten methodology/spec that is tighter, bounded, and implementation-ready

This skill is for the *class* of work where the right answer is not just "review it" or "rewrite it," but to do both in sequence.

It also covers panel-driven workflows where the methodology is first broken into specialist lenses, then recombined through a council-style synthesis into a deterministic, implementation-ready spec.

## When to Use

Use this skill when:
- a methodology draft includes research claims that may be overextended
- a document spans scientific validity, human factors, and system behavior
- you need to separate stable rules from provisional research
- the output should be a clean report plus a revised spec
- multiple specialist lenses improve the quality of the review
- the user explicitly wants *independent* reviewers with isolated perspectives, then a consolidated rewrite
- a scoring, measurement, or personalization draft needs separate psychometrics / math / UX lenses before revision

## Workflow

### 1. Survey the existing skill landscape first
Before doing anything, check whether an existing skill already fits part of the job.

Typical overlaps:
- `agent-delegation-discipline` for deciding whether to spawn specialists
- `subagent-driven-development` for structured delegation and review order
- `writing-plans` for turning the refined draft into a plan-like spec
- `requesting-code-review` for verification discipline and red-flag scanning
- `sibling-agent-talent-gate-protocol` and `multi-agent-panel-blueprinting` when the methodology review is being executed as a talent-gated expert panel with PDF handoff

If a relevant skill exists, follow its guidance for the part it covers. This skill handles the *methodology review + consolidation* layer.

### 2. Define the class before the instance
State the work in one sentence before starting:
- "This is a multi-specialist methodology review and spec consolidation task."

For recurring improvement cycles, also state the cadence and artifact that will persist between runs (e.g. a running changelog or cumulative update log).

The class should describe the recurring pattern, not the specific document.

### 3. Gather source documents
Read the primary draft and any supporting references.

Look for:
- core claims
- unstable or speculative sections
- pseudocode or algorithmic details
- safety/governance gaps
- sections that need to be labeled provisional
- conflict of interest statements and funding sources
- ethical approvals (IRB/ethics committee) and consent procedures

### 4. Assign specialist lenses
Use specialist viewpoints to review the draft. Typical lenses:
- measurement / psychometrics
- occupational load / feasibility
- vocational or role-fit logic
- human factors / ergonomics
- systems dynamics / stability
- cybersecurity architecture / threat modeling
- governance / compliance / insurance
- *adaptive personalization / behavior change science* when the draft involves routines, scoring, health, or intervention design

For cybersecurity or security-adjacent work, keep three lanes separate:
- technical controls
- governance / policy / insurance
- measurement / calibration / scoring

For adaptive routine or scoring systems, keep these layers separate:
- **population default** rules
- **trait-based** personalization
- **state-based** adaptation
- **response-history** learning
- **experience / quest / goal** layers at different time scales
- **score vs confidence** as distinct outputs

Each lens should produce:
- key risks
- overclaims
- missing guards
- concrete revisions

#### Parallel Subagent Implementation (three-review pattern)

When the user requests "three reviews from three different perspectives/models" on a physics, engineering, or scientific artifact, use `delegate_task` with the `tasks` array to fire three leaf subagents in parallel. Each subagent:

1. Gets the **same source files** (exact paths in the context field)
2. Gets a **distinct analytical lens** — e.g., dynamical systems vs. causal inference vs. network topology
3. Produces an **independent written analysis** to a specified output path
4. Uses web_search for literature backing (not just internal knowledge)

This works for: coupling matrix audits, algorithm validation, equation verification, architecture reviews. The parallelism saves wall-clock time (3 reviews in ~7 min vs 21 min sequential). After all three return, synthesize into a consensus document that averages recommendations and flags disagreements.

**Key discipline:** Each subagent must be told the other perspectives exist (so they focus on their lens) but must NOT see each other's work (isolation). Only the orchestrator sees all three and synthesizes.

**Worked example:** The κ coupling matrix audit (2026-06-15) fired three physicists: Kuramoto/dynamical systems, statistical/causal inference, and information theory/network topology. All three independently found Spiritual/DMN underweighting and the three-conflicting-matrices problem. See `physics-informed-engine-development` skill `references/coupling-matrix-audit-findings.md`.

### 5. Synthesize findings into a structured report
Write a report with:
- executive summary
- findings by specialist lens
- top fixes sorted by severity
- final verdict

Keep it evidence-based and avoid vague praise.

### 6. Rebuild the methodology into a tighter spec
Create a revised version that:
- preserves the core idea
- removes or quarantines unsupported claims
- defines the deterministic or bounded parts explicitly
- distinguishes stable rules from provisional research
- adds safety, governance, and validation gates
- uses the current best science for adaptive personalization: start with mass-market defaults, then narrow from trait → context → state → response history
- treats sleep as the day boundary when biologically appropriate, with flexible anchor-sleep handling for shift workers
- defines experiences, quests, and goals as separate levels of aggregation rather than one generic action bucket
- uses confidence to represent certainty/coverage/corroboration, not simple progress points

### 7. Verify the rewrite
Confirm the rewritten spec has:
- clear scope and non-goals
- explicit data model or inputs if relevant
- bounded personalization or adaptation rules if relevant
- auditability / reproducibility language
- provisional labeling for weakly supported ideas
- no hidden hand-wavy logic

### 8. Add a support file when the evidence is useful beyond one session
If the review surfaces durable research guidance, put a concise summary in `references/` and link it from the umbrella skill instead of bloating the main SKILL.md. Keep the reference short, actionable, and oriented toward repeatable review work.
## Output Pattern

Preferred deliverables:
- one review report file
- one rewritten methodology/spec file
- a short summary of the most important changes
- if this is a recurring cycle, a timestamped running update section that captures what changed this run, cumulative update count, and open questions for the next run

## ML/AI Claim Validation (Quality Gate with Veto Power)

When auditing ML/AI research or product claims, run these checks in order. Any fatal finding warrants a VETO on external publication until corrected.

### Check 1: Circularity in synthetic benchmarking

The most dangerous flaw: a physics-informed or domain-informed model tested against synthetic data generated by the SAME physics/domain model it encodes. This guarantees the informed model "wins" because it already knows the generating process.

**Detection method:**
1. Read the data generator code (e.g., `synthetic_data.py`)
2. Read the model code (e.g., `neural_ode_8d.py`)
3. Compare: Are the coupling matrices identical? Are the ODE terms the same? Are the same formulas generating the test data that the model hardcodes?
4. If yes → the comparison is circular. The "improvement" is an artifact.

**Remediation:** Validate on data from a DIFFERENT generative process, or on real data. Until then, all improvement claims are blocked.

### Check 2: Cherry-picked metric reporting

When a performance range (e.g., "4-12x improvement") is reported, verify ALL metrics, not just the best ones.

**Detection method:**
1. Open `results/metrics.json` (or equivalent)
2. Compute the ratio for EVERY metric: next-day MSE, extrapolation MSE, per-dimension breakdown
3. Identify which metrics were cherry-picked to construct the headline range
4. Report the full picture including metrics where the baseline WINS

**Worked example:** A prototype claims "4-12x improvement." Actual data shows: next-day MSE improvement = 1.06x (6%), extrapolation MSE = 4.24x, final-day extrapolation = 12x. The headline picks only the two extrapolation metrics and omits the 6% primary result. Additionally, the unconstrained baseline WINS on 4 of 8 dimensions. All of this was stripped from downstream documents.

### Check 3: Marketing-vs-code cross-referencing

External documents (marketing briefs, investor decks, product theses) often reference sophisticated techniques that don't exist in the codebase.

**Detection method:**
1. List every specific technical claim (named equations, algorithms, frameworks)
2. For each: search the codebase and architecture docs for implementation evidence
3. Build a matrix: claimed technique × present in code (Y/N) × present in architecture docs (Y/N)
4. Flag any technique claimed externally but absent from code

**Common pattern:** Marketing says "Langevin SDEs, Landau-Ginzburg phase transitions, Kramers escape rates" but the code has none of these. The talent request to BUILD them confirms they are future work, not existing capabilities.

### Check 4: HARKing (Hypothesizing After Results are Known)

Retroactive labeling of existing work with a fashionable framework. Example: "The architecture already was PIML, we just didn't call it that" — when no physics-informed loss function existed before the label was applied.

**Detection:** Check commit history, file creation dates, and talent requests. If the framework was "discovered" after the fact, the historical claim is HARKing.

### Check 5: Falsifiability assessment (Popperian core)

For each scientific claim, ask: what specific observation would refute this?
- "Resonance" without an equation of motion → unfalsifiable
- "Frequency" without oscillation → unfalsifiable
- "4-12x improvement" on circular data → unfalsifiable (tested against itself)
- "Phase coherence" without defined phases → unfalsifiable

Claims that cannot be falsified are conjecture, not science. They must be formalized (write the equations) or relabeled (use honest terminology) before external publication.

### Check 6: Structural consistency of LLM-generated scores

When a scoring pipeline uses an LLM to generate preliminary scores and a deterministic engine to rescore, the LLM's preliminary output must be internally consistent with its own component values. A preliminary TWC that is lower than what its own base dimensions compute to (weighted sum × stacked modifier) is structurally incoherent — the LLM is reporting a number that contradicts its own inputs.

**Detection method:**
1. Take the preliminary score's base 8D dimensions
2. Compute the structural floor: `Σ(w_i × D_i) × 10 × sqrt(modifier_1 × modifier_2)`
3. Compare to the reported preliminary TWC
4. If `preliminary_TWC < structural_floor`, the delta between the two is NOT wellness change — it's correction of LLM inconsistency

**Worked example (2026-06-13 audit):** A preliminary TWC of 41.5 was reported with base dimensions that compute to 55.43 — a 14-point structural inconsistency. The rescore "improved" it to 59.1 (delta +17.6), but 79% of that "improvement" was absorbing the LLM's own inconsistency, not actual wellness change. This makes the primary success metric (% of users showing improvement) uninterpretable because the system cannot distinguish real change from scoring inconsistency correction.

**Remediation:** Either (a) fix the LLM prompt to produce structurally consistent preliminary scores, or (b) report deltas measured from the structural floor, not the LLM-reported preliminary. Both must be done before any user-facing metric is valid.

### Check 7: Monotonicity bias in scoring systems

A scoring system with a hardcoded invariant (e.g., "positive evidence must never produce a lower score") has a built-in positivity bias. While this may have clinical justification (avoid demoralizing users), it means the system is structurally incapable of detecting certain legitimate patterns — e.g., a user eating well while declining across other dimensions.

**Why it matters methodologically:** This is the scoring equivalent of a one-tailed test that can never reject in the "wrong" direction. Under Popperian falsifiability, a measurement instrument that cannot produce certain legitimate findings is not a valid measurement instrument. It confounds any longitudinal analysis.

**Detection:** Search the scoring engine for assertion guards, clamp rules, or invariant checks that force monotonic increase. If present, flag that the system has a positivity bias that must be disclosed in any analysis using these scores.

**Remediation:** If the monotonicity rule is clinically necessary, it must be disclosed in any research or metric derived from these scores. The system should track what the "unconstrained" score would have been alongside the "clinically adjusted" score.

### Check 8: Bounded-output ≠ safe-output conflation

In health/wellness systems, a common error is claiming that because the numerical scoring engine bounds outputs to physically plausible ranges (e.g., [0, 100]), the entire system "cannot hallucinate" or "cannot produce dangerous advice." This conflates bounded scalar output with safe free-text generation.

**Detection:** Check whether any marketing or product claim uses language like "literally cannot hallucinate," "cannot produce impossible results," or "mathematically constrained." If the system uses LLM backends for coaching/advice text, these claims are false — physics constraints on scalar scores do NOT constrain LLM text output.

**Remediation:** Replace with: "Our scoring engine constrains numerical outputs to physically plausible ranges [0, 100]. Text output is generated by LLMs and requires its own safety review." Never claim that numerical boundedness implies output safety.

### Check 9: Marketing gate bypass — packaging unresolved flaws as selling points

The most dangerous organizational pattern: while methodology flaws persist unfixed (0% fix rate across cycles), the organism produces external-facing materials (investor decks, one-pagers, social media calendars, branding briefs) that package those exact flaws as features. The quality gate traditionally covers manuscripts and code — marketing materials bypass it entirely unless explicitly scanned.

**Detection method:**
1. Scan workspace for new external-facing documents since last cycle: `find ... -name "*one-pager*" -o -name "*positioning*" -o -name "*social-media*" -o -name "*marketing*" -o -name "*brief*" -o -name "*investor*"`
2. For each factual claim (performance, capability, technique-naming, precision, IP), map it to the applicable Check (1-8) or active VETO trigger
3. Build a violation catalog: `document_line × claim_text × violated_check × evidence_from_audit`
4. Flag any document containing claims blocked by an active VETO trigger
5. Check for explicit "no hedging" voice instructions — these compound every other violation by removing scientific uncertainty language from unvalidated claims

**Common pattern:** An investor ONE-PAGER claims "4-12x improvement" (Check 2: cherry-picked from circular data), "cannot suggest impossible outcomes because physics will not let it" (Check 8: bounded ≠ safe), "coupling matrices that map exactly how dimensions influence each other" (Finding 8: dead code + placeholder values), and "Langevin stochastic equations" (Check 3: absent from code). Every claim traces to an unresolved finding in the audit register.

**Regulatory risk:** "Cannot suggest impossible outcomes" or "cannot hallucinate" claims in health/wellness materials imply clinical reliability and could trigger FDA device classification. This directly contradicts established wellness-coaching regulatory posture.

**Remediation:** All marketing materials containing claims blocked by active VETO triggers must be held until either (a) the underlying finding is resolved, (b) the claim is removed, or (c) the claim is explicitly hedged with documented limitations. A categorical VETO on the entire document set may be issued when multiple claims violate multiple triggers.

### Check 15: Degenerate control + baseline omission (graph perturbation experiments)

When a perturbation experiment compares a biologically organized (or domain-informed) graph against a "randomized" control, the randomization method may structurally cripple the control under the experiment's own functional rule. This makes the reported advantage partly or entirely tautological.

**Detection method:**
1. Read the functional rule (e.g., "component survives only if all transitive dependencies survive").
2. Read the control construction (e.g., "edge-count-matched random rewiring of directed dependencies").
3. Ask: does the rewiring create spurious cycles, inflate path lengths, or generate long dependency chains that the functional rule would mechanically punish?
4. Check whether the 0% removal baseline (no components removed, both conditions at rest) is reported. If not, the reader cannot distinguish "the treatment graph is robust" from "the control graph is already structurally degraded by the rewiring itself."
5. Look for a gap amplification signal: if the treatment-vs-control gap at minimal perturbation (e.g., 10% removal) is already very large (e.g., 3:1 or greater), the control is likely degenerate.

**Worked example (2026-07-10 arXiv manuscript review):** A biologically organized dependency graph retained 0.623 functional capacity at 10% removal vs 0.180 for the edge-count-matched random control. The 3.5x gap at near-zero perturbation suggested the random control's baseline capacity was already degraded by rewiring artifacts (random directed edges create dependency cycles making most components non-functional even without removal). The paper acknowledged the functional rule favors shallower dependencies but did not report the 0% baseline, leaving the reader unable to quantify how much of the advantage was control degeneracy vs genuine resilience. Flagged as must-fix: report 0% removal baseline or explicitly acknowledge control degeneracy.

**Remediation:** Either (a) report functional capacity at 0% removal for both conditions, (b) use a degree-sequence-preserving or configuration-model control instead of raw edge rewiring, or (c) state explicitly that the random control's baseline is already degraded and the advantage partly reflects that.

### Check 16: Reproducibility-statement vs included-code mismatch

When a paper's Data and Code statement says results and scripts are "included with the source package," verify that the included scripts actually run from the package alone. A common pattern: the included script both runs the simulation AND generates figures, importing a proprietary or unavailable module. Running it as distributed fails.

**Detection method:**
1. Open every included script.
2. Check imports: does any import from a path or module not in the package?
3. Check environment variable dependencies (`os.environ.get(...)`, hardcoded paths).
4. Attempt to trace: if you ran this script fresh, would it succeed?
5. Compare the statement's claim ("included") against what actually runs.

**Remediation:** Clarify the statement: "The simulation requires module X, not distributed; only the aggregate JSON and figure PDF are directly usable from the package alone."

### Check 17: Proxy-score denominator transparency

When a composite proxy score reports values like 1.0000 or 0.5000 to four decimal places, check whether these are exact fractions (e.g., N/N components registered) presented as measured continuous values. Without numerator/denominator disclosure, a reader cannot assess what the proxy actually measures or whether it is meaningful.

**Detection method:**
1. Look for suspiciously round values at high precision (1.0000, 0.5000, 0.3333).
2. Check whether the paper states the basis (e.g., "97 of 97 components registered" or "23 of 46 roles matched").
3. If basis is absent, flag as a transparency gap.

**Remediation:** Add one sentence with numerator/denominator for each proxy component.

### Check 18: Construct overlap between scoring dimensions and outcome measures

When a composite score has a dimension that measures properties of the same artifact used as the outcome in a separate experiment, the score and outcome are not independent. Example: a C_r proxy measuring dependency-reference integrity of a registry, and a perturbation experiment testing resilience of the dependency graph derived from that same registry. A clean registry (high C_r) likely correlates with a clean topology (high resilience under the transitive rule).

**Detection method:**
1. List each scoring dimension and what artifact/data it draws from.
2. List the outcome measure and what artifact/data it draws from.
3. Identify overlap: same graph? same registry? same metadata?
4. Flag if a dimension and the outcome share a data source.

**Remediation:** Acknowledge the overlap explicitly. Note that high scores may reflect properties of the shared artifact rather than the construct the score claims to measure.

### Veto workflow

When a fatal finding is identified:
1. State the finding with evidence (quote the code, cite the metrics file)
2. List all downstream documents containing the problematic claim
3. Define remediation gates (what must be true before the veto lifts)
4. Check downstream agent status (search, causal, synthesis, writing) — are they aware of the problem?
5. Report to research director with veto decision and gate conditions

See `references/ml-claim-validation-patterns.md` for the PIML audit as a full worked example with detection recipes (Checks 1-5).

See `references/scoring-system-integrity-checks.md` for detection recipes for Checks 6-8 (structural consistency, monotonicity bias, bounded ≠ safe) with worked examples from the the specialist engine scoring pipeline audit.

See `references/marketing-claim-violation-detection.md` for detection recipes for Check 9 (marketing gate bypass) — violation catalog technique, regulatory risk assessment, and worked example from the the specialist engine marketing sprint audit (2026-06-13).

See `references/recurring-cycle-audit-methodology.md` for the cycle-over-cycle quality gate methodology — finding tracking, diagnostic query bank, escalation framework, and integrity scoring rubric for recurring methodology audit cron jobs (e.g., the specialist engine `bb2fc380f91d`).

See `references/physics-metaphor-abuse-and-evidence-language.md` for the physics-metaphor-abuse detection checklist (Check 5 extension), the evidence-level language discipline rules (VERITAS Stage 0), the parallel adversarial dispatch pattern (VERITAS Stage 2), and the post-review remediation protocol with the forced-concession salvage technique.

See `references/academic-novelty-positioning-and-prior-art.md` for academic novelty positioning checks (Checks 10-14): closest-prior-art depth audit, empirical-result novelty assessment, citation completeness audit, field-introduction vs position-paper calibration, trademark/commercial-use search, and the "known result" trap in case studies. Use these for ANY position, paradigm, or field-introduction manuscript review, not just ones with physics metaphor issues.

See `references/graph-perturbation-experiment-audit-patterns.md` for detection recipes for Checks 15-18 (degenerate controls, reproducibility-statement mismatches, proxy-denominator transparency, construct overlap) with the full worked example from the Physiomorphic AI arXiv manuscript review (2026-07-10).

## Formal Statistical Audit

When auditing ML/AI or scoring claims, run this audit table. Each item must be assessed independently:

| Item | What to Check | Block Publication If |
|------|---------------|---------------------|
| Effect size definition | What metric is improved? Is it clearly defined? | Vague ("improvement") with no metric |
| Confidence intervals | Are CIs reported? What is the range? | Single point estimate with no uncertainty |
| Power analysis | Is the sample size justified? | Claims from N=1 data generalized to population |
| Multiple comparison correction | Are corrections applied? (8 dims × 28 pairs = 36+ tests) | Multiple comparisons without Bonferroni/FDR correction |
| Pre-registration | Was the analysis plan registered before data collection? | HARKing — framework applied retroactively |
| Reproducibility | Can the result be reproduced with code + data + seed? | No training script, no saved results, no seed |

## Checklist Compliance Assessment

For health/wellness AI systems, assess compliance against the appropriate reporting checklist:

| Checklist | When Applicable | Key Requirements |
|-----------|----------------|-----------------|
| TRIPOD | System makes predictions (breakthrough probability, regime classification, trajectory) | Model development protocol, predictor definitions, missing data handling, performance metrics (C-statistic, calibration, DCA), internal/external validation |
| STROBE | Observational study of user data | Study design, participant selection, variables, bias, statistical methods |
| CONSORT | Any controlled evaluation | Randomization, blinding, outcome assessment, ITT analysis |
| PRISMA | Systematic reviews and meta-analyses | Title, abstract, introduction (rationale, objectives), methods (protocol, eligibility, information sources, search, selection, data collection, data items, risk of bias, effect measures, synthesis methods, reporting bias assessment), results (study selection, study characteristics, risk of bias, results of individual studies, syntheses, reporting biases, certainty assessment), discussion, funding |
| FAIR | Data management | Findable, Accessible, Interoperable, Reusable. Check metadata standards, data export format (FHIR), reuse license |

Non-compliance with the applicable checklist is a publication blocker until the gap is documented and a remediation plan exists.

## Good Review Questions

Ask:
- Which claims are validated vs speculative?
- What would fail in production if unbounded?
- What needs a safety floor or explicit cap?
- What needs a reason code, audit trail, or confidence flag?
- What should be labeled provisional instead of deleted?
- What must be deterministic to be engineerable?
- Which dimensions are truly independent vs just convenient labels?
- Whether the model should stay fixed or expand with the problem domain?
- Is the benchmark data generated by the same model being tested? (circularity)
- Are ALL metrics reported, or only the best ones? (cherry-picking)
- Does the marketing doc reference equations that exist in the code? (inflation)
## Common Pitfalls

- treating speculative research as production-ready
- leaving pseudocode bugs unaddressed
- mixing stable rules and experimental modules in one layer
- omitting governance or alerting rules
- writing a polished rewrite that still hides uncertainty
- skipping the lens-based review and jumping straight to prose cleanup

## Relationship to Other Skills

- `agent-delegation-discipline`: use it to decide whether to spawn a specialist at all
- `subagent-driven-development`: use it when the rewritten spec will be executed task-by-task
- `writing-plans`: use it if the methodology needs to become a sequenced implementation plan
- `requesting-code-review`: use it if the rewrite includes code or should undergo verification discipline

## Success Criteria

- the review names the highest-risk scientific and operational gaps
- the rewrite is tighter and more implementable
- unsupported claims are labeled or removed
- stable rules and provisional research are separated
- the final artifact is useful to both reviewers and implementers
