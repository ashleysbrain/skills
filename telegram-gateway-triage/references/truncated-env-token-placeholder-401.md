# Truncated `.env` Token — Placeholder 401 (2026-08-24 live case)

The bot token line in `<agent-home>/.env` was silently truncated to a
placeholder (`TELEGRAM_BOT_TOKEN=123:ABC`, 7 chars) by an unknown writer.
Distinct from the polling-stall wedge: the failure is AUTH, not polling.

## Symptom chain

- Outbound sends fail `401 Unauthorized` (both API tools and cron delivery:
  `Telegram send failed: Unauthorized (target telegram:<chat_id>)`).
- Gateway log: ``The token `123:ABC` was rejected by the server`` followed by
  `✗ telegram failed to connect`.
- `<agent-home>/gateway_state.json` → `platforms.telegram.state: "fatal"`.

## The masking trap

A gateway that started BEFORE the truncation keeps running on its in-memory
token and hides the corruption for hours — the failure only surfaces on the
next gateway restart. Live case: file truncated 11:01, gateway restarted
15:14, Telegram `fatal` until diagnosed ~20:20. A running bot is therefore
NOT evidence the token file is intact.

## Diagnosis

1. Read the token's length — real bot tokens are ~46 chars; under 30 = corrupted.
2. Probe candidates via `getMe` (never print the token; mask to 8 chars).
3. `ps eww <gateway_pid>` will NOT show it (env is read from file, not inherited).

## Recovery (proven live)

1. Check `<agent-home>/state-snapshots/*/‑pre-update/.env` BEFORE concluding the
   token must be re-minted at BotFather — the July snapshot held the intact,
   still-valid token (bot verified as HermesPAbot).
2. Restore the line(s): `TELEGRAM_BOT_TOKEN=<token>` and
   `TELEGRAM_ALLOWED_USERS=<chat_id>` (both may be truncated together).
3. Verify: `getMe` returns the bot username.
4. Restart: `launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway`.
   State path observed: `fatal` -> `connecting` -> `connected` within ~60s.
   (If kickstart is unavailable from the gateway's own shell, dispatch a
   leaf subagent — separate process can bootstrap.)

## Redelivery law (same as the wedge)

Messages sent while the bot was disconnected are NOT replayed if the polling
offset advanced. Confirm via `getWebhookInfo` → `pending_update_count: 0`
(polling mode) plus a direct one-shot `getUpdates?timeout=0` returning empty.
Ask the user to resend anything critical. Do NOT imply messages are queued.

## Security note

Unknown-writer truncation of a credentials file is a finding in its own
right (Saltzer-Schroeder fail-safe defaults: the running process concealed
the corruption). Route the writer-hunt to the security lane — do not just
restore and move on.
