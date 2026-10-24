---
name: honcho-memory-infrastructure
description: "Operate, monitor, and troubleshoot the Honcho deriver memory pipeline: launchd daemon management, LLM model switching (free vs paid based on OpenRouter credit status), watchdog automation, and log diagnosis."
version: 1.0.0
author: the operator agent Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [honcho, deriver, memory, infrastructure, launchd, openrouter, watchdog, daemon]
    trigger: "When Honcho deriver is down, OpenRouter credits are exhausted, memory pipeline errors appear, or when setting up/monitoring Honcho"
    related_skills: [hermes-memory-quality-audit, embedding-failover-system, gateway-startup-hooks]
---

# Honcho Memory Infrastructure

Operate and maintain the Honcho deriver — the background daemon that powers cross-session memory synthesis (peer profiles, deductive observations, dialectic reasoning). The deriver is the bridge between raw conversation observations and the synthesized user/peer model that gets injected into sessions.

## When to Use

- **Deriver health check**: User notices shallow recall, empty peer profiles, or stale observations
- **Credit exhaustion**: OpenRouter returns 402 Payment Required errors in deriver logs
- **Rate limiting**: Free-tier models returning 429 errors in deriver logs
- **Daemon stopped**: launchd shows deriver as not running after system restart
- **Model switching**: Need to switch between free and paid models based on credit availability
- **Setup/verification**: After Honcho installation, migration, or config changes

## Architecture

```
Honcho API Server (port 8000)     ← uvicorn, always-on
    ↕ PostgreSQL + pgvector
Honcho Deriver Daemon             ← background polling worker
    ↕ OpenRouter LLM API          ← gemini-2.5-flash (paid) or qwen:free
```

Two launchd services:
- `ai.honcho.api` — API server (uvicorn on port 8000)
- `ai.honcho.deriver` — Background deriver worker (polls for observation batches, calls LLM for synthesis)

**Key insight:** The API can be healthy while the deriver is dead. The API serves cached data; the deriver is what creates new synthesis. An empty peer profile with accumulated observations = deriver is not processing.

## Health Check Procedure

### Step 1: Check both processes
```bash
launchctl list | grep honcho
# Both should show a PID (number), not "-"
# If deriver shows "-" with exit code 0, it stopped cleanly and won't restart
```

### Step 2: Verify deriver is actually processing (not just alive)
```bash
# Check recent log activity — should see "Claimed" and "processing" lines
grep "$(date +%Y-%m-%d)" /<workspace> | tail -20

# Count errors by type
echo "429 rate limits: $(grep $(date +%Y-%m-%d) /<workspace> | grep -c '429')"
echo "402 payment:     $(grep $(date +%Y-%m-%d) /<workspace> | grep -c '402')"
```

**Alive ≠ processing.** A deriver stuck in a retry loop (all 3 attempts failing on 429/402) claims work units but never completes them. Check for `RetryError` and `RateLimitError` in logs.

### Step 3: Check OpenRouter credit status
```bash
source /<workspace>
curl -s "https://openrouter.ai/api/v1/key" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" | python3 -c "
import json,sys
d=json.load(sys.stdin).get('data',{})
print(f'Free tier: {d.get(\"is_free_tier\",\"?\")}')
print(f'Usage: {d.get(\"usage\",0)}')
print(f'Limit: {d.get(\"limit\",\"none\")}')
"
```

**Interpretation:**
- `is_free_tier: True` + `limit: None` = No prepaid balance. Paid models (gemini-2.5-flash) will return 402. Must use `:free` models.
- `limit` with remaining balance > 0 = Credits available. Can use paid models.

## Model Switching

The Honcho `.env` file (`/<workspace>`) configures 7 LLM models across the pipeline:

| Config Key | Purpose |
|-----------|---------|
| `DERIVER_MODEL_CONFIG__MODEL` | Observation synthesis (the core deriver LLM) |
| `SUMMARY_MODEL_CONFIG__MODEL` | Session summaries |
| `DIALECTIC_LEVELS__{minimal,low,medium,high,max}__MODEL_CONFIG__MODEL` | 5 dialectic reasoning levels |

Plus the embedding model (`EMBEDDING_MODEL_CONFIG__MODEL`), which is separate.

### Switch to free models (when credits exhausted)
Replace all model entries with a free model:
- **Recommended free model**: `qwen/qwen3-next-80b-a3b-instruct:free` (262K context, MoE)
- **Alternative**: `meta-llama/llama-3.3-70b-instruct:free` (131K context)

```bash
# All 7 LLM model lines need the same model name
# The embedding model (text-embedding-3-small) has no free alternative on OpenRouter
# Use local embedding failover instead (see embedding-failover-system skill)
```

### Switch back to paid models (when credits restored)
Replace all model entries with: `google/gemini-2.5-flash`

**Important:** The watchdog script automates this switching — see below.

### Restart after model changes
```bash
launchctl kickstart -k gui/$(id -u)/ai.honcho.deriver
# Or:
launchctl unload /<workspace>
launchctl load /<workspace>
```

## launchd Plist Configuration

### Critical: KeepAlive for polling daemons

The deriver plist (`~/Library/LaunchAgents/ai.honcho.deriver.plist`) MUST use unconditional KeepAlive:

```xml
<key>KeepAlive</key>
<true/>
```

**NEVER use** `KeepAlive.SuccessfulExit = false` for a polling daemon. This setting means "only restart if the process crashed (non-zero exit)." A daemon that receives SIGTERM during logout/restart exits cleanly (code 0) and will NEVER be restarted by launchd. The deriver was silently dead for 7 days because of this exact misconfiguration.

**Correct settings for the deriver plist:**
- `RunAtLoad = true` — start on system boot
- `KeepAlive = true` — unconditionally restart on ANY exit (clean or crash)
- `StandardOutPath` / `StandardErrorPath` — log to `<agent-home>/logs/honcho-deriver*.log`

## Watchdog Automation

An automated watchdog script monitors deriver health and credit status every 30 minutes via cron.

**Script:** `<agent-home>/scripts/honcho-deriver-watchdog.py`
**Cron:** Runs every 30 min (`*/30 * * * *`), `no_agent=True` (script-only, zero token cost)

### What the watchdog does:
1. **Checks deriver alive** → restarts automatically if down
2. **Checks OpenRouter credits** via API → detects free-tier vs paid balance
3. **Auto-switches models**: 
   - If free-tier + no balance + paid model configured → switches to free, restarts
   - If balance available + free model configured → switches back to paid, restarts
4. **Monitors error rates** (429/402 in last hour) → alerts if excessive
5. **Silent when healthy** — only outputs when action is needed or taken

### Adding the watchdog to a new installation
```bash
# Script is at <agent-home>/scripts/honcho-deriver-watchdog.py
# Create the cron job:
# Use cronjob action=create with no_agent=True, schedule='*/30 * * * *',
# script='honcho-deriver-watchdog.py', deliver='origin'
```

## Tiered Memory Architecture (2026-06-29)

The the operator agent persistent memory buffer (2,200 chars) is T0 only — identity, rules,
current priority. It must NOT hold project state, domain knowledge, or historical
decisions. Those overflow into T2.

| Tier | Function | Storage | Capacity |
|------|----------|---------|----------|
| T0 Active | User identity, comm style, standing rules, current priority | the operator agent 2,200 char buffer | ~10 entries |
| T1 Episodic | What happened in past sessions | Session search (FTS5) | Unlimited |
| T2 Semantic | Project state, domain knowledge, decisions | DS O'Keefe (:port) | Unlimited |
| T3 Procedural | How to do things (workflows) | Skills library | Unlimited |

### NEVER Destructively Delete Memories
The 2,200 char buffer fills up. The fix is NOT deleting important entries to
make room. The fix is routing T2 content to O'Keefe and keeping T0 lean.
Project state belongs in files/git/operator bus/O'Keefe, not the char buffer.

### DS O'Keefe Translation Layer (WORKING 2026-06-29)
O'Keefe (:port) stores memory traces as numeric vectors (trisynaptic circuit).
ALL endpoints now WORKING (fixed by sibling-agent 2026-06-29):
- `POST /encode` — accepts text + vector + tags + reward, returns trace_id
- `POST /retrieve` — pattern completion, returns memories WITH original text
- `GET /memories` — full listing with trace details
- `POST /consolidate` — sharp-wave ripple analog
- `GET /health` — reports memory_count + ec_dim (128)

The translation layer is BUILT AND PROVEN at `marketing-consortium/src/okeefe_bridge.py`:
- `store(text, tags, reward)` — embeds text via NVIDIA NIM, encodes to O'Keefe
- `recall(query)` — embeds query, retrieves matching memories with original text
- Uses NVIDIA NIM (nv-embed-v1, 4096-dim truncated to 128). NEVER Anthropic.
- Tested: stored "Marketing consortium v1.0.0..." fact, recalled it correctly via semantic query.

## Pitfalls

- **NEVER destructively delete memory entries to make room** — route T2 content to O'Keefe instead. Deleting important facts to fit the 2,200 char buffer is a protocol violation (user correction 2026-06-29).
- **NEVER use Anthropic for embeddings** — Gemini, OpenAI, NVIDIA NIM, local models all fine. The exclusion is Anthropic-specific, not provider-restrictive (user clarification 2026-06-29).
- **Alive ≠ processing**: A deriver stuck in a retry loop (all 3 LLM attempts failing) claims work units but never completes synthesis. Always check for `RetryError` / `RateLimitError` in logs, not just process existence.
- **Embedding model is separate from LLM models**: The deriver uses both an LLM (for synthesis) and an embedding model (for vectorization). Both go through OpenRouter. If the LLM is switched to free but the embedding model remains paid (`text-embedding-3-small`), embedding calls will fail with 402 once the LLM step succeeds. There is no free embedding model on OpenRouter — use local embedding failover (see `embedding-failover-system` skill).
- **Free models are heavily rate-limited**: Venice (upstream provider for OpenRouter free models) throttles aggressively. Expect 30-second retry-after delays and frequent 429s. The deriver retries 3x with backoff, but may exhaust retries on a single work unit. Throughput is significantly lower than paid models.
- **`DERIVER_STALE_SESSION_TIMEOUT_MINUTES`**: Sessions idle for this long (default 5 min) get processed. If the deriver was down, all sessions since the downtime are queued and will take time to process through the backlog.
- **SIGTERM during logout**: macOS sends SIGTERM to launchd jobs during logout/restart. A clean SIGTERM handler exits with code 0. With `KeepAlive.SuccessfulExit=false`, launchd treats this as intentional and does not restart. Always use unconditional `KeepAlive=true` for daemons that must survive reboots.
- **Log rotation**: The deriver error log can grow very large (84K+ lines observed). The log is at `<agent-home>/logs/honcho-deriver.error.log`. Consider periodic truncation if disk space is a concern.
- **Honcho fully dead but still configured as memory provider** — When Honcho has no process, no port, no data dir, but `memory.provider: honcho` remains in config.yaml, the agent queries it EVERY TURN for zero benefit. 58+ "Not Found" failures in 24h = ~1 wasted network round-trip per turn. The gateway log shows `WARNING ... Honcho session ... failed: Not Found` on every turn. Fix immediately: `hermes config set memory.provider ""` (disables external provider, falls back to built-in 2,200-char native memory buffer). Do NOT try to restart Honcho first — if the process, port, AND data dir are all gone, the infrastructure is dead. Disable the provider, then rebuild if needed. This is the absence of the Cannon/Vagus reflex: the organism needs to feel pain once, adapt, and stop. See operator bus handoff #947 for the circuit-breaker spec that would prevent this pattern systematically.

## Diagnostic Flow

```
Deriver health check
    │
    ├─ Process alive? ── NO ──→ Check plist KeepAlive setting → fix → restart
    │                              │
    │                              └─ Was it SIGTERM (clean exit)? → KeepAlive=true fix
    │
    ├─ Process alive ── YES ──→ Check log activity
    │                              │
    │                              ├─ 402 errors? ──→ Credits exhausted → switch to free models
    │                              │
    │                              ├─ 429 errors? ──→ Free model rate-limited → slower but functional
    │                              │                     (or add credits for paid model)
    │                              │
    │                              ├─ RetryError? ──→ LLM failing all 3 attempts → check model/credits
    │                              │
    │                              └─ "Completed" lines? ──→ Healthy, processing backlog
    │
    └─ Peer profile empty? ──→ Deriver not synthesizing → check above + deriver model config
```

## Reference Files

- `references/debugging-2026-06-19.md` — Real-world diagnosis of a deriver dead for 7 days: 3-layer root cause (plist KeepAlive bug, OpenRouter free-tier exhaustion, free-model rate limiting), exact log patterns, and fix sequence.

## Support Files

- `<agent-home>/scripts/honcho-deriver-watchdog.py` — Automated watchdog: monitors deriver health, OpenRouter credits, auto-switches models, restarts on failure. Deployed as no-agent cron every 30 min.
- `<agent-home>/logs/honcho-deriver.error.log` — Deriver stderr (main diagnostic log)
- `<agent-home>/logs/honcho-deriver.log` — Deriver stdout (summary/performance logs)
- `~/Library/LaunchAgents/ai.honcho.deriver.plist` — launchd service definition
- `/<workspace>` — Honcho configuration (model settings, API keys)
