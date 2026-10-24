# Scanner Pitfalls: Dedupe Keys, Whitelists, Append-Only Ledgers (2026-08-24)

Three defects caught (two self-caught in QA passes) while building the QA
fleet's lint/sweep organs (the specialist engine flow_lint.py, the specialist engine
glymphatic_sweep.py). All three are CLASS defects — they recur in any
scanner that mints ledger tasks or maintains "live store" lists.

## 1. Mint-scanner dedupe keys must be LITERAL title prefixes

The dedupe key must satisfy `title.startswith(key)` AND the prefix-match
query must span ALL task states, not just 'open'.

Live proof (flow_lint.py): the first version built
`key = f"EVOLVE: flow {subject} {check}"` but
`title = f"EVOLVE: flow {prose}"` where prose began with the subject name,
not the key structure — the key was never a literal prefix. Combined with
`AND state='open'` in the LIKE query, three runs minted 90+90+90 = 270 rows
(180 duplicates of the same 90 findings). Structural fix:

```python
key = f"EVOLVE: flow {subject} {check}"
title = f"{key} — {prose}"          # key is now a literal prefix
assert title.startswith(key)
# query: SELECT COUNT(*) FROM tasks WHERE title LIKE ?  (key + '%')
# NO state filter — cancelled/closed tasks must still suppress re-mint
```

Regression test that MUST accompany any new minting scanner: run it twice;
the second run must mint exactly 0. (This is the same disease as the S8
5-generation re-mint livelock documented in organism-reflex-arc.)

## 2. Whitelists must be probe-proven, not plausibility-claimed

Any "live store" whitelist entry must be verified by schema + row-count
probe before it is trusted:

```sql
select name from sqlite_master where type='table';  -- schema exists?
select count(*) from <main_table>;                   -- rows exist?
```

Live proof (glymphatic_sweep.py C2 detector): the whitelist initially
claimed `<agent-home>/cron/cron.db` and `<agent-home>/jobs.db` as live cron
stores. A QA pass probed both: ZERO schema, zero tables — decoys I had
whitelisted by plausible name. The actual live cron store is
`<agent-home>/cron/jobs.json` (a JSON file, actively rewritten — verify by
mtime). Fix: whitelist trimmed to probe-proven stores only; cron.db moved
into the quarantine candidate list and swept.

A whitelist containing a decoy is worse than no whitelist: the cleanup
organ defends garbage and quarantines nothing. Also: enumerated live-sets
age badly — whitelist updates belong to the process-improvement loop, not
one-time config.

## 3. Append-only ledgers forbid DELETE — cancel duplicates with outcome

Task ledgers modeling birth certificates reject DELETE (CHECK/trigger:
"tasks are birth certificates — close with outcome instead"). Never fight
the constraint, and never leave duplicates open:

```sql
UPDATE tasks SET state='cancelled',
  outcome='duplicate: superseded by canonical <scanner> entry'
WHERE origin='event:<scanner>' AND state='open'
  AND id NOT IN (
    SELECT MAX(id) FROM tasks WHERE origin='event:<scanner>' AND state='open'
    GROUP BY substr(title, 1, 60));
```

Note: `substr(title,1,60)` grouping works only when the canonical prefix
is stable — which is exactly why pitfall 1 (literal prefix keys) must be
fixed FIRST, or the cleanup groups the wrong rows together.

## Related session context

- Same session minted the specialist engine (cleanup seat), the specialist engine (process-flow
  reviewer), the specialist engine (Physiomorphic AI alignment SME with
  telegram_ask.py ADHD-friendly principal channel).
- Full Nedergaard build pattern:
  `references/glymphatic-cleanup-seat-2026-08-24.md`.
