# the specialist engine Registry — Condensed Reference

**Canonical source:** `/<workspace>` (488 lines)
**Ecosystem blueprint:** `/<workspace>` (532 lines)
**GAS v2.0 source:** `/<workspace>` (915 lines)
**8D Sleep Algorithm:** `/<workspace>` (856 lines)
**Lab manifest:** `/<workspace>`
**Rescore engine:** `/<workspace>` (1,072 lines)

## Overview
DS has 29+ algorithms spanning 9 mathematical domains. The ecosystem is a full behavioral physics research lab, not just a health scoring app. When preparing advisor reviews, scientific briefs, or technical documents, present the FULL ecosystem.

## Production (LIVE) Algorithms

| Algorithm | Lines | Domain | Key Math |
|-----------|-------|--------|----------|
| **GAS v2.0** | 915 | Riemannian geometry | Metric tensor `g(x) = I + κ·diag(α(x))·κᵀ`, geodesic distance, Ricci curvature, Wasserstein optimal transport, Kramers escape rates, Landau-Ginzburg phase transitions, Langevin SDEs on manifolds |
| **8D360 Scoring Engine** | 2,214 | Composite scoring | TWC weighted geometric mean, EWMA, cascade detection, hypomania flags, stock-and-flow dynamics |
| **8D Sleep Score** | 856 | Circadian dynamics | Van der Pol oscillators, Lotka-Volterra REM cycling, Markov sleep architecture, KL divergence, κ coupling matrix (8×8 symmetric) |
| **Rescore Engine** | 1,072 | Deterministic safety net | Full audit trail, atomic dimension+TWC writes |
| **Score from Evidence** | 901 | Evidence→score | Single entry point for all scoring |
| **Activity Scoring** | 269 | Activity ontology | Master activity scoring by health impact |
| **ASTRION** | 554 | Network theory | Partial Python implementation, spec incomplete |
| **Nutrition Engine** | 439 | Nutrition science | 7 sub-scores (protein, timing, frequency, glycemic, hydration, gut, med-food) → PHY/PSY/INT/VOC modifier |
| **Sexual Health Engine** | 309 | Sexual health | 6 sub-scores, ENM/CNM fairness adjustment |
| **Kink/BDSM Engine** | 402 | Kink analytics | 5 sub-scores, KAE curves, biomechanics, consent ethics |
| **ADHD EF COMPASS** | — | Neuropsychology | Sigmoid fusion, 7 behavioral domains |

## Specification-Only (NOT Implemented)

| Algorithm | Domain | Key Math |
|-----------|--------|----------|
| **EPHEMERIS** | Dynamical systems | 7 coupled nonlinear ODEs, bifurcation analysis, Lyapunov stability, Takens embedding, Kuramoto synchronization |
| **AETHER** | Neurophysics | Neural metabolic budget, PFC glucose/oxygen, Vyvanse pharmacokinetics |
| **CORONIS** | Markov processes | 8-state Markov chain, IRT latent composite, spectral decomposition |
| **ECLIPSION** | Chaos theory | Lyapunov exponents, Kaplan-Yorke fractal dimension, strange attractor reconstruction |
| **MAGNETRA** | Bayesian inference | 3-level hierarchical, Gaussian network priors |
| **NOVION** | Psychometrics | 2PL IRT model, test information function, MML calibration |
| **CONSTELLA** | Information theory | Shannon entropy, transfer entropy, Kolmogorov-Sinai entropy, rate-distortion theory |
| **UMBRAE** | Signal detection | d-prime, ROC curves, neural field theory |

## Master Framework
**Behavioral Physics Engine** — 8 layers (observation, latent state, history, geometry, distribution, dynamics, regime, policy). Only L1-L2 partially implemented. L3-L8 zero implementation.

## Implementation Gap Summary
- 8 algorithms SPEC-only (EPHEMERIS, AETHER, CORONIS, ECLIPSION, MAGNETRA, NOVION, CONSTELLA, UMBRAE)
- BP Engine L3-L8: zero implementation
- ASTRION: spec incomplete
- GAS v2.0: some equations not in production code
- Production scoring has 6 legacy scripts computing TWC independently (unification Phase 2 not complete)

## Key Equations (Quick Reference)
- **TWC:** `exp(Σ(wᵢ · ln(sᵢ)) / Σ(wᵢ))` with deficit penalty, PCM, momentum
- **Nonlinear map:** `100 · (1 - exp(-K·(x-1)/9)) / (1 - exp(-K))` where K=2.5
- **8D weights:** PSY .18, PHY .16, ENV .08, SOC .12, SPI .12, INT .10, VOC .14, FIN .10
- **κ coupling (strongest):** PSY↔PHY 0.82, cascade damping 0.30
- **Metric tensor:** `g(x) = I + κ·diag(α(x))·κᵀ`
- **Langevin SDE:** `dxⁱ = -gⁱʲ∂ⱼV dt + σⁱdWₜⁱ`
- **Kramers rate:** `k_escape = (ω₀·ω_b)/(2πγ)·exp(-ΔV/T_eff)`
- **Landau-Ginzburg:** `F(ψ) = a(T_eff)ψ² + bψ⁴`
- **Score-to-modifier:** `mod = clamp(lo, hi, center + range · ((composite/100) - 0.50))`

## PIML Prototype Results (Divinity Health)
- Location: `/<workspace>`
- 30-day extrapolation: Physics MSE 19 vs Unconstrained 82 (4× improvement)
- Final day: 15.89 vs 191.78 (12× improvement)
- Physics model wins PSY/PHY/ENV/FIN; baseline wins SOC/SPI/INT/VOC
- Advisor review: `ADVISOR-REVIEW.md` (being updated for Dr. Richard Anantua with full ecosystem)

## External Advisor
- **Dr. Richard Anantua** — Theoretical Astrophysicist, Rice University / UTSA
- Reviewing the full algorithm ecosystem for formalization guidance
- Build deliverables FOR him to review, not asking him to build from scratch

## File Locations (Quick Map)
```
/<workspace>
├── your-org-labs/behavioral-physics/   # Algorithm Registry, Lab Manifest, research
│   ├── ALGORITHM-REGISTRY.md                   # Canonical algorithm index (488 lines)
│   ├── LAB-MANIFEST.md                         # Lab manifest
│   ├── research/SCIENCE-FEED.md               # Science feed
│   └── products/INTERFACE-SPEC.md             # Interface spec
├── divinity-health/
│   ├── piml-prototype/                        # Neural ODE prototype + advisor review
│   └── sleep-app/agents/                      # GAS v2.0, 8D Sleep Algorithm source
├── health-private/                            # Production scoring, engines, rescore data
│   ├── SCORING-ECOSYSTEM-BLUEPRINT.md         # Full scoring architecture (532 lines)
│   ├── score_from_evidence.py                 # Single entry point (901 lines)
│   ├── rescore_engine.py                      # Deterministic rescore (1,072 lines)
│   ├── build_unified_db.py                    # Unified DB builder (684 lines)
│   ├── daily_scorecard_report.py              # Daily report (519 lines)
│   └── activity_scoring.py                    # Activity scoring (269 lines)
└── hydra-os/
    └── products/principal-8d-tracker/            # Unified pipeline, input adapters
```
