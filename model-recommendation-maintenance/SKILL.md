---
name: model-recommendation-maintenance
category: operations
description: Update and verify model recommendations, canonical model names, and runtime defaults across docs, repos, and fleet config when model policy or routing changes.
---

# Model Recommendation Maintenance

## Purpose
Keep model recommendation docs, routing defaults, and related config in sync when the preferred model stack changes or model names are normalized.

## When to Use
Use this skill when:
- model recommendations in docs are stale, inconsistent, or use outdated aliases
- repo docs, prompts, archived reports, and live config must all agree on model names/routing
- a fleet default model or heartbeat model needs to change
- model naming conventions need normalization across multiple files
- recommendation text and actual runtime configuration disagree
- a model policy update requires both documentation and live config changes

## Core Pattern
1. Survey all affected docs/config for model names, aliases, and recommendation language.
2. Identify the canonical model names that should be used everywhere.
3. Update human-readable recommendations and the actual runtime/default configuration separately.
4. Apply the live change with the relevant CLI or config command.
5. Verify both the text updates and the active default/routing state.
6. If the task includes a repo-wide cleanup, preserve archival/historical docs unless the user explicitly wants them normalized too.

## Procedure

### 1) Survey the surface area
Search for:
- model names and aliases
- recommendation matrices
- default model settings
- heartbeat/scanner/briefing routes
- any config files that override the default

Typical tools:
```bash
rg -n "claude|anthropic|gpt|gemini|glm|kimi|nemotron|haiku|sonnet|opus" .
```

### 2) Normalize names
Make sure references use the intended canonical format everywhere.
Examples:
- vendor + model name should be consistent in docs
- alias spellings should be corrected
- recommendations should distinguish between "best for" guidance and actual runtime defaults

### 3) Update docs and recommendations
Edit the relevant docs so they reflect:
- current preferred models by task class
- any model-routing changes
- any normalization of model naming

Avoid changing unrelated archival content unless the task explicitly asks for repo-wide cleanup.

### 4) Apply the live change
Use the project’s real management command or config path to update the active default.
Examples:
- `sibling-agent models set <model>`
- edit the canonical config file used by the service
- restart or reload only if the system requires it

### 5) Verify
Confirm:
- the updated text appears in the expected docs
- the active/default model reflects the intended value
- no stale alias remains in the live recommendation surface

Suggested verification commands:
```bash
sibling-agent models status
rg -n "<old-model-name>" <affected-paths>
```

## Pitfalls
- A recommendation in prose is not the same as the live default.
- A model name can appear in multiple places: docs, prompts, config, archived reports, and scripts.
- Don’t assume a partial replacement is sufficient; verify the runtime state.
- Keep archival content untouched unless the user wants a repo-wide standardization pass.
- Cross-check the live config (`sibling-agent models status`) against the edited files before declaring the stack consistent.

## Related Skills
- `model-compliance-guard` for preventing paid-model cron failures
- `sibling-agent-fleet-analytics` for model distribution audits and fleet reporting
