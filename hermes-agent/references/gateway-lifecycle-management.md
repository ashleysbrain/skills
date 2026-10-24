# Gateway Lifecycle Management on macOS

## Problem
the operator agent gateway on macOS runs under launchd which has several quirks:
- `launchctl bootstrap` fails with "Input/output error" on macOS 26+
- Gateway process gets SIGTERM during `hermes gateway start --replace`
- Background processes started via `hermes gateway start` don't persist across logout
- `launchctl bootout` leaves stale entries (-9 status)

## Clean Restart Pattern

```bash
# 1. Kill existing gateway processes
pkill -f "gateway run" 2>/dev/null; sleep 2

# 2. Remove launchd plist
rm -f ~/Library/LaunchAgents/ai.hermes.gateway.plist
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/ai.hermes.gateway.plist 2>/dev/null

# 3. Wait for launchd to clean up
sleep 3
launchctl list | grep -i hermes

# 4. Start fresh in background (NOT via launchd)
cd /<workspace>
/<workspace> -m hermes_cli.main gateway run 2>&1 &
```

## Verification
```bash
# Check logs
tail -30 <agent-home>/logs/gateway.log

# Verify Telegram connected
grep "telegram connected" <agent-home>/logs/gateway.log

# Check kanban dispatcher
grep "kanban dispatcher" <agent-home>/logs/gateway.log
```

## Common Issues

| Issue | Fix |
|-------|-----|
| "Boot-out failed: 3: No such process" | Remove plist, `launchctl bootout`, wait, restart |
| "Bootstrap failed: 5: Input/output error" | macOS 26+ launchd bug — run manually in background |
| Gateway dies on SSH logout | `sudo loginctl enable-linger $USER` (Linux) or use `nohup` |
| Telegram messages ignored | Check `TELEGRAM_ALLOWED_USERS` in `.env` and restart gateway |

## Best Practices
1. **Always kill via pkill first** before launchd operations
2. **Wait 2-3 seconds** between kill and restart
3. **Run manually in background** for development, not via launchd
4. **Check logs** for "kanban dispatcher: embedded in gateway" to confirm dispatcher active
5. **Use `--replace` flag sparingly** — causes SIGTERM to existing gateway