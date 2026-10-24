# Benchmark-as-Authority: The Harvey / Legal Agent Bench Pattern

**Session:** 2026-08-13 — the specialist engine (creative cortex) redo of the Harvey analysis
**Skill:** `open-core-skill-architecture` → Benchmark-as-Authority Strategy section

## The question this pattern answers

> "What is our equivalent of [competitor's open benchmark] — something that gets us credibility in [community] without requiring domain credentials we don't have?"

## The Harvey reference case

Harvey (legal AI) released **Legal Agent Bench** — an open benchmark of legal tasks with known answers, mechanical scoring, and a public leaderboard. It made Harvey the authority in legal AI. Critically, Harvey did NOT need their team to have law degrees to validate the benchmark. The benchmark was **self-validating** (tasks have known answers, anyone can run it) and therefore **authority-creating** rather than authority-dependent.

The credibility flywheel: release benchmark → labs adopt it → you become the reference → your product credibility rises. No domain license required at any step.

## The Harvey test — four conditions for a self-validating benchmark

A candidate benchmark qualifies only if ALL four hold:

1. **Self-validating** — mechanical, reproducible scoring. Anyone can run it without trusting your expertise.
2. **Falsifiable** — contains a prediction that *can fail*. If it can't be broken, it's marketing, not a benchmark.
3. **Authority-creating, not authority-dependent** — no domain expert can invalidate it by questioning your standing. If "on what basis do you define X?" is a fatal question, it's the wrong benchmark.
4. **Category-defining** — creates vocabulary others adopt. The moat is the term/definition; every paper using it cites you.

## The critical pitfall (observed 2026-08-13)

**Do NOT map the benchmark onto the domain you aspire to authority in. Map it onto the engineering property where you actually have authority.**

The rejected first analysis proposed a "Health Agent Bench" built on the 8D/TWC clinical scoring pipeline, synthetic patient cases with planted pathologies, and diagnostic validity protocols. This required medical authority to validate. Any clinician could ask "on what basis do you define a planted pathology?" — and DS has no answer that survives that question.

The fix: map the benchmark onto **biological isomorphism and cascade resilience** — an architecture property, not a health outcome. DS has genuine authority in multi-agent organism architecture (65 engines, 125 dependency edges, real physics foundations). No medical credibility is required to score "how structurally isomorphic is your multi-agent system to a biological organism?"

## Candidate discard criteria

| Candidate | Verdict | Reason |
|---|---|---|
| Multi-agent coherence benchmark | Discard | Too generic; AutoGen/CrewAI/LangGraph already claim this. Can't own the category. |
| Specialist panel reasoning quality | Discard | Subjective, no mechanical scoring. Devolves into Chatbot Arena. |
| Physics-informed architecture benchmark | Discard | "Physics" branding was already killed by a prior branding panel as externally puncturable. Don't relitigate. |
| Organism orchestration benchmark | Discard | Orchestration without isomorphism = generic multi-agent coordination. Differentiator is biological *structure*, not orchestration. |
| Open ECS taxonomy as standalone standard | Secondary | Ship as scoring rubric *inside* the benchmark. A taxonomy alone creates no leaderboard. |

## The DS application: Physiomorphic Isomorphism Benchmark (PIB)

Three components, all already built and runnable in the DS workspace:

1. **Isomorphism Score I(S)** (`isomorphism_score.py`) — composite score across four criteria: C_c (component), C_f (functional), C_r (relational), C_o (organizational). Fleet currently scores I(S)=0.80 (strong). Formula: `I(S) = (C_c + C_f + C_r + C_o) / 4`, bounded [0,1].

2. **Cascade Resilience Prediction P1** (`cascade_failure_sim.py`) — single falsifiable claim: "systems scoring higher on biological isomorphism exhibit lower cascade failure rates under random component removal than non-isomorphic systems of equivalent compute." Monte Carlo simulation: progressively remove agents, measure retained functional capacity, compare against randomized control. Preliminary advantage: +0.27.

3. **Reference Fleet** (65 engines, `ecs.py`) — the origin point other labs score their own systems against.

**What stays closed:** 8D/TWC scoring engine, health data, patient pipelines, coaching logic. PIB scores *organism structure*, not health output. Clean separation.

## Why "already built" is the strongest strategic move

The redo discovered the benchmark wasn't hypothetical — `isomorphism_score.py` and `cascade_failure_sim.py` already existed and ran. This changes the packaging timeline from "build" to "package" (2-3 weeks vs months). Always run the code to verify assets exist before recommending they be built.

## Document format constraint (principal-level strategy docs)

- ~3 pages, under 10KB. Explicit length ceilings ("not another 16KB") are hard constraints.
- One-sentence answer first, then reject prior approaches with reasoning.
- Ground claims in runnable code, not assertions.
- One decision asked at the end, not five moves.

## Related workspace artifacts
- `/<workspace>` — the strategy doc produced this session
- `/<workspace>` — the rejected (clinical-frame) first analysis
- `/<workspace>` — the academic skeleton (already contains P1 and I(S))
- `/<workspace>` — the benchmark scoring engine
- `/<workspace>` — the falsifiable prediction tester
