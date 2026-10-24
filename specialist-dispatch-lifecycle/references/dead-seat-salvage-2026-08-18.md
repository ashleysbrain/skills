# Session Detail: Salvaging Dead Audit Seats (2026-08-18/19)

Backing detail for section 4 of the parent SKILL.md. Two specialist seats
died in one QA pass; each needed different salvage.

## Death mode A — owner-exit at kickoff

**Signature**: batch result says "Delegation owner exited before recording a
terminal result"; transcript shows kickoff lines only; <1 min of wall time.

**Observed**: Knuth-class seat (6 structural HTML probes). Zero probes ran.

**Salvage**: nothing to extract. Two options:
1. Re-dispatch the same brief (it never started, so no moving-target risk).
2. Run the probes in-parent when the ENTIRE remaining work is mechanical —
   each probe was a single Python script (duplicate-id scan, tag-balance
   count, orphaned-reference walk, malformed-attr grep, onclick parse check,
   literal-`</script` scan). One script ran all six in ~2s. A re-dispatch
   costs minutes and a fresh context for work with zero judgment in it.

**Boundary**: in-parent completion is for MECHANICAL checks only. The moment
the probes require interpretation (is this wiring alive? is this copy
human-friendly?), that judgment belongs to a specialist seat.

**Outcome**: 6/6 probes clean + one real find (49 lines of dead code after
prior cuts) — the find's FIX was also mechanical (brace-walk amputation).

## Death mode B — hard timeout after full-budget work

**Signature**: last transcript line `status=timeout duration=900.2s`; the
log contains 15 minutes of real tool calls and findings.

**Observed**: Popper-class seat. Ran ~25 live probes against the API and
served page, surfaced 4 defects (restored cards in served page, malformed
panel attrs, unguarded deref, stale freshness numbers), timed out before
writing the verdict summary.

**Salvage**: the transcript IS the deliverable. Read the FULL log, not the
tail (the tail was already consumed during monitoring). Extract each find
with its timestamp and evidence, then:

1. **Re-verify every find against live state** — one curl/grep per claim.
   A dead run's findings are unverified self-reports.
2. **Check the moving-target hazard**: if you were repairing concurrently,
   defects found mid-repair may already be fixed. All 4 Popper finds were
   real-at-probe-time and already fixed by the time of salvage — the seat
   closes with "4/4 confirmed, real-at-probe-time, fixed during his run",
   not "4 defects outstanding".
3. **Chase loose threads he flagged but never resolved** (observed: a
   "forbidden strings: 7" count with no list — swept mechanically after;
   3 hits were the voice-checker's own detection array, not user copy).

## Verdict-table reconstruction

When the child died before writing its summary, the parent reconstructs it
FROM RE-VERIFIED evidence only (never from the child's characterization).
Format: | find (timestamp) | re-verified now | status |, one live probe per
row, committed to the audit record alongside the salvaged transcript
reference.

## Cost model

- Transcript read: seconds. Always do it before re-dispatching.
- Re-dispatch of never-started mechanical work: wasteful. In-parent.
- Re-dispatch of never-started judgment work: correct. Fresh seat.
- Re-verification of salvaged findings: mandatory either way.
