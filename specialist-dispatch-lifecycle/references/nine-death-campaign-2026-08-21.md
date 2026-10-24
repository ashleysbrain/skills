# Nine-death campaign: late echoes, takeovers, and claim-vs-code (2026-08-21)

Campaign: 14 build lanes + 10 adversarial QA passes (~3h, telemetry/ontology
of the OS). 9 subagent deaths (6× HTTP 429 storm, 3× non-streaming API
timeouts). Every death salvaged or takeover-completed; zero lost findings.
Companion to SKILL.md sections 8-12 (which this file informed).

## Death taxonomy observed
- **429 storm**: kills a whole WAVE at once (6 concurrent). Recovery:
  staggered re-dispatch, max 3 concurrent, local takeover for small scopes.
- **Timeout at final write**: child gathers ALL evidence, converges, dies on
  the API call that writes the record (2× observed). The transcript holds
  the complete evidence chain — reconstruct the record with an explicit
  provenance header ("orchestrator-reconstructed from transcript, probe
  outputs quoted verbatim").
- **Iteration-cap truncation**: mid-analysis death; salvage partials from
  transcript into a shared partials file the re-dispatch reads FIRST.

## Late-echo mining (the highest-yield pattern)
Async completion echoes arrived 20min-7.5h after dispatch. Do NOT discard
as stale — check absorbed ledger state, then MINE the full summary for
detail you never read (you often read only the run-record header). Yields
from this campaign's echoes:
- Q9 echo → quarantine list with 2 actionable residuals (cycles readers
  LIMIT-1 staleness bug; contaminated Linear tickets)
- Q6 echo → 60× unit mislabel (minutes published as seconds) + false-
  absence probe flap (os.popen env-dependence) — neither in the run-record
  header I had read
- Q2/Q4 echo → PROBE_DEAD detector existed only in campaign prose, zero
  implementing code (claim-vs-code fabrication by the orchestrator itself)

## Zombie-write guard (run on EVERY late echo)
Corpses have modified files post-mortem. Before declaring no-clobber:
1. `stat` mtimes of the lane's files vs your own edit windows
2. DB canaries: latest self-healing cycle id, verdict-store head row
3. Only then declare clean — and log the check.

## Claim-vs-code fabrication class (the final gate's catch)
The campaign ledger claimed a detector that was never implemented. The
final falsification gate (census: every cited record exists AND size>0;
every "fixed live" claim re-probed) caught it. Two response options:
- Edit the claim down (weaker)
- MAKE THE CLAIM TRUE (shipped the detector, live-verified, regression-
  locked) — chosen.
Also caught: two cited run-records at 0 bytes (silent write_file gate
failure). Census must check SIZES, not existence. Recovery: direct
os.write via execute_code, then read-back verify; reconstruct with
provenance headers.

## Lock the invariant, not the prose
A test lock froze the exact prose of a registry annotation; a legitimate
upstream sync (the operator agent jobs.json → federation registry) changed the wording
and broke the suite. When reality is the source of truth, assert the
INVARIANT (job enabled, no fictional claim, cited labels real), not exact
strings that sibling systems legitimately rewrite.
