# Freeze-lease actor identity — surgical gate pitfall (2026-08-18)

## Symptom
Every `g.apply()` in a run refused, anchors verified present:
`apply False — self-override guard: lease held by hermes-mr13-freeze`
while the operator applying WAS hermes.

## Cause
Lease actor strings are exact-match. A freeze lease claimed as
"hermes-mr13-freeze" (per-pass tag) blocks applies by actor "hermes":
the self-override guard treats different strings as different actors
even when the same operator holds both.

## Pattern (verified working MR13)
- QA freeze: `g.claim(path, "hermes-<pass>-freeze")` for panel isolation.
- Same-session remediation after the panel files:
  `g.release(path, "hermes-<pass>-freeze")` FIRST, then
  `g.apply(path, old, new, actor="hermes")`. Or hold ONE actor string
  (the tagged one) for claim/apply/release across the whole pass.
- Before re-reading anchors on a uniform refusal run, check actor-string
  mismatch (refused_because names the holder).

## Related
- QA-pass freeze law L10 lives in CONTRACT.md; leases TTL 300s,
  `surgical_gate --leases` surfaces active freezes, expired rows purge
  on scan (MR12).
- Distinct from the freeze discipline itself (L10): this is the actor-
  string identity trap inside it.
