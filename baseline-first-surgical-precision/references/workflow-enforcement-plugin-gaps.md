# Workflow Enforcement Plugin — Documented Gaps

Plugin: `workflow_enforcement` v0.1.0
Location: `<agent-home>/plugins/workflow_enforcement/__init__.py`

These gaps were observed in production during the 2026-06-06 through 2026-06-08 window and documented in the weekly review at `<agent-home>/state/workflow-enforcement-events.jsonl` (5,479 events, 62 blocked calls, 216 sessions).

---

## Gap 1: Baseline-miss false positive on new file creation

### Symptom

`write_file` is blocked with the message:

> "Baseline-first gate blocked a new file write to [path]. This turn looks like an edit to an existing artifact."

...even though the target file **does not exist on disk** and the task is genuinely to create a new deliverable.

### Cause

The `pre_tool_call` hook in `__init__.py` (line ~353) checks:

```python
if tool_name == "write_file" and intent.get("is_existing_edit") and not Path(path_value).exists():
    _bump_metric("blocked_baseline_misses")
    return {"action": "block", "message": ...}
```

The `is_existing_edit` flag is set by `pre_llm_call` → `_decompose_message()`, which looks for edit verbs ("edit", "update", "patch", "fix", "tweak", "revise", etc.) combined with edit hints ("existing", "current", "already", "same", "baseline", "surgical", etc.).

Cron job prompts commonly use edit-like language ("update the weekly review", "review and update the report") even when the target file may not exist yet. The intent classifier correctly identifies the turn as edit-like, but the baseline-miss gate doesn't distinguish between:

- **True positive**: Agent is editing an existing artifact but accidentally targets a new path → block is correct
- **False positive**: Agent is creating a genuinely new deliverable described in edit-like language → block is wrong

### Workaround

Before writing a new deliverable that gets blocked by this gate:

1. Verify the target path does NOT exist on disk (`search_files` or `read_file` to confirm)
2. If it genuinely doesn't exist, clear the stale intent by writing `<agent-home>/.session-state.json`:
   ```json
   {
     "intent": {"is_existing_edit": false, "objective": "Create new deliverable"},
     "active_artifact": {"path": null, "group": null, "locked": false, "last_touched_at": null}
   }
   ```
3. Retry the `write_file` call

### Recommended plugin fix

Add a group-novelty check to the baseline-miss gate. Only fire if the session has previously touched an artifact in the same group:

```python
# Before the baseline-miss block:
current_group = _artifact_group(path_value)
history_groups = {_artifact_group(p) for p in state.get("artifact_history", []) if p}
if tool_name == "write_file" and intent.get("is_existing_edit") and not Path(path_value).exists():
    if current_group in history_groups:
        # Session has touched this artifact group before — likely a variant-path drift
        _bump_metric("blocked_baseline_misses")
        return {"action": "block", "message": ...}
    else:
        # Novel group — probably a new deliverable, not a baseline miss
        return None  # allow
```

---

## Gap 2: Stale artifact lock with no TTL

### Symptom

Agent makes multiple consecutive blocked `write_file` attempts (6+ observed) on different files in the same session, even after the original task completed. Eventually the agent tries an unrelated test file which is also blocked.

### Observed instances

- **Session `20260606_154848_4bb644`** (2026-06-06): 6 blocked writes to `09-HOLISTIC-multi-dimensional-competitors.md` and variants, then blocked on `/<workspace>`. Agent was unable to produce output.
- **Session `20260606_093444_137706`** (2026-06-06): Agent had to manually patch `.session-state.json` to clear a stale lock before proceeding.
- **Session `cron_29cfc6c6aeba_20260608_100032`** (2026-06-08): Cron job blocked from creating `workflow-rails-weekly-review-latest.md` (new file) due to stale intent flags from cron prompt decomposition.

### Cause

The `active_artifact` lock in session state has no expiry mechanism. Once set by `_update_active_artifact()`, it persists until:

1. A new artifact overwrites it (via another successful write to a different path)
2. The session ends and a new session starts (which resets the state via `on_session_start`)
3. The agent manually patches `.session-state.json`

In long sessions (especially cron jobs that run multiple analysis phases), the lock can outlive its usefulness by hours.

### Recommended plugin fix

Add a TTL constant and expiry check in `pre_tool_call`:

```python
LOCK_TTL_SECONDS = 1800  # 30 minutes

# In pre_tool_call, before comparing artifact groups:
active_touched = active.get("last_touched_at")
if active_touched:
    elapsed = (datetime.now(timezone.utc) - datetime.fromisoformat(active_touched)).total_seconds()
    if elapsed > LOCK_TTL_SECONDS:
        # Lock expired — clear it and allow the write
        state["active_artifact"] = {
            "path": None, "group": None,
            "locked": False, "last_touched_at": None
        }
        _write_json(STATE_PATH, state)
        return None  # allow the tool call
```

This is self-contained within the plugin — no the operator agent core changes required.

---

## Gap 3: Event log unbounded growth

### Symptom

The event log file at `<agent-home>/state/workflow-enforcement-events.jsonl` grows without bound. As of 2026-06-08 it contains 5,479 lines (~1 MB).

### Recommended fix

Add rotation in `_append_event()`:

```python
MAX_EVENT_LOG_BYTES = 5 * 1024 * 1024  # 5 MB

def _append_event(event):
    try:
        _ensure_parent(EVENT_LOG_PATH)
        if EVENT_LOG_PATH.exists() and EVENT_LOG_PATH.stat().st_size > MAX_EVENT_LOG_BYTES:
            backup = EVENT_LOG_PATH.with_suffix(".jsonl.1")
            if backup.exists():
                backup.unlink()
            EVENT_LOG_PATH.rename(backup)
        with EVENT_LOG_PATH.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, sort_keys=True) + "\n")
    except Exception:
        logger.warning("workflow_enforcement: failed appending event log", exc_info=True)
```

---

## Metrics reset behavior

The metrics file at `<agent-home>/state/workflow-enforcement-metrics.json` is reset to zero values by `on_session_start` every time a new session begins. This means cumulative counters (turns, tool_calls, blocked_variant_writes, etc.) only reflect activity since the most recent session start, not the full history. For weekly reviews, rely on the event log for complete data and treat the metrics file as a current-session snapshot.

---

## Session state schema quick reference

```json
{
  "schema_version": "workflow_enforcement.v1",
  "session": {"id": "", "started_at": ""},
  "policy": {
    "patch_before_rewrite": true,
    "one_artifact_per_deliverable": true,
    "decompose_before_edit": true,
    "absorb_low_signal_corrections": true,
    "preserve_context_over_thrift": true
  },
  "active_artifact": {
    "path": null,
    "group": null,
    "locked": false,
    "last_touched_at": null
  },
  "intent": {
    "is_existing_edit": false,
    "objective": ""
  },
  "instruction_decomposition": {
    "required": false,
    "source_excerpt": "",
    "buckets": {
      "hard_constraints": [],
      "required_operations": [],
      "low_signal_corrections": []
    }
  },
  "tool_log": {
    "counts": {},
    "last_write_path": null,
    "last_tool": null
  }
}
```

Key fields for workaround purposes:
- `intent.is_existing_edit` — clear to `false` if blocked on a genuinely new file
- `active_artifact.path` / `active_artifact.group` — clear to `null` if lock is stale
- `active_artifact.locked` — clear to `false` to release lock
