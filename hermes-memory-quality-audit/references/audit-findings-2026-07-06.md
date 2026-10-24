# Audit Findings — 2026-07-06 (Cycle 6, Weekly)

**Session:** `cron_*` weekly memory-improvement audit
**Cadence:** Continuing from `audit-findings-2026-07-02.md` (Cycle 5). No same-day duplicate.
**Option-C status (from Cycle 5):** Still active — memory backend empirically disabled in cron context (`skip_memory=True` by design). No structural fix since Cycle 5. Pre-authorized batch from Cycle 5 has NOT been applied (no interactive session executed it between 07-02 and 07-06).

## What this cycle added (non-duplicative delta)

### New finding type: `skill-locked` preferences
Added as a new classification tag in the methodology. Catches preferences/constraints that live in skills (loaded on demand) but should fire in all sessions (incl. cron/fleet). Concrete examples surfaced this cycle:

- **Orchestrator-cognition rule (2026-06-21 correction):** "The orchestrator's own brain must reason as the relevant specialist before delegating — not just route tasks." Currently lives in `ds-organism-engine-creation` skill body. Sessions that don't load that skill never see it. Candidate for memory promotion.
- **Two 2026-07-06 delegation lessons:** (a) verify subagent-quoted numbers against PRIMARY DATA not source documents (PIML 4-12x inflation case), (b) specify exact output paths in delegation goals. Currently in `agent-delegation-discipline` skill. Cross-domain lessons, candidates for memory promotion.

### New recall-pipeline blocker: FTS5 skill-injection noise
Every `session_search` call in this audit returned 140-630KB payloads. FTS5-highlighted snippets were dominated by repeated SKILL.md text injected into cron user-messages, not genuine user voice. This directly blocked retrieval of the prior cycle's actual audit report (every window-scroll landed on the skill-injection message). Added to the recall-pipeline evaluation table as a structural signal-to-noise blocker with three mitigations.

### Mitigations used successfully this cycle
- `role_filter` restriction was NOT applied this cycle (workaround discovered late) — next cycle should default to `role_filter=user,assistant` to exclude the injected skill text where possible. NOTE: this won't fully help because the skill is injected INTO the user role in cron sessions. The deeper fix is code-level (down-weight skill-injected segments in discovery ranking).
- Quoting exact user phrases helped marginally.

## What stayed the same (no delta — do not re-recommend)

- Memory tool unavailable in cron context (confirmed again).
- No web_search tool available in cron context for best-practices lookup.
- Option-C escalation still correct — same structural conditions persist.
- The pre-authorized batch from Cycle 5 remains the correct next action for the next interactive session.

## Recommended next-cycle action
1. Verify `role_filter` workaround effectiveness against FTS5 skill-injection noise.
2. If skill-injection noise continues to block retrieval, file as an engineering issue against hermes-agent codebase (this is a code-level fix, not an auditor-level fix).
3. Continue Option-C: do NOT regenerate per-finding recommendations until the loop is structurally closed (memory write access granted to audit, or interactive-session owner assigned).

## Cycle 6 proposed memory entries (deferred — for next interactive session to verify/apply)
Compact, pre-authorized entries ready for the next interactive session with memory write access. Verify against live store first; skip any already present:

1. `[POLICY] Orchestrator's own brain must reason as the relevant specialist before delegating — specialist cognition ≠ only spawning specialists. (2026-06-21)`
2. `[POLICY] Delegation hygiene: (a) verify subagent-quoted numbers against primary data, not restatements (metrics.json > marketing brief); (b) always specify exact output file paths in delegation goals.`
3. `[PREF] the principal has ADHD → ONE recommendation, no walls of text, no abstract synthesis without a concrete anchor. For system architecture, prefer visual diagrams over prose.`
4. `[POLICY] Memory-vs-skill ownership: preferences applying to ALL sessions live in memory (always injected). Procedural workflows live in skills (loaded on demand). If a preference exists in >2 skills, promote to memory and reference from skills.`
