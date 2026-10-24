# Multi-Repo Disambiguation Checklist

Use this when a user refers to a named project and there are multiple local workspaces or repos that could plausibly contain it.

## Checklist

1. Verify the target repo by checking `git remote -v` before editing.
2. Confirm branch/status with `git status --short --branch`.
3. If the user mentions a specific package or engine, search the candidate checkout for the canonical docs or runtime wrappers before assuming the path.
4. When the project lives in a separate repo, keep the edits and commit in that repo, not in an adjacent workspace.
5. For doc/spec packages, update the landing README and docs index so the new files are discoverable.
6. Verify success with a clean `git status` and a successful push.

## Practical cues

- A repo name in chat does not guarantee the current working directory is the right checkout.
- If a local workspace has multiple related repos, scan for the repo that has the matching remote URL and then inspect its files.
- Runtime wrapper files (for example agent-facing `SOUL.md` and `AGENT.md`) should be included when the user asks for "everything related" to a packaged engine.
