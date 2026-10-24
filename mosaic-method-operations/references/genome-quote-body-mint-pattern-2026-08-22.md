# GENOME gate addendum: quote style, canonical bodies, script-file minting (2026-08-22)

*Extends ledger-genome-assignee-gotchas-2026-08-21.md. Hit live 2026-08-22 minting T-260822-0008.*

## Two rejections the base reference doesn't warn about

1. **physics MUST be double-quoted.** Single quotes fail the regex silently and surface as the MISLEADING error `GenomeGateError: no GENOME block in detail` — the block IS there, the quotes are just wrong. Symptom signature: "no GENOME block" + you can see the block in your string = check quote style first.
2. **body must be ONE canonical token.** Invented compounds (`organism-revenue-metabolism`) are rejected with the canonical list printed. For revenue/economics work, `metabolic` is the canonical body that fits. Do not compose descriptive body names; map the concept onto the nearest canonical system.

## The reliable minting pattern: script file, never `python3 -c`

Double quotes inside a GENOME block make inline `python3 -c "..."` a shell-quoting trap (the exact cause of failure #1 above). Write the mint as a small script with `write_file`, then run it:

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/<workspace>')
from task_ledger import connect, submit
c = connect()
detail = (
    "prose context... "
    'GENOME: body=metabolic scientist=the specialist engine physics="free energy: '
    'one-liner here" 8d=environmental'   # NOTE: python double-quoted string
)
tid = submit(c, title='...', kind='build', lane='bus',
             origin='ceo:<directive-slug>', created_by='hermes',
             flow='FLW-QUEUE', stage='submitted', assignee='P-ASHLEY',
             detail=detail, est_cost=4.0)
print('MINTED:', tid)
c.close()
```

(Inside a Python script you own the quoting; adjacent string literals concatenate; the GENOME line keeps its double quotes verbatim.)

## Verify after mint (birth certificate)

```
sqlite3 stores/task-ledger.db "SELECT * FROM task_events WHERE task_id='<tid>';"
```
Expect one `minted` row with ISO-8601 UTC offset timestamp. Also confirm auto-mapping: `SELECT id, workstream, state, stage, assignee FROM tasks WHERE id='<tid>';`

## est_cost discipline

Pass `est_cost` explicitly with a real estimate. If omitted/unset, the ledger appends `est_cost=default(unscored)` to detail and the number is excluded from downstream ratio math (physics instrumentation law, T-260821-0178).
