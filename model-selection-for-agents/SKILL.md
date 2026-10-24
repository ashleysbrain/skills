---
name: Model Selection for AI Agents
description: Select optimal AI models (Opus/Sonnet/Haiku, Z.ai LLM, OpenRouter free pool) for agent tasks based on cognitive complexity and strategic importance
tags: [agents, cost-optimization, model-selection, strategic-thinking, llm-vendor, openrouter]
tools: [terminal, file]
---

## ASHLEY DIRECTIVE — NO ANTHROPIC MODELS EVER

Per the principal's directive (2026-04-08, repeated): **NEVER use Anthropic/Claude models anywhere in the principal's fleet, cron jobs, main session, or subagents.** Not opus, not sonnet, not haiku. Not via direct provider, not via OpenRouter's `anthropic/` namespace.

**Primary model for all work:** `google/gemini-3.1-pro-preview` (via OpenRouter)
**Lighter tier for simple/mechanical work:** `google/gemini-3.1-flash-lite-preview` (via OpenRouter)
**Alternative elite tier:** `z-ai/glm-5.1` (via llm-vendor), `z-ai/glm-5v-turbo` (multimodal, via llm-vendor), openai via openai-codex
**Fallback chain:** gemini-3.1-pro-preview → glm-5.1 → gemini-3.1-flash-lite-preview

When auditing config, cron jobs, or subagent routing, grep for `anthropic`, `claude`, `opus`, `sonnet`, `haiku` and replace all hits with non-Anthropic equivalents. This includes main session `model.default`, `fallback_providers`, `delegation.model`, cron job model fields, and any in-prompt model references.

## When to Use

- Evaluating model tier for new agents
- Reviewing existing agent model assignments
- FIN phase of fleet optimization
- Agent experiencing quality issues
- Cost optimization without quality loss
- Model/rate-limit failover decisions

## Core Principle

**High-level strategic thinking and in-depth research reviews require Opus. Everything else uses Z.ai, free models, or cheaper tiers.**

Use Opus LESS aggressively than before. Free quality-ranked models (S-Tier: qwen3.6-plus-preview:free, nemotron-3-super, step-3.5-flash) are capable enough for most operational, research-scan, and medium-complexity tasks. Default to free S/A-tier before paid Sonnet/Haiku unless quality demands it.

Quality optimization > cost optimization, but free S/A-tier models ARE quality models — don't assume "free" means "bad."

## Decision Framework

### Opus Required For:
1. **Executive roles** - principal, CTO, CPO, CSO, CFO, COO agents
2. **High-level strategic thinking** - Priority decisions, product strategy, business direction
3. **In-depth research reviews** - Multi-document gap analysis, methodology design
4. **Cross-domain synthesis** - Finding novel connections across research domains
5. **Novel framework creation** - New methodology, original research, product architecture
6. **Research-to-product translation** - Understanding implications AND architecture

### Sonnet Appropriate For:
1. **Quality-critical but defined tasks** - Report generation with established templates
2. **Single-domain research** - Deep but bounded analysis
3. **Moderate complexity** - Analysis + writing, no novel reasoning
4. **Product updates** - Applying research to existing schemas

### Haiku Appropriate For:
1. **Simple operational tasks** - Status checks, file operations
2. **High-frequency monitoring** - Health checks, threshold monitoring
3. **Low cognitive load** - Counting, listing, simple notifications

### Flash (google/gemini-2.5-flash) — NEW TIER (added 2026-03-28):
1. **Research domain scans** - All 23 daily literature scans (AI/ML, Bioethics, Sleep Science, etc.)
2. **Data pulls and backups** - Linear backup, HealthKit pull, repo audits
3. **Monitoring/watchdog tasks** - URL watching, capacity checks, process freshness
4. **Journaling enforcement** - Compliance checks, indexing
Cost: ~$0.15/$0.60 per 1M tokens (10-20x cheaper than Sonnet)

### LLM (llm-vendor/glm-5) — Alternative for overnight batch:
1. **Overnight batch processing** - Dream cycle, analytics refresh, self-optimization
2. **Non-latency-sensitive tasks** - Can be slow but reliable
Cost: ~$1.00/$4.00 per 1M tokens

### Z.ai Coding Plan (Added 2026-04-01):
**Direct Z.ai API** — NOT via OpenRouter
- Base URL: `https://api.z.ai/api/coding/paas/v4`
- API Key: `GLM_API_KEY` in `<agent-home>/.env`
- Models: `z-ai/glm-5.1` (primary, latest), `z-ai/glm-5v-turbo` (multimodal), `z-ai/glm-5-turbo`, `z-ai/glm-5`
- Context lengths: LLM-5.1/LLM-5V/LLM-5-Turbo = 202K tokens, LLM-5 = 80K tokens
- Higher rate limits, optimized for coding scenarios
- Use for: Coding tasks, agent orchestration, complex multi-step reasoning, vision-based coding
- **Never downgrade strategic agents off Z.ai coding plan to free models**

### OpenRouter Free Pool (Added 2026-04-01):
**Unlimited fallback** — Any model with prompt=$0 pricing
- Models change frequently. Check live with API call (see "Live Model Discovery" above)
- Current top free models include Gemma 4, Nemotron 3, Qwen3, MiniMax M2.5, Trinity
- Cached at: `<agent-home>/openrouter-free-models.json` (may be stale - refresh via API)
- Use for: Fallback when rate-limited, low-priority tasks, testing, high-frequency polling
- Failover: On 429/503/529, INSTANTLY switch to next free model. NEVER retry, NEVER ask

## Cognitive Complexity Scoring

Score 0-10 for each:
1. **Strategic Reasoning** - principal-level decisions, priority-setting
2. **Research Synthesis** - Novel connections across domains
3. **Analytical Depth** - Multi-document gap analysis

**Formula:**
```
Cognitive Score = (Strategic × 4 + Synthesis × 4 + Depth × 3) / 1.25
+ 10 if multi-domain
+ 10 if novel output
+ 15 if executive impact
```

**Thresholds:**
- 70-100: Opus required
- 40-69: Sonnet (monitor quality)
- 20-39: Haiku
- 0-19: LLM (if high-frequency)

## Tools

### Live Model Discovery
OpenRouter's model catalog changes frequently. To get current models directly:

```bash
# List all available models
curl -s https://openrouter.ai/api/v1/models | python3 -c "import sys, json; data = json.load(sys.stdin); print('\n'.join([f\"{m['id']}: {m['name']}\" for m in data['data'][:20]]))"

# Filter by provider (e.g., Google Gemini models)
curl -s https://openrouter.ai/api/v1/models | python3 -c "import sys, json; data = json.load(sys.stdin); models = [m for m in data['data'] if 'gemini' in m['id'].lower()]; print('\n'.join([f\"{m['id']}: {m['name']} (ctx: {m['context_length']})\" for m in models]))"

# Filter by provider (e.g., LLM models)
curl -s https://openrouter.ai/api/v1/models | python3 -c "import sys, json; data = json.load(sys.stdin); models = [m for m in data['data'] if 'glm' in m['id'].lower()]; print('\n'.join([f\"{m['id']}: {m['name']} (ctx: {m['context_length']})\" for m in models]))"
```

Use this when model lists in configuration or skills appear outdated.

**Automated evaluation:**
```bash
cd ~/your-workspace/hydra-os
python3 scripts/model-selector.py audit \
  --agent "AGENT NAME" \
  --role "ROLE" \
  --current-model "current-model" \
  --task "TASK DESCRIPTION"
```

**Output includes:**
- Recommended model with confidence %
- Cognitive complexity score
- Justification
- Cost impact
- Alternatives with tradeoffs

## Never Downgrade List

These agents ALWAYS stay on Opus:

**Executive Layer:**
- SINGULARITY (all variants)
- NEBULA (strategic crons)
- FORGE (strategic crons)
- AURORA (strategic crons)

**Research Intelligence:**
- VITALS 8D Product Review
- Panel Orchestrator
- Weekly Rotating Expert Review
- Research Intelligence Self-Optimization
- AISHA Weekly Goal & Schedule Review

**Moved OFF Opus (2026-03-28 GENESIS FIN audit):**
- ATLAS-R2P → Flash (was doing scan/pull work, not executive synthesis)
- HORIZON Research Synthesis → Haiku (synthesis of existing data, not novel reasoning)

**Methodology Design:**
- AETHER Framework Research
- HALO Human Wellness Research
- Any "methodology" or "framework" agents

## Implementation Steps

### 1. Audit Current Assignment
```bash
# Get current model
sibling-agent cron list | grep "AGENT_NAME"

# Evaluate task
python3 scripts/model-selector.py audit \
  --agent "AGENT_NAME" \
  --role "ROLE" \
  --current-model "CURRENT" \
  --task "DETAILED TASK DESCRIPTION"
```

### 2. Make Decision

**If cognitive score >70 or on Never Downgrade List:**
→ Opus (no exceptions)

**If user directive applies:**
→ Follow directive (the principal's assessment > agent scores)

**If cost optimization candidate:**
→ Test quality for 3 runs before committing

### 3. Update Agent

```bash
sibling-agent cron edit AGENT_ID --model "anthropic/claude-opus-4-6"
# or
sibling-agent cron edit AGENT_ID --model "anthropic/claude-sonnet-4-6"
```

### 4. Monitor Post-Change

For any Opus→Sonnet migration:
- Track output quality for 3 runs
- Compare depth vs previous outputs
- Revert immediately if quality drops

## Common Mistakes

❌ **Don't:**
- Downgrade strategic agents for cost savings
- Use agent panel scores as sole quality measure
- Batch-migrate without task-level evaluation
- Prioritize cost over quality for executive agents

✅ **Do:**
- Evaluate task cognitive requirements first
- Respect "Never Downgrade List"
- Monitor quality post-migration
- Document justification for each change

## the principal's Directive

> "We need to use Opus for high-level thinking roles and tasks. Don't move everyone off of Opus just to save money. Consider who we're moving, which agents, and keep agents that need Opus for high-level thinking. Research requiring in-depth reviews needs Opus."

Translation:
- Strategic thinking > cost savings
- Task-by-task evaluation required
- High-level roles stay on Opus
- Research depth needs Opus

## Example Evaluations

### ✅ Correct: SINGULARITY Always-On → Opus
- Role: principal Authority
- Task: Strategic pulse, collaboration audit, priority decisions
- Cognitive Score: 85/100
- Justification: principal-level decision-making about fleet direction

### ✅ Correct: ATLAS Neuroscience → Sonnet
- Role: Domain Scanner
- Task: Daily research scan, extract insights
- Cognitive Score: 55/100
- Justification: Deep but single-domain, Sonnet with 1200s timeout = 5/5 quality

### ✅ Correct: HORIZON Synthesis → Haiku (revised 2026-03-28)
- Role: Research Synthesis (daily digest of domain reports)
- Task: Aggregate existing research scans into summary
- Cognitive Score: 35/100 (aggregation, not novel reasoning)
- Justification: Collates pre-existing domain scan outputs; no novel cross-domain discovery. Haiku handles this adequately. Was on Opus ($29/mo waste).
- Key distinction: "synthesis of existing reports" ≠ "novel cross-domain reasoning"

### ❌ Incorrect: Moving SINGULARITY principal Pulse → Haiku
- Role: principal Authority
- Task: Strategic decisions, fleet coordination, priority-setting
- Cognitive Score: 85/100
- Why Wrong: principal-level decision-making requires advanced reasoning
- Correct: Sonnet minimum, Opus for 2-hour strategic pulse

## Integration with GENESIS Sprint

**Phase 8 (FIN) requirements:**

Before any Opus downgrade:
1. Run model-selector.py audit
2. Check cognitive score (>70 = flag for approval)
3. Check Never Downgrade List
4. Document justification

Post-migration:
1. Monitor quality for 3 runs
2. Document in OVERNIGHT-CHANGELOG with [FIN] tag
3. Revert if quality issues

## Cost vs Quality Tradeoffs

**When to optimize cost:**
- Cognitive score <40
- High-frequency operational tasks
- Non-quality-critical output
- Easily reversible

**When to prioritize quality:**
- Cognitive score >70
- Executive-impact decisions
- Research-grade output
- Methodology/framework design
- Cross-domain synthesis

## Free Model Quality Scoring Algorithm (2026-04-01)

Don't hardcode which free models to use. OpenRouter's free pool changes constantly — models get added, removed, or lose free status. Instead, score every free model 0-100 dynamically:

```python
def quality_score(m):
    score = 0
    # Recency (0-30 pts): newer ~ generally better
    age_days = (now - m["created"]) / 86400
    if age_days < 30: score += 30
    elif age_days < 90: score += 25
    elif age_days < 180: score += 18
    elif age_days < 365: score += 12
    else: score += 5

    # Context length (0-20 pts)
    ctx = m["context_length"]
    if ctx >= 500000: score += 20
    elif ctx >= 200000: score += 15
    elif ctx >= 100000: score += 10
    elif ctx >= 50000: score += 5

    # Max completion tokens (0-15 pts)
    max_tok = m["top_provider"]["max_completion_tokens"]
    if max_tok >= 100000: score += 15
    elif max_tok >= 32000: score += 10
    elif max_tok >= 8192: score += 5
    elif max_tok is None: score += 5  # possibly unlimited

    # Agent capabilities (0-20 pts)
    params = m["supported_parameters"]
    if "tools" in params: score += 8
    if "structured_outputs" in params: score += 6
    if "reasoning" in params: score += 6

    # Model family tier boost (0-15 pts)
    # Known high-performers: gemma-4(15), qwen3.6(14), nemotron-3(12),
    # minimax-m2.5(12), trinity-large(11), qwen3-next(11), glm-4.5(11), etc.
    # Add ~5-15 based on known quality of the model family
```

- Filter out non text→text models (music, image, video-only)
- Query live API for current free models (see "Live Model Discovery" section)
- Always start fallback with the highest-scoring available model
- Rotate down the ranked list on rate limit — never retry failed model

## Z.ai Coding Plan Setup Notes (2026-04-01)

**Two Z.ai platforms exist:**
- International: `https://api.z.ai/api/coding/paas/v4` — uses `llm-vendor-` prefixed keys
- Chinese: `https://open.bigmodel.cn/api/paas/v4` — 32-hex-char API keys

If a key keeps returning 401 on all endpoints and auth formats:
- It may be expired/revoked — regenerate from dashboard
- Wrong platform — z.ai keys don't work on bigmodel.cn and vice versa
- Key may need activation — check subscription status

**Auth formats tested (all standard Bearer):**
- `Authorization: Bearer {key}` (correct format)
- `api-key: {key}` (rejected, needs Authorization header)
- `x-api-key: {key}` (same 401 as Bearer)

## Model Failover Architecture (2026-04-01)

**Routing:** Z.ai Coding Plan → OpenRouter Free Pool
- Primary: `https://api.z.ai/api/coding/paas/v4` (ZAI_API_KEY / GLM_API_KEY)
- Fallback: `https://openrouter.ai/api/v1` (OPENROUTER_API_KEY)
- Failover codes: 429, 503, 529, 502, 504
- Rule: On any failover code → instantly switch to next provider/model. Zero retries. Zero delays.
- Script: `<agent-home>/model-failover.py`
- Free models cache: `<agent-home>/openrouter-free-models.json` (refreshed every 6h)

## Files Created

1. `~/your-workspace/hydra-os/scripts/model-selector.py` - Automated tool
2. `~/your-workspace/hydra-os/processes/operations/MODEL-SELECTION-PROTOCOL.md` - Full framework
3. `<agent-home>/model-failover.py` - Model failover orchestration
4. `<agent-home>/openrouter-free-models.json` - Cached free models list

---

**Summary:** Evaluate cognitive complexity of tasks, not just mechanical steps. Use latest models (Gemini 3.1, LLM 5.1) — check OpenRouter API live when lists appear stale. Z.ai coding plan for primary coding/agent work with LLM-5.1 and LLM-5V-Turbo. OpenRouter free pool as unlimited fallback, auto-rotating on any rate limit.