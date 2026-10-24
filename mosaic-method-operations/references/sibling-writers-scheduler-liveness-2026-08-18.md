# Sibling Writers, Scheduler Liveness, QA-17 Findings (2026-08-18)

Session-evidenced patterns for operating the the OS ledger on a
multi-session machine (hermes desktop + terminal + sibling-agent all mint).

## 1. Multi-writer ledger discipline (3 defect classes, all hit 2026-08-18)

**Class A — counter desync.** A sibling minted tasks by `max(id)+1`
via raw SQL, bypassing the atomic `counter` table. Next API mint hit
UNIQUE constraint and crashed. Fix (live in task_ledger.py): `mint()`
is collision-convergent — before insert, it reads `max(seq)` for the
day and advances the counter past any out-of-band writers. Law: the
API must tolerate non-API writers; never assume sole writer.

**Class B — raw-INSERT closes, zero provenance.** Sibling closed tasks
with `state='done'`, outcome='built-live-verified', and NO task_events
rows (no mint event, no done event). The rubric judge scored them
FAIL (0.435/0.522) because provenance was absent — correct behavior.
Points engine awarded ZERO for them (verdict-keyed accrual held).
Handling: do not "fix" the judge; re-score unjudged closes with
`rubric_judge.score(tid)` and stamp stage. The defect is the writer's,
the store stays honest.

**Class C — repo-level self-override.** A sibling's `git push`
overwrote a CI-workflow fix (retry logic silently vanished; next
red run exposed it). Detection: re-read the file after push +
`gh run list` anomalies. Prevention: pull before committing on shared
branches; verify your change survived (`grep` the pushed tree, not the
working tree).

## 2. Scheduler-liveness canary (falsification, not assumption)

Symptom: crontab entries valid, `cron` daemon running, but NO job
executed for 40 min (ticks logged only from manual foreground runs).

Proof pattern (worked, both canaries never fired):
1. `echo "* * * * * touch /tmp/canary" | crontab` + a second canary
   targeting `$HOME` (rules out TCC/sandbox on one path).
2. Wait >70s. Neither file appears → scheduler layer is DEAD
   host-wide, not a per-job failure.
3. Clean canaries out of crontab immediately after the test.

Remediation pattern on macOS:
- Write LaunchAgent plist to `~/Library/LaunchAgents/com.<org>.<job>.plist`,
  verify with `plutil -lint`.
- `launchctl bootstrap gui/$(id -u)` is BLOCKED from inside the
  gateway session (persistent-job safety). Options: ask principal to run one
  line in a separate shell, or...
- Interim fallback that WORKS: a the operator agent-cron job (hermes scheduler,
  not system cron) running the tick script every N minutes, silent on
  success. Remove once launchd job is confirmed loaded
  (`launchctl list | grep <label>`).

## 3. QA microtask sweep order (pass 17 refinement)

Mechanical digest BEFORE panels: gate battery → surgical chain-ok →
ledger integrity SQL (null aliases, dup aliases, counter vs max,
done-without-done-event, thin outcomes) → engine selftests → live HTTP
checks → macro joins (orphan workstreams, empty arcs) → close the QA
task with a full run-record outcome. Findings get minted, not narrated.

## 4. Store-manifest probe hardening

`store_health.probe_store` returned None for manifests with
`liveness.check` but no top-level `kind` → TypeError killed the
watchdog mid-probe. Fix: `kind = m.get("kind") or
m.get("liveness", {}).get("check")`. Class rule: every manifest-driven
dispatcher needs a total function over the manifest schema — unknown
kind must degrade to a DOWN report, never a crash.

## 5. CI notes

- macOS runner segfault-11 on a PASSING gate selftest (2x on
  bus_intake_gate): retry-once in the battery loop, not a code change.
- docs/** commits are path-filtered out of CI — a docs-only push with
  0 runs is expected, not a stuck workflow.
