# Quantitative Marketing Math — Formula Reference
## The 44 Formulas Behind Agent Decision-Making

Condensed from 3 research tracks (deleg_b04df968, deleg_7aae2e87, deleg_347df7f4).
Full files: marketing-consortium/06a/b/c-QUANTITATIVE-MATH-*.md

## When Each Formula Runs (by decision phase)

| Phase | Formulas | Purpose |
|-------|----------|---------|
| Pre-content (selection) | Score(P,T), Free Energy F=COST/[Score*(1+INFO_GAIN)] | Pick philosophy |
| Content exists (quality check) | Anti-slop checklist, awareness match | Pass or fail |
| Pre-publish (prediction) | Bass diffusion, K-factor, prospect theory, elasticity | Predict performance |
| Post-publish (immediate) | CTR, engagement rate, dwell score | Instant feedback |
| Post-publish (delayed) | A/B significance, Thompson update, ROMI, CAC/LTV, Shapley, incrementality | Did it work? |
| Learning cycle | Bayesian update, weight refinement | Get smarter |

## Key Formulas

### Selection Math (runs BEFORE content exists)
Score(P,T) = 0.30*DNA + 0.25*EIGHT_D + 0.20*FIT + 0.15*EVIDENCE + 0.10*CONTRARIAN
F = COST / [Score * (1 + INFO_GAIN)]; F >= 1.0 -> SKIP

### Bass Diffusion (will this idea spread?)
dN/dt = p(M-N) + q(N/M)(M-N); p~0.03, q~0.38 (meta-analytic avg); SaaS: p~0.07, q~0.60

### Prospect Theory (how humans perceive messaging)
Gains: v(x) = x^alpha; Losses: v(x) = -lambda*(-x)^alpha; alpha~0.88, lambda~2.25
Loss-framed messaging is 2.25x more motivating BUT must pass 8D psychological harm gate.

### K-Factor (viral coefficient)
K = i * c; K > 1 = viral growth, K < 1 = decay

### Thompson Sampling (autonomous content optimization)
Sample theta_k ~ Beta(alpha_k, beta_k); Select max; Observe r; Update alpha_k += r, beta_k += (1-r)

### LTV:CAC (unit economics sustainability)
LTV = ARPU * Gross Margin / (Discount + Churn); CAC = (Marketing+Sales Spend) / New Customers
Healthy: 3:1. Unsustainable: <1:1. Under-investing: >5:1.

### ROMI (return on marketing investment)
ROMI = [(Attributable Revenue * Margin - Marketing Spend) / Marketing Spend] * 100

### Shapley Value Attribution (fair channel credit)
phi_i = Sum over coalitions S: [|S|!(n-|S|-1)!/n!] * [v(S+{i}) - v(S)]

### Incrementality (causal proof)
delta_delta = (Y_treated,post - Y_treated,pre) - (Y_control,post - Y_control,pre)

### Ebbinghaus Forgetting (for memory system design)
R = e^(-t/S); S = memory strength. Accessed memories strengthen (spacing effect).

## Sources
- Cohen (1988), Bass (1969), Kahneman/Tversky (1979), Thompson (1933)
- Shapley (1953), Fader/Wharton LTV, Sethuraman et al. (2011) ad elasticity
- Aral (2011) Science virality, Binet and Field (2007) IPA Databank
- Full citations in marketing-consortium/06a/b/c files
