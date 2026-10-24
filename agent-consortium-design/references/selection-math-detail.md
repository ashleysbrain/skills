# Selection Math Detail — Agent Decision Engine

## Selection Function

```
Score(P, T) = alpha*DNA(P) + beta*EIGHT_D(P) + gamma*FIT(P,T)
              + delta*EVIDENCE(P) + epsilon*CONTRARIAN(P)
```

Default weights: alpha=0.30, beta=0.25, gamma=0.20, delta=0.15, epsilon=0.10

## Component Scoring

### DNA(P) — the specialist engine DNA Alignment [0-1]
```
DNA(P) = (physics_informed + bio_isomorphic + anti_slop + elite_standard) / 4
```
Each marker scored 0-1. If DNA < 0.5 -> REJECT.

### EIGHT_D(P) — 8D HUMAN Wellness [-1 to +1]
All 8 dimensions protected. Score per dimension: +1 (supports), 0 (neutral), -1 (harms).
Any dimension < 0 -> REJECT (no hierarchy of harm).
Normalized: sum of 8 dimensions / 8.

### FIT(P,T) — Task-Audience-Channel Fit [0-1]
Composite of audience match, channel match, awareness level match, format match.

### EVIDENCE(P) [0-1]
1.0 = peer-reviewed academic. 0.8 = elite institutional. 0.6 = multi-company.
0.4 = single company. 0.2 = practitioner opinion. 0.0 = unproven.

### CONTRARIAN(P) [0-1]
Differentiation score. 1.0 = highly contrarian. 0.0 = completely generic.

## Free Energy Gate (RATIO, not difference)

```
F = COST(P) / [Score(P,T) * (1 + INFO_GAIN(P))]
```
- F < 1.0 -> ADMIT (value exceeds cost)
- F >= 1.0 -> SKIP (cost exceeds value)

This is a RATIO gate. The previous difference formulation (F = COST - T*Score*INFO_GAIN)
failed because COST (0.1-0.7) and Score (0-1) are on different scales. The ratio
formulation is scale-invariant.

## Superposition

After scoring, hold top 3 candidates. Do NOT collapse immediately. The quality
gate measurement (after content production) determines the winner. This prevents
premature commitment.

## Immutable Elements (Cannot Mutate Without principal Approval)

- ALL 8 protected dimensions
- DNA markers themselves
- REJECT on 8D < 0
- REJECT on DNA < 0.5
- Healing mission (positive language only)

## What CAN Mutate (+-0.05 per generation)

- Weights (alpha through epsilon)
- T_urgency default
- Evidence thresholds (stricter only, never looser)

## Deeper Math Layer (44 formulas across 3 tracks)

The selection engine draws from a library of quantitative formulas. These
formulas apply at different decision-sequence phases, not all at once.

### Measurement Math (applies at Phase 5-8)
- A/B testing: sample size, statistical power, p-value
- Thompson sampling: Beta(alpha+s, beta+n-s) posterior update
- MMM: regression Y_t = beta_0 + beta_1*X_1 + adstock + Hill diminishing returns
- Attribution: Shapley value phi_i, Markov removal effect RE_k
- ROMI, CAC, LTV, payback period
- Incrementality: difference-in-differences

### Prediction Math (applies at Phase 6)
- Bass diffusion: dN/dt = p(M-N) + q(N/M)(M-N)
- Prospect theory: v(x) = x^alpha (gains), -lambda*(-x)^alpha (losses). lambda=2.25
- SIR virality: R0 = beta/gamma
- K-factor: K = i*c. K > 1 = viral
- Price elasticity: epsilon = (dQ/Q)/(dP/P)

### Valuation + Decision Math (applies at Phase 2 + periodic)
- Expected Value: EV = Sum[P(i) * Payoff(i)]
- Shannon entropy: H(X) = -Sum[p(x) * log2(p(x))]
- Portfolio theory: Sharpe = (E(R_p) - R_f) / sigma_p
- UCB1 bandit: UCB_j = Q_j + sqrt(2*ln(t)/n_j)
- Real options: Black-Scholes analog for campaign investment decisions

## Worked Example

Task: LinkedIn post about organism concept for AI researchers.

Candidates scored:
- Dunford+Schwartz: DNA=0.88, 8D=0.38, FIT=0.70, EVID=0.80, CONTRA=0.70 -> Score=0.686
- Radical Transparency: DNA=0.81, 8D=0.62, FIT=0.50, EVID=0.60, CONTRA=0.90 -> Score=0.680
- FOMO Scarcity: 8D=-1.0 (Psychological harmed) -> REJECTED

Superposition: hold Dunford (0.686) + Radical Transparency (0.680) + Starr (0.617).
Collapse after Genesis produces content drafts.
