# Afferent Limbs + Fleet Review Seats — Build Record 2026-08-22

Session evidence behind the SKILL.md sections "Mycelium afferent" and
"Fleet review seats". Four organs built, wired into the 15-min
autonomous-iteration daemon, all live-verified.

## 1. steer_intake.py (guidance afferent)

- Inbox `stores/guidance-inbox.jsonl` drained EVERY anabolic pass;
  consumed lines archived to `guidance-processed.jsonl` (consume-on-drain
  added after v1 would have re-run lines forever).
- Provenance law: `--source` required; missing ⇒ exit 2 + defect record.
- DOMAIN_MAP regex bug caught live: un-bounded alternations matched
  "g**ui**dance"→design, "b**ui**lding"→build. Fix: `\b(?:a|b|c)\b`.
- Live proof: principal directive minted STEER-3/4/5 at T=1.9; inbox 1→0;
  `steers_minted: 1` in pass output.

## 2. mycelium_afferent.py (pull limb through the specialist engine :port)

- Census BEFORE building (the drift lesson): signal_store had 376 pushed
  / 11 pulled. quality_gate_verdict 0/14, talent_review 0/14 consumed.
  Engines feed, nobody eats — QA loop never pulled.
- Now pulls 5 signal types as `your-org/hub`; first live pass
  consumed ids 329/356/360/376 and pushed back `anabolic_pass_summary`
  as signal #377 (reciprocity closes the loop).
- Market afferent reads finance-thread/novelty-scan-results.json (20 items).
- Human notes via `memo` CLI scoped to Apple Notes "Divinity principal" folder
  ONLY — default Notes folder holds personal content (passwords,
  personal messages surfaced during folder listing). Privacy by scope.
- memo was BROKEN (brew python 3.13→3.14 severed its venv). Repair:
  symlink libexec/lib/python3.14 → python3.13 + wrapper shim at
  /usr/local/bin/memo inserting the site-packages path. Fix pattern for
  any brew venv CLI after a python version bump.
- Mint path v1 FABRICATED an API (`ledger/task_ledger.py` — never
  existed). Real writer found by `grep -rn 'INSERT INTO tasks'`:
  `gates/task_ledger.py` submit(c, title, kind, lane, origin, created_by,
  severity, detail). Lanes are taxonomy-validated; "qa" is NOT a lane
  (use fleet). Verified with synthetic mint T-260822-0010 → cancelled
  with honest outcome per birth-certificate law.

## 3. physics_review.py (the specialist engine seat: math/physics accuracy)

P1 constants-provenance / P2 isomorphism alignment / P3 engine dialogue
(p vs p_c vs claimed above_threshold over /health) / P4 method-name
fabrication detection.

False-positive storm and the three fixes (each verified by re-run):
1. P1 same-line provenance check missed block comments 2-14 lines above
   the constant → widened window to 14 lines.
2. P4 flagged 'Sherman' (stateless router, no telemetry lane) and
   'improvement_scan' (recorded in telemetry as the pass key
   `"anabolic"`) → alias map + Sherman removed from method set.
3. 21 first-breath findings → 20 closed as cancelled with honest
   outcomes; final state 0 false, 0 findings (healthy silence).

## 4. halfway_pin.py (halfway-build pinning)

- H1 stub functions / H2 specs referencing never-built scripts → mint
  kind=gap lane=fleet pins, idempotent vs live pins.
- THREE rounds of false positives from existence checks: flat roots
  missed (a) legacy repo your-workspace entirely, (b) deeper dirs
  organism/telemetry/, (c) sovereign-user/. Final fix: recursive glob
  over `[your-stack/gates, ~/your-org, ~/your-workspace]`.
- Real gap survived every purge: `mcp_roundtrip_test.py` (spec'd
  QA-PASS-25, never built) = T-260822-0053, pinned for the fleet.

## Daemon integration pattern (verified twice)

`anabolic_pass()` in organism/autonomous_iteration.py runs all four
gates; telemetry log line gains keys via
`{k: anabolic[k] for k in (...) if k in anabolic}`. Reload:
`launchctl kickstart -k gui/$(id -u)/com.your-org.autonomous-iteration`
then `tail -1 telemetry/iteration-log.jsonl` must show `physics_rc` /
`halfway_rc` (pass 297 proof).

## Open at session end

- Divinity principal notes folder empty (nothing to pull until principal writes there).
- No producer pushes market data_type onto the mycelium itself (local
  file only, for now).
- Popper LLM panel-cadence seat not yet auto-fired on P-flag anomalies.
- P3 dialogue covers 3 physics engines; widening to full 94-surface
  census is next fleet evolution.
