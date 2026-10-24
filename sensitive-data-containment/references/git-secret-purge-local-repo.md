# Secret purge from a fresh local-only repo (verified 2026-08-18)

Scenario: webhook secret file committed to a young local repo (never pushed).
Speed matters; git objects touched by the secret are burned either way.

## Steps
1. Detect: git ls-files | grep secret (also grep for token/key/cred patterns).
2. git rm --cached <secret> and write .gitignore covering the secret plus
   volatile state (*.db, *.log, *.err, and post-WAL *.db-wal / *.db-shm).
3. If the secret already sits in an EARLIER commit and the repo is young:
   git reset --soft $(git rev-list --max-parents=0 HEAD)
   git rm --cached <secret>; commit --amend with corrected message.
4. Verify purge mechanically, never by assertion:
   for c in $(git rev-list HEAD); do git ls-tree -r $c --name-only | grep -q <secret> && echo "$c LEAKS"; done
   Empty output = clean.
5. ROTATE the secret regardless (it existed in a git object): generate with
   secrets.token_hex(32), chmod 600, restart the consuming service, re-verify
   its health endpoint.

## Boundaries
This pattern is for local-only history. For pushed repos use filter-repo/BFG
class tooling plus credential revocation everywhere the remote replicated.
Note for AppleEvent-gated contexts: file edits and git work fine; launchctl
bootstrap/bootout may need osascript -e 'do shell script "..."'.
