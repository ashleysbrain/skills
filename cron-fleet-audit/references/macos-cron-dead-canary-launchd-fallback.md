# macOS Scheduler Falsification + Fallback Stack (2026-08-18)

## The canary technique (falsify scheduler liveness in one cycle)
Symptom: crontab entry valid, `cron` daemon process alive, but NO job output for
40 minutes. Before touching the jobs, falsify the SCHEDULER:
1. `echo "* * * * * touch /tmp/cron-canary" | crontab -l >> /tmp/new; crontab /tmp/new`
   — plus a SECOND canary writing under `$HOME` (isolates TCC/Full-Disk-Access
   blocking from daemon-dead).
2. `sleep 75` (one full minute boundary + margin), then `ls` both canaries.
3. Both absent = cron fires NOTHING host-wide. One absent = permission scope.
Cleanup: rebuild crontab without canaries afterward.

Evidence gathering: `log show --predicate 'process == "cron"' --last 40m`,
`/var/mail/$USER` for cron error mail.

## Findings from the 2026-08-18 incident
- macOS cron can be fully dead while `pgrep cron` shows the daemon running.
  Jobs never execute, silently. Any cron-fleet audit that only checks "daemon
  process exists" passes a dead scheduler — always canary-test.
- A tick script that exits 0 with no output line = it likely took a silent
  skip branch (stale mutex). Check lock dirs (`ls -ld /tmp/<name>.lock.d`),
  check `pgrep -fl <script>`, and grep the log for the completion line —
  exit code alone proves nothing.

## Recovery stack (in order)
1. **launchd LaunchAgent (preferred end state per principal uptime law):**
   write `~/Library/LaunchAgents/com.your-org.<name>.plist`
   (RunAtLoad + StartInterval), `plutil -lint` it.
   NOTE: `launchctl bootstrap gui/$(id -u)` is BLOCKED from inside the
   the operator agent gateway process (persistent-job safety). It needs one manual line
   from a separate shell: `launchctl bootstrap gui/501 ~/Library/LaunchAgents/<name>.plist`.
   Park the plist on disk and tell the user the one-liner.
2. **Interim: hermes-cron watchdog** (fires via the the operator agent scheduler, immune to
   system cron death): cronjob tool, `*/10`, deliver=local, prompt runs the
   tick and replies TICK-OK / TICK-FAIL+log-tail / LAUNCHD-ACTIVE (self-
   removal signal once launchd takes over).
3. Verify end-to-end by running the tick ONCE in foreground and grepping the
   log for its completion line — never declare scheduling restored on config
   presence alone.
