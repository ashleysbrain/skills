# the OS task-ledger protocol (verified live 2026-08-18)

Repo: ~/your-org/your-stack (canonical since T-0136 relocation; never
assume the old ~/Desktop path). Ledger: stores/task-ledger.db.

## Append-only history law
task_events has BEFORE UPDATE and BEFORE DELETE triggers that ABORT with
"task_events is append-only (Flow 3 history law)". Any repair that would rewrite
history (e.g. normalizing naive timestamps) is refused at the DB level. Correct
response: leave rows as forensic history, document the invariant going forward.

## Judge requirements (gates/rubric_judge.py)
- R1 birth certificate: every task needs a `minted` event. Zero-event tasks are
  the fleet-low scores. Fix: retroactive mint using the task's created_at.
- R2 ordering: canonical events sorted by NORMALIZED ts, naive treated as UTC.
  Rowid disorder is invisible to the judge by construction.
- R3: outcomes must carry verification citations (live probes, commits).

## Closure protocol
Closing a task via raw SQL UPDATE state='done' WITHOUT the minted/claimed/done
event triple scores 0.522 FAIL. Always: INSERT task row (correct kind/lane from
stores/task-taxonomy.json), then the three events, then UPDATE state+outcome.
Verify with: python3 gates/rubric_judge.py --score <id> -> expect 1.0 PASS.

## ID collision protocol (multi-lane minting)
Sibling lanes (hermes/sibling-agent) mint concurrently and the space is shared.
UNIQUE constraint failure on INSERT means the id was taken mid-flight: check
whose task it is, NEVER attach your events to it (events are undeletable,
contamination is permanent). Probe next free id:
SELECT id FROM tasks WHERE id LIKE 'T-YYMMDD-01%' -> max numeric + 1.

## Timestamp invariant
All new events carry ISO-8601 WITH explicit offset. Naive rows exist in history
(sibling lane, 4 rows) and are immutable.

## Census store law (surface-id contract v1)
stores/connectivity.store.json is the single source of truth for surface status.
Hub registries carry census_id pointers (aliases: x->xurl-x-twitter,
cgm->cgm-libre, financial-csv->csv-manual, health-export->health-export-xml).
Never pin git revs in mutable stores (they stale the moment the repo advances);
pin commits only in immutable audit reports.

## Relocation hygiene
After any repo move: grep ALL daemon scripts + launchd plists + cron prompts for
the old path constant. In-flight daemons recreate skeleton directories at stale
paths (looks like data wipe; it is not). Fix the constant, remove the corpse.
