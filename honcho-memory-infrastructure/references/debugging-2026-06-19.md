# Honcho Deriver Debugging — June 19, 2026 Session

Real-world diagnosis of a deriver that had been silently dead for 7 days. Documents the exact symptoms, log patterns, and fix sequence.

## Symptom

- Peer profile (`honcho_profile`) was empty despite ~80 observations accumulated
- Observation dump in memory context was noisy (completed-work logs, panel rubric fragments)
- No synthesis or deductive observations were being produced

## Root Cause (3 layers)

### Layer 1: launchd plist misconfiguration

The deriver plist had:
```xml
<key>KeepAlive</key>
<dict>
  <key>SuccessfulExit</key>
  <false/>
</dict>
```

This means: "restart ONLY if the process exits with non-zero status." The deriver received SIGTERM during logout (normal macOS behavior), its signal handler shut down cleanly (exit code 0), and launchd never restarted it.

**Log evidence:** The last log entry before the 7-day gap:
```
2026-06-12 13:01:59,887 - src.deriver.queue_manager - INFO - Received exit signal SIGTERM...
2026-06-12 13:02:22,932 - __main__ - INFO - Deriver process exiting
```

launchctl status showed:
```
-    0    ai.honcho.deriver
```
PID `-` = not running. Exit code `0` = clean exit. `KeepAlive.SuccessfulExit=false` = don't restart.

**Fix:** Changed to `<key>KeepAlive</key><true/>` (unconditional restart).

### Layer 2: OpenRouter free-tier with no balance

After restarting the deriver, it immediately hit 402 errors:
```
2026-06-19 06:43:19,084 - src.llm.api - WARNING - Error on attempt 1/3 with openai/google/gemini-2.5-flash: Error code: 402 - {'error': {'message': 'This request requires more credits, or fewer max_tokens. You requested up to 2500 tokens, but can only afford 0. To increase, visit https://openrouter.ai/settings/credits'}}
```

OpenRouter API key check revealed:
```json
{
  "is_free_tier": true,
  "usage": 0.199716962,
  "limit": null
}
```

`is_free_tier: true` + `limit: null` = No prepaid balance. All paid model calls return 402.

**Fix:** Switched all 7 Honcho LLM models from `google/gemini-2.5-flash` to `qwen/qwen3-next-80b-a3b-instruct:free`.

### Layer 3: Free model rate limiting

After switching to the free model, the deriver started processing but hit 429 rate limits:
```
2026-06-19 08:12:28,364 - src.llm.api - WARNING - Error on attempt 1/3 with openai/qwen/qwen3-next-80b-a3b-instruct:free: Error code: 429 - {'error': {'message': 'qwen/qwen3-next-80b-a3b-instruct:free is temporarily rate-limited upstream. Please retry shortly', 'retry_after_seconds': 30}}
```

56 rate-limit errors in one hour. The deriver retries 3x with 30-second backoff, but many work units exhaust all retries:
```
2026-06-19 08:02:28,766 - src.deriver.queue_manager - ERROR - Error processing representation batch: RetryError[<Future state=finished raised RateLimitError>]
```

**Status:** Functional but slow. Free-tier tradeoff: no cost, but significantly lower throughput.

## Additional Finding: Pre-existing empty summaries

Before the deriver died (June 12), it was producing 0-token summaries:
```
╭─────────────────── PERFORMANCE - summary_hermes_1167 ─────────────────╮
│   Short Summary Size                            0  tokens             │
│   Short Summary Creation                     8211  ms                │
╰───────────────────────────────────────────────────────────────────────╯
```

This suggests the gemini-2.5-flash model was already returning empty responses before the credit exhaustion became total. Likely a gradual credit depletion issue.

## Fix Sequence Applied

1. Backed up MEMORY.md and USER.md
2. Fixed plist: `KeepAlive.SuccessfulExit=false` → `KeepAlive=true`
3. Reloaded plist: `launchctl unload && launchctl load`
4. Verified deriver started (PID assigned, logs flowing)
5. Identified 402 errors → checked OpenRouter API → confirmed free-tier with no balance
6. Switched all 7 LLM models to `qwen/qwen3-next-80b-a3b-instruct:free` in `/<workspace>`
7. Restarted deriver again
8. Verified processing started (claiming work units, hitting 429 but retrying)
9. Built watchdog script (`<agent-home>/scripts/honcho-deriver-watchdog.py`)
10. Deployed watchdog as no-agent cron every 30 minutes

## Model Switching Details

### All 7 LLM config keys that need changing:
```
DERIVER_MODEL_CONFIG__MODEL
SUMMARY_MODEL_CONFIG__MODEL
DIALECTIC_LEVELS__minimal__MODEL_CONFIG__MODEL
DIALECTIC_LEVELS__low__MODEL_CONFIG__MODEL
DIALECTIC_LEVELS__medium__MODEL_CONFIG__MODEL
DIALECTIC_LEVELS__high__MODEL_CONFIG__MODEL
DIALECTIC_LEVELS__max__MODEL_CONFIG__MODEL
```

### Embedding model (separate concern):
```
EMBEDDING_MODEL_CONFIG__MODEL = text-embedding-3-small
```
This is paid and has no free alternative on OpenRouter. If the deriver gets past the LLM step (synthesis) and reaches the embedding step (vectorization), this will also fail with 402. Use local embedding failover (`embedding-failover-system` skill) as an alternative.

## Watchdog Design Rationale

The watchdog uses `no_agent=True` (script-only cron) because:
- Zero token cost — runs Python directly, no LLM calls
- Fast — completes in <5 seconds when healthy
- Silent when healthy — empty stdout = no notification sent
- Non-empty stdout = alert delivered to origin chat
- Non-zero exit = critical failure requiring human intervention

The auto-switch-back logic: when the watchdog detects `limit > 0` and `(limit - usage) > 0` on OpenRouter, it switches all models back to paid (`gemini-2.5-flash`) and restarts the deriver. This means adding credits to OpenRouter is the only action needed to restore full-speed operation.
