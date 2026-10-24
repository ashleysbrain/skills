# Glia 24/7 daemon + mint-gate build (T-260824-0649/0640, 2026-08-25)

## Fleet-loop self-serving pitfall
Loop engines (gap_cycle, autonomous_iteration, EVOLVE, physics-review)
mint and close their OWN series; nothing binds them to principal-minted P1/P2
work. Overnight: 138 "done" tasks = 87 one-incident EVOLVE cascade + ~25
spam re-mints of the same two findings + loop bursts; every principal P1 sat
untouched (queue ENTER median dwell: 937h). Spam series = dedup-gate
defect to fix, never throughput to report.

## Fix 1: glia_conduction.py (the specialist engine lineage)
Event-driven daemon — NOT cron:
- Triggers: ledger mtime change OR bus max-id change (poll trigger-state
  only, 20s). launchd KeepAlive com.your-org.glia-conduction.
- Cycle: harvest principal/governance-lane opens -> law-lint (flags
  done-without-outcome rows — caught 2 legacy false-dones on first run)
  -> novelty-weighted arbitration (severity x deviation-from-median-gap
  RPE; static weight alone = weight-chasing) -> state file persists.
- Escalation: only after 3 consecutive idle cycles, one bus alert, then
  silence (failure-only alert law). Healthy = zero output.
- Verification pattern: post live bus probe, confirm daemon cycles
  unprompted within 25s (state cycles 2 -> 4). That is daemon proof,
  not "process is running" proof.
- Non-numeric task ids in ledger (e.g. `L12A`) crash int() parsing —
  guard every id parse.

## Fix 2: mint_gate.py — single law membrane
One gate module, N writers (entanglement, not N law copies). Wired into
all 4 fleet mint functions (flow_lint, gap_hunter, isomorphism_lint,
security_audit) via insert-after-def-signature.

PLACEMENT BUG: snippet initially landed inside module docstrings in 2 of
4 files — compile passed, code dead. Assert offset-after-docstring, then
spy-prove (see tool-output-verification-discipline
references/false-done-marks-and-spy-verification-2026-08-25.md).

Known open decision: gate import is fail-OPEN (try/except pass) if
mint_gate missing — fail-CLOSED halts all fleet minting on gate break;
principal to rule.

## Innovator-watch pattern (T-260824-0650)
Follow-set watcher composed into existing research-scan tick (medialab
precedent) — zero new crons. Karpathy: blog RSS + GitHub events API.
PRECISION DEFECT: `au:the advisor` arXiv query matched any author named the advisor —
disable ambiguous-name sources until identity confirmed; purge wrong
entries from events.jsonl rather than polluting the catalog. Tier sets
attention priority only, never acceptance criteria.
