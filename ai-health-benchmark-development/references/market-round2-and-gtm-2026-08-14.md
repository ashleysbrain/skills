# Market Research Round 2 + GTM Operational Layer (2026-08-14)

Session detail: Andreasen live market research round 2, Osler user map, Andreasen GTM architecture. Consolidated into roadmap v2.4.0/v3.0.0 + companion doc `organism/AI-HEALTH-BENCHMARK-SETUP-AND-MARKET-ENTRY.md`.

## Market Round 2 Findings (live, x_search fallback — web_search down again)

**OTel GenAI verdict:** PROTOCOL (OTLP) is the standard — Arize AX native gen_ai.* ingestion Aug 11, W&B/Weave July, OpenLLMetry/Langfuse/SigNoz/Laminar/LangWatch all OTLP-native; OpenInference positioned complementary. SCHEMA still Development status, 12-18 months from stable, just moved to dedicated repo/WG (spec core v1.60.0). BUILD THE MANIFEST ON IT: versioned gen_ai.* semconv + pinned schema hash, abstracted behind our namespace. CONTRIBUTE upstream NOW — repo is weeks old, contributor leverage cheap, input channel not risk.

**Standards timer:** AAIF 247 members Aug 13 (+57 in 3 months: Anthropic, OpenAI, Google, AWS, Microsoft, Cisco, IBM, SAP, Datadog, Alibaba, Visa, Wells Fargo). Heavy on MCP/AGENTS.md/Goose/A2A-ACP. Observability + Identity/Trust WGs exist. NO conformance/benchmark program as of Aug 2026. NIST AI Agent Standards Initiative launched Feb 2026 (identity, security, authorization, auditing, interoperability; RFIs planned) — wants exactly our Stage 2 donation. ISO/IEC 42001 = governance not evaluation. UK AISI doing agentic cyber evals. DONATE-WITHIN-2-QUARTERS confirmed.

**New entrants:** NVIDIA + Artificial Analysis "AgentPerf" June 2026 (agents-per-megawatt, 200-turn trajectories) — closest Stage 1 collision but HARDWARE efficiency, not harness validity/composability. ServiceNow x AA "EnterpriseOps-Gym" (task space). AlphaEval DAIR.AI (task space). DeepSeek MIT agent harness Aug 14. Microsoft unified agentic runtime paper. NOBODY doing conformance + swap-delta certification. The "harness engineering" discourse (philschmid, LangChain 45%-of-stack) converges on our problem from commentary without building the instrument — vocabulary pre-seeded for us.

**SPEC adoption playbook:** founded 1988 BY competitor vendors (DEC/HP/IBM/Sun/MIPS) as non-profit — neutrality via co-ownership not third-party purity. Real-application workloads, Base vs Peak tiers, compiler-flag disclosure. Competitor peer review of submitted results (weeks-long challenge window). Publish-or-perish: use a result in marketing = must submit. Cold start solved by RFP/procurement demand — SPECint in procurement made participation table stakes. Friction mirror: BIG-bench died of friction; MMLU won on one-command determinism + HF leaderboard + citation flywheel.

## User Map (Osler)

**Personas:** (1) Enterprise platform engineer ($1k+/mo; ONLY cold-start-proof payer — instrument value at n=3 without leaderboard; R_0/p99/cost-ratio/swap-delta are self-referential measurements vs own baseline); (2) Procurement officer ($30M AI spend; the demand engine; one RFP line-item > 100 citations); (3) Agent startup CTO ($150/mo; follows enterprise demand, cannot create it); (4) Platform vendor PM ($1k+/mo certification; adversarial — wants scores not truth; 5x support load, meter it); (5) DevRel/content creator ($0 forever; CORROSIVE — their single-scalar-score demand is exactly the Goodhart design Stage 0 kills; give the one-command recipe and nothing else); (6) Standards participant (pays in legitimacy, 1 FTE engagement cost).

**Cold start honest:** leaderboard value at n=3 is ZERO; don't market rankings until n >= 20 (matches Stage 0 power analysis). First 20 users = Stage 0 validation cohort, not customers — free/discounted for held-out result donation rights. The SPEC insight: buyers adopted REPORTING REQUIREMENTS, not rankings.

**Decision chains:** engineer chain closes ONLY if it reads existing OTel telemetry (zero new deployment). Startups follow enterprise demand. Vendor adoption is LOSS-driven (lost deal), never vision-driven.

## GTM Architecture (Andreasen)

**Build stack (dependency order):** meshbench-core (M) -> telemetry manifest spec (S) -> meshbench-harness swap+fault-seeding hooks (M) -> mini-leaderboard recipe (S) -> arXiv preprint (M) -> leaderboard site + Mesh Forecast Registry (M) -> conformance suite (L) -> held-out corpus (ongoing). Order: 1,2,4 parallel; 3 after 1; 5 after 4; 6 after 5; 7 last.

**Phases with kill criteria:**
- Phase 1 CREDIBILITY (wk 1-8): exit = preprint + >=50 mini-leaderboard runs by >=20 external accounts + OTel PRs merged. KILL: ICC < 0.7 on reference meshes (stop, re-derive) or <20 external runs in 6 wks (friction wrong, redesign).
- Phase 2 COMMUNITY (mo 2-6): exit = >=10 org systems + 2-3 buyers in RFPs + 90-day registry record. KILL: zero buyer adoption by mo 5 or >1 engineer-week telemetry friction -> repackage as consulting.
- Phase 3 MOAT (mo 6-12): exit = donation filed + >=1 vendor cert pilot. KILL: rival standards program lands first (race or merge, never compete) or zero paid pilots in 2 quarters (retain corpus, license data).

**Viral engine:** the SWAP-DELTA CARD — one auto-generated image per run (A->B, swap-delta, cost delta, p99 delta, verdict CONTAINED/BLEEDING). METR-chart adapted: one number + safety band, comparable across posts; LMArena dynamics (every submission = a fight between two named vendors, measured by submitter not us). Four loops: engineer (identity value; HN angle "we measured 9.6x token variance in our own harness"), vendor (cite-or-perish), buyer (RFP spreads silently), forecast (quarterly scored predictions = recurring content). BRAND = THE METRIC NAME: swap-delta, mesh health, Mesh Forecast Registry. Never lead with org name.

**First 30 days:** W1 core repo + semconv pinned + manifest draft + first OTel PR. W2 test-retest on 2 reference meshes (ICC) + MTMM v1 + scope mini-leaderboard to ONE swap axis. W3 alpha + dogfood 3 internal + 2 external. W4 NIST RFI draft + preprint skeleton + Show HN + 2 enterprise buyer conversations.

**Setup risks:** (1) telemetry absence on real platforms -> harness ships adapters; the gap IS the Stage 2 pitch. (2) Stage 0 validity failure -> gates before any public number; 5 honest metrics beat 34 decorative. (3) standards window closes -> OTel W1, RFI W4, donation pre-drafted.
