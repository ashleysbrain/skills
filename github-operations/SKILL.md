---
name: github-operations
description: "Use when working end-to-end with GitHub auth, repos, issues, PRs, reviews, and releases from CLI or API fallbacks."
version: 1.0.0
author: the operator agent Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, auth, repos, issues, pull-requests, reviews, releases, actions]
---

# GitHub Operations

## Overview

Use this skill for the full GitHub workflow: authenticate, inspect or manage a repository, create or triage issues, work on branches and pull requests, review diffs, and perform common release or Actions tasks.

Prefer `gh` first when it is installed and authenticated. Fall back to `git` + `curl` when you need a portable path that works without `gh`.

## When to Use

- authenticating to GitHub for the first time on a machine
- cloning, forking, creating, configuring, or syncing repos
- creating, searching, labeling, assigning, closing, or commenting on issues
- creating branches, opening PRs, checking CI, merging, or auto-merging
- reviewing local diffs or open PRs and leaving inline comments
- managing releases, Actions workflows, secrets, or repo settings

## Core Pattern

1. **Detect auth and repo context**
   - Check whether `gh` is installed and authenticated.
   - If working inside a repo, resolve `owner/repo` from `origin`.
   - If auth is missing, use the simplest available path: token-based `gh`, then git credentials, then explicit `curl` with a token.

2. **Use the narrowest workflow that fits**
   - Repo identity / config / secrets / releases / workflows → repository operations
   - New bug/feature intake → issues
   - Branching, PRs, CI, merge flow → PR workflow
   - Reading or commenting on code → code review

3. **Verify before acting**
   - Confirm the target repo, branch, PR number, or issue number.
   - Do not assume the current checkout is the target repository in multi-repo workspaces.

## Shared Auth Bootstrap

```bash
## Shared Auth Bootstrap

```bash
## Shared Auth Bootstrap

```bash
## Shared Auth Bootstrap

```bash
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  AUTH=gh
else
  AUTH=git
  if [ -z "${GITHUB_TOKEN:-}" ]; then
    if [ -f <agent-home>/.env ] && grep -q '^GITHUB_TOKEN=' <agent-home>/.env; then
      GITHUB_TOKEN=$(grep '^GITHUB_TOKEN=' <agent-home>/.env | head -1 | cut -d= -f2-)
    elif [ -f ~/.git-credentials ] && grep -q 'github.com' ~/.git-credentials; then
      GITHUB_TOKEN=$(grep 'github.com' ~/.git-credentials | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
    fi
  fi
fi

REMOTE_URL=$(git remote get-url origin 2>/dev/null || true)
OWNER_REPO=$(printf '%s' "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(printf '%s' "$OWNER_REPO" | cut -d/ -f1)
REPO=$(printf '%s' "$OWNER_REPO" | cut -d/ -f2)
```

## Repository Operations

Use this branch for cloning, creating, forking, configuring, secrets, releases, and workflow admin.

- Clone or fork with `gh repo clone` / `gh repo fork` when possible.
- Create repos with `gh repo create` or the REST API when necessary.
- Keep repository settings, branch protection, topics, secrets, and workflows explicit.
- When managing release artifacts, verify the uploaded asset and the release tag.

## Issues

Use this branch for issue intake and triage.

Typical actions:
- list open issues
- search issues by label or keyword
- create an issue from a bug report or feature request
- label, assign, comment, close, or reopen

Best practice:
- preserve the user’s wording for the issue title when it is already good
- add a concise repro / expected-behavior body when the request is underspecified
- use labels and assignment as soon as the issue has enough signal to route

## Pull Requests

Use this branch for branch/PR lifecycle work.

Typical flow:
1. create or update a branch
2. push the branch
3. open a PR
4. monitor CI and fix failures
5. merge or enable auto-merge

Keep branch names and commit messages conventional when possible.

## Code Review

Use this branch when the task is to review local changes or a remote PR.

Checklist:
- correctness and edge cases
- security and secrets
- code quality and maintainability
- tests and missing coverage
- performance and operational risk

For remote PRs:
- prefer `gh pr view` / `gh pr diff` when available
- fall back to the API when you need portability or fine-grained automation
- leave both inline comments and a top-level summary when the review has actionable findings

## Releases and Actions

Use this branch when the user wants repo admin tasks:
- create or inspect releases
- upload assets
- inspect or rerun workflows
- inspect run logs
- manage secrets or repo settings

Keep the exact release tag, workflow name, or run ID explicit before making changes.

## Common Pitfalls

- **Using raw git commands instead of this skill (2026-06-21 correction):** When any GitHub operation is needed, LOAD THIS SKILL FIRST and follow the specialist workflow (branch, PR, review). Never run `git add && git commit && git push` directly as a generalist. The user explicitly corrected: "What brain did you have when you pushed that to GitHub?" — the answer must always be "GitHub operations specialist with the github-operations skill loaded."
- **GitHub password auth does not work; use a token or SSH.**
- Org-scoped operations can fail with `403` if the token lacks the needed scope.
- Multi-repo workspaces often make the current checkout ambiguous; verify the remote before editing or pushing.
- `gh` is the best path when available, but do not assume it exists on every machine.
- Always confirm the target PR or issue number before posting comments or reviews.

## Verification

- `gh auth status` succeeds, or the token-based fallback works.
- The resolved `owner/repo` matches the intended repository.
- The target issue / PR / release / workflow is the one you expected.
- Any posted comment, created issue, or release asset is visible on the remote side.
