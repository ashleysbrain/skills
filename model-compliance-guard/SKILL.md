---
name: model-compliance-guard
category: devops
description: Prevent cron job failures caused by using paid Anthropic models that return 402 Payment Required errors. Ensures all fleet jobs use free model alternatives.
---

# Model Compliance Guard

**Purpose**: Prevent cron job failures caused by using paid Anthropic models that return 402 Payment Required errors. Ensures all fleet jobs use free model alternatives.

## The Problem

Any paid model causes failures when credits/quotas are exhausted. This is NOT limited to Anthropic — OpenRouter credits drying up causes HTTP 402 ("insufficient credits") and HTTP 403 ("key limit exceeded") on ALL paid models including `google/gemini-2.5-pro`, `deepseek/deepseek-r1-0528`, and `google/gemini-2.5-flash`. The symptom is hundreds of credential exhaustion warnings followed by hard API failures. Cron jobs report `last_status: ok` because the wrapper succeeds, but the actual work inside fails silently or falls through to weaker fallbacks.

**Real incident (2026-05-27/28):** 13,227 error lines over weeks. 684 credential exhaustion warnings. 170 hard failures on gemini-2.5-pro. 48 context compression failures. All from OpenRouter credit exhaustion. The cron dashboard showed green because the runner doesn't flag failed API calls as job failures.

## The Solution

**ALL cron jobs should use free-tier models.** Period. No paid models in any cron job.

**Provider failover trap (2026-07-06):** When a job's primary provider fails
(e.g., google-gemini-cli), the the operator agent cron runtime can silently fall back to
OpenRouter. If OpenRouter credits are depleted, the job dies with HTTP 402.
This is invisible — the job shows `last_status: error` but the error message
mentions OpenRouter, not the configured provider, which is confusing.

**Prevention for repair agents:** Pin repair/fixer agents to `llm-vendor-glm`
(LLM-5.2) specifically — different provider pool from both google-gemini-cli
AND OpenRouter. This breaks the failover chain entirely. The Corpus Fixer
Agent cron is pinned to llm-vendor-glm for exactly this reason.

Current free model ranking (from `<agent-home>/openrouter-free-models.json`):
1. `nvidia/nemotron-3-super-120b-a12b:free` — score 92, 1M context (best overall)
2. `deepseek/deepseek-v4-flash:free` — score 74, 1M context (best for reasoning/audit)
3. `qwen/qwen3-coder:free` — score 69, 1M context

Model-to-free-tier mapping:
- **gemini-2.5-pro** → `nvidia/nemotron-3-super-120b-a12b:free`
- **deepseek-r1-0528** → `deepseek/deepseek-v4-flash:free`
- **gemini-2.5-flash** → `nvidia/nemotron-3-super-120b-a12b:free`
- **Haiku/Sonnet/Opus** → `nvidia/nemotron-3-super-120b-a12b:free`

## Compliance Script

Location: `<agent-home>/scripts/model-compliance-check.py`

**Usage:**
```bash
# Check only (no changes)
python3 <agent-home>/scripts/model-compliance-check.py

# Auto-fix non-compliant jobs
python3 <agent-home>/scripts/model-compliance-check.py --fix
```

**What it does:**
1. Fetches all cron jobs via `sibling-agent cron list --json`
2. Checks each job's payload.model for blocked keywords (anthropic, claude, openai/gpt)
3. Reports or auto-fixes jobs using non-compliant models
4. Maps old models to approved free alternatives

## Blocked Models

Never use these in cron jobs (all cause 402/403 when credits dry up):
- `anthropic/claude-*` (all versions)
- `openai/gpt-*` (all versions)
- `amazon/q-*` (all versions)
- `google/gemini-2.5-pro` (paid, causes HTTP 402 on OpenRouter)
- `google/gemini-2.5-flash` (paid on OpenRouter)
- `deepseek/deepseek-r1-0528` (paid, causes HTTP 403 key limit)
- Any model WITHOUT `:free` suffix on OpenRouter

## Approved Free Models (ALL cron jobs MUST use one of these)

**Standard tier (most jobs):**
- `nvidia/nemotron-3-super-120b-a12b:free` — quality score 92, 1M context

**Reasoning/audit tier:**
- `deepseek/deepseek-v4-flash:free` — quality score 74, 1M context, good for reasoning-heavy work

**Check current rankings:** `cat <agent-home>/openrouter-free-models.json | python3 -c "import sys,json; d=json.load(sys.stdin); [print(f'{i+1}. {m[\"id\"]} score:{m[\"quality_score\"]}') for i,m in enumerate(d['ranked_models'][:10])]"`

## Update Existing Jobs

To update individual jobs:
```bash
sibling-agent cron edit <job-id> --model <new-model>
```

To bulk update (use the compliance script):
```bash
python3 <agent-home>/scripts/model-compliance-check.py --fix
```

## Prevention

**Daily cron job**: `Daily Model Compliance Check` runs at 5 AM daily
- Automatically detects and fixes any jobs using non-compliant models
- Reports summary to origin chat

**When creating new jobs**: Always use free models WITH the `openrouter/` prefix and `:free` suffix:
```bash
# WRONG (will fail with 402 or allowlist rejection):
sibling-agent cron add "Job Name" --model anthropic/claude-haiku-4-5
sibling-agent cron add "Job Name" --model google/gemini-2.5-flash

# CORRECT (passes allowlist + free tier):
sibling-agent cron add "Job Name" --model openrouter/nvidia/nemotron-3-super-120b-a12b:free
sibling-agent cron add "Job Name" --model openrouter/qwen/qwen3-next-80b-a3b-instruct:free
```

## Agent Profile Requirements

**FORGE** (Chief Agent Architect) must enforce:
- All new cron jobs use compliant free models
- Model tier matches task complexity
- Monthly review of job model assignments

**NEXUS** (Chief Automation Officer) must:
- Auto-remediate any jobs hitting rate limits on paid models
- Redistribute load if single model has > 40 active jobs

## Verification

After any bulk changes, verify:
```bash
python3 <agent-home>/scripts/model-compliance-check.py
```

Should return: `✓ All cron jobs are using compliant free models`

**Important:** A prompt or log mentioning `anthropic` does not necessarily mean the job is still assigned to Anthropic. Only the job's actual `model` / `payload.model` field counts for compliance. If the gateway is unavailable, use the cached cron export or local job files to audit; do not assume failures from stale prompt text alone.

## Troubleshooting

If the compliance check times out when fetching cron jobs:
1. Check if the sibling-agent service is running: `sibling-agent ping`
2. If the service is overloaded, increase the timeout in the script or run during off-peak hours.
3. You can also run the check without the `--fix` flag first to see if it's a temporary issue.
4. For very large fleets, consider running the check more frequently with a subset of jobs or adjusting the sibling-agent service.

## Incident Response

If 402 errors occur or an Anthropic model is found in a job assignment:
1. Run compliance check with auto-fix: `python3 <agent-home>/scripts/model-compliance-check.py --fix`
2. Verify fleet health: Check `sibling-agent cron list` for error status
3. Update any jobs that failed to fix
4. If the gateway is down, collect diagnostics and queue the model change for when it returns; don't treat prompt-only Anthropic mentions as active violations
5. Document in incident log

## Memory Rules

**Save to memory:**
- "NEVER use Anthropic/Claude models in cron jobs - causes 402 errors"
- "Use compliance script: python3 <agent-home>/scripts/model-compliance-check.py --fix"
- "Daily compliance check runs at 5 AM via cron job 'Daily Model Compliance Check'"

**User preference:**
- "Execute NOW, never ask. /approve=always"
- "ADHD tiny-steps: minimize choice menus"
- "Alkaline water. AG1 daily"
