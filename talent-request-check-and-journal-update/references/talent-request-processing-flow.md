# Talent Request Processing Flow

This reference outlines the standard flow for processing a talent request file in the OpenClaw system.

## Overview
When a new talent request appears as a Markdown file in `~/.sibling-agent/workspace/intel/agents/talent-requests/`, the FORGE and ARBITER cron job (or manual processing) follows these steps:

## Detailed Steps

### 1. Read the Request
- Read the entire content of the request file.
- The file typically includes a description of the needed agent role, specialty, and any specific requirements.

### 2. FORGE Evaluation: Existing Agent Check
FORGE queries the `agents` table for all active agents to see if any existing agent matches the request.

```sql
SELECT display_name, role, specialty, primary_model
FROM agents
WHERE status='active';
```

- Compare the request's desired role/specialty against each agent's `role` and `specialty` fields.
- If a match is found (or a close enough match that the existing agent can handle the work), proceed to step 3a.
- If no match is found, proceed to step 3b (gap identification).

### 3a. Existing Agent Fits → Dispatch
- ARBITER writes a dispatch note to the request file.
- Append a section `## DECISION` with content:
  ```
  Dispatch to existing agent: <display_name>. No new agent needed.
  ```
- Do **not** spawn a new agent.
- Move on to step 5 (moving the processed request).

### 3b. Genuine Gap → New Agent Profile Required
- FORGE logs that a gap has been identified.
- Append a section `## DECISION` with content:
  ```
  Gap identified. New agent profile required.
  ```
- The actual creation of a new agent profile (soul file, DB registration, journal entry, etc.) is outside the scope of this cron job and requires separate approval and steps (see the full agent spawning protocol).
- For the purposes of this cron job, no further action is taken beyond logging the gap.

### 4. (Optional) Log Decision in Request File
Both outcomes (3a and 3b) involve appending a `## DECISION` section to the request file, as described above.

### 5. Move Processed Request
Regardless of outcome, move the request file to the processed directory to avoid reprocessing:

```bash
mv "$request_file" ~/.sibling-agent/workspace/intel/agents/talent-requests/processed/
```

## Notes
- The request file should be moved **after** the decision has been logged.
- If multiple request files are present, process each one sequentially.
- The cron job should handle zero, one, or many request files.
- Always ensure the `processed/` directory exists before moving files.

## Example Request File
```
# Talent Request: Junior Research Agent

We need an agent to assist with daily literature reviews in the field of quantum biology.
Preferred specialty: QTB (Quantum Biology)
Desired role: Research Assistant
```

## Example Dispatch Note (appended)
```
## DECISION
Dispatch to existing agent: DS QUANTUM RESEARCH ASSISTANT. No new agent needed.
```

## Example Gap Note (appended)
```
## DECISION
Gap identified. New agent profile required.
```