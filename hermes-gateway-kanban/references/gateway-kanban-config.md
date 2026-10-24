# Gateway Kanban Configuration (from session)

## Active config.yaml kanban section (June 2026)

```yaml
kanban:
  dispatch_in_gateway: true
  dispatch_interval_seconds: 60
  failure_limit: 2
  worker_log_rotate_bytes: 2097152
  worker_log_backup_count: 1
  orchestrator_profile: ''
  default_assignee: ''
  max_in_progress_per_profile: null
  auto_decompose: true
  auto_decompose_per_tick: 3
  dispatch_stale_timeout_seconds: 14400
```

## Key Settings Explained

| Setting | Value | Rationale |
|---|---|---|
| `dispatch_in_gateway` | true | Embedded dispatcher runs in gateway process |
| `dispatch_interval_seconds` | 60 | Poll every minute — responsive enough for Telegram |
| `failure_limit` | 2 | Low limit catches misconfigured tasks fast |
| `auto_decompose` | true | Parent tasks auto-split into subtasks |
| `auto_decompose_per_tick` | 3 | Limit decomposition rate |
| `dispatch_stale_timeout_seconds` | 14400 | 4-hour stale timeout (matches overnight cycles) |

## Verification Commands

```bash
# Check config is loaded
hermes config show | grep -A 15 kanban

# Verify dispatcher running in gateway logs
grep "kanban dispatcher" <agent-home>/logs/gateway.log
# Expected: "kanban dispatcher: embedded in gateway (interval=60.0s)"
```