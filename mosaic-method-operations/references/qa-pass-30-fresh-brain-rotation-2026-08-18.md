# QA Pass 30 — Process Flows, Fresh-Brain Rotation (2026-08-18)

Session detail for the process-flows audit. Report of record:
`~/your-org/your-stack/audit/QA-PASS-30-PROCESS-FLOWS-2026-08-18.md`
(task T-260818-0178/0179, bus 2315). Report naming note: sibling sessions were
minting QA passes in parallel (28 = collab ADR, 29 = ADR v3) — grep
audit/RUN-RECORD.md for "QA pass N" BEFORE naming a new pass; numeric
collisions happened this session.

## principal directive 2026-08-18: DIFFERENT BRAINS EVERY PHASE

"Do it again. Different brains every process flows mosaic os" — when the principal
asks for another QA/review pass on a surface already audited, rotate a FRESH
specialist per phase. Protocol as executed (recorded in the report header as
L9 dogfood):

1. Phase 1 census — flow/architecture brain (the specialist engine: conduction rhythm)
2. Phase 2 data/stores — stewardship brain (the specialist engine: registry/doc/vocab)
3. Phase 3 live systems — sync/physics brain (the specialist engine: live daemon probes)
4. Phase 4 falsification — adversarial brain (the specialist engine: attack the stamps)
5. Phase 5 consolidation — circulation brain (the specialist engine: report + bus handoff)

Each phase's specialist+variation goes in the report header. This is what L9
SAYS dispatch recording should do automatically but doesn't (QA-27 M1) —
manual recording is the dogfood bridge.

## Reusable method: registry-vs-doc vocabulary audit

1. Extract codes from the registry (stores/flow-registry.json: 10 FLW-*) and
   section headings from the doc (PROCESS-FLOWS.md: 15 sections).
2. Cross-reference BOTH directions: registry-minus-doc (FLW-QA-PASS
   undocumented) and doc-minus-registry (Flows 9-13 VERIFIED but unregistered
   — the ledger validates against a registry missing its newest flows).
3. GROUP BY flow, stage over the live ledger: off-vocab stages
   ('rubric:1.0/PASS', 'bridged' = 29 tasks), flow-without-stage (130),
   no-flow (44). Stage is a suggestion, not a state machine.
4. Falsify documented mechanisms live: Flow 3b claimed severity-1 principal alerts
   on mint — 5 sev-1 mints, zero principal-lane bus alerts. Wired claim, absent
   wiring.
5. Semantic drift check: doc severity-1 = incident class vs ledger 163/203
   tasks at default 4 (priority). One number, two meanings.

## Sticky-error health semantics (durable pattern)

conduction_daemon.py L104 sets last_error on exception, never clears on
success — /health showed a stale OperationalError for hours while the daemon
cycled fine (live poke: 655 cycles, results []). Verdict pattern: read
last_error + last_cycle_at + cycles TOGETHER; a stale timestamp with a
climbing cycle count means the error string is a fossil, not an outage. Same
defect class hid autonomous-build for 7 weeks (QA-26). Fix spec (bus 2315):
clear on success, add last_error_at, expose error rate not sticky string.

## Environment facts verified this session

- Conduction daemon: launchd plist runs it via the your-workspace bridge
  symlink; WORKSPACE anchor in mosaic_chain_executor.py handles both roots
  (DS_ORGANISM_ROOT env override exists). run_once() executes clean from a
  fresh interpreter through the bridge.
- task-ledger severity distribution is priority-inverted vs doc semantics
  (1=highest priority in practice).
- Terminal guard: `&` anywhere in a foreground command (even inside a Python
  heredoc) is refused — use .intersection()/.difference(), never set `&`.
- specialist_gate routing expires after 5 minutes — a long analysis phase
  can outrun the gate window before the consolidation write; re-route
  (--route --situation ... --specialist ...) before the write step.
- Surgical gate leases work as documented for RUN-RECORD.md appends and
  typo fixes (anchor -> addition pattern).
