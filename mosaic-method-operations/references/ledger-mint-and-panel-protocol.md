# Ledger mint/claim quick-ref + fresh-brain panel protocol (verified live 2026-08-19)

## Exact taxonomy vocabulary (task-taxonomy.json is DATA; unknown value = ValueError)

- lanes (12): scheduler, registry, interop, stores, bus, deck, report, gg, fleet,
  security, legal, connectivity. There is NO 'ui'/'research' lane — UI/product work
  goes under `deck`.
- kinds (8): build, defect, gap, verify, probe, decision, question, maintenance.
- origin must be a registered PREFIX (audit, event, ceo, bus, deck, cron), not free
  text — `--origin "principal-direct-2026-08-19"` is rejected; `--origin ceo` passes.

## Minting (CLI works for submit)

```bash
cd ~/your-org/your-stack
python3 gates/task_ledger.py --submit --title "<title>" --kind verify \
  --lane deck --origin ceo --by hermes --actor-class ai
# -> prints minted id T-YYMMDD-NNNN
```

## Claiming (CLI has NO --claim flag — use the module API)

```python
import sys; sys.path.insert(0, "<MM>/gates")
import task_ledger as tl
c = tl.connect()
tl.claim(c, "the specialist engine", "ai", task_id="T-260819-0026")
```
MIND THE ARGUMENT ORDER: (conn, actor, actor_kind, task_id=...) — reversing actor and
actor_kind raises "actor_kind must be 'ai' or 'human'". Claim before any work;
`complete()` refuses rows not in state='claimed'.

## Fresh-brain adversarial panel protocol (for "unlike any that have reviewed
this work so far" requests)

1. **Census prior reviewers first** — grep all audit/*.md for `\bDS [A-Z][a-z]+`,
   count occurrences, exclude every name already used (e.g. 25 prior names on the
   Research Studio). Select genuinely new lenses (e.g. the specialist engine/HC-heuristics,
   the specialist engine/information design, the specialist engine/team design — none prior).
2. **Mechanical digest BEFORE any brain argues** (the OS law 7): run the census
   battery, cross-reference routes, verify each anomaly with a corrected probe —
   reviewers then start from verified facts, not impressions. Write the digest to
   audit/rs-digest-<date>.md and hand ONLY that to reviewers.
3. **Withhold prior audit files** in every dispatch context ("do NOT read prior
   audit/*.md except <the new digest>") — independence is the point of fresh brains.
4. **One ledger task per reviewer + one synthesis task**; claim each with the
   reviewer's name as actor.
5. **Exclusive resource lanes per reviewer** (parallel-safe): reviewer A owns the
   chrome CDP port; reviewer B static-source only; reviewer C terminal/API only.
   State the lane explicitly in each context. Without it, interleaved probes on one
   browser profile produce phantom defects.
6. **Market/competitive scan runs as a separate background specialist** alongside
   the panel (goal: direct competitors + adjacent-sphere process flows + top-10
   steals + white space), so consolidation has external evidence too.

## Reusable artifacts from the 2026-08-19 run

- Census battery script + probe-trap reference: skill `headless-ui-qa-batteries`
  (`scripts/cdp-census-battery.cjs`, `references/cdp-census-battery.md`).
- Digests live in the product repo's audit/ dir (rs-digest, rs-census,
  rs-truly-orphan-routes JSON) — cite them, don't re-derive.
