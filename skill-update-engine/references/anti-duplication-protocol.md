# Anti-Duplication Protocol

This reference defines the concrete dedup algorithm for the skill update engine.

## Source Hash Computation

```python
import hashlib, json

def compute_source_hash(candidate: dict) -> str:
    """Compute a deterministic hash for deduplication."""
    normalized = json.dumps({
        "skill_id": candidate["skill_id"].strip().lower(),
        "change_type": candidate["change_type"].strip().lower(),
        "summary": " ".join(candidate["summary"].strip().lower().split())  # normalize whitespace
    }, sort_keys=True)
    return hashlib.sha256(normalized.encode()).hexdigest()
```

## Dedup Decision Tree

```
For each candidate:
  1. Compute source_hash
  2. Look up source_hash in applied-updates.jsonl
     - EXACT MATCH → SKIP (already applied)
  3. Look up (skill_id + change_type) in last 7 days of applied-updates.jsonl
     - SEMANTIC MATCH → MERGE (append to existing entry, do not create new patch)
  4. Check patches applied to this skill today
     - SAME CHANGE_TYPE today → SKIP (one patch per type per day)
  5. No match → NEW CANDIDATE (proceed to patch generation)
```

## Monthly Compaction

On the 1st of each month:
1. Copy entries older than 90 days to `applied-updates-archive-YYYY-MM.jsonl.gz`
2. Delete those entries from the hot file
3. Keep last 30 days hot for fast lookup

## Merge Rules

When merging a new candidate into an existing entry:
- Keep the earlier date
- Append the new summary to the existing summary (semicolon-separated)
- Update the confidence to `max(existing, new)`
- Update the impact to `max(existing, new)` by severity order: trivial < low < medium < high
- Increment a `merge_count` field on the entry
