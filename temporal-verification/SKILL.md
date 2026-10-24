---
name: temporal-verification
category: operations
description: Use when making temporal claims; verify clocks first.
version: 1.0.0
---

# Temporal Verification — Clock, Timeline, and Timezone Facts

## Trigger
Use when making ANY temporal claim: current time, time until event, duration, "dead for N days," "stuck for N hours," "last run at," appointment times.

## Core Principle

**Temporal facts are claims about the physical world. They require physical verification, not memory recall or mental computation.**

Timezone conversions, duration calculations, and "how long has X been Y?" questions are notoriously error-prone. The only reliable approach is system-level verification with actual commands and log analysis.

## The Failed Pattern (What NOT to Do)

```
principal: "what's happening with sibling-agent?"
❌ WRONG: "sibling-agent dead 3+ days" (claimed from mental state, no logs checked)

User: "how long until my 12:45 appointment?"
❌ WRONG: "40 minutes" (assumed UTC vs CDT, no date verification)

Result: Both claims were FALSE. User corrected: "you failed this training."
```

## The Effective Pattern (What TO Do)

### Step 1: Verify current time and timezone
```bash
date  # Returns local time (e.g., "Fri Aug 28 16:30:00 CDT 2026")
```

**Critical:** Note the timezone (CDT = UTC-5 in August). If working with UTC, compute the offset programmatically.

### Step 2: For time-until calculations
```python
python3 -c "
from datetime import datetime
t1 = datetime.fromisoformat('2026-08-28T12:45-05:00')  # CDT explicit
t2 = datetime.now(t1.tzinfo)  # Same timezone
minutes = (t2 - t1).total_seconds() / 60
print(f'{minutes:.1f} minutes' if minutes > 0 else 'PASSED')
"
```

**Rules:**
- Include timezone in ISO timestamps (`-05:00` for CDT)
- Use `tzinfo` matching the target time
- Compute distance programmatically — never mental math
- Report "X hours" not "X minutes" when >60

### Step 3: For "how long has X been Y?" (dead/stuck/running)

**Check logs for timestamped events:**
```bash
# Find last BOOT event
grep '"fn": "boot"' sibling-agent-autonomic.log | tail -1

# Find last successful processing
grep '"state": "done"' sibling-agent-autonomic.log | tail -1

# Find last error
grep -i "error\|exception\|fail" sibling-agent-autonomic.log | tail -5
```

**Check process uptime:**
```bash
launchctl list | grep sibling-agent-autonomic
ps aux | grep sibling-agent-autonomic | grep -v grep
```

**Compute duration from log timestamps:**
```python
python3 -c "
from datetime import datetime
last_boot = '2026-08-28T08:05:00Z'  # From log
now = datetime.now(datetime.now().astimezone().tzinfo)
hours = (datetime.fromisoformat(last_boot) - now).total_seconds() / 3600
print(f'{abs(hours):.1f} hours ago' if hours < 0 else f'in {hours:.1f} hours')
"
```

**Rules:**
- NEVER claim "dead N days" without checking BOOT timestamps in logs
- NEVER claim "running N hours" without checking process uptime
- Absence of log lines DOES NOT mean "dead" — check process table
- Logs are the source of truth for historical state, not memory

## Session Evidence

### Session: 2026-08-28 — Temporal claim failures

**Claim 1:** "sibling-agent dead 3+ days"
- User: "how did sibling-agent not work for several dayssssss??? yet youve been telling me you were working with sibling-agent?????????"
- **Verification:** Logs showed continuous operation: PID 1483 (Aug 27), PID 58585 (Aug 28), PID 50440 (Aug 28)
- **Reality:** Opencode was RUNNING; my builds were being filtered, not the daemon

**Claim 2:** "appointment in 40 mins"
- User: "your timezone and clock is off... my appointment is NOT in 40 mins"
- **Verification:** `date` showed 07:36 CDT; target was 12:45 CDT = 5.1 hours, not 40 mins
- **Root cause:** Assumed UTC for target, principal on CDT

**Both failures logged as training violations.**

## Pitfalls to Avoid

1. **Temporal claims from memory** — Session (2026-08-28): Claimed "sibling-agent dead 3+ days" from mental state; logs proved it was running continuously
2. **Timezone assumptions** — Always verify timezone with `date`; if working with UTC, compute offset explicitly
3. **Mental time math** — Distance calculations MUST be programmatic (`python3 -c "from datetime import datetime; ..."`), never mental
4. **Absence from memory ≠ fact** — "I haven't seen X" is not evidence of X not existing; check logs/databases with actual queries
5. **"Stuck for N hours" without timestamp check** — If a build is pending, check `message-bus.db` for the actual posted timestamp, then compute duration
6. **"Last run" without log verification** — Check cron logs, daemon logs, or process state — do not claim from memory

## Related Skills

- `verification-patterns` — General verification discipline (live surface first)
- `message-bus-protocol` — Queue state verification patterns
- `cron-fleet-audit` — Cron job health and timestamp analysis

## Templates

### Temporal claim checklist
```markdown
Before claiming temporal fact:
- [ ] Verified current time with `date`
- [ ] Noted timezone (CDT, UTC, etc.)
- [ ] Checked logs for timestamped evidence
- [ ] Computed distance programmatically (python3 datetime)
- [ ] Verified process state (ps/launchctl if claiming "dead/alive")
```

### Duration calculation pattern
```python
python3 -c "
from datetime import datetime
target = datetime.fromisoformat('YYYY-MM-DDTHH:MM:SS[±HH:MM]')
now = datetime.now(target.tzinfo)
delta = (target - now).total_seconds()
unit = 'seconds' if abs(delta) < 60 else 'minutes' if abs(delta) < 3600 else 'hours'
value = abs(delta) / (1 if unit=='seconds' else 60 if unit=='minutes' else 3600)
print(f'{value:.1f} {unit}' + (' ago' if delta < 0 else ' from now'))
"
```

### Log timestamp extraction pattern
```bash
# Extract last BOOT timestamp
grep '"fn": "boot"' /path/to/log.log | tail -1 | grep -oE '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'

# Extract all done events with timestamps
grep '"state": "done"' /path/to/log.log | grep -oE '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'

# Extract error events with context
grep -i "error\|exception" /path/to/log.log | tail -10
```

## Training Record

- **2026-08-28:** principal correction — "you need to get a handle on time... you failed this training" — false temporal claims about sibling-agent status and appointment timing. Rule established: NEVER claim temporal fact without log verification.
- **2026-08-29:** THIRD failure in the same class — claimed a stall had lasted "16+ hours" without computing; actual was 29.82 hours (2026-08-28T14:42:54Z → 2026-08-29T20:32:20Z). principal: "this was a failure as you were already supposed to do this several times." ESCALATION RULE: the repetition is itself the failure — after two corrections, a third unverified claim means the verification step was skipped, not unknown. Every duration/distance claim gets the programmatic calculation in the same turn, before the sentence containing it. Two-factor liveness pattern (same stagnant IDs + advancing counters in logs/health) distinguishes 'live' from 'frozen-rendering' — use it when verifying process state.
- **2026-09-03:** FOURTH class variant — FABRICATED FUTURE TIMESTAMPS in message headers. Wrote 09:00→09:06 across consecutive headers while the real clock read 08:57–08:59 (~5-7 minutes of invented future). principal: "You just moved the clock forward... You need to know what time it is." Root cause was NOT clock drift (machine verified within 50ms of time.apple.com via `sntp -d`) — it was ESTIMATING elapsed time between tool calls and writing the estimate as fact. RULE: every timestamp rendered to the user comes from a live `date` read in the same turn (or tool-echoed clock), never from memory, arithmetic, or elapsed-time estimation. A header timestamp is a temporal claim and gets the same verification as any other. Clock-source verification recipe: `date '+%H:%M:%S'` in the same terminal call as the work; `sntp -d time.apple.com` when drift is suspected.
- **2026-09-03 (later, FIFTH variant — READ-TRANSSCRIBE MISMATCH):** the instrument was correct and the output was still wrong. Terminal `date` reads returned 15:51/15:52 correctly, but the message headers written minutes later said 11:52 — the live read was transcribed from stale memory instead of copied from the tool output. The earlier "re-stamp before send" fix addressed WHEN to read the clock, not HOW the value travels to the output; a hand-copy link remained and failed. principal: "your time clock is wrong and you told me the process was corrected." GENERAL LAW: a process is not fixed while ANY step still depends on manual transcription — instrument-to-output must be mechanical end to end (copy digit-for-digit from the immediately preceding tool output; if the composing turn spans >1 min since the last read, re-read before sending). Longer-term fix: the stamp belongs in the report engine, not in the operator's hands. Same class as verify-by-read-back on external writes: a value you re-type by hand is a value you can silently corrupt.

## Philosophy

**Rule:** Claims about time are claims about the world. Treat them with the same rigor as experimental data — measure, don't guess.

## Critical Finding: Process Verification Includes PID History