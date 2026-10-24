# Pending SKILL.md body edits — MR13 session (2026-08-18 evening)

Curator: fold these into SKILL.md at next foreground pass. Two new
sections + one reference pointer. Background session could not edit the
body directly.

## 1. Insert after "## CI discipline" section

```
## Selftest hermeticity (LAW — bit twice in one day)
Every external resource a code path touches (prod bus DB, prod stores,
network endpoints) resolves through a module-level constant set from an
env var; selftest redirects ALL such constants to tempfiles — never just
the obvious one. The MR13 defect: selftest redirected the ledger but a
helper hardcoded the message-bus path, forging SEV-1 alerts onto the
principal channel with task IDs colliding with real prod tasks. Assert side
effects with a spy counting calls; verify with before/after counts on
the real store (must be equal). Re-falsify via SUBPROCESS (as CI runs
it), never import — py3.14 spawn-mode breaks multiprocessing selftests
on import. Full pattern:
references/selftest-hermeticity-and-refalsify-2026-08-18.md.
```

## 2. Insert new section after it

```
## QA passes (fresh-brain panels)
- EXCHANGE-FIRST: before dispatching a panel, grep audit/ for a sibling
  pass on the same surface. Un-remediated sibling findings = remediate
  then verify the remediated state, never re-audit known state (F > 0).
  MR13 precedent: QA-PASS-30 had audited process flows hours earlier;
  remediation + verification panel instead of duplicate audit.
- A-grade condition: re-run the finding author's probes against the fix,
  on copies, via the CI execution path (subprocess).
- New vocabulary/state machine on existing data: audit ALL writers of
  the column, not just the new API — an unguarded writer (rubric
  close-hook writing stage= directly) regenerates the debt the
  remediation retires. Also check computed defaults actually reach the
  INSERT (dead default = every mint lands unstaged; 132 tasks fixed).
- MR13 record: references/qa-panel-mr13-exchange-first-2026-08-18.md
```

## 3. Add to "## References" list

- `references/selftest-hermeticity-and-refalsify-2026-08-18.md`
- `references/qa-panel-mr13-exchange-first-2026-08-18.md`

## 4. package-map.md drift (pre-existing, now stale)
flow-registry count says 10 codes; registry is now 15 (v1.1.0, gained
BUS-INTAKE, TELEMETRY, ADMISSION, ESTRA, RESEARCH; QA-PASS has a doc
heading section). Also task_ledger gained set_stage() API + BUS_DB
constant + env override.
