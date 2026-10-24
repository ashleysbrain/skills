---
name: mosaic-fleet-status-sweep
description: Use when principal asks for system status. Probes every surface.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes.tags:
    - mosaic-os
    - fleet-health
    - operations
  hermes.category: operations
---

# Mosaic Fleet Status Sweep

## When to Use
principal asks "status of the system", "is everything up", or "the system was down, make sure everything is back up". Every claim in the answer comes from a probe executed THIS turn — never from memory of the last sweep, never parroted counts.

## Procedure (one batched pass, independent probes in parallel)
1. **Surfaces**: curl status codes for boards `http://100.107.113.11:port/`, GG3 gateway `:port`, studio API `127.0.0.1:port`. Studio: an unauthenticated `/api/drafts` probe returning 401 JSON proves the service is UP; `/health` endpoints 404 by design. Real liveness = `GET /api/auth/local-token` then `GET /api/drafts?limit=1` with the bearer → 200.
2. **Daemons**: `launchctl print gui/$(id -u)/<label>` state for `com.your-org.taskcal-boards`, `com.ds.studio-api`, `com.your-org.studio-tunnel`; cross-check `ps` PIDs for staleness (an old PID surviving kickstart means kill + kickstart — see deploy note below).
3. **Seat liveness — probe CLASS must match seat CLASS, never one probe for all seats**: HTTP-listening engines get `nc -z -w1 127.0.0.1 <port>` (Goethe 8120, Bell 8121, Luria 8122, Wernicke 8124, Tawara 8128, Andreasen 8108, Da Vinci 8116, Hall 8089, Harvey 8092); portless desktop apps (Muse is `/Applications/Muse.app`, deliberately no listening port) get a PROCESS check (`pgrep -f Muse.app`), never a port probe — a port probe on a portless seat reports a live seat as dark, and the false reading then propagates into every census/list that trusted it; CLI bench seats get `which`-path checks. Canonical per-seat-class census: `/<workspace>` (engine health, process, and which-path classes) — run it instead of hand-probing; its pool (`organism/model_selection_organ.json`) is where a new seat must be registered or it is invisible to every enumeration. **Probe class must match seat class**: port/HTTP probes are for engines only — app-based actuation organs (desktop-app seats) have no listening port by design, so probe them by process (`pgrep -if '<app name>'`), CLI bench seats by path (`which <cli>`). A port probe on a no-listener organ reads dark while the organ is live, and every census list built from that probe silently drops it.
4. **Content, not status codes**: grep the boards HTML for real render markers — `Tap to copy` (title case; a case-sensitive lowercase grep returns 0 and reads as a dead page) on `/comments`, "Art Division" on `/art`. A 200 error shell still says 200.
5. **Production heartbeat**: last rows of `gg_posts` in the live `writing-studio/linkedin_metabolism.db` — schema is `ts, for_date, pillar, body, source_title, source_url, panel_verdict` (no `created_at`/`text` columns; ORDER BY ts, text from `body`) — the nightly metabolism kept producing through the window or it did not; a dated row is proof of life. Same DB: `follow_strength_log` row count + latest (ts, band, outcome) proves the quality gate still enforcing.
6. **Bus evidence for outage truth**: query `message-bus.db` messages DESC — `messages` columns are `timestamp, from_op, to_op, msg_type, subject, content` (a `sender`/`topic` SELECT errors out). ws-guardian rows carry `REBOOT DETECTED` / `dark <minutes>` (FileVault gate = studio dark from boot until first login even with launchd showing the label), glia starvation alerts, Triangle re-admit rows. The bus is the source of record for WHEN and WHY; surfaces only prove NOW.
7. **Build-engine status** (when the ask is "status of all the things", not just "is it up"): sibling DONE handoffs today (`messages WHERE msg_type='handoff'` from the sibling, DESC — each row names a task id + verdict), the task ledger split (`state='done'` vs `'open'`/`'claimed'` for today's id prefix), and the alert rows (`msg_type='alert'` last 24h — claim-watchdog `dispatch-without-claim`, canary trips, law-block pin drift). Before reporting the ledger split, close input-gate rows whose questions were already answered in-channel — an answered-but-open row inflates the open count and the board lies until synced (answer-writeback mirror law in task-ledger-hygiene); sweep first, count after. Sync procedure: read the 24h open-window rows BEFORE classifying any as pending, close answered ones `state='done'` with outcome text naming WHAT shipped (sha/artifact/bus row — the outcome is the receipt, never "handled"), batch via a written script file (the terminal guard blocks inline payloads referencing the >1MiB ledger DB; also quote-escape outcome strings — an apostrophe inside a single-quoted SQL literal kills the whole batch with SyntaxError/OperationalError), catch per-row errors so one bad id never aborts the batch, then re-census and report the TRUE remainder. Only genuinely-unbuilt work stays open; echo/duplicate rows close citing their canonical row. Report open flags honestly from those rows, never filtered to green.
8. **Report shape**: surfaces → processes/organs → heartbeat → build engine → open flags, then name what waits on the principal (pending cards, flagged claims). Testimony outranks sensors: if the principal saw a specific failure, ask which surface and pull its logs — a clean sweep never overrides their report.

## Pitfalls
- **An operator redeploy is a ~5s blip the principal can perceive as downtime** — kickstart while filing a board card restarts the boards server. Before attributing an outage, check the bus guardian rows for the real window.
- **After a Mac reboot the studio stays dark until first login** (FileVault); ws-guardian's "heralded reboot (dark ~Nm)" row is the authoritative record — do not re-derive it from probes.
- **401 from the studio without a token is ALIVE**; only connection-refused/timeout counts as down.
- **kickstart can leave a stale PID serving**: if the new route 404s after an edit, kill the old PID, accept the brief downtime window, kickstart again, verify the route returns 200 with expected byte size.
- **Never reuse the previous sweep's numbers** — re-probe everything in the same turn as the answer; parroted counts are a standing law violation.
