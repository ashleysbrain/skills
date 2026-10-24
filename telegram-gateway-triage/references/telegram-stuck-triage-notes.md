# Telegram Stuck Triage Notes

## What to look for first

When a user says Telegram is stuck, not working, or the assistant is behaving oddly in chat, start by determining whether this is:

- **transport / routing**: message never arrived, wrong thread, wrong target, allowlist/path issue
- **content / interaction**: answer was too abstract, too verbose, or responded to the wrong thing
- **conversation-state drift**: the assistant replied to stale context, the wrong user ask, or the wrong turn in the thread

Do not treat these as the same problem.

## Fast first response pattern

Use a short reply that asks for the last reliable signal:

- "Tell me the last message that successfully went through, and I’ll separate delivery from content."
- "What’s the last concrete symptom you saw: no reply, wrong thread, or a bad answer?"

If the user says the chat is stuck but the transport looks fine, compare:
1. the latest user message
2. the immediately prior assistant turn

That usually tells you whether the failure is routing or stale-context drift.

## Practical recovery sequence

1. Confirm the intended target: home chat, specific chat ID, or thread/topic.
2. Ask for the last message that succeeded.
3. Check whether the assistant is answering the actual latest ask or a stale thread context.
4. Decide whether to inspect routing or tighten the response style.
5. Only claim success after the path is verified.

## Pitfall to avoid

- Don’t answer a routing complaint with a generic status essay.
- Don’t pivot into unrelated work before the chat path is understood.
- Don’t say the chat is fixed unless delivery has actually been confirmed.
- Don’t mistake "the assistant answered the wrong thing" for "Telegram is broken" without checking the last user/assistant pair.
- Session note: when a user says "my telegram is stuck and not working with you correctly," treat that as a signal to reset to the latest message and avoid continuing any unrelated task thread.

## Latency triage (user reports "too slow to respond")

When the complaint is SLOWNESS rather than delivery failure, the gateway is
alive and Telegram is connected, but responses take minutes instead of
seconds. Check these in order:

1. **Response time distribution in gateway.log.** Grep for `response ready`
   lines and look at the `time=` values:
   ```bash
   grep "response ready" <agent-home>/logs/gateway.log | tail -20
   ```
   p50 over 120s or p90 over 600s indicates a systemic bottleneck, not a
   one-off slow model call.

2. **Dead memory provider tax.** If `memory.provider` is set to a provider
   that is offline (no process, no port, no data directory), the agent
   retries it every turn for zero benefit. Each failed call adds a network
   round-trip of latency. Check:
   ```bash
   grep -i "Not Found\|connection refused\|memory.*provider.*fail" <agent-home>/logs/gateway.log | tail -20
   ```
   Fix: `hermes config set memory.provider ""` then `hermes gateway restart`.
   The native memory tool (configurable char buffer) still works without an
   external provider.

3. **Crashing subsystems mid-turn.** A tool or subsystem that crashes
   mid-execution forces an API retry, compounding latency. Check:
   ```bash
   grep "RuntimeError\|Traceback" <agent-home>/logs/gateway.error.log | tail -20
   ```
   Each crash is a micro-infarction bleeding latency into every tool-heavy
   turn. The fix belongs to sibling-agent (core surgery), not the triage skill.

4. **Subagent stream interruptions.** Look for `Stream interrupted by
   network error` warnings — these cause the agent to re-dispatch, adding
   the full subagent latency on top of the retry.
