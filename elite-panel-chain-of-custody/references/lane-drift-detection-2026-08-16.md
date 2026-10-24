# Lane Drift Detection via state.db — 2026-08-16

Session detail: the batch-complete header self-report (`Model: glm-5.3`) was
caught FALSE by the framework's own database. The Tetlock calibration pass
(the round that reordered the entire strategy map) actually ran on
`z-ai/glm-5.2` via provider failover mid-run. Six other seats in the same
gauntlet verified clean. The principal's distrust ("I don't trust this was done
with elite DS brains") was the diagnostic that forced the audit.

## The authoritative check

Never trust kickoff headers, batch-complete self-reports, or transcript
model tags. The framework's execution record is `<agent-home>/state.db`:

```sql
sqlite3 -readonly <agent-home>/state.db "SELECT delegation_id,
  json_extract(task_json,'$.model') AS requested,
  json_extract(result_json,'$.results[0].model') AS actual,
  json_extract(result_json,'$.results[0].api_calls') AS calls,
  json_extract(result_json,'$.results[0].tokens.input') AS in_tokens
FROM async_delegations WHERE delegation_id IN ('deleg_X','deleg_Y');"
```

requested != actual = LANE DRIFT. Token traces in the same row also prove
the work itself was real (e.g. 211K input tokens / 9 api_calls = genuine
deep read, not fabrication).

## Remediation sequence (proven)

1. Persist the finding before touching anything (audit trail first).
2. Re-dispatch the drifted seat with the elite-lane mandate stated IN the
   kickoff: "MODEL LANE: glm-5.3 REQUIRED — you are a re-run because the
   first pass drifted; your output will be diffed against it."
3. The re-run re-adjudicates ALL prior verdicts (CONFIRM / REVISE / REJECT),
   explicitly NOT bound by the drifted pass.
4. Diff elite vs drifted. Fold revisions into the canonical artifact; the
   map stands with clean provenance or updates, never silently carries an
   unaudited lane.
5. Outcome here: 7/8 verdicts confirmed (drift didn't corrupt the strategy),
   3 revisions applied — odds recalibrated (0.72->0.68, 0.12->0.10),
   "parallelize" relabeled to interleave (solo honesty), and one REAL miss
   found: the 14-day kill-shot had no pre-committed branch rule. A drifted
   lane doesn't just risk wrong numbers; it misses whole decision
   structures.

## Hardening (now live)

`verify_lane_from_statedb(delegation_id)` in
`<agent-home>/scripts/brain_integrity_gate.py` reads state.db directly and
returns the ACTUAL model. Verified against both the drifted delegation
(`z-ai/glm-5.2`) and the clean re-run (`glm-5.3`). Call it whenever the
gate prints "lane: no-model-tag (sync-run risk — verify manually)" — that
warning is real, not noise: the flagged delegation was exactly the one
that had drifted.

## Rule

Lane-verify every load-bearing delegation BEFORE folding its verdict into
a canonical artifact. The gauntlet's integrity is only as good as its
weakest unverified execution record.
