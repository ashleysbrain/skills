# CI-failure email storm: step-zero diagnosis + curated-battery fix (2026-08-23)

## The miss that cost 20+ minutes

User reported "junk going to my Gmail telling me the principal's brain has failed."
Wrong path taken first: grepping cron dirs, launchd plists, sibling-agent configs,
email bridges, health alert scripts for the phrase "brain fail" — all dead ends.
The phrase never existed in any local file.

## Step zero (correct first move)

`gh api /notifications` — returned verbatim subjects: "the OS CI workflow run
failed for main branch" x many, timestamps every ~10 min. That IS the junk.
The user's reading of "the principal (via the operator agent)" (the git commit AUTHOR name on
GitHub failure emails) as a health alert about themselves is expected — name
this mechanism explicitly when reporting.

## Root cause chain (your-stack, 2026-08-23)

1. overnight-volley daemon (launchd volley-tick, 10-min loop) commits telemetry
   ("chore(overnight-volley): bus intake tick") to main every tick.
2. ci.yml push trigger included `stores/**` — every telemetry tick fired CI
   (~144 runs/day).
3. CI was 40/40 failing (standing defect): the battery loop globbed
   `gates/*.py tools/*.py` demanding `--selftest` from 3 tools that have no such
   flag (conformance_suite, physics_probe, state_portability), plus 2 metrics
   gates crashing on fresh checkout (`ledger/state.db` not committed ->
   `no such table: dispatch`) and halfway_pin failing on an empty ledger.
4. Every failure = one email to the account = the storm.

## Fix (commit 7610295, verified green)

- Battery step now runs the curated `gates/ci_battery.py` (its GATE_TESTS list
  IS the intended membership; a glob is not a test suite).
- Drop `stores/**` (and other pure-telemetry paths) from push triggers:
  telemetry-only ticks must not fire CI. gates/tools/adapters/pins stay.
- Fresh-checkout crash class: reproduce with `git clone --depth 1 file://...`
  locally before concluding; local-pass/CI-fail = missing uncommitted state.

## Verification discipline (N>=3, per Deming seat ruling)

One green run on the fix commit is a POINT ESTIMATE, not "fixed." Claim label
stays THEORETICAL-pending-repro until: >=3 independent green runs AND a quiet
window (48h zero storm emails) observed. The 2026-08-23 session claimed "fixed"
on N=1 — logged as a claims-honesty miss.
