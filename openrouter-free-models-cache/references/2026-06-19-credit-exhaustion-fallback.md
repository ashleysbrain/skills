# 2026-06-19: Honcho Deriver Credit Exhaustion + launchd Downtime Incident

## Symptom
Honcho peer profile conclusions stopped being synthesized. Raw observations accumulated but remained unevaluated. No dialectic output for ~7 days.

## Root Causes (two-layer)

### Layer 1: launchd KeepAlive Bug
The deriver's launchd plist had `KeepAlive.SuccessfulExit = false`, which means "only restart if the process exits with non-zero status." The deriver received a SIGTERM during system logout on 2026-06-12 13:01:59, shut down cleanly (exit 0), and launchd **never restarted it**.

**Fix**: Changed plist to unconditional `KeepAlive = true`:
```xml
<key>KeepAlive</key><true/>
```
Then: `launchctl unload <plist> && launchctl load <plist>`

### Layer 2: OpenRouter Credits Exhausted (402)
After restarting the deriver, it immediately hit `402 Payment Required` — the OpenRouter account had 0 credits. The deriver's model (`google/gemini-2.5-flash`) couldn't afford even 2500 tokens.

This was also the pre-existing cause of empty summaries: the deriver had been producing `Short Summary Size: 0 tokens` for days before it died — silent LLM failures that didn't crash the process.

**Fix**: Switched all 7 LLM model references in `/<workspace>` from `google/gemini-2.5-flash` to `qwen/qwen3-next-80b-a3b-instruct:free`:
```bash
sed -i '' 's|google/gemini-2.5-flash|qwen/qwen3-next-80b-a3b-instruct:free|g' /<workspace>
launchctl stop ai.honcho.deriver && launchctl start ai.honcho.deriver
```

## Free Model Behavior
Both `meta-llama/llama-3.3-70b-instruct:free` and `qwen/qwen3-next-80b-a3b-instruct:free` route through Venice on OpenRouter's free tier. They hit 429 rate limits under load but retry successfully (3 attempts with 30s backoff). Processing is slower but functional — the deriver successfully processed the 7-day backlog.

## Monitoring Setup
Created `/<workspace>` (adapted version in `scripts/openrouter-credit-health-check.sh`) and scheduled it as a cron watchdog every 4 hours. The script:
- Checks deriver process + Honcho API health
- Tests OpenRouter with current model (detects 402)
- If on free model, tests paid model to detect credit restoration → outputs exact switch-back command
- Monitors log error patterns
- Silent when healthy (watchdog pattern)

## Key Lessons
1. **`KeepAlive.SuccessfulExit = false` is wrong for polling daemons.** Clean exits (SIGTERM during logout) won't be restarted. Use `KeepAlive = true`.
2. **402 ≠ 429.** Rate limits (429) are temporary; credit exhaustion (402) persists until funds added. Different response needed.
3. **Empty/zero-token outputs are a silent 402 symptom.** The LLM call fails but the process doesn't crash. Check logs for 402 when quality degrades before a service dies.
4. **the operator agent (z.ai/LLM) was unaffected** because it uses z.ai as primary provider, not OpenRouter. OpenRouter is only a fallback for the operator agent. But Honcho is 100% OpenRouter-dependent.
