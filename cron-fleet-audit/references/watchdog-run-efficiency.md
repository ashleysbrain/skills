# Watchdog Run Efficiency

For periodic watchdog cron jobs (e.g., every 4-6h) that monitor the same cycle repeatedly throughout the day. Avoids re-investigating from scratch on each run.

## The Problem

A watchdog that fires every 4-6 hours will run 2-4 times per day against the same target job. If each run independently investigates (cron list → session_search → read prior review output → compare targets), it burns 3-5 tool calls and significant tokens re-discovering what an earlier run in the same day already found.

## The Pattern

### Step 1: Check for prior watchdog runs today first
Before investigating the target job, search for earlier runs of YOUR OWN watchdog job from today:

```
session_search(query="<target job name or ID> watchdog", sort="newest", limit=3)
```

If a prior session from today exists, read it:
```
session_search(session_id="<prior_watchdog_session_id>")
```

### Step 2: Determine delta since last run
Compare the target job's `Last run` timestamp and status against what the prior watchdog found:
- **Last run unchanged** → the target job has not run since the last watchdog check. No need to re-inspect its output. Skip to step 3.
- **Last run updated** → a new run occurred. Inspect the new session output for target compliance.

### Step 3: Decide output class
| Situation | Output |
|---|---|
| Target ran and met targets since last check | `[SILENT]` (nothing new to report) |
| Target ran but missed targets | Concise drift alert with the NEW gap only |
| Target hasn't run since last check + day not ending | `[SILENT]` (already reported, no change) |
| Target hasn't run + day is ending + gap unresolved | **Escalation**: short "status unchanged, day closing" with cumulative totals and a next corrective action |

### Step 4: Track cumulative gaps
When escalation is needed, report cumulative gaps across all runs in the day, not just the current snapshot:

```
Target (2 days): 6 new skills, 10 updates
Actual:          0 new skills, 1 update
```

This gives the user the full picture of how far behind the cycle has fallen.

## Key Rules
- **Never re-investigate a target whose `Last run` timestamp hasn't changed** since the prior watchdog session. The output will be identical.
- **Cumulative gap tables** are more useful than per-run snapshots — show the total deficit against the multi-day target.
- **Escalations should include a concrete next action** (e.g., "trigger manual run of `<job_id>` tonight with instruction to produce N outputs").
- **When the day is closing and the gap is unresolved**, that's the highest-value time to escalate — the auto-schedule has already rolled to tomorrow, so without manual intervention the cycle will be another day behind.

## Pitfall: `hermes cron` Has Limited Subcommands — No JSON, No Output, No Info
The `hermes cron` CLI has exactly these subcommands: `list`, `create`, `edit`, `pause`, `resume`, `run`, `remove`, `status`, `tick`. The following do NOT exist and will waste a turn returning empty/error:
- **No `--json` flag** on `list` — output is formatted text only. Parsing requires text extraction, not JSON deserialization. `hermes cron list --json` returns exit code 2 with empty output.
- **No `output <id>`** — to inspect a job's last-run output, use `session_search(query="<distinctive output terms>")` and read the session transcript. Do not search by job name (see self-noise pitfall below).
- **No `info <id>`** — job details come from `hermes cron list` text parsing or direct `<agent-home>/cron/jobs.json` file reads.
- **No `history <id>`** — historical run data lives in `<agent-home>/state.db` (SQLite). Query it directly via `terminal` python3.
- **No `log` subcommand** — see above, same as `output`.

An agent that assumes "cron has `list`, so it should have `log`/`info`/`output`" will waste multiple turns on trial-and-error. To inspect a job's last-run output, use `session_search(query="<distinctive output terms>")` and read the session transcript — that is the canonical path for cron output inspection.

## Cron-Mode Tool Constraint
In cron execution mode, `execute_code` is blocked by the approval system. Use `terminal` directly for shell commands and `session_search` for session inspection. Do not attempt to wrap these in `execute_code`.

## Pitfall: session_search Discover-Mode Returns Watchdog Self-Noise
When a watchdog inspects its target job via `session_search` in **discover mode** (`query="..."`), searching by the target job's **name or ID** returns the **watchdog's own sessions**, not the target job's. This is because the watchdog prompt contains the target job's name/ID verbatim, so FTS5 matches the watchdog transcripts first. Observed Jun 25: two discover calls querying `"Divinity Health V1 Skill Product Review"` surfaced only prior watchdog runs (`cron_31e90033684f_*`), never the target review session (`cron_c37a1090869d_*`).

**Fix — search by distinctive CONTENT terms, not the job name.** Use tokens that appear in the target job's *output* but NOT in the watchdog prompt:
- A skill the target loads (e.g. `"skill-update-engine"`)
- A JSON field name from the target's output contract (e.g. `"new_skills_recommended"`, `"updates_generated"`)
- A distinctive output phrase

Once the target `session_id` (format `cron_<job_id>_<YYYYMMDD>_<HHMMSS>`) surfaces, switch to **read/scroll mode**: `session_search(session_id="cron_<id>_<date>_<time>")`.

**Shortcut — the discover snippet is often enough.** The FTS5-highlighted `snippet` field in a discover hit frequently contains the target's JSON summary block already. For pass/fail watchdog judgments (target met vs. target missed), read the snippet first; only open the full (often >100KB) session transcript if the snippet is ambiguous.

**Even better for batch audits:** `hermes sessions list --source cron --limit 30` maps job_id → session_id directly by ID segment, bypassing FTS5 entirely. Prefer this when available (see `references/stalled-job-detection.md` → Interactive Detection Recipe).
