# session_search Size Limit Workaround

## Problem

When `session_search` results exceed the character limit (~600KB), the tool output is persisted to a temporary file and the session object is returned with only a preview. This makes it impossible to directly read the full session messages to extract review job output.

## Symptom

```
This tool result was too large (596,131 characters, 582.2 KB).
Full output saved to: /var/folders/s7/vr8dmw9n7tn2f0wm_7phmslr0000gn/T/hermes-results/call_-7439109787347839792.txt
```

## Workaround Pattern

### Step 1: Read the persisted file

```python
import pathlib
import tempfile

# Path is provided in the error message
temp_file = "/var/folders/s7/vr8dmw9n7tn2f0wm_7phmslr0000gn/T/hermes-results/call_-7439109787347839792.txt"
```

### Step 2: Parse for counts using regex

The review job's output contains counts in plain text:

```python
import re

with open(temp_file, 'r') as f:
    content = f.read()

# Extract new skills count
skills_match = re.search(r'(?i)(\d+)\s*(?:new skills? recommended|recommended new skills?)', content)
new_skills = int(skills_match.group(1)) if skills_match else 0

# Extract updates count
updates_match = re.search(r'(?i)(\d+)\s*(?:updates? generated|total updates?|updates?)', content)
updates = int(updates_match.group(1)) if updates_match else 0

print(f"New skills: {new_skills}, Updates: {updates}")
```

### Step 3: Validate against targets

```python
TARGET_NEW_SKILLS = 3
TARGET_UPDATES = 5

skills_gap = max(0, TARGET_NEW_SKILLS - new_skills)
updates_gap = max(0, TARGET_UPDATES - updates)

if skills_gap == 0 and updates_gap == 0:
    print("[SILENT]")
else:
    print(f"⚠️ Gap: {skills_gap} new skills, {updates_gap} updates")
```

## Example from Production

**Date:** 2026-07-15  
**Session:** `cron_c37a1090869d_20260714_032501`  
**Persisted file size:** 596,131 characters (582.2 KB)

**Extraction results:**
- `SKILLS_COUNT=3` ✓ (meets target)
- `UPDATES_COUNT=5` ✓ (meets target)
- **Verdict:** `[SILENT]` — no action needed

## Why This Works

The review job (`c37a1090869d`) outputs structured session messages that include:
1. The JSON block with `new_skills_recommended` and `updates_generated`
2. Plain text summaries in natural language

When the full session object is too large to return directly, the persisted JSON file still contains the complete text content. Regex parsing on the raw JSON string reliably extracts the counts without needing to parse the complex nested message structure.

## Fallback Options

If the persisted file approach fails:

1. **Use `session_search` with specific date prefix:**
   ```python
   session_search(
       query="cron_c37a1090869d_20260715",
       sort="newest",
       limit=5
   )
   ```
   This targets the exact session ID and may return a smaller result.

2. **Read the cron output file directly:**
   ```bash
   cat /<workspace>$(date +%Y-%m-%d)_*.md
   ```

## References

- Production session: `cron_c37a1090869d_20260714_032501` — confirmed successful extraction via persisted file parsing
- Related: `references/json-block-extraction.md` — for extracting structured JSON blocks