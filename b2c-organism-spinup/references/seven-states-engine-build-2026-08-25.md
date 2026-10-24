# Seven States engine build — session detail (2026-08-25)

First gamification engine for the b2c-firstborn, built adversarially along the
way. Canonical spec: `b2c-firstborn/GAMIFICATION-PHILOSOPHY.md` v3.0 (survived
2 panels, 78 verdicts). Engine: **the specialist engine** `DS-ECS-SUB-04.07.21-v1.0.0`,
port 8160, wraps `organism/seven_states.py` (core) + `organism/ds_richter_engine/`
(FastAPI server) + `organism/seven_states_battery.py` (20-row battery).

## The adversarial-along-the-way build loop (worked; repeat it)

1. Read the SPEC and the real upstream code/constants before writing (Schultz
   engine: |d|<0.15 / 21 reps / alpha 0.15; Bragg :port; Conductor :port).
2. Write the organ core as a pure module (no server yet).
3. Write the attack battery BEFORE calling anything green — every row attempts
   an exploit and requires observable refusal; oracle law: positive evidence
   only, RED never skipped.
4. Run battery; fix the ORGAN, not the tests, unless the test data is wrong
   (happened twice: time-window overlaps, wrong-era decline data — debug-print
   the actual window contents before blaming the gate).
5. Battery green != ship. Dispatch a FRESH adversarial code reviewer (schema:
   findings w/ severity + SHIP/FIX-FIRST verdict) hunting what the battery
   missed: data-shape attacks (NaN/inf, out-of-order backfill, duplicate ts),
   `assert`-vs-ValueError, direct-transition bypasses around guarded paths,
   vocabulary leaks through "inspectable" payloads, persistence hygiene.
6. Fix ALL blockers+majors (and cheap minors), EXTEND the battery with one row
   per fix, re-run to green, THEN commit.
7. Convert to a real engine (registry/port/health/deps/collision checks), boot,
   verify /health + endpoints + battery-via-API, then wire the contract.

## Review-finding classes worth re-checking on any gate/health engine

- NaN survives Python min/max and `x < threshold` comparisons → reject
  non-finite at INGRESS, never downstream.
- Rate limits bypassed by any path that calls the transition function
  directly (drift was one) → route ALL downward moves through one guarded path.
- Out-of-order backfill: unsorted windows fabricate cliffs (negative span
  clamped to 1s explodes normalized slopes) → sort points by timestamp.
- Bare `assert` guards vanish under `python -O` → ValueError.
- Internal vocabulary leaks through user-facing "evidence" payloads → map
  internal reasons through a UI_REASON table at the boundary.
- Corrupt persist files: quarantine aside (rename .corrupt), never silent wipe;
  fsync + per-pid tmp + 0600 for PERSONA-zone data; UTC day keys for rate
  limits (TZ backfills dodge local-day buckets).
- A population clamp (hybrid anchoring) applied to level gates makes upper
  bands unreachable → keep a raw (unclamped) window for level gates, clamped
  window for variance/drift.

## Wiring contract (what other engines must do)

- rescore pipeline → `POST /observe {dimension, score, strain}` daily per dim
- XP-economy call sites → `GET /hyperfocus/{dim}?engagement_units=N` (law 19)
- the specialist engine → `GET /overlay` before any send (crisis overlay)
- UI → `GET /why_here/{dim}` (law 14 evidence card)
- `GET /battery` runs the 20-row battery in-process (uses /tmp only)

## Collision checks that saved this build

the specialist engine already registered+live (:port); port 8154 = the specialist engine live but
unregistered in the code-map; the specialist engine taken. Always grep registry by
scientist AND curl the port before binding a name/port pair.
