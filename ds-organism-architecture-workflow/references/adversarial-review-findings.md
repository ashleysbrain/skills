# Adversarial Review Findings — Worked Example

**Source:** Review of ENGINE-LAYER-ARCHITECTURE-SPEC.md (July 2026)
**Reviewer role:** the specialist engine (falsification)
**Spec reviewed:** Task graph (parallel/sequential/conditional), 5-stage failure recovery, 60s checkpoint interval, agent/system classification

## The 5 Adversarial Questions

Apply these to ANY architecture spec:

1. **Does it work on the happy path only?**
2. **Who watches the watchers?**
3. **Does the timing math work?**
4. **Is one size fitting nobody?**
5. **Do flags match reality?**

## Findings Summary

### Q1: Task Graph (6 gaps — CRITICAL)

- **Circular dependencies:** The spec's own example graph contains a cycle
  (Da Vinci → Bell → Luria → Da Vinci). No cycle detection, no max-iteration
  cap on feedback loops. Deadlock.
- **Race conditions:** Parallel groups lack shared-state protection. No barrier
  semantics defined.
- **Conditional dead paths:** No default/else path. If dependency never
  completes, condition is never evaluated. Graph hangs.
- **Dependency failure propagation:** No per-node `on_dependency_fail`
  strategy. Single `fallback` string on entire graph.
- **No priority/preemption:** No way to interrupt a running graph for
  higher-priority work.
- **Static graph, dynamic reality:** Engines may trigger parallel engines
  during execution (Step 5), mutating the graph. No mechanism handles this.

### Q2: Failure Recovery (5 weaknesses — CRITICAL)

- **Bernard is a god engine:** Stage 2 (restart) AND Stage 5 (degraded) both
  depend on the specialist engine. If Bernard is down, cascade can't trigger or escalate.
- **Wenckebach is sole detection path:** Cron job. If cron fails, organism
  goes blind. No peer monitor.
- **Timing math:** Total cascade = 110s. Task graph timeout = 30s. User gets
  nothing before recovery reaches Stage 3.
- **No split-brain handling:** Network partition → engine killed + restarted
  while original still processing. Two engines on same port.
- **No bootstrap ordering:** Recovery infrastructure assumed already running.
  No Tier 0 critical-infra startup sequence.

### Q3: Checkpoint Interval (tiering needed — HIGH)

- **68 engines checkpointing simultaneously** = thundering herd I/O burst.
- **Stateless engines waste I/O** checkpointing nothing (Edison, Gutenberg).
- **Critical engines need 15s**, not 60s (Quartz, Wenckebach, Neural-tube).
- **Recommended tiers:** None (stateless) / Event-driven (task completion) /
  300s (low-churn memory) / 60s (high-churn cognitive) / 15s (critical infra).
  Add jitter (±15s) to avoid synchronization.

### Q4: Agent/System Classification (flag is 50% wrong — HIGH)

- **40 engines have cognitive_layer=True. Only 20 are agents.**
- The other 20 are deterministic math (oscillators, differential equations,
  ETL pipelines) mislabeled as cognitive.
- Having a physics model is not cognition. An optimization algorithm is not
  reasoning.
- **Fix:** Add `type: "agent" | "system"` field. See
  `ds-engine-registry-maintenance/references/agent-system-classification.md`
  for the full 68-engine classification.

## Pattern: Finding Cycles in Example Graphs

The most damaging finding was that the spec's own example contained a deadlock.
This is common — architecture specs draw the happy path and include feedback
loops as bidirectional edges without considering that a topological sort fails
on cycles.

**Check:** Extract all edges from any example graph. Build adjacency list.
Run DFS cycle detection. If any cycle exists and no max-iteration cap is
defined, flag as CRITICAL.

## Pattern: Single Points of Failure in Recovery Cascades

For any N-stage recovery cascade, check:
1. Does any single engine appear in more than one stage? (god engine)
2. Is there a detection engine whose own failure goes undetected?
3. Is the total cascade time longer than the user-facing timeout?
4. What happens on cold start if the recovery infrastructure isn't running?

These four questions find the most common recovery-cascade design flaws.
