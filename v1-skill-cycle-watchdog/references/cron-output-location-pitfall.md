# Cron Output Location Pitfall

## Problem

Skills that assume a specific cron output file path (e.g., `/<workspace>`) will fail because:
- The directory does not exist
- The path was never standardized in the operator agent
- Cron job delivery modes (local vs. origin) have different output mechanisms

## Impact on Watchdog Operations

The following methods in `v1-skill-cycle-watchdog` are affected:

1. **Step 2a (Fallback Structural Marker Check)** — References cron output file paths that may not exist
2. **File-Size Anomaly Check** — Assumes output files are written to a known location
3. Any direct file system access to cron output directories

## Corrected Approach

### Do NOT assume cron output file paths

Instead, use the session database as the authoritative source:

```bash
# Verify job ran
hermes cron list | grep "c37a1090869d"

# Find the session via session_search
session_search(
    query="cron_c37a1090869d_20260718",
    sort="newest",
    limit=5
)
```

### Extract counts from session content

When session_search results are persisted to temp files due to size limits, read the persisted file and extract the JSON monitoring block:

```python
import json
import re

# Read the persisted session output (path from session_search error message)
with open('/var/folders/.../hermes-results/call_<hash>.txt', 'r') as f:
    content = f.read()

# Extract JSON block with counts
json_match = re.search(
    r'\{\s*"new_skills_recommended"\s*:\s*\d+.*?"pipeline_status"\s*:\s*"[^"]+".*?\}',
    content,
    re.DOTALL
)

if json_match:
    data = json.loads(json_match.group(0))
    new_skills = data.get("new_skills_recommended", 0)
    updates = data.get("updates_generated", 0)
    status = data.get("pipeline_status", "unknown")
```

## Verification Pattern

Before attempting to read cron output files, verify accessibility:

```bash
# Check if cron output directory exists (expect failure)
test -d /<workspace> || echo "Cron output directory not accessible"

# Correct approach: use session_search instead
hermes cron list  # Verify job status
session_search    # Retrieve output content
```

## Root Cause Analysis

The skill documentation was written with the assumption that the operator agent cron jobs write output to a predictable file system location. This assumption is incorrect for the following reasons:

1. **the operator agent cron delivery modes:**
   - `local` — Output delivered to local session database, not necessarily written to disk files
   - `origin` — Output delivered via operator bus or other delivery mechanism
   - Neither mode guarantees a specific file path

2. **Session database is authoritative:**
   - Cron job output is stored in the the operator agent session database
   - `session_search` is the correct tool for retrieval
   - File system paths are implementation details, not public APIs

3. **Temporary file persistence:**
   - When session_search results exceed size limits, they are persisted to temp files
   - The temp file path is shown in the error message
   - This is a fallback mechanism, not a primary output location

## Corrective Actions

1. **Remove all file system path assumptions** from skill documentation
2. **Update Step 2a** to use session_search instead of direct file access
3. **Update File-Size Anomaly Check** to rely on session metadata rather than file sizes
4. **Document session_search as the primary method** for retrieving cron job output

## Related Skills

- `cron-fleet-audit` — May have similar file path assumptions that need correction
- Any skill that reads cron output files directly — Should be updated to use session_search

## Example of Corrected Workflow

```bash
# 1. Verify job ran
hermes cron list | grep "c37a1090869d"

# 2. Find the session
session_search(
    query="cron_c37a1090869d_$(date +%Y%m%d)",
    sort="newest",
    limit=1
)

# 3. Extract counts from session content
# (If results persisted to temp file, read that file and extract JSON block)
```

## Historical Context

This pitfall was discovered during the 2026-07-18 watchdog cycle when:
- The watchdog attempted to read `/<workspace>`
- The directory did not exist
- The watchdog fell back to session_search, which succeeded
- This revealed that file system paths were the wrong abstraction layer

**Lesson:** Always use the operator agent session tools (session_search, hermes cron list) as the primary interface for cron job output. File system paths are implementation details that should not be relied upon.