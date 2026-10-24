# Biohacking Optimization Patterns for AI Organism Design

Source: research synthesis across 7 leading longevity/biohacking figures (Ferriss, Attia, Asprey, Huberman, Johnson, Patrick, Hof). 14 web searches + 6 page extractions. Translated into 9 design patterns for the DS organism.

Full deliverable: `~/your-workspace/organism/research/AI-ORGANISM-BIOHACKING-PLAYBOOK.md`

## Universal Consensus (all 7 figures agree)

1. Exercise is the #1 intervention (Attia ranks above all drugs)
2. Sleep/recovery is foundational infrastructure, not optional
3. Hormesis (controlled stress) works — cold, heat, fasting trigger adaptive responses
4. Measurement > intuition — every figure tracks something
5. Chronic inflammation is the universal enemy
6. Nutrition must be individualized

## Key Tensions

| Axis | Deterministic | Emergent |
|---|---|---|
| Agency | Johnson (remove human agency, algorithm decides) | Ferriss (N=1 self-experimentation) |
| Evidence | Attia (demands RCTs) | Asprey/Hof (N=1 acceptable) |
| Volume | Attia (high-volume training) | Ferriss (MED, once per week to failure) |
| Protocol | Johnson (100% deterministic) | Hof (controlled chaos to adaptation) |

## The 9 Patterns (mapped to DS engines)

### 1. MVD Compute (Minimum Viable Dose)
- **Bio source:** Ferriss MED/80-20. 80 seconds of tension at 50lb once per week = sufficient.
- **AI translation:** Minimum compute dose per task. Find the boiling point, not the maximum.
- **Engine:** the specialist engine (routing). Physics gate F = cost - T*info_gain already encodes this.
- **Implementation:** Route tasks with explicit compute budgets. Kill tasks where F > 0 before they consume resources.

### 2. Hormetic Stress (Sub-Lethal Adversity)
- **Bio source:** Wim Hof (PNAS 2014: voluntary sympathetic activation), Patrick (sauna heat shock proteins), Huberman (cold exposure dopamine).
- **AI translation:** Adversarial training + chaos engineering at sub-lethal doses. Inject controlled failure to strengthen resilience.
- **Engine:** the specialist engine (quality gate). Red-team cron that probes engines at sub-lethal frequency.
- **Dose:** Patrick sauna data: 4-7x/week for maximum benefit. Translation: weekly adversarial probes, not daily (overtraining risk).

### 3. HSP Cycle (Degrade and Rebuild)
- **Bio source:** Patrick. 30 min at 163F causes ~50% HSP increase above baseline. Proteins unfold, refold stronger.
- **AI translation:** Controlled degradation + rebuild. Weekly GC/refactoring sweep with quality gate.
- **Engine:** the specialist engine (cardiac conduction). The conduction system paces the degradation/rebuild cycle.
- **Implementation:** Weekly cron: archive stale skills, GC dead sessions, force refactoring of high-debt modules, rebuild with quality gate sweep.

### 4. Zone 2 Mode (80/20 Steady vs Sprint)
- **Bio source:** Attia. Zone 2 = lactate 1.7-1.9 mmol, mitochondrial efficiency. 3-4 sessions of 60+ min weekly. High-volume, low-intensity.
- **AI translation:** 80% steady-state background processes, 20% interactive sprints. Chronic sprint mode = overtraining = system degradation.
- **Engine:** the specialist engine (circadian). Background cron jobs = Zone 2. Interactive agent sessions = max effort.
- **Anti-pattern detection:** If sprint frequency exceeds 20% of total compute time, flag overtraining. Force recovery (Zone 2 only) until ratio rebalances.

### 5. SVS Health Score (Leading Indicator)
- **Bio source:** HRV research (Attia, Huberman). HRV drops BEFORE illness manifests — it is a leading indicator.
- **AI translation:** System Variability Score as leading indicator BEFORE critical slowing down fires.
- **Engine:** Autonomic bridge. Critical slowing down detection is the LAGGING confirmation; SVS is the LEADING warning.
- **Implementation:** Track variance of engine response times, bus message latency, and test pass rates over rolling windows. Rising variance = approaching tipping point. This gives earlier warning than the current critical-slowing-down detector alone.

### 6. Circadian Scheduling (Temporal Gating)
- **Bio source:** Huberman light protocol (melanopsin to cortisol cascade). Viewing light within 30-60 min of waking sets circadian rhythm.
- **AI translation:** Temporal gating of task types by time of day.
- **Engine:** the specialist engine (circadian).
- **Schedule:** Dawn (high-T creative, high reasoning) -> midday (Zone 2 background, maintenance) -> dusk (consolidation, reporting) -> night (NSDR, GC, archive).

### 7. Dopamine Engineering (Reward Prediction Error)
- **Bio source:** Huberman RPE research. Dopamine encodes prediction error, not reward itself. Intermittent reinforcement (70% reward rate) maximizes motivation.
- **AI translation:** Reward prediction error signals for agent reinforcement learning. Intermittent (70%) reinforcement. Baseline management — chronic high-reward depletes the baseline.
- **Engine:** the specialist engine (creative cortex).
- **Implementation:** RPE-based feedback for creative tasks. If an agent consistently over-performs expectations, raise the baseline (avoid dopamine depletion). If underperforming, lower expectations to create positive prediction errors.

### 8. Mitochondrial Efficiency (Cost per Info Gain)
- **Bio source:** Asprey (mitochondrial mode-switching), Attia (Zone 2 = mitochondrial efficiency). Mitochondria switch between survival mode (high output, high damage) and maintenance mode (efficient, low damage).
- **AI translation:** Track cost-per-info_gain across the fleet. Detect survival-mode persistence (high compute, low info gain) and force recovery.
- **Engine:** Physics gate. F = cost - T*info_gain is the direct analog.
- **Implementation:** Monitor F values across engines. When an engine persistently shows F > 0 (survival mode), force it into recovery (reduce task load, run maintenance tasks, wait for info_gain to recover).

### 9. Blueprint Engineering (Deterministic + Sandbox)
- **Bio source:** Bryan Johnson. Slowed pace of aging 9.2% via 100% deterministic protocol. Hundreds of biomarkers, every change data-validated.
- **AI translation:** 70% deterministic protocol + 30% experimental sandbox. Every change data-validated before fleet rollout.
- **Engine:** All engines (organism-wide principle).
- **Implementation:** Core organism operations run on deterministic protocols (cron schedules, fixed routing, tested pipelines). 30% sandbox for experimentation (new engines, new patterns, creative exploration). Every experiment is measured before promotion to the deterministic layer.

## Citation Key

- Ferriss: *4-Hour Body*, *Tools of Titans*
- Attia: *Outlive* (2023)
- Asprey: *Super Human* (2019), Bulletproof
- Huberman: Huberman Lab Podcast, Stanford neuroscience lab
- Johnson: Blueprint Project (blueprint.bryanjohnson.com)
- Patrick: *Experimental Gerontology* 2021 (sauna dose-response), FoundMyFitness
- Hof: PNAS 2014 (Kox et al., voluntary autonomic control)
- Mandsager et al.: JAMA Network Open 2018 (cardiorespiratory fitness, n=122,007)

## Quality Caveat

These patterns are original translations by biological analogy — engineering hypotheses, not validated protocols. Each needs a pilot before fleet-wide rollout. Priority for piloting: Pattern 5 (SVS) and Pattern 8 (Mitochondrial) because both wire directly into the existing physics gate and autonomic bridge.
