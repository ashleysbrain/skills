---
name: b2c-organism-spinup
description: Use when birthing a consumer (B2C) organism from a parent.
---

# B2C Organism Spin-Up (consumer organisms carrying personal data)

Use when spinning up a consumer (B2C) organism: single trusted user, personal
data stays local/trusted-domain, parent organisms push updates without
corrupting data. First instance: b2c-firstborn (2026-08-21, the operator agent-Live x GG3
dual parentage, "special/unlocked" child with sister-sandbox access).

## When to use

- Birthing any consumer-facing organism from a parent (the operator agent-Live and sisters)
- Designing personal-data residency firewalls (local-first, parent-gated)
- Corruption-proof OTA update channels from parent organisms
- Fungal (the specialist engine :port) node registration and percolation gating
- B2C birth gating / red-team acceptance batteries

## How B2C differs from B2B (see `b2b-organism-spinup`)

| | B2B | B2C |
|---|---|---|
| Tenancy | N orgs, tenant isolation | 1 trusted user |
| Compliance | external regimes (GDPR/HIPAA/SOC2) | implicit posture + permanent-exposure class |
| Data hazard | customer Tier-3 data | PERSONA data — first unclassified record = permanent exposure |

Shared hard law: NEVER let personal data flow before firewall + consent gates
are live CODE. Config dicts and docstrings do not count.

## The 3-zone data-residency model (placental law)

- **PERSONA** — all personal data. Never leaves the child. No parent path
  touches it.
- **TRUST** (e.g. GG3-TRUST) — data may flow child<->trusted domain under
  molecule-typed consent grants.
- **PUBLIC** — what the lineage parent (the operator agent-Live) may see: explicitly
  authorized, gated aggregates ONLY.

Two circulations never mix. Transport is selective and receptor-mediated
(placental IgG analog), never passive diffusion.

## Binding architecture laws (6-seat panel, critic-upheld, 2026-08-21)

1. **Firewall organ is a PROCESS, not a library call.** Decide the child's
   runtime form FIRST, then the enforcement (Critic correction A). Any
   updated code with socket access routes around a function-call gate:
   child gets no default route; the only egress is the firewall-organ
   proxy, allowlisting the fungal hub + pinned parent endpoints.
2. **Zone-tagged write buffers.** Logs/prompts/telemetry are zone-tagged at
   WRITE time; PERSONA bytes physically cannot enter a PUBLIC buffer.
   Transport inspection alone cannot catch prompt-borne exfiltration.
3. **Payload-class enum, deny-by-default.** Five classes: persona-aggregate,
   persona-raw-to-trust, telemetry beacons, consent traffic, solicitation.
   Anything else: refused, logged, surfaced.
4. **OTA trust anchors.** Per-issuer keys PINNED at install (manifest pubkey
   field is advisory — fixes the self-signing flaw where attacker swaps
   payload+key+sig together). Global file-ownership map: every file owned by
   exactly ONE issuer; cross-issuer touch = invalid manifest. Atomic commit
   only after boot-time postcheck; rollback retry cap 2 then SAFE-mode halt
   (running slot, no updates, human alert); monotonic anti-downgrade counters
   per issuer; dual-key rotation with overlap; offline revocation list
   shipped inside the next counter-signed manifest.
5. **Consent keyed (issuer, data_type) — never issuer alone** (a parent can
   send both update and personal molecules). Short renewals, never standing
   grants. Revocation total + immediate at the chokepoint; residual exposure
   (absorbed molecules, published aggregates) recorded and human-notified.
6. **Fungal transport.** Pull-only (point-to-point push is banned); child
   verifies BEFORE absorbing; issuer claim is channel-bound (pairwise keys
   minted at seed-entry — kin-recognition analog); fresh percolation probe
   AFTER pruning stale nodes at seed-entry is a BIRTH GATE; child emits
   hunger/solicitation signals to pull.
7. **Graft-vs-host audit.** A signed update is parent CODE executing in
   child context. For N hours post-apply, diff child egress against the
   consent ledger; violation = auto-rollback + manifest-lineage quarantine.
8. **SAR ledger (acquired immunity).** Quarantined lineages recorded; the
   chokepoint holds them under heightened verification (full audit, human
   confirmation on first re-entry); broadcast to sister sandboxes as a SAR
   molecule class so they inherit the priming.
9. **Quorum commit for shared surfaces** (constitution, config schema,
   firewall allowlist): BOTH parents' channel-signed concurrence within a
   window — WITH a time-bounded single-parent fallback + SAR entry + human
   notification (Critic correction B: a dead parent must not wedge the
   child; bacterial quorums have many senders, dual parentage has two).
10. **Birth gate = red-team battery against the LAUNCHED child:** direct
    egress to parent endpoint, PERSONA bytes in telemetry, swapped-key
    manifest, downgrade, unsigned git-pull-style push. Each attack must
    FAIL observably or NO BIRTH.

## Birth process (adiabatic, dependency-ordered)

P1 trust anchors -> P2 applier with A/B + rollback -> P3 consent organ ->
P4 firewall chokepoint (code-enforced) -> P5 fungal registration +
percolation probe -> P6 canal birth (blueprint -> genome injection with
GENOME block -> sandbox compile -> APGAR >= 7 -> seed-entry /simard/connect)
-> P7 first gated update cycle proven end-to-end.

Verify the canal BEFORE planning: `reproductive_flows.py --verify` must
return ALL_GREEN (13 engines). No personal data before P3+P4 are live.

## Acceptance battery pattern (TDD for organisms)

- Implementation-independent checks defined against INVARIANTS, not modules;
  point them at the planned impl paths and they auto-tighten when builds land.
- Attack-first: each check ATTEMPTS the exploit and requires observable
  refusal (attacker key substitution, raw PERSONA export, downgrade,
  cross-issuer file touch).
- Oracle law: a check passes ONLY on positive evidence; absence of evidence
  = RED, never skip.
- Run pre-build for the honest RED baseline; leased builds turn it GREEN;
  the battery IS the birth gate (APGAR reachability != security).
- Starter: `templates/acceptance-battery.py`.

## Process discipline that worked (2026-08-21)

Architectural review BEFORE birth: live-probe gap ledger -> file-pointer
brief -> 6-seat sequential panel (systems/security, fungal network, consent,
falsifier, nature-analogs, cross-model critic) -> fold verdicts into the SAME
doc -> mint deltas as genome-gated ledger tasks -> lease builds to sibling-agent
via the bus (6h lease, deltas propagated mid-lease) -> keep building YOUR
lane (the battery) while leased. Label every claim BUILT (live-verified) /
THEORETICAL / GAP.

## Pitfalls

- **MICRO-TASK SIZING LAW (principal 2026-08-24)**: any dispatch that times out or hits iteration caps = the task was too large. Decompose at mint-time: one deliverable per task, 1-2h scope, machine-checkable DONE criterion (curl probe / pytest / live run / battery row), explicit depends_on chain. Mint-time test: if the DONE criterion needs "and" twice, split it.
- **CHAIN RESOLVABILITY LAW (2026-08-24, caught in self-audit)**: depends_on MUST hold canonical task IDs, never human labels ("M3"); a chain is not done until a programmatic re-read shows zero dangling refs and an acyclic graph. Run the check before handoff, every time.
- **Lease supervision is mechanical, not trust** (panel 2026-08-23): every build lease needs expiry auto-escalation (outcome row + human notify + re-pool, checked <=30min) and mid-lease checkpoint acks. Prior failure: 6 leases -> 0 builds, stall detected only by principal visit 48h later. QA the re-lease BEFORE firing it (amend-order rule: panel precedes executive action).
- Declarative firewall dicts are dead on arrival — zero enforcement. Code or it doesn't exist.
  it doesn't exist.
- The cheapest attack path wins: if any parent still updates via unsigned
  `git pull` + restart, the signed channel is theater. Close or firewall the
  cheap path FIRST.
- Fungal-layer consent can be coarse (live probe: requested narrow grant ->
  stored all categories, never expires). The organism-side consent gate is
  the REAL boundary; treat network-layer grants as transport hints only.
- Molecule vocabulary is biology-typed (carbon/nitrogen/phosphorus/defense/
  hormone); tech cargo rides phosphorus by convention. Verify against the
  LIVE engine schema — client copies diverge (source/target vs
  source_organism/target_organism field names).
- Percolation margins are thin (p - p_c ~ 0.012 measured once); adding nodes
  raises coordination number. Prune stale nodes, then re-probe at every
  topology change.
- A mostly-down parent fleet (the operator agent-Live on host) means the child treats parents
  as lineage/update ancestry, not live boot dependencies.

## References

- `references/b2c-firstborn-architecture-review-2026-08-21.md` — full gap
  ledger (F1-F12), 6-seat panel verdicts, 11 binding deltas, task IDs
  (T-260821-0167..0176), bus exchange IDs, battery run history.
- `references/model-lane-selection-lessons-2026-10-05.md` — binding rules
  for B2C classification-organ model lanes (T-261005-0071, principal-tagged):
  evaluation grades the business taxonomy (exact-match), never JSON
  validity; closed-label decoding; SLM privacy/cost envelope.

## Related skills

- `b2b-organism-spinup` — the B2B counterpart (8-gate pipeline, 11 systems)
- `your-stack-operations` — ledger mint/claim/verify discipline
- `organism-deployment` — Docker port isolation
- `elite-panel-chain-of-custody` — the panel pattern used for review
