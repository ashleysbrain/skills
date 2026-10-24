# the OS Package Map — paths, APIs, gotchas (verified 2026-08-17)

Package root: `~/your-org/your-stack/`
Remote: private GitHub `your-org/your-stack` (gh CLI works).

## Gates (gates/*.py) — run with the --selftest FLAG
A positional "selftest" arg is an argparse ERROR (exit 2). Battery:
`for g in gates/*.py; do python3 "$g" --selftest || echo "FAIL $g"; done`
(That loop is also the CI gate-battery step.)

- surgical_gate.py — `--selftest` (15 cases), `--chain-ok` (audit chain)
- task_ledger.py — submit/claim/complete/list; v2 fields flow/stage/assignee
- scheduler_queue.py — physics queue; submit/claim/complete
- routing_gate.py — specialist routing, taxonomy-driven, phd_panel_minimum
- free_energy_gate.py — `--check '{...}'`, `--order '[...]'` (JSON list only;
  non-list now returns readable JSON error, exit 2)
- interop_gate.py — cross-harness planning; unknown domain RAISES (no fallback)
- store_gate.py / store_health.py / synergy_gate.py / telemetry_gate.py /
  contract_sync_gate.py

## Two taxonomies — do not confuse
- `taxonomy/capabilities.json` — ROUTING: classes/patterns/ranks,
  constraints, health_blocklist, limits {phd_panel_minimum: 15,
  max_recursion_depth: 6}. Loaded by routing_gate.
- `stores/task-taxonomy.json` — TASKS: kinds (8), lanes (11),
  origin_prefixes, severity. Loaded by task_ledger (duplicates rejected).

## Stores
- `stores/task-ledger.db` — the LIVE ledger (NOT ledger/; ledger/ holds
  state.db + ledger_init.py). Tables: tasks (+flow/stage/assignee,
  user_version=2), counter, task_events (append-only history).
- `stores/*.store.json` — Codd manifests; CI validates JSON + "store" key.
- `stores/flow-registry.json` — 10 FLW-* codes (HANDOFF, QUEUE, LEDGER,
  DECISION, REGISTRY, STOREHEALTH, AUTONOMY, SURGICAL, QA-PASS, DISPATCH),
  each with stages[]; isomorphism: flow-registry : task-ledger ::
  ECS-registry : engine-instances.
- `stores/people.json` — P-ASHLEY, P-BRANDON (add members as data).

## task_ledger.py API gotchas (cost real time this session)
- `submit(c, title, kind, lane, origin, created_by, **fields)` — order
  matters; kind/lane/flow/assignee validated against the JSON registries.
- `claim(c, actor, actor_kind, task_id=...)` — (actor, actor_kind) ORDER;
  wrong order raises "actor_kind must be 'ai' or 'human'".
- `complete(c, task_id, outcome, actor=...)` — refuses unless state='claimed'.
- SQLite Row objects: `dict(row)` fails on multi-col selects; index rows
  directly (`r[0]`) or select explicit columns.

## Conduction daemon (poke layer, crons are watchdogs only)
Port 8280: GET /health (status/pokes/cycles/last_error), GET /poke.
Mint/complete in ledger + scheduler + bus auto-poke it. Verify liveness:
curl -s -m 4 http://127.0.0.1:port/health

## CI (macos-latest, python 3.12)
- `gh run list --limit 1` after push; cite green run IDs in run-records.
- Concurrency tests must be deterministic serial exclusion proofs; close
  all sqlite connections before interpreter exit (see
  ci-deterministic-testing.md).
- Surgical chain-ok step runs on every push.

## Related repos
- technology-registry at ~/your-workspace/technology-registry/ — probe
  runner, cost_ledger.py (prices.json budgets), events, Hebb pipeline.
- your-workspace organism/ — conduction_daemon.py, poke.py,
  mosaic_chain_executor.py, autonomy_report.py, operator_bus.py.

## Standing semantics
- DEFERRED chain verdicts do NOT close the origin bus message (retry).
- Selftests NEVER touch production stores (tempdir isolation).
- sibling-agent unreachable → bus build_request + build around it.
