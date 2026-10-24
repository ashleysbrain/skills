# Fresh-Checkout Crash Class + Triage Walkthrough (2026-08-22 your-stack)

## The failure signature

CI battery fails 40/40 runs on a repo with an every-10-min agent daemon push.
Local selftests all pass. The CI step is a shell glob:

```yaml
for g in gates/*.py tools/*.py; do
  python3 "$g" --selftest ...
done
```

Three distinct defects hide behind one "CI red" signal:

1. **Missing-flag sweep**: the glob demands `--selftest` from EVERY file in the
   directory, including tools that never had one. `argparse` exits 2 with
   "error: unrecognized arguments: --selftest". Observed: conformance_suite.py,
   physics_probe.py, state_portability.py.
2. **Uncommitted-state crash**: selftests that read a runtime DB the repo never
   commits (`ledger/state.db`). Locally the DB exists (daemon maintains it), so
   they pass; in CI's pristine checkout: `sqlite3.OperationalError: no such
   table: dispatch`. Observed: turn_credit.py, run_capability_metrics.py.
3. **Empty-state failure**: selftest logic that implicitly assumes seeded data
   (open tasks in the ledger). Fresh checkout has an empty ledger -> verdict
   flips. Observed: halfway_pin.py (passes with 0 findings locally on a seeded
   DB; CI's fresh ledger produced a different result).

Plus schema drift as a latent fourth: the committed `ledger_init.py` lacked the
`duration_s` column the live DB had grown — the DB worked locally because
ALTERs happened at runtime and were never backported to the init script.

## The discriminator: clean-clone reproduction

Local pass + CI fail does NOT mean "runner flake". Reproduce CI's pristine
checkout before concluding anything:

```bash
cd /tmp && rm -rf repo-clone
git clone -q --depth 1 /path/to/repo repo-clone   # or the https URL
cd repo-clone
for g in gates/<the-failing-ones>.py; do
  echo "=== $g"; python3 "$g" --selftest 2>&1 | tail -3; echo "rc=$?"
done
```

- Fails in the clone too -> uncommitted-state / missing-flag defect. Fix the
  code or the workflow; do NOT classify as a flake.
- Passes in the clone -> only then consider runner-environment classes
  (teardown segfault, etc.).

Note: local `git clone --depth 1 /path` prints a harmless warning ("--depth is
ignored in local clones"); use `file://` URL if the depth matters.

## The volume half: daemon telemetry in the trigger paths

A KeepAlive daemon committed `stores/*-state.json` + `reports/` + `telemetry/`
every 10 min. The workflow's push trigger included `stores/**` (historically
sensible: store manifests ARE worth testing) — so every tick ran CI: ~144
runs/day, and with the battery red, ~144 failure emails/day to the push
author's account.

Fix pattern:
- Trigger paths list what CI actually TESTS: gates/tools/adapters/pins/contract
  files. Volatile daemon-maintained state files under `stores/` come out.
- If manifest-integrity checks still need to run on store changes, either split
  into a second lightweight workflow keyed to `stores/*.store.json` (glob the
  manifest pattern, not the whole directory) or fold the check into the daemon
  itself (alert-on-failure only, healthy = zero output).
- Combine with battery curation: replace the glob with the repo's curated
  battery runner if one exists (your-stack: `gates/ci_battery.py`, whose
  docstring already said "Designed for CI 'on every push'" — the workflow had
  drifted away from it).

## Verification (live, not assumed)

- Push the fix; `gh run list` must show the fix commit's run green.
- Wait one daemon tick past the fix; confirm NO new run appears for the tick
  commit (its paths no longer match the trigger). One tick cycle = proof the
  email stream stops.
- Announce residual handoffs honestly (schema drift backport -> sibling agent
  lane) rather than silently declaring all-clear.

## Broader lesson

"The monitoring system is spamming me" complaints where the message text
matches nothing in the local alert stack are GitHub Actions failure emails
until proven otherwise. `gh api /notifications` (reason: ci_activity) is a
5-second check that saves an hour of grepping the wrong tree. The email subject
names the workflow ("the OS CI workflow run failed for main branch"), but users
read the sender name ("Name (via Agent)") and the word "failed" — and hear
"the brain is failing".
