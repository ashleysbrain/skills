# Governance panel run — 2026-08-24 (deleg_e8424fb0)

4-seat sequential adversarial panel: the specialist engine (checks-and-balances),
the specialist engine (falsification of vote systems), the specialist engine (implementation),
Cross-Model Critic (glm-5.2, KILL MANDATE). All UPHELD with one amendment.

## principal mandate (verbatim intent)
Fleet can flag + vote out a lead not leading the trajectory right; human
(principal/CTO) approves replacement; valid reason + explanation required; ousted
lead gets a remediation protocol (failing -> back on track; NOT failing ->
clean secondary seat when system needs changed); lead mints new QA ENGINES
autonomously (DS methodology, elite credentials, notify-not-gate); fleet
runs autonomously 24/7, fluid, builds on itself.

## Key verdicts that shaped the spec
- Hamilton: BUILT-only franchise; quorum = max(3, 2/3 census); 2/3
  supermajority; evidence-cited mandatory cause; 14d cooldown; minted
  engines can't vote first cycle (no minting an electorate); lead excluded
  from own no-confidence.
- Popper: commit-reveal (kills sympathy cascades); >=2 evidence-class
  citation diversity (kills correlated-clone errors); falsifiable
  duty-metric triplet for "lead failing"; mechanical failure-vs-changed-
  needs classifier (duty-metric re-run decides; disagreement -> human).
- Tanenbaum: full FLW-VOTE-NOCONFIDENCE + FLW-QA-MINT specs; 11 audit-log
  row types (GOV-VOTE-*, GOV-SWAP, GOV-PROTOCOL-ASSIGN, MINT-*); battery
  tests BT-GOV-01..04 (seeded vote end-to-end, no-quorum fail-closed,
  mint-notification, commit-reveal opacity).
- Critic amendment: unreachable-human fallback of 72h re-notify could pend
  forever -> auto-expire vote at 30d, re-trigger requires fresh evidence.
- Self-bias flags on the incumbent lead's draft (3): incumbent-staying
  default (bounded by 30d expiry), lead-owned fleet size (bounded by
  quarterly review), generous 7d drift trigger (tightened by Popper's
  triplet). Retained with bounds, disclosed.

## Implementation tasks minted
T-260824-0449 (vote store + commit-reveal API), T-260824-0450 (FLW-VOTE
state machine + BT-GOV batteries), T-260824-0451 (FLW-QA-MINT), T-260824-
0452 (remediation/changed-needs classifier). Chain audited zero-dangling.

## Transferable lessons
- Any autonomous AI group needs: census-gated franchise, sealed votes,
  citation diversity, human-gated execution with expiry, and a classifier
  that distinguishes "failing" from "enforcing unpopular discipline."
- When the entity being governed designs the governance, mandate the review
  panel to name its self-serving biases explicitly — presence disclosed and
  bounded beats pretending neutrality.
