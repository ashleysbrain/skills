# OpenRouter Idle Timeout in Gateway

**Created:** 2026-06-13
**Context:** principal-interface profile deployed, Telegram messages received, tools executed, but response synthesis hangs on OpenRouter idle timeout.

---

## The Issue

When Telegram messages route to principal-interface profile:
1. Gateway receives message ✅
2. Creates session with principal-interface profile ✅
3. Agent loads SOUL.md ✅
4. Agent analyzes intent, calls tools (terminal/curl) ✅
5. Tools return engine data ✅
6. **Agent tries to synthesize response → HANGS on OpenRouter idle timeout** ❌

Error in logs: `Upstream idle timeout exceeded` (provider=openrouter, model=nvidia/nemotron-3-ultra-550b-a55b:free)

---

## Root Cause

OpenRouter's free tier models have aggressive idle timeouts. The agent:
- Takes time to process tool results
- Builds response
- OpenRouter connection drops during synthesis

This is a **provider issue**, not a gateway/profile/engine issue.

---

## Workarounds

### Option 1: Switch principal-interface model (Recommended)
```bash
hermes -p principal-interface config set model.default "openrouter/google/gemini-2.5-flash"
# or
hermes -p principal-interface config set model.default "openrouter/deepseek/deepseek-r1:free"
# or
hermes -p principal-interface config set model.default "openrouter/z-ai/glm-4.5"
```

### Option 2: Use provider with better reliability
```bash
# In config.yaml, add provider for principal-interface profile
providers:
  llm-vendor:
    name: Z.ai
    base_url: https://api.z.ai/v1
    api_key: <zai_key>
```
Then set model to `llm-vendor/glm-4.5`

### Option 3: Reduce token overhead
- Limit tool output size in config
- Use fewer tool calls per turn
- Enable response caching: `openrouter.response_cache: true`

---

## Verification

Test locally before deploying to gateway:
```bash
cd <agent-home>/profiles/principal-interface
hermes chat -q "health check" -Q  # -Q = quiet mode
```

If local works but gateway times out → provider issue specific to gateway environment.

---

## Gateway Log Signature

```
WARNING [session_id] agent.conversation_loop: API call failed (attempt 1/3) 
error_type=APIError provider=openrouter base_url=https://openrouter.ai/api/v1 
model=nvidia/nemotron-3-ultra-550b-a55b:free summary=Upstream idle timeout exceeded
```

---

## Mitigation Pattern

For any the operator agent profile used in gateway:
1. **Avoid nemotron-3-ultra:free** for high-traffic gateway profiles
2. **Prefer gemini-2.5-flash, deepseek-r1:free, or glm-4.5** for reliability
3. **Test with `hermes chat -q "test" -Q`** before gateway deployment
4. **Monitor gateway.log for "Upstream idle timeout exceeded"**