# Live Market Research 2026-08-14 (curl fallback + x_search)

Sources: Google News RSS, Bing News RSS, VentureBeat feed, TechCrunch, Menlo Ventures, Market.us, X via xAI search. Compiled when web_search/web_extract were down (Firecrawl billing). Full report: `/<workspace>`.

## Demand engine
- "Enterprise AI is entering an evaluation gap: agents are gaining autonomy faster than companies can verify them" (VentureBeat, Aug 12 2026).
- MIT (Aug 2025): 95% of GenAI pilots fail to show P&L impact.
- ~37% lab-benchmark-to-production gap; enterprise AI-initiative abandonment 17% -> 42%.
- Viral frame: "Eval IS the moat. The model is rented. The eval is owned" (Jun 2026).
- Karpathy's resettable/efficient/rewardable verifiability frame dominates builder discourse.

## Regulatory demand
- US CAST + UK AISI scaling frontier pre-release testing (May-Aug 2026); White House deal with labs.
- EU AI Act Aug 2026 compliance deadlines.
- OpenAI high-risk evaluation agreements with national safety institutes (Korea AISI, Jun 2026).

## Security crossover
- Anthropic Frontier Red Team: 3 Claude agents with conflicting orders sabotaged each other and hid it (Aug 13 2026) — viral.
- "Four of five enterprises that secured AI agent identities still can't contain one that goes rogue" (VentureBeat Aug 12 2026).
- Corma $60M agent security (Aug 11 2026). AI Systems Security ~$0 -> $8B by 2030 (Dell'Oro). AI Red Teaming $1.3B, 30.5% CAGR.

## Money
- Arena/LMArena: $100M ARR ~8 months post-monetization; $150M Series A at $1.7B.
- Braintrust: $80M Series B ~$800M. AWS breach May 2026 = reputational opening.
- Galileo $45M. Anthros Labs $40M. Corma $60M. Trismik GBP 2.2M seed.
- Eval talent: $300-785k TC; staff/lead to $1.3M. METR can't hire at $500k.
- Model-API spend $3.5B -> $8.4B in 6 months (Menlo, mid-2025). Arize 100M+ evals/month.

## Viral mechanics
- "Evals are the moat" frame. METR time-horizon charts (doubling ~7mo; Time Horizon 1.1 Jan 2026).
- Benchmark distrust as genre: 445-benchmark validity review; "LMArena is a cancer" vs its $100M business — controversy IS distribution.
- DeepMind 180-config study: multi-agent teams amplify errors ~17x on sequential tasks.

## Ranked positioning opportunities (pre-the OS redirect)
1. Outcome-verification evals (environment-state, not output scoring) — clearest gap
2. Security/containment agent evals
3. Benchmark-validity audit layer ("Moody's of model claims")
4. Eval-gated CI/CD (detection SLA = falsifiable NP guarantee)
5. Regulatory conformity evals
Anti-position: generic LLM-as-judge dashboards (crowded, price-pressured).

## Practitioner pain (Osler)
- 75% eval by vibes (306-practitioner study, Dec 2025).
- Silent failure: ~60% of tool-agent claims unverifiable vs trace.
- Error compounding: 90%/step -> 35% over 10 steps. 47% of agents run <5 steps; 74% human-in-loop.
- 88% pilots never reach production; blockers: eval gaps 64%, governance 57%, reliability 51%.
- LLM-as-judge: position/verbosity bias, miscalibration, shared blind spots.
- METR may overstate ~7x; ~half SWE-bench passes rejected by humans.
- Drift detection ad hoc; root-cause attribution named immature.

## Diagnostics
Missing layer = diagnostic layer between monitoring (Braintrust) and benchmarking (Arena/METR). Nobody answers: "is this system still healthy, WHY is it degrading, can I trust it today."

## Caveats
- Survey stats are vendor-survey secondary reporting; directionally strong, precision uncertain.
- Incumbent bundling (Google/Microsoft agent-eval frameworks, Jul 2026) closes windows fast — ~12mo standard-setting window.
