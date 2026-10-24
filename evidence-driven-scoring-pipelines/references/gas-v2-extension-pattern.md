# GAS v2.0 Extension Pattern — Kramers + Landau-Ginzburg

Session reference for extending the Goal Attainment Scoring Algorithm from flat-space physics to spacetime geometry with barrier crossing and regime transition theory.

## What happened

User asked about incorporating theoretical physics principles into GAS v2.0. Agent initially proposed a menu of disconnected frameworks (quantum tunneling, string theory, Boltzmann distributions, Gibbs free energy). User corrected: "I need calculations that fit our needs. I don't want you to smash calculations together unless they make sense and align with human behavioral physics."

Agent then evaluated which frameworks genuinely share variables with the existing math stack. Only two passed all five checks:

1. **Kramers escape rate** — extends existing barrier diagnostics (ΔVᵢ) into breakthrough probabilities
2. **Landau-Ginzburg phase transitions** — replaces static regime labels with physics-derived classification

## The evaluation criteria (generalized)

For any proposed physics extension to an existing scoring engine:

1. **Variable sharing** — uses same V(x), T_eff, g_ij already in pipeline
2. **Self-consistency** — operates on the same dynamical system (Langevin SDE)
3. **Zero human-rating preservation** — all new variables from counts/timestamps/ratios
4. **Real calculations** — produces numbers (rates, probabilities), not descriptions
5. **Layer extension** — deepens existing layers, doesn't add disconnected parallel systems

## Files modified

- `your-workspace/divinity-health/sleep-app/agents/GOAL-ATTAINMENT-SCORING-ALGORITHM.md` — GAS v2.0 spec (Sections 6, 7, 13, 17, 18, 19 updated; file grew from ~19KB to ~29KB)
- `your-workspace/hydra-os/docs/your-org-behavioral-physics-engine.md` — behavioral physics engine Layers 6 and 7 updated with Kramers and Landau-Ginzburg equations

## Key architectural decisions

- Kramers was added as an extension of Section 6 (potential landscape dynamics), not a new section — it shares the same potential V(x) and noise model
- Landau-Ginzburg became new Section 7 (regime transition theory) because it fills a gap in the existing stack between dynamics (Section 6) and consistency scoring (Section 8)
- Both are cross-referenced in the behavioral physics engine spec so the layer specs and GAS spec stay aligned
- The order parameter ψ uses cos(θᵢ) between velocity and goal gradient — entirely from existing pipeline quantities

## User correction captured

"I don't want you to smash calculations together unless they make sense and align with human behavioral physics" → encoded as pitfalls in the evidence-driven-scoring-pipelines skill: don't propose menus of disconnected frameworks, don't present qualitative analogies as scoring extensions.
