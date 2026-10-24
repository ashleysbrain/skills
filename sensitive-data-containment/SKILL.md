---
name: sensitive-data-containment
description: Scrub PHI/secrets from git history and macOS surfaces.
version: 1.0.0
metadata:
  hermes:
    tags: [security, phi, git, scrub, privacy, vault, macos]
    category: devops
---

# Sensitive Data Containment

Class: finding, containing, and scrubbing private data (PHI, credentials,
personal records) that has leaked into git repos, cloud-synced folders, search
indexes, or world-readable paths on this macOS host — and building the vault
architecture that keeps it out. First executed end-to-end 2026-08-17 when 287
health files were discovered PUSHED to GitHub (not merely tracked locally) for
two months; full runbook grew out of that execution.

## When This Skill MUST Load

- Any task asking whether private/health/PHI data is safe, exposed, or leaking
- Untracking, scrubbing, or rewriting git history that touched private files
- Force-push coordination on a SHARED repo after a history rewrite (siblings'
  commits get rewritten — bus alert before, fetch+reset guidance after)
- Designing or migrating a personal data vault (location, perms, encryption)
- Auditing where sensitive files live before a B2C/health organism reads them
- Checking macOS leak surfaces: Spotlight index, iCloud containers, Obsidian
  vaults, Time Machine snapshots, world-readable permissions

## The core distinction: TRACKED vs PUSHED (measure before acting)

`git ls-files` (tracked) and local history tell you almost nothing about
exposure. What matters is what a CLONER can reach:

1. `git log origin/main --oneline -- <path> | wc -l` — commits touching the
   path that ARE on the remote (18 found 2026-08-17, oldest 2026-06-20)
2. `git rev-list --objects origin/<every-remote-branch> -- <path> | wc -l` —
   object count reachable from the remote ref (364)
3. Fresh-clone simulation — clone to a temp dir with `--no-local`, count PHI
   objects in the clone. This is the ground truth; nothing else substitutes.
4. `gh api repos/<org>/<repo> --jq '.private, .forks_count'` + collaborators —
   blast radius of what sat on the remote.

Untracking (`git rm --cached`) + .gitignore fixes ONLY the future. If objects
are reachable from any remote ref, a history rewrite is mandatory.

## Containment sequence (adiabatic, order matters)

1. CENSUS + CLASSIFY first: walk every candidate surface (see macOS census
   reference), classify false positives before touching anything (2026-08-17:
   `8D360-Human/` looked health-related but is the public open-source product;
   `.hermes-state/health-check*.json` is engine telemetry, not PHI).
2. FREEZE MANIFEST before any operation: SHA-256 per file + count-at-freeze
   written INSIDE the private dir. File counts drift (285→287 same morning);
   the manifest is the truth. Re-verify 0 mismatches after EVERY later step.
3. LOCK PERMS: dir 0700, files 0600 (`chmod`, then `find ! -perm` to verify).
4. SAFETY NET: `git bundle create <vault> --all` (full history incl. PHI) +
   stash patches → lock 0700/0600. This bundle is now the ONLY copy of old
   history — keep it OUT of git dirs, note it contains PHI deliberately.
5. UNTRACK: `git rm -r --cached <path>` + .gitignore entries (path + `vaults/`
   + backup patterns) + commit.
6. SCRUB: `git-filter-repo --invert-paths --path <path> --force` (gotchas
   below), then `git reflog expire --expire=now --all` + `git gc --prune=now`.
7. VERIFY LOCAL: rev-list 0 objects, commits/files counts intact vs pre-scrub,
   fresh-clone test 0 objects.
8. PUSH + VERIFY REMOTE: force-push per-branch, then re-fetch and run the
   object count against EVERY remote head — including remote-only branches
   that `--all` missed (anatomical-audit had no local branch and was skipped
   by `push --all`; it happened to be clean, but only the per-ref audit proved it).
9. BACKUP LOCKDOWN + residual surfaces: chmod the vault dir, handle Spotlight
   exclusion, re-run full QA battery a second time from scratch (multiple QA
   passes are the standard, not a bonus).

## Gotchas (each cost real time on 2026-08-17)

- **filter-repo "already ran" marker blocks re-runs**: a stale
  `.git/filter-repo/already_ran` from a PREVIOUS session's attempt makes the
  sanity check prompt `Treat this run as a continuation (Y/N)?` → `EOFError`
  in any non-interactive shell, with no hint in the tail output. Fix: `rm -f
  .git/filter-repo/already_ran` then re-run. Check for the marker whenever
  filter-repo "succeeds" instantly but object counts don't change.
- **Stash blocks the rewrite**: a stash referencing PHI paths triggers another
  interactive sanity prompt → same EOFError. `git stash show -p > backup.patch`
  first, then `git stash clear`.
- **filter-repo DROPS remotes on success** (anti-force-push protection):
  re-add `origin` before pushing or you get "Could not read from remote".
- **macOS LibreSSL kills big force-pushes**: `SSL_read ... sslv3 alert bad
  record mac` / "unexpected disconnect". Fix: `git config http.version
  HTTP/1.1` (the real fix) + `http.postBuffer 524288000` + push ONE branch at
  a time. Retry with the same command after the SSL error — sometimes partial.
- **`push --force --all` covers only local branches**: remote-only branches
  survive with old history. Enumerate `git ls-remote --heads` and audit each.
- **9-check QA battery beats single checks**: perms, tracked count, gitignore,
  manifest re-hash, per-ref remote counts, backup lock, stray copies
  (`find` outside the dir), TM snapshots, fork count — all ten, every pass.

## macOS leak surfaces (census techniques)

- **Spotlight indexes file CONTENT**: `mdfind -count "kMDItemTextContent ==
  '*<med-or-term>*'"` found 665 files. Fix requires sudo (System Settings >
  Siri & Spotlight > Privacy drag the dirs in) — a principal manual step; say so
  explicitly rather than claiming it done.
- **Obsidian vaults symlink into iCloud**: `~/Documents/Obsidian Vault` was a
  symlink → `~/Library/Mobile Documents/com~apple~CloudDocs/Obsidian Vault`.
  `os.walk` does NOT follow a symlinked root — `os.path.realpath()` it first.
  iCloud-evicted (dataless) files read as errors; `brctl download <file>`
  materializes them for inspection. Classify content before panicking (that
  vault held product docs, zero personal health data).
- **FileVault** is the at-rest floor: check `fdesetup status` (was ON).
- **Time Machine local snapshots** can retain pre-scrub `.git`: `tmutil
  listlocalsnapshots /` (none found, but check every time).
- **Live writers**: `lsof <db-path>` before migrating a DB someone may hold
  open; also `-wal`/`-shm` files mean a SQLite writer was recently active.
- **Architecture rule from the census**: never place a personal-data vault
  inside a shared, git-tracked agent workspace or any iCloud container; the
  vault lives outside both, 0700/0600, with the QA organ watching for drift.

## Permanent enforcement

Containment without a sensor decays. Extend the self-evolving QA organ
(`<agent-home>/qa/qa-manifest.json`) with a phi-surface sensor — perms drift,
git retrack, gitignore rules — and negative-test it with the forced-due
protocol (see `organism-reflex-arc` skill, genome extension pitfall).

## References

- `references/git-history-scrub-runbook.md` — the exact command sequence with
  verification outputs from the 2026-08-17 execution (copy-adapt for any repo)
- `references/macos-data-surface-census.md` — commands for each macOS leak
  surface, false-positive classification examples, iCloud/Obsidian symlink trap
