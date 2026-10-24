# QA Fleet Build Chain (2026-08-23/24) — passes #7–#10

Session reference for the principal-driven QA-fleet design chain. Ten adversarial
passes in two days; each pass's evidence pack + review live in
`/<workspace>` (QA-*, DS-WILLIAMS-*,
B2C-*, DS-TRAJECTORY-*, QA-GLIA-PASS9-*, QA-ISOMORPHISM-PASS10-*).

## The consolidated fleet (as ruled through pass #10)

- **Name:** The Glia (internal codename) / Quality & Trust Layer (public).
  Critic correction: glia:neuron ratio is ~1:1 (Azevedo 2009), NOT 10:1 —
  the "maintenance majority" claim survives on workload, not cell count.
- **Org:** principal → the specialist engine (LEAD) → seats; the specialist engine = scheduler;
  autonomous_iteration daemon = conductor. Engine ECS block 12.04–12.09
  (Williams/Gilchrist/Margulis/Goldman-Rakic/Hebb/Denning).
- **Governance:** no-confidence vote (franchise = BUILT engines only,
  census-gated; commit-reveal sealed votes; ≥2 evidence-class citation
  diversity; 14d cooldown; 30d human-gate expiry), human approves via
  BUTTONS, remediation-vs-changed-needs classifier, lead mints engines
  autonomously w/ free-energy demand gate + notify-only.
- **Engines-vs-agents law:** ONE hyper-specific task, own model, own
  harness, machine-checkable DONE, kill criteria, harness-into-able;
  graduate at ≥20 runs + 95% held-out.
- **POLARIZATION (pass #10):** the principal's "chameleon-like engines" concept,
  formally named. Fixed core + named signal-selected states (AUDIT/REPAIR/
  STANDBY), each state REQUIRES exit criteria (anti-scarring: a state
  without exit = accidental mode). MODES rejected (ECS collision),
  PLASTICITY rejected (too vague to gate).
- **Composite isomorphism:** glial fleet (org) + polarization (variation) +
  immune-style PRE-mint selection (not blind clonal minting — contradicts
  anti-chaos) + stem-cell bank as recruitment layer (census prerequisite).
- **Anti-chaos preconditions before minting gap-engines:** 2:1 fleet cap,
  burn-down tracker, kill-criteria enforcement cron.
- **B2C exit gate (5 booleans):** zero empty coverage-matrix cells; 3 clean
  independently-graded passes; 100% engines meet a–f standard; full
  CURRENCY cycle; ≥1 proven kill.

## Hard-won process lessons (each bit a principal correction)

1. **Micro-task sizing law:** a dispatch that times out = task too large.
   Decompose at mint: one deliverable, 1–2h, machine-checkable DONE, no
   "and-and" criteria. Applied at mint, not after failure.
2. **Chain-resolvability law:** depends_on must carry canonical task IDs
   (not M-labels); programmatic re-audit for zero dangling + acyclic BEFORE
   handoff. Caught a real defect the principal's distrust surfaced.
3. **BUILT vs THEORETICAL honesty:** never claim fleet status from
   narrative; machine-generated reality report (qa-fleet-reality generator,
   QA8-M5; PROVENANCE engine generalizes it). "Opencode said it's done" →
   verify on disk (ledger states, curl the health port, grep the registry)
   BEFORE reporting; found a criterion-gap + ECS drift this way.
4. **Conventions pre-inlined in retries:** after a panel dies to the llm-vendor
   90s timeout, re-dispatch with schemas/formats inlined so seats burn zero
   iterations on file research, and per-seat disk writes so progress
   survives mid-panel death.
5. **Conflict-of-interest disclosure in panels:** when the current lead
   (Deming) designs her own governance, the critic seat gets an explicit
   self-serving-bias flag mandate.
6. **Composite rulings beat winner-take-all:** isomorphism adjudications
   (glia vs stem vs immune vs liver) landed as layers (org / recruitment /
   selection), each seat arguing its candidate at full strength first.

## Mint hygiene (task-ledger, your-stack)

- `mint()` collisions: same-day prefixes reuse — compute max numeric suffix
  live, never assume.
- INSERT needs explicit created_at (NOT NULL) and severity 1–4 (CHECK).
- After minting any chain: resolvability re-audit + bus handoff to sibling-agent
  with build order + preconditions in the same script.
