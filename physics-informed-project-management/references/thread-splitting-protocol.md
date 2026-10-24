# Multi-Thread Work Session Protocol (validated 2026-08-15)

For running several parallel principal workstreams inside one chat session before splitting them to desktop sessions.

## Thread lifecycle
1. LABEL each workstream on creation ([ESSAY], [STRATEGY], [SELF-HEALING OS], [WRITING]...). Use the label in every status line so streams never tangle.
2. When the principal asks to "start another thread" in a DM: Telegram DMs have no native topics. The working equivalent = a labeled parallel workstream in-session, staged for a desktop split.
3. Persist EVERY thread's state to O'Keefe (okeefe_bridge.py store) at each milestone — desktop sessions resume cold with no chat history.
4. On handoff, write a workspace handoff doc (e.g. THREAD-2-STRATEGY-DESKTOP-HANDOFF.md) containing: new facts with verbatim intent, sections + microtasks each with assigned brain, open questions for the principal, and banked artifacts it builds on.

## Cross-thread rules
- Threads share nothing in-flight: a thread's deliverables feed other threads only through banked artifacts (dossier, handoff doc, O'Keefe).
- Mid-thread thesis pivots (principal correction changing the framing) require triage of all banked deliverables in THAT thread: survives / rework / superseded. Never silently reuse superseded outputs in other threads.
- Writing thread founds on the strategy thread's identity statement but does not wait for it: cadence publishing starts on honest current assets; the big paper follows the strategy landing.

## ADHD accommodation (standing)
- Every thread's plan decomposes to 90-minute single-deliverable sessions.
- Status reporting: one table or short bullet board per thread, never walls of text.
- Open questions presented as a numbered short list the principal answers in one pass.

## Sequencing discipline (principal-corrected 2026-08-15)
- Sequential dispatch is the default for specialist chains: one micro-task in flight at a time unless the user explicitly approves parallel waves ("Not in parallel").
- When interrupted mid-sequence, resume at the exact interrupted step; check the delegation live-transcripts dir before re-dispatching anything.
