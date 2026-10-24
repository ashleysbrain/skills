# Volatile-State Push Storm (observed 2026-08-22, your-stack)

## Pattern
A KeepAlive daemon (overnight-volley, every 10 min) commits telemetry-only files
(`stores/*-state.json`, `reports/`, `telemetry/`, `audit/`) to main. CI trigger
paths included `stores/**`, so every tick fired a run: ~144 runs/day. The battery
was ALSO failing (see below), so each run emailed the push author a failure
notice. User saw "~6 junk emails/hour saying the brain failed" — the push author
string made infrastructure noise look like a health-alert product.

## Fixes applied (commit 7610295, verified: next tick runs dropped to zero)
1. **Drop volatile dirs from push paths.** `stores/**` removed from `on.push.paths`.
   Gates/tools/adapters/pins/contract changes still trigger. Telemetry-only
   pushes = no run = no email. This alone kills the storm regardless of battery state.
2. **Curated battery list over glob.** The step globbed `gates/*.py tools/*.py` and
   demanded `--selftest` from everything. Three tools legitimately have no
   `--selftest` flag (conformance_suite, physics_probe, state_portability) and two
   metrics gates crash on fresh checkout. Replaced the ad-hoc loop with the
   repo's own `gates/ci_battery.py` (curated GATE_TESTS list, built for exactly
   this). Rule: if a curated battery exists, CI runs IT; globs and curated lists
   must never both exist — the glob silently wins at scale.

## Hidden-DB failure subclass (fresh-checkout crashes)
Selftests that pass locally but fail in CI because they read a local DB that is
NOT committed (`ledger/state.db` — only `ledger_init.py` is in git). Symptom:
`sqlite3.OperationalError: no such table: dispatch` in CI, rc=0 locally.

**Diagnosis: clean-clone reproduction.**
```bash
cd /tmp && rm -rf mm-ci-test && git clone --depth 1 <repo> mm-ci-test \
  && cd mm-ci-test && python3 gates/<gate>.py --selftest
```
If it fails in the clone but passes in the working tree, the selftest depends on
uncommitted state — fix the selftest (temp-DB fixture) or add the gate to the
battery's exclusion list with a reason. Never "fix" by committing a live DB.

## Triage shortcuts for this class
- `gh api /notifications` — a wall of identical "workflow run failed" subjects
  with reason `ci_activity` = storm, not N distinct bugs.
- Failure count first: `gh run list --limit 40 --json conclusion --jq 'group_by(.conclusion)'`.
  40/40 failure = standing defect + high push frequency; flakes would be mixed.
- Check what the recurring commits actually touch (`git show --stat HEAD`): if the
  diff never names a tested path, the fix is the trigger, not the tests.
