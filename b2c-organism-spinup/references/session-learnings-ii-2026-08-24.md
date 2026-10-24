# Session Learnings II — 2026-08-24 late (QA fleet passes #7–#10)

Continuation of `session-learnings-2026-08-24.md`. Covers the afternoon/evening
chain: security passes, QA fleet org, governance, Glia naming, pass #9–#10.
Panel-level detail lives in elite-panel-chain-of-custody
`references/qa-fleet-build-chain-2026-08-24.md`.

## 1. Verifying a sibling's "done" (sibling-agent claim audit)

principal relayed "sibling-agent said it's done." Verification sequence (all four steps,
~2 min):
1. Ledger: `SELECT state,claimed_by,outcome FROM tasks WHERE id IN (...)` —
   found 3/36 closed, 33 still open (the claim was directionally true, not
   complete).
2. Bus: recent sibling-agent messages named the specific closes.
3. Disk: engine dir exists? `curl :port/health` (200 + identity JSON =
   real); registry grep for the entry; run the module's `--selftest`.
4. Diff claim vs DONE-criterion text: found (a) "3-substrate baseline
   COMPLIANT" run on boot files, not the 7-day logs the criterion required;
   (b) ECS code drift (ruled 12.06.01, built 14.01.01).
Both went back as ONE bus correction citing the criterion text verbatim.
Rule: accept partial truths by naming exactly what closed and what didn't;
never round a partial up in the principal report.

## 2. Mint hygiene (task-ledger, recurring traps)

- Same-day re-mint: compute `max(numeric suffix)+1` live — earlier
  collisions when assuming continuity.
- INSERT: explicit `created_at` (NOT NULL) + severity within 1–4 (CHECK);
  count `?` placeholders against the value tuple (off-by-one happened 3x).
- After minting a chain: resolvability re-audit + bus handoff (build order,
  preconditions, dependency notes) in the SAME script — the handoff is part
  of the mint, not a follow-up.

## 3. Governance panel with a conflict of interest

Current lead (Deming) ruling on her own succession rules: name the conflict
in the dispatch, give the critic an explicit self-serving-bias flag mandate.
Outcome: 3 bounded biases flagged (incumbent-default, lead-owned fleet size,
generous drift trigger), all retained WITH bounds + disclosure. Pattern:
bias present, bounded, disclosed — not denied.

## 4. Composite-isomorphism adjudication (pass #10)

principal proposed stem cells vs the glia ruling; the panel ran 4 concurrent-blind
seats each arguing one candidate at full strength (Yamanaka/stem, Golgi/glia,
Metchnikov/immune, liver-regen sweep) + sequential critic. Landed composite:
glia=org, polarization=engine variation, immune selection PRE-mint,
stem-cell bank=recruitment (census-gated). The critic's key corrections:
(1) famous 10:1 glia:neuron ratio is a myth (~1:1, Azevedo 2009) — the
maintenance-majority claim survives on workload; (2) blind clonal selection
(mint-then-kill) contradicts anti-chaos — selection operates on candidate
specs BEFORE mint; (3) naming a concept formally must check for vocabulary
collisions first (MODES already spent by ECS "cell types are modes").

## 5. BUILT/THEORETICAL as a standing report, not a narrative

principal: "you feel like you're starting to flirt with theoretical." The fix is
structural: a machine-generated reality census (qa-fleet-reality generator /
PROVENANCE engine) is the ONLY authority on fleet status. Any sentence about
"what we have" that isn't backed by that artifact is narrative. Designs
minted-but-unclaimed count as progress toward ZERO until claimed+built.

## 6. ADHD full-capture on recovered voice notes (reinforced)

The second recovered note (16:20) explicitly re-invoked the law: "every
single piece... they're all important." Digest pattern that held: number
every ask (N1..Nn / M1..Mn), write each into the evidence pack with an
action or explicit shelve, report the count back. Two notes, 14 asks, zero
dropped — the numbered digest IS the deliverable the principal checks.
