# Conductor-reach census (MR14, 2026-08-19)

Trigger: principal asks to verify "process flows through ALL engines and
systems" / "flows through everything, the OS OS". This is a WIRING
census, not a spine health check — the conduction daemon (:port) can be
perfectly healthy while entire lanes conduct nothing.

## Census method (digest before dispatch)

1. **Wiring grep per system**: `grep -c '8280|message-bus|poke|task_ledger'`
   per engine file. Live wiring = fire-and-forget poke helper at write
   sites. Beware false positives: `genesis_engine.py` matched "bus" only
   in business-word content ("b2b", "customer") — verify each match is a
   real call, not prose.
2. **Store liveness**: db file mtimes + latest row timestamps. A db with
   no writers in weeks (task_crystal Jul 13, bragg Jun 25) is a DEAD
   ENGINE on disk — retire it to migrations/retired-<date>/, never wire
   dead code to the conductor (wiring theater). Zero-references grep
   confirms safe retirement.
3. **Schedule census**: `launchctl list | grep <label>` + `crontab -l`.
   Plist existing on disk does NOT mean loaded (autonomous-build: plist
   present, service never in domain, cron entry silent across 3 observed
   boundaries = build lane dead ~24h while everything looked configured).
4. **Then dispatch orthogonal fresh-brain panels per named lane**
   (rotation: after Popper/Tanenbaum came Feynman/Shannon/Wiener). Each
   brain gets: environment paths (canonical vs symlink), its lane's key
   files, 5 specific probes, report path, "NO EDITS to prod" unless
   verified-restorable.

## Five error classes found (all recurred before; recognize on sight)

1. **Keyword-filter fragility**: executor demanded literal "step" in
   prose; typed dispatches (build_request/task/design_request) parked
   forever (bus 2313/2315, ~24h). Fix: TYPE makes it a step; keyword
   check only for generic 'handoff' prose.
2. **Selftest prod-channel pollution**: any module-level path constant
   (BUS_DB, alert endpoints) that selftest does NOT redirect gets real
   writes from test runs — 10 of 11 principal alerts on the bus were selftest
   forgeries with colliding task IDs. Fix: module constant + selftest
   redirects it + spy-asserts alert counts; sweep fakes + post a
   retraction notice so channel history stays honest. Generalize: EVERY
   external surface a test touches must be redirectable.
3. **Healthy-silent vs dead-silent**: watchdogs that print nothing when
   healthy (virchow sweep) are indistinguishable from dead. Fix:
   heartbeat state-stamp every cycle (findings count + timestamp) to a
   state file a liveness probe renders.
4. **Raw INSERT protocol bypass**: app code opening message-bus.db
   directly (pipeline_api calendar push) skips validation, poke, and
   FORGES provenance (from_op hardcoded "hermes"). Fix: subprocess
   through operator_bus.py CLI; note --type enum (handoff/build_request/
   design_request — "request" is invalid).
5. **Off-vocab writes on the major path**: guard added to the minor path
   (set_stage) while the major path (complete() rubric hook) still wrote
   raw stage strings — the system kept generating the debt the fix
   claimed to retire. Fix: route EVERY writer of a governed column
   through the vocabulary law; add monotonic metric (off-vocab count
   must only decrease).

## Panel ops

- **Exchange-first**: grep audit/ for an existing pass on the surface
  (QA-PASS-30 existed) — remediate + verify rather than re-measure.
- **Re-falsification gate**: a finding is closed only when the original
  prober's exact probe re-runs clean (subprocess form, as CI runs it —
  NOT heredoc-stdin, which breaks multiprocessing spawn on py3.14).
- **Transcript salvage**: subagent exhausting iterations before writing
  its report is recoverable — the live transcript's think-lines carry
  each finding + evidence; reconstruct the report, then re-verify each
  salvaged claim yourself before filing it.
- **Disposition honesty**: remediated-in-another-lane dispatches get a
  resolution note (in_reply_to) + marked handled, never silently
  dropped or re-built.

## Open at time of writing

autonomous-build cron resurrection (root cause unread), Veritas gate on
live evidence ingest (sibling-agent lane, bus 2352), guardian bus reporting.
