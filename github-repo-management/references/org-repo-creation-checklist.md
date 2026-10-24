# Org Repo Creation Checklist

Session-derived pattern for creating a new repo inside an organization and verifying it landed in the right place.

## Pattern

1. Confirm the organization name.
2. Check accessible org repos with the GitHub API.
3. Create the repo under the org, not the personal account.
4. Push the current directory to the new repo.
5. Verify the repo URL and visibility.

## Commands

```bash
# Inspect accessible org repos
gh api orgs/your-org/repos?per_page=100 --jq '.[].full_name'

# Create a private repo under the org from the current directory
gh repo create your-org/ds-wave-coaching-engine --private --source . --remote origin --push

# Verify the repo exists and is private
gh repo view your-org/ds-wave-coaching-engine --json name,visibility,url,description

git remote -v
git status --short --branch
```

## Notes

- Use the org/repo form explicitly so the repo is not created in the personal namespace by accident.
- A successful `gh repo create ... --source . --remote origin --push` should leave the local branch tracking `origin/main`.
- If the repo already exists, `gh repo view ORG/REPO` will confirm it quickly.
