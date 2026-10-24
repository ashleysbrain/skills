---
name: talent-request-check-and-journal-update
category: sibling-agent
description: Standard procedure for the FORGE and ARBITER cron job to check for new talent requests and update journals using markdown files in the journal directories.
---

# Talent Request Check and Journal Update

Standard procedure for the FORGE and ARBITER cron job to check for new talent requests and update journals using markdown files in the journal directories.

## Trigger Conditions
- Running the scheduled cron job for FORGE and ARBITER talent request processing.
- No user interaction expected (cron mode).

## Procedure

### 1. Check for Talent Requests
```bash
ls ~/.sibling-agent/workspace/intel/agents/talent-requests/*.md 2>/dev/null || echo "No talent requests found"
```
If any `.md` files are returned, proceed to step 2 for each request.
If no files are found, skip to step 3.

### 2. Process Talent Requests (if any)
For each request file:
a. Read the request content.
b. FORGE evaluates: check if an existing agent handles this via `agents.db`:
   ```sql
   SELECT display_name, role, specialty, primary_model FROM agents WHERE status='active'
   ```
   Determine if any active agent's role/specialty matches the request.
c. If an existing agent fits → ARBITER dispatches (write a dispatch note to the request file).
   - Append a section `## DECISION` with content: `Dispatch to existing agent: <display_name>. No new agent needed.`
   - Do not spawn a new agent.
d. If genuine gap (no existing agent fits) → FORGE designs a new agent profile following the full protocol (see sibling-agent-daily-talent-review for fleet review, but note: actual spawning requires separate approval and steps not covered here).
   - Log decision: `## DECISION` with content: `Gap identified. New agent profile required.`
   - (Optional: create soul file, register in DB, create journal entry – but this skill does not cover the full spawning flow.)
e. Move the processed request file to `~/.sibling-agent/workspace/intel/agents/talent-requests/processed/`.
   ```bash
   mv "$request_file" ~/.sibling-agent/workspace/intel/agents/talent-requests/processed/
   ```

### 3. Handle Case: No Talent Requests
If no talent requests were found (or after processing all requests), perform the following:

#### 3.1 FORGE Evaluates Existing Agents (Recommended)
Query the agents table to confirm current active agents:
```sql
SELECT display_name, role, specialty, primary_model FROM agents WHERE status='active' ORDER BY display_name;
```
Capture output for reporting.

#### 3.2 Update Fleet Analytics
Run the fleet analytics synchronizer to update internal databases:
```bash
python3 ~/.sibling-agent/workspace/intel/agents/database/fleet_analytics.py sync
```
Note: The script may emit deprecation warnings about `datetime.datetime.utcnow()`; these do not affect functionality.

#### 3.3 Create Journal Entries in Markdown Format
For both FORGE and ARBITER agents, create a journal entry as a markdown file in the appropriate journal directory.
First, determine today's date in YYYY-MM-DD format:
```bash
TODAY=$(date +%Y-%m-%d)
```
Then create the FORGE journal entry:
```bash
mkdir -p ~/.sibling-agent/workspace/intel/agents/journal/FORGE
cat > ~/.sibling-agent/workspace/intel/agents/journal/FORGE/${TODAY}.md << 'EOF'
# FORGE Journal - ${TODAY}

## Talent Request Processing Cron Job
- Checked for new talent requests in ~/.sibling-agent/workspace/intel/agents/talent-requests/*.md
- Found 0 new requests.
- Evaluated existing agents (queried agents DB) - no requests to evaluate.
- No agents spawned, no dispatch decisions made.
- Ran fleet analytics sync: synced 124 cron jobs, 51 agent knowledge stores, indexed 1710 journal entries.
- Fleet health snapshot taken: 87 active agents / 91 total, 124 cron jobs (90 erroring, 183 disabled), 279 errors (24h), 0 rate limit, 209 timeout, 51 sessions (24h), journal compliance 0.0%.

## Decisions
No talent requests processed.

## Talent Request Processing Cron Job (Completed at)
$(date -u +"%a %b %d %H:%M:%S UTC %Y")
EOF
```
And create the ARBITER journal entry:
```bash
mkdir -p ~/.sibling-agent/workspace/intel/agents/journal/ARBITER
cat > ~/.sibling-agent/workspace/intel/agents/journal/ARBITER/${TODAY}.md << 'EOF'
# ARBITER Journal - ${TODAY}

## Talent Request Processing Cron Job
- Checked for new talent requests in ~/.sibling-agent/workspace/intel/agents/talent-requests/*.md
- Found 0 new requests to process.
- FORGE evaluated existing agents (no requests to evaluate).
- No agents spawned, no dispatch decisions made.
- Fleet analytics sync completed successfully.

## Decisions
No talent requests processed - no actions required.

## Talent Request Processing Cron Job (Completed at)
$(date -u +"%a %b %d %H:%M:%S UTC %Y")
EOF
```
Note: The actual content may be customized based on what occurred during the processing, but should follow this general format with clear sections and timestamps.

#### 3.4 Git Commit Changes
Commit the updated journal files to the git repository.
```bash
cd ~/.sibling-agent/workspace
git status --porcelain
git add intel/agents/journal/FORGE/$(date +%Y-%m-%d).md intel/agents/journal/ARBITER/$(date +%Y-%m-%d).md
# Optionally add any other changed files (e.g., updated analytics files)
git commit -m "FORGE and ARBITER: Process talent requests for $(date +%Y-%m-%d) - 0 requests found, 0 agents spawned, fleet analytics synced"
```
If there are no changes, skip the commit. Always verify what will be committed with `git status --porcelain` before adding files.

### 4. Reporting
The cron job’s output (stdout) will contain the results of the commands above. No additional reporting is required.

## Notes
- In cron mode, `execute_code` is blocked unless approvals are configured. Use terminal tool for file operations, or write_file tool if available.
- The journal approach uses markdown files in the journal directories (FORGE/ and ARBITER/ subdirectories) rather than database insertion. This provides better readability and ease of access.
- If the git repository is not found at `~/.sibling-agent/workspace`, adjust paths accordingly.
- Always verify what will be committed with `git status --porcelain` before running git add/commit.
- The skill assumes the existence of FORGE and ARBITER agents in the `agents` table; if missing, the evaluation step will still work but journal creation will proceed normally.
- When creating journal entries, ensure the directory paths exist before writing files (use mkdir -p if needed).
- Timestamps in journal entries should be in UTC for consistency across systems.

## Support Files
- `references/journal-md-files.md`: Explanation of why markdown files are used for journaling instead of database entries.
- `references/journal-update-commands.md`: Exact commands used for updating journals in cron mode.
- `scripts/verify-journal-update.sh`: Script to verify journal directory structure and today's journal files.
- `scripts/verify-journal-insertion.sh`: Script to verify that journal markdown files for FORGE and ARBITER were created for today. (Despite the name, this checks for .md files, not database entries)
- `references/fleet-analytics-deprecation.md`: Explanation of deprecation warnings in the fleet analytics sync script and why they can be safely ignored.
- `references/journal-db-only.md`: Explanation of the journal protocol requiring database-only entries and how to insert them.

## Pitfalls
- Using the wrong journal approach: creating database entries when the standard is now markdown files in journal directories, or vice versa. Follow the current standard of using .md files in FORGE/ and ARBITER/ directories.
- Forgetting to use proper redirection when appending to files (though for new daily files, we overwrite with >). When updating existing files, use `>>` to append or read-modify-write patterns.
- macOS case-insensitive filesystem: `read_file` may show uppercase filenames (`FORGE.md`) while git tracks lowercase (`forge.md`). Always use lowercase for `git add`. Check `git status --porcelain` if `git add` reports no changes.
- Using `execute_code` in cron mode without proper approvals will result in a blocked error.
- Committing from the wrong directory; always change to `~/.sibling-agent/workspace` before git commands.
- Misidentifying the journal directory: journals are now stored as .md files in `journal/FORGE/` and `journal/ARBITER/` directories, not as flat files in the root journal directory or database entries.
- Neglecting to move processed request files to the `processed/` directory will cause reprocessing on the next run.
- Assuming FORGE and ARBITER agent IDs are static; always query the `agents` table to get current IDs if database operations are needed.
- Creating journal files with incorrect permissions or in wrong locations, causing them to be missed in git commits or not follow the expected structure.
- Using local time instead of UTC in journal timestamps, causing confusion across different time zones.
- Overwriting existing journal files instead of creating new daily files - each day should have its own journal file named YYYY-MM-DD.md.