# Native AI Dimensions and PIML Results (2026-07-06)

Session-specific knowledge for two topics that came up during the organism
review and 8D redesign: (1) why the human-mapped dimensions feel wrong for AI
and what native replacements exist, and (2) the real PIML prototype numbers
versus the inflated marketing claim.

---

## Why the human dimensions are wrong for 8D360AI

The current 8D360AI dimensions borrow human wellness categories and
force-map them to AI agents:

- Psychological -> reasoning quality (but "psychological" implies a human psyche)
- Physical -> infrastructure uptime (AI has no body)
- Environmental -> context hygiene (but the word suggests workspace lighting)
- Social -> collaboration (AI has handoffs and schemas, not relationships)
- Spiritual -> alignment/purpose (loaded word for what is really mission compliance)
- Intellectual -> knowledge currency (academic-sounding)
- Vocational -> task completion (HR-speak)
- Financial -> token costs (reductive)

The root issue: these describe what AI SHOULD BE (humans), not what AI
ACTUALLY IS (systems that fail in specific, measurable ways).

---

## Primary proposal: The 8 Resilience Pillars

Derived from real AI failure modes. Every dimension has clear telemetry,
measurable degradation, and cascade pathways.

1. **Cognitive Integrity** (hub, sigma = 0.68). Hallucination rate,
   contradiction density, context coherence. Couples strongest to Pipeline
   Reliability (0.76) and Knowledge Currency (0.72).

2. **Pipeline Reliability** (foundation). Tool success rate, API latency,
   stale reference rate, context waste accumulation. Couples to Cognitive
   (0.76) and Resource Efficiency (0.64).

3. **Resource Efficiency** (constraint). Tokens per task, model-tier routing,
   retry/abandon ratio, MED compliance. Couples to Pipeline (0.64) and
   Cognitive (0.59).

4. **Knowledge Currency** (learning). Source age distribution, knowledge
   refresh frequency, learning rate on new task types. Couples to Cognitive
   (0.72) and Adaptation Capacity (0.68).

5. **Interaction Coherence** (coordination, critical for multi-agent).
   Handoff rework rate, schema mismatch count, joint vs solo task success.
   Couples to Cognitive (0.68) and Aligned Execution (0.64).

6. **Adaptation Capacity** (resilience). Novel-input success rate, recovery
   time after failure, hormesis-cycle success. Couples to Knowledge (0.68)
   and System Volatility (0.71).

7. **Aligned Execution** (governance). Soul-directive compliance, boundary
   violations, identity drift detection. Couples to Interaction (0.64) and
   Cognitive (0.57).

8. **System Volatility** (canary, HRV analog). Rolling 7-day variance of
   dimension scores, OCI, Cascade Amplification Ratio. Couples to ALL.
   Key insight: zero volatility means the system is rigid and about to
   break, not healthy.

Three alternative naming sets use the same telemetry with different framing:
- Telemetry Pillars (dry engineering names for dashboards)
- Resilience Layers (OSI-model style for architecture teams)
- Signal Pillars (biohacking-inspired, tech-native, bridges the
  BIOHACKING-THE-AI-ORGANISM.md mapping)

Full design lives in the Andreasen panel output. Search
`/<workspace>` for the panel summaries from 2026-07-06.

---

## PIML prototype: real numbers vs marketing claim

**Marketing claim (DO NOT REPEAT without correction):** "4-12x improvement
over standard ML approaches" (from PIML-MARKETING-BRANDING-BRIEF.md, June
2026).

**Actual measured results** (`divinity-health/piml-prototype/results/metrics.json`):

| Metric | Physics-Informed | Unconstrained | Improvement |
|---|---|---|---|
| Total MSE | 10.94 | 11.64 | **6%** |
| Extrapolation MSE | 19.22 | 81.50 | **4.2x** |

The 4.2x is on extrapolation only (predicting future states outside the
training distribution). Overall accuracy improved 6%. The marketing claim
of "4-12x" inflated the extrapolation number into a blanket claim.

**Honest framing for pitches:** "4x better at predicting future health
states from limited data, because physics constraints replace the need for
massive datasets. This is why it works for health data, which is always
sparse."

The prototype code is real: `neural_ode_8d.py` implements a Physics-Informed
Neural ODE with the kappa coupling matrix baked in, compared against an
unconstrained baseline. The kappa matrix in the prototype matches the 8D
Sleep Algorithm Section 7.7 values (PSY-PHY strongest coupling at 0.82).

---

## Autonomous self-healing loop (8 stages)

Full architecture spec: `/<workspace>`

Sense -> Score -> Detect -> Diagnose -> Triage -> Intervene -> Validate -> Learn

Three physics principles make it work and form the moat:
- **Critical slowing down** (early warning: recovery time or variance
  trending up = near tipping point)
- **Free energy principle** (triage: F = cost - T*info_gain; if F > 0,
  skip the intervention)
- **Adiabatic invariance** (safe application: max 0.5 pts/hr change, 24h
  between same-dimension interventions)

The kappa coupling matrix LEARNS from every intervention outcome:
`kappa_new = kappa_old + alpha * (observed_ratio - kappa_old)`. That
learning loop is the moat. Competitors who copy the framework start with
static coefficients.
