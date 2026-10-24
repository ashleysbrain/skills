---
name: hermes-cron-scheduling
description: Use when scheduling recurring the operator agent cron jobs.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [cron, scheduling, hermes, ops, watchdog]
    category: devops
---

# the operator agent Cron Scheduling

## When to Use

- Adding any recurring maintenance job: liveness watchdogs, catalog syncs,
  failure-only monitors, periodic digests.
- The CLI create path stalled and a direct jobs.json edit is considered.
- Verifying a scheduled job actually runs under the scheduler (not just
  manually).

Recurring maintenance jobs are scheduled through the the operator agent scheduler —
never hand-written crontab entries or launchd plists.

## Elite-brain gate (applies at creation AND at every audit)

Every agent-seat job (anything with a prompt) must carry all three elite
axes before it enters the fleet — a job missing any axis is a defect at
birth, not a later optimization:

1. **Model** — pinned to the current elite line (verify by probing the
   provider for what it actually serves, never by memory of model names).
   Unpinned jobs inherit the default, which is acceptable only while that
   default is itself verified elite.
2. **Credential** — the provider key live-verified with a REAL completion
   (HTTP 200 with content). A 200 on the models endpoint alone does not
   prove the chat path (a key can list models while completions return
   `content: null`). Probe before trusting; record dead providers.
3. **Brain content** — a named specialist with real pedigree IN the prompt:
   degrees + universities, layered methodology, named methods. A job whose
   NAME carries a specialist while its prompt carries none is the recurring
   failure shape — the name rides the title and the seat runs generalist.
   Canonical pedigree blocks live in
   `docs/persona-system/SCIENTIST-PEDIGREE-LAYER.md`; prepend the block,
   never rely on the job name.

Disabled jobs re-enable only through this gate. Zero-prompt script runners
are exempt from the persona axis, never from the credential axis. Jobs
carry `model` and `provider` as flat string fields in jobs.json — batch
uplifts match flat fields, snapshot via the cron_jobs_snapshot wrapper
first, and re-run the census afterward to verify (classify every job by
enabled / has-prompt / pedigree-present / model-line / provider-probe).

## Procedure

1. Write the script failure-only: silent on success, output only when it
   acted or could not. Healthy = zero output.
2. Place the script under `<agent-home>/scripts/` — cron resolves the job's
   `script:` field relative to THAT directory only.
3. Create the job:
   `hermes cron create --name "<name>" --deliver local --no-agent "every 60m" "<instruction>"`.
   `--no-agent` plus `script:` runs script stdout directly with no model
   turn; `--deliver local` keeps routine output out of chat.
4. If the CLI create hangs (it can exceed a 30s foreground timeout without
   writing the job), edit `<agent-home>/cron/jobs.json` directly: snapshot it
   first with `python3 /<workspace>
   --tag <label>` (takes the tagged backup AND prunes the bak stack to the
   glymphatic keep-5 policy — T-261006-0049; never bare-`cp` a bak by hand),
   append a job object matching an existing script job's shape
   (id = 12-hex, schedule {kind: interval, minutes: N} or {kind: cron,
   expr}, enabled, script, deliver, no_agent, prompt ""), save, confirm via
   `hermes cron list`.
5. Verify by forcing a run: `hermes cron run <job-id>`, then read the newest
   file under `<agent-home>/cron/output/<job-id>/`. "succeeded" or "silent
   (empty output)" is the pass state; a failure note names the actual
   lookup path the scheduler used.
6. Jobs guarding a principal-facing surface follow the watchdog liveness pattern
   (kill-test recovery once, HTTP 200 confirmed).

## Pitfalls

- **Script-not-found on first run** — the scheduler resolves `script:` only
  under `<agent-home>/scripts/`; a copy elsewhere (workspace dir,
  `<agent-home>/cron/`) fails with "Script not found" naming the expected
   path. Copy the script there before the first `hermes cron run`.
- **CLI timeout is not job failure** — `hermes cron create` can outlive a
  foreground timeout without writing anything. Check jobs.json before
  retrying, or go straight to the JSON edit path.
- **JSON edit without backup takes the whole fleet down** — one syntax
  error in jobs.json breaks every job; snapshot with
  `python3 /<workspace> --tag <label>`
  before touching it. The wrapper also prunes the bak tail to keep-5
  (min-age 3d guard) so hand-copied `jobs.json.bak-<tag>` stacks cannot
  recur (C1-cron-bak-stack, glymphatic bus #70543 / T-261006-0049).
- **Never assert the schedule from create output alone** — the next-run
  line can render "?" until the scheduler ticks; `hermes cron list` is the
  confirmation.
- **A script that succeeds manually can still fail as a job** — paths and
  working directory differ under the scheduler; always finish with the
  forced `hermes cron run` check, not the manual invocation.
- **`--no-agent` script jobs take no prompt** — a create call passing a
  script plus a positional instruction is rejected; drop the prompt
  argument entirely for script jobs.
- **Symlinked scripts fail the path check** — `script:` must be a real file
  inside `<agent-home>/scripts/`; a symlink back to the source repo is
  rejected as a traversal escape ("Script path escapes the scripts
  directory"). Copy the file in, and re-copy after editing the source.
- **Copy job IDs from `hermes cron list` output, never from grepped
  process output** — a hash lifted from an adjacent line fails
  `cron run` with "Job with ID or name … not found"; re-list and use the
  printed id exactly.
- **ASCII-fold names when batch-matching jobs by name** — accented
  specialist names (e.g. "Río Hortega") never match an ASCII-only key, so a
  fleet-wide uplift silently skips that seat and the census shows one thin
  survivor; match on the surname stem.
- **A delegation banner claiming a provider rejected the model can be
  transient noise** — verify with a direct completion probe before
  reconfiguring anything; banners have reported "not a valid model ID"
  while direct calls to the same model returned 200.
- **Batch audits must parse `schedule` as an object, not a string** —
  jobs.json carries `schedule: {kind: "cron", expr: "m h dom mon dow"} |
  {kind: "interval", minutes: N} | {}`. A regex against the dict raises
  TypeError, and an hour-window census ("what fires overnight") must read
  the HOUR field (field index 1 of the expr, minutes is field 0) and expand
  lists, `*`-steps like `*/45`, ranges, and bare `*` — otherwise the filter
  returns 0 jobs on a fleet that runs all night. Always-on loopers (`*/5`,
  `*/45`) count as night-shift load even though their schedule names no
  night hour.
- **Schedules in the host's sleep window fire late or fight the sleep** — on
  a laptop that sleeps, a job placed around 01:00-05:00 either misses its
  fire and runs hours late on wake (the Dispatch line in `hermes cron list`
  shows "catch-up after missed fire … N h late") or its maintenance wake
  keeps the machine churning on battery all night. Unless a job is genuinely
  24/7, place it inside waking hours: `hermes cron edit <job-id> --schedule
  "M H * * *"`, then confirm the Next-run line actually moved via
  `hermes cron list` — edit output does not echo the recomputed schedule.
- **Preflight mtime gates must filter bytecode/venv noise** — `__pycache__`/
  `.pyc` recompiles are not work; when a wake-gate's files-newer check counts
  them, a QA seat wakes with nothing real to gate and writes a verdict report
  from noise. Exclude `__pycache__`, `.pyc/.pyo`, `.venv`, `venv-embed`,
  `site-packages`, `.DS_Store`, `.log` inside the preflight scanner itself
  (never per-job), and re-run the scanner against the exact path that leaked
  to confirm it returns NO_WORK.
- **Set an explicit `delivery` on EVERY job at creation** — an unset delivery
  field defaults to the origin chat, so a QA/verdict organ's raw report lands
  uninvited as a file attachment. Internal-organ and QA-seat jobs get
  `delivery: local` (verdicts land under `<agent-home>/cron/output/<job-id>/`
  for division consumption); only curated digests the principal asked for ride to
  chat. When auditing an existing fleet, an unset delivery on any
  report-producing job is itself the defect to fix, independent of whether it
  has leaked yet.
