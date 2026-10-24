# B2C-firstborn architecture review — 2026-08-21 session record

First B2C organism birth (b2c-firstborn), principal directive: special/unlocked child
straddling the operator agent-Live (lineage/updates) + GG3 (trusted personal domain), personal
data local/GG3-side behind hard firewalls, corruption-proof parent updates via
the specialist engine fungal routing. Session = architectural review BEFORE birth.

## Verified live state (gap ledger F1-F12)

- F1 update_distributor.verify_manifest trusts in-manifest pubkey (self-signing
  flaw: swap payload+key+sig together, verification passes). SEV-1.
- F2 No applier exists — staged/rollback semantics defined but nothing
  executes them. SEV-1.
- F3 consent.py referenced in docstring only — missing on disk. SEV-1.
- F4 GG3 updates via unsigned git pull + live-mounted volume + restart. SEV-1.
- F5 Tier isolation/firewall_rules = declarative dicts, zero enforcement. SEV-1.
- F6 the operator agent-Live fleet mostly DOWN on host (only :port/:port). Fact.
- F7 Simard consent API drops granularity: requested narrow 1h grant ->
  stored all 5 categories, expires never, scope forced anonymized (live probe).
  SEV-2 -> organism-side consent gate is the real boundary.
- F8 Molecule vocab = carbon/nitrogen/phosphorus/defense/hormone (no
  update_manifest type; tech cargo rides phosphorus by convention); client
  copies diverge from live :port API field names. SEV-2.
- F9 GG3 federation client points at dead :port. SEV-3.
- F10 Stale qa-src/qa-tgt nodes skew percolation. SEV-4.
- F11 Percolation p=0.1786 vs p_c=0.1667 — margin 0.012; adding the child
  raises coordination number; prune + re-probe is a birth gate. SEV-2.
- F12 No organism has ever been born through the canal (verify = engine
  reachability ALL_GREEN, not a completed birth). First-of-kind.

## Panel run (deleg_51ee79f3)

6 seats sequential in ONE child (Tanenbaum/Simard/Medawar/Popper/nature-analogs
+ same-family critic with kill mandate). Verdicts: conditional x4, Popper
FAILS-AS-DRAFTED-salvageable, critic UPHELD with 2 corrections (A: runtime
form before enforcement mechanism; B: quorum needs time-bounded single-parent
fallback or dead gg-live wedges the child). Popper kill shot: "the cryptography
protects a pipeline that terminates in nothing." Brain-gate false-failed
(PhD=0 in transcript render; spec verbatim in dispatch echo) -> manual PASS
banked per documented gate-matcher false-fail rule.

11 binding spec deltas + the 10 laws live in SKILL.md. Full verdict text:
`/<workspace>`; consolidated
doc: `ARCHITECTURE-REVIEW-v1.md` (sections 1-6).

## Task ledger (genome-gated, lane=gg)

T-260821-0167 nature-analogs gap scan / 0168 firewall organ / 0169 OTA channel
(pinned keys + applier) / 0170 consent surface / 0171 Simard registration /
0172 birth execution / 0173 SAR ledger / 0174 quorum commit + fallback / 0175
key lifecycle / 0176 red-team birth battery. Builds leased to sibling-agent
(bus 2918/2919); panel deltas propagated mid-lease (bus 2922, 2209 chars).

## Acceptance battery

`/<workspace>` — 19 checks, executed
pre-build: 1 GREEN (no PERSONA data pre-birth) / 18 RED (impl absent = honest
baseline). Attack-first checks: U1 substitutes attacker key+payload+sig and
requires rejection; Z2/Z3 attempt raw PERSONA exports; U2 downgrade; U4
cross-issuer file touch. Battery IS the birth gate (T-0176 extends it to run
against the LAUNCHED child — 5 attack classes must fail observably).

## Reusable session patterns

- Architecture review BEFORE birth caught 12 defects pre-build; cost ~3h.
- File-pointer brief (6KB) + no-re-probe instruction kept the panel child fast.
- Mid-lease delta propagation: when a panel materially changes a leased build,
  send the deltas to the builder IMMEDIATELY (bus), not at lease expiry.
- Keep building your own lane during a lease (battery) — the no-idle law.
- Port block census before claiming availability; child took 8600-block.
