# False-Positive Restarter Diagnosis (2026-08-21 — "telegram is down again, third time today")

## The class
Recurring Telegram outages where the gateway process is healthy, Bot API answers, polling mode correct, zero pending updates — **the outages are CAUSED by watchdogs restarting a healthy gateway**, not by the gateway failing.

## Root physics (memorize these two facts)
1. **`<agent-home>/gateway_state.json` is written ONLY on platform state CHANGES.** A quiet gateway (user not messaging) leaves the file stale for hours while perfectly healthy. Staleness ≠ wedge.
2. **Cron ticks write `agent.log`, NOT `gateway.log`.** Log-silence thresholds on gateway.log fire during normal quiet hours. (Measured: 24 gaps >50min in 4 days, all quiet windows, median inter-write gap 0.0min when active.)

## Diagnosis sequence (proven)
1. **Count the killers**: `grep "Received SIGTERM" <agent-home>/logs/gateway.log | grep <today>` vs what each watcher claims (`<agent-home>/logs/telegram-guardian.log` restart_issued lines, `/<workspace>` kickstart lines). Mismatch = another killer exists.
2. **Read `<agent-home>/logs/gateway-exit-diag.log`** — gateway.start/exit_clean/exit_nonzero/previous_unclean_exit with pids and timestamps. This file attributes deaths honestly.
3. **Independent Bot-API truth**: getMe (bot valid) + getWebhookInfo (url=none/polling, pending_update_count=0) — transport healthy regardless of what watchers think.
4. **Gap-analyze gateway.log inter-write times** over 48h: if >50min gaps are frequent in quiet windows, any watchdog threshold near that range is a false-positive machine.
5. **Hunt duplicate watchdogs under BOTH launchd namespaces**: `ai.hermes.*` AND `com.your-org.*` labels can run the SAME script. Found: `ai.hermes.telegram-liveness-watchdog` (300s StartInterval) + `com.your-org.watchdog.telegram_liveness_watchdog` (KeepAlive daemon_loop wrapper) both live.

## Fix pattern (evidence-gated, one restarter)
- Bootout ALL but one restarter: `launchctl bootout gui/$(id -u)/<label>`. Keep the rate-limited guardian (its decide() ladder + 10min cooldown).
- Harden the survivor's wedge rule: restart ONLY when stale AND (telegram state != connected OR pending_update_count > 0 from getWebhookInfo). Probe failure = not evidence.
- Watchdog scripts return: 0 healthy-silent / 1 healed / 2 unhealable.
- **Never patch a script that restarts the gateway from inside the gateway process** (the agent's own terminal runs under the gateway; a restart kills the patch command). Use the patch TOOL, not terminal heredocs, for gateway-adjacent scripts.

## Verification after fix
- Watchdog manual run exits 0 silent on a healthy-but-quiet gateway.
- Exactly one telegram-related restarter in `launchctl list | grep -i telegram`.
- gateway_state.json still stale is NOW EXPECTED during quiet — do not re-add a staleness watchdog.
