# O'Keefe Operational Resilience Audit (2026-08-12)

**Auditor:** the specialist engine (Walter Cannon — homeostasis/resilience)
**Question:** Can the O'Keefe memory system survive unattended for a week?

## System Architecture (verified live)

O'Keefe (:port) relies on TWO independent crash-recovery supervisors:

1. **auto_repair_watchdog** — the operator agent cron `132dd1d69078`, every 2 min
   - Scans `FLEET_REGISTRY` directly via `scan_registry_direct()`
   - Probes each engine port with `_engine_alive(port)` (0.5s timeout on `/health`)
   - Restarts dead engines via `_restart_engine()` (kills stale port holders, starts new process, waits 8s for health)
   - Retry logic: MAX_RETRIES=3, RETRY_COOLDOWN=300s
   - After 3 failures: posts escalation to `message-bus.db`

2. **fleet-autonomic** — launchd plist `com.your-org.fleet-autonomic`
   - `RunAtLoad=true`, `StartInterval=30` (every 30 seconds)
   - Runs `organism/start_engines.py` — idempotent fleet sweep
   - No retry limit — tries every engine once per sweep

**Machine reboot coverage:** Both supervisors start at boot.
- the operator agent gateway: launchd plist `ai.hermes.gateway` with `KeepAlive=true` + `RunAtLoad=true`
- Fleet-autonomic: launchd plist with `RunAtLoad=true`
- O'Keefe itself has NO dedicated launchd/crontab entry — it relies on the supervisors.

## Critical Findings (all observed live during audit)

### CRITICAL 1: Chronic crash-loop risk (8s restart window too short)

The watchdog `_restart_engine()` waits only 8 seconds for `/health` to respond
(8 polls × 1s). Cold-boot uvicorn with numpy/scipy imports can exceed this.

**Live evidence (2026-08-12):** O'Keefe died 4 times in 28 minutes during the
audit (14:09, 14:10, 14:22, 14:37 CDT). 3 of 4 restarts succeeded; 1 FAILED
("started but never healthy, PID 833"). The failed restart burned a retry
counter. At ~1 death per 7 minutes, this produces ~1260 death events per week.

```python
# auto_repair_watchdog.py line 144:
for _ in range(8):          # <-- only 8 seconds
    time.sleep(1)
    if _engine_alive(port):
        return True, ...
return False, f"... started but never healthy ..."
```

### CRITICAL 2: Amnesia on restart (no persistence verification)

Neither supervisor verifies that persisted memories loaded correctly after
restart. Observed live: `memory_count` dropped from 28 to 0 during a restart
race, despite the persist file (`<agent-home>/state/okeefe_memory.json`) having
144KB / 8 traces.

The engine `/health` reports `memory_count: len(_engine.traces)`. If
`_load_persistent_state()` fails silently (e.g., transient file lock,
corrupt read), the engine runs with zero memories. New writes then
overwrite the old persist file — **permanent data loss**.

**Verification command (run after ANY O'Keefe restart):**
```bash
# Check memory_count is non-zero if persist file has data
curl -s http://127.0.0.1:port/health | python3 -c "import sys,json; print('memory_count:', json.load(sys.stdin)['memory_count'])"
python3 -c "import json; d=json.load(open('$HOME/.hermes/state/okeefe_memory.json')); print('persist traces:', len(d.get('traces',{})))"
# If memory_count=0 but persist has traces → AMNESIA. Restart again.
```

### CRITICAL 3: Escalation chain is the operator agent-dependent (no independent fallback)

After 3 consecutive restart failures, the watchdog posts to `message-bus.db`
(`to_op='hermes'`, `status='pending'`). The `hermes-autonomic-bridge` cron
(every 2 min) reads pending alerts and outputs to cron stdout → Telegram.

**BUT:** If the operator agent itself is down, the alert is NEVER delivered. The
`bus_hygiene.py` cron marks alerts older than 24h as `'done'` with no action.
**30,292 historical escalation messages** were found — all silently consumed.

There is NO notification mechanism independent of the operator agent:
- No launchd-level email/iMessage/Telegram fallback
- No direct push notification
- bus_hygiene.py silently cleans alerts after 24h

**The escalation ladder:**
```
Watchdog detects 3 failures
  → _post_to_bus(esc) writes to message-bus.db
    → hermes-autonomic-bridge (cron 2min) reads pending
      → outputs to cron stdout → Telegram delivery
        → IF HERMES DOWN: message sits pending
          → bus_hygiene.py (cron 2h) marks as 'done' after 24h
            → SILENT LOSS
```

### CRITICAL 4: Dual-supervisor race condition

Both watchdog (cron every 2min) and fleet-autonomic (launchd every 30s)
independently detect O'Keefe as dead and attempt to start it. They do not
coordinate. If both fire simultaneously:

1. Watchdog calls `_kill_port_holders(8147)` — kills ANY process on the port
2. Fleet-autonomic calls `start_engine()` — starts a new process
3. Watchdog's kill may terminate fleet-autonomic's just-started process
4. Result: restart loop, port thrashing

The `_kill_port_holders()` function kills ANY process on the port (not just
O'Keefe), with only a weak `_engine_alive()` check as a safety guard. A
non-O'Keefe service without `/health` would be killed.

### ACCEPTABLE 5: Machine reboot IS covered (contrary to initial assumption)

Task context stated "O'Keefe is NOT started by any boot hook or launchd."
This is **FALSE**. Verified:

```bash
# Fleet-autonomic launchd (starts engines at boot)
plutil -p ~/Library/LaunchAgents/com.your-org.fleet-autonomic.plist
# RunAtLoad = true, StartInterval = 30

# the operator agent gateway launchd (starts cron system at boot)
plutil -p ~/Library/LaunchAgents/ai.hermes.gateway.plist
# KeepAlive = true, RunAtLoad = true

# Fleet supervisor runs start_engines.py (idempotent sweep)
# 10854 historical runs, last exit code = 0
```

### ACCEPTABLE 6: Persist path consistency confirmed

Both startup paths use the same canonical persist path:
- `start_engines.py` line 144: `<agent-home>/state/okeefe_memory.json` (hardcoded)
- `hippocampal_startup.py` line 40: `os.environ.get("OKEEFE_PERSIST_PATH") or "<agent-home>/state/okeefe_memory.json"`

Running process confirmed via `ps -E`:
`OKEEFE_PERSIST_PATH=/<workspace>`

Minor inconsistency: `start_engines.py` hardcodes the path (ignores existing
env var). `hippocampal_startup.py` respects an existing env var. Both default
to the same path, so no divergence under normal operation.

### ACCEPTABLE 7: _engine_alive timeout adequate for steady-state

5 measured `/health` response times: 1-9ms. The 0.5s timeout in
`_engine_alive()` is fine for steady-state checks. Would only cause
false-death detection under extreme load (not observed).

## self_healing.db Analysis

```sql
SELECT timestamp, level, detail FROM repair_events
WHERE detail LIKE '%OKeefe%' OR detail LIKE '%8147%'
ORDER BY id DESC;
```

**30-minute window during audit:**
- 4 death events detected
- 3 successful repairs (REPAIRED)
- 1 failed restart (FAILED 1/3)
- 0 escalations triggered (never reached 3 consecutive failures because
  fleet-autonomic recovered between watchdog cycles)

## Unattended Survival Estimate

**0.5–2 days** before first significant data loss event.

| Scenario | Outcome |
|----------|---------|
| Best case (stable period) | O'Keefe stays alive for hours/days |
| Expected (current instability) | ~1260 deaths/week, ~315 failed restarts, multiple amnesia windows |
| Worst case (the operator agent crash + crash-loop) | No escalation delivery, bus_hygiene cleans alerts, system runs degraded indefinitely |

**System will NOT cleanly survive 7 days unattended** in current state.

## Key Files

- Watchdog: `organism/auto_repair_watchdog.py`
- Engine starter: `organism/start_engines.py`
- Fleet supervisor: `organism/fleet_autonomic_supervisor.sh`
- Fleet launchd: `~/Library/LaunchAgents/com.your-org.fleet-autonomic.plist`
- the operator agent gateway launchd: `~/Library/LaunchAgents/ai.hermes.gateway.plist`
- Repair state: `organism/.repair_state.json`
- Repair events DB: `organism/self_healing.db`
- Persist file: `<agent-home>/state/okeefe_memory.json`
- Operator bus: `<agent-home>/message-bus.db`
- Bus hygiene: `organism/bus_hygiene.py`
- Autonomic bridge: `organism/hermes-autonomic-bridge.py`
- Escalation cron: the operator agent cron `132dd1d69078` (every 2 min)
