---
name: qa-fleet-governance
description: Use when designing or operating a self-governing QA fleet.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [qa, governance, fleets, engines, autonomy]
---

# QA Fleet Governance (self-governing engine fleets)

## When to use
- Designing or operating a fleet of QA engines (not agents — engines with
  GENOME blocks, ports, /health, 5-layer specs, kill criteria)
- Setting up lead-engine election / no-confidence / replacement mechanics
- Granting a lead engine autonomous minting authority with human notification
- Hardening a fleet against capture, faction formation, empire-building
- principal ruling context (2026-08-24): "AI isn't trustworthy; to build a
  trustworthy self-maintaining system we need an extensive QA fleet" —
  near-parity between QA engines and regular engines.

## Fleet structure (proven org)
```
principal (human)
 └─ the specialist engine — QA fleet LEAD (health checks, queue arbitration,
     │            starvation alarms, lease supervision)
     ├─ lane specialists (process flows, security, isomorphism,
     │  cleanup, detection, identity drift)
     └─ strategic engines (cognitive core, trajectory, evolution-research)
 the specialist engine = scheduler (staff)
 autonomous_iteration daemon = conductor/kernel (infrastructure)
```
Key separations: LEAD (arbitrates) != SCHEDULER (sequences) != CONDUCTOR
(runs the loop). One engine per TYPE; the lead coordinates, never does the
work.

## Queue-routing law (autonomy like humans picking tickets)
- Lane-tagged tasks; atomic OPEN->CLAIMED with lease TTL; lane enforced AT
  CLAIM (out-of-lane claim = REJECTED, tested).
- Starvation -> lead escalation. Zero crons; event-driven only.
- Every REJECTED/REDO verdict auto-mints a process-flow review task citing
  the failed canonical ID (QA fixes the PROCESS, not just the instance).

## No-confidence vote law (checks and balances)
- Franchise: BUILT engines only, census-gated (theoretical designs cannot
  vote — closes the mint-an-electorate hole). New engines cannot vote their
  first seniority cycle. One vote each; lead excluded from its own vote.
- Quorum max(3, 2/3 census); supermajority 2/3 of cast.
- Cause statement MANDATORY with >=2 DISTINCT canonical evidence classes
  (kills correlated-clone errors); cause_class in {failure, changed_needs}.
- Commit-reveal sealed votes (hashes at open, payloads at close) — kills
  sympathy cascades.
- 14-day same-lead cooldown; one active window fleet-wide; vote expires at
  30 days if the human gate is unreachable (re-trigger needs fresh evidence).
- HUMAN GATE: buttons (approve/reject/discuss) to principal/CTO. NO auto-execution
  ever. Unreachable human -> lead stays seated, duties continue, re-notify
  72h.

## Remediation protocol (failure != changed-needs)
Duty-metric re-run decides mechanically: red -> diagnosis + remediation
tasks + 14-day re-evaluation. Green + documented needs-article -> CLEAN
secondary seat, skills-acknowledgment record, no stigma (a lead who did
everything right while system needs moved carries no demotion scar).
Metric/cause disagreement -> human buttons.

## Lead minting authority (autonomous engine creation)
- Lead mints new QA ENGINES autonomously: free-energy demand gate (queue
  depth / lane starvation evidence required — the anti-empire guard), full
  engine standards (GENOME, 5-layer, scientist naming, ECS codes,
  micro-task sizing, chain resolvability, MANDATORY kill criteria), notify
  ONLY (bus + button digest), never gated per-mint.
- New engines enter SECONDARY; seniority by accepted-proposals, not tenure.

## Anti-capture laws
- Kill criteria reap unused engines.
- Discipline-enforcement classifier: votes whose real pattern is "engines
  voting out a lead who executed kill criteria on them" get reject-default
  at the human gate (unpopular discipline is protected from punishment).
- Citation diversity + commit-reveal defeat factions and cascades.
- Quarterly fleet-size review with variance N>=3 for seniority.
- SELF-BIAS DISCLOSURE: when the current lead designs its own governance,
  the review panel MUST flag incumbent-serving biases explicitly (proven:
  3 flagged — incumbent-default on unreachable human, lead-owned fleet size,
  generous drift trigger — all retained only with bounds).

## QA-of-QA: coverage layer, not just organs (2026-08-27 defect pair)
A fleet can pass every liveness check while its COVERAGE rots. Proven
pattern (T-260827-0086/0087): infra QA (daemons, stores, cron, determinism)
ran clean for days while the lens-family angle-pass layer (technical/
scientific/clinical/experiential audit passes) silently stalled — because
the principal-facing immune view was a PASSIVE READER of `audit/*.md` mtimes and
NOTHING owned writing those files on cadence. Three laws:
1. Every dashboard that reports freshness of artifacts MUST have a named
   engine (flow owner) obligated to produce those artifacts. A reader with
   no writer is a slow-falsehood machine.
2. Silent-clean vs dead-silent: a monitor whose healthy state is zero
   output (monitor hash frozen at sha256(empty)) cannot self-report
   health. Meta-meta checks must include (a) artifact-freshness thresholds
   (angle pass >72h = CRITICAL) and (b) monitor liveness heartbeats so
   "empty for hours" is an alert, not silence.
3. Classification scanners that cap by mtime (top-12 newest files) will
   misreport EXISTING work as missing when newer files crowd the window —
   scan by keyword across the full set, or index once.
Also: when a QA defect is found, mint it through the ledger (single write
path, `task_ledger.submit()`); triangle/immune-lane auto-enrollment picks
up routing (observed: enrollment within seconds, bus handoff rows).

## Pitfalls
- Narrative-ahead-of-reality drift: fleets get described as "approaching
  parity" while engines sit unclaimed. Countermeasure: a machine-generated
  reality report (disk census -> BUILT/THEORETICAL per engine) that replaces
  any human narration of fleet status.
- Naming law: engines are scientist-named with ECS codes. Generic system
  names (mise_engine, identity-drift-detector) are violations — rename at
  discovery (proven: mise->the specialist engine, drift->the specialist engine).
- Conflict-of-interest routing: when the lead rules on its own governance,
  note the conflict in the dispatch and mandate the panel to counter-bias.

## References
- references/governance-panel-2026-08-24.md — the 4-seat run (Hamilton,
  Popper, Tanenbaum + glm-5.2 critic) with the consolidated vote law,
  remediation classifier, and self-bias flags
- references/qa-coverage-diagnosis-2026-08-27.md — the coverage-layer
  stall (passive /api/immune reader, no angle-pass writer, 12-file mtime
  cap misclassifying existing passes as missing, silent-monitor blind
  spot) with verification commands and fix dispatch
