# CI paths-filter blind spot, pin re-pin, ledger closure (2026-08-19, PASS-3)

Session detail backing the CI-discipline rules in SKILL.md (body edit was
curitor-gated this pass; this file carries the full procedure).

## 1. Paths-filter blind spot

Symptom: pushed a fix commit (a persona chain re-pin), `gh run list
--limit 1` kept showing the OLD red run. The fix commit had triggered NO
run at all.

Diagnosis sequence:
1. `git log origin/main --oneline -1` and `git rev-parse HEAD` — push landed.
2. `gh run list --commit <sha>` — empty = no run for that SHA.
3. `git show --stat <sha>` — commit touched ONLY `personas/pins/`.
4. `.github/workflows/ci.yml` `paths:` filter lacked `personas/pins/**`.

Rule: every input the CI battery reads (gates/, tools/, stores/,
adapters/, personas/pins/, CONTRACT.md, mosaic.manifest.json,
ORGANS.json) must appear in BOTH push and pull_request path filters.
A battery input outside the filter = fixes that never verify = a
permanently red newest-run that misleads every future session.

## 2. Pin-diff drift after persona adds

`gates/ci_battery.py --selftest` FAIL line: `pin-diff chain-3:
registry/engines drifted`. `python3 ledger/ledger_init.py --pin-diff 3`
showed four specialists added since the pin (Banting, Bernard, Neumann,
van Leeuwenhoek). Drift after intentional registry additions is BY
DESIGN — the fix is re-pinning, not suppressing the gate.

Re-pin procedure (verified live):
```
python3 ledger/ledger_init.py --pin 4        # bare integer; "chain-4" raises ValueError
python3 gates/ci_battery.py --selftest       # must print: BATTERY PASS
git add personas/pins/chain-4.json && commit && push
```
The pin commit itself must touch a filtered path (or include a filtered
change) or CI won't run — see pitfall 1. In this session the ci.yml
paths edit supplied the trigger; run 32268518541 went green.

Note: `task_ledger.py --pin-diff` is NOT a ledger flag; pin-diff and
--pin live on `ledger/ledger_init.py`. Wrong tool = argparse error.

## 3. Ledger closure via Python API

The task_ledger.py CLI only exposes --submit/--list/--selftest. Closing
rows requires the module API (mind the signatures — they differ from
what you'd guess):

```python
import sqlite3, sys
sys.path.insert(0, 'gates')
import task_ledger as tl
c = sqlite3.connect('stores/task-ledger.db')
tl.claim(c, "P-HERMES", "ai", task_id=tid)          # (c, actor, actor_kind)
tl.complete(c, task_id=tid, outcome="...", actor="P-HERMES")  # (c, task_id, outcome, actor)
```

Discipline defect caught this pass: three PASS-2 ledger rows sat `open`
while prose claimed closure. Claim-of-closure must equal ledger state.
