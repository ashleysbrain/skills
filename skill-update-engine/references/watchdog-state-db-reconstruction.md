# Watchdog State-DB Reconstruction (when the JSON block is missing)

When a watchdog detects that the engine report did not emit the required §13.1 JSON block (the "JSON block missing" template case), it cannot trust the cron `ok` status and it cannot read the delivered counts from a report. This document is the concrete recipe for reconstructing what the engine **actually shipped** by reading `state.db` directly.

This is the "extract counts by hand" step that §13.2 references but does not detail.

## When to use this

- Cron status shows `ok` but the engine's final assistant message is truncated, empty, or obviously incomplete (e.g., a stray word like `Templates:`).
- No JSON monitoring block is present anywhere in the session.
- The cron output `.md` file at `<agent-home>/cron/output/<job_id>/<date>_<time>.md` ends mid-skill-content or mid-prompt rather than with a clean report.

This is the R16 / §11.1 single-job stall signature. The session hit its token/time budget before emitting the JSON block — but patches may have been applied *before* the stall.

## Recipe

### 1. Resolve the session ID

```bash
sqlite3 <agent-home>/state.db \
  "SELECT DISTINCT session_id FROM messages
   WHERE session_id LIKE 'cron_<job_id>_%'
   ORDER BY session_id DESC LIMIT 1;"
```

The session_id is shaped `cron_<job_id>_<YYYYMMDD>_<HHMMSS>`. Cross-check the timestamp against the `Last run:` field from `hermes cron list`.

> Note: `session_search(query='cron_<job_id>_<date>')` often returns **zero** hits for today's run because the session DB has not been flushed/indexed for FTS yet at watchdog time. Direct `sqlite3` queries against the `messages` table are the reliable path; do not conclude "no session found" from an empty FTS result alone.

### 2. Confirm whether the report completed

Read the **last assistant message** in the session:

```bash
sqlite3 <agent-home>/state.db \
  "SELECT id, length(content), substr(content,1,200)
   FROM messages
   WHERE session_id='<session_id>' AND role='assistant'
   ORDER BY id DESC LIMIT 1;"
```

Classification:
- Content is empty / length ~0 but `tool_calls` is non-empty → agent was mid-tool-call when the session ended (stall).
- Content is a stray fragment (e.g., `Templates:`, a heading with no body) → the final report never assembled (stall).
- Content is a full report with a JSON block → not this case; use the JSON block normally.
- **Content is exactly `[SILENT]` (length ~8) → producer/observer confusion (R17), NOT a stall.** The job finished cleanly with cron `ok` but the engine misidentified itself as an observer and emitted the watchdog suppression marker. Do NOT treat this as "targets met." Continue to step 3 — you will almost always find **zero** write calls, confirming a no-op producer run.

Either stall case ⇒ `shortfall_label: "structural"` regardless of cron `ok`.

### 3. Count what actually shipped

The engine applies patches via the `patch` / `write_file` / `skill_manage` tools. A successful application lands as a `tool`-role message whose JSON payload starts with `{"success": true, "diff":` (for `patch`) or `{"success": true,` (for `write_file`/`skill_manage`).

**Count successful patch applications:**

```bash
sqlite3 <agent-home>/state.db \
  "SELECT COUNT(*) FROM messages
   WHERE session_id='<session_id>' AND role='tool'
     AND content LIKE '{\"success\": true, \"diff\":%';"
```

This is the true `patches_shipped` / delivered-update count — it is often **greater than zero** even when the report never emitted.

**Identify which skill(s) were patched** (from the diff path):

```bash
sqlite3 <agent-home>/state.db \
  "SELECT substr(content,1,120) FROM messages
   WHERE session_id='<session_id>' AND role='tool'
     AND content LIKE '{\"success\": true, \"diff\":%'
   ORDER BY id;"
```

The `diff` header contains `--- a//<workspace><category>/<skill>/…`, which names the patched skill. Group by skill to report per-skill update counts and the total.

### 3a. Tool-call histogram audit (detect R17 producer/observer confusion)

When the final assistant message is `[SILENT]` (the R17 case above), or whenever you suspect the engine did no real work despite a cron `ok`, audit the session's **tool-call histogram**. Count, per function name, every tool call the agent made:

```bash
sqlite3 <agent-home>/state.db \
  "SELECT json_extract(tc.value, '$.function.name') AS fn, COUNT(*) AS n
   FROM messages m, json_each(m.tool_calls) tc
   WHERE m.session_id='<session_id>' AND m.role='assistant'
   GROUP BY fn ORDER BY n DESC;"
```

**Decision rule:** if the histogram contains **only** read-only tools (`read_file`, `search_files`, `terminal` used for `hermes skills check` / usage-stats reads / `cat`) and **zero** of (`skill_manage`, `write_file`, `patch`), the run is a **no-op producer run** regardless of its final text. Classify as `shortfall_label: "structural"` with reason "producer emitted `[SILENT]` / made zero write calls (R17)". Do not report "0 delivered" as if the engine deliberately found nothing — report it as a contract violation that needs a stronger model or a corrected prompt.

This is the signature of the 2026-06-19 failure on `c37a1090869d`: 5×`read_file` + 1×`search_files` + 8×`terminal` (all read-only) + 0 writes → final `[SILENT]`.

### 4. Distinguish update type (optional, for richer reports)

For each applied patch, look at the *preceding* assistant message's `tool_calls` column to get the function name (`patch` vs `write_file` vs `skill_manage`). `patch` with a `path` ending in `SKILL.md` = a core edit; `path` ending under `references/|templates/|scripts/` = a support-file edit. This lets the watchdog classify delivered updates without the engine's own summary.

## How to report the reconstructed result

Use the **§13.2 structural-shortfall template**, but fill the `Delivered` column from the reconstructed counts (step 3) rather than defaulting to 0. State plainly that the JSON block was missing and counts were reconstructed from `state.db`. Example language:

> *Shortfall classification: structural — single-job stall (R16). The engine applied N patches to `<skill>` before the session hit its budget; the required JSON monitoring block was never emitted. Counts reconstructed from `state.db`.*

The corrective action is always the §11.1 recovery protocol: re-run with an explicit "resume from scan, emit JSON block first, skip already-patched skills" prompt.

## Pitfalls

- **Do not default delivered counts to 0** when the JSON block is missing. A stall after patching is common; the watchdog that reports "0 delivered" when 4 patches actually shipped is misleading. Always reconstruct before reporting.
- **Do not rely on the cron-output `.md` file** for counts. That file is a raw dump of the prompt + skill content + tool messages; it is not a curated report and may be truncated. Use `state.db` for authoritative counts.
- **`session_search` FTS may be empty for today's run.** FTS indexing can lag the live `messages` table. If `session_search` returns nothing for today's session id, fall back to the direct `sqlite3` query in step 1 — do not report "no session found" from FTS alone.
