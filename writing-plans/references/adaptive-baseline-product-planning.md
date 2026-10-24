# Adaptive Baseline Product Planning Notes

Use this when the feature involves personalized scoring, health calibration, or any system where the user's baseline changes over time.

## Core planning rule
Do not model a person with fixed population defaults if the product is meant to adapt to them. Plan a baseline layer that can evolve.

## Recommended build order
1. Baseline intake and schema
2. Normalization layer that maps evidence to user-specific anchors
3. Drift and recalibration engine using snapshots and EMA-style updates
4. Activity scoring persistence
5. Aggregate scoring and TWC rollup
6. Quest or gamification layer sourced from the DB

## Planning checklist
- Define the baseline objects first, before activity scoring
- Treat baselines as versioned and mutable over time
- Include snapshot history and explainability
- Persist activity scores, not just final totals
- Make the DB the source of truth for the game layer
- Write end-to-end tests that prove recalibration changes later scores

## Common pitfall
A plan that starts with the final score formula but skips baseline normalization will produce mathematically elegant, user-wrong results.
