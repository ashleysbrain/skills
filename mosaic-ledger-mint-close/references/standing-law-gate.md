# Standing-law gate: SL checks + build-row verdicts

Depth for the standing-law gate that enforces principal always/never orders at the
ledger write path. Governing skill: `operations/ceo-standing-law-enforcement`.

## Gate module

`/<workspace>`, wired fail-closed
into gap_cycle's mint path (check runs BEFORE tl.submit; a violation records
a reject and skips the row). Usable standalone by any operator before minting.

```
python3 organism/standing_law_gate.py --selftest
python3 organism/standing_law_gate.py --check-build '<json: title, detail, origin, kind>'
```

Exit 0 = pass, exit 3 = violation (JSON verdict names the law ids).

## Law registry (SLn)

| Law | principal order | Test on a kind=build row |
|-----|-----------|--------------------------|
| SL1 | research lineage required | origin/detail references the research corpus (gap-cycle/gap_hunter origin, or an `sr-<hash10>` token) WITHOUT a lineage token (`sr-...` or a registered topic id) -> REJECT |
| SL2 | all-systems dispatch required | no `ALL-SYSTEMS DISPATCH` scope note -> REJECT |
| SL3 | prior-science receipt required | no `prior-scan:` / `science-scan-covered` / explicit `no prior science exists` trail -> REJECT |

Add SLn rows here as new always/never orders arrive; each new check needs the
same falsification proof (a violating row rejected with the law id) before it
counts as enforcement.

## Known trap: false-positive lineage keys

SL1's regex accepts `sr-[0-9a-f]{10}` plus loose `[a-z0-9-]{3,40}` topic ids
prefixed st-/scan-/ceo-/referrals-. The `st-` prefix collides with VERITAS
stage strings (`st-closure`, `st-ingestion`) in ledger detail text — when
JOINING corpus to ledger by lineage, match against the actual scan_topics
vocabulary, not the substring (see references/research-corpus-lineage.md).
For gate purposes the looseness is safe (it only requires that SOME lineage
key be present); for measurement purposes it is not.

## Telemetry

Per-law rejection counts (SL1/SL2/SL3) go in the morning packet. Any principal
repeat-order triggers a retroactive gate-gap audit: count BUILD rows missing
a stamp that the corresponding law required, name the write path that lacked
the check, and close the gap the same turn.

## Behavioral rules for repeat-orders and same-turn shipping

- **A repeat-order is a retroactive audit trigger, not a defense moment.**
  When the principal re-issues an order already given ("I already asked you
  this"), the same-turn move is: measure WHERE the law decayed (count the
  rows missing the stamp, name the ungated write path), build the gate
  check, falsify it live against a violating row — never re-promise in
  prose. The reply carries the measured defect plus the working gate; the
  principal judges the fix by its mechanism, not its vow.
- **Same-turn means same-turn.** The law row, its gate check, the live
  falsification run, and the organic-producer wiring (templates that should
  pass ungated) all land in ONE turn; shipping the mint first and the gate
  later is the decay pattern the law exists to kill.
