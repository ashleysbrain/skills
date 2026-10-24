# Science Layer Registry — Reference for Overnight Builder

**Source:** DS AXIOM Physics & Methodology Guardian analysis (2026-06-10)
**Location:** `/<workspace>`

## Registry Format

Each layer entry contains:
- Theory name and origin (paper, author, year)
- Governing equation or core principle
- Target engine (Quartz / Wave / Self-Healing)
- Specific improvement mechanism
- Complexity: LOW / MEDIUM / HIGH
- Fidelity target (1-10)

## Phase 1 (Overnight — Highest ROI)

| Layer | Engine | Complexity | Fidelity |
|-------|--------|------------|----------|
| Shannon Entropy H(X) = -Σ p(x)log₂p(x) | Quartz | LOW | 8/10 |
| Self-Determination Theory → Kuramoto K | Wave | LOW | 7/10 |
| Bayesian Belief Updating P(H\|E) | Self-Healing | MEDIUM | 9/10 |
| MRAC Adaptive Control θ̇ = -Γ·e·x | Self-Healing | MEDIUM | 8/10 |

## Phase 2 (Week 1)

| Layer | Engine | Complexity | Fidelity |
|-------|--------|------------|----------|
| Percolation Theory (p_c threshold) | Quartz | MEDIUM | 7/10 |
| Transtheoretical Model (stages) | Wave | MEDIUM | 7/10 |
| Flow Theory (C/S ratio ≈ 1) | Wave | MEDIUM | 6/10 |
| Scale-Free Networks (Barabási-Albert) | Quartz | MEDIUM | 8/10 |

## Phase 3 (Week 2+)

| Layer | Engine | Complexity | Fidelity |
|-------|--------|------------|----------|
| Bass Diffusion dN/dt = [p+qN/M](M-N) | Quartz | MEDIUM | 7/10 |
| TD Learning δₜ = rₜ + γV(sₜ₊₁) - V(sₜ) | Wave | HIGH | 8/10 |
| Model Predictive Control | Self-Healing | HIGH | 9/10 |
| Friston Free Energy Principle | Self-Healing | HIGH | 7/10 |

## Builder Logic

1. Read SCIENCE_LAYERS.md
2. Check src/ directories for implemented layers
3. Identify next unfinished phase
4. Build ALL layers in that phase with:
   - Governing equations in Python
   - Unit tests for each layer
   - Integration with existing engine
5. Run pytest — 0 failures required
6. Commit and push
7. Report: what built, phase status, next phase

## Physics Foundation (Must Exist First)

**Quartz:** Energy functional E(x) = Σ E_self + Σ V_coupling, simulated annealing, coupling coefficients k_ij, temperature T, phase transitions
**Wave:** Kuramoto dθᵢ/dt = ωᵢ + (K/N)ΣKᵢⱼsin(θⱼ-θᵢ) + ξᵢ(t), separate Aᵢ/ωᵢ/θᵢ, damping γ, TWC = Kuramoto order parameter
**Self-Healing:** PID u(t) = Kp·e + Ki∫e + Kd·de/dt, Lyapunov V(y)>0, dV/dt<0 → convergence