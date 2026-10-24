---
name: agent-fleet-ci-hygiene
description: Use when CI failure emails storm a repo agents push to.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [ci, github-actions, triage, notifications, agent-fleets]
---

# Agent-Fleet CI Hygiene

Use this skill when a repository receives frequent pushes from agent sessions (every
few minutes) and CI must stay green AND quiet. Covers: diagnosing failure-email
storms, honest triage of runner flakes vs real defects, and reducing run volume.

## Trigger Conditions
- User reports "emails saying CI is erroring and these are coming out of nowhere"
- `gh run list` shows dozens of runs per day on a repo agents push to
- A CI failure needs classification: real defect vs runner-environment flake
- You are about to edit a shared workflow file other sessions may also edit

## Why this class exists

GitHub emails the account on every FAILED Actions run. On an agent-fleet repo
(observed: 39 runs/day, one push every ~2 min), even a 15% failure rate means
multiple failure emails per hour that look unexplainable to the user. Two
independent noise sources stack: (1) run FREQUENCY (fleet pushes), and
(2) failure RATE (flakes + real defects). Fix both.

## Triage Chain

1. **Quantify**: `gh run list --limit 40 --json conclusion,createdAt --jq 'group_by(.conclusion) | map({conclusion: .[0].conclusion, n: length})'`
   Also group by day to see the trend.
2. **Correlate**: match failure timestamps against the user's complaint window.
3. **Isolate**: `gh run view <run-id> --log-failed` — find the failing step.
4. **Read before the crash**: grep the log for `FAIL|Segmentation|Traceback` AND
   examine what printed IMMEDIATELY BEFORE the crash. A success marker printed
   before a segfault means the test body completed; the crash is teardown.

## The Teardown-Segfault Class (observed 2026-08-18)

On GitHub-hosted runners (macos AND ubuntu, setup-python 3.12), a test body can
complete and print its success marker (e.g., `SELFTEST PASS: 4/4`), then the
interpreter segfaults ~2s later during shutdown. Unreproducible on local Pythons
of the same version. Naive CI treats it as failure; naive retry masks real bugs.

**Honest classifier** — pass ONLY when the body verifiably completed:

```bash
set +e
out=$(python3 "$g" --selftest 2>&1)
rc=$?
set -e
if [ $rc -eq 0 ]; then
  echo "$out"; echo "PASS $g"
elif [ $rc -ge 128 ] && echo "$out" | grep -q "SELFTEST PASS"; then
  echo "$out"; echo "PASS $g (teardown segfault after PASS — runner env, not logic)"
else
  echo "$out"; echo "FAIL $g"; fails=$((fails+1))
fi
```

- **`set +e` is mandatory.** GH Actions run steps execute under `bash -e`; a signal
  exit (rc >= 128) terminates the step before any `elif` classifier can run. A
  classifier without the guard fails open-loop — observed live.
- **This is not masking**: the classifier requires the printed success marker,
  which only exists if the test body ran to completion. A mid-test crash still fails.
- Adapt the marker grep to the suite's actual success string.

## Volume Control

- **Paths filter** on the trigger so doc/report pushes don't burn runs:
  ```yaml
  on:
    push:
      branches: [main]
      paths: ["gates/**", "stores/**", ".github/workflows/ci.yml"]
  ```
- **Runner choice**: prefer ubuntu for Python/sqlite suites; the macOS runner has
  its own segfault-11 flake class (observed hitting sqlite-based selftests).
- Before switching runners, grep the suite for real OS dependencies
  (`launchd|launchctl|/Library/|osascript|darwin`) — docstring mentions are fine,
  runtime calls are not.

## Real Defects Found During Triage

Flake classification is not an excuse to skip reading the code. The 2026-08-18
triage also found and removed a genuinely corrupted dead-code block in a gate
selftest (an `executescript(...) if False else None` construct with a malformed
INSERT inside). Always: reproduce locally under the same Python version CI uses
(`/usr/local/bin/python3.12` etc.) before concluding "runner env, not logic".

## Pitfalls

- **Classifier without `set +e`** — the signal exit kills the step before the
  classifier runs; you ship a "fix" that still fails (observed: first attempt
  failed with exit 139 for exactly this reason).
- **Concurrent-session pushes**: another agent session may push to the same
  workflow file between your commit and your push, interleaving results and
  resurrecting superseded file versions. Pull `git log origin/main` fresh before
  editing; after pushing verify your commit is HEAD and its run carries your
  message. Re-apply on top of sibling edits; never force-push over them.
- **Masking disguised as tolerance**: never retry-on-failure without a completion
  marker. Retry-only classifiers pass tests that never ran.
- **Local reproduction is the honesty gate**: if the failure reproduces locally
  under CI's Python version, it is a real defect — fix the code, not the workflow.

## Verification Checklist

- [ ] Failure count before/after quantified via `gh run list` JSON grouping
- [ ] Each historical failure classified (defect fixed vs flake classified vs runner changed)
- [ ] Classifier verified live: its run log shows the note string when the flake recurs
- [ ] Paths filter in place; doc-only pushes verified to NOT trigger runs
- [ ] No `set -e` between the command substitution and the rc check
- [ ] Your commit is HEAD on origin/main after the final push

## References

- Session detail backing this skill: teardown-segfault logs, the failing-first
  classifier attempt, and the concurrent-push incident live in
  `subtractive-design-review/references/` and
  `hermes-multi-instance-coordination/references/concurrent-push-hazard.md`
  (2026-08-18 Writing Studio / your-stack session).

## Related Skills

- `github-operations` — general GitHub CLI workflow (user-owned; adopt separately)
- `hermes-multi-instance-coordination` — lane discipline for shared-file edits