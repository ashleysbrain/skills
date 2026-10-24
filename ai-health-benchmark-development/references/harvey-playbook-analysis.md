# Harvey Playbook Analysis (from Gabe Pereyra talk, 2026-08-13)

## Source
Gabe Pereyra, co-founder and president of Harvey (legal AI), ex-DeepMind.
Talk: "How Harvey Built a Research Lab on a Budget"

## Harvey's 10-Point Playbook

1. **Benchmarks first** — Build domain benchmarks before training (Legal Agent Bench, contracting datasets, diligence datasets). Open-sourced them.
2. **Domain experts guide synthetic data** — Lawyers "vibe code" to generate realistic legal datasets with planted issues. Can't train on customer data.
3. **Open-source models now competitive** — LLM 5.2, Kimmy 3, NeMo-Megatron. Post-train to frontier-level for specific tasks.
4. **Multiple post-training partners** — Fireworks, Base 10, Ngram, Trajectory, Applied Compute. Different bets.
5. **Serving infrastructure first** — Model serving, fallbacks, routing BEFORE post-training.
6. **Simple swaps** — Find places to naively swap open-source models for cost/perf.
7. **Model routing** — Route certain queries to open-source models.
8. **Production feedback flywheel** — Serve -> collect feedback -> improve datasets -> post-train -> serve better.
9. **Open-source benchmarks** — Community validation, pull requests, lab adoption.
10. **Moneyball thesis** — Compete with frontier labs on a budget using the ecosystem.

## What the specialist engine (non-gaps)
- LLM 5.2 in production (already running Moneyball thesis)
- 63 engines in organism architecture
- the specialist engine routing (live model routing)
- 8D/TWC scoring as our benchmark
- PhD-credentialed specialists
- HIPAA constraint (same structural problem as legal privilege, harder)

## What the specialist engine (true gaps)
1. No public/open benchmark
2. No planted-issue dataset at scale
3. No formal post-training partner portfolio
4. No model-level feedback flywheel
5. No production monitoring at parity
6. No difficulty-calibrated eval curve

## the specialist engine Doesn't Have
1. Real organism, not metaphor (63 engines mapped to body systems)
2. 8D/TWC scoring IS the product (Harvey's benchmark measures the product)
3. HIPAA > legal privilege in severity (harder constraint = deeper moat)
4. Health data is multimodal (biomarkers, vitals, behavioral) vs text-only

## Key Insight for Benchmark
The viral formula: simple scoring + maps to something humans value + headline-friendly + leaderboard that drives competition. Every major benchmark measures peak capability. Almost none measure real-world reliability.
