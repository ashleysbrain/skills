# Repo discovery in multi-repo workspaces

Use this when the user names a repo, folder, or doc set that may live outside the current working directory.

## Verified pattern from this session

- The first guessed path can be wrong, even when it contains similar project names.
- Check the actual git root before drawing conclusions:
  - `git status --short --branch`
  - `git remote -v`
- If the path is not a git repo, search upward and laterally for nearby workspaces instead of assuming the user meant the current repo.
- Confirm the target repo by checking for the expected docs/files, not just the folder name.
- When a repo has a documentation-led workflow, read the repo README and the main doc index before answering about process flow or implementation state.

## Quick verification sequence

1. Locate candidate checkout.
2. Confirm `.git` exists.
3. Read `git remote -v`.
4. Search for the user-named artifact in file contents.
5. Read the top-level README plus the relevant doc index.
6. Only then state whether the requested item is present and where it lives.
