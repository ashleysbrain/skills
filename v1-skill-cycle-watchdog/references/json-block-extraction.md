# JSON Block Extraction from Cron Outputs

## Challenge

The review job's output file contains a JSON monitoring block (Section 13.1 contract) that watchdogs need to parse. However:
- Output files are large (140KB+ in the V1 review job's case)
- The JSON block is embedded in markdown with backticks
- Simple `grep -A 10` or `grep -B 10` approaches may miss the full JSON if it spans more than 10 lines
- Multiple JSON blocks may exist in the file (the skill documentation contains examples)

## Robust Extraction Method

### Method 1: Python Regex with Context

This is the most reliable approach — find the markdown JSON block, extract the content between the backticks, and parse it:

```python
import json
import re
from pathlib import Path
from datetime import date

# Locate today's output file
output_dir = Path.home() / ".hermes/cron/output/c37a1090869d"
today_files = list(output_dir.glob(f"{date.today():%Y-%m-%d}_*.md"))

if not today_files:
    print("ERROR: No output file found for today")
    exit(1)

output_file = today_files[0]
content = output_file.read_text()

# Extract JSON block using regex (Section 13.1 format)
# Pattern: ```json\n{...}\n``` (with possible newlines and indentation)
json_match = re.search(
    r'```json\s*({[^`]+})\s*```',
    content,
    re.DOTALL
)

if not json_match:
    print("ERROR: No JSON monitoring block found")
    exit(1)

try:
    data = json.loads(json_match.group(1))
    
    # Extract metrics
    new_skills = data.get("new_skills_recommended", 0)
    updates = data.get("updates_generated", 0)
    status = data.get("pipeline_status", "unknown")
    shortfall_label = data.get("shortfall_label", "structural")
    shortfall_reason = data.get("shortfall_reason", "")
    target_profile = data.get("target_profile", "unknown")
    candidates_unique = data.get("candidates_unique", 0)
    patches_shipped = data.get("patches_shipped", 0)
    
    print(f"Target profile: {target_profile}")
    print(f"Pipeline status: {status}")
    print(f"New skills recommended: {new_skills}")
    print(f"Updates generated: {updates}")
    print(f"Candidates unique: {candidates_unique}")
    print(f"Patches shipped: {patches_shipped}")
    print(f"Shortfall label: {shortfall_label}")
    if shortfall_reason:
        print(f"Shortfall reason: {shortfall_reason}")
        
except json.JSONDecodeError as e:
    print(f"ERROR: Failed to parse JSON block: {e}")
    exit(1)
```

### Method 2: jq for JSON Files

If the JSON block is extracted to a separate file first:

```bash
# Extract JSON block to a temp file
sed -n '/^```json$/,/^```$/p' /<workspace>$(date +%Y-%m-%d)_*.md | sed '1d;$d' > /tmp/metrics.json

# Parse with jq
jq '.new_skills_recommended, .updates_generated, .pipeline_status, .shortfall_label' /tmp/metrics.json
```

### Method 3: grep with Extended Context

If the JSON block is known to be within a certain line count window:

```bash
# Extract with 50 lines of context (adjust based on actual block size)
grep -A 50 '"new_skills_recommended"' /<workspace>$(date +%Y-%m-%d)_*.md | head -60
```

**Warning:** This approach is fragile — if the JSON block size changes or the spacing varies, it will truncate or include irrelevant content.

## Validating the Extracted JSON

After extraction, verify the JSON contains the required fields per Section 13.1:

```python
required_fields = [
    "new_skills_recommended",
    "updates_generated",
    "target_profile",
    "pipeline_status",
    "candidates_unique",
    "patches_shipped"
]

missing = [f for f in required_fields if f not in data]
if missing:
    print(f"ERROR: JSON block missing required fields: {', '.join(missing)}")
    # If shortfall_label is also missing, this is a structural failure
    if "shortfall_label" not in data:
        print("ERROR: shortfall_label field also missing — cannot classify gap")
    exit(1)
```

## Edge Cases

### Multiple JSON Blocks in File

The skill documentation itself contains example JSON blocks (see skill-update-engine §13.1). The watchdog must:
1. Search for the **last** JSON block in the file (the actual engine report, not the examples)
2. Verify the block appears after the response section marker
3. Or parse all blocks and use the one with `pipeline_status` field (example blocks may not have this)

```python
# Extract all JSON blocks and filter for the real report
json_blocks = re.findall(r'```json\s*({[^`]+})\s*```', content, re.DOTALL)

for block_str in json_blocks:
    try:
        data = json.loads(block_str)
        # The real report will have pipeline_status
        if "pipeline_status" in data:
            # This is the engine report, not an example
            json_match = type('obj', (object,), {'group': lambda i, n=1: block_str})
            break
    except json.JSONDecodeError:
        continue
```

### Indented or Multiline JSON

The regex pattern `{[^`]+}` captures everything between the opening `{` and the closing `}` as long as no backticks appear in between. This handles:
- Multiline JSON with indentation
- Nested JSON objects
- Arrays and complex structures

However, if a backtick character appears **inside** the JSON string values, the pattern will truncate early. This is rare in Section 13.1 blocks but possible.

## Integrating into the Daily Status Check Script

Update `scripts/daily_status_check.py` to use the Python extraction method instead of shell-based grep:

```python
def extract_metrics(output_file):
    """Extract metrics from the JSON monitoring block in a cron output file."""
    content = output_file.read_text()
    
    json_match = re.search(r'```json\s*({[^`]+})\s*```', content, re.DOTALL)
    
    if not json_match:
        return None
    
    try:
        return json.loads(json_match.group(1))
    except json.JSONDecodeError:
        return None

# In the main validation function:
metrics = extract_metrics(today_file)

if not metrics:
    print("ERROR: No valid JSON monitoring block found")
    return 3  # Cannot determine status

# Extract and validate fields
new_skills = metrics.get("new_skills_recommended", 0)
updates = metrics.get("updates_generated", 0)
status = metrics.get("pipeline_status", "unknown")
shortfall_label = metrics.get("shortfall_label", "structural")

# Route based on shortfall_label
if shortfall_label == "philosophical" and status == "nominal":
    print("OK: Philosophical shortfall — family is coherent and complete")
    return 0  # No alert needed
elif shortfall_label == "structural" or status != "nominal":
    print("ALERT: Structural shortfall or pipeline issue")
    # Calculate gaps and report
    return 1  # Gap detected
```

## Reference

- skill-update-engine §13.1: Required JSON block format and fields
- skill-update-engine §R15 and §13.2: Shortfall classification and routing rules
- skill-update-engine §13.1 pitfall: session_search exceeds size limits → prefer direct file access