---
name: telegram-gateway-triage
description: Triage Telegram chat and delivery issues so the operator agent can distinguish transport problems from content/reasoning problems, verify the active chat path, and recover with short, concrete next steps.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [telegram, gateway, triage, delivery, troubleshooting, chat, productivity]
---

# Telegram Gateway Triage

Use this skill when a user says Telegram feels stuck, messages are not landing correctly, replies seem to go to the wrong place, or the chat behavior is otherwise confusing.

This is a *triage* skill: first determine whether the problem is transport/delivery, routing, conversational content, or conversation-state drift. Do not assume the model is "stuck" until the chat path and the latest message/response alignment are ruled out.

A common failure mode is not a broken Telegram transport at all, but a thread/context mismatch: the assistant is answering the wrong ask, following stale context, or speaking to the wrong topic/thread. Treat that as a separate diagnosis from pure delivery failure.

If the user rejects your first diagnosis, *stop and reset* rather than defending the stale interpretation. Re-anchor on the latest explicit user instruction and ask for the exact thing to retry.

Another failure mode is reply drift: the assistant continues an older line of work instead of responding to the most recent Telegram complaint. In that case, restart from the user’s latest message and answer only that.

If the assistant has already drifted into unrelated work, acknowledge the mismatch briefly and return to the Telegram issue instead of explaining the unrelated thread.

## When to use

- the user reports Telegram is stuck, delayed, or behaving oddly
- the assistant seems to be replying in the wrong thread or context
- a user asks why Telegram is not working correctly with the operator agent
- a message may have been delivered, but not where or how the user expected
- the user sees a duplicated response in the desktop TUI (one broken, one correct) — this is a transport/streaming layer issue, not a content issue. See `references/pre-llm-call-plugin-injection-causing-duplication.md`

## Core principle

Separate the problem into two buckets:

1. **Transport / routing problem**
   - the message did not arrive
   - the message arrived in the wrong chat or thread
   - the platform path is misconfigured
   - the target is ambiguous or missing

2. **Content / interaction problem**
   - the response is too verbose or too abstract
   - the reply answered the wrong question
   - the assistant needs to be more concrete or shorter

Treat those as different failures. Fix the right one first.

## Recommended triage order

0. **Is the gateway process alive AND healthy?** (check this FIRST)
   - Before any routing/delivery triage, confirm the messaging gateway process is running. A dead gateway kills Telegram in BOTH directions and is the most fundamental transport failure.
   - `hermes gateway status` — authoritative. `pgrep -fl "gateway run"` — is a process up?
   - The the operator agent desktop app spawns `hermes dashboard` only — it does NOT spawn the gateway. A dead gateway stays dead across reboots unless the launchd service is installed.
   - If not running: `hermes gateway install` + `hermes gateway start` (durable), or `hermes gateway run` (foreground). Verify `✓ telegram connected` in gateway.log before claiming recovery.
   - Full procedure + the launchd disabled-state trap: see `references/gateway-process-lifecycle-and-launchd.md`.
   - **Process-alive ≠ healthy.** A second, sneakier failure is the *silent polling stall* (wedge): the process is up, the TCP socket to Telegram stays `ESTABLISHED`, and launchd/systemd sees it as healthy — but the async `getUpdates` coroutine has died and no inbound messages flow. The tell is **log recency**: check `stat -f "%Sm" <agent-home>/logs/gateway.log` against the wall clock, and look for a multi-minute gap in `inbound message:` lines while the user is actively sending. A live PID + a stale log + 0.0% CPU = wedge. Recovery is `hermes gateway restart`; full symptom signature and the missing-message diagnostic sequence are in `references/silent-polling-stall-diagnosis.md`.

1. **Confirm the active destination and direction**\n   - Identify whether the message is meant for the home Telegram chat, a specific chat ID, or a thread/topic.\n   - Determine if the issue is with OUTGOING messages (agent → Telegram) or INCOMING messages (Telegram → agent).\n   - For OUTGOING messages (using `hermes send -t telegram` or send_message tool):\n     - The tool runs in the agent process and reads config.yaml directly\n     - TELEGRAM_HOME_CHANNEL can be set as a top-level key in config.yaml\n     - Verify with: `hermes config get TELEGRAM_HOME_CHANNEL`\n   - For INCOMING messages (gateway process):\n     - The gateway reads TELEGRAM_HOME_CHANNEL from environment (.env) or gateway.platforms.telegram.home_channel\n     - Verify gateway connection: `grep -i \"telegram connected\" <agent-home>/logs/gateway.log`\n     - If not set, configure as nested dict under gateway.platforms.telegram.home_channel

2. **Check whether the symptom is delivery or comprehension**
   - If the user says "stuck" or "not working", ask for the *last concrete symptom* or the last message that succeeded.
   - Keep the first diagnostic reply short.

3. **Recover with one concrete action**
   - If the issue is platform routing, verify the chat path, allowlist, topic/thread mapping, or delivery configuration.
   - If the issue is conversation-state drift, compare the latest user message against the immediately prior assistant turn, then answer the actual ask first.
   - If the user explicitly says the Telegram diagnosis is wrong, drop it immediately and switch to the real task.
   - If the issue is conversational, switch to a concise, action-first response.
   - If Step 0 found a silent polling stall (wedge), the one action is `hermes gateway restart`. Confirm `✓ telegram connected` in the log. Then — critically — set user expectations: any message sent during the stall whose offset already advanced will NOT redeliver and must be resent.

4. **Verify before claiming success**\n   - For OUTGOING messages: Do not say a message was sent unless you have an actual send success from `hermes send -t telegram`\n   - For INCOMING messages: Do not say the gateway is fixed until you see `✓ telegram connected` in gateway.log
   - For a wedge-recovery restart specifically: `✓ telegram connected` proves the poller is back, NOT that the user's missing message will arrive. Confirm the missing message's fate by checking all three sinks (gateway log inbound lines, `audio_cache/` newest file, session JSONL timestamps). If a missing message left no trace, declare it unrecoverable and ask for a resend — do not imply it is queued for redelivery.\n
## Response style when the user reports a stuck chat

- acknowledge the problem plainly
- avoid a long meta explanation
- separate "Telegram delivery" from "assistant reasoning"
- ask for one narrow detail if needed: last successful message, exact symptom, or target chat/thread
- if the user says the chat is "stuck" or "not working correctly," do *not* jump to unrelated repo edits, content rewrites, or generic reassurance; first isolate the active chat path, the thread/topic mapping, and the last successful message/assistant turn pair
- if the user explicitly corrects you that this is *not* a Telegram issue, stop gateway triage immediately and re-anchor on the new task instead of continuing to debug transport
- if the current reply has drifted away from the user's latest Telegram complaint, explicitly drop the unrelated thread, acknowledge the mismatch in one short sentence, and answer the complaint directly instead of continuing the prior work stream
- do not surface unrelated repo/status progress, planning, or previous task context when the user is asking about Telegram being stuck; re-anchor on the latest complaint first

A good first reply is short and direct, for example:
- "I may be seeing a Telegram delivery/routing issue. Tell me the last message that went through, and I’ll separate platform vs. content."

## Pitfalls

- triaging routing/home_channel when the gateway process is simply not running. Always run Step 0 first — `hermes gateway status`. A dead process dwarfs every delivery-layer issue.
- **stopping at "process alive" when the poller is wedged.** A live PID + ESTABLISHED socket + healthy launchd status does NOT mean messages are flowing. If the user is actively sending and the gateway log has no fresh `inbound message:` line in the last few minutes, the async polling loop has stalled silently. Check log recency (`stat -f "%Sm" <agent-home>/logs/gateway.log`) and CPU state before declaring the transport healthy. See `references/silent-polling-stall-diagnosis.md`.
- **assuming a restart will recover a message that went missing during the wedge.** Telegram delivers updates by a stored offset. If the wedged poller already fetched/acknowledged the user's message before stalling, that update is marked delivered server-side and will NOT replay on reconnect — the message leaves no trace in the log, audio_cache, or session JSONL. Run all three checks; if empty, tell the user to resend. Do NOT imply the message "will come through once polling resumes."
- `launchctl bootstrap exit 5` on `hermes gateway install`. This is a stale *disabled* launchd label from a prior install; the install silently falls back to a bare process that dies on reboot. Fix: `launchctl enable "gui/$(id -u)/ai.hermes.gateway"` then re-bootstrap. See `references/gateway-process-lifecycle-and-launchd.md`.
- assuming the model is malfunctioning when the issue may be routing or thread-context drift
- Assuming the home channel is set when it is not, leading to delivery failures when sending to the bare 'telegram' target.
- Using `hermes config set TELEGRAM_HOME_CHANNEL <id>` — this writes a top-level flat key that the gateway process NEVER reads for incoming message handling. However, for OUTGOING messages via the send_message tool (which runs in the agent process), this DOES work as the tool reads config.yaml directly.
- Setting `home_channel` as a bare scalar in config.yaml (e.g. `home_channel: <chat-id>`) — causes `'int' object is not subscriptable` because `HomeChannel.from_dict()` expects a dict. Must be a nested object with `chat_id`, `platform`, and `name` keys.
- Editing source code (`gateway/config.py`) when the problem is config data format. The `send_message` tool calls `load_gateway_config()` in the *calling process*, not the gateway process. Trace the actual data format the parser expects before modifying parser code.
- giving a long status essay instead of a concrete diagnostic step
- mixing platform troubleshooting with content revision
- continuing to troubleshoot Telegram after the user has said that is not the task
- hiding uncertainty behind vague reassurance
- claiming success without a verified send or route confirmation
- answering the wrong user ask because the assistant followed stale context instead of the latest message
- fabricating or implying that a Telegram-related action succeeded when no verified delivery or route check has happened
- **editing config.yaml directly for config changes** — `<agent-home>/config.yaml` is guard-protected for security-sensitive writes and will reject tool edits. Use `hermes config set <key> <value>` CLI instead (e.g., `hermes config set memory.provider ""`). This is the canonical path for all runtime config changes.
- **using `whisper --model turbo` for voice message recovery** — turbo takes 60+ seconds on a single voice memo and will timeout under the default terminal timeout. Use `whisper --model tiny` instead (transcribes in ~15s, good enough for recovery). Voice messages are cached at `<agent-home>/audio_cache/` as `.ogg` files. To find a user's message by time, check gateway.log for `msg=''` entries (empty msg + nearby `Cached user voice at` line = voice message). Cross-reference timestamps to find the right `.ogg` file.
- **duplicated TUI output (broken first copy, clean second copy)** — this is NOT a Telegram delivery issue. It is a plugin `pre_llm_call` hook injecting visible metadata (bracket blocks) into the user message, which leaks into the streaming preview. The `message.complete` event then replaces it with clean ground-truth text, producing two visible copies. Check enabled plugins for `pre_llm_call` hooks that return non-None strings. See `references/pre-llm-call-plugin-injection-causing-duplication.md`.
- **gateway.error.log noise from the `workflow_enforcement` plugin** — the error log can be dominated by thousands of `FileNotFoundError: ...workflow-enforcement-metrics.json.tmp` errors (a `.tmp` rename race in the plugin). The plugin fails open and is NOT a Telegram issue, but the volume buries Telegram-specific errors. When scanning the error log, grep-filter instead of reading the tail: `grep -n "Telegram" <agent-home>/logs/gateway.error.log | tail -20`.
- **the exhausted-reconnect-budget wedge variant** — the adapter has a fixed budget of 10 reconnect attempts with 60s backoff. During a transient network outage (even a 10-minute blip), it burns through all 10 attempts against `api.telegram.org` and fallback IPs, then the retry loop terminates and the polling coroutine dies permanently — but the gateway process stays alive. Network may have fully recovered by diagnosis time. Confirm the network path is fine with `curl -s --connect-timeout 5 https://api.telegram.org` (a 302 means network OK, wedge is a stale adapter state). The error-log fingerprint is the `attempt N/10` sequence followed by silence. See `references/silent-polling-stall-diagnosis.md` section "Common trigger: exhausted reconnect budget" for the full recovery procedure.

## Overlaps

- Use `telegram-artifact-delivery` when the task is specifically about sending files or attachments.
- Use `gateway-startup-hooks` when the issue is the gateway boot sequence or startup checklist.

## Support files

- `references/telegram-stuck-triage-notes.md` — session-specific triage notes, symptom patterns, and recovery prompts.
- `references/conversation-drift-recovery.md` — concise notes on recovering when the user rejects the initial interpretation and the assistant must re-anchor on the actual task.
- `references/stuck-chat-reply-drift.md` — session note on Telegram triage when the assistant accidentally answers the wrong thread or spins into unrelated work.
- `references/stale-context-reanchor.md` — compact recovery note for when the latest user complaint is about Telegram but the assistant has drifted into a different task.
- `references/telegram-home-channel-fix.md` — complete procedure for setting the Telegram home channel correctly (nested dict in YAML, `.env` fallback, common pitfalls like the misleading `hermes config set TELEGRAM_HOME_CHANNEL` command).
- `references/gateway-process-lifecycle-and-launchd.md` — diagnosing a dead gateway process, starting/persisting it as a launchd service, and clearing the stale disabled-label trap (`launchctl bootstrap exit 5`).
- `references/silent-polling-stall-diagnosis.md` — the wedge failure mode: process alive + socket ESTABLISHED but the async `getUpdates` loop is dead. Symptom signature, the "message didn't land" diagnostic sequence (log → audio_cache → session JSONL), and the hard truth that a restart does NOT recover messages whose Telegram offset already advanced.
- `references/pre-llm-call-plugin-injection-causing-duplication.md` — desktop TUI duplicated output (one broken copy + one clean copy). Caused by a plugin's `pre_llm_call` hook injecting visible bracket metadata into the user message, which leaks into the streaming preview then gets replaced by message.complete ground truth.
- `templates/telegram-home-channel-config.yaml` — known-good config.yaml snippet for the home channel nested dict structure.
- Add more notes here whenever a new failure pattern shows up in chat or delivery triage.
