# CI-Deterministic Testing on the macOS Runner (2026-08-17 hunt)

## Symptom
Gate selftest printed `SELFTEST PASS: 9/9` then the process died with
`Segmentation fault: 11` at interpreter teardown. CI red (exit 139)
while the SAME test passed locally every time. Four consecutive red
runs: 32065447261, 32066387826, 32066752606, 32066864016.

## What it was NOT (each fix attempted, each still segfaulted)
1. mp.Queue feeder not closed before exit → closed q2, joined thread,
   reaped processes. Still crashed.
2. spawn multiprocessing racers → replaced with THREADS. Still crashed.
3. Open sqlite connections at exit → closed all conns. Still crashed.

Diagnosis by elimination: ANY concurrent-sqlite pattern in a selftest
trips a teardown crash on Python 3.12 / macos-latest runners, even when
the test logic passes. Local builds (3.14) tolerate it. The segfault
happens AFTER all output, so logs show PASS + FAIL for the same file.

## The fix that held (run 32067283844, green since)
Replace concurrent racers with a DETERMINISTIC SERIAL EXCLUSION PROOF
of the same property. For BEGIN IMMEDIATE mutual exclusion:

```python
a = sqlite3.connect(db); a.execute("BEGIN IMMEDIATE")   # writer A holds
b = sqlite3.connect(db, timeout=0.3)
try:
    b.execute("BEGIN IMMEDIATE")                          # must fail
    excluded = False
except sqlite3.OperationalError:
    excluded = True                                       # B blocked
finally:
    a.rollback(); a.close(); b.close()
w = claim(c, "engine-1")                                  # post-release
assert excluded and w["id"] == race_id                    # single winner
```

The property under test is the LOCK SEMANTICS, not the scheduler.
Holding the lock on one connection and proving the second is excluded
proves exactly what two racing processes prove — deterministically, in
one process, with zero teardown surface.

## Rules extracted
1. CI selftests prove properties serially whenever the property is
   lock/exclusion semantics. Save real concurrency for integration
   tests outside the gate battery.
2. Close every sqlite connection before interpreter exit in ANY test
   that will run on the macOS runner.
3. Teardown crashes after PASS output = infrastructure interaction,
   not test logic — stop patching the test's logic and remove the
   concurrency instead.
4. Never declare a concurrency-related CI fix proven until 2+ green
   runs land (the failure was intermittent at 1-run granularity).
