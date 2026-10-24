# Scoring System Integrity Checks — Detection Recipes with Worked Examples

Reference for Checks 6-8 of the ML/AI Claim Validation quality gate in the parent SKILL.md.
Captures reusable detection patterns from the the specialist engine scoring pipeline audit (2026-06-13).

---

## Detection Recipe 5: Structural Consistency of LLM-Generated Preliminary Scores

### The Pattern

When a scoring pipeline has two stages — (1) an LLM generates a preliminary score from
evidence, (2) a deterministic engine rescores when new evidence arrives — the LLM's
preliminary output may be internally inconsistent with its own component values. This
inconsistency masquerades as "improvement" in the rescore delta.

### How to Detect

1. Extract the preliminary score's component values (base dimensions, modifiers)
2. Compute the structural floor using the documented formula:
   ```
   structural_floor = Σ(w_i × D_i) × 10 × sqrt(modifier_1 × modifier_2)
   ```
3. Compare `preliminary_TWC_reported` vs `structural_floor`
4. If `preliminary_TWC_reported < structural_floor`, the inconsistency gap is:
   ```
   inconsistency_gap = structural_floor - preliminary_TWC_reported
   ```
5. The fraction of the rescore delta that is inconsistency correction:
   ```
   correction_fraction = inconsistency_gap / (final_TWC - preliminary_TWC_reported)
   ```

### Worked Example: the specialist engine Audit (2026-06-13)

**May 29 v1 rescore:**
- Preliminary TWC reported: 41.5
- Base dimensions weighted sum: psy=7.0×0.18 + phy=5.0×0.16 + env=5.0×0.11 + soc=5.5×0.12 + spi=5.0×0.10 + int=5.0×0.13 + voc=6.5×0.11 + fin=5.0×0.09 = 5.543
- Weighted sum × 10 = 55.43
- Stacked modifier: sqrt(0.985 × 1.0) = 0.992
- Structural floor: 55.43 × 0.992 = 54.99
- **Inconsistency gap: 54.99 - 41.5 = 13.49 points**
- Rescore delta: 59.1 - 41.5 = +17.6
- **Correction fraction: 13.49 / 17.6 = 77%**

The "improvement" was 77% correction of LLM inconsistency.

**May 29 v2 rescore:**
- Preliminary TWC: 56.0, structural floor: ~71.1
- Inconsistency gap: ~15.1 points
- Rescore delta: +16.5
- **Correction fraction: 91%**

### Why This Matters

The product thesis defines the primary success metric as "% of active users who report
measurable improvement in their coached area within 30 days." If the scoring system
cannot distinguish real wellness change from scoring inconsistency correction, this
metric is uninterpretable. Every rescore delta must be decomposed into:
- `real_change` (legitimate lift from evidence)
- `correction_change` (absorption of LLM inconsistency)
- `bonus_change` (integration bonus / follow-through credit)

### The Rescore Engine Already Knows

The production code (`rescore_engine.py` line 666) already handles this silently:
```python
structural_prelim_floor = max(prelim_twc_reported, prelim_pre_integration)
```
It uses the floor to avoid false plausibility-guard alerts, but the reported delta
is measured from the LLM's inconsistent preliminary, not the structural floor.

### Remediation

1. Fix the LLM prompt to produce structurally consistent preliminary scores
2. Report deltas measured from the structural floor
3. Add a `correction_fraction` field to the rescore output so consumers can distinguish
4. If `correction_fraction > 50%`, flag the day as "inconsistent preliminary — delta not interpretable"

---

## Detection Recipe 6: Monotonicity Bias in Scoring Systems

### The Pattern

A scoring system with a hardcoded invariant that forces scores to never decrease
when positive evidence is present. While this may have clinical justification
(avoid demoralizing users), it means the system is structurally incapable of
detecting certain legitimate wellness patterns.

### How to Detect

1. Search the scoring engine code for:
   - Assertion guards: `assert final >= preliminary`
   - Clamp rules: `max(preliminary, ...)`
   - Invariant checks that throw on decrease
2. For each found rule, ask: "What legitimate pattern does this rule prevent detection of?"
3. Flag the rule as a positivity bias source

### Worked Example: the specialist engine Engine (2026-06-13)

The rescore engine (`rescore_engine.py` lines 682-689) has a hardcoded invariant:
```python
has_positive_evidence = any(l > 0 for l in base_lifts.values()) or followthrough_credit > 0
if has_positive_evidence and final_twc < prelim_twc_reported:
    raise AssertionError("INVARIANT VIOLATED: positive evidence produced lower TWC")
```

**What this prevents detecting:**
- User eats well (nutrition evidence → PHY lifts) while simultaneously crashing on
  Emotional and Financial dimensions
- User exercises (physical evidence) while sleep deteriorates and stress spikes
- Any pattern where one dimension improves while the aggregate should decline

**Popperian critique:** A measurement instrument that cannot produce certain legitimate
findings is not a valid measurement instrument. It has a built-in positivity bias that
confounds any longitudinal analysis. Under conjecture-and-refutation, this is analogous
to a one-tailed hypothesis test that structurally cannot reject in the negative direction.

### Remediation

If the monotonicity rule is clinically necessary (user retention > measurement fidelity):
1. **Disclose** the bias in any research or metric derived from these scores
2. **Track the unconstrained score** alongside the clinically adjusted score
3. **Never use these scores in published research** without the bias caveat

---

## Detection Recipe 7: Bounded-Output ≠ Safe-Output Conflation

### The Pattern

A health/wellness system claims it "cannot hallucinate" or "cannot produce impossible
results" because its numerical scoring engine bounds outputs to a range (e.g., [0, 100]).
This conflates bounded scalar output with safe free-text generation.

### How to Detect

1. Search marketing materials for: "literally cannot," "mathematically prevented,"
   "physically impossible," "cannot hallucinate"
2. Check whether the claim refers to numerical scoring OR text/coaching output
3. If the system uses LLM backends for coaching text, any claim that the "system cannot
   hallucinate" is false — physics constraints on scores do NOT constrain LLM text

### Worked Example: the specialist engine Claim (2026-06-13)

PIML-MARKETING-BRANDING-BRIEF.md line 239:
> "Our AI literally cannot hallucinate bad health advice."

Line 32:
> "Our models are constrained by sigmoid response curves and stochastic dynamics.
> The math prevents impossible predictions by design."

**The category error:** The Neural ODE prototype (`neural_ode_8d.py`) has a
`boundedness_loss` that penalizes predictions outside [0, 100]. This constrains the
SCALAR score trajectory. The coaching engine uses LLM backends (ARCHITECTURE.md line 337)
to generate free-text coaching advice. The boundedness of the score does NOT constrain
the LLM's text output in any way.

**Regulatory risk:** This claim directly contradicts the regulatory posture
(REGULATORY-COUNSEL-BRIEF.md frames the product as "wellness coaching, not medical device").
A "cannot hallucinate" claim could trigger FDA scrutiny as implying clinical reliability.

### Remediation

Replace with: "Our scoring engine constrains numerical outputs to physically plausible
ranges [0, 100]. Text output is generated by LLMs and requires its own safety review."

---

### Recurring Detection Note (2026-06-13, 17:38 Cycle)

This pattern (bounded ≠ safe) was detected AGAIN in a new context during the 17:38 audit cycle. The claim appeared in `DIVINITY-SCIENCE-ONE-PAGER.md` line 32: "The model cannot suggest impossible outcomes because the physics will not let it." This is the same category error as the marketing brief, now packaged for investor consumption. The claim persists despite prior remediation guidance, confirming it is systemic — not a one-off drafting error but an organizational pattern of conflating numerical boundedness with output safety.

When this check fires repeatedly across different documents, escalate to a categorical VETO on ALL marketing materials until the voice guide is updated to prevent the pattern at the source. See Check 9 in the parent SKILL.md and `references/marketing-claim-violation-detection.md` for the full detection workflow.

---

## Cross-Cutting: N=1 Calibration → Universal Claims

### The Pattern

A scoring system calibrated on a single individual (founder, N=1) is presented as a
universal scoring system for all users. Coupling coefficients, dimension weights, lift
rules, and modifier bounds are all tuned to one person but deployed as if they represent
population parameters.

### How to Detect

1. Check file headers and comments for personal calibration language ("the principal's personal",
   "the principal's 8D weights", "from calibration.json")
2. Check whether any coupling/weight/parameter has a documented population source
   (literature citation, multi-user data fit, expert elicitation)
3. If parameters have N=1 provenance but are presented as universal → generalizability flaw

### Remediation

Label all N=1 parameters as "priors calibrated on initial data, pending population
validation." Do not claim proprietary IP status for N=1-derived coupling values without
documented derivation. Run calibration on diverse users before claiming universality.

---

## Key Files for the Scoring Pipeline Audit

- Rescore engine: `~/your-workspace/hydra-os/scripts/rescore-engine/rescore_engine.py`
- PIML prototype: `~/your-workspace/divinity-health/piml-prototype/neural_ode_8d.py`
- Real scoring outputs: `~/your-workspace/health-private/daily/rescore-result-*.json`
- Marketing claims: `~/your-workspace/ds-wave-cto-advisory-panel-private/PIML-MARKETING-BRANDING-BRIEF.md`
- Physics fidelity report (DS AXIOM): `~/your-workspace/ds-wave-cto-advisory-panel-private/PHYSICS_FIDELITY_REPORT.md`
