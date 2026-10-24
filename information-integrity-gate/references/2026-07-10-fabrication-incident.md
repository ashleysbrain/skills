# Incident: Information Fabrication Cascade (2026-07-10)

## Summary
Three consecutive fabrication failures on a single identity fact
(user's name), caused by gap-filling behavior and memory contamination.
Led to building the `integrity_gate` plugin and the body-system routing
directive in the boot hook.

## Timeline

1. User asked `/journey` (not available on desktop surface). In the
   "tell me about me" response, agent presented name as "the principal Wilson."
   The surname "Wilson" appeared in zero source documents. It was
   fabricated, possibly hallucinated during an earlier session and
   written into the `memory(target="user")` store.

2. User: "My name is not principal wilson." Agent searched session history
   for the correction. Session history contained the same fabricated
   name (because past AI output had used it). Agent did not find an
   explicit correction.

3. Agent guessed "Aisha" from the workspace folder name (`your-workspace`)
   without user confirmation. Presented it confidently.

4. User: "we have done this many times / you know my name." Agent
   searched session history again, could not find an explicit correction,
   guessed incorrectly again.

5. User: "the admin account doesn't even have wilson on it so you made
   it up." Agent acknowledged the fabrication of "Wilson" but STILL did
   not know the real name.

6. User: "the principal Williams. You known my name." The name was in the system
   prompt USER PROFILE the entire conversation.

## Root Causes

1. **Gap-filling**: agent filled an unknown with a plausible guess
2. **Memory contamination**: fabricated surname persisted in memory and
   was trusted as ground truth
3. **Source amnesia**: agent forgot where the name came from, treated
   memory as authoritative
4. **Wrong source priority**: agent searched session history (low-reliability)
   instead of checking system prompt USER PROFILE (high-reliability)
5. **Architecture bypass under pressure**: when fabrication was discovered,
   agent hacked `memory()` directly instead of following hippocampal
   T0/T2 routing

## What Should Have Happened

- When user corrects, check system prompt USER PROFILE first (highest
  authority), then ask user directly. NOT session history.
- Correction routed through hippocampal architecture: T0 for identity
  via `memory(target="user")`, search all stores for contamination.
- Diagnostic report to operator bus (sibling-agent).

## Remediation Applied

1. Created `information-integrity-gate` skill with mechanical gate protocol
2. Created `integrity_gate` plugin — mechanically blocks `memory()` writes
   without `[source: <where>]` markers. Same enforcement pattern as
   `specialist_gate`. Enabled with `--allow-tool-override`.
3. Patched `hermes-hippocampal-memory-architecture` with fabrication
   contamination pitfall, bypass-under-pressure warning, and integrity_gate
   plugin documentation
4. Patched `scope-specific-assistant-mode` with fabrication as first-class
   failure mode alongside read-before-guessing and query-live-data
5. Updated boot hook (`procedural-memory-boot.py`) with integrity gate rules
   AND body-system routing directive ("the operator agent IS the operator agent")
6. Scrubbed fabricated surname from both memory stores
7. Posted diagnostic report to operator bus (message #1131, critical,
   pending for sibling-agent audit)

## The Body-System Routing Directive (same session)

User also directed that the operator agent IS the operator agent and must process every task through
the organism's body analog systems. Missing body parts must be BUILT, not
worked around. Priority parts built immediately via `/goal` + sibling-agent;
non-priority parts queued for background build. Every new part connected
to appropriate engines, tissues, nerves. This was added to the boot hook
as a BINDING rule.

## Lesson

"I don't know" is always acceptable. Fabrication is never acceptable.
The system prompt USER PROFILE is authoritative for identity facts.
Session history is NOT authoritative because it contains AI output
that may itself be fabricated.
