# 10-Step Process Fork Architecture

**Added:** 2026-07-19 — the 10-step flow is NOT linear. Three forks and two feedback loops are the architecture. Mapping them is the fastest path to "fully operational" because the forks are force multipliers.

---

## Why this matters

When asked to break down or revive the 10-step process, the temptation is to treat it as a sequential pipeline: Step 1 → Step 2 → ... → Step 10. That framing hides where the real implementation leverage lives. Three **forks** inside the flow are each force multipliers — wiring one fork unlocks disproportionate value relative to the lines of code. Two **feedback loops** govern iteration. Reasoning about the forks is how you phase the build correctly.

## The three forks

### Fork 1 — Confidence gate (after Step 3)

**Location:** Between Step 3 (determine if more context needed) and Step 4 (narrow coaching mode).

**Decision:** Is there enough signal in the user's message to produce a useful response right now?
- **YES (high confidence)** → skip directly to Step 9 (respond with value). Bypass Steps 4-8.
- **NO (low confidence)** → continue to Step 4 and begin gathering.

**Why it's a force multiplier:** Without this fork, every request runs the full pipeline even when a three-word answer would satisfy the user. Implementing the confidence gate alone collapses the median response time and frees the panel machinery for cases that actually need it.

**Runtime gap signature:** Every request produces the same depth of response regardless of signal strength. A vague one-liner and a detailed multi-paragraph request get the same treatment.

**Implementation note:** Confidence is not binary. The spec says "if the answer is uncertain but useful, state the assumption and respond." The gate is: can I produce *something useful* with what I have? If yes, respond with the assumption labeled. If no, gather.

### Fork 2 — Single-advisor vs panel (after Step 5)

**Location:** Between Step 5 (build advisor panel) and Step 6/7 (gather context / run advisors).

**Decision:** Does this request need a multi-advisor panel, or can one lead advisor answer directly?
- **Single-lane need** → skip Steps 7-8 (consecutive review, synthesis). One lead advisor answers at Step 9.
- **Multi-lane need** → proceed to Steps 7-8 for consecutive review and synthesis.

**Why it's a force multiplier:** Without this fork, every request either forces a panel (expensive, slow) or skips panels entirely (loses the moat). The fork routes based on actual need.

**Runtime gap signature:** Either every request gets a placeholder panel deliberation, or no request does. There's no routing logic that says "this is single-lane, answer directly."

**Implementation note:** The decision hinges on whether the user's need spans multiple lanes (e.g., a product question that touches marketing AND finance) or sits cleanly in one lane. Lead-advisor routing is the mechanism: one advisor whose lane most matches the request carries the primary answer; others contribute only outside that specialty.

### Fork 3 — Session fate (after Step 10)

**Location:** At Step 10 (continue or close).

**Decision:** What happens to the session after the response is delivered?
- **Continue** → user wants more; return to Step 4 with the new context.
- **Persistent** → user wants a 24/7 coach; enter `monitoring` state.
- **Done** → user finished; close with summary, preserve state for resumption.

**Why it's a force multiplier:** Without this fork, sessions either never persist (every interaction is one-off) or persist everything (storage bloat, no signal-driven re-engagement). The fork enables the persistent 24/7 coaching loop that distinguishes this engine from a Q&A bot.

**Runtime gap signature:** No `monitoring` state exists. No `next_checkin` scheduling. No `research_queue`. No `freshness_timestamp` updates. The `closed` state may exist but no summary is preserved.

**Implementation note:** See `references/spec-runtime-gap-audit.md` for the full monitoring-state architecture. The fork itself is a routing decision at the end of every response; the *infrastructure* it routes into (monitoring state + four signal watchers) is the build effort.

## The two feedback loops

### Loop A — Confidence re-check (Step 6 → Step 3)

After gathering one piece of context in Step 6, the flow returns to Step 3 to re-evaluate confidence. This is NOT infinite interrogation.

**Stop rule:** Maximum 1-2 questions, then answer with assumptions stated. The spec is explicit: "If the answer is uncertain but a useful answer is still possible, say what is assumed and respond. Do not stall the session just to avoid choosing."

**Runtime gap signature:** Either the engine asks no questions (always answers immediately) or asks too many (interrogates the user). The loop-with-stop-rule is what produces the "one question at a time, then answer" cadence.

### Loop B — Monitoring re-entry (monitoring → Step 1)

When the engine is in the `monitoring` state, four independent signal watchers run in parallel. When ANY one fires, the flow re-enters at Step 1 with the new context and runs Steps 1-10 again.

**The four watchers:**
1. **New research in domain** → `research_queue` fires. Fresh domain knowledge is now available.
2. **User goal drift** → `panel_revision_notes` fires. The user's needs have evolved; the panel should change.
3. **Panel obsolescence** → rebuild the panel (return to Step 5). Existing advisors no longer fit.
4. **next_checkin timestamp** → scheduled re-engage. Time to touch base.

**Critical principle:** This is signal-driven, not schedule-driven. A cron fires on a clock regardless of signal value. The monitoring loop fires on signal quality — it only interrupts the user when new information is materially useful. See the "this is more than a cron" pitfall in `references/spec-runtime-gap-audit.md`.

## Compact fork map

```
                Step 1 (start)
                    ↓
                Step 2 (domain)
                    ↓
              ┌─Step 3─┐  ← FORK 1: confidence gate
              │        │
         low conf    high conf
              │        │
          Step 4      ↓
              │     Step 9 (direct answer)
          Step 5 ←─── FORK 2: single vs multi advisor
              │
        ┌─────┴─────┐
     single       multi
        │           │
        ↓        Step 7 (consecutive review)
     Step 9         ↓
                 Step 8 (synthesize)
                    ↓
                 Step 9 (respond)
                    ↓
              ┌─Step 10──┐  ← FORK 3: session fate
              │          │
          continue    persistent
              │          │
           Step 4     monitoring ──→ signal ──→ Step 1
                          ↑                    (LOOP B)
                       (24/7 loop)

  Loop A: Step 6 answer → Step 3 (re-check confidence, max 1-2 iterations)
```

## How to use this for phasing a revival

The forks tell you what to build in what order, because each fork's value depends on the infrastructure underneath it:

1. **State machine into runtime** (enables Fork 3) — without real session state, you can't route to `monitoring`.
2. **Confidence gate** (enables Fork 1) — small to build, collapses median response depth correctly.
3. **Advisor deliberation** (enables Fork 2) — the product moat; heaviest build.
4. **Question flow + response type classifier** (enables Loop A with stop rule) — UX polish; depends on real state.

## Related

- `references/canonical-process-doc-set.md` — the 10 steps themselves
- `references/spec-runtime-gap-audit.md` — how to reconcile spec with runtime, including the four-phase revival order
- `references/four-coaching-modes.md` — the user-facing modes that sit on top of this process
