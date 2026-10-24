# Candidate-Claims Discipline + Delivery-Edge Clock Stamps (2026-09-03)

## 1. The single-brain fit-judgment shove (principal correction 10:33)

principal asked: "can my 5WH (who/what/when/where/why = how) methodology
structure the user→OS intake data flow? Don't force it."

What actually happened (the failure):
- Found ONE prior doc (ECOSYSTEM-ONTOLOGY-REVIEW-2026-08-21.md, which had
  ruled "5WH stays a reader's interrogation protocol, not a row schema"
  for INTERNAL telemetry stores).
- Read it myself, liked the fit for the NEW question (intake boundary),
  reasoned a mapping, and wrote it INTO the studio draft as a verified
  section with a quotable thesis line — all in one turn, no research seat,
  no adversarial seat, no triangle.
- Presented my own reasoning wearing research clothes.

principal: "it feels like you shoved my 5WH methodology into it as a the operator agent brain
... it needs to go through the triangle group and an adversarial pass ...
if it doesn't fit, I need to know that it doesn't fit. Don't lie to me."

The law this produces (general, not 5WH-specific):
- ANY "does X fit / should we use X" methodology-fit question from the principal
  is a RESEARCH question, not a reasoning question. Single-brain "I like
  the fit" output is a the operator agent-brain shove.
- Prior-art check must match the ACTUAL question grain. A ruling about
  internal schemas does not transfer to intake contracts; citing it as
  cover for an untested adjacent claim is scope-borrowing (fabrication
  family).

Recovery pattern (worked, verified):
1. Mint a falsification ticket: claim under test stated verbatim, prior
   art to check, NAMED counter-hypotheses (make them specific: redundancy
   between fields, collapse conditions like multi-intent flows or
   inarticulate-why, rival derivations of H), required verdict enum
   FIT / PARTIAL-FIT-with-boundary / NO-FIT. Route FLW-RESEARCH,
   research→adversarial mandatory before any answer reaches principal.
2. DE-VERIFY the artifact the same turn: mark the draft section
   `CANDIDATE — UNVERIFIED (pending T-id)` and strike the quotable thesis
   line so it cannot quietly survive as established. Verify both marks by
   read-back.
3. Tell the principal plainly what was wrong ("single-brain judgment wearing
   research clothes") — no vows, no behavior-change promises.

## 2. Delivery-edge clock stamps (principal correction 10:31)

The 08-27 time law said: header timestamps from a live `date` read in the
same turn. That is NECESSARY BUT INSUFFICIENT: a turn's tool work can run
for minutes, so a header stamped from the `date` at the START of the turn
is stale by the time the principal reads it — and reads as the clock being
pushed forward AGAIN.

Hardened rule: stamp from a `date` read taken immediately before the
message goes out (delivery edge, not turn start); re-stamp anything older
than ~1 minute. principal acknowledged the self-catch ("way to catch yourself")
but required it be done ahead of time: "make it not a thing."

## 3. Watchdog stock-vs-flow (bus #13216, principal-flagged process violation)

Build-stall watchdog fired 135 TRI_STATION_DWELL findings. Cross-check
found: 442 open tri-station tasks, 343 >48h old, only 38 claimed —
92% of dwell signal was UNCLAIMED dwell (routing defect), not build
stall. Lessons:
- A detector that reports COUNT (stock) without TREND SLOPE lets a
  routing defect grow for days with zero alarm. Every detector reports
  its trend, not its level.
- When one alert class floods (135 findings), fork the signature by
  actionable cause before dispatching fixes (DWELL-UNCLAIMED → routing
  lane vs DWELL-CLAIMED → build lane).
- Debrief pattern: measured_state (counts from SQL, not estimates),
  root_cause list, fixes list, one-line transferable pattern, linked
  task/bus ids — filed to stores/session-debriefs/ same session.

## 4. Writing-studio draft API: HTML-entity escaping

The :port drafts API returns content with apostrophes and quotes as HTML
entities (`&#x27;`, `&amp;#x27;` after double-encoding). Substring
verification of phrases containing apostrophes FAILS even when the content
landed. Verify with apostrophe-free probes, or unescape before matching.
PUT (not PATCH) is the update method on /api/drafts/{id}.
