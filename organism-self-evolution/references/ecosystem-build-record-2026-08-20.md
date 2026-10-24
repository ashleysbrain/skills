# Ecosystem Build Record — 2026-08-20 (hermes / the specialist engine + the specialist engine)

One session, four organs, all live-verified. This file carries the raw
evidence the SKILL.md summarizes.

## What was built (in order)

1. `organism/improvement_scan.py` — 7-scan battery (S1 stagnation 21d,
   S2 unprobed capability 14d, S3 recurrence ≥3, S4 gap aging, S5 seizure
   σ²<1e-9 / distinct<3, S6 dormant lane, S7 physics decay) + free-energy
   appraisal + ledger minting. Selftest PASS. Dry-run: 1 candidate
   (dormant legal lane, F=0.10) correctly SKIPped.
2. Wired `anabolic_pass()` into `autonomous_iteration.py` (the live
   15-min daemon, launchd KeepAlive) — later extended to run qa_meta too.
   Daemon restarted via `launchctl kickstart -k`, new PID verified.
3. `gates/steer.py` + `stores/steer.json` — principal steer lane. STEER-1
   minted live (fleet, T=1.8, 90d).
4. `gates/qa_meta.py` — the specialist engine meta-QA battery (M1-M5). First live
   run: 21 findings, 17 of them FALSE POSITIVES (see autopsy).
5. `ci_battery.py` patched to persist `telemetry/ci-battery-last.json`
   (evidence contract for M3).
6. Rubric judge R8 mission-genome axis + manifest mission block +
   the specialist engine minted in personas/registry.json (DS-ECS-SUB-04.06.08).
7. Pin chain-5 minted after registry edit; ci_battery → BATTERY PASS.

## Live verification outputs (verbatim)

```
improvement_scan --dry-run: [SKIP] S6-dormant legal F=0.10 T=1.00
  battery: 1 candidates, 0 GO, 1 SKIP, 0 already-open, 0 minted
steer physics proof:
  unsteered  T=1.0 F=+0.20 -> SKIP
  steered    T=1.8 F=-0.44 -> GO
  matcher: T=1.80 steers=['STEER-1']
rubric R8 live:
  T-260820-0074 (genome build):  PASS  R8: 1.0
  T-260817-0001 (legacy build):  PARTIAL R8: 0.0   <- honest, not rubber-stamp
ci_battery after --pin 5: BATTERY PASS: gates + pins green
anabolic_pass (both batteries): {'rc': 1, 'qa_rc': 1, 'ok': True, 'stderr': ''}
```

## The M4 false-positive autopsy

Detector v1 regex hunted `F\d+` findings tokens; this corpus files gaps
as `G1..G10` (QA-PASS-10 gap register), micro-reviews as `M#`. Result:
12 healthy QA passes flagged "nullity". Fix: vocabulary-sampling first
(`F#|G#|M#|DEF-#`), plus a secondary explicit-zero-claim signal. Re-run:
0 false positives, 4 real findings. RULE: sample corpus vocabulary before
writing content detectors; test against known-good docs.

## The M3 dead-evidence-channel bug

v1 read a telemetry stream (`selftest_ok` records in qa-meta.jsonl) that
no process ever writes → every gate read as "rotted". Fixed by making the
writer real: ci_battery.py now persists per-gate results + timestamps,
M3 reads that file. NEVER point a detector at an evidence channel without
confirming a writer exists.

## Rubric R8 bug (two attempts, both caught live)

v1 computed `_genome_ok` inside `rubric()` but read it in `score()` —
never crossed (and `sqlite3.Row.get` doesn't exist → AttributeError on a
live task). Fix: compute at point of use inside the score loop, import
genome_gate there, wrap in try/except. Lesson: helper-computed state does
not flow across functions unless passed explicitly.

## Pin re-mint

Adding the specialist engine to personas/registry.json → ci_battery
`DRIFT pin-diff chain-4` → `python3 ledger/ledger_init.py --pin 5` →
`PASS pin-diff chain-5` → BATTERY PASS. Pins work as designed.

## Open at session end

- 4 QA-META tasks minted open (T-260820-0082..0085): judge coverage gap,
  3 gates (synergy/telemetry/contract_sync) outside ci_battery GATE_TESTS.
- Bus #2641 to sibling-agent: mosaic-chain-executor launchd limb unloaded.
- Adversarial physics panel (deleg_79396ce1) mid-review; verdict destined
  for `audit/ADVERSARIAL-PHYSICS-ECOSYSTEM-2026-08-20.md`.
