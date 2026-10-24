# Talent Request Processing - FORGE/ARBITER Procedure

This file documents the procedure for processing talent requests in the OpenClaw system as performed by FORGE (Chief Agent Architect) and ARBITER (Chief Task Dispatcher).

## Procedure Overview

1. Check for new talent requests: `ls ~/.sibling-agent/workspace/intel/agents/talent-requests/*.md 2>/dev/null`
2. For each unprocessed request:
   a. Read the request
   b. FORGE evaluates: Does an existing agent handle this? Check the analytics DB:
      `sqlite3 ~/.sibling-agent/workspace/intel/agents/database/agents.db "SELECT display_name, role, specialty, primary_model FROM agents WHERE status='active'"`
   c. If existing agent fits → ARBITER dispatches (no spawn needed). Write dispatch note.
   d. If genuine gap → FORGE designs the new agent profile following full protocol:
      - Read spawn template: `~/.sibling-agent/workspace/intel/agents/SPAWN-TEMPLATE.md`
      - 15-20 role-specific PhDs, MBTI/Enneagram/Big Five, 8D scores, model tier
      - Create soul file, register in DB, create journal entry
   e. Log decision in the request file (append DECISION section)
3. Move processed requests to `~/.sibling-agent/workspace/intel/agents/talent-requests/processed/`
4. Update fleet analytics: `python3 ~/.sibling-agent/workspace/intel/agents/database/fleet_analytics.py sync`
5. Report: requests processed, agents spawned (if any), dispatch decisions made
6. Journal both agents' entries. Git commit changes.

## Detailed Steps

### Step 1: Check for Requests
```bash
ls ~/.sibling-agent/workspace/intel/agents/talent-requests/*.md 2>/dev/null
```

### Step 2a: Read Request
Use `read_file` or `cat` to examine the markdown request file.

### Step 2b: FORGE Evaluation
Check existing agents:
```bash
sqlite3 ~/.sibling-agent/workspace/intel/agents/database/agents.db "SELECT display_name, role, specialty, primary_model FROM agents WHERE status='active'"
```

### Step 2c: Dispatch Decision
If match found, ARBITER creates dispatch note in agent's journal.

### Step 2d: New Agent Design (if gap)
Follow SPAWN-TEMPLATE.md to create:
- Soul file with 15-20 role-specific PhDs
- MBTI/Enneagram/Big Five personality assessment
- 8D dimension scores
- Model tier selection
- Register in agents.db
- Create initial journal entry

### Step 2e: Log Decision
Append "DECISION" section to request file with rationale.

### Step 3: Move to Processed
```bash
mv request.md ~/.sibling-agent/workspace/intel/agents/talent-requests/processed/
```

### Step 4: Update Analytics
```bash
python3 ~/.sibling-agent/workspace/intel/agents/database/fleet_analytics.py sync
```

### Step 5: Report
Document: requests processed, agents spawned, dispatch decisions.

### Step 6: Journal & Git
- Add entries to FORGE and ARBITER journals
- Commit changes to git repository

## References
- SPAWN-TEMPLATE.md: Standard template for new agent profiles
- agents.db schema: Contains agent information
- fleet_analytics.py: Script for synchronizing fleet data

## Pitfalls
- Ensure proper permissions for database access
- Handle case where no requests exist (normal operation)
- Verify git repository exists before committing
- Journal directories may need creation before first use
