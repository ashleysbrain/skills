# QA-Pass Remediation + Composition Protocol (MR13-MR15, 2026-08-19)

Distilled from three consecutive conductor/process-flow QA passes
(QA-PASS-30 remediation, MR14 conductor-reach census, MR15 composition).
Pattern proven across 20+ defect fixes, two verification panels, three
salvaged subagent runs.

## A. The exchange-first remediation loop (never re-measure known state)

When asked for "another QA pass" on a surface:

1. EXCHANGE: grep `audit/` for existing QA reports on that surface. If a
   sibling already filed findings, REMEDIATE THOSE FIRST. Re-auditing
   known defects is F>0 (physics gate: skip it).
2. REMEDIATE with the surgical gate (`your-stack/gates/surgical_gate.py`,
   `SurgicalEdit().apply(path, old, new, actor=...)`).
3. VERIFY each fix live — run the thing, don't read the diff. L11 Claims
   Gate: no claim without code-backed output.
4. DISPATCH fresh-brain verification panel on the REMEDIATED state (rotate
   specialists every pass; never the same brain twice in a row).
5. CONSOLIDATE: fix the panel's findings inside the same pass, then
   re-falsify the two worst ones yourself.

## B. Conductor-reach census method (does X flow through the conductor?)

The conductor = conduction daemon :port + mosaic_chain_executor +
message-bus. A subsystem "conducts" only if it POKES or POSTS. Census:

```bash
# 1. wiring census: which files reference the conductor at all
grep -rln "8280\|message-bus\|_poke_conduction" <dir>/*.py

# 2. dead-store detection: DB mtime vs last row timestamp
sqlite3 <db> "SELECT MAX(<ts_col>) FROM <table>"   # vs file mtime
# Fresh -shm/-wal mtimes alone = reader traffic, not writes.

# 3. scheduler split-brain: same job in cron AND launchd
crontab -l | grep <name>; launchctl list | grep <name>
# A plist that exists but "Could not find service" = never loaded.
# A cron entry that never fires = check /var/mail/<user> for the errors.
# Fix: pick ONE supervisor (launchd for the house standard), load it,
# delete the other leg. Prove liveness by waiting one full interval and
# seeing a SECOND self-fired cycle (kickstart proves nothing).

# 4. healthy-silent vs dead-silent: any "silent when healthy" watchdog
# must ALSO write a heartbeat state file, or the conductor cannot
# distinguish the two.
```

## C. Defect classes found (each fixed + falsified)

1. **Keyword-filter step gates**: an executor that requires the literal
   word "step" in prose will park typed dispatches forever. Typed
   messages (build_request/task/design_request) ARE steps by type;
   keyword checks only for generic handoffs.
2. **Gate exit-code contract violations**: a router that PRINTS "GO
   (exit 0)" but exits 1 on degraded status lies to every shell caller.
   Contract: REFUSE/blocked = exit 1; GO-with-degradation = exit 0, with
   degradation carried in the status field. Callers strand work items
   otherwise (picker never re-matches them).
3. **Selftest pollution of prod channels**: any test path that shares a
   module-global bus/alert path WILL write forged prod alerts (10 of 11
   principal alerts on the bus were selftest fakes). Fix: selftest redirects
   to a temp bus AND spy-asserts the prod channel stayed untouched.
   After fixing: retract forged rows + post a retraction notice (history
   stays honest).
4. **Write-only data lanes**: tables whose only consumer is COUNT(*)
   (brainstorm angle_threads). Fix by COMPOSITION, not a new consumer:
   wire the dead lane into an existing gated path (distill endpoint ->
   same Veritas-gated evidence pool the writing lane already reads).
5. **Raw sqlite INSERTs into the bus**: bypasses protocol validation,
   forges provenance, skips the conduction poke. Always post through the
   bus CLI (`operator_bus.py post`), which validates msg_type enums and
   pokes :port. Note the enum: handoff/result/status/alert/ping/pong/
   design_request/design_spec/build_request — 'request' is NOT valid.
6. **One gate vocabulary rule**: when a sibling gates one ingest path,
   compose the SAME gate call into the sibling paths rather than writing
   a second gate (FAIL refuses, other verdicts store with the stamp
   `pool_data.veritas_gate`).

## D. Historical-findings re-verification (before "fixing" anything)

Re-probe every historical finding against TODAY's live system before
counting it open. In MR15, all 6 QA-8 adversarial findings were already
fixed, and an initial misread (wrong key check in /health JSON) nearly
produced duplicate "fixes" for non-defects. A finding is closed only by
a live probe of the exact original symptom.

## E. Subagent iteration-cap salvage (see SKILL.md 4a)

status=completed + exit_reason=max_iterations = the deliverable usually
lives complete inside `subagent-summary-<n>-*.txt`. Persist it verbatim
with a provenance note; execute the child's unfinished state restores
yourself; verify criticals against live state before remediating.

## F. Micro-fixes worth remembering

- `flow-sync` gate: FLW codes count only in HEADINGS; a code mentioned in
  body text or a heading note creates duplicate/missing-code failures.
  One code, one owning heading.
- lane names in `task_ledger.submit()` are taxonomy-enforced — check
  task-taxonomy.json lanes before minting (a rejected submit at close
  time leaves the ledger entry un-minted; file the close in the bus
  instead and note the loose end).
- crontab edits via pipe (`crontab -l | grep -v ... | crontab -`) hang
  the macOS terminal tool. Write a temp file and `crontab /tmp/cron.new`.
- ws-good-* backups: refresh the studio API backup AFTER each verified
  pipeline_api.py edit (sibling guardian auto-restores from the newest
  ws-good-* on JS failure).
