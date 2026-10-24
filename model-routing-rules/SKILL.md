---
name: model-routing-rules
description: Correct model names and routing rules for API providers. Apply to ALL model selection and subagent configuration.
version: "1.2.0"
last_updated: "2026-10-24"
---

# Model Routing Rules

## MODEL-CURRENCY POLICY (T-261022-0103, principal directive "we should not run on old models")
- **ACTIVE DEFAULTS must be current-gen.** A default model string in code/config
  (TASK_MODEL_TABLE, engine MODEL_ROUTES, organism builder resources, effector pools,
  cron lanes) must name a current-frontier model, not a prior generation.
- Current frontier (verified 2026-10-24): glm-5.3 family / gpt-5.6-* / claude-5 family /
  gemini-3.x. Flash-tier current = glm-5.3-flash.
- **Menus are exempt**: multi-gen fallback MENUS are legitimate resilience — menus are
  not defaults. Migration touches defaults only.
- **Sweep ownership**: when this policy is violated fleet-wide, run the
  model-recommendation-maintenance skill sweep. Defaults rot silently — audit quarterly
  or on every frontier shift.
- Alias candidate for permanent currency (needs live verification before adoption):
  `z-ai/glm-flash-latest` / `z-ai/glm-latest` auto-pointing aliases.
- **TWO-TIER LANE RULE (T-261022-0105, principal question "why 100 glm"):**
  autonomous/unattended lanes (crons, daemons, engine fleets) stay subscription-pinned
  on llm-vendor-glm coding plan — flat cost, no credit cliff (402 economic law,
  model-compliance-guard: paid per-token elites die HTTP 402/403 silently in
  unattended runs). **principal-initiated peak work** (deep research, marquee deliverables,
  adversarial review) MAY route to paid current-gen elites (gpt-5.6-* / claude-5 /
  gemini-3.x) with an explicit per-run credit cap declared at dispatch time.
  Cross-vendor diversity at zero cost where lanes allow: OpenRouter free-pool
  failover ladder + local-first embedding failover. Menus stay multi-gen (resilience).

## Zai / LLM
- **USE (reasoning lanes):** glm-5.3
- **USE (fast/mechanical/flash tier):** glm-5.3-flash
- **DEPRECATED as ACTIVE DEFAULTS:** glm-4.5-flash (2 gens behind), glm-4.x family,
  glm-5, glm-5.1, glm-5.2 (superseded by 5.3)
- Migrated 2026-10-24 (T-261022-0103 build): sherman_router TASK_MODEL_TABLE mechanical
  lane, adversarial_pool effector-divergent, organism_config builder defaults,
  ds-deming methodology routes. Remaining known glm-5.2/4.5-flash defaults: ~936
  occurrences across agent-organism engine methodology layers (sweep pending).
- KEY NOTE (flagged 2026-10-24): bare GLM_API_KEY (hermes .env) returned 1113
  "insufficient balance" for glm-5.3 AND glm-5.3-flash while glm-4.5-flash completed —
  paid-tier balance is exhausted on that key; flash-legacy free quota still works.
  the operator agent-owned key, needs recharge or migration to coding-plan auth.

## Google Gemini
- **USE:** Gemini 3.5 Flash, Gemini 3.1 Pro
- **DEPRECATED (do NOT use):** Gemini 2.5 Pro, Gemini 2.0 Flash, Gemini 2.5 Flash (old models, auth failures)
- **NOTE:** Google Gemini CLI re-auth is pending. Will update when done.

## OpenRouter
- **NEVER use Anthropic models through OpenRouter.** This means:
  - No Claude (any version)
  - No Opus
  - No Sonnet
  - No Fable
  - No Mythos
  - No Quad models
- Anthropic must go through Anthropic's own API directly, not through OpenRouter.

## Nvidia
- **USE:** Neumatron Super 120B (free), Neumatron 3 Ultra Free (550B params)
- **DO NOT use:** Other Nvidia model references that return "invalid model" errors

## Quantitative-Perception No-Go (state-vs-recover law, T-261022-0060)
- **Measured basis:** PhySimCode (arXiv 2610.15722; 160.6K samples, 162 phenomena, 10 SOTA MLLMs): law RECITATION 4.27-4.93/5 vs law INFERENCE-from-video 1.51-2.47/5; best parameter recovery **7.7% within +/-20%** (Claude Sonnet 4.6). VERITAS CONDITIONAL PASS 75% (2026-10-22, self-reported benchmark numbers, single-source).
- **RULE:** tasks converting observation streams (video, sensor telemetry, imagery) into quantitative parameters or simulation code are a **measured NO-GO for direct MLLM extraction**. Do not route them to any multimodal model as the measuring instrument.
- **LABEL:** every such dispatch gets stamped `[RECOVERY-CONFIDENCE: <=7.7% within 20%, best known 2026-10]` at routing time. MEASURE-BACK: log stamped label vs actual outcome for the next 3 observation-to-parameter dispatches.
- **DECOMPOSE INSTEAD:** instrumentation (programmatic extraction of raw observables: tracking, edge/flow detection, digitizer output) + fitting (numeric optimization over an explicit model). The MLLM may orchestrate and interpret; it must never be the meter.
- **WHY:** knowing physics is not seeing physics. Law-recitation scores are NOT evidence of perception competence — a model that can state F=ma and cannot recover m or a from video has decorative physics.

## General Rules
- When configuring cron jobs or subagents, always check model names against this list
- If a model returns auth failures or "model not found" errors, check this list first
- Update this skill when new models are verified or old ones deprecated
