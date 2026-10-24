---
name: offsite-encrypted-backup
description: Use when building encrypted offsite backups over git.
category: devops
tags: [backup, encryption, gpg, git, launchd, disaster-recovery]
---

# Offsite Encrypted Backup (GPG + git transport)

Class of task: getting critical local state (SQLite stores, agent state dirs,
memory/skill trees) off-machine, encrypted CLIENT-SIDE, on a schedule, with
proven restorability — using a git host as the transport because it is the one
remote already authenticated with repo scope and no human in the loop.

## Procedure

1. **Discovery before design.** `which rclone restic borg age` — if any exist,
   prefer it. Then check transports: `gh auth status` (repo scope suffices);
   cloud CLIs that require interactive re-auth are a user-side step, not
   yours. Pick the transport that needs no human mid-loop.
2. **Create the private remote** (`gh repo create <org>/<vault> --private`),
   HTTPS remote + gh credential helper — SSH needs key config the vault does
   not have.
3. **Encrypt PER FILE, never one tarball.** Tar directories first, then GPG
   each file individually under the host's per-object limit (100MB on GitHub
   pre-receive); `split` any single file over the limit before encrypting.
   A monolithic multi-store tarball is rejected after the whole upload.
4. **Ciphertext-only staging law.** The local clone receives encrypted files
   only; decrypt NEVER happens inside it; stage an explicit manifest list —
   `git add -A` in a vault clone is how plaintext leaks (a failed run left
   staged plaintext, the next blanket add swept it into a push). A
   `.gitignore` banning plaintext patterns is the standing guard, and the
   script must clean its staging dir on failure (trap) — the half-failed run
   is exactly when decrypted artifacts sit on disk.
5. **Absolute binary paths** in the script — launchd runs a minimal PATH, so
   `/usr/local/bin/gpg`, not `gpg`. A run dying on a missing binary
   mid-staging is the plaintext-leak scenario from step 4.
6. **Push reliability:** `git config http.postBuffer 52428800` and retry the
   push ×3 with backoff — LibreSSL throws transient `bad record mac` on
   multi-MB pushes.
7. **Schedule via launchd** plist (daily). `launchctl load -w` after a silent
   bootstrap failure (a load that printed nothing may not have registered);
   verify by reading the run log after the FIRST scheduled window, not just
   after a manual `launchctl start` — the manual run inherits your shell
   environment, the scheduled one runs as launchd (different PATH, different
   behavior).
8. **Prove restorability before reporting done:** fresh clone from the remote,
   decrypt with the recipient key, open the DB, count rows, compare against
   the live store. A backup that has never been restored is a hypothesis, not
   a backup.
9. **Record the key fingerprint and a ciphertext manifest** (names, sizes,
   sha256 — safe, describes ciphertext only) in the repo so a restore session
   knows what should come back.

## Pitfalls
- **Key placement defines what you survive.** A GPG private key that exists
  only on the backed-up machine protects against disk loss, not host loss —
  get the key to a second location or say explicitly which failure mode is
  covered.
- **Verify the remote tree via the host API** after the first push and after
  any purge; the local clone's state is not evidence of the remote's.
- **If plaintext ever reached the remote:** orphan-branch force-push purge —
  full runbook in `sensitive-data-containment` (git-history-scrub reference).
  For a single-purpose vault the orphan-branch path is faster than
  filter-repo.
- **Split files reassemble on restore** — record the split command in the
  manifest so the restore session knows `cat` order and chunk naming.

## Related skills
- `sensitive-data-containment` — leak scrubbing and the purge runbook.
- `hermes-cron-scheduling` — scheduling alternatives when launchd is not the
  right supervisor.
