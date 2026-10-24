# Session Learnings — 2026-06-11

## Key Findings

### The `report` subcommand replaces manual DB queries
Running `python3 fleet_analytics.py report` after sync produces a complete, formatted fleet health report:
- Agent count with persona listing (40 personas across AISHA, COSMOS, DSWAVE, FORGE families)
- Status distribution (enabled/error/disabled)
- Top errors ranked by consecutive failure count with job names and error types
- Model distribution with exact job counts
- Journal compliance
- Fleet TWC score
- Daily productivity (last 3 days)

No need to query `analytics.db` manually for standard sync reports. The report subcommand does a re-sync internally (~5s overhead) but gives everything in one shot.

### analytics.db state after sync
- `cron_jobs` table: **0 rows** despite sync succeeding (exit 0, "Synced 124 cron jobs")
- `fleet_health_snapshots`: **0 rows** despite "Snapshot saved" message
- `journal_entries`: **0 rows** despite "Indexed 1710 journal entries"
- `cron_runs`: 0 rows
- `error_log`: 0 rows

The sync reports to stdout. The DB tables remain empty. This has been the case since at least June 9.

### Error landscape shift
- **All errors are now timeouts.** 656 timeout errors in 24h, 0 rate-limit, 0 auth errors.
- Previous error types (auth_permanent seen June 9 at 40 occurrences) have dropped to zero.
- Top erroring jobs: SINGULARITY Always-On Strategic Pulse (12x), hydra-hourly-dispatcher (9x), various scan jobs (5x each).

### Fleet composition
- 91 total agents, 87 active, 4 inactive
- 40 registered personas across 4 families (AISHA V1-V10, COSMOS V1-V10, DSWAVE V1-V10, FORGE V1-V10)
- All models are free-tier OpenRouter:
  - meta-llama/llama-3.3-70b-instruct:free (79 jobs)
  - z-ai/glm-4.5-air:free (61 jobs)
  - nvidia/nemotron-3-super-120b-a12b:free (56 jobs)
  - qwen/qwen3-next-80b-a3b-instruct:free (34 jobs)
  - qwen/qwen3-coder:free (27 jobs)
  - openai/gpt-oss-120b:free (27 jobs)
  - nvidia/nemotron-3-nano-30b-a3b:free (23 jobs)

### Daily productivity (from report)
- 2026-06-11: 0 completed, 0 failed, 51 sessions, 2 commits, 1 agent active
- 2026-06-10: 0 completed, 0 failed, 51 sessions, 4 commits, 2 agents active
- 2026-06-09: 0 completed, 0 failed, 51 sessions, 2 commits, 1 agent active

### Schema notes (analytics.db)
If you do need to query the DB directly:
- `cron_jobs` table uses `job_name` (not `name`) and `job_id` (not `id`) for external references
- `fleet_health_snapshots` has a `details` JSON text field that can contain rich data (top_errors, model_distribution, status_distribution) when snapshots are actually persisted
- `journal_entries` uses `entry_date` (not `timestamp`) for date filtering
- `error_log` uses `occurred_at` (not `timestamp`) for time filtering
