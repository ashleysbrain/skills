# Git History Scrub Runbook (executed 2026-08-17, verified)

Context: 287 PHI files under `health-private/` had been PUSHED to
github.com/your-org/the operator agent (18 commits, 364 objects reachable from
origin/main, oldest 2026-06-20). Repo private, 0 forks, FileVault ON. Shared
repo: sibling-agent commits to it actively — bus alert BEFORE the rewrite is
mandatory (their 109 local commits were rewritten; guidance: fetch + reset
--hard if diverged). Adapt paths/repo for any repeat use.

## 0. Measure exposure (never skip — this decides everything)

```bash
git fetch origin
git log origin/main --oneline -- health-private | wc -l          # 18 pushed commits
git rev-list --objects origin/main -- health-private | wc -l     # 364 objects
T=$(mktemp -d) && git clone -q --no-local . $T/c && cd $T/c
git rev-list --objects --all -- health-private | wc -l           # cloner's view
cd - && rm -rf $T
gh api repos/your-org/the operator agent --jq '.private, .forks_count' # blast radius
```

## 1. Freeze manifest (inside the private dir, before ANY operation)

```python
import hashlib, os, json, datetime
root='health-private'; manifest={}
for dp,_,fns in os.walk(root):
    for fn in fns:
        p=os.path.join(dp,fn)
        manifest[p]={'sha256':hashlib.sha256(open(p,'rb').read()).hexdigest(),
                     'size':os.path.getsize(p)}
out={'frozen_at':datetime.datetime.now().isoformat(),'count':len(manifest),'files':manifest}
json.dump(out,open('health-private/MIGRATION-MANIFEST.json','w'),indent=1)
```
Then `chmod 600` it. Re-verify 0 mismatches after every later step (verified
3x during the 2026-08-17 run). Count-at-freeze is the truth — file counts
drift (285→287 the same morning).

## 2. Safety net + bus coordination

```bash
mkdir -p /<workspace>
git bundle create /<workspace> operator agent-full-backup-2026-08-17.bundle --all
git bundle verify /<workspace> operator agent-full-backup-2026-08-17.bundle
git stash show -p stash@{0} > /<workspace>   # if stashes exist
# bus alert to sibling operators: rewrite imminent, commit NOW
```
Lock the vault dir 0700/0600 afterward. The bundle is now the ONLY copy of
the old history (contains PHI by design) — never move it into a git dir.

## 3. Lock perms + untrack

```bash
chmod 700 health-private
find health-private -type f -exec chmod 600 {} +   # note: lint prefers search_files for discovery
find health-private -type d -exec chmod 700 {} +
git rm -r --cached health-private -q
printf "\n# PHI containment\nhealth-private/\n*.vault-backup\nvaults/\n" >> .gitignore
git add .gitignore && git commit -m "PHI containment: untrack, ignore vault paths"
git ls-files health-private | wc -l   # expect 0
```

## 4. Scrub (with the three gotchas that block everyone)

```bash
# (a) clear the stale marker from any PREVIOUS attempt, else interactive
#     prompt -> EOFError in non-interactive shells:
ls .git/filter-repo/ 2>/dev/null && rm -f .git/filter-repo/already_ran
# (b) stash referencing PHI paths triggers another prompt — stash show -p >
#     backup.patch, then git stash clear (done in step 2)
git-filter-repo --invert-paths --path health-private --force
git reflog expire --expire=now --all
git gc --prune=now
# (c) filter-repo DROPS remotes on success — re-add before pushing:
git remote add origin https://github.com/your-org/the operator agent.git
```

## 5. Verify local

```bash
git rev-list --objects --all -- health-private | wc -l   # 0
git log --all --oneline -- health-private | wc -l        # 0
git rev-list --count HEAD                                 # 471 (vs pre-scrub, must match)
git ls-files | wc -l                                      # 3170 intact
# fresh-clone test again — 0 objects in the clone
```

## 6. Push (macOS SSL gotcha) + audit EVERY remote ref

```bash
git config http.version HTTP/1.1        # fixes LibreSSL 'sslv3 alert bad record mac'
git config http.postBuffer 524288000
git push --force origin main            # ONE branch at a time; retry on SSL error
git push --force origin <branch2> <branch3>
# CRITICAL: push --all covers LOCAL branches only. Remote-only refs survive
# with old history:
for ref in $(git ls-remote --heads origin | awk '{print $2}' | sed 's|refs/heads/||'); do
  git fetch origin $ref -q
  echo "$ref: $(git rev-list --objects origin/$ref -- health-private | wc -l)"
done   # every line must read 0
```
2026-08-17 result: all 4 refs (main, anatomical-audit, sibling-agent/session-2026-06-25,
recover-organism-work) verified 0. The remote-only `anatomical-audit` had been
skipped by `--all` — only the per-ref audit caught the gap (it was clean).

## 7. Final QA battery (run twice, from scratch each time)

Perms (`stat` + `find ! -perm` counts) / tracked count / gitignore rules /
manifest re-hash / per-ref remote object counts / backup bundle lock state /
stray copies outside the dir / `tmutil listlocalsnapshots /` / fork count /
unpushed-count == 0. Then make enforcement permanent (QA-organ phi-surface
sensor, forced-due negative test — see organism-reflex-arc skill).
