---
name: ceo-standing-law-enforcement
description: Use on principal always/never orders. Gate check same turn.
version: 1.0.0
metadata:
  hermes.tags: [ceo-orders, laws, gates, enforcement, mosaic]
  hermes.category: operations
  hermes.related_skills: [law-enforcement-gates, mosaic-os-conductor-laws]
  author: hermes
  license: internal
---

# principal Standing-Law Enforcement

## When to Use

- A principal message issues a standing order ("always X", "never Y", "every time
  Z", "this should never fail again", "I already asked you this")
- Auditing whether past principal laws are actually enforced
- Before minting any law-shaped ledger row

## The Defect Class

principal standing laws were minted as ledger rows + memory entries but enforced
NOWHERE on the write path. Measured 10-21: SCIENCE-FIRST receipt present on
1 of 787 BUILD rows; research-staleness and build-dispatch orders repeated
multiple times before enforcement existed. principal: "I had already asked you to

do this a couple of times… this should never fail again."

## The Rule

1. DIGEST the order; identify the mechanical shape (what artifact must
   always/never carry what).
2. MINT the law row (ledger) AND its gate check in the SAME TURN.
   - Enforcement lives at the write path (mint/claim/submit), fail-closed.
   - Existing gate: /<workspace>
     (SL1 lineage / SL2 dispatch / SL3 science-first; add SLn there).
3. FALSIFY: feed a violating row through the gate; verify rejection with the
   law id. A gate never tested against a violation is decoration.
4. Wire organic producers (gap_cycle template etc.) so healthy flows pass
   without friction.
5. REPORT: per-law rejection counts in morning packet; any principal repeat-order
   = retroactive gate-gap audit (find which law lacked its check).

## Isomorphism

Reflex arc: protective responses enforced at the spine, below conscious
routing. The cortex (conduction) is not asked each time and cannot forget.

## Pitfalls

- Never enforce via vigilance/reminder crons — gates at the write path only.
- Gate must VALIDATE, never write.
- A law too fuzzy to test mechanically: ask the principal for the measurable form
  OR mark it ORDERED-ONLY honestly.
