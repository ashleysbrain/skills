# Gateway Home Channel Syntax Error Troubleshooting

## Symptom
- `send_message target: telegram` fails with error: "No home channel set for telegram to determine where to send the message. Either specify a channel directly with 'telegram:CHANNEL_NAME', or set a home channel via: hermes config set TELEGRAM_HOME_CHANNEL <channel_id>"
- `send_message target: telegram:CHAT_ID` works fine (direct channel ID bypasses home channel resolution)
- Telegram gateway shows as connected in `hermes gateway status` and logs
- TELEGRAM_HOME_CHANNEL is correctly configured in config.yaml and/or environment variables

## Root Cause
A syntax error in `<agent-home>/hermes-agent/gateway/config.py` in the `_apply_env_overrides` function (around lines 1384-1394) prevents proper parsing of the gateway configuration. Most commonly:
- Missing comma after `"Home")` in a `HomeChannel(` constructor call
- Debug `print` statements accidentally breaking syntax when added/removed
- The error causes the Telegram home_channel to remain `None`, leading to the "no home channel" error

## Diagnosis Steps

1. **Verify direct channel ID works** (confirms Telegram connectivity):
   ```bash
   send_message {'action': 'send', 'message': 'Test', 'target': 'telegram:YOUR_CHAT_ID'}
   ```
   If this works but home channel doesn't, the issue is config parsing.

2. **Check gateway logs for Telegram connection**:
   ```bash
   grep "telegram connected" <agent-home>/logs/gateway.log
   ```
   Should show "✓ telegram connected" if the platform adapter is working.

3. **Test config syntax**:
   ```bash
   cd /<workspace>
   python3 -m py_compile gateway/config.py
   ```
   If there's a syntax error, it will be reported here (look for lines around the telegram_home section).

4. **Inspect the problematic code section**:
   ```bash
   # Look at lines ~1384-1394 in gateway/config.py
   sed -n '1380,1400p' gateway/config.py
   ```
   Check for:
   - Missing commas in `HomeChannel(` constructor calls
   - Unbalanced parentheses
   - Debug print statements that interfere with syntax

## Fix Procedure

1. **Fix the syntax error** in `gateway/config.py`:
   - Locate the `_apply_env_overrides` function
   - Find the Telegram home channel section (look for `telegram_home = os.getenv("TELEGRAM_HOME_CHANNEL")`)
   - In the `HomeChannel(` constructor, ensure there is a comma after the `name=` parameter:
     ```python
     # BEFORE (missing comma - causes syntax error):
     name=os.getenv("TELEGRAM_HOME_CHANNEL_NAME", "Home")
     thread_id=os.getenv("TELEGRAM_HOME_CHANNEL_THREAD_ID") or None,
     
     # AFTER (correct - comma added):
     name=os.getenv("TELEGRAM_HOME_CHANNEL_NAME", "Home"),
     thread_id=os.getenv("TELEGRAM_HOME_CHANNEL_THREAD_ID") or None,
     ```
   - Remove any debug `print` statements that were added for troubleshooting but left in the code (they can break syntax if not careful)

2. **Restart the gateway** to load the fixed configuration:
   ```bash
   # Stop existing gateway
   hermes gateway stop
   # Or kill manually if needed
   pkill -f "gateway run" 2>/dev/null; sleep 2
   
   # Start fresh
   hermes gateway run --replace &
   ```

3. **Verify the fix**:
   ```bash
   # Test home channel resolution now works
   send_message {'action': 'send', 'message': 'Test: home channel fixed!', 'target': 'telegram'}
   ```
   Should succeed with "Sent to telegram home channel" message.

## Prevention Tips
- When adding debug prints to config.py, always verify syntax afterward: `python3 -m py_compile gateway/config.py`
- Use a syntax-checking editor or pre-commit hook to catch these errors early
- Remember that the gateway runs on cached bytecode (.pyc) - changes to .py files require restart to take effect
- If in doubt, compare against a known-good version or check git history

## Related References
- See `references/gateway-allowlist-config.md` for issues where outbound works but inbound is blocked
- See `references/telegram-stuck-triage.md` for general Telegram responsiveness issues
- See `references/gateway-lifecycle-management.md` for proper gateway restart procedures on macOS