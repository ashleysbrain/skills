# Census→Registry Generation + Multi-Brain QA (2026-08-18, T-260818-0152)

## Pattern: store generates UI
- Census store (stores/connectivity.store.json) = single source of truth; UI
  registries are GENERATED artifacts (tools/generate_registry.py emits
  connection-hub/registry.gen.js, header "DO NOT HAND-EDIT", regen command
  in file comment).
- Collision-safe by construction: the generated file never touches
  hand-maintained app.js; sibling-lane panels are append-only sections.
  This lets parallel lanes proceed WITHOUT waiting for a bus round-trip.
- Merge semantics: census-over-hand by census_id, null-guarded (absent/null
  census fields NEVER override hand values). INHERIT: where the census has
  no opinion, the hand entry keeps its verified status.

## Status truth mapping
- Census probe records are evidence STRINGS with verdict words (not dicts).
  Map: ACCESSIBLE/PARTIAL -> live, AVAILABLE -> ready,
  DEGRADED/BLOCKED/EMPTY -> untested.
- NEVER fabricate a default status for records lacking one. Doing so
  demoted 5 verified-live badges to untested (caught live; code-read
  verification would have shipped the lie).

## Live DOM verification battery (caught 5 defects code-read missed)
1. Duplicate <script> tag -> "Identifier already declared" SyntaxError.
   Cause: a surgical apply SUCCEEDED but the report read crashed after
   applying; the retry double-applied. Always grep the file before
   re-applying after any post-apply crash.
2. Renderer reads the data array in MULTIPLE places (stats forEach, layer
   filter, card builder). Rewire ALL of them; one missed = silent partial
   render.
3. Generated entries lacking optional fields crash renderers (dims ->
   TypeError). Guard: (c.dims || []).
4. document.title instrumentation proves merge state when DOM greps fail:
   set title to array lengths (MERGED=33 CEN=17), read from --dump-dom.
5. chrome-headless-shell --enable-logging=stderr surfaces console errors.
- Decisive merge test: card count + a census-ONLY entry (location-history)
  rendering at all.

## Multi-brain QA cadence (principal law)
- "Another thorough pass, different brain" = NEW specialist(s) never used
  on that artifact. This stack: build (Da Vinci) -> art direction (Luria)
  -> claim falsification (Popper) -> systems + state gaps
  (Tanenbaum + Lamport).
- Reviewers REPORT, operator lane repairs + re-verifies. Salvage timed-out
  delegations from the live transcript
  (<agent-home>/cache/delegation/live/<id>/task-0.log), then verify each
  salvaged claim independently before filing it under the specialist's name.
- Freeze discipline: mid-audit remediation churns the auditor's evidence
  landscape. Either pause fixes during the audit window or timestamp-anchor
  every probe.

## "mosaic os" as an answer = full protocol, not the quick path
message-bus exchange (messages table: timestamp/from_op/to_op/msg_type/
subject/content/status) -> task_ledger submit/claim/complete API (never raw
SQL; kind/lane/flow validated against JSON registries) -> surgical_gate
edits -> live verify -> RUN-RECORD.md append -> push -> gh run list green.
Delegation ceiling: child_timeout_seconds raised 900 -> 1800 after three
specialists hit the wall same day.
