# Starvation probe pattern: adversarial live-test of a daemon fix (2026-08-25)

The canonical worked example for failure-mode probing. Companion to
`live-probe-daemon-verification-2026-08-25.md` (recipe) and
`search-before-asking-and-adversarial-retest-2026-08-25.md` §2 (rules).

## Situation
principal rejected a "starvation fixed" claim: "I don't believe the overnight
starvation problem is fixed." The fix (a Glia conduction daemon harvesting
the principal task lane) had passed its happy-path demo.

## The probe sequence (proven live)
1. Mint a test task through the ledger's OFFICIAL API
   (`gates/task_ledger.submit(..., origin='ceo:starvation-test')`) — the
   taxonomy format (`ceo:<topic>`), not the filter's assumed literal
   (`ceo-directive`). This one difference is the whole test.
2. Snapshot daemon state (`stores/glia/cycle-state.json`) before.
3. Wait one trigger interval; re-read state; check `last_claim` and
   visible-lane count.
4. Verdict: cycles advanced but probe invisible = filter bug (found). After
   patch: manual `cycle` run surfaces a SECOND defect (non-numeric task-id
   crash = silent serve-mode death) that the daemon's try/except had been
   swallowing.
5. Only after: patch (prefix match + `_num()` safe parser), compile,
   manual-cycle, `launchctl kickstart -k`, live re-probe, THEN re-close the
   task with the run record.

## Why it worked
The probe was built from the REAL producer's data format (the taxonomy
file), so it exercised the failure mode the hand-crafted demo had defined
away. User skepticism was correct twice in one probe — treat expressed
disbelief as a defect-finding instrument, not a persuasion problem.
