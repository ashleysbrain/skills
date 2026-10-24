# Session Reference: The 2026-08-16 Second Catch (recurrence + re-injection)

## What happened

Day after the first catch, the SAME program shipped three new overclaims, and a
delegate spec re-injected the already-caught fabrication hours after the audit.
Two distinct failure classes, both new to this skill.

## Class 1: marketing copy graded as data (recurrence, worse source)

Topic 9 ("My sleep and my spending move together: 48 hours apart") was graded A
against NEWSLETTER-001/002, advisor-drafted marketing copy (authors listed as
"Sahil Bloom structure, Mark Hyman credibility, Quill polish"). The vivid
findings (48h sleep/finance lag, environment most predictive) were INVENTED for
the campaign voice. Ground truth: ashley_unified_health.db daily_scorecard has
27 sparse rows over 5 months, most NULL, July values frozen placeholders
(finance stuck 1.59, social 1.0). No lag correlation is computable.

Rule: marketing copy is not evidence, even in-house. Advisor-persona drafts are
voice targets, never data sources. Everything from the marketing directory gets
live-state verification.

Also caught same session: "live runs carry the statuses" (A to B; pipeline runs
carry evidence_level vocabulary, not claim grades) and critical-slowing-down
presented as a built detector (no engine implements it; benchmark design
vocabulary only).

## Class 2: re-injection after downgrade

The metadata downgrade (grade C + audit note in drafts) did NOT purge the
fabricated claims from the draft's CONTENT body: the brief still instructed a
writer to use "Week 1 data" findings. Four hours later a delegate spec used the
same fabricated lag as fuel in its first-five sequence table, marked [NEEDS
DATA] in a footer while the table presented it as fact.

Rules:
1. A downgrade rewrites the content body, not just metadata. PARKED briefs lead
   with parked status and name the fabrication.
2. Delegate outputs are screened against the known-false list BEFORE folding
   into plan docs. A footer disclaimer does not neutralize an asserting table
   row.
3. Every C-grade brief carries an explicit graduation condition. The audit
   found 2 of 4 parked briefs were missing theirs.

## Mechanical screens that worked (reuse verbatim)

- Regex the known-false phrases ("48 hour", "environment most predictive",
  etc.) across ALL docs, briefs, and delegate outputs; a hit is acceptable only
   inside an audit/downgrade context ("originated in", "fabricated",
   "graduation"), never as assertion.
- Grade consistency: metadata evidence_grade must agree with grade:X tags; B
  needs a reword condition; C needs a parked marking plus graduation condition.
- CJK scan on delegate output (one spec shipped two Chinese sentences in an
  English-only context; the user has corrected Chinese twice before).
- Em-dash scan on everything entering a principal-read doc.

## Outcome

Three topics downgraded (A to C, B to C, A to B) with bodies rewritten, two
graduation conditions added, the delegate spec purged and its Post 3 fuel
replaced with the claim-grading catch itself (real, self-referential proof of
the honesty system). Survivors verified: phantom-citation gate (code L292 plus
9 quality-issues runs), 1-of-7 OS assessment, 8D engine 701 lines, founding
essay.

Meta-lesson: an audit is not an event, it is a standing screen. The fabrication
came back through a new channel (delegate output) the same day it was caught.
Screens run on every artifact, every time, forever.
