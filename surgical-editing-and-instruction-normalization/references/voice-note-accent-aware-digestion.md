# Voice-Note Directive Digestion — accent-aware transcription handling (2026-08-26)

Session-derived procedure for digesting the principal's voice notes, which carry a
country twang that garbles ASR output. Two real failures occurred same-day:

1. **"QAT / QATM"**: the principal's name for the QA team transcribes inconsistently.
   Resolved by matching against known fleet/team vocabulary before interpreting.
2. **"mastermind, synergy, and entourage effect"**: the transcript dropped
   "entourage effect" entirely; the agent digested a THREE-dynamic doctrine
   where the principal said FOUR. The principal corrected: "There should be four of them."
   The correction also came by voice, so the fix required canon cross-check.

## Procedure (order matters)

1. **Transcribe with a lossy-channel mindset.** The transcript is evidence, not
   ground truth. Note confidence-dropping patterns: dropped list members,
   homophone merges, invented compound words.
2. **Enumerate every list in the transcript and COUNT the members.** Then count
   the canon members of the same list (relationship dynamics, dimensions,
   engine families, laws). If the principal says "there should be N of them" and the
   transcript shows N-1, the missing member is a transcription loss — recover
   it from canon or the principal's correction, never invent a replacement.
3. **Cross-check domain vocabulary:**
   - Team/fleet names (QAT = the QA team; QATM is not a thing)
   - Standing doctrine lists (mastermind, synergy, symbiosis, entourage effect)
   - Engine names (always DS-prefixed; bare "Gilchrist"/"Williams" means the
     DS engine pair or the human partners — disambiguate from context)
4. **Digest into numbered directives on disk** (D1..Dn / M1..Mn), citing the
   transcript as source. None missed.
5. **Route per memory law:** durable facts -> O'Keefe T2
   (`memory_bridge.py remember ... --tags ...`); one-line pointer in the T0 block
   only; full digest on disk under technology-registry/.
6. **Amend, never re-mint,** when the principal corrects a digested doctrine: UPDATE
   the ledger record (append the amendment), store a fresh T2 correction memory,
   and note the transcription root cause so the pattern is findable later.

## Signals a correction is transcription-caused (vs. the principal changing their mind)

- The correction adds a member to a list the transcript truncated
- The correction renames something to a canon vocabulary item
- The correction phrasing is "remember, X needs to be in there" (recall of a
  prior intent) rather than "actually, let's do Y instead" (new intent)

Transcription-caused corrections get the accent-aware pass added to the
procedure; intent-change corrections get a doctrine amendment.
