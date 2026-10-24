# CI failure-email storm — volume + battery-glob class (2026-08-23)

Live case: principal Gmail inbox flooded with "workflow run failed" ~144x/day.
NOT a health-alert system (first suspicion wrong) — the storm was GitHub
Actions failure emails. Diagnosis path that worked, encode it:

## Diagnosis chain (in order — each step cheap, narrows fast)
1. `gh api /notifications` — look for repeated `ci_activity` with the same
   title. Count the cadence (timestamps ~10min apart = a daemon pusher).
2. `gh run list -R <repo> --limit 40 --json conclusion,createdAt --jq
   'group_by(.conclusion) | map({conclusion: .[0].conclusion, n: length})'`
   — 40/40 failure = a STANDING failure (every run red), not flakes.
3. `gh api 'repos/<o>/<r>/commits?per_page=6'` — identify the committer.
   Agent-authored telemetry ticks ("chore(overnight-volley): bus intake
   tick" every 10min) mean the failure emails hit the user's inbox because
   the user is the push author of record on every one.
4. `gh run view <id> --log-failed | grep -E "FAIL|##\[error\]"`.

## Two independent noise sources — fix BOTH
1. Run FREQUENCY: telemetry-only pushes (stores/, reports/, telemetry/,
   audit/) should NOT trigger CI at all. paths-filter the trigger to code
   surfaces only (gates/, tools/, adapters/, pins/, contract files).
2. Failure RATE: a standing failure turns every push into an email.

## Battery-glob overreach class (the standing-failure root cause)
A CI step globbing `for g in gates/*.py tools/*.py; do python3 "$g"
--selftest` sweeps in EVERY file in those dirs, and fails three ways:
- Tools with NO --selftest flag → argparse "unrecognized arguments" FAIL.
- Gates whose selftest depends on an uncommitted local DB (e.g.
  ledger/state.db gitignored) → "no such table" on any fresh checkout.
  Reproduce with a clean clone: `git clone <local-path> /tmp/t && cd /tmp/t`
  before concluding "works locally."
- Env-dependent gates (fresh-checkout empty ledger) that PASS locally.

Fix pattern: keep an explicit curated battery module (GATE_TESTS list —
e.g. gates/ci_battery.py) that CI invokes as one command; the glob was
the bug. New gates join the list deliberately, not by directory accident.
Verify locally first: `python3 gates/ci_battery.py` rc=0 before pushing.

## Claims discipline
A "fixed" claim needs N>=3 independent green runs + a quiet observation
window (48h zero storm emails), not one green run on the fix commit.
(Panel ruling 2026-08-23; a 1-green-run "fixed" claim is premature per
L11 claims honesty.)
