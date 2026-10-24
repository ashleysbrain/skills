# the OS OS Staged Benchmark Ladder — Completed Research + Design (2026-08-14)

Status: research COMPLETE (deleg_b4f5d8ba). Roadmap doc on disk: `organism/AI-HEALTH-BENCHMARK-STAGED-ROADMAP.md`.

## Live Market Findings (Andreasen, via x_search fallback)

**What exists (crowded, fast-moving):**
- Model-centric agent benchmarks mature: GAIA, tau-bench/2/3, AgentBench, MultiAgentBench/MARBLE, SPIN-Bench, TheAgentCompany, AppWorld — all measure TASK OUTCOMES, not system properties.
- MAS empirical scaling (hottest signal): Google/MIT ~180-config study — mean ensemble gain NEGATIVE (-3.5%), error amplification 17.2x decentralized vs 4.4x centralized, ~45% single-agent accuracy ceiling. DeepMind topology scaling laws (fan-out ~5 limit). Research papers, NOT owned benchmarks.
- Harness-layer eval (emerging): Shanghai AI Lab — 9 frameworks, 23 benchmarks, same model: accuracy flat, token cost varies 9.6x. Practitioner completion: LangGraph ~62%, AutoGen ~58%, CrewAI ~54%. Scale AI HarnessOpt-Bench (~1.8x attribution).
- Interop protocols exploding: A2A -> Linux Foundation (Jun 2025, 100+ cos, v1.0 signed agent cards). MCP -> LF Agentic AI Foundation (Dec 2025, 400M+ monthly SDK downloads). Agent mesh now named production pattern. **ZERO formal conformance/compliance suites** — only testnets.
- Composability metrics (borrowable, dormant): CK metrics (CBO, LCOM), instability index, Pact contract testing, fitness functions, SRE Golden Signals, chaos engineering, MTTR. **Nobody has ported these to agents.**
- Personalization: all single-user single-agent (LaMP, LoCoMo/LongMemEval, PAST-Bench 2026, PAHF, MerchantBench ~27% of human over 365 days, MatrAIx 8.3B personas).

## The Staged Gap Ladder (the deliverable)

**Stage 1 — Mesh/Harness System-Health** (9-15 month window)
- Gap: golden signals + MTTR + topology resilience + coordination tax + error containment + context saturation never assembled into a standing agent-mesh health index. Ingredients exist (SRE + Google/MIT findings); benchmark doesn't.
- Who's close: Galileo (platform, not open), LangSmith (proprietary), DeepMind (papers). Nobody ships open vendor-neutral.
- Velocity HIGH — reliability is the 2026 narrative.

**Stage 2 — Composability/Interchangeability** (12-24 month window, THE MOAT)
- Gap: no swap-delta benchmark; no A2A/MCP conformance suite; no composability score; no valid-composition-count. Literally no one building it. LF/AAIF natural owner but unannounced ("plausible late 2026-2027").
- Strategy: donate conformance + swap-delta suite to AAIF -> the OS becomes reference implementation -> benchmark defines category (the MCP playbook).

**Stage 3 — Personalization** (6-12 month window on multi-user)
- Gap: no multi-agent-teams-to-one-user, no multi-user households, no personalization portability across component swaps (swap the engine, keep the soul). Only WE have structural reason to build portability — it's a the OS feature.
- PAST-Bench finding is a gift: harness quality dominates personalization outcomes (+0.13-0.24 framework-dependent).

**Competitive threats by speed:** Galileo, Scale (harness evals), DeepMind (topology laws), LF/AAIF. None building Stage 2.
**Sequencing:** Stage 1 first (cheapest, borrow SRE, credibility) -> Stage 2 moat -> Stage 3 differentiator.
**Field-confirmed quote:** "An Agent Orchestration Bench equivalent to LLM arenas would fill a clear gap."

## Physics Metric Design (Lyapunov, 18 metrics)

**Stage 1 (7+):** algebraic connectivity lambda_2 > 0.1 | spectral gap > 0.2 | Kuramoto r > 0.8 under load | cascade eigenratio eta < 1 (Friedkin-Johnsen) | transfer entropy T(i->j) permutation-tested | queue utilization variance < 0.05 | emergence coefficient S > 0.2 | participation ratio PR > N/3.

**Stage 2 (7):** swap invariance |Delta_F| < epsilon | impedance mismatch R_match < delta_R (Bloch boundary-condition) | composition gain C_emergence > 1.2 | degradation Lyapunov lambda_max < 0 | modularity Q > 0.3 | coupling entropy H(J) decreasing | injection latency < 200ms.

**Stage 3 (4):** adaptation rate tau_adapt < 7 days | personalization depth Delta_theta > 0.3 | privacy leakage I_leak < 0.1 nats | co-adaptation ratio R_co in [0.7, 1.3].

**Ladder logic:** Stage 1 metrics (lambda_2, r, transfer entropy) inform safe swap distances in Stage 2; Stage 2 emergence baseline sets Stage 3 adaptation targets; Stage 3 co-adaptation validates personalization doesn't break Stage 1 health.

**Asset mapping (all prior machinery reused):** INTER <-> Kuramoto r | ALIGN <-> composition gain | ADAPT <-> tau_adapt | Fisher <-> coupling entropy | StochThermo <-> privacy leakage | RG <-> PR | Bloch <-> impedance matching | Spectral <-> lambda_2 | Multi-scale EMA <-> tau_adapt | Ring <-> r. Coupling matrix + cascade patterns = Stage 1 root-cause attribution. Bloch sphere = Stage 2 swap-state representation.

## Perceptual-Physics Rung (rung #19 — SPEC, DESIGNED until measured; T-261022-0060)

**Status:** spec only. Counts as a ladder rung ONLY when a scored run exists (MEASURE-BACK clause in the ledger row).

- **Gap:** all 18 metrics above measure system/coordination properties; none measures whether a model can SEE physics — convert observation streams into quantitative parameters. External measured basis proves the gap is live: PhySimCode (arXiv 2610.15722, 160.6K procedural samples, 162 phenomena, 10 SOTA MLLMs, released 2430-video eval set) — law RECITATION 4.27-4.93/5 vs law INFERENCE-from-video 1.51-2.47/5; best parameter recovery 7.7% within +/-20% (Claude Sonnet 4.6). VERITAS CONDITIONAL PASS 75% 2026-10-22 (self-reported numbers, single-source).
- **Scored metric:** parameter-recovery percent-within-tolerance — fraction of estimated parameters falling within +/-tol% of ground-truth simulator parameters, per phenomenon, aggregated over the eval set. Primary tolerance 20% (matches the measured ceiling reference). Report per-model: %within20 as headline, %within10/%within30 as spread.
- **Candidate corpus:** PhySimCode released 2430-video eval set (procedurally generated, ground-truth parameters known by construction — no manual annotation needed for scoring).
- **Ladder logic:** this rung grounds Stage 1 — a mesh whose agents claim physics competence (routing label in ops-model-routing-rules) must show recovered parameters, not recited laws; recitation-only physics claims are DECORATIVE per AUDIT_PHYSICS.md F8.
- **Scoring procedure (draft):** (1) present video + phenomenon class, model outputs parameter estimates; (2) score %within-tolerance against constructor ground truth; (3) baseline table = the 10 PhySimCode MLLMs at 7.7% ceiling; (4) a scored run on any model upgrades this spec from DESIGNED to MEASURED.

## Strategic notes (carried forward)

- Isomorphism score I(S) RESURRECTED from rejection: no market existed for organism-structure benchmarks when only we built organisms; if the composable agent OS category emerges, structural coherence becomes THE benchmark the category needs.
- Strategic flip: "compete in crowded market" -> "define the benchmark for a market that's about to exist."
- Prior assets all carry over as scoring machinery: 6+1 dims (INTER is mesh-native), 7 physics frameworks, coupling matrix = differential diagnosis, Bloch sphere phi = etiology.
- Tie-in: the OS OS being written/published weekend of 2026-08-14. Stage 2 composability metrics ARE the the OS architecture's acceptance tests.

## Open Items (third deep-dive pass, deleg_2cee3ed9, dispatched 2026-08-14, results pending)

1. **Popper adversarial:** threshold provenance (which numbers are derived vs magic), telemetry collectibility in real agent systems, AAIF lock-in reality, the OS decoupling risk (does benchmark survive if the OS ships late), physics-cosplay audit of all 18 metrics, cross-topology comparability (star-of-5 vs ring-of-8 normalization).
2. **Kuramoto physics corrections likely needed:** plain Kuramoto assumes identical oscillators — agent meshes have heterogeneous frequencies AND weighted coupling (needs networked-Kuramoto variant); transfer entropy estimator finite-sample bias + surrogate null; Friedkin-Johnsen vs SIR/branching-process for error cascades; emergence decomposition standard (Shapley vs nonnegative); Stage 2 degradation Lyapunov should probably be JOINT SPECTRAL RADIUS of the switching family (block swaps = switched-system dynamics); missing network physics (structural controllability, effective resistance, Jackson queueing stability, mesh renormalization).
3. **Osler missing categories:** security/immunology (multi-vendor mesh trust boundaries, prompt-injection propagation), economic metabolism (per-block cost attribution, composition ROI), human-in-the-loop (escalation appropriateness — 74% of production agents lean on humans, unmeasured), failure recovery (mesh MTTR, blast radius, chaos engineering), longitudinal development (block version drift, mesh reconfiguration effects, memory growth pathologies), context hygiene across blocks, governance/provenance in multi-vendor meshes, benchmark construct validity itself.
