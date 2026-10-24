# Org remote push verification

When user says "push to Cyber-the operator agent not mine" (or any org repo):

```bash
git remote -v
# expect: https://github.com/Divinity-Science-Research-Lab/Cyber-the operator agent.git

git push
git fetch origin
git status -sb          # main...origin/main
git rev-parse HEAD
git ls-remote origin HEAD
# SHAs must match
```

Clean local tree alone is insufficient if remote is wrong or push never reached origin.
