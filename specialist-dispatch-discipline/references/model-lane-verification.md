# Model-Lane Verification via state.db (Authoritative)

Learned 2026-08-16: the principal challenged provenance ("I don't trust this was done with elite DS brains") and the challenge was VALID. The batch-completion message and the kickoff header both said "Model: glm-5.3" for every seat — and one of seven had actually run on `z-ai/glm-5.2` (provider failover mid-run). Self-reports lie. The framework's own execution record does not.

## The authoritative query

`<agent-home>/state.db`, table `async_delegations`:

```sql
sqlite3 -readonly /<workspace> \
"SELECT delegation_id,
        json_extract(task_json,'$.model')            AS requested,
        json_extract(result_json,'$.results[0].model') AS actually_ran,
        json_extract(result_json,'$.results[0].api_calls'),
        json_extract(result_json,'$.results[0].tokens.input'),
        json_extract(result_json,'$.results[0].tokens.output')
 FROM async_delegations
 WHERE delegation_id IN ('deleg_x1','deleg_x2');"
```

- `task_json.$.model` = what was requested at dispatch
- `result_json.$.results[0].model` = what the child ACTUALLY ran on
- Mismatch = lane drift (typically provider failover), even when every self-report agrees

Token counts also prove behavioral depth: a falsification pass showing 211K input tokens and 9 API calls genuinely read the code; 0 api_calls means a pure-reasoning seat (fine for falsifier roles, suspicious for seats ordered to inspect files).

## Worked example (2026-08-16, convergence-map gauntlet)

7 dispatches, all requested glm-5.3, all self-reported glm-5.3:

| delegation | seat | actually ran |
|---|---|---|
| e18cbf0b | Karpathy | glm-5.3 |
| 9914300b | Popper (falsify) | glm-5.3 |
| a261378e | Tanenbaum | glm-5.3 |
| c8b1d4f1 | Lamport | glm-5.3 |
| f969cb05 | Popper (readiness QA) | glm-5.3 |
| e11cb7d8 | Tetlock (calibration) | z-ai/glm-5.2 — DRIFTED |
| 608290cf | Andreasen | glm-5.3 |

The drifted seat was the one whose output restructured the canonical strategy (spec bisect, parallel tracks, calibrated odds). Worst-case seat, silent failure. The integrity gate had printed `lane: no-model-tag (sync-run risk — verify manually)` on exactly that delegation — the flag was real.

## Remediation pattern

1. Re-dispatch the SAME seat with explicit elite-lane mandate in the context: "MODEL LANE: glm-5.3 REQUIRED — you are a re-run because the first pass drifted to a lower lane; your output will be diffed against it."
2. The re-run must NOT be bound by the drifted pass: instruct it to CONFIRM / REVISE / REJECT each prior verdict independently.
3. Diff the two outputs. If verdicts survive, the consolidated artifact stands with a provenance note appended. If revised, update the artifact.
4. Bank the audit trail (O'Keefe) including which artifact had carried the unaudited verdict.

## Integration points

- `brain_integrity_gate.py` prints `lane: no-model-tag (sync-run risk — verify manually)` when it cannot confirm the lane from the kickoff alone — treat that flag as REAL, not noise. When it fires, run the state.db query before trusting the run.
- Never accept "Model: X" from batch-completion messages, kickoff echoes, or the child's own summary as lane evidence. Only `result_json` counts.
- Applies to the "Degraded-lane run" recovery pattern in SKILL.md: verify lane from state.db, not the batch-complete header.
