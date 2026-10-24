---
name: paid-key-budget-guard
description: Use when spending a paid API key under a credit ceiling.
version: 1.0.0
author: hermes-curator
license: MIT
---

# Paid-Key Budget Guard

## When to Use

Any task that automates calls on a credit-backed API key where the owner's
constraint is "use it, but don't drain the balance" (NVIDIA NIM dev credits,
OpenRouter prepaid wallets, trial keys). Also when reporting a guarded key's
status to the owner.

## Why a local ledger

Most credit providers expose no live balance endpoint. The guard is a local
SQLite spend ledger that every call passes through BEFORE the HTTP request
fires — refusal happens at reserve time, not after the money moves.

## Procedure

1. **Identify the key's real wallet state first, by probing, never by
   assumption.** "No credits" beliefs go stale; a dead-seeming key may be
   LIVE with a full wallet behind a per-key spend cap. For OpenRouter:
   `GET /api/v1/credits` (workspace wallet) vs `GET /api/v1/auth/key`
   (this key's own limit). A capped key over a full wallet = one console
   action to unlock; report both numbers, never "needs refuel".
2. **Register the provider**: ceiling (total credit), reserve (headroom
   that must never be spent — "don't drain" means a floor above zero,
   typically ~10%), pre_spent (usage predating the guard, seeded from the
   provider's usage API where it exists so day-one accounting is honest).
3. **Route every automated call through `allow(model, est_prompt_tok,
   est_completion_tok, purpose)`** — check-and-reserve. Over-cap raises
   `BudgetExceeded` and the call never fires. Free-tier slugs and local
   models bypass the guard; metering them is noise.
4. **`record_actual(run_id, real_tokens)` after the response** — most APIs
   return usage; overwrite the estimate. Prices are per-1M-token; update
   from measured receipts, not folklore.
5. **Keep the ledger equal to real spend** — delete smoke-test rows
   immediately after testing. A ledger with test noise makes `status()`
   lie, and status IS the principal report.

## Placement

- Ledger DB lives with the operational stores, never in scratch — it is
  accounting, not session state.
- Guard module lives in the workspace next to its consumers; bench fleets
  and pipeline runners import it, and a `BudgetExceeded` abort exits with a
  code distinct from other failures so fleets mark the run SKIPPED-BUDGET,
  not errored.

## Reporting shape

Status reports carry measured numbers only: `spent $X / cap $Y /
remaining $Z, N metered calls`. Key values never enter the guard, logs, or
reports — resolve from the auth store at call time; reports carry dollar
figures only.

## Pitfalls
- Do not promise a balance the provider won't confirm — label the ledger as
  the accounting source and reconcile against any provider usage page when
  reachable.
- A per-key cap and an empty wallet present the same error from the call
  site; only the two-endpoint probe distinguishes them.
