# macOS Data-Surface Census (commands + classification traps, 2026-08-17)

Companion to the git scrub runbook: the non-git leak surfaces on this host.
Run every surface; classify before touching; some "health" paths are products.

## Spotlight indexes file CONTENT

```bash
mdfind -count "kMDItemTextContent == '*Vyvanse*'"   # 665 files indexed
```
Fix needs sudo (System Settings > Siri & Spotlight > Search Privacy, drag
`health-private` + `vaults-prep` in). Agent cannot sudo non-interactively —
report it as an explicit principal manual step; never claim it done.

## Obsidian vaults symlink into iCloud

`~/Documents/Obsidian Vault` is a symlink into
`~/Library/Mobile Documents/com~apple~CloudDocs/Obsidian Vault`.

Traps hit during the census:
- `os.walk()` does NOT follow a symlinked root — a walk of the Documents path
  scanned 0 files twice before `os.path.realpath()` was used. Always
  realpath the vault root first.
- iCloud-evicted (dataless) files fail `open()`/`head` until materialized:
  `brctl download "<file>"` pulls the content back for inspection.
- `brctl status` shows the actual sync containers and whether sync is
  disabled (one container showed `>>> SYNC DISABLED (app not installed)`).
- Classify content before reacting: this vault's health-named folders
  (02-8D360, 04-Qubit-Health) held product docs (PRDs, spec stubs), zero
  personal health data. The iCloud-synced ARCHITECTURE is the risk note, not
  the current contents.

## FileVault (at-rest floor)

```bash
fdesetup status    # FileVault is On — baseline disk encryption present
```

## Time Machine local snapshots (pre-scrub .git can persist)

```bash
tmutil listlocalsnapshots /    # none present on 2026-08-17, but check every time
```

## Live writers + SQLite sidecars

- `lsof <db-path>` before migrating any DB (catches an active writer).
- `-wal` / `-shm` siblings mean a SQLite writer was recently active
  (health-private DB had fresh 08:05 wal/shm that morning).
- A writer cron must be repointed BEFORE migration (the 8D360 HealthKit
  daily pull was scheduled to repoint to the vault ingest dir).

## False-positive classification (before declaring PHI)

- `8D360-Human/` — public open-source product (LICENSE/README/SETUP docs),
  NOT personal data despite the name.
- `.hermes-state/health-check-*.json` — engine telemetry (ports, statuses),
  not PHI.
- Scan result must be content-based (regex for meds/conditions in file
  bodies), not name-based, or these swamp the real surface.

## Architecture rule (from the principal vault question)

A personal-data vault never lives inside (a) a shared git-tracked agent
workspace or (b) an iCloud-synced container. It lives outside both, dir
0700 / files 0600, with the QA-organ phi-surface sensor watching for drift
(genome v4+, hourly).
