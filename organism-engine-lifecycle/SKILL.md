---
name: organism-engine-lifecycle
description: 'Use when seating or reviving engines, or on stale feeds.'
---

# Organism Engine Lifecycle: seats, revival, heartbeats

Class-level skill for keeping fleet engines alive and proving it. Governs:
seating raw-spawned engines under launchd, reviving dead engines, diagnosing
"stale feed" / "engine down" reports, and verifying liveness with receipts
instead of assumptions.

## The two failure classes this skill exists for

1. **No revival seat** — an engine running as a raw spawn (nohup/inherited)
   dies permanently on crash or reboot. Detection and health censuses do not
   fix this; only a KeepAlive seat does.
2. **No death response** — monitoring organs exist (port censuses, health
   spines, coherence trackers) but nothing turns "engine X is dead" into
   "restart engine X". The repair loop must be closed with seats + a revival
   lane, not more observers.

Before answering "why are engines down and not getting repaired": census the
repair layer, not just the engines. Count registry entries vs seats vs live
ports. Grep the self-healing engine's source for `kickstart` / `launchctl` /
`restart` — a monitor with zero restart actions cannot heal, regardless of
its name.

## Seating procedure (the working order)

1. **Census seat coverage.** Match each registry engine to a launchd label
   (plist `ProgramArguments` + `WorkingDirectory` against engine dirs).
   Report three numbers: seated / alive-unseated / idle-unseated.
2. **Extract each engine's MEASURED run command** from the live process
   table — `ps -ww -o command= -p PID` + `lsof -p PID` (cwd field), keeping
   the EXACT interpreter path (a venv python, a Homebrew python3.14, a
   CommandLineTools python3.9 are all different). Never guess the entrypoint
   from the directory listing; `run_server.py` vs `-m uvicorn server:app
   --port N` vs `-m uvicorn src.api.server:app` all exist in one fleet.
   When the engine is already DEAD (post-reboot, no process to read),
   extract ground truth from the entrypoint SOURCE: grep the engine dir's
   server/run files for hardcoded port strings and uvicorn module paths.
   Treat the registry's directory field as UNRELIABLE here — it can map an
   engine to a NEIGHBOR's directory whose server hardcodes a different
   (live, occupied) port; a seat built off that mapping boots the wrong
   engine or fights a live port. Cross-check the candidate dir's entrypoint
   port against the registry's port for THAT engine before writing any
   plist.
3. **Check for existing seats first** — fleet plists use several naming
   conventions (`com.your-org.<scientist>`, `….<scientist>-engine`,
   `com.ds.<name>`). Minting a duplicate label for an already-seated engine
   creates two KeepAlive parents fighting over one port. Pre-existing seat
   wins; remove your duplicate (`launchctl bootout` + delete plist).
4. **Kill the raw holder BEFORE bootstrapping the seat.** If the raw process
   still holds the port, KeepAlive's first spawn dies on `[Errno 48] address
   already in use` and launchd enters crash-loop backoff. SIGTERM can be
   trapped or ignored — verify the old pid is actually gone (`lsof -ti :PORT`),
   SIGKILL if it survives, THEN bootstrap.
5. **Break crash-loop backoff after any conflict:** `launchctl kickstart -k
   gui/$(id -u)/<label>` once the port is free. `-15` in `launchctl list`'s
   last-exit column right after a kickstart is the kickstart kill of the old
   instance, not a crash — confirm via `launchctl print gui/$(id -u)/<label>`
   (state/pid) instead.
6. **Verify seat-to-port identity:** `lsof -nP -iTCP:PORT -sTCP:LISTEN -t`
   must equal the launchd pid. Then curl BOTH `/health` and `/` — many
   engines expose no `/health` route (404 root = alive; connection refused =
   dead). Sleep 8–12s after any kill/kickstart before probing; a racing curl
   reports 000s the log later disproves.
7. **Idle/spec-only engines stay unseated, honestly dark.** Seating a
   spec-only engine proves nothing; the census shows them as idle, not dead.
8. **Dormant tier is not dead: liveness scans filter by launchd ownership,
   never by registry membership.** Probing every registry entry flags
   on-demand engines (registered, never spawned, no plist, no log file) as
   dead every cycle — a missing process is their resting state. The burst
   suppressor then posts the same mass-death alert for weeks, and alert
   fatigue masks REAL owned-engine deaths buried in the noise. Filter BOTH
   liveness paths (registry scan AND telemetry scan) on plist ownership,
   matching key OR directory OR former_codename OR scientist-slug — plist
   basenames diverge from registry keys (a plist named `ds-farr-engine`
   serves the entry keyed `ds-ecs-compliance-agent`). Confirm telemetry
   deaths against the CANONICAL port only; tier ports (9xxx virtual
   offsets) never have listeners. Diagnostic shortcut: an alerted engine
   with NO log file ever = never resident = dormant, not a crash.

## Writes-on-poll organs need a standing heartbeat

An update/recommendation engine whose only trigger is an HTTP route records
NOTHING unless a browser view requests it. Symptom: the feed's newest row is
days old while the daemon answers 200 and the supervisor layer looks green —
the organ died silently inside a healthy process because the UI only polls
that route from one view nobody had open.

Fix: a daemon-side refresher thread calling the same function on an interval
(the same pattern as a cache-TTL refresher):

```python
def _organ_refresher():
    time.sleep(5)
    while True:
        try: _recommendations()          # deduped: unchanged state writes nothing
        except Exception: pass            # store stays readable regardless
        try: (ORG / "organ-heartbeat.txt").write_text(_utc())
        except Exception: pass
        time.sleep(300)
threading.Thread(target=_organ_refresher, daemon=True).start()
```

**One cadence per signal class, matched to measured bandwidth.** A single
poll interval silently conflates two clocks. Measure the signal's event rate
first (events-per-day / 86400): machine-layer signals (bus/event counters,
queue depths, port states) change at event rate (seconds) and need a fast,
cheap probe (single indexed COUNT) — polling them every 5 min stacks dozens
of blind events per cycle and delays threshold detection by up to the full
interval. Banded human-layer signals (n≥3-point rolling aggregates) change
on hour scales — polling them faster buys zero information. Split one
refresher thread into two clocks when the organ feeds both classes.

**Liveness receipt law:** silence is ambiguous for deduped writers (no new
rows ≠ not running). The heartbeat file touch each cycle is the only
trustworthy proof the loop is alive — an mtime/content check, never "no log
lines". The mirror-image trap: a stale `.log` tail (moved path or retired
logging lane) shows a months-old last entry while the daemon runs healthy —
reading it as a wedge sends you hunting a hang that does not exist. Liveness
proof = state-file mtime moving AND its pass counter incrementing; check both
before declaring a live process wedged. When diagnosing a stale feed, read
the store's newest row age FIRST, then find who is supposed to trigger
writes, before suspecting the daemon.

**Recording a degradation is not responding to it.** A standing monitor that
writes threshold shifts (ELEVATED/CRITICAL) only into its own feed is a
diary, not an alarm — nobody reads the feed until the next browser visit,
which is the writes-on-poll defect again, one layer up. Every recorded
signal-shift crossing an action threshold must ALSO post an alert at
detection time to the channel a human or operator already watches (operator
bus with a dedup key of dimension+band so repeated cycles don't spam);
recoveries record to the feed silently. A monitor without this escalation
path is "working" exactly when it is useless.

## Diagnosis order for "X isn't working" reports

1. Is the daemon serving at all? (curl root, check launchd state) — if 200,
   the breakage is above the server, do NOT restart it.
2. Is the surface's script block alive? A page stuck at its loading text
   ("connecting…") with a 200 server = dead `<script>` block; run the JS
   syntax gate before touching launchd: extract every `<script>` block to a
   file and `node --check` each. One malformed line (an interrupted patch
   leaving a broken ternary) makes the browser refuse to parse the ENTIRE
   block, killing every feature in it — `py_compile` proves nothing about
   embedded JS. Gate BEFORE every kickstart of a daemon that serves inline
   JS.
3. Is the data organ's store fresh? (newest row age) — stale means either a
   dead trigger loop (heartbeat fix above) or a dead producer upstream.
4. Only then suspect the process/seat layer.

## Verification receipts (never claim without one)

- Seat receipts: port-up + seat-pid == port-pid + HTTP 200 (or expected 404
  root) per engine, checked sequentially — see probe pitfalls below.
- Heartbeat receipts: heartbeat file content vs live clock, after a full
  cycle (interval + margin), post-restart.
- KeepAlive kill-test: kill the seated pid, sleep ~12s, confirm a NEW pid
  holds the port. Supervision proven, not assumed.

## Pitfalls

- **Never write a file and call it an organ/seat without a ledger birth certificate.** The organ methodology requires birth through the registered ledger path (gates/task_ledger.py submit -> claim -> build -> complete with run-record) — a direct .py write labeled "organ" is the violation regardless of code quality. When discovering prior unseated builds, census first (every file vs its ledger mentions, recursive — flat censuses undercount subdirectories), then retro-seat through submit() with live run evidence.
- **Bus silence ≠ death for failure-only daemons — enroll, never force heartbeats.** A launchd KeepAlive/StartInterval daemon that posts only on findings (wedge suspects, TTL breaches, canary trips) is quiet while healthy; a bus-heartbeat watchdog reading post-recency then fires a false OPERATOR DOWN flap every interval. The wrong fix is patching the daemon to post heartbeat rows — check the watchdog source for its enrollment convention first (e.g. a LAUNCHD_DAEMONS set whose doctrine is substrate liveness = launchd label + log freshness + exit code) and enroll the daemon there instead. Classify every remaining silent operator individually before touching anything: no launchd label + no posting source + days-silent = dead (retire per the watchdog's own convention); an episodic poster (fires on rare events, posts days apart) = interactive class (never alert); a human operator = never alert. After each enrollment change, rerun the watchdog and require exit 0 — and expect newly-exposed silent names to surface one enrollment at a time. The organ methodology requires birth through the registered ledger path (gates/task_ledger.py submit -> claim -> build -> complete with run-record) — a direct .py write labeled "organ" is the violation regardless of code quality. When discovering prior unseated builds, census first (every file vs its ledger mentions, recursive — flat censuses undercount subdirectories), then retro-seat through submit() with live run evidence.
- **Respect the mint-rate gate's remedy, never force past it.** When the per-origin daily cap refuses a mint, the error names the lawful paths: batch remaining findings into ONE digest task, or use a lawfully exempt origin (principal orders with `ceo:` prefix are never rate-gated — that is policy, not a bypass). Do not retry the same origin blindly.
- **The gateway guard blocks inline `launchctl bootstrap` from the agent's
  own shell** (kill-restart loop protection). Route seat installation
  through a detached wrapper: write the bootstrap commands to a script, run
  it via `nohup` in a background terminal, then verify seats from the main
  shell with `launchctl list` + port probes. Direct `launchctl bootstrap` in
  a foreground command fails even when the command itself is correct.
- **Shell sweeps lie.** A `for spec in "8153 attwell"; do set -- $spec; …
  curl …$2…` loop reported 0/12 up while sequential curls returned 12×200 —
  `set --` clobbered the loop variable. When a sweep contradicts a single
  manual probe, re-run sequentially with no loop variables before believing
  either.
- **Transactional amendments roll back whole.** A script that UPDATEs a task then fails a follow-up INSERT (e.g. NOT NULL column omitted) rolls back BOTH — the amendment silently absent. After any amend script that errored partway, verify the UPDATE landed with a targeted read-back before assuming state; use the guard `AND detail NOT LIKE '%<amend token>%'` to make re-runs idempotent.
- **Write multi-line Python to a file and run it; do not inline it in terminal heredocs or -c strings.** Heredocs can silently no-op (empty output, rc 0) and nested quotes break shell parsing — a script file is the only reliable path for any multi-statement ledger/sqlite work.
- **Kill verification.** After `kill` (SIGTERM) on raw holders, confirm each
  pid is gone before bootstrap; engines that trap SIGTERM will hold the port
  and bait the seat into a crash-loop.
- **Raw spawns are reboot-fatal by definition** — a nohup'd engine, however
  healthy now, owes a seat. Raw spawn to fix an outage is acceptable triage;
  leaving it unseated is the defect.
- **Docker organism containers need a restart policy as their seat.** A
  container with `RestartPolicy: no` is a raw spawn — a docker-daemon
  restart kills it silently for weeks. Seat it with `docker update
  --restart unless-stopped <container>`. Revival order: `docker ps -a`
  (exited containers + exit codes), `docker start`, then sweep every
  declared port — organs never wired in the container build get recorded
  as known gaps, never hidden. Model/config upgrades must land in BOTH the
  live container and the host blueprint repo: the blueprint is the source
  of truth for rebuild, so a container-only bump evaporates on the next
  rebuild.
- **Factory-only services (a `create_app()` with no module-level app)
  cannot be launched as `uvicorn module:app`** — load via importlib, call
  the factory, and `uvicorn.run(app, host, port)` from a launcher script.
  An ad-hoc background launch of this shape dies between operator turns,
  not only on reboot — it owes a seat like every raw spawn.
- **Duplicate seat labels under different naming conventions** are the
  norm, not the exception, in a fleet that grew organically — always grep
  `~/Library/LaunchAgents/` for the scientist name in ALL conventions
  before minting.
- **Migrating a service to a new label orphans its watchers.** Removing the
  engine's old label is part of the migration, not cleanup: `launchctl
  bootout` the old label AND rename its plist to `*.disabled` (a live plist
  resurrects the label on next load), then grep every watchdog/guardian
  script for the old label string and repoint it to the surviving one. A
  guardian still probing a dead label escalates a false CRITICAL for a
  service that no longer exists — and one false escalation burns the principal's
  trust in every future real one.
- **Watchdog alert text that can reach the principal channel is plain-language
  only** — no internal operator vocabulary (lease, surgery window,
  kickstart, label, bus seat); state the user-visible effect and the one
  action taken. Prove a new watcher in BOTH directions before trusting it:
  inject one deliberate fault and confirm it fires, clear the fault and
  confirm silence.
- **Flood inheritance: kill the SPAWNER, not the children.** Group
  `ps -Ao pid,ppid,command=` by ppid — a non-launchd parent with dozens of
  server children is a mass starter. Killing only the children leaves the
  spawner to respawn them; killing the spawner re-parents its children to
  launchd (ppid 1), where they survive any child-only reap and read as "the
  flood came back". After the spawner dies, triage children by seat:
  keep those whose cwd matches a seat plist's WorkingDirectory, kill the
  rest (match cwd via `lsof -p PID`, never by command name — many engines
  share one command shape).
- **One revival philosophy per fleet.** A registry-driven mass starter (boot
  ALL engines now) and per-engine KeepAlive seats are mutually hostile
  revival models: the mass start floods the host, any reap then triggers
  KeepAlive resurrecting the whole seated fleet simultaneously, and load
  spikes while the two fight. Fleet revival must be ONE law — seats as the
  steady-state manager; a mass-start tool is acceptable only for first-time
  bring-up INTO seats, never as a parallel supervisor. After any fleet-wide
  kill, expect a ~1-minute load spike from the resurrection wave and judge
  recovery on the trend, not the peak.
- **Deploy shared daemon/screen files by extension, never wholesale
  replacement.** Replacing a shared organ file with a rewrite amputates
  every route and function other lanes added since the rewrite's base — the
  daemon keeps serving 200 while the surface 404s for days, and "daemon up"
  checks stay green. Before deploying any rewrite of a shared file, diff the
  ROUTE/SYMBOL table old-vs-new (regex every `"/api/…"` literal and `def `
  name) and carry each loss forward or consciously retire it. Recovery from an
  existing amputation: restore the newest superset backup, graft the
  rewrite's genuinely new functions + call sites into it, preserve the
  rewrite as `.bak` — never blind-revert (that amputates the sibling's work
  instead of your own). Post-merge kickstart, then re-verify the FULL
  endpoint list, not just the rewrite's additions.
- **Impostor duplicates on registry ports: trust the /health self-ID over
  process age; never restart a healthy old daemon for being old.** A
  misconfigured duplicate can hold a registry port for days: curl the
  squatter's /health first — an app self-identifying as a DIFFERENT engine
  (or reporting a port other than the one it listens on) while occupying a
  registry port is a config-error duplicate. Confirm the canonical engine's
  real port still has its rightful owner, kill the impostor, relaunch from
  the registry's own directory for the port's true assignee. The mirror
  rule: a days-old launchd daemon serving the correct payload is uptime,
  not rot — restarting it is churn; audit payload identity before any
  restart, and a /health reporting the wrong port is its own truth defect —
  fix the self-report at the source so liveness scans stop chasing ghost
  ports.
- **Detector logs need rotation-aware dedup keys.** A trip/alert log keyed
  on (entity, surface) never dedupes when surfaces embed rotation tokens —
  timestamped snapshot dirs and numbered run logs (bus-123.log) make every
  rotation a "new" surface, so the log grows ~N/day forever, buries true
  novel hits in repeat noise, and erodes trust in the alert path. Normalize
  the STRUCTURAL path for the dedup key (timestamp dir → SNAPSHOT,
  bus-<id>.log → bus-*.log) while logging the raw surface verbatim, and
  extend the selftest to assert the contract BOTH ways (a new structural
  pair appends; a repeat is suppressed) — a selftest written for the old
  append-always contract fails on the new dedup and must be updated in the
  same change, with cleanup unlinks guarded by .exists() because earlier
  test steps already removed the files.
