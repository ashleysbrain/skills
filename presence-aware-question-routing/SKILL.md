---
name: presence-aware-question-routing
description: Route any user question to their active interface.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [routing, presence, questions, ceo-surface, interfaces, communication]
---

# Presence-Aware Question Routing

## When to Use
- ANY time a question, approval request, or decision needs to reach the user — before choosing WHERE to put it.
- When a clarify() form, ratify button, or panel-roster approval would otherwise default to "the thread I'm in."
- When the user asks "why didn't I see your question" or "I don't understand what is needed of me" — that is this law failing.
- When wiring engine-originated questions (any the OS engine asking its user something).

## The Law (principal order, minted T-260826-0143, 2026-08-26)
Questions meet the user WHERE THEY ARE. Physics: cardiac conduction delivers the impulse to whichever chamber is receiving blood NOW — the signal follows the active circulation path, not a fixed address.

Presence rules:
1. **User-role message recency per surface wins.** Assistant/tool activity on a surface does NOT count as presence (the agent's own tool calls refresh timestamps and will lie to you).
2. **Open-but-idle loses.** The #1 real scenario: desktop thread open and running, user is actually on Telegram doing voice notes. An idle desktop window is not presence.
3. **Each interface renders natively** via its SME engine: Telegram = buttons + Other field (ADHD law), desktop = chat question card, sibling-agent = one-screen terminal prompt. Never render one interface's form into another.
4. **Questions follow the user.** Unanswered question + user moves surfaces = re-route to the new active surface. Question state must persist (queue/store), not live in one thread.
5. **Default = proceed autonomously.** Only genuine human-decision-class items route at all; "what is needed of me" should almost always be answerable with "nothing yet."

## The Probe (BUILT and live-tested)
`/<workspace>`
- Reads `<agent-home>/state.db` (sessions + messages): `SELECT source, MAX(timestamp) ... WHERE role='user'` grouped per surface, read-only URI.
- Stale thresholds: desktop 15 min, telegram 30 min, sibling-agent 15 min. Most-recent non-stale surface = the route.
- `--question "..."` adds the per-interface render directive.
- Known cost: the sessions join has no index — the query takes ~30s; budget the timeout (a 30s tool timeout will kill the probe).

## Minted-vs-Built (the meta-law this skill exists for)
The presence law was minted at 09:00 on 2026-08-26 and then VIOLATED twice the same day by the operator who minted it — an approval question parked in an idle desktop thread, then a Telegram status message claiming "buttons will come there" (telling the user the interface instead of detecting it). The user had to repeat the full order twice. Lesson encoded:
- **A minted law without its built organ is a narration device.** When a principal order produces a ledger task, the session is not done until either the organ is built or the gap is disclosed as "law exists, wiring does not."
- When caught having violated a standing law, verify the law's build state FIRST (ledger: `SELECT state, claimed_by, outcome FROM tasks WHERE id=...`) before apologizing — the apology means nothing if the build is still missing, and the fix is the build, not the words.
- Presence-detect before EVERY question, even when confident: the probe costs 30 seconds; a misrouted question costs a principal correction and a stalled workstream.

## Related failure class: "running now" narration
Do not send status messages claiming work is "running now" unless the dispatch result object is already in hand. The honest form is "dispatching next" (then dispatch in the same turn) or naming what is actually in flight. A status message that outruns reality is an anti-fluff violation even when sent to the correct surface.

## The render fallback law (principal correction 2026-08-26, defect T-260826-0153)
Two clarify() button cards sent on desktop both timed out unanswered; principal: "i don't see the questions and don't understand how to answer." The buttons-law intent is ZERO friction — a question card the user can't see or doesn't recognize as answerable is a failed surface, and the failure mode is silent (times out looking like "no answer").
- **Until the card render is verified working on a surface, questions render as PLAIN NUMBERED TEXT**: 3 options max, one line each, "type the number, or type your own words — your words override the options." State the default action on silence ("if you don't answer, I keep going" per standing rule) so non-answer is never ambiguous.
- Re-enable cards only after the user answers ONE real question through a card; that verification event is the re-entry condition.
- A timed-out question card is a QA signal to mint, not to re-send louder: log the defect, switch format, move on.

## Temporal discipline + the shutdown principle (principal corrections 2026-08-28, two strikes + one F)

**Strike 1 — clock-read law:** the operator signed off "good night" at 06:32 CDT — inside the principal's morning wake window (04:00–06:00), during the exact window a morning report was due. Root cause: inferred session phase from conversational rhythm (a long reflective message read as "session ending") instead of reading the clock. Binding rules:
1. **No time-bearing message (greeting, sign-off, "tonight/tomorrow" framing) without a live clock read in the same turn.** Run `date` before any temporal claim — no exceptions. Timezone awareness is the operator's job (convert UTC bus/ledger timestamps programmatically before quoting times).
2. **Message rhythm NEVER implies session phase.** Only clock + user-presence signals do. A reflective closing tone is not "goodnight"; it may be 6:30 AM.
3. **User-model accuracy beats system-model fluency:** principal wakes 04:00–06:00 CDT; works "whenever the hell he wants" — no principal schedule assumption is valid, ever. The OS works overnight; the principal is unscheduled. Never let a model of the system (circadian/overnight work) leak into a false model of the user.

**Strike 2 — the shutdown principle (principal LAW):** never say goodnight / sign off / close a session UNLESS the user initiates it ("I'm going to bed") or it is a genuine task/reminder context. principal's reasoning, captured verbatim in intent: shutting a user down mid-thought or mid-build kills the thought — users must feel EVERY thought is valuable and welcome, never ignored or dismissed. Universal across all users and organisms. The refinement: **sensing conversational closure is good intelligence — respond with AVAILABILITY (lighter touch, present, receptive), never termination.** The sense stays; the response changes. Sole exception: a B2C health organism may RECOMMEND sleep for the user's own wellbeing (care, not closure).

## Question lifecycle: the button-incident family, closed at root (2026-08-28, four incidents)

Three distinct root causes produced "buttons I have no context for" / "same buttons twice" — each needed its own fix; none were rendering bugs:

**1. Empty-brief fallback (context-free buttons).** Decision cards had a context system (what / why you / if-approved / if-rejected) but the mint-time fallback left 3 of 4 fields EMPTY when no written brief existed — title + buttons + nothing. Fix went in the emitter (`conduction_daemon.py` ceo_brief fallback fills all four fields from the task record), daemon restarted, verified against the live API (`:port/api/immune` → `rulings_pending[]` → each `ceo_brief` field truthy). **Law: every approval surface ships the full context block — what it is, why the user, what approving does, what rejecting does.** No exceptions, no bare prompts.

**2. Ratification-vs-decision (re-asking what was already ordered).** Tasks minted FROM a principal order (origin `ceo:order`/`ceo:training`/`ceo:question`) auto-rendered as approve/reject buttons — re-asking permission already granted. principal-verbatim orders render as "law recorded ✓" (one-line summary + timestamp + source quote); ruling buttons are reserved EXCLUSIVELY for genuinely open decisions. Batch-relief was applied by marking principal-verbatim decision tasks done/acknowledged at mint. Physics: a well-wired relay returns a command as confirmation, never as a question.

**3. Ruling writeback (THE root of "same buttons as earlier").** principal ruled the backup question IN CHAT (tiered architecture) — but only on-surface button clicks closed the question record. Chat answers had no writeback path → the conduction lane retried the "unanswered" question hours later to desktop then Telegram. Fixed by closing the stale record (linked to the ruling build) and minting the **ruling-writeback law**: ANY channel the user answers on (chat, voice, surface button) closes the underlying question record THE SAME TURN — the orchestrator writes chat rulings back immediately; the conduction lane checks question age against ruling events before retrying; retrying an already-ruled question = counted conduction defect. **A question loop without a writeback path is an echo, not a loop.**

Pitfall: when a question incident recurs, check ALL THREE layers before concluding the earlier fix failed — the incident family shares one symptom (bad buttons) with three independent mechanisms (brief rendering / mint-time auto-render / lifecycle writeback).

## Integration points
- **Panels** (elite-panel-chain-of-custody Phase 1.2): roster approval and principal-surface synthesis route by presence.
- **Operator bus**: cross-harness wiring (sibling-agent presence signal, question relay) is engine-lane work — hand off via bus post, don't build outside your lane.
- **Cron jobs**: autonomous runs must NEVER route questions (no user in the loop); they queue decisions for the next interactive turn.

## Pitfalls
- Do not count your own assistant/tool messages as user presence (the state.db `messages.role='user'` filter exists for exactly this).
- Do not hardcode a favorite surface ("always Telegram") — that flattens the law back into a fixed address and the principal will correct you again.
- The sibling-agent log-mtime proxy in the probe is a WEAK signal; treat sibling-agent routing as provisional until the sibling lane exposes a real last-user-activity timestamp (bus handoff pending).
- A clarify() form that times out with an empty response is NOT a yes and NOT a no — the work stays un-ratified, and you disclose that state honestly rather than proceeding as if approved. EXCEPT where the principal's standing autonomous-default order covers the class of work (spec-only, reversible, no public surface): then silence = proceed + the reversal path stays one tap away, disclosed in the same message.
- See `references/button-incident-debugging.md` for live paths, the 3-step diagnostic sequence, post-fix verification rules, and the GENOME-gate format gotchas learned while fixing the emitter.
