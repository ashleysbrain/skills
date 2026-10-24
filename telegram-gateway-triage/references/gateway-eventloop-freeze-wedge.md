# Gateway Event-Loop Freeze Wedge (2026-08-16 incident)

Sibling failure mode to the silent-polling-stall, with a DIFFERENT signature and detection signal.

## Symptom signature (verified live)

- Gateway process ALIVE (ps shows R state, ~1.2% CPU) — launchd sees healthy
- `<agent-home>/gateway_state.json` `updated_at` FROZEN at the exact timestamp of the last inbound flush (the gateway's platform-state liveness loop stopped ticking)
- `platforms.telegram.state` still reads `"connected"` — the label lies; the loop that would update it is dead
- Bot API outbound works the whole time (direct `sendMessage` delivers) — only inbound processing is dead
- gateway.log shows `Flushing text batch` + `inbound message:` for the triggering message, then ZERO lines (no errors, no stalls, no responses)
- Other agent sessions keep churning in agent.log independently (workers don't die with the loop)

**User experience:** they send messages, nothing answers. "Telegram is down." Outbound diagnostics delivering can mislead you into declaring it healthy — outbound uses the bot API directly, inbound requires the wedged loop.

## Detection (what to check, in order)

1. `gateway_state.json` `updated_at` age vs wall clock — frozen >10 min with live PID = wedge
2. `platforms.telegram.state` != connected OR state file frozen (state can ALSO lie "connected")
3. gateway.log tail: last `inbound message:` line vs when the user says they sent
4. Independent cross-check: bot `getMe`/`sendMessage` success while inbound dead confirms wedge (not network)

## Heal

```bash
launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway
```

Verify: new PID, then `Connected to Telegram (polling mode)` in gateway.log (~30s), commands registered.

## Prevention: the OFF-PATH WATCHDOG RULE (the critical lesson)

`telegram_liveness_watchdog.py` detects (state-file staleness >600s with live pid, or disconnected platform) and heals via kickstart. It is registered TWICE, and the second registration is the one that matters:

- hermes cron `*/5` — fast path, works only while the gateway is healthy enough to run cron
- **launchd one-shot** `ai.hermes.telegram-liveness-watchdog` (StartInterval 300, RunAtLoad) — OFF-PATH

RULE: **a watchdog that runs inside the process it watches dies with it.** This wedge kills the gateway's cron scheduler; a cron-only watchdog can never fire to heal it. Any self-healing watchdog for a supervisor process MUST have a launchd (or otherwise external) registration. Same principle as Lamport's watchdog-of-watchdog meta-invariant: the checker must be off-path.

## Restart collateral: unsupervised child engines die with the gateway

The kickstart killed the O'Keefe memory engine (:port) — it ran as an unsupervised child with no launchd parent (Tanenbaum's diagnosis proven live). After ANY gateway restart, probe dependent infra ports. Permanent fix: give infra engines their own launchd KeepAlive plists (done for okeefe: `com.your-org.okeefe-engine`). KeepAlive is for resident services only.

Note: `ds-okeefe-engine/scripts/hippocampal_startup.py` is broken as a recovery path — it runs `server.py` bare (no `__main__`, instant exit). Working launch: `python3 -m uvicorn api.server:app --port 8147` from `ds-okeefe-engine/src/`.

## Deeper root-cause suspects (engine lane)

Recurring in logs at wedge time: `conversation_compression: session ownership lookup failed` (ProgrammingError) and `Pre-call sanitizer: healed N empty non-final message(s)`. Both in the compression/persistence subsystem — plausible wedging source. Route to the engine-owner agent with log timestamps, don't chase in the triage lane.
