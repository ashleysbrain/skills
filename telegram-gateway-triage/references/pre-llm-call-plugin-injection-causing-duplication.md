# pre_llm_call Plugin Injection Causing TUI Streaming Duplication

## Symptom

User sees a duplicated response in the desktop TUI: first copy is garbled/contaminated
with bracket metadata text, second copy is clean and correct. The user asks "why is it
twice and why is the first one broken?"

## Root Cause

A plugin's `pre_llm_call` hook returns a string. That string is injected into the user
message content (appended in `agent/turn_context.py` line ~457, then applied in
`agent/conversation_loop.py` line ~797-802). The model's response is then streamed back
with that injected bracket text leaking into the streaming preview.

The duplication mechanism:
1. `pre_llm_call` returns `[plugin_name] metadata text [/plugin_name]` — this gets
   appended to the user's actual message before the API call
2. The model's response streams via `message.delta` events — the streamed preview
   shows text contaminated with the injected metadata
3. `message.complete` delivers the clean ground-truth text (the `recordMessageComplete`
   function in `turnController.ts` replaces the streamed preview with authoritative text)
4. User sees TWO copies: the garbled stream preview, then the clean complete text

## Specific Case

The `workflow_enforcement` plugin's `pre_llm_call` hook was injecting:

```
[workflow_enforcement]
objective: <user's objective>
required_operations: N
hard_constraints: ... | ...
[/workflow_enforcement]
```

into every user message. This leaked into streamed responses.

## Fix Applied

1. Made `pre_llm_call` return `None` instead of the bracket block. The plugin's
   enforcement value lives in `pre_tool_call` (write blocking), not in prompt injection.
2. Fixed the plugin's `_write_json` to use atomic writes (write to temp file, then
   `tmp.replace(path)`) to prevent concurrent JSON parse errors from partial writes.

## Diagnostic Steps

1. Check for enabled plugins with `pre_llm_call` hooks:
   ```bash
   grep -n "pre_llm_call" <agent-home>/plugins/*/__init__.py
   ```
2. Look for hooks that return a non-None string value
3. Check the gateway log for the injected text appearing near model responses
4. The tell: first copy garbled with bracket text, second copy clean = streaming
   preview contaminated by injection, then replaced by message.complete

## General Rule

`pre_llm_call` hooks that return strings inject text into the user message. This is
by design for memory/context injection, but if a plugin injects VISIBLE METADATA
(bracket blocks, status text, diagnostic info) rather than silent context, that text
leaks into the model's output stream and causes duplication.

Plugins should use `pre_llm_call` for:
- Silent context injection (memory, retrieved knowledge) — invisible to the user
- State tracking / telemetry — return None, store state internally

Plugins should NOT use `pre_llm_call` for:
- Injecting visible metadata blocks into the conversation
- Enforcing workflow rules via prompt text (use `pre_tool_call` for enforcement)
- Any text the user would see if it leaked into the response

## Code Locations

- Plugin hook invocation: `agent/turn_context.py` ~line 434-459
- Injection into user message: `agent/conversation_loop.py` ~line 790-802
- Streaming preview: `ui-tui/src/app/turnController.ts` `recordMessageDelta` / `scheduleStreaming`
- Ground-truth replacement: `ui-tui/src/app/turnController.ts` `recordMessageComplete`

Session: 2026-07-06
