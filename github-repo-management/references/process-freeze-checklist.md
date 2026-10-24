# Process Freeze Checklist

Use this when the user asks to freeze a workflow, process, or doc set in a GitHub repo.

## Goal
Keep the repo's process docs generic, stable, and free of named advisor or persona references unless the user explicitly wants them.

## Steps
1. Confirm the correct git checkout with `git status --short --branch` and `git remote -v`.
2. Search the repo for any named references the user asked to exclude.
3. Edit the minimum set of files so the process stays generic and process-only.
4. If the repo is a docs/spec engine, update the landing README and docs index together so the freeze is discoverable.
5. Commit the freeze with a clear docs-oriented message.
6. Push to the target branch.
7. Verify the repo is clean and the excluded references are gone.

## Verification
- `git status --short --branch` shows a clean tree on the target branch.
- A content search for the excluded names returns zero hits.
- The pushed commit is on the expected remote branch.

## Pitfalls
- Do not hard-code a specific persona into generic workflow docs.
- Do not stop after editing one file if the repo has multiple entry points for the same process.
- Do not claim the freeze is complete until the clean status and search verification both pass.
