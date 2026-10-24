# macOS Auto-Start Fix for Services

## The Problem
A service (e.g., `pipeline_api.py`) runs as a child process of a dev server
or desktop app. It has no independent auto-start mechanism. When the parent
process stops (reboot, crash, app closure), the service dies silently.

## Diagnosis
```bash
# Check if the service has any auto-start mechanism
launchctl list | grep <service-name>     # launchd job?
ls ~/Library/LaunchAgents/com.*.plist    # plist file?
ps -p $(pgrep -f <service>) -o ppid=     # who is the parent?

# If the parent is a desktop app or dev server, there is NO auto-start.
```

## Fix: Create a launchd LaunchAgent

Create `~/Library/LaunchAgents/com.<org>.<service>.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
 "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.<org>.<service></string>

    <key>ProgramArguments</key>
    <array>
        <string>/path/to/python3</string>
        <string>-B</string>
        <string>service.py</string>
        <string>--port</string>
        <string>8310</string>
    </array>

    <key>WorkingDirectory</key>
    <string>/path/to/workspace</string>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>ThrottleInterval</key>
    <integer>10</integer>

    <key>StandardOutPath</key>
    <string>/path/to/logs/service.stdout.log</string>

    <key>StandardErrorPath</key>
    <string>/path/to/logs/service.stderr.log</string>
</dict>
</plist>
```

## Load and Verify

```bash
# Kill the old manually-started process first
kill <old-pid>

# Load the LaunchAgent
launchctl load ~/Library/LaunchAgents/com.<org>.<service>.plist

# Verify it started
sleep 3
launchctl list | grep <service>
curl -sf http://localhost:<port>/health

# Test crash recovery
kill -9 $(pgrep -f 'service.py')
sleep 5
pgrep -f 'service.py'  # should show a NEW pid (launchd restarted it)
```

## Key Flags
- `RunAtLoad`: starts on login (no need for the parent app)
- `KeepAlive`: auto-restarts on crash
- `ThrottleInterval`: minimum seconds between restarts (prevents tight crash loops)
