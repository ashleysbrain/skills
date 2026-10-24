# Ledger minting pitfalls (observed live 2026-08-20)

## 1. AUTO-mint ID collisions

The gap-hunter / auto-minters consume task IDs continuously. Mints at
guessed IDs collide with `UNIQUE constraint failed: tasks.id` — and the
collision surfaces on a HALF-APPLIED batch (task row inserted, event row
not, because the exception fires mid-loop).

Before minting:
```sql
SELECT MAX(CAST(SUBSTR(id,10) AS INTEGER)) FROM tasks WHERE id LIKE 'T-260820-0%';
```
Mint at MAX+1. After any constraint error, backfill missing events:
```sql
SELECT task_id, COUNT(*) FROM task_events WHERE task_id IN (...) GROUP BY task_id;
-- any task with 0 events needs its 'minted' event inserted
```

## 2. task_events is append-ONLY (Flow 3 history law)

A DB trigger raises ABORT on UPDATE/DELETE. Fixing a malformed task ID:
1. `UPDATE tasks SET state='cancelled', outcome='re-minted as <new>' WHERE id=<bad>`
2. INSERT the corrected task
3. Append events on BOTH ids (cancel event on old, mint event on new)
Never rewrite event rows.

## 3. tasks.state CHECK enum

`open/claimed/done/blocked/cancelled` only. There is NO 'in_progress' —
use 'claimed' for active work. CHECK fires on anything else.

## 4. Schema drift across DBs

research-library.db and task-ledger.db have DIFFERENT schemas:
- findings: `title` + `body` (NOT `claim`); sources: `credibility_weight`
  (NOT `credibility`), `created_at` (NOT `added_date`)
- tasks: `state` (NOT `status`), `severity` INTEGER 1-4
Read `.schema <table>` before the first INSERT in any session; never carry
column names across databases.

## 5. f-string ID formatting

`f'T-260820-01{n}'` with n=109 mints `T-260820-01109` (5-digit suffix —
wrong format). Zero-pad explicitly: `f'T-260820-{n:04d}'`. Check string
length before INSERT.
