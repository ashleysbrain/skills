# Mint-Loop Amplification Cascade (2026-08-21 falsification pass)

principal trigger: "will this junk up our process flows like this?" — answer
was yes. Adversarial pass found a 4-stage cascade; root causes fixed at
the source, never downstream. 86 junk tasks cancelled across 4 rounds.

## The cascade chain

```
improvement_scan S8 (dedupe dead: queried nonexistent `state` column)
  -> re-minted 9 orphan principal directives EVERY run
     -> gap_cycle minted BUILD tasks for them
        -> sandbox_engine minted QA twins for each BUILD
           -> cleanup CANCELLED the dupes
              -> gap_cycle's lineage dedupe EXCLUDED 'cancelled'
                 -> re-minted a 4th copy -> fresh twin -> loop
```

## Defect-by-defect (root causes, all live-verified)

1. **S8 dedupe dead since birth** (`improvement_scan.py`
   `open_prefixes()`): `WHERE state IN ('open','claimed')` — the tasks
   table has BOTH `state` and `outcome`; the query targeted the wrong
   one for this corpus and returned empty forever. Fixed to
   `outcome IS NULL/''` + fallback. Proof: dry-run reports
   "8 already-open, 0 minted" (N=3).
2. **gap_cycle lineage dedupe semantic bug** (`gap_cycle.py`
   `_already_minted()`): counted lineage only in
   `open/claimed/done`, with the comment "'cancelled' does NOT count
   (dupes must re-mint legitimately)". Falsified: cleanup cancellation
   un-deduped the canonical → 4 BUILDs per canonical in lineage. Fixed:
   lineage scan counts ALL states. Proof: 59 open gaps, dry-run N=3 →
   minted=0 closed=0.
3. **sandbox_engine liveness rule wrong** (`qa_intake_fresh_gaps`):
   checked `outcome in ('cancelled','done')` but the conductor writes
   free-text "DEDUP ..." notes into `outcome`. Fixed: any non-empty
   outcome = dead source.
4. **Bus schema drift in 2 daemons** (circadian_conductor,
   sandbox_engine): emitted with `who/kind/payload`; real bus schema is
   `from_op/to_op/msg_type/subject/content`. try/except swallowed it —
   visible ONLY as "bus emit failed ... no column named who" in the log
   tail. Fixed both; live proof by invoking the real `pass_lane()` code
   path: bus row 2761 landed (from_op=ds-hall,
   msg_type=circadian_checkpoint).

## Cleanup pattern (repeatable)

Cancel with event-trail notes (never delete): UPDATE state='cancelled'
+ outcome carrying the reason + task_events row. Rounds 1-2: 56 tasks.
Round 3: 15 stragglers. Round 4: 25 dead-source twins killed by joining
twin -> source liveness:

```sql
SELECT t.id FROM tasks t
WHERE t.origin LIKE 'sandbox:qa-intake:%'
  AND t.state IN ('open','claimed')
  AND NOT EXISTS (SELECT 1 FROM tasks s
                  WHERE s.id = substr(t.origin, -13)
                    AND s.state IN ('open','claimed'));
-- must return 0 rows at steady state
```

Steady state after: 6 live twins (all live sources), 5 canonicals with
exactly 1 live build, 9 canonicals correctly held by cancelled lineage.

## Idempotency proofs (Deming N>=3)

- `gap_cycle.py --dry-run` x3: minted=0, closed=0, open_gaps=59 stable.
- `sandbox_engine.py --once` x3: qa_intake=0, mycelium=3 nodes,
  roadblocks=0. (First run after the source-patch minted 1 LEGITIMATE
  twin — its source T-260820-0166 was genuinely live. One mint from a
  live source is correct behavior, not junk.)
- JSON shape gotcha: parse the tool's ACTUAL output keys first
  (`qa_intake` is an int, not a dict) — read one raw output before
  writing the parse one-liner.

## Daemon install notes (same session)

launchd installs via browser_exec separate-process shell worked
first-try for both daemons (rc=0, PIDs live). circadian LANES:
am-review=7, midday-pulse=12, pm-review=17 local; a quiet log after
restart is CORRECT lane logic when today's lanes already passed — prove
the fixed emitter by calling the real code path, not by waiting for the
window. GENOME gate independently rejected stale blocks with trailing
periods ('intellectual.' not a canonical dimension) — gate healthy.

Ledger steady-state + run record: `your-stack/audit/RUN-RECORD.md`
entries 2026-08-20/21.
