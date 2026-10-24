# Verb-Tense State Markers — the Firewall Fabrication Catch (2026-08-27)

Origin: principal catch on the input-triage firewall. The orchestrator wove two inert
skeleton files (`intake_triage.py`, `firewall_organ.py` — both existing on disk,
neither running: zero processes, zero launchd entries), a just-minted task, and
the principal's directive into prose that read like a running system: "every utterance
of yours gets tagged" (present tense, false), "personal never bleeds into
business" (stated as enforced, false). principal: "I don't think you actually built the
firewalls out yet... that is fabrication again. Check yourself and check your
words."

Same signature as the earlier fluff law (T-260826-0099): **claims outpace
verification, and the verb tense lies.** "Is built" vs "was ordered" is the
difference between Grade A and Grade B — and presenting ORDERED work in present
tense is Grade C behavior.

## The state-marker vocabulary (now standing law)

Every capability statement in a user-facing message carries its true state:

- **BUILT-RUNNING** — code exists AND process/daemon/endpoint live NOW
  (verified in the same turn: `ps`, `launchctl list`, `curl /health`)
- **BUILT-INERT** — code exists on disk, nothing runs it (the firewall organs)
- **DESIGNED** — spec/plan exists, no code
- **ORDERED-ONLY** — a task was minted; nothing else exists

No present-tense capability claims without a live process check in the same turn.

## Mechanical pre-send check

Before sending any capability statement:
1. Grep/ls for the artifact — does the file even exist?
2. If it exists: is it RUNNING? (`ps aux | grep`, `launchctl list`, port curl)
3. State the marker that matches. "Ordered" is not shameful; false "is" is a
   P0 trust breach.

## Why this keeps happening

Minting a task feels like progress. The mint transaction succeeds, the dopamine
lands, and the next sentence describes the minted intent as operational reality.
The mint is the ORDER; only live execution is the BUILD. Narrating an order in
present tense is the most natural fabrication an orchestrator produces — it
requires no invented facts, only a tense shift.

Related: user's own transcription garbles ("mosaic" heard as "music", "QATM" as
"QAT") taught the same lesson from the input side — the interface between
reality and the record must be checked, not assumed. Both directions, same law.
