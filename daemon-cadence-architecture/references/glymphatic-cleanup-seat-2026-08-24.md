# Glymphatic Cleanup Seat — the specialist engine build (2026-08-24)

principal directive: elite cleanup specialist that goes behind other agents' work,
quarantines debris, and routes cleanup logs to the producing engines/teams
for process improvement + self-correction. Fewest crons; clean data
structures and file organization.

## The pattern (reusable for any cleanup/hygiene seat)

**Physics framing that drove the design:** debris follows `W'(t) = P − K·W`.
Under-clearance (K) is fixed by sweeping; overproduction (P) is fixed by
routing manifests back to the producer. A cleanup log that nobody receives
is waste relocation, not cleanup.

1. **Name from the 4-category convention:** the specialist engine (glymphatic
   system, Iliff 2012). Distinct from the specialist engine (lymphatic pruning /
   forgetting) — interstitial clearance vs structural pruning. Always run
   the name-collision grep first (`rg -l "DS <Name>"`).
2. **Mint seat additively:** ORGANS.json entry (kind=seat, flow=FLW-QA-FLEET)
   via an idempotent mint script mirroring `scripts/mint_qa_fleet.py`;
   ledger task lane=immune. Note: ledger stage `minted` warns off-vocabulary
   (accepted legacy); canonical stages are sense/appraise/mint/dispatch/
   verify/learn.
3. **Detectors as functions** in one sweep module, each returning debris
   dicts with `class/path/evidence/producer`. Detector failure is logged,
   never crashes the sweep. Classes that caught real debris on day one:
   - `jobs.json.bak-*` stacking (keep newest 5, quarantine the tail; age-gate
     3d so an in-flight backup is never touched)
   - decoy DBs (0-byte or no `sqlite_master` schema; live set is an
     explicit WHITELIST of proven-canonical paths — never infer by name)
   - 0-byte cold logs, tmp-/probe scripts unreferenced by RUN-RECORD.md
4. **Reversible quarantine ONLY:** move into
   `quarantine/glymphatic/<date>/<class>/`, append to `MANIFEST.jsonl` with
   original path, evidence, and a literal `restore` command per entry.
   Deletion requires 30d age + zero restores.
5. **Quiescence gate:** `lsof -nP <file>` before any move; live-held files
   are reported + blocked, never moved.
6. **Route manifests by producer** via the LIVE operator bus
   (`/<workspace>`; `<agent-home>` copies are
   stale) — typed msg_type `cleanup_log`, one message per producer group.
7. **Compose into the daemon, never a cron:** add a `*_pass()` function to
   `organism/autonomous_iteration.py` calling the sweep via `_cmd`, join its
   result dict into the pass log. rc 0 = clean, 1 = findings (healthy for a
   scanner), 2 = broke (defect).

## Verification recipe (all executed, all passed)

```
python3 -m py_compile glymphatic_sweep.py autonomous_iteration.py
python3 glymphatic_sweep.py --dry-run      # count before touching
python3 glymphatic_sweep.py                # sweep; rc=1 expected on findings
python3 glymphatic_sweep.py --status       # all classes must read 0 after
sqlite3 <live-bus> 'SELECT id FROM messages ORDER BY id DESC LIMIT 3'
# reversibility proof: mv one item back out of quarantine -> re-run sweep
# -> it is re-detected and re-quarantined
# daemon kill-test: kill <pid>, sleep 12, launchctl list shows NEW pid
```

First live sweep: 19 items (13 cron baks, 3 decoy DBs, 3 tmp scripts),
3 bus manifests posted, post-sweep vitals all zero, restore+re-detect
proven, daemon relaunched under launchd KeepAlive (73941 -> 90789).

## Pitfalls found during the build

- **Pyright caught `vit` vs `vitals`** typo that py_compile missed — keep
  LSP diagnostics on for new sweep modules.
- **`grep -ril` across `<agent-home>` for name-collision checks times out**
  (300s) — the home dir is too big for unanchored recursive greps. Use
  `rg -l --glob '!*.log'` on targeted trees instead.
- **The whitelist must be taught new canonical DBs as they are born** —
  an enumerated live-set ages badly; treat whitelist updates as part of the
  process-improvement loop, not a one-time config.

## Files created (canonical locations)

- `your-stack/scripts/mint_nedergaard.py` (idempotent mint)
- `your-stack/methodology/DS-NEDERGAARD-METHODOLOGY.md` (rate-equation
  physics, 6 standing laws, verification hooks)
- `organism/glymphatic_sweep.py` (detectors + clearance + routing)
- `organism/quarantine/glymphatic/MANIFEST.jsonl` (append-only ledger)
- Daemon wiring: `glymphatic_pass()` in `organism/autonomous_iteration.py`
