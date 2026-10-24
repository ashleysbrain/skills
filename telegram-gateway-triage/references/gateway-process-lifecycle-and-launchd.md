# Gateway Process Lifecycle & launchd Persistence

Notes on the layer *below* routing/delivery: when the messaging gateway
**process itself is not running**, Telegram is dead in both directions.
This is the first thing to rule out before any chat-path triage.

## Symptom

User says "Telegram is broken / I can't send / messages aren't arriving."
No recent `gateway.log` activity. The agent can still chat via the desktop
app / TUI / dashboard because those are separate surfaces.

## Step 0 — is the gateway process alive?

```sh
hermes gateway status          # authoritative
pgrep -fl "gateway run"        # is a process running?
tail -20 <agent-home>/logs/gateway.log   # last connect / errors
```

If `status` says "not running" and `pgrep` returns nothing, the gateway is
dead. **This is the root cause — do not start triaging routing/home_channel
until the process is back up.**

Key fact: the the operator agent desktop app only spawns `hermes dashboard` — it does
NOT spawn the messaging gateway. A dead gateway stays dead across reboots
unless the launchd service is installed and loaded.

## Start the gateway

- Foreground (debug): `hermes gateway run`
- As a service (durable): `hermes gateway install` then `hermes gateway start`

Always verify after start:
```sh
grep -i "telegram connected" <agent-home>/logs/gateway.log
```
Do not claim success until `✓ telegram connected` appears.

## The launchd disabled-state trap (macOS, recurring)

`hermes gateway install` can silently fail with:

```
launchctl bootstrap exit 5
```

and fall back to a bare background process that **dies on reboot / does not
auto-restart on crash**. Root cause is almost always a stale *disabled*
label left by a previous install:

```sh
# confirm
launchctl print-disabled "gui/$(id -u)" | grep hermes
#   "ai.hermes.gateway" => disabled    <-- the trap

# fix: clear the disabled flag, then re-bootstrap
launchctl enable "gui/$(id -u)/ai.hermes.gateway"
launchctl bootstrap "gui/$(id -u)" ~/Library/LaunchAgents/ai.hermes.gateway.plist
```

A successful load reports `state = running`. Verify the service (not just a
process) is loaded:

```sh
launchctl print "gui/$(id -u)/ai.hermes.gateway" | head
hermes gateway status    # should say "Gateway service is loaded"
```

The plist at `~/Library/LaunchAgents/ai.hermes.gateway.plist` must carry
`RunAtLoad = true` (start at login) and `KeepAlive = true` (restart on
crash). With both set and the label enabled, the gateway survives reboot
and crash.

## Why this recurs

When the install falls back to a bare process (because of the disabled
label), the user gets a working gateway *today* but it dies on the next
reboot and "Telegram is broken again." Each reinstall re-trips the same
disabled state. Clearing the label once (`launchctl enable`) breaks the
loop permanently.
