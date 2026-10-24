# Document QA Gauntlet: Rotated Elite Brains (validated 2026-08-20)

## The pattern
Sequential QA passes by DIFFERENT specialist brains catch disjoint defect
classes. A repeated brain catches repeats; a rotated brain catches new defect
families. Four passes, 26 defects, zero fabrication shipped on the TSC
explainer (audience: designer, HS-junior register).

## Pass schedule that worked
1. **Falsifier (the specialist engine)**: verify EVERY factual claim against named source
   files. Caught: blanket "biology IS the math" overclaim (physics audit says
   2 of 9 audited engines are physics-SOUND), invented scope, unsourced
   examples, wrong counts, an acceptance claim ahead of an unchecked
   submission checkbox, 10 em dashes. Result: FAIL, 9 defects.
2. **Domain expert (the specialist engine, physics)**: accuracy at the target
   simplification level; simplification wanted, errors not. Caught: naked
   "free energy" collapsing three distinct quantities (informational gate vs
   Friston variational vs Helmholtz), a table row implying BUILT when the
   audit rates it DECORATIVE. Result: PASS, 3 phrasing fixes.
3. **Meta-reviewer (the specialist engine)**: independent re-verification, do NOT trust
   passes 1-2; spot-check table with file:line. Caught: readability
   stumble-sentences, unglossed acronyms, source-attribution asymmetry, and
   the biggest real gap: the DESIGNER BRIEF (specs, audience, what NOT to
   draw, visual-metaphor inventory, hero-image concept) was missing entirely.
   Result: PASS-conditional, 3 must-fix + 8 should-fix.
4. **Voice/register reviewer (the specialist engine)**: register consistency for new
   sections, paste-ready context block accuracy vs body, first-try
   actionability of tool-setup steps, final leak hunt.

## Dispatch contract (what makes folding mechanical)
Each pass dispatched read-only with:
- named target file + named source files to verify against
- explicit numbered check list
- requirement: verdict PASS/FAIL + numbered defects + EXACT replacement wording
- "read-only: do NOT edit" (parent folds; avoids concurrent-edit hazards)
- pass N+1 receives prior-pass context but is instructed to re-verify
  independently (replication-as-QA). Two independent primary sources
  converging on the same methodological lesson = signal; raise priority.

## Fold discipline
- Fold ALL findings from a pass in one write (next version number)
- Mechanical scans before delivery: em dashes (excluding math notation),
  banned phrases, internal leak terms (outage/fallback/tooling/finding-IDs/
  census plumbing)
- Update the document footer's QA history line (passes, folded dates)
- Close the ledger task with a run-record citing each delegation ID + duration

## Leak rule (principal 2026-08-20)
Team-facing docs never mention internal tooling problems or workaround
narratives. Limits are declared as product facts ("still to verify: X"),
never as incident reports. Run-record stays in the task ledger.
