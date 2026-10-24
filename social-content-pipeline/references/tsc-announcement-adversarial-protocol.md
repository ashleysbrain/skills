# TSC / Academic Announcement Adversarial Review Protocol

Protocol for writing scientifically accurate conference acceptance and
research announcement posts. Developed through the 2026-08-03 TSC 2026
announcement session (3-pass adversarial review, 8+8+8 fixes applied).

## When to use

Any LinkedIn post that:
- Announces academic acceptance, publication, or presentation
- Makes scientific claims about a software system
- References consciousness, biology, medicine, or clinical applications
- Introduces a field or paradigm

## The 5-seat adversarial panel

Dispatch via `delegate_task` with role=orchestrator. Include all 5 seats:

1. **Multi-agent systems researcher** — DEFENSIVE of AutoGen/LangGraph/CrewAI. Catches unfair characterizations.
2. **Consciousness scientist** — knows IIT, GWT, FEP, TSC standards. Catches proximity traps and loaded terms.
3. **Medical/research scientist** — catches clinical overclaims, drug interaction claims, disease modeling claims with no basis.
4. **Popper falsification auditor** — every claim must be falsifiable. Catches marketing dressed as science.
5. **Scientific marketing/copy reviewer** — catches generic hooks, AI tells, pacing, voice drift.

## Minimum passes

- **Pass 1:** Full 16-claim audit. Expected to find 4-8 FAILs/REVISEs.
- **Pass 2:** Verify fixes hold. Find anything pass 1 missed. Expected to find 2-4 residual issues.
- **Pass 3 (if medical/consciousness claims added):** Deep audit of new paragraphs for proximity traps and clinical overclaims.

## Key traps to watch

### Consciousness proximity traps
- "Substrate" = physical substrate of consciousness (NCC). Never use for software.
- Listing self-regulation + adaptive response as "consciousness indicators" = factually wrong.
- "Same indicators consciousness science has been developing" = overclaim.

### Medical overclaims
- "Drug interactions" for a software system = indefensible. No pharmacological basis.
- "Cascade failures in the body" = implies biological mechanism. Use "in complex systems."
- Conditional framing collapses: "If that holds" gets forgotten by the time you list applications.

### Terminology precision
- "Operating system" implies kernel/syscall/process isolation. Use "architecture."
- "Running operational principles" implies functional equivalence. Use "structured to mirror systemic role."
- "Measured" implies instrument calibration. I(S)=0.80 is a scoring methodology. Use "scored."
- "Mandatory" implies runtime enforcement (Paxos quorum). Actual is prompt-level + exit-code. Use "protocol-mandated."
- "Binding" same issue. Use "protocol-mandated."

### z.ai 429 handling (binding, user-corrected 2026-08-03)
- HTTP 429 "Insufficient balance" from z.ai is almost always a TRANSIENT
  rate limit, NOT a real balance issue. The same error message is returned
  for both rate limits and actual balance exhaustion.
- **NEVER shortcut the review when you hit 429.** The user said: "if you
  hit 429 don't short cut try again." Retry the delegate_task after a
  few seconds. The subagent uses the same provider (llm-vendor/glm-5.2) as the
  parent session.
- Verify the API is alive first: `curl -s -w "%{http_code}"` against the
  z.ai endpoint. If it returns 200, the 429 was transient. Re-dispatch.
- If the subagent genuinely cannot run after 3 retries, run the review
  yourself as the routed the specialist engine specialist. Do NOT skip the review.
- The retry typically succeeds within 60-120 seconds of the first 429.
- The parent session IS using glm-5.2/llm-vendor. The subagent inherits the same
  provider. A 429 from the subagent is NOT a reason to fall back to a
  generalist review. Either retry the delegate or run the review yourself
  as the routed the specialist engine specialist.

## Company repost blurb pattern (learned 2026-08-03)

When the Divinity Science company page reposts the principal's personal
announcement, the repost blurb must:

- Open with the NEWS as excitement, not as a memo ("just got accepted"
  not "is presenting")
- Reinforce that the operator agent is live infrastructure ("Not on paper. Not in a
  proposal. Live, running.")
- Signal the shift from stealth to public ("We have been building toward
  this moment quietly. That changes now.")
- Close with forward momentum, not a flat CTA ("This is the beginning of
  the story, not the end of it" not "Follow along")
- Read with genuine excitement. Company voice (we) but with energy.
- Run through ai-tell-removal-gate before presenting ("reach out" will fail)
