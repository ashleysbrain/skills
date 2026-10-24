---
name: saved-thread-resume-protocol
description: >-
  Protocol for safely resuming a saved thread (.md file) by cross-checking
  against the live session DB, active Telegram/gateway sessions, and live
  service state BEFORE presenting continuation points. A saved thread .md is
  a snapshot, not ground truth — parallel sessions and live services may have
  already advanced the work. Use whenever the user says "pull up the X thread."
---

# Saved Thread Resume Protocol

## When to Use

The user says any variant of:
- "pull up the [topic] thread"
- "we were just working on..."
- "load the [topic] thread"
- References a saved `.md` thread file (PHYSICS-THREAD.md, ECS-THREAD.md,
  MARKETING-THREAD.md, PDF thread, etc.)

## The Problem This Prevents

A saved thread `.md` captures the state at the moment it was written. But
work continues across parallel sessions (Telegram gateway, TUI, cron jobs).
If you read only the `.md` and present its continuation/next-steps section
as authoritative, you will be stale — presenting items as "next" that are
already done, or priorities that have been superseded. The user then has to
correct you, which erodes trust.

**Real example (2026-06-20):** The physics thread's Section 9 listed
"build ECS coding system" and "run spine on 8D Sleep MVP" as next steps.
But the active Telegram session had already BUILT the ECS system (48 engines,
spec v2.0.0), shipped 8D Sleep (CI green), renamed the Maturation engine to
Semmelweis, and built a browser viewer. Four of six continuation points were
already done. The user had to say: "look at my current active session in my
telegram hermes... you are outdated and not working synergistically with the
telegram thread."

## The Protocol (5 Steps)

### Step 1: Read the .md thread file

Load the file the user references. This gives you the historical context,
decisions, and the author's intended continuation points. Treat these
continuation points as HYPOTHESES to verify, not facts.

### Step 2: Search the session DB for active/recent sessions on the same topic

```
session_search(query="<topic keywords>", limit=5, sort="newest")
session_search()  # browse recent sessions
```

Look specifically for:
- Sessions from a different channel (Telegram when you're in TUI, or vice versa)
- Sessions with more recent timestamps than the .md file's save date
- The LAST user message in those sessions — it reveals where work actually stopped

### Step 3: Check live service and artifact state

Verify the actual state of things the thread references:
```bash
# Services the thread depends on
curl -s localhost:PORT/health

# Git state — what's committed vs uncommitted vs unpushed
git status -s
git log --oneline -5
git log origin/main..HEAD --oneline

# Files that may have been created/modified since the .md was saved
ls -la <key directories>
```

If the thread says "X needs to be built," check whether X already exists.

### Step 4: Reconcile — compare .md claims against live reality

Build a reconciliation table:

| Thread .md says | Live state shows | Action |
|---|---|---|
| "Build ECS system" (next step) | ecs.py exists, 48 engines, v2.0.0 | Mark DONE |
| "8D Sleep MVP ship" (next step) | Repo in your-org, CI green | Mark DONE |
| "Rename Maturation engine" (next step) | :port reports "the specialist engine" | Mark DONE |
| "Quantum coherence layer" (next step) | No evidence of progress | Still PENDING |

### Step 5: Present the RECONCILED state, and update the stale .md

- Lead with what's changed since the .md was saved
- Present only GENUINELY remaining work as continuation points
- If the .md's continuation section is stale, **patch it** to match reality
  before the user has to ask (this prevents the same staleness next session)

## Variant: cross-channel thread takeover (proven 2026-08-15)

When the user says "move the [topic] thread from Telegram to here" / "take over and move it all here" — that is a MIGRATION, not just a resume. Additional steps beyond the 5 above:

1. **Find the source session and scroll to its END.** Discovery query on the topic, then scroll to the LAST messages. The critical artifact is the trailing edge: sessions closed mid-conversation have UNANSWERED user messages after the last assistant reply. Those messages are the actual work order — in the proven run, two trailing principal messages (a strategy expansion + the move request itself) sat unprocessed; everything the desktop thread needed to do was in them.
2. **Verify banked state independently.** If the source session banked verdicts to memory stores (O'Keefe, etc.), confirm they persisted (`recall` by topic) — never re-derive what already landed.
3. **Check the sibling lane** (operator bus / git log) before producing anything — the takeover must build on sibling work, not collide with it.
4. **Decompose the unanswered messages into sections with one specialist seat each**, dependency-ordered, and keep a visible board (section / seat / state) as the takeover progresses.
5. **Patch the source session's own handoff doc if one exists** (search for it — `*HANDOFF*.md`, `THREAD-*.md` in the workspace root): mark executed sections, flag open ones, and record any CONFLICTS between sources (in the proven run, a voice transcript and a written handoff disagreed on whether sales was a principal strength — flagged to the user, not silently resolved; voice transcripts garble exactly at compression points, so the written artifact usually wins pending confirmation).

Anti-patterns specific to takeover:
- Answering only the move request and letting the substantive trailing message sit unprocessed (the exact failure the source channel committed).
- Starting fresh strategy work without scrolling the source transcript — you will duplicate or contradict banked verdicts.
- Treating the source channel's session as dead: it may still receive messages; the takeover owns the TOPIC, so say so explicitly in the first reply.

## Anti-Patterns

- **DO NOT** read the .md and immediately present its Section 9 / "Next Steps"
  as your response without steps 2-4. That is the exact failure this protocol
  prevents.
- **DO NOT** assume the .md is current just because it was saved "today."
  Multiple sessions can run in parallel across channels within hours.
- **DO NOT** skip the session DB search because "I'm already in the right
  session." The user may have advanced the work in Telegram while you were
  in TUI, or vice versa. Cross-channel drift is the core failure mode.
- **DO NOT** present "next steps" that are already done. If you can't verify
  completion via live state, say so — don't assume either way.

## Quick-Start Checklist

When the user says "pull up the X thread":
1. `read_file` the .md thread
2. `session_search(query="<topic>")` — check for newer sessions
3. Check live services: `curl localhost:PORT/health`
4. Check git: `git status`, `git log`
5. Reconcile before responding
6. Patch the .md if its continuation points are stale

## References

- `references/vague-reference-recovery.md` — recovering a past conversation when
  there is NO .md thread file, only a vague user reference ("we were working on X
  yesterday"). Covers the 4-step escalation: discovery queries → browse → scroll
  → direct SQLite query on `state.db`.

## Related Skills

- `conversation-archival-before-compression` — saving threads before compression
  (the write side; this skill is the read/resume side)
