# Watchdog Daemon Migration — cron watchdogs → launchd-owned daemons (2026-08-16)

## principal directive (two-step correction, same day)
1. "Crons is not how we get system live and keep it live" — cron polling is not supervision.
2. "The watchdog is a cron based system" — demoting a watchdog to a "failure-only cron" is STILL polling theater with a timer. The watchdog itself must be supervised by the kernel, not by a scheduler tick.

Key insight: a dead cron watchdog stays dead until the next tick of whatever watches it. A launchd KeepAlive daemon is resurrected by launchd in milliseconds.

## The migration tool
`<agent-home>/scripts/daemonize_watchdog.py <script-name> <interval-seconds> [python3|bash]`

Generates per watchdog:
- `<agent-home>/scripts/daemon-loop-<script>` — bash `while true` loop: run script, capture output+rc, append to `<agent-home>/watchdog-events/<script>.events` ONLY on rc!=0, sleep interval, repeat
- `~/Library/LaunchAgents/com.your-org.watchdog.<name>.plist` — RunAtLoad=true, KeepAlive=true (launchd owns the watchdog's own liveness)

Then REMOVE the cron job so nothing double-runs.

## Migrated 2026-08-16 (8 watchdogs)
ws-guardian (300s), mosaic-gateway (60s), telegram-liveness (300s), model-health (1800s), self-healing-loop (900s), virchow-afferent (900s), mycelium-bootstrap (600s), autonomic-bridge (60s)

## Proof protocol (executed, all passed)
1. `launchctl list | grep com.your-org.watchdog` — all 8 live PIDs
2. **Kill-test:** kill a daemon PID → launchd resurrects in <4s (the supervision property cron cannot provide). Verified on autonomic-bridge: old PID 85602 → new PID 86434.
3. **Silence check:** 60s of healthy operation = zero event files
4. Cron counterparts removed (no double-run)

## Two traps hit during migration (both caught by inspection)

### Trap 1: healthy-run chatter becomes event noise
Scripts designed for cron PRINT status on success (mycelium "BOOTSTRAP COMPLETE", model-health "evaluated 688 new log bytes"). First daemon ticks recorded these as events with rc=0. **Fix:** loop records events ONLY on rc!=0; healthy output goes to the stdout journal (0B when silent).

### Trap 2: the migration exposes pre-existing defects
The ws-guardian daemon's FIRST tick flagged "server will not restart on :port" — real: the old cron guardian's earlier heal had spawned an orphan server holding the port, leaving the launchd label dead. The cron had been papering over its own artifact. **Fix:** adopt the orphan (kill PID, `launchctl kickstart -k gui/$(id -u)/<label>`, verify stable PID + health 200), guardian goes silent.

### Trap 3: journal-mtime is NOT a liveness test
A 70s mtime watch on the stdout journal reported "LOOP DEAD" — false alarm. Healthy daemons write NOTHING, so journal mtimes never move. **Correct liveness check:** `ps -p <pid> -o pid,stat,etime` (state S + growing elapsed time = alive). Also: `timeout` is not available in macOS default PATH — use explicit kill or `gtimeout` if installed.

## Correct split (the standing architecture)
- **launchd = staying alive** — services AND watchdogs, millisecond restarts, zero scheduler dependency
- **cron = scheduled WORK only** — daily reviews, audits, pipelines, reports. Never liveness polling at any cadence.

## Supervision v1 known gaps (formal Lamport review 2026-08-16; design in when hardening)
1. **No per-tick timeout** — a script hanging on network/file-lock leaves the daemon "healthy" and silent forever; supervision watches the loop, not the tick. Needs per-tick timeout + tick-heartbeat (watchdog-of-the-watchdog).
2. **RunAtLoad thundering herd** — all 8 daemons fire at login simultaneously; fast-cadence daemons check services that haven't started yet → false CRITICALs on reboot. Stagger initial ticks or add a startup grace window.
3. **rc!=0-only events hide flapping** — flap where internal heal succeeds returns 0; the flap is invisible. Capture flap/persistence/recovery when flapping matters.
4. **Single-supervisor blind spot** — launchd is one supervisor; if launchd itself wedges, all 8 daemons are unsupervised and nobody knows. A slow second-order cron check (e.g. hourly) is the one legitimate cron use here.
5. **exit-code column confusion** — `launchctl list` column 2 is LAST exit status (-15 = SIGTERM from kickstart restarts), not current state; a daemon with live PID and -15 exit is HEALTHY, not failing.

## Operator-bus R1 (sibling lane)
After migrating, post R1 to sibling-agent on the operator bus: engine state (kappa learning, MM queue) is now mutated by launchd daemons instead of crons — sibling-agent must verify no file-lock/atomicity assumptions broke. The phantom-guard patch invariant (healthy API + dead label = do nothing) must hold if the pipeline_api launch path changes.
