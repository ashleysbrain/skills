# Crash Recovery for Sequential Delegation Chains

**Status:** Gap identified 2026-08-27 — NO procedure exists.

## Problem

When the system crashes mid-sequential-delegation-chain (research R1-R10, adversarial A1-A20, glial G1-G25), there is NO checkpoint file to detect which seat was running when the crash hit. The operator (hermes/sibling-agent) has NO resumption protocol to:

1. Detect the gap in the sequential chain
2. Verify which seats landed on disk
3. Continue from the correct next seat

## What EXISTS (from mesh-layer methodology)

1. **Stage 0 Load Governor** (`MESH-LAYER-ARCHITECTURE-2026-08-27.md` §2) — prevents crashes (ceiling, serialization, stagger, catch-up coalescing). Prevention, NOT mid-task recovery.

2. **Daemon crash-resume semantics** (`BEYOND-CRONS-INFRA-MEMO.md`) — daemons are level-triggered reconcilers; a missed pass costs nothing (next pass converges). Applies to daemon passes, NOT delegation chains.

3. **Dispatch-chain checkpoints** (`estra_reanchor.py` line 249-275) — `snapshot_dispatch_chain()` and `restore_dispatch_chain()` for the OS bus dispatch chains. Checkpoints pending bus steps, but NOT delegate_task chains.

## What's MISSING

### 1. Checkpoint file for delegation chains

Location proposal: `stores/delegation-checkpoint.jsonl`

Format per line:
```json
{"ts": "2026-08-27T12:22:17Z", "task_id": "T-260827-0145", "phase": "adversarial", "seat": "A20", "delegation_id": "deleg_225bede5", "status": "in-flight", "output_file": "/<workspace>"}
```

- Write BEFORE dispatch (status="dispatched")
- Update on drain (status="completed")
- No entry on skipped/error

### 2. Resumption protocol

On session restart (after crash):

1. Read checkpoint file: most recent `status="in-flight"` entry
2. Verify deliverable on disk (file exists, size >0)
3. If present → mark checkpoint as "completed", continue to next seat
4. If missing → re-dispatch from crashed seat (sequential law preserved)

### 3. Chain integrity verification

Command to detect gaps:
```bash
# Expected seats vs actual files
expected="A1 A2 A3 A4 A5 A6 A7 A8 A9 A10 A11 A12 A13 A14 A15 A16 A17 A18 A19 A20"
actual=$(grep "^## A" /path/to/audit/file.md | wc -l)
if [ "$actual" -lt 20 ]; then
  echo "GAP: expected 20, found $actual"
fi
```

## Integration with Existing Laws

- **Chain-of-custody law** (memory): sequential execution, each seat reads prior sections
- **Checkpoint writes** happen in the orchestrator before delegate_task call
- **Checkpoint reads** happen on session init (before any new dispatch)

## Pitfalls

- Don't rely on harness reports (corrupted by `max_iterations` bug until restart)
- Trust on-disk deliverables, not harness summaries
- Don't auto-dispatch "parallel make-up" — violates sequential law