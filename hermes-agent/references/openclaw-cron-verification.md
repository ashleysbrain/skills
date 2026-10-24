# OpenClaw Cron Job Verification

When managing cron jobs in the OpenClaw system (used by NEXUS for auto-remediation), it's critical to verify that job IDs exist in the live system before attempting edits.

## Key Lesson from NEXUS Auto-Remediation

During auto-remediation cycles, the NEXUS agent encountered `GatewayClientRequestError: Error: unknown cron job id: <job_id>` errors when trying to edit cron jobs based on data from the analytics database.

### Root Cause
- The analytics database (`~/.sibling-agent/workspace/intel/agents/database/agents.db`) contains historical cron job records
- The live OpenClaw system only contains currently active/scheduled cron jobs
- Job IDs from the analytics DB may not exist in the live system if the job was deleted or never synced

### Verification Procedure
Before editing any cron job obtained from analytics or other sources:

1. **Check live system first**:
   ```bash
   sibling-agent cron list --json
   ```
   or
   ```bash
   sibling-agent cron list
   ```

2. **Verify job ID exists** in the live output before attempting edits

3. **If job not found in live system**:
   - Skip the edit operation
   - Log that the job appears to be historical or already removed
   - Continue with other jobs

### Example Workflow
```bash
# Get candidate jobs from analytics DB
sqlite3 agents.db "SELECT job_id, job_name FROM cron_jobs WHERE consecutive_errors >= 3"

# For each job, verify in live system
sibling-agent cron list | grep <job_id>  # or use --json and parse

# Only edit if found in live system
sibling-agent cron edit <job_id> --model "new-model"
```

### Best Practices for NEXUS
- Always verify job existence in live OpenClaw system before editing
- Treat analytics DB as a historical record, not a source of truth for live job state
- Add verification step to all cron job automation scripts
- Log verification results for audit trails