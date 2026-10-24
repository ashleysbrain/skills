# Telegram Polling Watchdog Fix

## Problem

`python-telegram-bot`'s Updater can enter a silently-wedged state: `Updater.running=True`
but the underlying long-poll consumer task is dead. No `error_callback` fires, so the
reconnect ladder never engages. The gateway process stays alive but stops receiving ALL
messages indefinitely.

Before this fix, Telegram had only a one-shot health probe (`_verify_polling_after_reconnect`)
that ran once 60s after a reconnect. It did NOT continuously monitor polling health.
Slack already had `_socket_watchdog_loop`; Telegram did not.

## File Modified

`gateway/platforms/telegram.py`

## Changes (4 edits)

### 1. Add watchdog task field in `__init__`

```python
self._polling_watchdog_task: Optional[asyncio.Task] = None
```

### 2. Add `_polling_watchdog_loop()` method (after `_verify_polling_after_reconnect`)

```python
async def _polling_watchdog_loop(self) -> None:
    """Continuous polling health monitor.

    Runs every WATCHDOG_INTERVAL and probes polling health the same way the
    one-shot does: check Updater.running, then hit getMe() with a tight timeout.
    On failure it re-enters the existing reconnect ladder via
    _handle_polling_network_error.

    Slack has an equivalent (_socket_watchdog_loop); this brings Telegram to parity.
    """
    WATCHDOG_INTERVAL = 300  # 5 minutes
    PROBE_TIMEOUT = 15

    while True:
        try:
            await asyncio.sleep(WATCHDOG_INTERVAL)
        except asyncio.CancelledError:
            return

        try:
            if self._webhook_mode:
                continue
            if self.has_fatal_error:
                continue
            if not (self._app and self._app.updater):
                continue

            if not self._app.updater.running:
                logger.warning(
                    "[%s] Polling watchdog: Updater not running — "
                    "triggering reconnect",
                    self.name,
                )
                await self._handle_polling_network_error(
                    RuntimeError("Updater stopped (detected by watchdog)")
                )
                continue

            try:
                await asyncio.wait_for(self._app.bot.get_me(), PROBE_TIMEOUT)
                self._send_path_degraded = False
            except asyncio.TimeoutError:
                logger.warning(
                    "[%s] Polling watchdog: getMe() timed out after %ds — "
                    "httpx pool likely wedged, triggering reconnect",
                    self.name, PROBE_TIMEOUT,
                )
                await self._handle_polling_network_error(
                    RuntimeError("getMe() timeout in watchdog")
                )
            except Exception as probe_err:
                logger.warning(
                    "[%s] Polling watchdog: getMe() failed: %s — "
                    "triggering reconnect",
                    self.name, probe_err,
                )
                await self._handle_polling_network_error(probe_err)
        except asyncio.CancelledError:
            return
        except Exception:
            logger.warning(
                "[%s] Polling watchdog iteration failed; continuing",
                self.name,
                exc_info=True,
            )
```

### 3. Start watchdog in `connect()` after "Connected to Telegram" log

```python
# Start the continuous polling watchdog (polling mode only).
if not self._webhook_mode:
    self._polling_watchdog_task = asyncio.ensure_future(
        self._polling_watchdog_loop()
    )
    self._background_tasks.add(self._polling_watchdog_task)
    self._polling_watchdog_task.add_done_callback(
        self._background_tasks.discard
    )
```

### 4. Cancel watchdog in `disconnect()`

```python
if self._polling_watchdog_task and not self._polling_watchdog_task.done():
    self._polling_watchdog_task.cancel()
    try:
        await self._polling_watchdog_task
    except asyncio.CancelledError:
        pass
self._polling_watchdog_task = None
```

## Why 5-minute interval

- Long enough to not add meaningful API load (getMe is cheap, once per 5 min)
- Short enough that a wedge is caught before the user notices in most cases
- Telegram long-poll timeout is ~30s, so a healthy poller completes many cycles
  between checks

## How to verify the watchdog is running

```bash
# Check gateway logs for watchdog activity (only logs on failure, not on success)
grep "Polling watchdog" <agent-home>/logs/gateway.log

# Verify the code is loaded
cd <agent-home>/hermes-agent && source venv/bin/activate
python -c "from gateway.platforms.telegram import TelegramAdapter; import inspect; assert '_polling_watchdog_loop' in inspect.getsource(TelegramAdapter.connect); print('Watchdog wired')"
```

## Observed stall pattern (pre-fix)

The gateway stalled twice in a single day (Jun 18, 2026):
- ~13:50 — after a 47-minute response (2824s, 1 API call)
- ~19:34 — after a 17-minute response (1015s, 12 API calls)

Both stalls followed long-running agent responses. The pattern suggests the event loop
or httpx pool becomes exhausted after sustained load, and the polling consumer dies
without raising an exception.
