# QA Fleet Mint + Ledger Laws — session record 2026-08-20 (evening)

Companion to `qa-fleet-build-2026-08-20.md`. What the fleet-ecosystem session
proved live, and the exact interfaces that bit.

## What was minted/built (parent-verified)

- FLW-QA-FLEET in `stores/flow-registry.json` (registry_version 1.2.0);
  `immune` lane in `stores/task-taxonomy.json` (v1.1.0).
- ORGANS.json 22 -> 26 organs: the specialist engine, the specialist engine, the specialist engine, the specialist engine
  (all body_system=immune, flow=FLW-QA-FLEET, with GENOME blocks).
- Idempotent mint script: `your-stack/scripts/mint_qa_fleet.py`
  (re-runnable; dedupes on seat name and ledger title).
- Ledger tasks T-260820-0145..0148 (0145 frontier lane + seats, 0146 S8 scan,
  0147 variance law, 0148 brainstorm backfill). 0145/0148 closed done with
  run-record events; 0146/0147 re-dispatched tight after first subagent
  timeout.
- Brainstorm backfill verified: seeder chain fixed (OpenAlex daily budget
  exhausted -> Crossref fallback preserving peer-review tier) and RUN:
  brainstorms 12 -> 15 real rows in `writing-studio/drafts.db`;
  session/split + session/merge routes live; Wave :port + Genesis :port
  wired; brainstorm.db empty orphan retired with README.
- Frontier lane: 8 standing queries -> 7 rows in research_scans.db
  scan_topics (created_by='qa-frontier'), zero new crons.

## Daemon wiring (how scans become 24/7)

`organism/autonomous_iteration.py` (launchd KeepAlive,
com.your-org.autonomous-iteration, INTERVAL env default 900s) runs
`anabolic_pass()` = improvement_scan.py + gates/qa_meta.py each pass. A new
scan joins BATTERY (line ~282 of improvement_scan.py) and inherits 24/7
automatically — no cron ever. Liveness = launchctl last-exit + log mtime.

## Ledger interface laws (learned the hard way)

1. `tl.complete(c, id, outcome)` fires ONLY from state='claimed'. On an open
   task it silently returns False — no error, no event. Sequence:
   `tl.claim(c, actor, actor_kind, task_id=...)` then `tl.complete(...)`,
   then `SELECT state` to verify.
2. `claim` signature: `(c, actor, actor_kind, task_id=None, lane=None)`,
   actor_kind strictly 'ai'|'human'.
3. Genome gate on kind=build requires 8d= field:
   `GENOME: body=immune scientist=DS <Name> physics="..." 8d=<dimension>`.
4. Stage vocabulary enforced per flow (set_stage warns on off-vocab);
   FLW-QA-FLEET stages: sense/appraise/mint/dispatch/verify/learn.
5. TWO task-ledger.db files exist: `your-stack/stores/task-ledger.db` is
   real; `your-org/organism/task-ledger.db` is an empty shell. Never
   guess — `import task_ledger; tl.LEDGER`.
6. Events table is `task_events` (cols: seq, task_id, ts, actor, actor_kind,
   event, detail) — not `events`, no `id`/`note` cols.

## Delegation lessons (see also subagent-anti-timeout-patterns Pattern 30)

The S8/variance build subagent burned 1800s / 47 API calls because the brief
carried a WRONG PATH (your-stack/organism/ vs organism/) and invited
"find the file" exploration. Fix: pre-verify every path in the parent
(one `find` beats 30 subagent minutes), put exact paths + line anchors in
the brief, cap ledger queries explicitly, and steer in-flight children with
delegate_task action='steer' instead of relaunching.
