# PENDING SKILL.md BODY EDITS (blocked by bg _read_before_write guard)

Apply in a FOREGROUND session (or via curator) — the background
curator's dedup skill_view does not count as the read the guard wants,
and patching SKILL.md from background keeps refusing with
"current SKILL.md content has not been loaded in this review turn".

## Edit 1 — CI discipline section (replace whole section)

OLD:
```
## CI discipline (macos runner)
Gate battery + store-manifest integrity + surgical chain-ok on every
push. Concurrency tests MUST be deterministic (serial exclusion proof),
and close every sqlite connection before interpreter exit — four CI
runs died to segfaults before this rule existed. Full hunt:
references/ci-deterministic-testing.md.
```

NEW:
```
## CI discipline (ubuntu runner)
Gate battery + store-manifest integrity + surgical chain-ok on every
push. Concurrency tests MUST be deterministic (serial exclusion proof),
and close every sqlite connection before interpreter exit — four CI
runs died to segfaults before this rule existed. Full hunt:
references/ci-deterministic-testing.md.

- Runner is ubuntu-latest (macOS sqlite segfault class).
- CI paths filter must cover: gates/**, stores/**, adapters/**,
  CONTRACT.md, mosaic.manifest.json, ORGANS.json (QA-21 D3: contract
  surface ran ZERO CI until extended — 5 commits, no runs).
- Selftest isolation is load-bearing: pin the DB INSIDE the --selftest
  branch ONLY; wrapping __main__ clobbers the CLI path (QA-22: MCP tool
  returned SELFTEST output). Prove: before/after prod row delta = 0.
- Selftests writing fixtures into prod stores poison them run by run
  (QA-10 D2 recurred QA-22: 85 of 93 dispatch rows were fixtures).
- Surgical edits to CONTRACT/manifest/harness-registry/adapters run a
  post-flight contract-sync check; violations REFUSE and atomically
  RESTORE the original — a refused edit must never stay on disk (QA-22:
  refused v9.9.9 title got committed; CI 32169758442 caught it).
- Zero-byte DB twins under ledger/ are migration residue; verify no
  writer, then delete.
```

## Edit 2 — References section (append one line)

OLD:
```
- `references/ci-deterministic-testing.md` — the 4-run segfault
  root-cause hunt + the deterministic exclusion-test pattern.
```

NEW (append after it):
```
- `references/qa-pass-21-22-2026-08-18.md` — architectural audit method
  (self-location census, attribution audit, CI coverage matrix) + the
  refuse-restores-disk and selftest-isolation patterns.
```

Note: references/pending-skill-body-edits-2026-08-18.md already exists
from pass 20 with the same workaround pattern.
