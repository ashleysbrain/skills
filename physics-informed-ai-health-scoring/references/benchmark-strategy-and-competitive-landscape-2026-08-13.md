# AI Health Benchmark — Strategy & Competitive Landscape

**Session:** 2026-08-13
**Source:** the specialist engine (competitive), the specialist engine (adversarial), the specialist engine (architecture), the specialist engine (physics), the specialist engine/Avrami (deep physics)
**Status:** Research complete, principal decisions pending

---

## The Opportunity (Verified Empty Space)

The intersection of **public + longitudinal + standardized + health-framed** AI monitoring is completely unclaimed. Every existing player occupies at most 2 of 4 quadrants:

| Player | Public? | Longitudinal? | Standardized? | Health-framed? |
|--------|---------|---------------|---------------|----------------|
| MMLU/Arena/HF | Yes | No (snapshot) | Yes | No (capability) |
| LangSmith/Arize/WhyLabs | No (private) | Yes | No (per-customer) | Partial |
| LiveBench/SEAL | Yes | No | Yes | No |
| **DS (proposed)** | **Yes** | **Yes** | **Yes** | **Yes** |

## Competitive Landscape Detail

### Public benchmarks (saturated on capability, empty on health)
- **Chatbot Arena (LMSYS):** crowdsourced Elo. Can't detect drift cleanly (Elo confounded by voter base shifts).
- **Artificial Analysis:** point-in-time comparisons. No longitudinal framing.
- **HuggingFace Leaderboards:** snapshot, severe contamination/gaming.
- **LiveBench/Scale SEAL:** contamination-resistant but still snapshots.

### Observability platforms (private, not standardized)
- **LangSmith, Arize Phoenix, Langfuse (OSS), Helicone:** per-customer, internal. No public/comparable health signal.
- **WhyLabs/whylogs:** drift detection heritage but built for tabular ML. LLM-specific is bolted on.
- **Datadog/New Relic:** "is it up" (latency/uptime), not "is it good" (quality/drift).

### Nobody does: public longitudinal drift tracking of frontier models

## The Architecture (Lyapunov Design)

**600-task frozen test suite** across 7 strata: factual recall (120), closed reasoning (120), code generation (100), format compliance (80), instruction following (80), long-context retrieval (50), refusal/safety calibration (50).

**4 parallel drift detectors:**
1. **CUSUM** for gradual drift (ARL-to-alert ~10 days for 1-sigma shift, ARL-false ~1000 days)
2. **Bayesian changepoint detection** (Adams-MacKay 2007) for silent provider swaps
3. **Embedding-space drift** via permutation test on cosine distance centroids
4. **Two-proportion z-test** with Bonferroni correction for format/structural regression

**Composite H score on [0,100]:** weighted across accuracy (0.30), stability (0.25), semantic (0.15), format (0.15), consistency (0.10), provenance (0.05). Use geometric mean or floor operator, NOT arithmetic mean.

**Infrastructure:** ~$5/day/endpoint, SQLite + self-hosted judge model, daily sweep + 4-hour high-sensitivity subset.

## The Three Things That Would Kill This (Popper)

1. **Judge model without kappa validation** — Cohen's kappa < 0.7 vs human raters = every score suspect. NON-NEGOTIABLE: must validate before launch.
2. **Arithmetic-mean composite** — masks safety regressions when other dimensions improve. Use geometric mean or min().
3. **Frozen test suite contamination** — public frozen suite WILL enter training data. Longitudinal tracking requires frozen; frozen gets contaminated. Must be first-class architectural concern.

## Physics Foundation (Shannon)

- **Unifying theory: Minimum Description Length (MDL).** Health = description-length efficiency. KL is excess description length. JS distance is bounded form.
- **JS DISTANCE (not divergence)** is the correct composite unit — it's a true metric (triangle inequality).
- **Hallucination decomposition:** H(Y) = I(Y;C) grounded + H(Y|C) unaccounted. Chain rule identity. Most original contribution.
- **Quantum framework is ~80% decorative.** Only entanglement entropy survived testing (as coupling-saturation diagnostic). The rest is quantum mysticism.

## principal Decisions Pending

1. **Naming:** "AI Health Score" (attackable, biology metaphor) vs "Behavioral Stability Score" (defensible) vs "Model Pulse" (viral brand)
2. **"First" claim:** "First longitudinal AI benchmark" is FALSE (HELM, Dynabench exist). "First PUBLIC LONGITUDINAL DRIFT-SPECIFIC benchmark" is TRUE.
3. **Biology metaphor:** Physics framing defensible ONLY if formulas derived from physics. Currently decorative in places.
4. **Credential deficit:** No DeepMind/Stanford/UCB pedigree. Path: radical transparency + NeurIPS D&B submission + 6-12 month track record.
5. **Open source split:** Dataset open + methodology open + judge closed? Or full reproducibility?
6. **Revenue:** Enterprise API ($150/mo/endpoint), certification/badge, premium analytics.
7. **Contamination strategy:** Private suite (best resistance, "trust us") vs procedural generation (resists memorization, adds variance) vs quarterly rotation (fresh, breaks comparability).
8. **Self-improvement:** How does benchmark adapt to new capabilities without losing longitudinal comparability? Sandbox environment needed.
