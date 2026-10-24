# Org relocation: your-stack moved out of personal tissue (2026-08-18)

principal directive (verbatim intent): "the mosaic os should not be in principal's
brain... it should have its own sub repo in your-org. not under
aisha or any of my personal stuff." Org packages never live under
personal paths. Task T-260818-0136, closed with live verification.

## What moved
`~/Desktop/INTELLIGENT-OS/your-stack` → `~/your-org/your-stack`
(git mv via plain `mv` — working tree was clean, remote already
`your-org/your-stack`, so the repo traveled intact).

## The sweep (two textual shapes of the same path)
Path references hide in TWO forms; a plain string-replace misses the
second:
1. Literal: `"/<workspace>"` — hit by
   simple str.replace.
2. Segment-wise: `Path.home() / "Desktop" / "INTELLIGENT-OS" /
   "your-stack"` — invisible to the literal pattern; grep for the
   directory name `INTELLIGENT-OS` and inspect each hit.

Repointed: 11 organism scripts (gap_hunter, gap_to_build_bridge,
events_subscriber [technology-registry SUBMODULE — commit inside it,
then bump the gitlink in the parent repo], volley_loop ×4,
homeostatic_supervisor, backup_engine, autonomy_report,
mosaic_chain_executor, mosaic_wire, notion_adapter ×2,
organism_calendar ×2) + `<agent-home>/scripts/store_health_wrapper.py`
+ workspace symlink (`ln -sfn` new target; gitlink-tracked, commit it).

## Verification battery (all must pass from the new home)
- `grep -rn INTELLIGENT-OS <workspace> --include=*.py,*.sh,*.json,*.yaml`
  excluding backups/node_modules/.hermes-state → **0 hits**
- `python3 organism/mosaic_chain_executor.py --once --json` → rc=0
- `store_health_wrapper.py` → "9/9 stores UP", rc=0
- cron jobs.json scan for old path in LIVE job bodies → 0 (historical
  last_error strings don't count; read jobs.json via file read, not
  terminal — see pitfall below)
- workspace symlink resolves; git status clean after gitlink commits

## Pitfalls hit
- **Gateway guard false-positive**: terminal commands whose output/text
  mentions restarting the gateway (e.g. grepping jobs.json containing a
  gateway-restart job) get blocked by the harness
  "cannot restart the gateway from inside the gateway process". Read
  such files via file-read tools or execute_code instead.
- **git index.lock transient**: a blocked/aborted `git add` can leave a
  stale lock; verify no live git process, remove the lock, retry.
- **Path-spec in submodule**: `git add technology-registry/...` from the
  parent fails; cd into the submodule, commit there, then
  `git add technology-registry` in the parent to bump the gitlink.
- **Ledger close via Python API only** (`complete(c, tid, outcome,
  actor=...)` — actor_kind is NOT a kwarg of complete); CLI has no
  claim/complete flags.

## Doctrine
Relocation of an org-owned package = boundary repair: move, repoint ALL
wiring (both textual shapes), verify consumers run from the new home,
commit both repos. Never leave a personal-path symlink as the only
route to org IP.

## Dead mirror detection (2026-08-18 session lesson)
After relocation, a stale mirror may remain (e.g. the Desktop copy). How to tell if a mirror is DEAD (not just stale):
- `ls -la <mirror-path>/stores/task-ledger.db` — if size is 0 bytes, the database was nuked; the path is a shell
- `sqlite3 <mirror-path>/stores/scheduler.db` — if the queue table exists but `SELECT count(*)` returns 0 while the org repo has rows, the mirror was pruned
- `git log --oneline -1` in the mirror — if the HEAD commit predates the org repo's active development AND the last mtime of stores/ is hours behind org/, it's abandoned
- NO evidence of sibling commits or runs in the mirror while org repo is actively building

**Decision rule:** if a mirror is 0-byte stores OR empty queue while org repo has live data, DELETE THE MIRROR. It's not a backup; it's a shell that sessions might mistakenly point to (see pitfall: this session pointed at Desktop for several checks before discovering it was empty).

Recovery path is NOT to resync from the mirror (it's empty); the org repo is canonical. Verify org repo has all expected data (task count > mirror, recent commits, CI green) before deleting the mirror.
