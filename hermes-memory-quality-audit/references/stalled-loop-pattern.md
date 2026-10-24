# The Stalled Audit Loop Pattern

Generalizable process pattern observed in the the operator agent memory-quality audit cron
(June 2026). Applies to **any** recommend-only review/audit/diagnostic process
that runs on a schedule but cannot execute its own fixes.

## The pattern

A recurring audit (cron, scheduled review, periodic diagnostic) produces a
report with correct, specific, actionable recommendations. The report is
delivered. Nothing executes the recommendations. The next cycle runs, produces
the same recommendations, delivers them again. Loop continues indefinitely.

## Diagnostic signals

1. **Findings are stable across cycles.** Run `session_search` for the prior
   N audit reports. If the findings list is ~identical across ≥2 cycles, the
   loop is stalled.
2. **No fix-attribution between cycles.** Search for memory writes, skill
   patches, or config changes timestamped between two audit runs that
   reference the prior findings. If zero matches, nothing was executed.
3. **The audit context lacks write access.** Cron sessions skip memory
   injection by design. If the audit runs as a cron with no path to apply
   fixes, the loop is structurally guaranteed to stall.

## Why it happens

- The audit is framed as "produce a report" rather than "close the loop."
- The audit context (cron) has read access to prior state but no write access
  to apply fixes.
- No explicit owner is assigned to execute recommendations between cycles.
- Recommendations are phrased as discussion prompts ("consider adding X")
  rather than pre-authorized batch operations.

## Case study: the operator agent memory-quality audit, Jun 4 → Jun 25 2026

Four consecutive weekly audits identified the same six content-side findings
(blended routing note, missing exact-corrections preference, missing
memory-maintenance expectation, missing model-policy note, stale Honcho
provider state, memory at ~99% capacity). None were executed. The June 25
audit's primary finding shifted from per-item content issues to the structural
loop failure itself.

**Physics-informed read:** four recovery cycles with zero convergence is a
critical-slowing-down signal. The system is near a tipping point. Continuing
to push the same intervention is the wrong move — redesign the loop.

## Fixes (priority order)

### Option A — Grant the audit write access (preferred)

If the audit is the correct owner of the fix, give it the capability to
execute. Either:
- Configure the cron to run in a context with memory write capability
- Convert the cron trigger into an interactive-session trigger
- Add a post-audit execution step that runs in an interactive context

### Option B — Pre-authorize execution

When recommendations are verified across ≥2 prior audits, stop phrasing them
as discussion prompts. Format them as a copy-paste batch with exact
`old_text` / `new_text` pairs. The next interactive session runs the batch
as a pre-authorized action list, not a re-deliberation. Include the
prerequisite space-freeing step if memory is at capacity.

### Option C — Stop auditing, escalate

After 3+ stalled cycles, convert the audit into a pure escalation. The report
becomes: "The loop is structurally stalled. Stop running per-finding
recommendations. Fix the loop first (Option A or B). Then resume per-finding
audits." Do not generate the same per-finding list a 4th time — it has
near-zero information gain and trains the user to ignore audit output.

## Generalization

This pattern is not memory-specific. It applies to:
- Any cron-driven diagnostic that reports but cannot remediate
- Any recurring review process (code review, security audit, compliance sweep)
  where the reviewer lacks commit/merge authority
- Any "generate recommendations" agent that never gets paired with an
  "execute recommendations" agent

The fix is always the same shape: either give the reviewer execution
authority, pair them with an executor, or stop running the review until the
loop is closed.

## Anti-pattern: the generalist fallback

When the audit identifies that fixes were not executed, the wrong response is
for the auditor to hand-write the missing memory entries itself as a
one-off. That:
1. Doesn't fix the structural loop (next cycle stalls again)
2. May apply fixes without the interactive-session verification the loop was
   supposed to provide
3. Conflates "I noticed the gap" with "I am the right agent to close it"

The correct response is to escalate the loop stall and apply Option A, B, or C.
