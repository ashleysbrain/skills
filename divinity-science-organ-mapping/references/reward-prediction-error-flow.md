# Reward Prediction Error Flow (the specialist engine)
# Session 2026-07-07
# The biological isomorphism for gamification

## Classification

This is a PROCESS FLOW (ECS-NPR), NOT a standalone engine. It flows THROUGH
existing engines:
- the specialist engine (:port) — task completion events (INPUT)
- the specialist engine (:port) — RPE computation (THE FLOW)
- the specialist engine (:port) — action reinforcement (OUTPUT)
- the specialist engine (:port) — neuromodulatory context (MODULATOR)

ECS: DS-ECS-NPR-13.01.07-v1.0.0

## The Core Formula

delta = R_actual - R_expected

- delta > 0: reward exceeds expectation. Dopamine spike. Reinforce behavior.
- delta < 0: reward below expectation. Dopamine dip. Extinguish behavior.
- delta = 0: reward matches expectation. Baseline. Maintain, do not amplify.

## The Chain of Events (Habit Loop)

1. Bragg fires: task completed with free energy delta
2. Schultz computes: was the reward more or less than expected?
3. Carlsson acts: positive delta reinforces (GO pathway), negative extinguishes (NOGO)
4. Schultz updates: expectation baseline shifts (Rescorla-Wagner: E_new = E_old + alpha * delta)
5. Schultz checks: has delta been near zero for N repetitions? If yes, habit formed. Gamification fades.
6. Dale broadcasts: neuromodulatory context modulates quest difficulty

## Three Computation Modes

1. **Standard**: for stable users. Plain delta computation.
2. **Scarcity-adjusted**: inflates delta for chronically ill/overwhelmed users. Scientific basis for Resilience XP. Chronic stress elevates cortisol which dampens VTA dopamine (Pruessner et al 2008). The adjustment corrects for this neuroendocrine compression.
3. **Habit-formation**: delta naturally declines toward zero as context stabilizes. When delta has been near zero for N repetitions in stable context, the behavior transferred from ventral striatum (goal-directed) to dorsal striatum (habitual). This is Wood's 66-day finding in computational form. Triggers gamification sunset.

## The Gamification Toggle

The RPE flow runs ALWAYS. The toggle controls SURFACING, not computation:
- off: RPE computed internally, user sees nothing (ventral striatum without awareness)
- standard: RPE surfaced as XP, streaks, levels (ventral striatum with prefrontal awareness)
- full: RPE narrated as RPG world state (full narrative consciousness of learning)

## The Moat

Every gamification system can give points. Only a system with reward prediction error can LEARN what rewards each specific user. The expectation baseline calibrates per individual. The same task gives more XP to a user who expected less. Over time, predicted rewards produce delta=0 and the gamification fades for that behavior.

## The Four Adversarial Review Scientists

Each scrutinizes a different part of the flow:
- **Berridge**: does delta create genuine "liking" or just "wanting"? Pair every delta with a reflection prompt to engage the liking system, not just wanting.
- **Ryan**: does the delta support or undermine autonomous motivation? The sunset condition (habit formation then gamification fade) ensures delta eventually disappears and behavior persists.
- **Wood**: is the habit transfer actually working? Detect context instability and extend threshold. Do not punish.
- **Mullainathan**: is the scarcity adjustment sufficient? Calibrate against real population data.

## Key Citations

- Schultz, Dayan & Montague (1997) "A neural substrate of prediction and reward" Science 275:1593-1599
- Schultz (2016) "Dopamine reward prediction error coding" Frontiers in Neuroscience 10:243
- Berridge & Robinson (1998) "What is the role of dopamine in reward?" Psychological Review
- Deci, Koestner & Ryan (1999) meta-analytic review, Psychological Bulletin
- Wood & Neal (2007) "A new look at habits" Psychological Review
- Mullainathan & Shafir (2013) "Scarcity"
- Mani, Mullainathan et al (2013) "Poverty impedes cognitive function" Science

## Full Design Spec

See: `ds-wave-gamification-advisory-panel-private/PROCESS-FLOW-RPE-SCHULTZ-SPEC.md`
for the complete 5-layer spec, ECS registry entry, habit loop sequence, and
gamification toggle mapping.
