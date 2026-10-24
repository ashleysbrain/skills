# Talent Request Check Command

Command to check for new talent request files in the OpenClaw workspace.

## Command
```bash
ls ~/.sibling-agent/workspace/intel/agents/talent-requests/*.md 2>/dev/null || echo "No talent requests found"
```

## Explanation
- `ls ~/.sibling-agent/workspace/intel/agents/talent-requests/*.md` lists all Markdown files in the talent-requests directory.
- `2>/dev/null` suppresses error messages if the directory is empty or no files match.
- `|| echo "No talent requests found"` provides a friendly message when no files are found.

## Notes
- This command is safe to run in cron mode as it only reads the filesystem.
- The output can be captured and used to decide whether to process requests or just update journals.
- If the directory does not exist, the command will output "No talent requests found" (due to the error suppression and fallback).

## Example Output
When no requests are found:
```
No talent requests found
```
When requests are found:
```
/<workspace>
/<workspace>
```