# Journal Protocol: Database-Only

As per the AGENT JOURNAL PROTOCOL (ENFORCEMENT) effective 2026-03-30, all agent journal entries must be stored in the database table `journal_entries`. Writing `.md` files under `learning-journals/` or `journal/` directories is prohibited.

## Why Database-Only?
- Centralized storage enables querying, analytics, and compliance checks.
- Reduces file sprawl (previously 1,281 .md files across 400+ directories).
- Ensures consistency and prevents lost entries.

## How to Insert a Journal Entry
Use SQL to insert a row into the `journal_entries` table. Required columns:
- `agent_id`: Foreign key to `agents.id`.
- `entry_date`: DATE (use `DATE('now')` for today).
- `file_path`: Optional; can be a descriptive string or left empty.
- `content_hash`: MD5 hash of the entry content (optional but useful for deduplication).
- `word_count`: Number of words in the entry.
- `quality_score`: Self-assessed score from 0 to 10.
- `has_learnings`, `has_gaps`, `has_recommendations`: Boolean flags (0/1).
- `on_time`: Boolean indicating if the entry was made on schedule (usually 1).
- `created_at`: TIMESTAMP defaults to `CURRENT_TIMESTAMP`.

### Example Insertion for FORGE
```sql
INSERT INTO journal_entries (
    agent_id,
    entry_date,
    file_path,
    content_hash,
    word_count,
    quality_score,
    has_learnings,
    has_gaps,
    has_recommendations,
    on_time
) VALUES (
    (SELECT id FROM agents WHERE display_name='DS FORGE' LIMIT 1),
    DATE('now'),
    'FORGE journal entry for 2026-06-10',
    MD5('# FORGE Journal — 2026-06-10\n\n## Talent Request Processing\n- No new talent requests found.\n## Fleet Analytics\n- Updated via sync script.\n## Actions Taken\n- Checked for talent requests.\n- Evaluated existing agents.\n- Updated fleet analytics.\n- Created journal entries.\n- Prepared to git commit changes.'),
    45,
    8.5,
    0,
    0,
    0,
    1
);
```
Adjust values as needed.

## Verification
After insertion, verify with:
```sql
SELECT * FROM journal_entries WHERE agent_id = (SELECT id FROM agents WHERE display_name='DS FORGE') AND entry_date = DATE('now') ORDER BY created_at DESC LIMIT 1;
```

## Note on Existing .md Files
Existing .md files in `learning-journals/` should be left untouched; they are historical. Do not write new ones. If you need to migrate old entries to the DB, that is a separate one-time task.