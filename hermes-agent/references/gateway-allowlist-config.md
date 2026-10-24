# Gateway user allowlist configuration

## Symptom

Telegram (or other messaging platform) appears to "not work" — outbound messages from the agent succeed, but inbound messages from users are silently ignored. Gateway logs show:

```
WARNING gateway.run: No user allowlists configured. All unauthorized users will be denied. Set GATEWAY_ALLOW_ALL_USERS=true in <agent-home>/.env to allow open access, or configure platform allowlists (e.g., TELEGRAM_ALLOWED_USERS=your_id).
```

## Root cause

The the operator agent gateway has a security feature that **denies all inbound messages by default** unless explicitly allowed. This is controlled by:

1. `GATEWAY_ALLOW_ALL_USERS=true` in `.env` — allows everyone (not recommended for production)
2. Platform-specific allowlists in `.env`:
   - `TELEGRAM_ALLOWED_USERS=123456789,987654321` (comma-separated Telegram user IDs)
   - `DISCORD_ALLOWED_USERS=...`
   - `SLACK_ALLOWED_USERS=...`
   - etc.

## Finding your user ID

**Telegram:** Send a message to the bot, then check gateway logs for:
```
inbound message: platform=telegram user=YourName chat=<chat-id> msg='...'
```
The `chat=` value is your Telegram user ID (for DMs) or chat ID (for groups).

**Discord/Slack:** Similar pattern in logs, or use platform dev tools.

## Fix

1. Add to `<agent-home>/.env`:
   ```bash
   TELEGRAM_ALLOWED_USERS=<chat-id>
   ```

2. Restart the gateway:
   ```bash
   hermes gateway restart
   ```

3. Verify in logs:
   ```
   INFO gateway.run: inbound message: platform=telegram user=YourName chat=<chat-id> msg='...'
   ```

## Common pitfalls

- **Multiple Telegram accounts:** If you use multiple Telegram accounts, you need all their IDs in the allowlist
- **Group chats:** For group messages, use the chat ID (negative number), not user IDs
- **Platform-specific:** Each platform needs its own allowlist env var; there's no global "allowed users" list
- **GATEWAY_ALLOW_ALL_USERS=true** works but disables the security feature entirely — prefer explicit allowlists

## Verification checklist

- [ ] Allowlist env var added to `<agent-home>/.env`
- [ ] Gateway restarted (`hermes gateway restart`)
- [ ] Gateway logs show "inbound message" for your test message
- [ ] Bot replies to your message in Telegram