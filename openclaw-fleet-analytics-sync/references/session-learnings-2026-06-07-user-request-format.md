# Session Learnings: User Request Format for Fleet Analytics Sync (2026-06-07)

## Overview
This document captures the specific format and data points requested by the user for a fleet analytics sync report on 2026-06-07. The user asked for:
- How many cron jobs synced
- Current status distribution (enabled/error/disabled)
- Top 5 errors
- Model distribution
- Journal compliance
- Flag any new critical errors since last sync

## Exact Commands and Queries Used

### 1. Run the sync
```bash
python3 ~/.sibling-agent/workspace/intel/agents/database/fleet_analytics.py sync
```

### 2. Verify sync worked and get cron job count
```bash
sqlite3 ~/.sibling-agent/workspace/intel/agents/database/agents.db "SELECT COUNT(*) FROM cron_jobs;"
```

### 3. Get status distribution (enabled/error/disabled)
```bash
sqlite3 ~/.sibling-agent/workspace/intel/agents/database/agents.db "SELECT status, COUNT(*) FROM cron_jobs GROUP BY status;"
```

### 4. Get top 5 errors (last 24 hours)
```bash
sqlite3 ~/.sibling-agent/workspace/intel/agents/database/agents.db "SELECT error_message, COUNT(*) as cnt FROM error_log WHERE datetime(occurred_at) > datetime('now', '-1 day') GROUP BY error_message ORDER BY cnt DESC LIMIT 5;"
```

### 5. Get model distribution (top 5)
```bash
sqlite3 ~/.sibling-agent/workspace/intel/agents/database/agents.db "SELECT model, COUNT(*) as cnt FROM cron_jobs WHERE model != '' GROUP BY model ORDER BY cnt DESC LIMIT 5;"
```

### 6. Get journal compliance (from sync output or manual query)
From sync output: "Journal compliance: X.X%"
Or manual query:
```bash
sqlite3 ~/.sibling-agent/workspace/intel/agents/database/agents.db "SELECT COUNT(DISTINCT agent_id) * 100.0 / (SELECT COUNT(*) FROM agents) FROM journal_entries WHERE entry_date > date('now', '-7 days');"
```

### 7. Check for new critical errors since last sync
First, get last sync timestamp:
```bash
cat ~/.sibling-agent/workspace/intel/agents/database/last_sync.timestamp
```

Then get new critical errors:
```bash
sqlite3 ~/.sibling-agent/workspace/intel/agents/database/agents.db "SELECT error_message, COUNT(*) as cnt FROM error_log WHERE datetime(occurred_at) > datetime('LAST_SYNC_TIMESTAMP') GROUP BY error_message ORDER BY cnt DESC LIMIT 5;"
```
Replace `LAST_SYNC_TIMESTAMP` with the actual timestamp from last_sync.timestamp file.

## Report Format Used

The user requested the report be structured as:

**FLEET ANALYTICS SYNC REPORT — TIMESTAMP**

**✅ Sync Completed Successfully**

**📊 Cron Job Statistics**
- **Total cron jobs synced:** X  
- **Status distribution:**  
  - Enabled: X  
  - Error: X  
  - Disabled: X  

**🔧 Model Distribution (Top 5)**
1. `model1` – X jobs  
2. `model2` – X jobs  
3. `model3` – X jobs  
4. `model4` – X jobs  
5. `model5` – X jobs  

**⚠️ Error Analysis (Last 24 Hours)**
- **Total errors:** X  
- **Rate limit errors:** X  
- **Timeout errors:** X  
- **Top 5 error messages:**  
  1. Error message 1  
  2. Error message 2  
  3. Error message 3  
  4. Error message 4  
  5. Error message 5  

**🚨 NEW CRITICAL ERRORS SINCE LAST SYNC (TIMESTAMP)**
[List any new errors that appeared after last sync, or note if none]

**📓 Journal Compliance**
- **Compliance rate:** X.X%  
- **Journal entries indexed:** X from Y agent dirs  

**🔄 Additional Sync Metrics**
- **the operator agent sessions synced:** X (in last 24h)  
- **Agent knowledge stores synced:** X  
- **Fleet health snapshot:** Saved for DATE (Z active / W total agents)  
- **Analytics collection:** Complete for DATE  

**📋 Recommended Actions**
1. [Action based on findings]
2. [Action based on findings]
3. [Action based on findings]

**--- End of Report ---**

## Key Learnings

1. **Status Distribution Nuance**: The sync output reports "enabled" as jobs where enabled=1 (includes both healthy and erroring), while the database `status='enabled'` only shows healthy running jobs. For accurate reporting matching sync output, use:
   - Enabled (should run): enabled=1 (includes healthy + erroring)
   - Erroring: enabled=1 AND status='error' 
   - Disabled: enabled=0

2. **Error Tracking**: For recent error volume (last 24h), query the `error_log` table with time filtering. For persistent error states, check `cron_jobs` where `consecutive_errors > 0`.

3. **New Critical Errors**: Compare against the `last_sync.timestamp` file to identify errors that are truly new since the last sync, not just ongoing issues.

4. **Journal Compliance**: The sync script's reported compliance percentage is often unreliable (known bug). Always calculate manually using:
   ```sql
   SELECT COUNT(DISTINCT agent_id) * 100.0 / (SELECT COUNT(*) FROM agents)
   FROM journal_entries WHERE entry_date > date('now', '-7 days');
   ```

5. **Verification**: Always verify data was written to `agents.db` (not `analytics.db` or `fleet_analytics.db`) by checking row counts directly in the database.

## Pitfalls Avoided

- Didn't confuse the sync output's "enabled" count with the database's `status='enabled'` count
- Used `error_log` for recent errors (last 24h) rather than relying solely on `cron_jobs.state` 
- Checked for truly new errors by comparing against last sync timestamp
- Verified data persistence in the correct database file
- Used manual journal compliance calculation due to known bug in sync script