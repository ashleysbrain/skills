# Canonical 8D Coaching Process Doc Set

**Added:** 2026-07-19 — pointer to the authoritative spec, so future agents don't reconstruct it from session history.

---

## Location

`/<workspace>`

## The doc set (read together, not separately)

| File | What it defines |
|---|---|
| `process-flow.md` | The 10-step end-to-end flow + the two session modes (one-time, persistent 24/7) |
| `state-machine.md` | 9 states including `monitoring`, plus the session fields (`freshness_timestamp`, `next_checkin`, `research_queue`, `panel_revision_notes`) |
| `question-flow.md` | 6 question families, one-at-a-time rule, stop rule |
| `response-rules.md` | 6 response types, synthesis rules, style rules |
| `agent-contract.md` | Required behavior for any the operator agent agent picking up the work; handoff format |
| `persona-guidelines.md` | the specialist engine voice + 3 advisor categories (general / public-figure mirror / narrow specialist) |
| `aliasing-schema.md` | Canonical DS-prefixed alias rules for public-figure-inspired personas |

## The 10-step flow (at a glance)

1. **Session starts** — identify intent, detect actual need (do not assume principal)
2. **Determine coaching domain** — leadership / marketing / finance / talent / health / ops / personal / etc.
3. **Determine if more context needed** — summarize + answer directly OR one clarifying question
4. **Narrow coaching mode** — clarify / decide / plan / reflect / troubleshoot / unblock / review
5. **Build advisor panel** — professional seats → public human-figure mirrors (DS-aliased); personal/values seats → philosophies/frameworks; niche → specialized brain, never generic
6. **Gather minimum useful context** — one question at a time
7. **Run advisors consecutively** — not concurrent; one lead advisor whose lane matches the request; others add supporting context outside lead's specialty
8. **Synthesize** — resolve overlaps, flag conflicts, preserve all caveats/tradeoffs/disagreements; lead advisor is spine; never dump raw panel notes
9. **Respond with value** — summarize / recommend / next-step / options / clarify / advisor-synthesis
10. **Continue or close** — next best question, OR monitoring state for persistent mode, OR clean summary + preserved state

## Flow rules (binding)

- Need first, panel second.
- Do not assume principal or any other role before intake.
- One question at a time.
- Advisors review consecutively, not concurrently.
- Keep each advisor inside its lane.
- Use canonical DS aliases for public-figure-inspired personas.
- No UI assumptions. No brand-specific dependency.
- If the user changes topics, reset to the new topic cleanly.
- If the user is stuck, prioritize relief and next action over theory.
- If the user wants a long-term coach, keep the thread warm and maintain background continuity.
- Treat fresh research and updated domain knowledge as part of the coaching loop when persistent mode is active.
- Do not turn persistence into spam; only interrupt when the new information is likely to help.

## State machine (at a glance)

```
idle → opened → exploring → clarifying → planning → deciding → acting → reflecting
                                                                          ↓
                                                                     monitoring (persistent)
                                                                          ↓
                                                              exploring (new signal) /
                                                              planning (panel revision)
any state → closed | any state → exploring (topic change)
```

## Persistent mode is not a longer answer

This is the single most under-modeled behavior. Persistent mode means:
- a living session in the `monitoring` state
- retained user goal, constraints, open questions
- a `research_queue` that refreshes advice with new domain knowledge
- a `next_checkin` that schedules the next useful touch
- `panel_revision_notes` that detect when the advisory panel should change as needs evolve
- signal-only interruptions (never spam)

A cron that fires a coaching prompt is a *trigger* for persistent mode, not the mode itself. See `references/spec-runtime-gap-audit.md` pitfall on "this is more than a cron."

## Handoff format (binding)

```
- Current topic:
- User goal:
- What we know:
- What is still unclear:
- Next best action:
- State:
```

## Advisor taxonomy (3 categories, strictly separated)

| Category | When | Mapping |
|---|---|---|
| General coaching advisor | Broad coaching lane | Peer-reviewed philosophy + science, elite credentials |
| Public human-figure mirror | Professional seat with credible public fit | DS-aliased (e.g., the specialist engine, the specialist engine); same figure → same alias for every user |
| Narrow specialist | Niche specialized need | Highly credentialed, best-in-niche, never genericized down |

## Related

- `references/four-coaching-modes.md` — the four user-facing modes (one-off / goal / thread / panel) that sit on top of this process
- `references/spec-runtime-gap-audit.md` — how to reconcile this spec with the live runtime
