# QA Panel Protocol + Laws L10/L11 (session 2026-08-18, MR10-MR12)

Class-level learnings from three QA micro-review panels (10 brains total)
on the census->registry->hub build in the sovereign-user layer.

## L10: QA freeze (three-witness finding -> law)

During MR10, a sibling remediation lane regenerated the audit target
mid-panel THREE times; two subagents burned budget re-anchoring to moving
shas (one timed out at 1800s because of it). MR11 ran with the fix and had
zero churn events.

Protocol that works:
1. Before dispatching the panel, `SurgicalEdit().claim(path, '<pass>-freeze')`
   every target file; record shas (`shasum`) in the dispatch context.
2. Subagents get: "FROZEN (sha at dispatch): <files>. Report only, no edits."
3. After reports land: release leases, then remediate.
4. Surface freezes any time: `python3 gates/surgical_gate.py --leases`
   (expired rows purge automatically; the old bug was stale rows outliving
   their TTL and blocking later edits).

## L11: claims honesty (Osler grade-C finding -> law + gate)

Three falsified-claim classes found in one panel:
- "encrypted" token storage with zero crypto code (plaintext localStorage)
- "PHI-class handling" prose with no phi/consent enforcement anywhere
- consent/egress functions declared, never invoked, listed as features

Law: no doc/table/card/note may claim an enforcement that code does not
run. Declared-but-unused = finding, not feature. Honest escape hatch: label
claims "pending" (claims_gate passes `encrypt...pending`).

Enforcement: `gates/claims_gate.py --check <dir>` (exit 1 on findings).
It caught the exact live findings on its first real run. Wire it into CI.

## Runner-only segfault diagnosis chain (rc = -11)

CI red, local green, selftest PRINTS PASS then fails = segfault at
interpreter teardown, not a test failure. Diagnosis chain that worked:
1. Improve the battery's failure capture first (print returncode + stderr)
   -> `returncode=-11` with passing stdout = SIGSEGV at Py_Finalize.
2. Known package cause: sqlite connections outliving the interpreter.
3. gc-sweep of connections was NOT enough (C-level state); the fix that
   went green: flush stdout/stderr then `os._exit(0)` at selftest end,
   bypassing interpreter teardown entirely.
CI green run after fix: 32189509117.

## Registry merge law (census-over-hand), verified semantics

- Merge by `census_id`: census fields win; NULL census fields must NOT
  override hand values (null-guard in the Object.assign loop).
- Census-no-opinion (no status voiced) = INHERIT hand status. Never
  fabricate a default status for silent records (this bug demoted 5
  verified-live badges to untested in one render).
- Probe evidence strings carry verdicts (ACCESSIBLE/PARTIAL/AVAILABLE/
  BLOCKED/EMPTY/DEGRADED); map verdict->status, never invent.
- Stats must count RENDERED cards only; entries with unknown layer
  counted-but-not-rendered = phantom inflation (fail-open class).
- Generated registry stamps `generated_at` + source sha; the consuming page
  renders registry age; regeneration is launchd-scheduled (drift bounded).

## Live DOM battery (the only verification that counts)

Code-read verification missed every defect above. The battery that caught
all of them: chrome-headless-shell --dump-dom + grep/node assertions on
card counts, badge counts, string presence (target strings, casing, em
dash, ellipsis), plus --enable-logging=stderr for Uncaught errors.
Two same-session regressions (JS hoisting violation -> 0 cards; CI-only
segfault) were caught by this battery, not by review.
