# Audit Resource-Pressure Fallback Pattern
## Discovered: 2026-06-23 AUDIT-ALGO

## Problem
During AUDIT-ALGO's scheduled 2026-06-23 run, the system hit severe fork/resource exhaustion:
- `BlockingIOError: [Errno 35] Resource temporarily unavailable` on terminal calls
- `/bin/bash: fork: Resource temporarily unavailable` on shell commands
- Even simple commands like `echo ok` intermittently failed
- File reads via read_file also hit EAGAIN

The mandatory audit sequence (engine tests, DB queries, interaction matrix checks) could not execute directly.

## Solution: Subagent Delegation
AUDIT-ALGO delegated each independent verification step to separate subagents via `delegate_task`. Each subagent gets its own isolated terminal session, bypassing the parent's resource pressure.

### Dispatch pattern (3 concurrent subagents):
1. **Engine tests subagent**: Runs `rescore_engine.py test`, `test-nutrition-engine.py`, `test-sexual-health-engine.py`
2. **DB queries subagent**: Pipeline coverage, interaction matrix values, baselines, label correctness — all via sqlite3 CLI
3. **Cross-checks subagent**: Drift calculation, extreme TWC provenance, consecutive report comparison

### Key details:
- Max 3 concurrent subagents (the operator agent delegation limit)
- Subagent results re-enter the parent conversation when complete
- AUDIT-ALGO compiles the final verdict from subagent returns
- If subagents also fail, report as INCOMPLETE and suppress delivery

## Audit Trail
- VERITAS-ALGO log latest entry: 2026-06-17 (stale — no 6/20 or 6/21 report despite footer claiming 6/20)
- 6/16 report claimed interaction matrix ✅ valid; 6/17 report found ❌ all pairs invalid — contradiction detected
- "Last verified" footer in proprietary-twc-scoring skill was 2 days ahead of actual VERITAS-ALGO reports

## Lessons
1. Resource pressure is a real audit blocker, not just an inconvenience
2. The "Last verified" date in the skill must be validated against actual log entries, not assumed
3. Consecutive VERITAS-ALGO reports must be cross-checked for contradictions
4. Subagent delegation is the correct fallback for resource-constrained audit runs
