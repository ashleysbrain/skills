# Gateway Kanban Dispatcher Log Patterns (from session)

## Expected Log Patterns

### Startup (Success)
```
2026-06-14 06:20:10,338 INFO gateway.run: kanban dispatcher: embedded in gateway (interval=60.0s)
2026-06-14 06:20:10,338 INFO gateway.run: Gateway running with 2 platform(s)
```

### Normal Operation (Polling)
```
2026-06-14 06:21:10,338 INFO gateway.kanban: dispatcher: polling board...
2026-06-14 06:21:10,340 INFO gateway.kanban: dispatcher: no ready tasks
# OR
2026-06-14 06:21:10,340 INFO gateway.kanban: dispatcher: assigned task_t_abc123 to profile_worker1
```

### Task Assignment
```
2026-06-14 06:22:10,338 INFO gateway.kanban: dispatcher: task_t_caa69668 ready, 3 workers available
2026-06-14 06:22:10,340 INFO gateway.kanban: dispatcher: assigned task_t_caa69668 to profile_quartz
```

### Heartbeat & Stale Detection
```
2026-06-14 06:23:10,338 INFO gateway.kanban: dispatcher: heartbeat from profile_wave for task_t_xyz
2026-06-14 06:23:10,340 INFO gateway.kanban: dispatcher: task_t_stale exceeded 14400s, re-queueing
```

### Failure Handling
```
2026-06-14 06:24:10,338 WARNING gateway.kanban: dispatcher: task_t_fail failed (attempt 1/2)
2026-06-14 06:24:10,340 INFO gateway.kanban: dispatcher: task_t_fail re-queued for retry
# After failure_limit (2):
2026-06-14 06:25:10,338 ERROR gateway.kanban: dispatcher: task_t_fail exceeded failure limit, blocked
```

## Troubleshooting

### Dispatcher Not Running
**Symptom**: No "kanban dispatcher: embedded in gateway" line in logs
**Fix**: 
1. Check `config.yaml` has `kanban.dispatch_in_gateway: true`
2. Restart gateway: `hermes gateway restart`
3. Verify gateway process: `ps aux | grep hermes`

### Tasks Not Assigned
**Symptom**: "dispatcher: polling board..." but no assignments
**Causes**:
- No worker profiles with `kanban-orchestrator` skill
- Workers at `max_in_progress_per_profile` limit
- Tasks not in "ready" state (missing dependencies)
- `default_assignee` set but that profile unavailable

### Stale Tasks Not Recovered
**Symptom**: Tasks stuck in "in_progress" beyond `dispatch_stale_timeout_seconds`
**Fix**: 
- Verify dispatcher is polling (check logs)
- Check `dispatch_stale_timeout_seconds` (default 14400 = 4 hours)
- Ensure worker heartbeats are working (profile must call `kanban_heartbeat`)

### Telegram Messages Not Creating Tasks
**Note**: Gateway dispatcher ONLY polls existing Kanban board. It does NOT create tasks from Telegram messages.
**Solution**: Interface profile (`principal-interface`) must use `kanban-orchestrator` skill to create tasks from Telegram messages, OR use a webhook to create Kanban cards.

## Verification Commands

```bash
# Check dispatcher running
grep "kanban dispatcher" <agent-home>/logs/gateway.log

# Watch live dispatcher activity
tail -f <agent-home>/logs/gateway.log | grep -i kanban

# Check for assignments
grep "assigned task" <agent-home>/logs/gateway.log

# Check for failures
grep -i "fail\|blocked\|stale" <agent-home>/logs/gateway.log | grep kanban
```