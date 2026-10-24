---
name: sensor-validation
description: "Use when trusting or building gauges. Verify by execution."
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [monitoring, gauge, watchdog, verification, dead-code, sensors]
    category: devops
---

# Sensor Validation — verify the watchers themselves

Monitoring code fails SILENTLY: a broken gauge looks identical to a clean
one in every log. Before trusting any sweep, watchdog, or threshold check —
yours or a sibling's — run this battery. A monitoring promise in a docstring
or comment is a claim, not a sensor.

## When to Use

- Building or inheriting any watchdog, hygiene sweep, or threshold gauge
- Diagnosing "why did no alert fire" after an incident
- Reviewing a sibling's monitoring code before depending on it
- Post-incident when a monitored value silently crossed a limit

## Procedure (in order)

1. **Docstring vs body.** Grep the function body for every check the
   docstring or header promises. A promise ("checks memory usage",
   "alerts on stall") with no implementing code is decoration — nothing
   errors because the code that exists runs clean.
2. **Dead-trigger scan.** For every boolean that gates whether monitoring
   fires, grep ALL assignments to it. Only ever `False` or initialization =
   the scheduled work is inert. The tell is compute-and-discard: a value
   computed (`age_h = ...`) then never compared or assigned into the gate.
3. **Phantom-literal scan.** Grep each literal the checker requires against
   the live corpus it polices. A zero-match literal manufactures a finding
   on every run — permanent false positives train operators to ignore the
   sensor, which then masks the one true finding that matters. Replace
   paraphrased expansions of a source's rules with tokens copied VERBATIM
   from the source file.
3a. **Zero-count-through-a-storm falsification.** A sensor that reports 0
   events while the raw source visibly overflows with them is worse than a
   broken sensor — it is a CONFIDENTLY WRONG one. When a counter reads
   zero, grep the raw log for the last N matching-looking lines and diff
   the sensor's regex against the actual text: real sources emit multiple
   DIALECTS of the same error (bare JSON `"code": "1302"` alongside
   `Error code: 429` and quoted-dict `'code': '1113'`), and a pattern list
   built from one dialect silently under-counts the others. Copy every
   observed dialect verbatim into the pattern list. Check the window filter
   with the same lens: a timestamp format that parses (space→T for
   fromisoformat, comma-milliseconds) can still yield zero in-window events
   if the cutoff comparison is computed in the wrong unit or against the
   wrong reference frame — assert one known-stamped line lands inside the
   window before trusting any window count.
4. **Seeded run.** Put one monitored thing in a known-bad state (one store
   above threshold), run the check directly, and require findings to map
   1:1 to true positives. Empty findings on a seeded breach = the check
   cannot fail (vacuous verification).
5. **Trigger-vs-live-state.** Restart the owning daemon, then evaluate the
   gate's logic against live state and assert it computes `True` when the
   seeded condition holds. A correct trigger in an un-restarted daemon is
   still running the old code.
6. **Silent-subprocess check.** If a daemon invokes the sweep via
   `capture_output=True` with no exit-code check, a broken sweep is
   indistinguishable from a clean one — run the sweep binary directly and
   read its findings before believing the daemon's log.
7. **Advice-vs-evidence audit.** Grep every alert template's advice clauses
   and ask what sensor output PROVES each one. Advice derived from a regex
   over upstream MESSAGE TEXT inherits the upstream's mislabeling — a
   rate-limit error whose canned text says "insufficient balance" classifies
   as a balance problem, and the alert then tells the operator to recharge a
   funded account. Classify on structured status codes where they exist; when
   only text is available, gate any resource/balance/capacity advice on a
   direct probe of the real endpoint before the alert may word it. An alert
   channel that fires inaccurately loses its privilege to fire at all:
   silence the misfiring template first, repair the accuracy, re-arm only
   with proven numbers — a source-mute that already failed once means the
   fix must be structural (terminal-state the stale records), not another
   mute.

## Repair order (binding)

Consolidate the damaged stores FIRST, then repair the sensor, then restart
the daemon, then re-run seeded. Validating the gauge before fixing the
overflow hides whether the gauge can fire at all; the seeded re-run is the
only step that proves the repair.

## Environment pitfalls

- **Read-only WAL audits can fail at open, not at query.**
`sqlite3 file:<live>.db?mode=ro` intermittently returns `unable to open
database file` (14) while writers hold the db — this is lock contention, not
corruption. Copy the db AND its `-wal` sidecar to scratch (`cp` both) and
query the copy; committed WAL frames come along and the live file is never
perturbed. For abandoned/legacy files a plain ro-open can fail on stale
WAL-journal remnants while `immutable=1` still reads them — use immutable only
for forensic reads of stores no writer can touch, never for anything live.
- **Heavy scans on a busy live db belong in background jobs.** Full-table
COUNT/SUM(LENGTH()) over millions of rows against a WAL db with active
writers (rolling dumps, sibling processes) can exceed foreground timeouts.
Launch with background=true + notify, stream results to a scratch file, and
read the file — and budget around the competing I/O, not just the query plan.
- **Timestamps in SQLite are not always unix seconds.** Test the unit on one
row before strftime/datetime arithmetic: ms-epoch needs `/1000` inside the
formatter, and ISO-8601 text columns compare lexically against ISO cutoff
strings. A wrong unit yields empty month buckets that look like missing data.
- **Size attribution needs the measured split, not the file size.** `PRAGMA
freelist_count` = 0 means nothing is reclaimable without deletion; per-table
bytes come from SUM(LENGTH(col)) or dbstat, and event-log tables
(append-per-update) are the usual silent majority — attribute before proposing
any slimming path.
- **Symlinked trees**: `readlink` the directory before patching "both
copies" of a file — a path and its symlink target are one physical file;
  patching both applies the same edit twice. Also check which copy a running
  daemon resolves via its `WORKSPACE = __file__...` derivation before
  editing, and restart via the supervisor (`launchctl kickstart -k
  gui/$(id -u)/<label>`), not by killing the process.
- **Threshold placement**: warn-threshold belongs well below failure — a
  warn at the same level as breach leaves no consolidation runway. 80% warn
  / 92% breach on hard caps leaves one usable consolidation cycle.
- **Capacity-accounting proxy**: when a store's true char accounting is
  internal to a tool, sum non-separator line lengths as the proxy and carry
  the ~1% drift in the threshold margin; never block on obtaining the exact
  internal counter.
- **Orphan-scheduler hunt.** A state file updating on a fixed cadence with no
  locatable scheduler is an ownership defect, not a ghost. Hunt in order:
  `launchctl list` labels, LaunchAgents/LaunchDaemons plists (grep the script
  name), hermes cron `jobs.json`, sibling-agent cron stores, `daemon_loop.py`
  wrapper rosters, and cadence-citing comments in sibling scripts. If every
  register is clean, catch the writer with an mtime sting: loop
  `stat -f %m <state-file>` sleeping under half the observed cadence and
  dump the process table the moment the mtime goes fresh. Keep the process
  running while you hunt — an accurate silent witness is worth registering,
  not killing.
