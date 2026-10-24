# Sessions Table Schema

This is the expected schema for the `sessions` table in the the operator agent Agent database.

```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL UNIQUE,
    user_id TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    data TEXT  -- JSON blob or similar
);
```

Note: The actual schema may vary. Please refer to the the operator agent Agent source code or documentation for the exact definition.