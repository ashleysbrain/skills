# Search-before-asking and adversarial re-test discipline (2026-08-25 additions)

Companion to `false-done-marks-and-spy-verification-2026-08-25.md` and
`live-probe-daemon-verification-2026-08-25.md`. Two principal corrections from the
same session that did not fit those files.

## 1. Search your own history before asking the user who someone is
principal named "Dr. Gil"; the watch source was disabled and the principal was asked to
confirm the full name — yet `session_search("Gil")` returned him immediately:
Gil Alterovitz, Harvard biomedical informatics, discussed across many prior
sessions (funding landscape, QAI advisor, academic bench). principal correction:
"You know which Dr. Gil. You didn't search our history well enough."

Rule: before ANY "who/which/what is X" question to the user, run
`session_search` on the name AND grep user profile/memory. The lookup is
cheap and usually decisive. Only ask when BOTH come back empty.

Accent trap (same session): voice-note transcripts render names through the
principal's accent — "Glia" became "gleeya/glier", "crons" became "crimes". The principal
ruled the system must LEARN her accent: normalize transcripts against a
canonical glossary (Glia, Mosaic, sibling-agent, hermes, Karpathy) before treating
a name or term as unknown. Never let transcript misspellings leak into
naming, docs, or the ledger.

## 2. Fix claims need adversarial live tests of the FAILURE mode
principal: "I also don't believe the overnight starvation problem is 'fixed'."
The daemon fix had been demoed once with a hand-crafted probe whose values
matched the fix's own assumptions; the forced live re-test found TWO more
real defects:
1. Harvest filter used exact origin match `ceo-directive` while the ledger
   taxonomy mints principal tasks as `ceo:<topic>` — most real principal tasks invisible.
2. Novelty parser crashed on non-numeric task ids (`L12B`); in serve mode
   that exception means silent daemon death (try/except backoff, no alert).

Rules:
- A fix is verified only by a probe built from the REAL producer's data
  format, tested against the failure mode it claims to close — never by a
  happy-path demo. (Full recipe: live-probe-daemon-verification reference.)
- When the user voices disbelief at a fix claim, that is a signal to re-test
  adversarially, not to re-argue or re-assert. Both times the principal's
  skepticism was correct — budget for it as a defect-finding instrument.

## 3. Memory consolidation as the principal-praised exemplar
Memory store consolidated 100%->96% by REPLACING stale verbose entries with
tightened text (batch replace ops that shorten as they add) — not appending —
cited by the principal as exactly the execution standard: "surgical precision,
build for the future, not band-aids." At capacity: consolidate-and-shrink in
one atomic batch; never "no room, skip persisting" (that loses corrections).
