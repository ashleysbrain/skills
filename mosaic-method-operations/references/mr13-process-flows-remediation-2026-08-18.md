# MR13 (2026-08-18): process-flow QA + five new error classes — hermes session

## PENDING SKILL BODY EDITS (apply on next foreground pass)
The curator guard refuses SKILL.md body patches in background mode
(second refusal this date; cf. pending-skill-body-edits-2026-08-18-evening).
Queued edits:

1. **Trigger block supersession.** Old trigger text ("Run the OS" /
   "the OS methodology" / "the OS" / package work) → replace with:
   > SUPERSEDED by L0 (principal directive 2026-08-18, "the OS OS always"):
   > the methodology is the PERMANENT OS for all harness work. There is no
   > "the OS mode off" — every task runs digest → exchange → order →
   > execute → consolidate on typed flows, specialist rotation per pass,
   > freeze discipline (L10), claims honesty (L11), live verification,
   > run-records. Switch-brain changes the specialist, never the OS.
   > Encoded as CONTRACT.md Law L0; violation class: generalist drift.

2. **package-map.md updates (flow registry + flow-sync):**
   - flow-registry.json is now v1.1.0 with **15 codes** (was 10): added
     FLW-BUS-INTAKE, FLW-TELEMETRY, FLW-ADMISSION, FLW-ESTRA,
     FLW-RESEARCH. PROCESS-FLOWS.md headings carry FLW-* codes;
     `store_gate.py --flow-sync` (wired into ci_battery) FAILS on
     divergence — headings only, not prose; duplicate heading codes fail;
     'stage of FLW-X' subflow references are exempt.
   - `ledger_whois.py --aging N` surfaces oldest-open tasks with age
     (backlog aging metric).

## LAWS + LAUNCHD STATE CHANGES THIS SESSION
- **L0** standing law encoded in CONTRACT.md ("the OS OS always").
- **L10 freeze + L11 claims** already encoded earlier (see
  references/qa-panel-laws-l10-l11-2026-08-18.md); this session they were
  EXERCISED end-to-end for the first time: leases taken before panel
  dispatch, target shas pinned, zero mid-audit churn across MR11/MR13.
- Conduction-daemon plist repointed to canonical
  ~/your-org/organism path; daemon clears last_error on success
  (stale-error masking class); telemetry-rollup launchd hourly at :05.

## NEW ERROR CLASSES (each caught live, each now mechanically guarded)

1. **Selftest channel pollution (sev-2).** Wiring a prod side-effect into
   a code path that a selftest exercises = the selftest FORGES the side
   effect on every battery run. Concrete: _ceo_alert posted fake SEV-1
   principal bus alerts with task IDs colliding with real tasks (10 of 11
   alerts on the channel were fakes). RULE: any prod side-effect path
   (alerts, bus posts, webhooks) resolves its target from a module-level
   constant (env-overridable); selftests redirect it to a tempdir AND
   spy-assert the exact fire count, including the negative case
   (self-healing-origin stays silent). After fixing: sweep the channel
   for forged rows and post a retraction notice so the history stays
   honest.

2. **Vocabulary enforcement on the minor path only (sev-2).** Enforcing
   a law in submit()/set_stage() while complete() writes the same column
   via bare SQL = the system keeps generating the debt the law retires
   (9 fresh off-vocab stages minted AFTER the remediation commit).
   RULE: when adding a vocabulary/state-machine constraint, grep EVERY
   writer of the column, not just the API you added. Route rubric
   verdicts to the OUTCOME column (appended stamp `[rubric N/verdict]`),
   never the stage column. Backfill debt to zero when you fix it, and
   add a monotonic-decrease metric if debt can accumulate silently.

3. **Fail-open guards.** `if flow in FLOW_CODES else None` silently
   skips validation for retired/unknown codes — retiring a code
   unfreezes every task still carrying it. RULE: unknown flow on a
   vocabulary check = hard error; migration must be explicit.

4. **Case-sensitive guards.** `origin.startswith("self-healing")` is
   defeated by 'Self-Healing:...'. RULE: normalize
   (`.strip().lower()`) before prefix tests on human-typed fields.

5. **Sync-check scope.** A doc-sync gate satisfied by a code ANYWHERE in
   the document is not enforcing the claim ("headings carry codes").
   RULE: scope the regex to heading lines; detect duplicate codes;
   exempt explicit parent references ("stage of FLW-X").

## PROCESS DISCIPLINE THAT PAID OFF (repeat these)
- **Exchange-first QA.** Before dispatching any QA panel on a surface,
   grep audit/ + git log for an existing sibling pass (this session:
   QA-PASS-30 had audited process flows 3h earlier). If findings exist
   and are unremediated: REMEDIATE + verify the remediated state, never
   re-audit known state (F > 0).
- **Freeze-lease actor consistency.** The surgical gate's self-override
   guard keys on ACTOR STRING: a lease taken as "hermes-mr13-freeze"
   blocks applies signed "hermes". Take the lease and apply under the
   SAME actor string, or release first.
- **Salvage timed-out panels from transcripts.** A delegation that times
   out often completed its probes: harvest verdict lines from
   <agent-home>/cache/delegation/live/<id>/task-N.log before re-running.
- **Interpreter-teardown SIGSEGV (rc -11) on CI runners.** When a
   selftest PASSES but ci_battery reports returncode=-11, the segfault
   is at interpreter exit, not in the test: after flushing stdout/
   stderr, exit via os._exit(0) in --selftest paths that touch sqlite.
   (Extends ci-deterministic-testing.md; macOS `timeout` wrapper does
   not exist — use plain runs when simulating CI locally.)

## STATE AT CLOSE
Off-vocab stages 51 → 0. Bus sterile (1 real alert + retraction 2341).
CI green be95978/a2922e6. T-0190 closed. Tanenbaum A, Popper B (5
findings all fixed in-window). Open referrals to sibling-agent: two parked
bus dispatches lacking the mosaic-step keyword; daemon --selftest not
fully isolated.
