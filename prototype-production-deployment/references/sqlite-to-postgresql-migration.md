# SQLite to PostgreSQL Migration Pattern

## When to Use
When migrating a single-user SQLite-backed app to multi-user PostgreSQL.
The existing data needs to be preserved and assigned to the admin user.

## Approach

1. **Read all existing SQLite databases** using the standard `sqlite3` module
2. **Map each table to a SQLAlchemy model** with a `user_id` foreign key
3. **Write to the new database** (PostgreSQL in production, SQLite in dev)
4. **Support `--dry-run`** to verify row counts before committing

## Migration Script Structure

```python
# Key patterns from the migration script:

def _parse_dt(val):
    """Parse various datetime formats into UTC datetime.
    SQLite stores timestamps as strings in inconsistent formats."""
    for fmt in ["%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S.%fZ", ...]:
        try:
            return datetime.strptime(str(val), fmt).replace(tzinfo=timezone.utc)
        except (ValueError, TypeError):
            continue
    return datetime.now(timezone.utc)

def _safe_json(val, default=None):
    """SQLite stores JSON as TEXT; PostgreSQL uses JSON columns."""
    if isinstance(val, (list, dict)):
        return val
    try:
        return json.loads(val)
    except (json.JSONDecodeError, TypeError):
        return default

# Assign all existing data to the admin user
admin_id = admin.id  # found or created at the start

# Shared tables (papers, search_queries) have NO user_id
# User-scoped tables (drafts, runs, publications) get admin_id
```

## Pre-Migration Checklist

1. Count rows in every SQLite table:
   ```bash
   for t in $(sqlite3 <db>.db ".tables" | tr ' ' '\n' | grep -v sqlite_sequence); do
       echo "  $t: $(sqlite3 <db>.db "SELECT count(*) FROM $t") rows"
   done
   ```

2. Run migration in dry-run mode:
   ```bash
   DATABASE_URL="sqlite+aiosqlite:///tmp/test.db" \
   WORKSPACE="/path/to/workspace" \
   python3 migrate_sqlite_to_pg.py --dry-run
   ```

3. Verify dry-run row counts match the source counts.

4. Run for real:
   ```bash
   DATABASE_URL="postgresql+psycopg2://user:pass@host:5432/db" \
   WORKSPACE="/path/to/workspace" \
   ADMIN_EMAIL="<org-email>" \
   python3 migrate_sqlite_to_pg.py
   ```

## Gotchas

- **SQLite read-only mounts**: Docker `:ro` volume mounts block SQLite from
  creating WAL files. Mount as read-write for the migration container.
- **Email validation**: Pydantic `EmailStr` rejects `.local` TLDs. Use
  `.com` or `.example.com` for test data.
- **ID truncation**: SQLAlchemy model IDs are 12 chars (`uuid.uuid4().hex[:12]`).
  Ensure existing IDs fit or truncate consistently.
- **Datetime parsing**: SQLite stores timestamps inconsistently (ISO format,
  space-separated, with/without timezone). The `_parse_dt` function handles
  the common variants but may need extension for edge cases.
