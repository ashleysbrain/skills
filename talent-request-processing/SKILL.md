---
name: talent-request-processing
category: devops
description: Standard procedure for processing talent requests in OpenClaw system.
---

# Talent Request Processing

## Overview

Use this skill for the OpenClaw talent-request patrol loop: scan incoming requests, compare them against the live agent fleet, decide whether to dispatch an existing agent or spawn a new one, log the decision, move the request to processed, and refresh fleet analytics.

This is the canonical umbrella for the older FORGE/ARBITER talent-request variants.

## When to Use

- cron-driven talent request patrols
- manual review of new talent requests in the OpenClaw workspace
- capacity checks that decide between dispatching an existing agent and spawning a new profile

## Templates

- `templates/sample-request.md` - A sample talent request markdown file to be filled out and placed in the talent-requests directory.

## References

- `references/2026-06-10-talent-request.md` - Session-specific detail of a no-request talent request processing run.
- `references/2026-06-10-quartz-builder-request.md` - Session-specific detail of the Quartz Builder build sprint request.
- `references/fleet-analytics-sync-2026-06-10.md` - Sample output of the fleet analytics sync command for 2026-06-10.
- `references/2026-06-12-talent-request.md` - Session-specific detail of the June 12, 2026 talent request processing run (zero requests).
- end-of-run journaling and analytics refresh after requests are processed

## Shared Workflow

### Legacy FORGE/ARBITER aliases absorbed

Older narrow variants such as `forge-arbiter-talent-request-processing` and `forge-arbiter-talent-patrol` are now treated as legacy entry points for this same patrol loop. Keep the workflow here authoritative and avoid re-creating separate sibling skills for the same request-scanning / dispatch / journaling cycle.

### 1. Find incoming requests

Scan the active talent-request intake location used by the workspace. In current OpenClaw layouts this is typically the `talent-requests/journal/` directory, with completed requests moved to `processed/`.

If no request files are present, exit cleanly and report that no action was required.

### 2. Read and evaluate each request

For every request file:

- read the request content
- extract the role, responsibilities, required skills, and any special constraints
- query the active agents database
- compare the request against existing agents before deciding to spawn

Decision rule:
- **dispatch existing agent** when a current agent already covers the request **and satisfies any special constraints in the request (e.g., forbidden models)**
- **spawn new agent** only when there is a genuine gap in the fleet **or no existing agent meets the request's constraints**

### 3. Log the decision in the request file

Append a `## DECISION` section that records:
- timestamp
- decision (`DISPATCH_EXISTING` or `SPAWN_NEW_AGENT`)
- reasoning
- target agent or new agent identifier

Keep the decision record close to the request so later patrols can see what happened without searching logs.

### 4. Move processed requests

After each request has been handled, move it to the processed directory so it is not re-evaluated on the next patrol.

### 5. Refresh fleet analytics

Run the fleet analytics sync after the batch completes so the reporting layer reflects the latest dispatch and spawn decisions.

### 6. Journal and commit

Write the patrol summary to the workspace's FORGE and ARBITER journal locations, then commit the request updates, journals, and any database changes if the workspace is under git.

If the environment blocks shell redirection into dotfile paths, use the operator agent file tools (`write_file` / `patch`) instead of raw `>` or `>>` redirection.

## Support Notes

- Use the active agents table as the source of truth before considering a spawn.
- Preserve the request file until the decision has been appended.
- Keep the patrol idempotent: once a request is moved to `processed/`, it should not reappear in the next run.
- If the workspace has both patrol-specific and general talent-request notes, prefer the workspace-canonical path and keep the README-level instructions here concise.

## Common Pitfalls

- moving files before writing the decision record
- spawning a new agent when an existing one already matches the request
- forgetting the analytics sync, which leaves the fleet view stale
- using shell redirection into blocked dotfile paths when file tools are required
- assuming the current directory is the OpenClaw workspace without verifying it first
- forgetting to check request constraints (e.g., forbidden models) when evaluating existing agents, leading to unsuitable dispatches

## Verification

## Scripts

- `scripts/verify-request.sh` - Verifies that a talent request has been processed (contains DECISION section and moved to processed/).

## Session References
- See `references/2026-06-10-talent-request.md` for a session-specific example of a no-request run.
- FORGE and ARBITER journals reflect the same patrol run
- git status shows the expected request, journal, and database changes
