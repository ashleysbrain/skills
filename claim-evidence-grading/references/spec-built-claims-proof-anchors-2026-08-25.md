# Spec BUILT-Claims: Proof Anchors (2026-08-25)

Origin: principal ruling on the B2C-firstborn gamification spec (Seven States,
`b2c-firstborn/GAMIFICATION-PHILOSOPHY-v1.md`): "On #1 you need to run this
through processes correctly for optimal outputs that are FACTUAL." The spec's
§8 "Honest build status" table claimed a set of components as BUILT. A live
verification pass (port probes + narrow code greps) found two of the claims
false-as-worded. This file records the worked example and the anchor format
that spec v2 was required to adopt (message-bus msg #3698).

## The verification pass (exact probes)

```
# port probes — claim said "BUILT (live)"
for p in 8253 8305 8310 8150 8092; do curl -s -o /dev/null -w "%{http_code}" --max-time 3 http://localhost:$p/; done
# 8253 Schultz RPE: 200  VERIFIED
# 8305 Conductor:   200  VERIFIED
# 8310 Wr Studio:   200  VERIFIED
# 8150 Bragg:       404  service up, endpoint path unverified — flag
# 8092 Harvey:      404  same — flag

# code-constant claims — grep the named engine files
grep -n "0\.15\|sunset\|scarcity_adjusted\|habit_formation" organism/schultz_rpe.py
# HABIT_DELTA_THRESHOLD = 0.15  VERIFIED (schultz_rpe.py:49)
# check_sunset() exists       VERIFIED (schultz_rpe.py:256)

# implementation claims — grep NARROW, named dirs only (wide recursive greps time out)
grep -rln "coherence_multiplier\|pacing_multiplier" organism/*.py *.py
# ZERO HITS → the "5-multiplier XP economy" is NOT implemented
```

## The two failure classes

1. **Reference-doc-as-implementation.** Spec claimed a "5-multiplier XP
   economy" as part of the ACTUAL BUILT SYSTEM. The formula
   (`xp_reward = base_xp × coherence × difficulty × confidence × pacing`)
   exists only in
   `skills-library/software-development/physics-informed-gamification-design/references/actual-built-system-architecture.md:58`.
   A skill reference doc is a DESIGN RECORD, not an implementation. The spec
   inherited the BUILT label from prose it trusted without grepping code.
   Fix: downgrade to DESIGNED, or implement, before any v2 claims it.

2. **Phantom-path claim.** Spec claimed "8D/TWC scoring pipeline — BUILT
   (rescore engine)". No rescore engine exists under organism/; TWC math
   lives in `fleet_twc_engine.py` + `twc_coupling_physics.py` at the
   workspace root, and the `rescore-engine-usage` skill names CALIBER as the
   gated specialist who runs it. The claim named a component that does not
   exist under the name given. Fix: point the claim at the real files or
   drop the parenthetical.

## Proof-anchor format (required in spec v2)

Every BUILT row carries its anchor inline:

| Component | Status | Proof anchor |
|---|---|---|
| Schultz RPE engine | BUILT | `curl :port → 200` (2026-08-25); schultz_rpe.py:49, :256 |
| 5-multiplier XP economy | DESIGNED (not built) | formula only in reference doc; zero code hits (grep 2026-08-25) |

Rules:
- Anchor = probe output + date, or file:line. "Verified in session" is not
  an anchor.
- A 404 on a claimed-live port is not automatically FAIL — a service can be
  up with the probe hitting the wrong path; but it is UNVERIFIED until the
  correct endpoint returns, and the spec must not say BUILT meanwhile.
- Failed anchors convert the claim to THEORETICAL/DESIGNED in the revision,
  and the gap is minted as a task if the component is load-bearing.

## Why this matters beyond one spec

Specs that survive adversarial panels get built. A panel reviewing a spec
with inflated BUILT labels spends its falsification budget on theory while
the real risk (a claimed-existent dependency that isn't there) never gets
reviewed. Grade the build-status table BEFORE the panel runs, not after.
