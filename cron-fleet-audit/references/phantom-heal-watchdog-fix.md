# Phantom-Heal Watchdog Fix — Worked Case (2026-08-16)

## Symptom (principal report)
"What is this writing studio cron garbage in my telegram? Crons is not how we get system live and keep it live"

The Writing Studio Guardian cron ran every 5 minutes with `deliver=origin`. Every non-empty stdout line = one Telegram delivery. The principal was receiving watchdog chatter constantly.

## Root cause chain
1. `pipeline_api.py` (:port) was running as an orphaned process (PID 44555) — serving 200 OK on `/api/pipelines/health`.
2. The launchd label `com.your-org.pipeline-api` showed no PID with last-exit 1: every KeepAlive respawn attempt died instantly because port 8310 was already held by the orphan.
3. The guardian's `check()` trusted `service_has_pid()` (the launchd label), concluded "dead," ran `load_service()` + appended "reloaded launchd service" to actions — every single tick.
4. Any action list entry → print → Telegram.
5. Bonus noise: `datetime.utcnow()` DeprecationWarning printed to stdout on every run.

## Diagnosis commands (run in this order)
```bash
launchctl list | grep <label>          # "-  1  com.your-org.pipeline-api" = no PID, exit 1
lsof -nP -iTCP:port -sTCP:LISTEN      # who ACTUALLY owns the port
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:port/api/pipelines/health   # 200 = healthy under orphan
```
launchd-dead + port-owned + health-200 = phantom-dead label with orphaned server.

## The three fixes

### Fix 1 — phantom-guard patch (in the watchdog script)
Before acting on a dead service label, probe HTTP health FIRST:
```python
if not service_has_pid():
    if http_ok("/api/pipelines/health"):
        pass  # healthy under orphaned process: nothing to heal, nothing to say
    elif PLIST.exists():
        # real reload path, only when health actually fails
        load_service(); time.sleep(3)
        if not service_has_pid() and not http_ok("/api/pipelines/health"):
            restart_service(); time.sleep(3)
        actions.append("reloaded launchd service")
    else:
        # plist missing = genuine CRITICAL
```

### Fix 2 — adopt the orphan under launchd
```bash
kill 44555                                # the orphan
launchctl kickstart -k gui/$(id -u)/com.your-org.pipeline-api
# verify: launchctl list shows live PID; curl health = 200; re-check after 20s
```

### Fix 3 — silence stdout
Replace deprecated `datetime.utcnow()` with timezone-aware equivalents; any warning or status print on a `deliver=origin` cron becomes user-facing spam.

## Proof protocol (never skip)
1. Run the watchdog check twice manually — expect EMPTY stdout, exit 0.
2. Confirm launchd PID stable after 20s+.
3. Confirm health endpoint still 200.

## Architecture principle (principal directive, verbatim intent)
Crons are not a liveness mechanism. launchd (KeepAlive) owns service supervision with millisecond restarts; the watchdog exists only for failures a human must know about. Any every-few-minutes print-unconditionally cron with `deliver=origin` is a spam generator by construction — audit the whole fleet for this class (heartbeat 2min, mosaic-gateway 1min, virchow 15min share the smell).
