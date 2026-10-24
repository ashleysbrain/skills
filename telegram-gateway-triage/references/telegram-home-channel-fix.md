# Telegram Home Channel Fix

Complete procedure for fixing Telegram message delivery when the home channel
is not set or is incorrectly configured.

## Symptoms

`send_message` to bare `telegram` target fails with:
```
No home channel set for telegram to determine where to send the message.
```

## Root cause

The gateway reads `TELEGRAM_HOME_CHANNEL` from the environment via
`os.getenv("TELEGRAM_HOME_CHANNEL")` in `gateway/config.py` (`_apply_env_overrides`).
This env var is loaded from `<agent-home>/.env`. If it is not in `.env`, the home
channel is not set.

The `send_message` tool error message tells you to run:\n```\nhermes config set TELEGRAM_HOME_CHANNEL <channel_id>\n```\n**This does NOT work for the gateway process.** That command writes a flat top-level key to config.yaml that the gateway code never reads for incoming message handling. However, it DOES work for OUTGOING messages via the send_message tool (which runs in the agent process) because the agent process reads config.yaml directly.

## Fix Option A — Nested YAML config (RECOMMENDED)

Set the home channel as a proper nested dict in config.yaml:

```bash
hermes config set gateway.platforms.telegram.home_channel.chat_id <chat_id>
hermes config set gateway.platforms.telegram.home_channel.platform telegram
hermes config set gateway.platforms.telegram.home_channel.name Home
```

This produces the correct YAML structure:
```yaml
gateway:
  platforms:
    telegram:
      home_channel:
        chat_id: <chat-id>
        platform: telegram
        name: Home
```

**CRITICAL**: Do NOT use a bare scalar:
```yaml
# WRONG — causes "'int' object is not subscriptable"
gateway:
  platforms:
    telegram:
      home_channel: <chat-id>
```

The `HomeChannel.from_dict()` parser expects a dict with `platform`, `chat_id`,
and `name` keys. A bare integer will crash at config load time.

## Fix Option B — Environment variable

Add to `<agent-home>/.env`:
```
TELEGRAM_HOME_CHANNEL=<chat_id>
```

The gateway reads this via `os.getenv()` at startup. Requires a gateway restart.

## Fix Option C — Top-level config.yaml (AGENT PROCESS ONLY)\n\nSet as top-level key in config.yaml:\n```\nhermes config set TELEGRAM_HOME_CHANNEL <channel_id>\n```\n\nThis works FOR OUTGOING messages via `hermes send -t telegram` or send_message tool\nbecause the agent process reads config.yaml directly.\n\n**DOES NOT WORK** for incoming message handling via the gateway process.\n\n## Finding your chat ID

1. Send any message to your Telegram bot.
2. Check the gateway log: `grep -i "chat_id" <agent-home>/logs/gateway.log`
3. Or use `hermes tools` in an interactive terminal to list targets.

## Key architectural note

The `send_message` tool calls `load_gateway_config()` **in the calling agent
process**, not in the gateway process. This means:
- Config changes in config.yaml take effect immediately for `send_message` (no
  gateway restart needed for the tool itself).
- But the gateway process needs a restart to pick up config changes for polling,
  receiving messages, and other gateway-side operations.

## Verification

```bash
# Test send
hermes send -m "Test via home channel" -t telegram
# or in agent: send_message(target="telegram", message="test")

# Check gateway log for Telegram connection
grep -i "telegram connected" <agent-home>/logs/gateway.log
```

## Debugging methodology

When config is not being picked up, DO NOT immediately edit source code. Instead:
1. Trace the actual data path: `os.getenv()` → `.env`, or YAML → `from_dict()`.
2. Check the format the parser expects (dict vs scalar).
3. Fix the data, not the parser.
4. Only edit source code if the data format is correct but parsing has a bug.
