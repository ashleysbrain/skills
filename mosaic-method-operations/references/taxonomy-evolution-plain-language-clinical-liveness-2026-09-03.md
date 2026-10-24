# Taxonomy Evolution Loop, Plain-Language principal Comms, Engine Liveness Census (2026-09-03)

Three principal corrections from the 11:20-11:40 CDT window of the writing co-work
session. All three generalize beyond that session.

## 1. Plain-Language principal Comms ("legal" jargon incident)

I told the principal "an essay pipeline with no legal task type is exactly the
outdated-flow class." principal: "I don't understand what you mean by legal. Are you
throwing legal out as like a fluff term there?"

"Legal" = on the closed list in stores/task-taxonomy.json (kinds/lanes the
ledger recognizes). "Illegal" = a value submit() rejects with ValueError. It
is internal jargon, and it leaked into principal-facing prose unexplained.

Rules:
- Never deliver system vocabulary to the principal without plain wording:
  "recognized by the ledger" not "legal"; "the review queue" not "tri:review";
  "the metadata gate" not "GENOME gate" unless explained in the same breath.
- When jargon leaks and the principal asks what it means, answer plainly (what the
  mechanism is, what happened concretely), then re-word permanently. Do not
  defend the term.

## 2. Taxonomy Evolution Loop (adaptability law, T-260903-0059)

principal: "how do we make sure that list evolves and doesn't just get rejected
anytime a new verb gets thrown at it... every component has to be adaptable
(build on, within, interchangeable)."

Manual taxonomy edits (add kind, add lane, backup first) are a STOPGAP, not
the system. The ordered design, dispatched to the engine lane:
1. SOFT-REJECT: unknown kind/lane accepts the task under a provisional
   prefix (provisional-writing) with provenance stamped, instead of raising.
2. Every rejection AUTO-MINTS a taxonomy-evolution candidate (kind=decision,
   "promote provisional <x>?") with usage evidence.
3. Promotion queue with pull-through (force-reroute once T-260903-0051
   lands); research->adversarial verdict, then ratification.
4. Versioning: every promotion/rejection bumps task-taxonomy.json version
   with a change-log; scout alarms on provisional-prefix volume trending up
   without decisions (trend not level).

Until shipped: any manual taxonomy edit = backup + record why the loop was
absent. The GENOME gate rejection in the same session (8d='early-warning'
not canonical, use adaptability/accuracy/etc.) is the same closed-rulebook
class; the evolution loop must cover both reject-without-candidate paths.

## 3. Engine Liveness Census (clinical family, T-260903-0060)

principal asked whether the diagnostic/oncology engines from months ago are "up and
live and scanning latest medical research." Measured truth:
- pairing-registry.json: full clinical family REGISTERED with symbiosis
  contracts (Osler, Rontgen, Semmelweis, oncology=the specialist engine, Humboldt,
  Sherrington, Cannon, Selye, Metchnikoff, Spleen).
- engine-contracts.json: ZERO ports for any of them; no /health anywhere;
  no pubmed/oncology/medical-research watcher in cron/flows/organism.
- Verdict: BUILT-INERT (reality law: registry entry without port + health =
  designed, not running; never call it "live").

Census method that produced this (reusable for any engine family):
1. Registry pass: pairing-registry.json + ecosystem-registry.json entries.
2. Port pass: engine-contracts.json -> port assignments for the family.
3. Liveness pass: HTTP GET /health on each port, short timeout, record
   ALIVE/DEAD.
4. Outward-sensing pass: grep cron configs, flows/, organism/ for the
   domain's external sources (none found = the sensing loop does not exist).
Note: immune-fleet angle passes QA OUR OWN outputs; they are not outward
scanners. A broad `find / -name` sweep times out; search the known store
directories directly.

Ordered build (T-260903-0060): ports+/health for the family; the specialist engine
outward watcher (PubMed, arXiv q-bio, trial registries) emitting typed
findings cards; isomorphism bridge -> findings become process-flow
improvement CANDIDATES in isomorphism-register.json through triangle
research->adversarial verdict (the Aug-21 anti-shove law generalizes to
medicine: findings influence flows as verdicted candidates, never direct
application); trend audit on scan freshness + conversion.

principal framing that motivated it: body isomorphism has been one-directional
(borrow anatomy for architecture, then stop listening to medicine); a body
that stops sensing its environment degenerates. Process-flow issues = body
processing issues; medical research on healing/clearance/conduction/tolerance
is the improvement source for flow mechanics.

## Cross-links
- Pull-through root cause + escalation recipe:
  references/unclaimed-dwell-escalation-and-pull-through-2026-09-03.md
- Closed-rulebook rejection mechanics (GENOME dimension traps):
  see "Ledger mint gate traps" in SKILL.md
- BUILT-INERT claim vocabulary: references/registry-first-routing-and-identity-drift-2026-09-03.md
