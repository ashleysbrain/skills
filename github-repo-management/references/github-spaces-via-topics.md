# GitHub "Spaces" via Topic Tags (No Nested Groups)

GitHub has no nested groups/subgroups (that's a GitLab feature). When the user
asks to "create a space" or "put this under X space," implement the logical
grouping with two mechanisms working together:

1. **Repo-name prefix** — every repo in the space shares a prefix (e.g. `8d-`)
2. **Shared topic tag** — every repo carries a topic that identifies the space (e.g. `8d`)

The topic tag is what makes the space queryable: `gh api orgs/<org>/repos` +
filter on `.topics` returns the full family.

## Creating a New Space Member (verified sequence)

```bash
# 1. Create the repo under the org (NOT the personal account)
gh repo create your-org/8d-sleep \
  --private \
  --description "8D Sleep — ... Powered by Divinity Science."

# 2. Init locally + add remote + first commit + push
cd /path/to/project
git init -b main
git remote add origin https://github.com/your-org/8d-sleep.git
git add -A
git diff --cached --name-only | grep -c node_modules   # must be 0
git commit -m "feat: initial commit ..."
git push -u origin main

# 3. Tag with topic(s) — this is what binds the repo to the space
gh api repos/your-org/8d-sleep/topics \
  --method PUT \
  -f names[]=8d \
  -f names[]=your-org \
  -f names[]=<product-specific-tags>

# 4. Verify the space (all repos in the family)
gh api "orgs/your-org/repos?per_page=100" \
  --jq '.[] | select(.topics[]? | contains("8d")) | "\(.name) — \(.visibility)"'
```

## the specialist engine (hard rule)

User correction (2026-06-19, exact words):

> "This does not need to sit in aisha or ashleys brain. This needs to go in
> your-org."

**DS product repos live in the `your-org` GitHub org.** They do NOT
live in the AISHA/the principal workspace (`/<workspace>`) or any
personal namespace. The workspace is for agent operations; product code is for
the org.

Current DS org structure:

| Repo | Visibility | Space |
|---|---|---|
| `8d-sleep` | private | 8D (topics: 8d, sleep, pwa, physics-informed) |
| `8d-pattern-awareness` | public | 8D (topics: 8d, your-org) |
| `divinityscience.com` | private | marketing |
| `health-intelligence-platform` | public | research |
| `ds-wave-coaching-engine` | private | ds-wave |

When creating a new DS product: pick the prefix for its space (or start a new
one), create under `your-org/`, tag with `your-org` + the space
tag + product-specific tags.

## Pre-Commit Hygiene for First Commit of an Existing Untracked Project

When a project has been developed without version control (no `.git`, working
files only), the first commit must be clean:

1. **Create `.gitignore` BEFORE `git add`** — exclude `node_modules/`, `dist/`,
   `.env*`, editor cruft. A Vite project can be 139MB with deps; only ~1MB
   without.
2. **Verify exclusions**: `git diff --cached --name-only | grep -c node_modules`
   must return 0 before committing.
3. **Scan for secrets**: check staged filenames for `.env`, `secret`, `key`,
   `token`, `credential`, `password` patterns before pushing.
4. **`gh repo create` does NOT accept `--default-branch`** — use `git init -b
   main` locally instead, or rename after creation via `gh repo edit
   --default-branch main`.
