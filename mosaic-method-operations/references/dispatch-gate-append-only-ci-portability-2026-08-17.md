# Dispatch Gate, Physical Append-Only, CI Portability (2026-08-17 late volley)

Three learnings from the T-0027/QA-PASS-13 session. SKILL.md pointer may
be missing (curator read-gate refused the patch); this file is the
canonical detail until it lands.

## 1. dispatch_gate.py — the WHO+WHICH join (Flow 8, T-260817-0027)

One dispatch = routing specialist + substrate model + economics, in ONE
append-only record (`stores/dispatch.db`). Composition laws that made it
survive falsification:

- **REFUSE composes, strictest layer wins**: routing > substrate >
  entity-fallback. An unroutable task refuses regardless of model
  availability; no substrate can rescue a missing WHO. An empty measured
  pool refuses; no model pick without measured facts. Unknown entity
  falls back to `org:your-org` reservoir ONLY if registered —
  else refuse. Never a silent default lane.
- The λ profile comes from the wellness reservoir drain state (see
  technology-capability-registry skill, wellness-budget-coupling
  reference), never inline in the gate — one fact, one place.
- Live proof shape: architecture task → the specialist engine + the specialist engine +
  the specialist engine (WHO) + nemotron-lightning fitness 100 est $0 (WHICH) under
  org reservoir $33.33/day.
- **Popper note**: routing REFUSES generically-phrased probe tasks
  ("probe new model for registry" matched no capability class). Check
  `taxonomy/capabilities.json` patterns and phrase the task to a real
  class, or extend the taxonomy as data. Refusing is correct behavior.

## 2. Append-only history became PHYSICAL law (Popper C2)

Claim under test: "task_events is append-only (no code path deletes)".
Falsified: true only by CONVENTION — zero triggers meant any raw SQL
hand or future bug could rewrite history. Fix: `BEFORE DELETE/UPDATE`
triggers on task_events + `BEFORE DELETE` on tasks, wired into
`task_ledger.py`'s schema DDL (not just applied to the live DB) so
fresh installs inherit them. Selftest now ATTEMPTS the forbidden
operations and asserts the abort (14/14).

Generalizable rule: **an integrity property that lives only in code
discipline is unverified. If the storage engine can enforce it
(triggers, constraints, types), enforce it there and selftest the
violation.**

## 3. CI portability — absolute machine paths break the gate battery

Defect: dispatch_gate.py hardcoded
`Path("/<workspace>")`. Local selftest
passed; CI run 32075471213 failed with ModuleNotFoundError (no
substrate_selector). The gate violated the package's own
no-hardcoded-anything law.

Fix pattern (reusable for any cross-repo dependency):
1. Discovery chain: env var (`MOSAIC_REGISTRY_DIR`) first, then
   `Path.home()/your-workspace/technology-registry`, then a sibling
   path relative to the package.
2. If the dependency is absent, the gate must REFUSE with an honest
   reason ("registry not present — set MOSAIC_REGISTRY_DIR"), never
   crash and never silently degrade.
3. Selftest branches on availability: full assertions when present,
   assert-the-REFUSE when absent (CI environment).
4. Verify BOTH modes before pushing: real run + simulated-absence run
   (`dg.REGISTRY_AVAILABLE = False` monkeypatch).

Also: pipe-through-grep on CLI output can mask a failed exit code —
rerun bare when output looks wrong (the `| grep` exit-1 vs the real
REFUSE JSON confusion cost a diagnostic cycle).
