# Selftest hermeticity + re-falsification (MR13, 2026-08-18)

Defect class bit TWICE in one day. Law now: a selftest that touches any
production resource through ANY path is a defect, whatever its assertions say.

## Case 1 (morning): selftest READ prod stores
CI runner lacked census stores -> selftest crashed. Fix: fixture data.
Lesson: reading prod is also pollution (runner-dependence, not just writes).

## Case 2 (evening, sev-2): selftest WROTE the prod principal alert channel
`_ceo_alert()` hardcoded `/<workspace>`.
Selftest redirected the LEDGER global to a tempdir but never the bus path.
Every battery run forged 2 SEV-1 alerts with temp-minted IDs COLLIDING with
real prod task IDs (wrong title on a real ID = misdirection, not noise).
10 of 11 principal alerts on the bus were fakes. Caught by the specialist engine 13A F1.

## The fix pattern (copy this)
1. EVERY external resource resolves through a module-level constant set
   from env with prod default:
   ```python
   import os
   BUS_DB = Path(os.environ.get("OPERATOR_BUS_DB",
                                "/<workspace>"))
   ```
2. Selftest redirects ALL constants, not just the obvious one:
   ```python
   global LEDGER, BUS_DB
   BUS_DB = Path(tmp) / "bus.db"   # plus CREATE TABLE for the spy to hit
   ```
3. Assert side effects with a spy wrapping the real function, counting
   calls; add `len(alerts_fired) == 2` as a selftest case (fires for
   sev-1, silent for self-healing origin).
4. Restore ALL globals in `finally`.
5. Sweep + retract any forged prod rows; post a retraction notice to the
   polluted channel so history stays honest (bus 2341 precedent).

## Re-falsification (the A-grade condition)
Re-run the finding author's probes against the fix:
- On COPIES of prod stores, never prod.
- Via SUBPROCESS exactly as CI runs it. NOT import: py3.14 default-spawn
  multiprocessing breaks selftests containing Process() when the test
  module is imported (`<stdin>` FileNotFoundError, RuntimeError
  bootstrapping phase). Subprocess = the CI path = the path that counts.
- Before/after count on the real store must be EQUAL (1 -> 1 clean).

## Spy-detail gotcha
`globals()["_ceo_alert"] = _spy` inside selftest; restore the real one in
finally or subsequent in-process submits silently lose alerting.
