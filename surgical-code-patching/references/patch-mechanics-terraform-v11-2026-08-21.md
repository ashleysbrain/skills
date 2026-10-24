# Patch-mechanics learnings — TECH-TERRAFORM v1.1 delta application (2026-08-21)

Session: QA pass 2 (deleg_5cc0ed45) deltas applied to technology-registry code
(events.py, registry.py, probe_runner.py, free_energy.py). Two NEW defect classes
for the taxonomy above, plus the verification battery that caught them.

## Defect 1 — Call-site patch landing as an ASSIGNMENT

Rerouting `REG_FILE.write_text(...)` in `registry.seed()` to the new shared helper,
the patch's fuzzy matcher applied:

    _locked_write = locked_write  # delta 3: seed() uses the shared helper

instead of `locked_write(REG_FILE, json.dumps(reg, indent=2))`. The CALL became an
alias ASSIGNMENT. Symptoms: patch applied "successfully", module imported, no
exception — seed() silently no-op'd (nothing written). The ONLY catch was the LSP
diagnostics block in the patch tool's own result: `"_locked_write" is not defined`
(that symbol was never defined at module scope; my helper was named locked_write).
Fix patch applied immediately; behavioral battery then proved the call executes.

Rule: read the diagnostics block of EVERY patch result before declaring victory.
A clean diff is not a correct patch. For any rerouted call, prove the call site
still executes (run the function, check the artifact changed).

## Defect 2 — Two lock files = zero mutual exclusion

Unifying registry writers on one locked-write helper, the new helper computed
`path.with_suffix(path.suffix + ".lock")` → `registry.json.lock`, while
probe_runner's pre-existing private helper used `REG_FILE.with_suffix(".lock")`
→ `registry.lock`. Two different sidecar locks over one resource: both flocks
succeed, neither excludes the other — the race the delta was meant to kill
survived the "fix". Caught by reading probe_runner's implementation before
declaring delta 3 done (grep every construction of the coordination artifact).

Rule: when centralizing ANY mechanism (locks, caches, queues), first grep for
every existing construction of the coordination artifact and migrate ALL
instances to one canonical name in the same change. `Path.with_suffix` on a
name containing a dot (`registry.json`) silently drops the earlier suffix.

## Verification battery (the pattern worth reusing)

Post-patch live battery, all in one execute_code run, no mocks of the system
under test:
1. import every touched module (syntax + wiring).
2. Positive path: F-gate GO math (assert exact f), PARK math, ledger read-back.
3. Negative paths that MUST raise: operator="system", unnamed temperature
   raise, PARK without re-entry conditions, tech.* emit without entry=.
4. Shape-on-disk check: parse the actual events.jsonl last line, assert the
   top-level key — never trust the emitter's return value alone.
5. Concurrency: 8 threads × locked_rmw appending distinct markers; assert
   set equality (8/8). Catches lock-splitting and lost updates at once.
6. Fault injection: append a torn JSON line, then emit; assert seq is
   max-parseable+1 (not poisoned by the corrupt line's seq 999) and readers
   don't crash.
7. Cleanup selftest artifacts from production state inside the same run.

Meta-lesson: one battery "FAIL" was the TEST's expectation string (asserted
f=-2.5; correct is f=10-6.0*5=-20 — I mis-added the raise). Verify the
expectation's arithmetic before convicting the code under test.

## Records
- Full review: ~/your-workspace/technology-registry/REVIEW-TECH-TERRAFORM.md (QA PASS 2)
- Run record: ~/your-org/your-stack/audit/DELTAS-TECH-TERRAFORM-v1.1-2026-08-21.md
- Events: seq 8-9 (2026-08-21) validation emissions
