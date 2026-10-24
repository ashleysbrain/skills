# Silent Polling Stall — Diagnosis & Recovery

The "wedge" failure mode: the gateway process is **alive but the Telegram polling
loop is dead**. This is the inverted twin of the dead-process case in
`gateway-process-lifecycle-and-launchd.md`, and it is *harder to catch* because
every shallow health check passes.

## Symptom signature (all four together)

1. `hermes gateway status` reports the service as loaded/running; `pgrep` shows a PID.
2. `ps -o pid,stat,%cpu ...` shows the process `S` (sleeping) at **0.0% CPU**.
3. A live TCP socket to `149.154.x.x` / `[2001:67c:4e8:...]` (Telegram) is still `ESTABLISHED` via `lsof -p <pid>`.
4. The gateway log has gone **silent for many minutes** with no `inbound message:` line.

The decisive signal is #4: log recency. A healthy polling loop writes an inbound
line within seconds of any user message. A gap of >5 min with the user actively
sending means the loop is wedged, not idle.

## Diagnostic sequence for "my message didn't land"

Run these in order. Stop at the first hit.

1. `hermes gateway status` + `pgrep -fl "gateway run"` — process up?
2. `stat -f "%Sm" <agent-home>/logs/gateway.log` — when was the log last written? Compare to wall clock. A stale log with a live PID = wedge.
3. `ps -o pid,stat,%cpu,etime -p <pid>` — 0.0% CPU + `S` state on an idle-but-active chat confirms it.
4. `lsof -p <pid> | grep -iE "ESTABLISHED|149\.154"` — socket to Telegram still up? (Distinguishes wedge from network outage.)
5. If a voice/photo/attachment was involved: `ls -lat <agent-home>/audio_cache/ | head` — newest file older than the missing message? Confirms it never reached the adapter.
6. Session JSONL check: `grep -oE '"timestamp":"2026-06-29T1[3-9][^"]*"' <agent-home>/sessions/20260629_*.jsonl | tail` — no rows after the suspected send time = message never entered the agent loop.

## Recovery

`hermes gateway restart` — kills the wedged process and brings up a fresh poller.
Confirm recovery by grepping the log for `✓ telegram connected` within ~10s. New
messages the user sends after restart arrive normally.

## CRITICAL: what restart does NOT recover

A restart reconnects polling using Telegram's **stored update offset**. If the
wedged poller had already fetched (and acknowledged) the user's message before
stalling — even if it never processed it — Telegram considers that update
**delivered** and will NOT replay it on reconnect.

- The message leaves **zero trace**: no inbound log line, no audio_cache file, no session JSONL row.
- There is no `getUpdates` flag that forces redelivery of a past-offset message.
- The only recovery is to **ask the user to resend**. Be upfront about this; do not imply the message will "come through once polling resumes" — it will not.

Confirm the offset-advance case by checking all three sinks (log, audio_cache,
session JSONL). If all three are empty for the missing message, it is gone.

## Common trigger: exhausted reconnect budget

The most common cause of the wedge is not exotic — it is a **transient network
outage that outlasts the adapter's reconnect budget**. The adapter retries
`api.telegram.org` and its fallback IPs up to 10 times with 60s backoff. If the
outage lasts longer than ~10 minutes, all 10 attempts fail, the retry loop
**terminates permanently**, and the polling coroutine dies — but the gateway
process stays alive.

The critical nuance: **network may have fully recovered by diagnosis time.** A
transient blip at 13:00 that resolved by 13:15 leaves a permanently wedged
poller even though `curl api.telegram.org` works fine at 13:30.

**Diagnostic step to distinguish wedge from active outage:**

```
curl -s --connect-timeout 5 https://api.telegram.org
```

A 302 (nginx redirect) or any HTTP response means the network path is fine and
the wedge is a stale adapter state. A timeout or connection refused means the
outage is still active — restart won't help until network recovers.

**Error-log fingerprint** — look for this sequence in gateway.error.log:

```
WARNING ... Telegram network error (attempt 6/10), reconnecting in 60s
WARNING ... Telegram network error (attempt 7/10), reconnecting in 60s
WARNING ... Primary api.telegram.org connection failed
WARNING ... Fallback IP 149.154.166.110 failed
(silence — no more attempts, no inbound messages)
```

The `attempt N/10` sequence climbing to silence is the signature of an
exhausted reconnect budget. Grep-filter the error log to find it — the raw tail
will be buried under thousands of `workflow_enforcement` plugin errors.

## Why launchd doesn't self-heal this

launchd's `KeepAlive` / `OnDemand` keys watch **process liveness**, not
application-level health. A wedged poller keeps the process alive (event loop
blocked, not crashed), so launchd never restarts it. The same is true of a naive
`restart=on-failure` systemd unit. A real fix needs an application-level
watchdog (alert when gateway log goes silent >N min, or when no successful
`getUpdates` in a window) — that belongs to the central/cortical operator, not
the gateway triage skill.

## Hand-off note

A related but separate code bug often appears in the error log during these
sessions: `RuntimeError: Could not determine home directory.` from
`agent/subdirectory_hints.py` (`Path(raw_path).expanduser()`). It is NOT the
wedge cause, but it kills in-flight API calls. Route it to the diagnostic/surgeon
operator (sibling-agent) — do not attempt a source fix from the peripheral/autonomic side.
