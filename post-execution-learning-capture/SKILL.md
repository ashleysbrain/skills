---
name: post-execution-learning-capture
category: operations
description: Capture what worked vs what didn't after any non-trivial execution (builds, surgeries, incident response, creative production runs). principal directive 2026-08-27 "neurons that fire together wire together" — learning that isn't written down is learning that didn't happen. Ends the manual-training-doc pattern (TRAINING-260827 gap section 4).
version: 1.1.0
author: the operator agent Agent (T-260827-0081, principal directive 2026-08-27; consolidated 09-09 qa pass — merged forked operations/ + documentation/ variants into one file)
---

# Post-Execution Learning Capture

## When to fire
- After SHIP verdict on any triangle-offense volley (consolidate ALL passes: review/research/build/adversarial/qa into one doc)
- At DONE of any ledger task with est_cost >= 1.0 (or any principal-directive task regardless of cost)
- At close of any incident / outage / adversarial kill
- End of any creative production run (the specialist engine/Bell/Luria pipeline)
- NOT for trivial mechanical completions (F > 0: cost exceeds info gain)

## Procedure (write ONCE, at completion, never retro-fitted later)

1. **Capture within the completion turn.** The capture doc is written in the same
   working window as the execution, while the failure modes are still concrete.
   If the session died first, mine the timeout/run logs — that is the fallback,
   disclosed as such, never presented as fresh memory. Author the doc EARLY in
   the session when wall-cap risk exists (wrap-order law, bus #5441).

2. **Write the 5-section doc** to
   `/<workspace><YYMMDD>-<topic-slug>.md`:
   - **What We Learned** — concrete outcomes, measured numbers, verdicts. Facts
     with state labels (BUILT-RUNNING / BUILT-INERT / DESIGNED / ORDERED-ONLY).
     No vows, no crescendos.
   - **Process Improvements** — what in the WORKFLOW helped or hindered; name
     the exact step and the fix. One line each, actionable.
   - **Tool Improvements** — what in the TOOLING (gates, CLIs, engines) helped
     or hindered; file:line where applicable.
   - **Skill Gaps** — capabilities that did not exist and were needed. Each gap
     either gets a ledger task minted NOW (with FLW flow tag) or is explicitly
     parked with a reason.
   - **Future Enhancements** — ranked, each with a first atomic step.

   Reference exemplar:
   `/<workspace>`

3. **Ledger wiring (the part that makes it stick).**
   - Mint skill-gap tasks in the same turn, tagged `est_cost` (never unscored)
     and flow per taxonomy.
   - Reference the training doc path in each minted task's detail.
   - Reference the minted task IDs back in the doc's Skill Gaps section.

4. **Post-mortem gate binding (law T-260828-0154).** Before any task close, the
   ledger enforces a post-mortem: `post_mortem_gate.py --scaffold <TASK_ID>` →
   fill 10+ entries across learnings/gaps/research_questions → `--file`. This
   skill's 5-section doc is the source material; transcribe, don't re-derive.
   Waivers need an explicit reason.

5. **Dispatch to QA fleet (the specialist engine seats at sibling-agent).** Post to the
   operator bus — the bus post IS the deliverable step, not an afterthought:
   ```
   operator_bus.py post --from <seat> --to sibling-agent --type result \
     --subject "LEARNING DOC: T-<id> <slug>" \
     --content "<5-section summary + evidence pointers for replay>"
   ```
   Include evidence pointers: lane logs, changed files, live endpoints, ledger
   ids, bus thread ids — the specialist engine replays from these, not from prose.
   Alternative: mint a ledger task assigned to the QA lane.

6. **Skill update when the learning is a PROCEDURE, not an event.** If a lesson
   changes how future work should be done (not just what happened once), patch
   the relevant skill's SKILL.md in the SAME turn — skills are where procedures
   live; training docs are where events live. Never duplicate a procedure into
   both.

7. **Memory discipline.** Nothing from the capture goes into harness memory
   unless it is a durable USER fact or ENV fact (memory routing law). Task
   debris stays in the training doc + ledger.

## Standing Rules Embedded (from the 08-27 volley)
- Two-clean rule: SHIP requires two consecutive ROTATED cleans, recorded in
  the rotation ledger — encode in checks, never operator memory.
- Interleaved volley: alternate adversarial seats with build steps instead of
  dispatch-then-wait.
- Gauges need a window AND a minimum-n; unwindowed averages fabricate.
- Registry-derived strings, never hand-typed; exact-match citation IDs
  (digit-transposition neighbors are distinct papers — real arXiv 1608.02238
  vs falsified 1608.03239, from the 09-06 adversarial pass).
- Wall-cap discipline: state-save + honest partial beats a fresh surgical edit
  when budget is low.

## Anti-patterns (each observed in the wild, 2026-08)
- Manual-only capture: TRAINING-260827 was written by hand with no mechanism —
  this skill is the fix; the doc must never again be the only record.
- Retro-capture: writing "what we learned" days later from memory produces
  plausible fiction — mine logs or say nothing.
- Naked closure: capture without ledger wiring means gaps never become tasks and
  the same gap re-fires months later (BUS_DEADLINE_BLOWN cohort 08-27 → 09-07).
- Procedure-in-doc: a how-to buried in a dated training doc is invisible to
  future sessions — promote it to the skill (step 6).
- Skill fork: two SKILL.md variants under different categories with the same
  name drift apart silently (operations/ + documentation/ fork found and merged
  at the 09-09 qa station). One skill, one file.

## Verification (what DONE means)
- Training doc exists on disk with all 5 sections, zero placeholder text
- Every named gap is either minted (task ID present) or parked (reason present)
- If a procedure changed: the owning skill file shows the change
- The completion ledger event references the doc path
- QA-fleet bus post sent (evidence: message id)
