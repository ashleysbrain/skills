# Claim-Enforcement + Width-First Wave — session record 2026-09-04

Source: principal corrections 05:34–07:35 CDT, the specialist engine dispatcher session.

## Measured failure state (the evidence for the law)
- Bus: 13,883 messages, 24 id-sequence gaps; renumbering task T-260831-0058
  unclaimed 4 DAYS at tri:adversarial (deadline blown by 3).
- All 15 tasks minted 09-03 unclaimed at tri:review, including both principal
  verdicts (0045/0047, 18h+ past 18:00Z deadline), the pull-through cure
  itself (0051), taxonomy evolution (0059), failure-wheel research (0089).
- Fleet throughput in the same window: 52 tasks closed, 138 claims, 404 bus
  messages — the system processes volume; nothing forces principal-priority work
  through. 110 principal-origin active tasks, 41 overdue. 305 tasks open >48h.
- 421 open tasks dep-free (parallelizable); distinct ever-claimers: 21;
  claimed-now: sibling-agent 69, hermes 15.

## The three laws added to SKILL.md (condensed)
1. Dispatch done = CLAIM landed, not bus post. Checks at +1h/+4h/+24h.
2. Width-first: independent tasks fan out as concurrent mixed-harness waves;
   serial dispatch of dep-free work is a protocol violation.
3. Forced-claim fallback after escalation window expires: registry-first
  station OR isolated adversarial subagent seats for judgment work; verdicts
   recorded with full provenance (seat id, model, duration, summary path).

## The 2-minute datapoint
Two verdict tasks, 20h unclaimed in the voluntary queue → force-dispatched as
2 parallel NK-arm seats (glm-5.3, isolated, 9+8 api calls, 127s + 92s) →
complete evidence-cited verdicts (PARTIAL-FIT; PARTIAL with 5 named repairs).
Serial waiting cost ~600x the forced-width cost.

## Verdict-recording pattern (sqlite, direct)
UPDATE tasks SET state='done', done_at=<now ISO>, outcome=<verdict ≤3900 chars
with provenance>, stage='verdict:returned' WHERE id=<tid>; then read back
state+stage. Count gate openings from the ledger after recording, never from
memory of having posted about them.

## Seat corrections to pass through, not absorb
- Task details can carry WRONG source paths (one cited a ruling at repo root;
  actual location `audit/`). Seats find and report these — forward the
  correction to the ledger/task, don't silently fix in the verdict only.
- A seat may report a deadline as "past" when ledger shows hours REMAINING —
  deadline fields drift; re-read the task row before repeating any temporal
  claim to the principal.

## Artifacts minted this session
- Debrief: stores/session-debriefs/debrief-2026-09-04-mint-and-walk-away.json
- Policy: stores/dispatch-policy.json (width-first concurrent dispatch)
- Build order (the structural cure): T-260903-0051, severity-1, claimed to
  sibling-agent — claim-enforcement wave in glia_conduction.py, principal-priority lane,
  deadline re-attach at mint, trend-slope alarm in analytics_scout.py S1.
