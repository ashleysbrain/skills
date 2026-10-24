# Git Commit Procedure for Journal Updates

After updating the FORGE and ARBITER journals, commit the changes to the OpenClaw workspace repository.

## Steps
1. **Check the git status** (from the OpenClaw workspace root)
   ```bash
   git -C ~/.sibling-agent/workspace status --porcelain
   ```
   Look for changes to `intel/agents/database/FORGE-journal.md` and `intel/agents/database/ARBITER-journal.md`.

2. **Add the updated journal files**
   ```bash
   git -C ~/.sibling-agent/workspace add intel/agents/database/FORGE-journal.md intel/agents/database/ARBITER-journal.md
   ```

3. **Commit the changes**
   Use a descriptive message that includes the date and action.
   ```bash
   git -C ~/.sibling-agent/workspace commit -m "Update journals: checked for talent requests, none found"
   ```
   If talent requests were found and processed, adjust the message accordingly.

## Notes
- The `-C` flag allows running git commands from a specific directory without changing the shell's current directory.
- Always verify that you are committing from the OpenClaw workspace root (`~/.sibling-agent/workspace`) to ensure the correct repository is used.
- If the repository is not found at `~/.sibling-agent/workspace`, adjust the path accordingly.

## Example Output
```
$ git -C ~/.sibling-agent/workspace status --porcelain
 M intel/agents/database/ARBITER-journal.md
 M intel/agents/database/FORGE-journal.md
$ git -C ~/.sibling-agent/workspace add intel/agents/database/ARBITER-journal.md intel/agents/database/FORGE-journal.md
$ git -C ~/.sibling-agent/workspace commit -m "Update journals: checked for talent requests, none found"
[main 7bee2348] Update journals: checked for talent requests, none found
 2 files changed, 2 insertions(+)
```