# Cross-Examining Subagent Refutations (2026-08-17, the OS QA passes 2-3)

A REFUTE verdict from an audit subagent is a claim about ONE probe context,
not a fact about the system. Pass 2 produced two false refutations, both
correctly identified only because the parent re-probed.

## The two incidents

1. **Lane-scoped refutation.** the specialist engine refuted the Sherman design-spec
   misroute ("write a design spec for the engine contract protocol") by
   probing the sibling-agent lane, which correctly refuses (GENERALIST_REFUSED).
   The hermes lane still misroutes the same phrase to ds-luria-engine.
   Verdict: REFUTED on lane A, CONFIRMED on lane B — a split verdict.

2. **Wrong-database refutation.** She probed one of EIGHT bus databases on
   the machine (<agent-home>/message-bus.db) and correctly reported no pending
   VERITAS thread there; the canonical bus (<agent-home>/message-bus.db is a
   DIFFERENT file from ~/your-workspace/message-bus.db) had it pending.
   Both auditors were right about different realities.

## Rules (binding for audit-wave parents)

1. When a seat REFUTES a defect the parent observed live, the parent
   re-probes on ITS exact lane, config, and database path before killing
   the finding. Split verdicts are a real, recordable outcome.
2. Never assume a single bus/DB/config store. Enumerate instances first
   (`find ~ -maxdepth 3 -name "*bus*.db"`) before treating any single probe
   as ground truth.
3. Rotate lenses across repeated QA passes on the same target. Pass 2:
   falsification / OS-architecture / information-theory (Popper, Tanenbaum,
   Shannon). Pass 3: exhaustive code verification / state-machine /
   store-integrity (Knuth, Lamport, Codd). Identical lenses re-find the
   same defects; different traditions find different defect classes.
4. Fix-your-lane-while-the-wave-runs is concurrent AND sequential-correct:
   apply own-lane fixes during the wave (registry version literals, bus
   thread closure, threshold bump, stale adapter doc rewrite all landed
   while the pass-2/3 waves ran); consolidate after all seats return.
5. The parent's own mechanical digest can contain bugs (an `open().strip()`
   AttributeError killed sections F-J of the pass-3 probe script). Fix the
   probe and re-run the section; never skip the section.

## Proven dispatch shape (both waves completed, no timeouts)

- 3 seats per wave, elite lane (glm-5.3), leaf role
- Each context: persona identity + pronouns, target paths, the KNOWN
  findings so far, "Respond in English, terse"
- Each goal: numbered questions (5-7), BREVITY cap 800 words, "probe LIVE,
  no code reads alone", "Do NOT write files. Return directly."
- Cleanup mandate for any seat that touches DBs (insert/delete probe rows,
  show cleanup counts)
- Parent writes the digest file (/tmp) BEFORE dispatch; every seat reads it
  first so the wave starts from shared ground truth
