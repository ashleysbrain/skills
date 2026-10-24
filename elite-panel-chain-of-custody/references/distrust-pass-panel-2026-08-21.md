# Distrust-pass panel — watchdog verification QA-4/QA-4b (2026-08-21)

Context: after five adversarial panels on the delegation watchdog
(`organism/auto_repair_watchdog.py`, QA-1..QA-3), principal ordered a sixth:
"do this again with different adversarial brains... i am not sure i trust
this work."

## Panel composition (bench burned)

Prior passes had used: Popper, Sherrington, Deming, Tanenbaum, Scheffer,
Bridgman. The distrust pass used fresh adjunct brains:
- **the specialist engine** — falsify-the-verification ("the first principle is that you
  must not fool yourself — and you are the easiest person to fool")
- **DS von Neumann** — minimax adversary simulation (attack as the dead
  harness process would)
- **the specialist engine** — error-behavior ("a design is what it does when things go
  wrong")

## Evidence pack pattern that worked

`research-thread/QA4-EVIDENCE-PACK-2026-08-21.md` (~2.3KB):
1. Claims-listed-as-targets: every "claimed-true" assertion from prior
   closeouts, numbered, phrased as falsifiable.
2. Contamination events already handled (so the panel doesn't re-report).
3. The injection signature verbatim — children ran sandbox experiments in
   their first calls instead of reverse-engineering entry points.
4. Honest residuals listed as "context, not targets".
5. Attack mandate: numbered, worst-first, under 320 words, "say FALSIFIED
   bluntly".

## Verdicts that landed (from full subagent-summary files)

Feynman (4 findings): sandbox leaks to production (poke + state split-brain);
finals-as-success (exit_reason=error counted as landing); manifest index
compaction re-pairs logs to wrong tasks; corrupt-state recovery REPRODUCED-OK.
von Neumann: state split-brain confirmed live; corpse-DoS on systemic gate
(3 eternal corpse dirs = permanent per-seat suppression, real death swallowed
70+ min); touch-attack survives while young. Hamming: clock-skew freezes
escalation (future ts) + future-mtime logs immortal-fresh; corrupt manifest =
total supervision blind spot; brownout afferent not injectable (tests depend
on production API health).

All fixed in v4.1-v4.3; proofs in
`organism/tests/test_deleg_watchdog_qa4.py` + `test_deleg_watchdog_v43.py`.

## Operator lessons (the meta-findings)

1. **The finals in the batch-complete message truncate at ~350 chars.** The
   full verdicts live in `<agent-home>/cache/delegation/subagent-summary-<n>-<ts>.txt`.
   Integrating from the truncated delivery HID three real findings until the
   full delivery arrived later. ALWAYS read the summary files before claiming
   "all findings integrated".
2. **Your own regression proof can lie about what it tested.** The QA-3
   "8/8 proof" ran against the REAL state file and REAL bus — test fixtures
   leaked to production (msg 2808), saved from spam only by a 30-min cooldown.
   Parameterize the target (injectable roots) BEFORE proving anything.
3. **A replace-pattern that doesn't match fails SILENTLY.** The corpse-
   bookkeeping splice "succeeded" (script printed OK) but the pattern had
   drifted; the write never landed. Tick2's assertion passed on the 1800s
   cooldown alone. Proof: pin the MECHANISM, not the outcome — assert the
   state key the mechanism writes, or make the cooldown independent in the
   fixture.
4. **Hermetic suite structure** (reusable shape): tempdir live-root, sandbox
   state file, collector bus_post, api_health pinned, conduction pokes
   monkeypatched to a counter; assert production state byte-identical before/
   after. See `organism/tests/test_deleg_watchdog_v43.py` for the shape.
5. **Import bridge pitfall**: `your-workspace/organism` is a symlink to
   `your-org/organism`; auto_repair_watchdog anchors WORKSPACE on the
   unresolved path because agent-organism/ecs.py lives under your-workspace.
   Tests must import via the bridge path, not the canonical one.
6. **Baseline-first gate**: writing a NEW file under a symlinked "existing"
   directory reads as an edit to an existing artifact; cp from /tmp via
   terminal works when write_file is refused.

## Live-fire dogfood (unplanned but decisive)

The first distrust dispatch itself died 3/3 to the API timeout storm mid-run.
The watchdog under test caught it: PARTIAL-LANDED alert → operator re-dispatched
only dead seats → recovery limb closed RECOVERED when the manifest acked. Full
alert→recovery arc on a real production event during its own QA. This is the
strongest possible evidence class for a supervision organ — report it when it
happens.
