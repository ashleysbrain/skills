# Physics-Informed Scoring: Structural Isomorphisms Pattern

Reference pattern for building scoring pipelines where biological phenomena share **the same mathematical structure** as well-established physics equations. Not analogies — identical equations with renamed variables.

## Core Principle

An isomorphism means two systems share the same mathematical structure. The equations are identical; only the variable names change. If you remove the physics domain label, you cannot tell which system the equation describes.

When a user names a physics concept (antigravity, entropy, gravity, resonance), research whether a genuine structural isomorphism exists in the published literature. If yes, build the full treatment with citations. If no, say so honestly — do not force a metaphor.

## The Honesty Rule

When the user asks "does this really make sense or are you stretching it," tell the truth. Break down what's real, what's a legitimate isomorphism, and what's decorative. The user values intellectual honesty over validation of their ideas.

## Proven Sleep↔Physics Isomorphisms

All mappings below are backed by peer-reviewed sleep research where the physics equation was explicitly used to model the biological phenomenon.

### 1. Homeostatic Sleep Pressure (Process S) ↔ RC Circuit

**Biology:** Adenosine accumulates in basal forebrain during wake, clears during sleep.
**Math:** `dS/dt = (S_max − S) / τ_wake` [wake], `dS/dt = −S / τ_sleep` [sleep]
**Physics:** Capacitor charge/discharge: `dV/dt = (V_source − V) / RC`
**Time constants:** τ_wake ≈ 17.2 hr, τ_sleep ≈ 4.2 hr
**Source:** Borbély (1982) two-process model; Riedy et al. PLoS Comp Bio (2017) model adenosine with explicit first-order kinetics

### 2. Circadian Rhythm (Process C) ↔ Van der Pol Oscillator

**Biology:** SCN generates near-24hr oscillation in firing rate, hormones, temperature.
**Math:** `dx/dt = y + ε(x − 4/3·x³)`, `dy/dt = −(24/π)²·x + B(t)` where B(t) is light forcing
**Physics:** Nonlinear electrical oscillator — originally vacuum tube circuits (Van der Pol 1927). Same equation, same limit cycle dynamics.
**Source:** Kronauer (1990); Forger, Jewett & Kronauer (1999), Journal of Mathematical Biology

### 3. REM–NREM Cycling ↔ Lotka-Volterra

**Biology:** REM-on (FTG) and REM-off (LC) neurons reciprocally inhibit each other.
**Math:** `dR_on/dt = a·R_on − b·R_on·R_off`, `dR_off/dt = −c·R_off + d·R_on·R_off`
**Physics:** Population dynamics / predator-prey equations. Predicted time course matches actual single-unit recordings.
**Source:** McCarley & Hobson, *Science* 189:58–63 (1975)

### 4. Wake–Sleep Switching ↔ Double-Well Potential + Langevin Dynamics

**Biology:** Sleep/wake are bistable states; transitions occur when Process S + C cross thresholds.
**Math:** `F_switch = S(t) + C(t) − H` (sleep onset when crossing zero from below). Stochastic forcing: `dX/dt = F_switch(X) + σ·ξ(t)`
**Physics:** Particle in time-varying double-well potential (Duffing oscillator). Langevin dynamics for stochastic barrier crossings = same as Brownian motion with drift.
**Source:** Diekmann et al. Physica D (2022); Booth et al. (2017)

### 5. Thermoregulation ↔ Newton's Law of Cooling

**Biology:** Sleep onset requires core temperature decline via distal vasodilation (DPG gradient).
**Math:** `dT_core/dt = −k·(T_core − T_set)`
**Physics:** Classical thermodynamics — Newton's law of cooling. DPG > 2.5°C → SOL < 15 min.
**Source:** Kräuchi et al. Am J Physiol (1999); Sleep Medicine Reviews (2012)

### 6. Brief Awakenings ↔ Non-Homogeneous Poisson Process

**Biology:** Awakenings occur stochastically with stage-dependent rates.
**Math:** P(N events in interval) = (λt)^N · e^(−λt) / N! where λ varies by sleep stage
**Physics:** Radioactive decay detection, photon counting. Memoryless property holds.
**Source:** Lo et al. PNAS (2002) — continuous-time Markov model of sleep stages

### 7. Sleep Architecture Transitions ↔ Continuous-Time Markov Chain

**Biology:** Transitions between Wake, N1, N2, N3, REM follow probabilistic rates.
**Math:** 5×5 transition rate matrix Q; deeper stages have higher "activation barriers" to exit
**Physics:** Statistical mechanics / master equation
**Source:** Laumann et al. Nature Communications (2019) — Hidden Markov Models for whole-brain dynamics

### 8. Caffeine ↔ First-Order Elimination

**Biology:** Caffeine competitively blocks adenosine A₁ receptors, reducing Process S charging rate.
**Math:** `C(t) = C₀ · e^(−t/τ)` with τ ≈ 4.9 hr (population mean from 141 studies)
**Physics:** Radioactive decay / RC discharge / first-order chemical kinetics
**Source:** Zenk et al. Frontiers in Pharmacology (2021) — systematic review of 141 publications

### 9. Light-Melatonin Suppression ↔ Hill Equation

**Biology:** Blue light (446–477 nm) suppresses melatonin via melanopsin ipRGCs.
**Math:** `M_suppressed = M_max / (1 + (ED₅₀/I)ⁿ)` with n ≈ 0.5–1.0
**Physics:** Langmuir adsorption / oxygen-hemoglobin binding — cooperative binding sigmoidal dose-response
**Source:** Zeitzer et al. J Clin Endocrinol Metab (2000); Brainard et al. (2001)

## Disruptor Modeling Pattern

**Wrong approach:** Apply a single post-hoc multiplier to the composite score (e.g., `CSI_adjusted = CSI × (1 − AGI/200)`). This is arbitrary and unexplainable.

**Right approach:** Each disruptor modifies the specific sub-component it actually affects:
- Caffeine → reduces N3 penetration and increases SOL (via Process S receptor blockade)
- Blue light → phase-shifts CAS (via van der Pol oscillator forcing function B(t))
- Stress/Noise/Pain → increases FI (via Langevin noise amplitude σ)

This is more honest, more explainable, and produces better coaching output because the user learns *which aspect of their sleep* is affected, not just "your score was lowered."

## Coaching Integration

Each disruptor gets a component-level explanation:
- "Caffeine at 4 PM reduced your deep sleep by 14% (adenosine receptor blockade). Moving your last coffee to before 2 PM would help."
- "Evening screen time shifted your circadian phase by ~20 min (melatonin suppression via the Hill dose-response)."

Not: "Your antigravity was 58." Users need actionable, mechanism-specific language.

## Pipeline Position

```
Raw evidence → Evidence interpretation (extract signals)
            → Component scores (SAS, CAS, SES, FI) — each with physics-motivated math
            → Disruptor modifications at the component level (not the composite)
            → CSI composite (weighted sum of modified components)
            → 8D cascade propagation (coupling matrix)
            → Personal baseline delta
            → Final composite score
            → Presentation + mechanism-specific coaching
```

## Proven Behavioral↔Physics Isomorphisms (GAS v2.0)

These mappings extend the physics-informed scoring pattern beyond sleep into general goal-attainment scoring. They were validated against the GAS v2.0 engine and share the same math stack (Riemannian metric tensor g_ij, potential landscape V(x), Langevin SDE with T_eff).

### 10. Barrier Crossing ↔ Kramers Escape Rate

**Behavior:** A user stuck on a goal has to "break through" a behavioral barrier with sustained effort. The barrier height ΔV_i was already computed in the potential landscape.
**Math:** `k_escape,i = (ω₀,i · ω_b,i) / (2π · γ_i) · exp(−ΔVᵢ / T_eff)`
**Physics:** Kramers (1940) — mean first-passage time for noise-driven barrier crossing in overdamped systems.
**Why it's not metaphor:** The Langevin SDE in the scoring engine IS the dynamical system Kramers analyzed. Same potential V(x), same noise σ(x) defining T_eff, same friction γ_i. The escape rate is a theorem about the existing system, not a new system imported by analogy.
**Output:** τ_escape (days), P_escape(Δt) (probability of breakthrough in forecast window).
**ADHD connection:** Higher T_eff (more behavioral noise) increases k_escape exponentially — models the real phenomenon where ADHD chaos occasionally breaks through stuck states.

### 11. Regime Shifts ↔ Landau-Ginzburg Phase Transitions

**Behavior:** Users don't gradually slide from Stable to Crisis. They hit a threshold and flip. This is a phase transition.
**Math:** `F(ψ) = a(T_eff) · ψ² + b · ψ⁴` where ψ is the order parameter (behavioral coherence), a(T_eff) = a₀(T_eff − T_c).
**Physics:** Landau (1937), Ginzburg-Landau (1950) — standard theory for continuous phase transitions in statistical mechanics.
**Why it's not metaphor:** The effective temperature T_eff comes from the Langevin SDE (same variable). The order parameter ψ is computed from geodesic progress φᵢ and velocity vectors ẋⁱ (both already in the pipeline). The susceptibility χ = 1/(2a + 12bψ²) quantifies intervention leverage as a theorem, not an analogy.
**Output:** Regime classification, susceptibility χ (intervention leverage), transition probability P_transition(Δt), critical slowing down as early warning.
**Key insight:** Near the critical point (a → 0), χ diverges — small interventions have outsized effects. This explains WHY Ricci curvature flags leverage points.

## Source

Divinity Health Sleep App (2026-06-07). Algorithm v2.0.0 — structural isomorphisms replaced the v1.1.0 antigravity metaphor after user correction: "I don't want the metaphor I want to map math behind sleep physics to other physics if possible so we have a blueprint or foundation to start with for scoring and helping users sleep better."
