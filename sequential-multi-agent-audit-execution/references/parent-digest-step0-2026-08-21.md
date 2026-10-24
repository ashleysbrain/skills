# Step 0: parent mechanical digest before any auditor dispatch — 2026-08-21

Add-on to the Execution pattern: insert a "### 0) Parent mechanical digest
FIRST" step before "### 1) Lock the sequence". Full worked case lives in the
sibling skill `elite-panel-chain-of-custody/references/mechanical-digest-panel-2026-08-21.md`.

## The rule
Before ANY reviewer/auditor seat dispatches, the PARENT mechanically
re-verifies every claim made by the work under audit:
- correct key names — the key the CONSUMER reads (a dead-edge check on
  `depends_on` was vacuously green; registry and scorer use `dependencies`),
- counts re-derived from artifacts (diff backup vs live) rather than trusting
  the number computed mid-action ("141 edges updated" was really 53 dep-sets
  / <=131 lines),
- the instrument's IMPLEMENTED operations read from source, not its docstring
  (C_r promised biological-plausibility checks; code did string-resolution
  only, zero-dep engines scored 1.0 by fiat).

## Why the parent must do it (why not just let the panel find everything)
The 2026-08-21 pass-2 digest caught three defects the original full 5-seat
panel had missed — two of them in the orchestrator's OWN pass-1 record
(overclaimed count; corrupted table cell `0.85_o_r`). Panels catch conceptual
flaws; only the parent's mechanical digest catches self-inflicted metadata
rot, and it must land BEFORE dispatch so every seat inherits verified facts
instead of the record's errors. Digest findings become numbered findings
(F1..Fn) in the shared evidence pack; seats attack the numbered findings.

## Crash-insurance companion rule (same session)
Instruct multi-seat children to APPEND each seat's verdict to a dated on-disk
verdicts file under `## Seat N — <name>` headers as each seat completes. When
the parent's dispatch-timeout wall cut a 6-seat chain at seat 4, seats 1-4
were recovered from disk and delivered honestly with an owed-list — instead of
zero. Never invent the missing seats; re-dispatch only them with the on-disk
verdicts as chain-of-custody context.
