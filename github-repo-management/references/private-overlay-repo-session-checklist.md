# Private overlay repo session checklist

Use this checklist when the user wants a new private repo that sits beside an existing private repo, not inside it.

## Verify first
- Confirm the parent repo URL the user named.
- Confirm the local checkout is the repo you think it is with `git status --short --branch` and `git remote -v`.
- If the target is a sibling repo, create it in a separate local directory.

## Scaffold the overlay repo
- `README.md` for purpose and guardrails.
- `manifest.yaml` for stable IDs, file paths, and status.
- `PROCESS.md` for the workflow.
- `HISTORY.md` for compact rolling history.
- One logical item per file under a dedicated subdirectory like `coaches/`.

## Create and publish
1. `git init -b main`
2. Commit the scaffold locally.
3. Create the GitHub repo as `--private`.
4. Push `--source . --remote origin --push`.
5. Verify the GitHub repo visibility is private.
6. Verify the local checkout is clean after push.

## Helpful verification commands
```bash
gh repo view OWNER/REPO --json name,url,visibility,defaultBranchRef
git status --short --branch
```
