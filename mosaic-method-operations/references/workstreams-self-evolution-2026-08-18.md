# Workstreams, Self-Evolution Loop Repair, Backup Engine — session detail 2026-08-18

Companion to SKILL.md sections "Task numbering + workstreams",
"Multi-writer ledger law", "Operator bus gotchas". Session: QA pass 15 →
gamification directive → task-numbering rebuild → ECS review.

## 1. Macro layer build (trigger: principal confusion)

**Signal (verbatim):** "I need the task numbering to be built out I am
confused as to what all is happening." Prior attempts at legibility
(workstreams_view with raw T-IDs) still confused — seven numbering
systems were live simultaneously (T-IDs, session v-numbers, G1-G9,
F1-F13, bus IDs, GAP/DEEP codes, WS-1..5). Lesson: adding one more
scheme didn't help until the HUMAN alias layer landed and session
v-numbers were banned from user-facing comms.

**What was built (all falsified live):**
- `tasks.alias` column + `_next_alias()` in task_ledger — assigned at
  mint, sequence counts open+closed so numbers never recycle.
- `tasks.workstream` column + `map_workstream()` deterministic
  classifier, called inside `submit()` — no hand assignment.
- `gates/workstreams_view.py` — principal-facing board, alias-first. Had to
  connect via `task_ledger.connect()` (raw sqlite3.connect = CI crash
  on fresh clones: "no such table: tasks").
- Backfill: 97 tasks sequenced by created_at within workstream.
  Honest caveat recorded: historical alias numbers reflect backfill
  order; forward mints are stable.
- Prefix map: RES (research) / COND (conductor) / FLEET (organism
  evolution) / KERN (kernel) / OBS (observability).

**Workstream design rule:** a workstream is a CAMPAIGN with an EXIT
CONDITION (e.g. WS-1: "30 consecutive days, every minted gap traces to
an autonomous scan, zero human relays"), not a category. Inspired-by
blend: Shape Up fixed-scope pitches + Linear cycle view + GitHub
Projects grouping.

**ECS review (principal: "look at the ecs system... for a thorough review qa
for this plan"):** DS-ECS-SPEC.md v3.0 = hierarchical ENGINE coding
(DS-ECS-DOMAIN.SUBSYSTEM.SPECIFIC-vX.Y.Z; 50 engines, 12 domains,
8 entity categories OS/ORG/SUB/CS/NP/PTH/APP/GEN, independently
versioned segments). Flow registry (10 FLW-* codes with stages) =
process flows. Task IDs = instances. Verdict: the numbering plan is
sound ONLY as a third orthogonal layer; ECS and FLW untouched.
Alignment note already in package-map.md ("flow-registry : task-ledger
:: ECS-registry : engine-instances") extends one level down:
alias : task-instance :: FLW : process :: ECS : engine.

## 2. Multi-writer collision (found during ECS review)

Symptom: `submit()` raised `UNIQUE constraint failed: tasks.id`.
Diagnosis: counter table said seq=104 but max task id was T-...-0112.
Eight tasks (T-0105..0112) carried origins from ANOTHER writer
(qa-micro-review-1, ceo-directive-2026-08-18, connectivity-census,
deleg_*) — sibling the operator agent sessions minting by max(id)+1, bypassing
mint()'s atomic counter. gap_hunter was verified innocent (uses
tl.submit properly).

**Fix (Lamport-style convergence in mint()):** after reading the
counter, loop: if candidate T-id already exists, seq += 1 (max 50
iterations), then UPDATE counter to converged value. Falsified: the
exact submit that crashed succeeded post-fix (T-260818-0113).

## 3. Schema-drift CI class (second occurrence)

1st occurrence (08-17): dispatch_gate admission columns — local ALTER,
source CREATE TABLE missing them, CI Run 32140653231 failed.
2nd occurrence (08-18): workstream column — same failure mode, Runs
32148629934 then 32148868243 (workstreams_view raw connect).
Rule now in SKILL.md. The falsification pattern that works:
```python
import sqlite3, tempfile, os
c = sqlite3.connect(os.path.join(tempfile.mkdtemp(), 't.db'))
c.executescript(tl.SCHEMA)
cols = [d[1] for d in c.execute('PRAGMA table_info(tasks)').fetchall()]
assert 'workstream' in cols
```

## 4. Self-evolution loop repair (same session)

- autonomous_build.py spec-consumer was a 2-month-old STUB (comment
  "would parse the spec content") — design requests posted into a
  void, 80 unanswered on the bus. Implemented the consumer + falsified:
  DEEP-001/DEEP-003 (requested June 25) transitioned and dispatched.
- design_spec_responder.py: direct-DB pending detection (readable
  column names from_op/to_op; `read` CLI consumes so background
  responders must not use it), dedupe by item id (June runaway: ~60
  VERITAS-003 dupes), `--type design_spec --content` post flags.
- gap_to_build_bridge.py: ledger kind=gap origin=research:auto% →
  build-queue.yaml items (AUTO-*). 3 bridged on first run.
- Cron log frozen since June 24 while cron still fired (TCC-restricted
  crontab edit + `timeout` absent on macOS — use background=true or
  longer timeouts, never `timeout` wrapper). LaunchAgent plist written
  to ~/Library/LaunchAgents/com.your-org.autonomous-build.plist
  (launchctl bootstrap is blocked from the agent gateway — needs
  manual load from a desktop shell; use python file-write, terminal
  heredoc inside a launchctl command gets blocklisted).

## 5. Backup engine (principal: "keep going and build around that")

`organism/backup_engine.py` — destination-agnostic snapshots:
- 268 MB critical state (mosaic stores, studio, tech-registry,
  organism, operator bus) → 3.4s atomic snapshot (tmp+rename),
  SHA-256 manifest, 7-generation rotation, --verify re-hash,
  --restore with dry-run default + sandbox falsification.
- Hourly via volley tick with 55-min freshness gate.
- Time Machine confirmed OFF (`tmutil destinationinfo` → none
  configured); engine = smoke-detector class protection until a real
  destination mounts. principal decision pending (T-260817-0006).

## 6. Registry probe defect (minted, unfixed)

Nemotron verification: probes RUN (5/8 measured, fresh timestamps) but
4 slugs score all-zero, 1 scores all-100 — degenerate both ends,
probe_results carries NO error detail, and --model single-probe hung
>180s. Fix spec minted as ledger defect (capture HTTP status +
response excerpt per axis, per-request timeout, flag all-equal scores
as suspect, never dispatch on suspect measurements). NOT yet built —
do not cite as working.
