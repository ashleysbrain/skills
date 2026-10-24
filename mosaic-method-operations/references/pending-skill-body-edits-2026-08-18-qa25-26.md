# PENDING SKILL BODY EDITS — QA passes 25-26 (2026-08-18)

Status: blocked by background _read_before_write guard (dedup skill_view
does not satisfy it). Apply these exact patches in a foreground curator
session, then delete this file. Pattern follows existing pending files.

## PATCH 1 — SKILL.md step 4 (iteration protocol): verification teeth

REPLACE:
```
4. **VERIFY live**: gate selftests AND a real run of the changed
   surface. Code-read-only verification does not count.
```
WITH:
```
4. **VERIFY live**: gate selftests AND a real run of the changed
   surface. Code-read-only verification does not count. Regression
   tests must be MUTATION-PROVEN (revert the fix -> test fails on
   exactly that defect -> restore -> pass), and coverage checks must
   verify AGREEMENT with the source of truth, not mere field presence
   — a presence check passed while 5/12 surfaces carried fabricated
   dims contradicting census evidence (passes 24-26, MR10A F2).
```

## PATCH 2 — SKILL.md "CI discipline (macos runner)" section: outdated

REPLACE the whole section:
```
## CI discipline (macos runner)
Gate battery + store-manifest integrity + surgical chain-ok on every
push. Concurrency tests MUST be deterministic (serial exclusion proof),
and close every sqlite connection before interpreter exit — four CI
runs died to segfaults before this rule existed. Full hunt:
references/ci-deterministic-testing.md.
```
WITH:
```
## CI discipline (ubuntu runner, python 3.12 — moved off macos 2026-08-18)
Battery loops `gates/*.py` AND `tools/*.py` through --selftest; the
selftest contract therefore binds BOTH directories — any new file in
either must implement --selftest isolated from production stores, or
the battery reds (ledger_whois shipped without one and killed run
32178080076; the red landed on an unrelated docs commit atop the
3-commit batch, masking the culprit). Workflow paths filter includes
gates/**, tools/**, stores/**, adapters/**, CONTRACT.md,
mosaic.manifest.json, ORGANS.json, ci.yml — audit/** docs do NOT
trigger CI, so green-run citations must come from code commits.
teardown-segtest classifier: rc>=128 with "SELFTEST PASS" in output =
runner teardown noise, counted PASS. Concurrency tests MUST be
deterministic; close sqlite connections before exit. Full hunt:
references/ci-deterministic-testing.md; battery history:
references/qa-passes-25-26-2026-08-18.md.
```

## PATCH 3 — references/package-map.md CI section: same staleness

In package-map.md REPLACE:
```
## CI (macos-latest, python 3.12)
```
WITH:
```
## CI (ubuntu-latest, python 3.12 — moved 2026-08-18)
```
and after the `- Surgical chain-ok step runs on every push.` line ADD:
```
- Battery covers gates/*.py AND tools/*.py (selftest contract binds
  both dirs since T-0156); teardown-segfault classifier counts
  rc>=128 + "SELFTEST PASS" as PASS.
- Stores ledger DB (stores/task-ledger.db) is .gitignored — local
  state only; never `git add -f` it.
```

## PATCH 4 — SKILL.md References list: add pointer line

AFTER the ci-deterministic-testing.md line ADD:
```
- `references/qa-passes-25-26-2026-08-18.md` — QA pass 25/26 methods:
  mutation-proven teeth, agreement-not-presence checks, batch-red
  masking, corruption-recovery protocol, sibling exchange pattern.
```
