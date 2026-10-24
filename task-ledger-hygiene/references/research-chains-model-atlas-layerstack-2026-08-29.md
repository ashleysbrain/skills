# Model-capability atlas + layer-stack research chains (2026-08-29)

Reference for task-ledger-hygiene / message-bus-protocol. Session record of the two verified research chains and their artifacts.

## Chains delivered (all verified by the V1-V3 triangle wave)

- `your-stack/research/MODEL-CAPABILITY-ATLAS-2026-08-29.md` (389 lines) — R1 dossiers (7 flagship families: LLM-5.x, Nemotron-3, Claude, GPT-5.6, GPT-5.4/Codex, Grok-4.x, DeepSeek-V4), R2 thinking-level taxonomy (T0-T4, exact invocation names like `reasoning_effort: low/high/max`), R3 priced bands P1-P4, R4 task-kind x lane pairing matrix, R5 wiring spec with G1-G4 guards + 6 build drafts.
- `your-stack/research/LAYER-STACK-INTEGRATION-2026-08-29.md` (303 lines) — L1 layer-stack map + 59-flow truth audit, L2 ecosystem-adaptation layer (DECIDE algorithm: RUN/DOWNGRADE-REPLAN/DEFER/ESCALATE; EWMA feedback per harness x model x task-kind), L3 merged 11-task mint list + rulings table.
- `your-stack/audit/TRIANGLE-PASS-ATLAS-LAYERSTACK-2026-08-29.md` (302 lines) — V1 adversarial / V2 QA / V3 synthesis verdict: VERIFIED, PASS-WITH-CONDITIONS.

## Census facts (measured live 2026-08-29, `<agent-home>/provider_models_cache.json`)

10 providers / 320 models: llm-vendor 12 (glm-5.3/5.2/5.1/5, 5v-turbo + 4.x coding-paas lane), nvidia 85 + NIM custom 83 (nemotron-3 ultra/super/lightning, jamba, starcoder2), openrouter 46 (claude lanes), nous 34, copilot 17 (gpt-5.4, 5.3-codex), xai 13 (grok-4.6, 4.20 reasoning variants), codex 12 (gpt-5.6 sol/terra/luna + 900k variants), sibling-agent-free 8. `moonshotai/kimi-k3` present in 3 lanes; zero Mythos models.

## Key structural findings

- **Flow-registry truth:** 59 flows registered, docs claimed 23. 28 honestly [THEORETICAL]. Always count, never trust prose.
- **Broker liveness two-factor proof:** same stagnant approval IDs + advancing poke counters = live but frozen worklist. Advancing both = healthy.
- **Ecosystem-adaptation layer (T-260829-0041):** per-microtask gated model selection within harness entitlements/budgets; quality-first (band below bar = ESCALATE, never silent downgrade); EWMA fitness per (harness, model, task-kind) written to `stores/ecosystem-fitness.json`.
- **DEPLOYMENT-STATE field:** `spec | partial | shipped — <artifacts>` mandatory in chain handoffs (grep-auditable); catches the 100%-spec/0%-shipped failure class.
- **Two config effort dials:** main session `reasoning_effort` (~line 49 config.yaml) vs `delegation.reasoning_effort` (~line 397). The delegation one was `low` and made all child seats lazy while the model name read glm-5.3. Patched to `high` 2026-08-29.
- **Single-source polling failure class:** action_broker polled only message-bus, never task-ledger — 822 tasks piled up silently. Polling organs must poll ALL task sources; queue pileups need monitors with named owners.

## Minted this session (ledger, all TRI-stamped)

T-260829-0038 (atlas, done), T-260829-0040 (layer-stack, done), T-260829-0041 (ecosystem-adaptation layer), T-260829-0042/0043/0044 (screen orders: ladder attribution, live-strip redesign, drawer dynamism), T-260829-0046 (step-drill drawers + correction affordances), T-260829-0047 (G5 free-lane SLA guard), T-260829-0048 (verified-to-action dwell clock), T-260829-0049 (overnight backlog drain), T-260829-0050 (model-tier law).