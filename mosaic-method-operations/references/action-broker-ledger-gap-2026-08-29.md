# Action Broker Ledger Gap — Minted Tasks Never Dispatched

**CRITICAL 2026-08-29 FAILURE:** Tasks minted to task-ledger.db never dispatched to sibling-agent, causing 20+ hour silent backlogs.

## Mechanism

```
Mint task → task-ledger.db (state='open')
         ↓
Action broker (organism/action_broker.py) polls message-bus.db ONLY
         ↓
LEDGER_DB path defined but NO _rank_ledger() function exists
         ↓
Tasks never ranked → never dispatched → never built
```

## Evidence

| Task ID | Hours Open | Dispatched? |
|---|---|---|
| T-260828-0163 (the specialist engine) | 20.7h | ❌ NO |
| T-260828-0169 (the specialist engine v2) | 19.4h | ❌ NO |
| T-260828-0170 (Fisher/Gilchrist collab) | 19.2h | ❌ NO |
| T-260828-0173 (Interface visibility) | 18.8h | ❌ NO |

## Contrast: What DID Work

T-260828-0166 (Flow database table) built because it was posted to message-bus as handoff — bypassed ledger ranking entirely.

## Required Fix

Add ledger task ranking to action_broker.py:

```python
def _rank_ledger() -> list:
    # Query task-ledger for open tasks
    # Rank by severity, age, type
    # Merge with bus message candidates
    # Return unified candidate list
```

Integration point: action_broker.py line 337 already connects LEDGER_DB, so the query path exists — ranking logic is the missing piece.

## principal Mandate

"I need to be able to walk away from you with confidence that you will do what you are supposed to do while I am away."

**Minted ≠ Dispatched ≠ Built**

Overnight work produces visible interface changes ONLY when tasks are handoffs (bypass ledger), not ledger tasks. This is a systemic reliability gap — the organism forgets its own commitments.

## Prevention Rule

After ANY task mint to ledger, verify dispatch:
1. Check message-bus for matching build_request/handoff
2. If not present within 5 min, flag action broker gap
3. No handoff workaround → fix the broker, not the workflow