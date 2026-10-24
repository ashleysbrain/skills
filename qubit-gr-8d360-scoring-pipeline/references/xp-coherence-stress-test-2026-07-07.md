# Monte Carlo Population Stress Test for Scoring Formulas
## Technique: Validating formula gaps at scale before shipping

### When to Use
- Someone claims a scoring formula (coherence multiplier, coupling term, XP formula) creates an unacceptable gap at scale
- You need to verify whether a flagged mathematical risk is real or an extreme edge case
- Pre-shipping gamification XP or any formula that multiplies scores by derived factors

### The Pattern

1. **Import the REAL formula** from the canonical calculator (e.g., `hydra-os/products/principal-8d-tracker/calculator.py`). Never reimplement it. The simulation must call the same code path as production.

2. **Define population archetypes** that reflect realistic distribution. For health scoring, five segments cover the space:
   - balanced_high (health-conscious, all dims strong)
   - balanced_mid (average user)
   - imbalanced (some dims strong, some weak — where coherence penalty bites)
   - chronic (one or more dims persistently low — illness, depression)
   - struggling (most dims low)

3. **Mix the population** with realistic proportions (25% balanced_mid, 20% balanced_high, 25% imbalanced, 18% chronic, 12% struggling). This matters: extreme edge cases are rare in real populations.

4. **Test at multiple scales**: 1K, 10K, 50K. If the gap is stable across scales, it is a structural property of the formula, not a scale artifact.

5. **Compare formula variants**: naive, linear, squared, capped, log-diminishing, flat. This shows which variant creates the gap.

6. **Report p99/p10 gap** (not max/min). Extreme tails are not representative of user experience. The original "4.7x gap" claim likely used max/min, which overstates the risk.

7. **Check archetype equity**: break down mean XP by archetype. This is the Red Team / vulnerability concern. balanced_high vs struggling ratio tells you if the formula punishes users with health challenges.

### Worked Example: Coherence Multiplier (2026-07-07)

**The claim**: Session 2 of the Gamification Advisory Board flagged a 4.7x XP gap from coherence multiplier compounding. This was a standing blocker for two weeks.

**The simulation**: 50,000 users, 5 archetypes, real TWC formula `TWC = ETA * mu * C * (1 + 0.5 * S)` where `C = 1 - sigma/mu`.

**The result**: The 4.7x gap does NOT replicate. Actual worst case at 50K scale:
- Coherence squared: 3.48x p99/p10
- Coherence linear: 3.00x
- Flat (no coherence on XP): 2.64x
- Gap is STABLE across scales (1K=3.42x, 10K=3.47x, 50K=3.48x)

**The lesson**: The original flag was likely computed at max/min (best possible coherence user vs worst possible coherence user), not at population percentiles. Always verify flagged gaps with Monte Carlo population simulation before accepting them as blockers.

### Key Formula Relationships (verified)

For the coherence factor C = 1 - sigma/mu:
- Perfectly balanced profile (all dims equal): C = 1.0, sigma = 0.0
- Extreme imbalance (half dims at 1, half at 9): C drops significantly
- C is bounded [0, 1] and rewards consistency, not absolute level

For XP formula variants (TWC = score, C = coherence):
- `XP = TWC` — flat, C is diagnostic only (safest for v1)
- `XP = TWC * (1 + C)` — linear boost, 3.0x gap at 50K
- `XP = TWC * (1 + C)^2` — quadratic boost, 3.48x gap (worst case)
- `XP = TWC * (1 + min(C, 0.6))` — capped, 2.65x gap
- `XP = TWC * (1 + 0.5 * log(1 + C*4))` — log diminishing, 2.81x gap

### Archetype Equity Check (Red Team concern)

At 50K scale with coherence_squared:
- balanced_high: mean XP 221, mean C 0.904
- balanced_mid: mean XP 114, mean C 0.755
- imbalanced: mean XP 82, mean C 0.619
- struggling: mean XP 73, mean C 0.763

Ratio balanced_high / struggling = 3.0x. Significant but not the 4x+ that would require redesign. The imbalanced archetype has lower coherence (higher sigma) despite moderate mean scores — this is where coherence penalty bites hardest.

### Files
- Simulation script: `ds-wave-gamification-advisory-panel-private/xp_stress_test.py`
- Raw results JSON: `ds-wave-gamification-advisory-panel-private/xp_stress_test_results.json`
- Meeting brief: `ds-wave-gamification-advisory-panel-private/MEETING-BRIEF-2026-07-07.md`

### Reproducibility
Seed=42. Reproducible across runs. Uses the real `compute_twc()` from calculator.py, not a reimplementation.
