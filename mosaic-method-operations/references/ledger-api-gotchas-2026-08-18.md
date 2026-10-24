# Ledger + judge API gotchas (QA pass 18, 2026-08-18)

Verified by live execution during QA passes 16-18 (T-260818-0123,
T-260818-0129). All still true as of CI run 32156936467 (green).

## CLI vs Python API surface
- `gates/task_ledger.py` CLI supports ONLY `--submit / --list / --selftest`
  (+ title/kind/lane/origin/by/severity/actor-class flags). There is NO
  `--claim` / `--complete` flag — claiming and closing are Python-API only:
  `tl.claim(c, actor, actor_kind, task_id=tid)` (MIND THE ORDER),
  `tl.complete(c, task_id, outcome=...)`.
- Python-API `submit()` validates `flow` against flow-registry.json and
  rejects unknown codes. The CLI `--submit` path writes `flow=''` (empty
  string, not NULL) when unspecified — rubric_judge R6 treats `''` ≡ None
  since QA-18.

## complete() behavior (as of QA-18)
- Refuses rows not in `state='claimed'`.
- On success: writes canonical `done` event, pokes conduction, then
  AUTO-RUNS rubric_judge and stamps `stage='rubric:<score>/<verdict>'`.
  Judge errors surface as `stage='rubric:ERROR:<msg>'` (QA-18 D1 fix) and
  never block the close.
- Raw-SQL `UPDATE tasks SET state='done'` bypasses ALL of this: no done
  event (R7 fails), no judge stamp, `outcome` column may stay empty while
  run-records live only in task_events (invariant I2 fails). This is the
  T-0122 sibling-writer defect class; three tasks scored FAIL 0.522 from
  it (T-0104/0105/0107 — also carried unregistered lane `health-sensors`
  and no birth events, i.e. minted outside the API too).

## Schema facts
- `task_events.actor_kind` is NOT NULL — raw INSERTs must include
  `actor_kind IN ('ai','human')` or they raise IntegrityError.
- Ledger timestamps are MIXED FORMAT: canonical API events use ISO
  `2026-08-18T13:35:49+00:00`, raw-SQL writers emit `2026-08-18 15:04:21`
  (space separator, timezone-naive). Any lexical ORDER BY / sort on `ts`
  across both formats silently inverts chronology (space < 'T'). Parse +
  UTC-normalize (naive=UTC) before comparing — see rubric_judge R2 `_ts_key`.

## rubric_judge quick facts
- `--score T-xxxx` CLI; R3 credit regex is gated by a negation lexicon
  (NEGATION_RE) since QA-18; R5 lanes come from task-taxonomy.json data,
  never code.
- Corpus baseline after QA-18 repair: 41 done = 35 PASS / 3 PARTIAL /
  3 FAIL. The FAILs were true ledger debt, not judge noise.

## Surgical gate
- `SurgicalEdit.apply(path, old, new, actor=...)` — `actor` REQUIRED;
  omitting raises TypeError (not a refusal).
- Batch pattern: build `edits = [(path, old, new), ...]`, loop
  `g.apply(*path_old_new, actor="hermes")`, print OK/REFUSED per edit.
