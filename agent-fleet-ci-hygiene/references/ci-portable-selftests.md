# CI-portable selftests and gate batteries (MR12, 2026-08-18)

Three failure classes hit while making gates pass on the GitHub Actions
runner after passing locally. Encode these into any new gate or selftest.

## Class 1: interpreter-teardown segfault (returncode -11)

Symptom: gate selftest PRINTS its PASS summary, then the process exits with
rc -11 (SIGSEGV) on the CI runner only. Local runs exit 0 every time.
Root cause: sqlite connections / module state surviving to CPython
finalization. The rc arrives AFTER all output, so stdout looks green while
the step fails.

Fixes, in order of preference:
1. Close every sqlite connection you opened (package rule; four CI runs
   died before this rule existed).
2. If the segfault persists (it did for bus_intake_gate even after a gc
   sweep of Connection objects), bypass interpreter teardown entirely:
   flush stdout/stderr, then `os._exit(0)`. This is the CI-portable form
   of the close-connections rule when the leak is in C-level state.

## Class 2: selftests must never touch production stores

The CI runner does not have the operator's census/store files. A selftest
that reads the live store (absolute path or module default) passes locally
and fails on the runner with FileNotFoundError. Rule: selftests run on
fixture data in a tempdir ONLY. Any check that needs a real store must
guard on existence and skip on the runner (see generate_registry selftest:
hand-side uniqueness check skips when app.js absent).

## Class 3: battery flake diagnosis

When a gate battery marks a gate FAIL but the captured stdout is the PASS
summary: the check is `returncode == 0 and "FAIL" not in stdout`. Print
`returncode=<rc> detail=<stdout | stderr>` on every failure BEFORE
debugging anything else. The rc distinguishes segfault (-11 / -15) from
assertion failure (1) from timeout (124-ish) from missing file (2).
Note: macOS lacks the `timeout` command; use `gtimeout` from coreutils or
run bare when simulating CI locally.

## Local verification loop (fast, before pushing)

```
for g in gates/*.py; do python3 "$g" --selftest > /dev/null 2>&1 \
  || echo "FAIL $g"; done          # rc-based, immune to wording
python3 gates/ci_battery.py        # the exact battery CI runs
python3 gates/store_gate.py --flow-sync
git push && gh run watch           # then confirm green on the sha
```

Caveat learned live: the push webhook occasionally lags for docs-only
commits. A missing run on HEAD is not a code problem; verify with the
local battery and `gh api repos/{owner}/{repo}/actions/runs?per_page=3`.
Never claim CI green from a run on an older sha than HEAD without saying so.

## JS edit hygiene (hub-class UIs)

- After every edit to a browser JS file: `node -e "new Function(src)"`
  parse check. MR12 shipped `dims:["PHY", "PSY]` (unbalanced quote) that
  only a parse gate catches; it killed the whole page.
- `const` declarations do not attach to the sandbox global in headless
  dump-dom; probe via rendered DOM text, not window properties.
- Hoisting: a `const LAYERS` used in an earlier function than its
  declaration throws at runtime, not parse time. Render battery (cards
  count == 0) catches what node parse misses.
