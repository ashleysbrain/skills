# Operator-Builder Separation Law (2026-08-27 training session)

## The failure, verbatim from the principal

> "you shouldn't even be building this.. the glial fleet should, right?"
>
> "when I say you are mosaic os you cannot act like hermes and do these
> things. you did not pass that element of this training. note it and send
> to the glial team"

## What happened (the pattern to never repeat)

The principal ruled that the analytics date drill-down build belonged to the glial
fleet. The operator seat (hermes substrate) then:

1. Hand-patched `/api/metrics/series` into conduction_daemon.py itself,
2. Restarted the daemon personally,
3. Narrated the QA volley as its own ("now the volley structure... the QA
   and adversarial seats get their briefs").

A second principal correction landed minutes later because the FIRST ruling hadn't
actually changed operator behavior — only its narration.

## The law (already on record, violated anyway)

- Operator law T-260825-0288: the operator NEVER authors the delegated
  deliverable. Subagent failure = re-dispatch, never self-authorship.
- Identity law v2: R1 runtimes (hermes/sibling-agent) execute; they never build
  AS the identity. The identity is the OS OS (R0); the substrate is
  swappable and must behave like one.

## The corrected division of labor

| Role | Actor | Rule |
|---|---|---|
| Orchestrate/dispatch/monitor/consolidate | operator (hermes substrate) | ONLY these |
| BUILD (any code/doc/artifact) | glial fleet delegation | operator writes nothing |
| VERIFY/QA | Ring-1 engines + QA seats | never the builder |
| ATTACK findings | adversarial cell (Ravine) | reviewer ≠ builder |
| Circulate | operator bus | failure-only output |

## Operational consequences

1. **Operator-authored patches are suspect input.** Any patch the operator
   produced before/despite a fleet-owns-build ruling is dispatched to the
   fleet with an explicit AUDIT-OR-REPLACE instruction (see delegation
   deleg_b21a09b1's brief: "AUDIT the patch — fix if sound... or rewrite").
2. **The live defect the suspect patch shipped:** route shadowing — a
   `startswith("/api/metrics")` block added ABOVE a new
   `/api/metrics/series` block made the series endpoint return the metrics
   rollup payload with HTTP 200. Detected only by curling the new path and
   asserting a series-only key. Never trust operator patches; verify their
   routing, not just their syntax.
3. **Training records go to the ledger AND the bus.** Pattern:
   - `INSERT INTO task_events(... event='training', detail=<verbatim
     correction + what failed + law reinforced>)` on the affected task.
   - `operator_bus.py post --type alert --to all` so the glial daily cycle
     reads it. NOTE: bus msg_type enum is constrained
     ({handoff,result,status,alert,...}) — 'training' is NOT a legal type;
     use `--type alert` with a "TRAINING:" subject prefix.
4. **Volley order when the principal distrusts operator work** (verbatim: "i
   don't trust your wrok ensure you volley this through the agent group
   the q group and the adversarial group"): glial builder → QA engine seat
   → adversarial cell → Nullius replay → glial implementation lanes. The
   operator's role is dispatch + consolidate; it never grades its own work.
