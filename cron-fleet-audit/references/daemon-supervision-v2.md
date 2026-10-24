# Daemon Supervision v2 — must-fix closure + migration-completion rule (2026-08-16 evening)

Companion to `references/watchdog-daemon-migration.md` (which documents v1 + the migration itself). This file records the v2 hardening pass: the specialist engine's formal failure-mode review, the must-fix set executed and live-tested, and the generator-consistency rule.

## What the kill-test proves (and does not)
P(respawn | process death) ≈ 1. It does NOT cover: hung ticks (no timeout), rc==0-garbage output accepted as health, unbounded event growth on persistent failure (~1440 events/day at 60s cadence), crash-loop of the loop itself (KeepAlive has no backoff; default throttle gives ~8640 restarts/day after a bad edit), disk-full silencing `>>` appends exactly when the system is sick, and no recovery signal (silence is ambiguous between healthy and dead).

## The v2 must-fix set (all executed, all live-tested)
1. **Per-tick timeout**: `daemon_loop.py` runs each tick via `subprocess.run(timeout=N)`. Hang killed, rc=124, "HANG: killed after Ns" in event detail. Proven: a 300s-sleep script was killed at 5006ms.
2. **Heartbeat files**: every tick writes `<script>.heartbeat` (unix-ts, rc, dur). The alarm predicate is TIMESTAMP FRESHNESS, not process existence. Meta-check alarm: age > 2×interval + timeout + 60.
3. **Transition event schema**: one JSON line per state change `{ts,daemon,rc,outcome,dur_ms,consecutive_fail,detail}`, outcome = OK | CRITICAL | RECOVERY. Records OK→CRITICAL, CRITICAL→OK (RECOVERY), every 10th consecutive fail (rate-limited persistence). Flap = alternating events; persistence = consecutive_fail; recovery events now exist. rc!=0 alone was the WRONG predicate — it observes the watchdog, not the service (a successful internal heal returns 0 and the flap vanishes).
4. **Bounds**: event rotation (keep last 100 past 200 lines); ThrottleInterval=60 in every plist (crash-loop cap ~1440/day).
5. **Boot stagger**: deterministic `md5(script) % 26` seconds — no thundering herd on login, no false CRITICALs from fast-cadence daemons checking services that haven't started.
6. **The one legitimate cron**: `daemon-fleet-meta-check.py` (job `aadd44c40acf`, 2-hourly, deliver=telegram) checks heartbeat freshness + launchctl presence. Its value is firing from a DIFFERENT failure domain than launchd — cron is the correct tool for the second examiner, NOT for liveness polling. Healthy = zero output. Negative-tested: planted 5000s-stale heartbeat → alarm fires; restored → silent.

## v2 artifacts (paths)
- `<agent-home>/scripts/daemon_loop.py` — the unified loop (one program, N instances; replaces all per-watchdog bash loops)
- `<agent-home>/scripts/daemonize_watchdog.py` v2 — generates ONLY daemon_loop plists (timeout auto = max(30, interval/4)); emits no bash artifacts
- `<agent-home>/scripts/daemon-fleet-meta-check.py` — supervision-of-supervision

Layer stack: launchd = liveness (KeepAlive + ThrottleInterval) → loop = cadence + timeout → heartbeat = freshness → meta-check cron = second examiner.

## Migration-completion rule (the hard-won lesson)
A migration is NOT done when the fleet is converted. It is done when:
1. The GENERATOR matches the deployed architecture — post-migration QA caught daemonize_watchdog.py still emitting v1 bash loops; any NEW watchdog would have been born without the must-fix set.
2. Old-architecture artifacts are purged — 8 orphaned daemon-loop-* bash files were still on disk (zero plist references verified before deletion).
3. The regenerated generator is PROVEN — scratch-daemon test: register → live PID → heartbeat written (rc=0) → clean teardown → zero remnants.

## v2 proof matrix (every claim live-tested, never inspection-only)
Healthy silence (zero event files fleet-wide) | CRITICAL transition on forced exit 1 | HANG kill at 5006ms | RECOVERY event on fail→OK | stale-heartbeat alarm fires on planted 5000s age, silent when restored | kill-test resurrection on the v2 loop (<5s).

## Why "failure-only cron" was not enough
The principal's second correction ("The watchdog is a cron based system") rejected the v0.5 design where watchdogs were demoted to failure-only CRONS. A watchdog on a cron is still polling theater with a timer — it dies between ticks and nothing resurrects it. The watchdog must be a launchd-owned DAEMON (KeepAlive = millisecond resurrection by the kernel); the loop owns its own cadence internally. Cron survives only as: scheduled work (reviews, audits, pipelines) + the single meta-check whose job is to out-live launchd.
