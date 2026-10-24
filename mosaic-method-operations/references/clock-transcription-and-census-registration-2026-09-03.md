# Clock Transcription Mode + Census Registration + Framework Delta-Check (2026-09-03 late session)

## 1. Third clock failure mode: correct read, wrong transcription (15:53 incident)

Three principal clock violations in one day, THREE DIFFERENT failure modes:
1. Stamped estimate instead of live read (10:22 vs 10:09).
2. Read at turn start, stale by send time (fix: re-stamp >1min old).
3. **Read correct, header transcription wrong**: terminal `date` returned
   15:51/15:52; headers said "11:52". The instrument worked; the hand-copy
   link between instrument and output failed (hour-group transposition).

Rules:
- Header time is copied DIGIT-FOR-DIGIT from the `date` output of the
  immediately preceding tool call — never from memory of it.
- A process is NOT fixed while any step still depends on error-prone manual
  copying. The stamp belongs in the report engine (header generator), not in
  the operator's hands — that is the permanent fix; interim rule is the
  digit-for-digit copy.
- When a "corrected" process fails again, ask whether the correction covered
  ALL steps or just the failing one — mode 3 existed because fix-for-mode-2
  left the transcribe step manual.

## 2. Census registration for principal future-vision domains

When the principal says "low priority, but I want to work towards this in our
ecosystem" (brain-wellness apps, connect-everything vision):
- Register the domain in `stores/connectivity.store.json` under the right
  layer (SOVEREIGN_USER for anything touching personal/user data — local-only
  by law), NOT just a ledger ticket. The census is what the future
  connect-everything engine reads; a ticket alone leaves the domain out of
  its world model.
- Entry shape: `priority` (with principal quote + date), `research_card` (T-id),
  `status: planned - no live connection`, per-app `connection_surface`
  (api/bridge/sdk_risk/evidence), `sovereignty_law`, `recommendation_feed`.
- Backup before edit (`cp file file.bak-pre-<slug>-<date>`); read back after.

Brain-app evidence ladder (measured 2026-09-03, for the registry):
- BrainHQ/Posit: 300+ studies, only 4+/4 MARS app of 4,822 reviewed; research
  partnership unprobed (worth a probe).
- Peak: MARS "good" tier. Elevate: limited independent research, 25 ad/analytics
  SDKs, no public API. Lumosity: limited; $2M FTC settlement 2016.
- Integration truth: no public APIs anywhere in the class; HealthKit/Health
  Connect structured signals are the only machine bridge; per-user game data
  requires own assessment layer (external baselines: digit span, n-back,
  Stroop) + game-CATEGORY prescription (apps' category buckets are public).
- Cadence science: 5-15 min daily beats 30 min 2x/week (consolidation); encode
  in recommendation math, verify via 3-week re-baseline far-transfer check.

## 3. External-framework intake: always run the delta-check

When routing a principal-supplied framework (neuroscience-of-failure wheel:
FALL -> INVESTIGATE -> ACKNOWLEDGE -> LEARN -> EVOLVE -> REALIGN) through
research->adversarial:
- Mandatory counter-hypothesis #1: "is this <known cycle> rebranded?" (the
  wheel vs PDCA/Deming). The verdict must name what the framework ADDS over
  the incumbent, not just the overlap.
- Mandatory reconciliation test when the framework's advice conflicts with
  standing law ("produce more attempts" vs quality-over-speed / free-energy
  gate) — adversarial must reconcile or rule, never let both stand.
- Verdict vocabulary fixed at mint: ADOPT (named flow changes) / ADAPT
  (boundary named) / REJECT (reason). Nothing touches flow-registry without
  verdict + glial QA.
- Wheel-stage mapping method: map each stage onto existing flow anatomy
  (FALL=gate-reject-log/debriefs, INVESTIGATE=root-cause, EVOLVE=taxonomy
  loop, REALIGN=registry updates), then attack the thin stages — ACKNOWLEDGE
  and LEARN mapped thinnest.

Ledger anchors: T-260903-0089 (failure wheel), T-260903-0092 (brain apps),
T-260903-0056 (gated outline v3), debrief-2026-09-03-clock-transcription-defect.json.
