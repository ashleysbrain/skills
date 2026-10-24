# the operator agent Cron List Output Format

The `hermes cron list` command outputs a formatted table of scheduled jobs. Understanding this format is key to parsing the output programmatically.

## General Structure

The output consists of:
1. A header and footer made of dashes and pipes
2. One or more job entries, each spanning multiple lines
3. Each job entry has a consistent structure

## Job Entry Format

Each job entry follows this pattern:

```
  [JOB_ID] [STATE]
    Name:      [JOB NAME]
    Schedule:  [CRON EXPRESSION]
    Repeat:    [REPEAT COUNT]
    Next run:  [NEXT RUN TIMESTAMP]
    Deliver:   [DELIVERY METHOD]
    [OPTIONAL FIELDS...]
    Last run:  [TIMESTAMP]  [STATUS]
```

### Field Details

- **JOB_ID**: Unique identifier for the job (e.g., `63f5bb919948`)
- **STATE**: Either `active` or `paused` in brackets (e.g., `[active]`)
- **JOB NAME**: Descriptive name of the job
- **CRON EXPRESSION**: Standard cron schedule (e.g., `0 */6 * * *`)
- **REPEAT COUNT**: 
  - `∞` for recurring jobs
  - `0/1` for one-shot jobs that have run
  - (blank or other format for one-shot jobs that haven't run yet)
- **NEXT RUN TIMESTAMP**: ISO 8601 timestamp with timezone (e.g., `2026-06-11T00:20:00-05:00`)
- **DELIVERY METHOD**: Either `local` or `origin`
- **OPTIONAL FIELDS** (may be absent):
  - `Skills:` - comma-separated list of skill names
  - `Workdir:` - working directory for the job
  - `Script:` - script name (for script-based jobs)
  - `Mode:` - execution mode (e.g., `no-agent`)
- **LAST RUN**:
  - Timestamp: ISO 8601 format (same as next run)
  - Status: Either `ok` or an error message prefixed with `error:`

## Example Entries

### Active Recurring Job
```
  63f5bb919948 [active]
    Name:      VITALS: Fleet Health Check (Every 6 Hours)
    Schedule:  20 */6 * * *
    Repeat:    ∞
    Next run:  2026-06-11T00:20:00-05:00
    Deliver:   local
    Last run:  2026-06-10T17:40:50.828774-05:00  ok
```

### Active Job with Skills and Workdir
```
  6730968ad57e [active]
    Name:      principal Advisory Board — AM Review
    Schedule:  15 4 * * *
    Repeat:    ∞
    Next run:  2026-06-11T04:15:00-05:00
    Deliver:   origin
    Workdir:   /<workspace>
    Last run:  2026-06-10T09:43:58.197693-05:00  ok
```

### One-Shot Job (Has Run)
```
  ac5860cdf854 [active]
    Name:      GitHub Maintenance Agent (Weekly Sunday 10 PM)
    Schedule:  0 22 * * 0
    Repeat:    0/1
    Next run:  2026-06-14T22:00:00-05:00
    Deliver:   origin
    Workdir:   /<workspace>
```

### Erroring Job
```
  633b60897fc9 [active]
    Name:      the specialist engine Build
    Schedule:  0 0 * * *
    Repeat:    ∞
    Next run:  2026-06-11T00:00:00-05:00
    Deliver:   origin
    Skills:    overnight-implementation-discipline, test-driven-development
    Last run:  2026-06-10T15:11:15.930703-05:00  error: RuntimeError: [truncated]
```

## Parsing Considerations

1. **Indentation**: Job entries are indented with 2 spaces. Field lines are indented with 6 spaces.
2. **Multi-line Values**: Some fields (like job names or error messages) may span multiple lines if they're long.
3. **Missing Fields**: Optional fields (Skills, Workdir, Script, Mode) may be absent entirely.
4. **Blank Values**: Some fields may appear blank if not applicable (e.g., empty Workdir).
5. **Timestamp Format**: All timestamps include timezone offset (e.g., `-05:00` for EST).
6. **Error Truncation**: Error messages in the "Last run" line may be truncated if too long.

## jobs.json Raw File Structure

When parsing `<agent-home>/cron/jobs.json` directly (bypassing `hermes cron list`), the file is a JSON **object** (not a flat list):

```json
{
  "jobs": [ ... ],
  "updated_at": "2026-06-25T12:00:00-05:00"
}
```

**Pitfall:** If you assume `json.load(f)` returns a list and iterate directly, you get `AttributeError: 'str' object has no attribute 'get'` because iterating a dict yields its keys. **Always access `data["jobs"]` first.**

Each job object in the array contains:
- `id`: string (e.g., `"c37a1090869d"`)
- `name`: string
- `prompt`: string (can be very long — the full agent prompt)
- `schedule`: object with `kind`, `expr`, `display`
- `repeat`: object with `times` (null for recurring) and `completed` (int)
- `enabled`: boolean
- `state`: `"scheduled"` | `"paused"` | etc.
- `last_run_at`, `next_run_at`: ISO 8601 timestamps
- `last_status`: `"ok"` | `"error"` | null
- `deliver`: `"local"` | `"origin"`
- `origin`: object with `platform`, `chat_id`, `chat_name`, `thread_id`
- `skills`: list of skill names
- `model`, `provider`, `script`, `no_agent`, `workdir`, `profile`: optional fields

## Cron Output File Location

Run output for a completed cron job is stored at:
```
<agent-home>/cron/output/<job_id>/<YYYY-MM-DD_HH-MM-SS>.md
```

Example: `<agent-home>/cron/output/c37a1090869d/2026-06-25_03-28-03.md`

The output file contains: the full prompt (including loaded skill content), tool calls, and the final response. To find the actual report, search for the job's report heading (grep for `^##` lines near the end — the last `##` heading is typically the report).

## Terminal Security: Pipe-to-Interpreter Blocked

The the operator agent terminal security scanner blocks commands that pipe file content directly into an interpreter:

```
# BLOCKED — "Pipe to interpreter: cat | python3"
cat jobs.json | python3 -c "import json, sys; ..."

# ALLOWED — standalone python3 reads the file itself
python3 -c "import json; data = json.load(open('jobs.json')); ..."
```

**Detection:** You get an approval prompt with `[HIGH] Pipe to interpreter: cat | python3: Command pipes output from 'cat' directly to interpreter 'python3'.` If approved, it still works — but auto-approval won't fire and the command stalls. **Fix:** Rewrite as standalone python3 that opens files directly with `open()`.

## Recommended Parsing Approach

1. Split the output by double newlines (`\n\n`) to separate job entries
2. Skip entries that don't start with a job ID pattern
3. For each entry, split by newlines and process each line:
   - First line: extract job ID and state
   - Subsequent lines: parse based on the prefix (Name:, Schedule:, etc.)
   - Handle continuation lines for multi-valued fields
4. Convert timestamps to datetime objects for easier comparison
5. Handle missing fields gracefully by setting them to None or appropriate defaults