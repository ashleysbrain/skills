# Strategy Session — Telegram Takeover + Funding Panel (2026-08-15, desktop)

The session that proved the source-pack architecture, R1/R2 dual-run adjudication,
and the cross-channel thread takeover. Companion to the strategy-panel-rebuild
reference (same morning, Telegram side).

## Context

principal moved a live Telegram strategy thread to desktop mid-flight ("this thread is
now for strategy from telegram... take over and move it all here"). The Telegram
session had closed with TWO unanswered principal messages after the Andreasen 11-seat
panel verdict landed (O'Keefe mem_951) — a large strategy expansion (sister-lab
alliance, hub equity vehicle, principal-talent design) plus the move request itself.

## Takeover sequence (proven)

1. `session_search(query="strategy", sort="newest")` → found the Telegram session
   by FTS hit; `session_search(session_id=..., around_message_id=...)` scroll →
   full transcript including the unanswered messages and the banked verdict ID.
2. Verify banked state independently: `okeefe_bridge.py recall` → verdict present.
3. Check sibling lane before producing anything (EXCHANGE step): operator bus →
   sibling-agent on Writing Studio reliability, zero strategy collision.
4. Decompose the unanswered message into sections (A alliance / B funding /
   C principal-model / D pitch assets), each with its own specialist seat, dependency-
   ordered (D blocked on B; A unblocked once B's R1 established SBIR structure).
5. Ask the principal only the questions that genuinely block design, WITH defaults
   proposed — principal answered 1/2/3/4 tersely ("default", "idk", "research it",
   "idk"); unanswered-by-choice items stay open variables in the design, never
   blockers. One question (pitch front) resolved by superposition → collapsed by
   instrument sequence when the data landed.

## The funding-seat casualty chain (what NOT to repeat)

- **v1 (long inline brief + web tools):** timed out at 900s. Transcript tail
  showed 15 minutes fighting broken tools: subagent web_search/web_extract empty,
  terminal output capture empty. Found the working path (execute_code + urllib)
  22 SECONDS before the cap. Lesson: read the transcript tail BEFORE re-dispatch
  (already in Timeout recovery above) — the tool-failure signature dictates the
  fix, and the fix was architectural, not a retry.
- **v2 (environment-brief inline):** dispatch echo came back corrupted —
  audio-transcription fragments, "askew" definitions, clinical text injected
  mid-sentence. Timed out producing nothing. Discarded unread, one-line
  disposition, zero attention spent.
- **v3 (source-pack, minimal context):** parent fetched 6 sources via
  execute_code+urllib in ~2s, wrote 35KB pack to disk, dispatched a minimal
  brief. Completed 499s, 11 API calls, all 6 URLs cited. Gate FAILED on
  PERSONA-SPEC-MISSING — the minimal brief had dropped the persona spec.
- **v4 (source-pack + full persona spec):** completed 799s, 15 API calls,
  gated PASS. Diverged from v3 on two points → adjudication (below).

## Divergence adjudication (the two decisions)

| Question | v3 (R1) | v4 (R2) | Winner + principle |
|---|---|---|---|
| Hub vehicle | SPV under parent | Subsidiary LLC ("SPV overkill") | v4 — adiabatic: same ring-fence at fraction of legal overhead; SPV deferred until real securitization need |
| First-raise range | $750K-1.5M | $323K-500K | v4 — dilution timing: never stack SAFEs pre-validation-paper; aim at what the structure requires |

Both verdicts banked with rationale; consolidated doc at
`strategy/DS-FUNDING-STRATEGY-2026-08-15.md`.

## Other seats (clean single runs, all gated PASS)

- **Executive Architect** (principal operating model): 228s, gated PASS first try.
  CONFLICT caught in consolidation: the Telegram voice transcript said "weak at
  ops and sales" but the desktop handoff doc records sales as a STRENGTH —
  flagged to principal rather than silently resolved. Voice transcripts are garbled
  exactly at compression points; cross-check against written artifacts.
- **Alliance Architect** (Gilchrist sister-lab): 277s, gated PASS. Caught the
  STTR caveat: for-profit partner cannot be the STTR research institution —
  route via SBIR subaward; academic bench holds the STTR lane.
- **Deal-doc producer**: dispatched WITH visible corruption in the context echo;
  child flagged it, located the real architecture doc (dispatch path was stale),
  grounded its NIH skeleton in the actual 6+1 engine names, gated PASS.
  Hard-gate-on-arrival (not auto-discard) is the right default.

## Baseline discipline that paid off

The Telegram session had written its own handoff doc
(`THREAD-2-STRATEGY-DESKTOP-HANDOFF.md`) with an S1-S5 microtask map. The
consolidation pass PATCHED it with execution state + the sales-strength conflict
flag instead of duplicating it — and surfaced genuinely open sections (S1.2 hub
economics, S1.3 Popper red-team, S2.2/S2.3, S4.2) that a fresh-start doc would
have silently dropped. First write of the consolidated doc tripped the
baseline-first gate (workflow_enforcement) — correct behavior: inspect the
existing artifact, patch it, then write the new one via execute_code fallback.

## Tooling failures survived (all cross-verified via subprocess reads)

1. `terminal` output capture dead session-wide (exit 0, empty string, even for
   `echo`) — execute_code + raw subprocess remained reliable.
2. `read_file` returned empty for a 4.7KB file that `os.path.getsize` confirmed
   existed (transient; second occurrence of the known intermittency).
3. Dispatch-context corruption in delegate_task echoes (2 of 6 dispatches).
4. `patch` failed an exact-match anchor present in the file (whitespace);
   execute_code string-replace with assert landed it.

None tainted the banked verdicts — every gate ran against on-disk transcripts,
every banked text was written and read back through the verified path.
