# The Seven States — built architecture + panel record (2026-08-25)

Canonical spec: `b2c-firstborn/GAMIFICATION-PHILOSOPHY.md` (v3.0).
Full 78-verdict ledger: `b2c-firstborn/panel-evidence-base-2026-08-25.md`.

## The architecture (survived 12 panel seats, 2 rounds)

Thesis: the right amount of game is a function of need state, PER DIMENSION.
Seven SERVICE MODES (Maslow = inspiration only; ERG simultaneity clause):
HOLD (n=1) / GROUNDED / COMPANION / PACE / MIRROR / GARDENER / QUIET (n=7) —
plus CALIBRATING initial state. UI law: modes render as "___ mode", never as
user descriptors. Arc test that renamed them: "I started on Hold, and now
it's Quiet."

**The inversion:** promotion by STABILITY (level+buffer AND variance, user's
own clinical baseline, shrinkage, upper CI) — you heal your way up, not grind.
Demotion by CARE (sustained strain >=20h span, rate limits 1/dim/day +
2 dims/day, causal distinctness, plain-timeline copy, never loss framing).
Dignity ceiling: rising strain REMOVES mechanics (zero-mechanic-events
assertion, not a quieter skin).

**Dual-criterion graduation (ionization):** Schultz sunset (avg|delta|<0.15
over 21+ reps) is NECESSARY, NEVER SUFFICIENT + exogenous calendar-verified
unprompted completion + user-initiated any time + paused during declared
episode flags + TWC-plateau escape + >=60% quorum. Panel convergences that
forced this: silence-masquerading-as-mastery (Popper), RPE-is-the-right-signal
(behavioral), Schultz-self-sunsetting-loop (systems).

## Envs BUILT (registry: gigi3/ds-engine-registry/ecs.py)

- the specialist engine DS-ECS-SUB-04.07.21-v1.0.0 :port — mode arbiter (launchd daemon,
  plist com.your-org.ds-richter-engine). Battery: organism/seven_states_battery.py (20 rows).
- the specialist engine DS-ECS-SUB-04.07.22-v1.0.0 :port — XP economy: idempotent
  awards, 3.0x ceiling, coherence locked <n=5, confidence capped 1.25 + locked
  <n=4 (fidelity-tax law), pacing decay, hyperfocus factor, graduation fade,
  PERSONA ledger 0600. Battery: organism/xp_economy_battery.py (14 rows).
- Both serve /battery over HTTP; both autosave + quarantine corrupt files.

## Constitution v3.0 = 20 laws (all named in spec sections 3-7)

Beyond the original vetoes, round 2 added: 12a demotion copy, 13 monetization
detachment, 14 never-diagnostic + intent disclaimer + inspectability, 15a
no-ad-tech covenant + deletion path, 16 enforcement seat (watchdog checks
laws 1-20; law without checker = deleted), 17 decision-support (never force
unexplained choice; recommendation PRE-SELECTED; defer-to-recommendation),
18 vocabulary firewall, 19 hyperfocus ceiling, 20 drift law (fast re-places /
slow = consent review; hybrid anchoring bounded by population floor/ceiling).

## Battery-first build loop (the repeatable pattern)

1. Write core module (pure stdlib logic + PERSONA persistence).
2. Write ADVERSARIAL battery BEFORE the engine earns GREEN — every row is an
   attempted exploit needing observable refusal (oracle law: positive
   evidence only, never skip).
3. Run to red; fix organ AND battery data bugs honestly (label which failed).
4. Fresh-brain adversarial CODE review (delegate, read-only, findings schema
   with BLOCKER/MAJOR/MINOR/NIT + SHIP/FIX-FIRST verdict). Expected catches:
   NaN through IEEE comparisons, rate-limit bypass via internal paths, bare
   asserts under -O, UI-vocabulary leaks in evidence payloads, silent corrupt
   wipes, TZ-dodging day keys, missing 0600/fsync/pid-tmp.
5. Fix ALL blockers+majors + cheap minors; EXTEND battery with one row per
   fix; re-run green.
6. Registry + collision checks (name AND port; three collisions caught live:
   Tawara/Fuster/Bernard) -> FastAPI server (/health ECS envelope, /battery)
   -> launchd KeepAlive plist (venv python pinned) -> verify /health, restart
   persistence, battery-via-API -> commit in the owning repo (organism/ is
   its OWN repo, reached via the your-workspace symlink).

## Open at session end
- Bernoulli adversarial review verdict pending (mode-truth ownership question:
  client-supplied mode field vs fetching /mode from Richter).
- Graduation module + watchdog (laws 1-20 checker) unbuilt.
- XP-reconciliation standing CI + sims (10K coherence+ROC, 1M-cell load,
  1K/10K/50K XP with 4 arms) are minted gaps, not built.
