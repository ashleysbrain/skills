---
name: cron-federation-mycelium
category: devops
description: "Use when wiring crons to push via the specialist engine fungal network."
---

# Cron Federation via Mycorrhizal Network

Hub-and-spoke cron architecture where gg-live processes general crons and pushes results to sibling organisms (gg3, cyber-gg) through the specialist engine (:port, the mycorrhizal network). Specialist organisms pull results instead of recomputing.

## Architecture

```
Hub crons (gg-live) produce result
  -> organism/mycelium_push.py CLI pushes to the specialist engine
  -> POST /signal stores in signal_store.db (persistent)

Specialist crons (gg3, cyber-gg) check mycelium before computing
  -> organism/mycelium_client.py pull() checks GET /signal/pull
  -> If HIT: consume, skip local compute (free energy gate F<0)
  -> If MISS: compute locally, push result back
```

## Key Files

| File | Purpose |
|---|---|
| `organism/CRON-FEDERATION-SPEC.md` | Full architecture spec |
| `organism/cron-federation-registry.json` | All crons classified by organism/layer/dedup |
| `organism/mycelium_client.py` | Python client: push(), pull(), gated_compute() |
| `organism/mycelium_push.py` | CLI exit handler for crons |
| `organism/mycelium_bootstrap.py` | Reconnects organisms after the specialist engine restart |

## How to wire a new hub cron

1. Add `mycelium_push.py` call to the cron's prompt
2. Set `--source` to the organism that owns the cron
3. Set `--data-type` to a descriptive label
4. Set `--consumers` to which organisms need the result

```bash
python3 /<workspace> \
  --source gg-live \
  --job <CRON_JOB_ID> \
  --data-type <LABEL> \
  --consumers all \
  --payload '<JSON>'
```

## How to make a specialist cron pull before computing

```python
from mycelium_client import MyceliumClient, gated_compute

mc = MyceliumClient(source_organism="gg3")
result = gated_compute(
    client=mc,
    source_organism="gg-live",
    data_type="health_scorecard",
    compute_fn=lambda: my_local_scoring(),
    consumer_organisms=["gg3"],
    cron_job_id="my-job-id",
)
```

## Dedup rules

- **DELETE**: Dead/superseded jobs (completed, erroring, no active engine)
- **MERGE**: Overlapping watchdogs into the canonical one
- **MIGRATE**: Specialist jobs to the correct organism when it activates
- **KEEP**: All HUB-GENERAL, all WATCHDOG, distinct SPECIALIST jobs

## Organism Reassignment + Visibility Matrix

`organism/cron_reassign.py` manages cron ownership and enforces security:

```
VISIBILITY MATRIX:
  gg-live   sees: gg-live, gg3, cyber-gg (hub sees all)
  gg3       sees: gg-live, gg3           (CANNOT see cyber-gg)
  cyber-gg  sees: gg-live, cyber-gg      (CANNOT see gg3)
```

Commands:
```bash
python3 organism/cron_reassign.py --list                    # all crons by organism
python3 organism/cron_reassign.py --assign <job_id> <organism>
python3 organism/cron_reassign.py --visible <organism>      # what can it see?
python3 organism/cron_reassign.py --visibility-matrix       # full matrix
```

the specialist engine consent gates enforce this: no gg3<->cyber-gg grants exist.

## MANDATORY: Jargon lint before ANY output

Before writing ANY user-visible text (cron name, prompt, doc, bus message), run:

```bash
python3 /<workspace> <file>
```

Banned terms and replacements are defined IN that script (single source of truth).
Current mappings:
- "knowledge canon" / "canon.db" / "knowledge-canon" -> "Research Library"
- "the corpus" / "corpus absorption/discovery/health/fixer" -> "Course Library"

If this script finds violations, fix them BEFORE sending output to user.
This is a mechanical gate, not a memory entry. Memory fails. Scripts don't.

## Pitfalls

- the specialist engine in-memory topology is LOST on engine restart. mycelium_bootstrap.py cron (every 10m) reconnects automatically.
- signal_store.db SURVIVES restarts.
- result_payload in POST /signal must be a STRING (JSON-encoded), not a dict.
- Pull auto-marks signals as consumed. Second pull returns MISS.
