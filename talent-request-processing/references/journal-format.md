# Journal Entry Format for FORGE and ARBITER

## Observed Format in Journal Files

The FORGE and ARBITER journal files (`FORGE-journal.md` and `ARBITER-journal.md`) have historically used a multi-line summary format. Each patrol session appends a timestamped section followed by bullet points summarizing the actions taken.

### General Structure

```
## [TIMESTAMP] - [AGENT] [DESCRIPTION]
- [Bullet point 1]
- [Bullet point 2]
...
```

### Examples from Actual Journal Entries

**Example 1 (FORGE):**
```
## Thu May 21 18:46:25 UTC 2026 - FORGE Agent Processing Talent Requests
- Checked for new talent requests in ~/.sibling-agent/workspace/intel/agents/talent-requests/
- Found 3 requests (2 processed earlier today, 1 pending)
- Processed 2 talent requests (NUT and SX panels from 2026-04-04)
- Spawned 0 agents (panels already existed)
- Made 2 dispatch decisions (used existing agents)
- Processed 1 talent request (FORGE scoring panel expansion fr
```

**Example 2 (FORGE):**
```
## 2026-05-23T08:02:43 - FORGE Talent Request Sweep (Automated)

- Scanned talent-requests directory: 0 new unprocessed requests found
- Active fleet: 252 agents registered in analytics DB
- Fleet analytics sync completed successfully:
  - 123 cron jobs synced, 252 active agents
  - 458 errors in 24h (0 rate-limit, 0 timeout)
  - 51 sessions active, 1703 journal entries indexed
  - Journal compliance: 0.0% (flagged for attention)
- Decision: No new talent gaps identified; fleet at operational capacity
- No agents spawned, no dispatch decisions required
```

**Example 3 (ARBITER):**
```
## 2026-05-22T16:06:23 - ARBITER Agent Processing Talent Requests
- Checked for new talent requests in ~/.sibling-agent/workspace/intel/agents/talent-requests/
- Found 0 requests
- Processed 0 talent requests
- Spawned 0 agents (no requests)
- Made 0 dispatch decisions (no requests)
```

### Notes on Format

- The timestamp format varies: sometimes it's `Day Mon DD HH:MM:SS UTC YYYY`, sometimes `YYYY-MM-DDTHH:MM:SSZ`.
- The description after the agent name can be free-form (e.g., "Agent Processing Talent Requests", "Talent Request Sweep (Automated)").
- Bullet points use a hyphen and a space.
- Indentation is used for sub-bullets (two spaces then a hyphen).
- Blank lines may appear between the header and the first bullet.

## Machine-Readable Format (Alternative)

For automated processing, a single-line format may be preferred. This format is not currently used in the journal files but is supported by the skill:

```
[YYYY-MM-DD HH:MM:SS UTC] FORGE: Processed talent requests - X found, Y dispatched, Z spawned.
```

Where:
- X = number of talent request files found
- Y = number of requests where an existing agent was deemed suitable (dispatch)
- Z = number of new agents spawned (genuine gaps)

If no requests were found, the entry is:
```
[YYYY-MM-DD HH:MM:SS UTC] FORGE: Processed talent requests - none found.
```

## Security Note
Due to security scanner blocks on shell redirection to dotfile paths, journal updates must be performed using the operator agent tools (`read_file`, `write_file`, `patch`) instead of shell redirection (`>>`, `>`). See the talent-request-processing skill for the recommended workflow.

## Note on Format and Tools

- The journal entry can be either the multi-line summary format (as observed) or the single-line format (for machine readability).
- To update the journal, use the operator agent tools (`read_file` and `write_file`) to read the current content, append the new section, and write it back. Do not use shell redirection (`>>` or `>`) as it may be blocked by security scanners.