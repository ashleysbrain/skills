# AI Evaluation Practitioner Pain — Market Research Knowledge Bank

Session: 2026-08-14. Research commissioned after principal rejected drift-benchmark
positioning as too narrow. Method: `x_search` (xAI/Grok live X + web search)
after DDG/Bing/Mojeek/Brave all bot-blocked curl and web_search/web_extract
were unconfigured. **Caveat: stats below are practitioner/X-reported and were
not independently re-verified — re-check before citing externally.**

## Symptoms practitioners report

1. **"Evals are vibes"** — 75% of teams evaluate agents without formal
   benchmarks (A/B tests, user feedback, eyeballing). Source: Dec 2025 study,
   306 practitioners + 20 case studies across 26 domains.
2. **Benchmark-to-production collapse** — ~37% avg drop from lab benchmark
   scores to enterprise performance; benchmarks contaminated, saturated,
   single-turn, static.
3. **Silent failure dominates** — plausible-but-wrong outputs, no crash, no
   alert. ~60% of tool-use agent claims accepted as "correct" were unverifiable
   from the actual tool-call trace (Provably analysis). Detection typically =
   user complaints.
4. **Error compounding** — 90% per-step reliability → ~35% over 10 steps
   (0.9^10). Hence production agents are tiny: 47% run <5 steps, 68% cap at
   ~10 steps before human intervention, 74% human-in-the-loop.
5. **Pilot graveyard** — ~88% of agent pilots never reach production; top
   blockers: evaluation gaps (~64%), governance friction (57%), model
   reliability (51%). Gartner: 40%+ of agentic projects canceled by 2027.
6. **LLM-as-judge untrustworthy** — position/verbosity bias, miscalibration
   (inflates low-true-accuracy, deflates high), shared blind spots with judged
   system, non-determinism. Trusted for ranking only + ~5% human sampling.
7. **Frontier benchmarks suspect** — METR time-horizon may overstate ~7x
   under human quality-grading; ~half of SWE-bench "passing" solutions
   rejected by human maintainers. RE-Bench/BrowseComp/GAIA/τ-bench miss
   persistent state, continual learning, output quality/impact.
8. **Post-deployment drift detection ad hoc** — silent provider model
   updates, prompt drift, data drift, agent context contamination. Teams
   cobble golden datasets + embedding-drift checks; root-cause attribution
   ("why did quality drop") named immature.

## Diagnosis (underlying condition)

Eval stack measures **capability on clean, static, pre-deployment tasks**;
the failure mode that kills deployments is **degradation in messy, dynamic,
post-deployment trajectories**. Observability tells you *what* happened;
benchmarks told you what the model *could* do once. Nothing answers: *is this
system still healthy, why is it degrading, can I trust it today?* The
diagnostic layer between monitoring and benchmarking is missing.

## The missing diagnostic test (market gaps)

1. **Differential diagnosis / root-cause attribution** — prompt change vs.
   provider update vs. data shift vs. agent context decay.
2. **Trajectory-integrity verification** — output-vs-trace consistency
   (the ~60% unverifiable-claims finding is the smoking gun; no product
   verifies artifact against evidence).
3. **Continuous "still healthy?" certification** — quality SLOs,
   drift/hallucination budgets with kill-switches, EU AI Act / ISO 42001
   audit evidence. Enterprises need a deployment gate, not a dashboard.
4. **Calibrated, domain-specific judging** — judges teams trust enough to
   auto-act on without human sampling.

## Positioning implication

Sell the **diagnostician**, not the drift test: continuously examines a live
agent, identifies failure etiology, issues trust verdict with audit-grade
evidence. Drift = one panel in the workup, not the product.

## Enterprise deployment requirements (context)

EU AI Act (phased through 2027, conformity assessments), ISO/IEC 42001,
SOC 2 / ISO 27001 table stakes, auditable signed logs of AI decisions,
regression testing + drift detection + human oversight evidence.

## Tool landscape criticism (Langfuse/Braintrust/LangSmith/Galileo/Phoenix)

Praised: tracing/observability (Langfuse OTEL-native), experiment velocity
(Braintrust "evals as the new PRD", ~12.8 experiments/day mature teams).
Missing: agent trajectory/process evals, closed loop trace→dataset→judge→
optimize→regression, CI/CD regression gates, compliance integration,
native alerting/kill-switches, calibrated judges.
