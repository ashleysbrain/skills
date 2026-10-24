# List Design Science: bounded portions over infinite scroll

Research base for the bounded-list law on principal-facing list surfaces.
Distilled from primary sources at intake; re-derive parameters from this
file instead of re-searching.

## The three converging findings

1. **Bottomless bowls (Wansink et al., Obesity Research 2005, n=54).**
   Self-refilling soup bowls led people to eat ~73% more while rating
   their fullness no higher than controls. Humans self-regulate consumption
   by VISIBLE PORTION CUES, not internal state. A bottomless container
   removes the stopping cue. Infinite scroll is a bottomless bowl: it
   deletes the "finished" signal and converts deliberate scanning into
   compulsive continuation.
2. **Agency and time perception (CHI controlled lab study, 2-condition
   design on a short-video app).** Infinite scroll measurably lowers the
   sense of agency and distorts time perception; replacing it with an
   explicit pagination/load-more control restores agency, and participants
   PREFERRED the bounded variant despite it being "less smooth".
3. **Mobile load-more threshold (Baymard Institute, year-long usability
   corpus across 50+ e-commerce sites).** On mobile, a "load more" button
   outperforms both infinite scroll and numbered pagination for
   scan-and-find tasks; the working threshold is ~15–30 items per load.
   Infinite scroll is never appropriate for task/scan lists on phones
   (footer items become unreachable, back-navigation loses position).

## The design law

- Initial portion: 15–20 cards (within the Baymard mobile threshold).
- Explicit continuation: a button labeled with the portion size AND the
  remaining count ("Show 15 more (45 left)") — the count is the portion-cue
  restoration; it tells the user how much bowl is left.
- Progress line: "1–15 of 60" (or "40 shown of 249 total") — the plate the
  user can see.
- Terminal state: "End of list" marker; small lists get "All N items shown
  — that is the whole list" so the boundary is felt at every size.
- Never auto-append on scroll. Each boundary is a decision point:
  continue, or act on what was just seen. This converts the list from an
  open system (no boundary condition) into a bounded one.
- Page parameters must be clamped to the real page count; over-range
  requests fall back to the last real page (prevents inverted ranges like
  "61–60 of 60").

## Partition-before-sort (ordering law for mixed boards)

A list can be perfectly portioned and still unfindable if the ROW SET is
wrong. Two findings converge on the same rule:

- **Set theory, not sequence.** Sort is a function over a set; applying it
  to the union of two disjoint kinds optimizes nothing because the kinds
  answer different questions ("what needs my hands?" vs "what did the
  system note about itself?"). Recency is only a valid key WITHIN a
  partition — across partitions it interleaves chatter above artifacts.
- **Findability is the acceptance test.** The principal's complaint pattern is
  not "the sort is wrong" but "I can't find the thing you told me you
  delivered" — i.e. the surface failed its retrieval job, which is a
  SET-COMPOSITION failure, not a pagination one. Bounded portions fix
  consumption; partitioning fixes retrieval. Both are required.

Rule: partition the row set (actions ⊎ journal), render the action
partition as the default view with kind-then-recency ordering, collapse
the journal below with its own count, and make every counter count the
action partition only. Verify by retrieval: after the change, the most
recently delivered artifact must be findable at card #1 without
navigation.

## Isomorphism (with deformations — not metaphor)

- list = meal portion; card = bite; portion boundary = satiety cue;
  count badge = visible plate.
- Deformation 1: a digital list has no stomach — the boundary is a
  deliberate circuit-breaker restoring the cue the bottomless container
  removed, not a biological signal.
- Deformation 2: fullness here is a DECISION (continue/act), not a
  sensation; the design goal is agency, which is measurable (task
  completion, time distortion reports), not consumption reduction for its
  own sake.

## Where it is implemented

Comments tab: 15/plate with filter-aware totals. Tasks tab: 20/portion
steps off a 40 default, capped at 200. The shared portion-nav helper owns
progress + continuation + end marker; new list surfaces reuse it rather
than re-implementing counters.
