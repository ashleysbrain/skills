# Session Discovery Challenge for Cron Jobs

**Date:** 2026-07-13
**Job ID:** c37a1090869d (Divinity Health V1 Skill Product Review)

## Problem

When validating cron job execution, the expected output file location (`<agent-home>/cron/output/c37a1090869d/`) does not exist. This is a **configuration drift issue** — the cron system output location has changed, but documentation still references the old path.

## Impact

- Watchdog scripts cannot locate job output files
- Status checks fail when looking for expected file paths
- Manual verification requires multiple fallback methods

## Workaround: Multi-Method Detection

Since the output file location is unreliable, use a priority-ordered detection strategy:

### Method 1: the operator agent CLI (Primary)
```bash
hermes cron list | grep "c37a1090869d"
```

**What to look for:**
- `Last run: 2026-07-13T03:27:38.999398-05:00  ok` (today's date)
- `Next run: 2026-07-14T03:25:00-05:00` (scheduled for tomorrow)
- `[active]` status

**Advantages:**
- Most reliable
- Shows both last run status and next scheduled run
- Built-in the operator agent command

**Disadvantages:**
- Requires the operator agent daemon running
- May fail if CLI is unavailable

### Method 2: Session Database Query (Secondary)

Query the sessions database for cron sessions:

```python
import sqlite3
from pathlib import Path
from datetime import datetime

db_path = Path.home() / ".hermes/sessions/sessions.db"
today = datetime.now().strftime("%Y-%m-%d")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Schema varies — try multiple query patterns
queries = [
    # Schema 1: sessions table with created_at
    """
    SELECT session_id, title, created_at
    FROM sessions
    WHERE source = 'cron'
    AND created_at >= ?
    ORDER BY created_at DESC
    LIMIT 10
    """,
    # Schema 2: different column names
    """
    SELECT id as session_id, title, timestamp as created_at
    FROM sessions
    WHERE source = 'cron'
    AND timestamp >= ?
    ORDER BY timestamp DESC
    LIMIT 10
    """
]

for query in queries:
    try:
        cursor.execute(query, (today,))
        results = cursor.fetchall()
        if results:
            break
    except sqlite3.OperationalError:
        continue

# Filter for V1 Skill / Divinity Health sessions
relevant = [r for r in results if any(kw in r[1].lower() for kw in ["v1 skill", "divinity health"])]
```

**Advantages:**
- Works if the operator agent CLI is unavailable
- Can query by date range
- Can filter by job type

**Disadvantages:**
- Schema varies between the operator agent versions
- Requires trial-and-error with query patterns
- May fail if database is locked or corrupted

### Method 3: Directory-Based Session Inspection (Tertiary)

Search session files by modification time:

```bash
# Find session files modified in last 24 hours
find <agent-home>/sessions -type f -name "*.json" -mtime -1
```

Or with Python:

```python
from pathlib import Path
from datetime import datetime, timedelta

sessions_dir = Path.home() / ".hermes/sessions"
cutoff = datetime.now() - timedelta(hours=24)

for session_file in sessions_dir.glob("*.json"):
    stat = session_file.stat()
    mtime = datetime.fromtimestamp(stat.st_mtime)

    if mtime >= cutoff:
        print(f"Found recent session: {session_file.name}")
```

**Advantages:**
- Most robust — no schema dependencies
- Works even if database is corrupted

**Disadvantages:**
- No semantic filtering (job type, source, etc.)
- Requires manual inspection of file contents
- No query capabilities

### Method 4: Use the Automated Script (Recommended)

All three methods are combined in the provided script:

```bash
python3 skills-library/operations/v1-skill-cycle-watchdog/scripts/daily_status_check.py
```

**Exit codes:**
- `0`: Job ran successfully
- `1`: Job did not run
- `2`: Job ran but failed with error
- `3`: Cannot determine status

## Root Cause

The cron output directory structure changed in a recent the operator agent update. The old path:
```
<agent-home>/cron/output/<job_id>/<date>_*.md
```

No longer exists. The new location has not been documented in the watchdog skill.

## Corrective Actions

1. **Immediate:** Use the multi-method detection approach above for status checks
2. **Documentation:** Update watchdog skill to reference primary detection method (the operator agent CLI)
3. **Investigation:** Determine actual cron output location in current the operator agent version
4. **Long-term:** Ensure watchdog scripts adapt to configuration changes without manual updates

## Related Skills

- `v1-skill-cycle-watchdog`: Primary consumer of this workaround
- `cron-fleet-audit`: General cron health checks
- `sibling-agent-fleet-analytics-sync`: Fleet-wide cron job data collection

## Session DB Schema Variations Observed

| Schema Version | Table Name | Timestamp Column | Status |
|----------------|------------|------------------|--------|
| v1 (older) | `sessions` | `created_at` | Working |
| v2 (newer) | `sessions` | `timestamp` | Working |
| v3 (current) | Unknown | Unknown | Unconfirmed |

**Note:** The current schema (2026-07-13) could not be determined — all query patterns failed, suggesting either:
- Schema changed significantly
- Database is in a different location
- Database format changed (not SQLite)

## Test Cases

Run these to validate detection methods:

```bash
# Test Method 1
hermes cron list | grep "c37a1090869d" && echo "CLI method works" || echo "CLI method failed"

# Test Method 2
python3 -c "import sqlite3; conn = sqlite3.connect(str(Path.home()) + '/.hermes/sessions/sessions.db'); cursor = conn.cursor(); cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\"'); print([row[0] for row in cursor.fetchall()])"

# Test Method 3
find <agent-home>/sessions -type f -name "*.json" -mtime -1 | head -5

# Test Method 4 (full script)
python3 skills-library/operations/v1-skill-cycle-watchdog/scripts/daily_status_check.py
```