# PENDING SKILL BODY EDIT — 2026-08-21 (apply via curator)

Curator: the background patch gate refused the edit this session ("content not
loaded in this review turn" despite name-only AND file_path skill_view loads,
one returning dedup/unchanged). Apply manually. Patch is unique-anchor, tested.

## Target section: "Dispatch discipline (binding, proven 2026-08-21)"

### old_string
2. **SHORT-OUTPUT RULE.** Every seat brief carries: "think briefly, then emit your final message in ONE pass, under 350 words, numbered list, no preamble." The final long reasoning turn is what times out; capping output kills the failure class at the root.

These two laws recovered the exact failure that cost 3h13m on 2026-08-20 (Bridgman pass).

### new_string
2. **SHORT-OUTPUT RULE.** Every seat brief carries: "think briefly, then emit your final message in ONE pass, under 350 words, numbered list, no preamble." The final long reasoning turn is what times out; capping output kills the failure class at the root.
3. **INCREMENTAL IN-CHILD WRITES (multi-seat single-child panels, proven 2026-08-21).** When N seats rotate inside ONE child, instruct it to write each seat's section to the output file IMMEDIATELY after finishing that seat (read+rewrite), NEVER holding all seats for one giant final turn. Also instruct: do NOT load extra skills beyond harness-forced ones (mandatory skill_view calls burned 2+ min of the child's budget), route the specialist gate ONCE at start as the chair, and include the exact gate re-route command for when the 5-min unlock expires mid-panel. Evidence: 5-seat architecture panel died to max_iterations + 150s non-streaming timeout with ZERO seats landed (606s wasted); identical roster re-dispatched with incremental writes + skill-skip + short-final landed ALL 6 seats (critic included) in 224s with per-seat file writes verified.

These two laws recovered the exact failure that cost 3h13m on 2026-08-20 (Bridgman pass).

(Also update "Two proven-laws" -> "Three proven-laws" in that section's intro line.)

## Evidence

deleg_a9e2d2f7 (5 seats, one giant final turn): max_iterations + 150s
non-streaming timeout x3 retries, 0 seats landed, 606s. Transcript:
<agent-home>/cache/delegation/live/deleg_a9e2d2f7/task-0.log (2+ min burned on
mandatory skill_view loads before any work). Re-dispatch deleg_51ee79f3 with
laws 1-3 in the brief: all 6 seats landed in 224s, per-seat incremental writes
to b2c-firstborn/REVIEW-ARCHITECTURE.md verified after each seat.
