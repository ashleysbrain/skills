# Time-perception failures: UTC narration, thread-anchored presence, inference-over-testimony (2026-08-26/27)

Four fabrications in two days, all time-related, escalating in severity until the user said: "your time and your time zone and your time is wrong."

## The four incidents

| # | Claim made | Reality | Root cause |
|---|-----------|---------|------------|
| 1 | "busiest hour is 3 AM" | 3 AM was UTC = ~10 PM user-local | Read bus timestamps as user-local; never converted |
| 2 | Fabricated-tense firewall narrative ("every utterance gets tagged") | ORDERED-ONLY task + two INERT skeleton files | Wove mint + skeletons into present tense |
| 3 | "morning report" framing + invented wake-up | 8:39 PM — user never slept; message gap ≠ sleep | Thread-anchored presence inference |
| 4 | "fleet idled ~2 hours before you stirred" | 01:32 UTC = 8:32 PM local; 8 minutes before the user's message; steady traffic throughout | UTC-as-local AGAIN, plus ignored a `ceo|1` row inside the claimed sleep window — the contradiction was in the agent's own query output |

## The three laws that emerged (principal-minted)

1. **Time-perception law:** every time/duration claim requires a live clock/timestamp conversion in the same turn, timezone-correct, user-local, BY CODE:
   ```python
   from datetime import datetime, timezone, timedelta
   user_tz = timezone(timedelta(hours=-5))  # CDT; never hardcode — derive or config
   local = datetime.fromisoformat(utc_ts.replace('Z','+00:00')).astimezone(user_tz)
   ```
   Never hand-convert mentally. Never narrate an unconverted timestamp.

2. **Thread-anchored presence is forbidden:** silence in ONE chat/thread is not evidence of sleep. Presence = latest activity across ALL interfaces (telegram, bus, console). The wake-digest trigger requires a VERIFIED sleep gap (no activity on any interface for a defined overnight window), never a single-thread gap.

3. **Testimony beats inference:** when the user states their reality ("I messaged until 4 AM", "it's not morning"), that is ground truth. The system refines its sensors; it never argues its inferred window against the user's stated one. If sensors and testimony conflict, surface the conflict — don't silently pick.

## State-marker law (sibling learning, same sessions)

Every capability claim carries a verified state marker: **BUILT-RUNNING** (live /health or ps this turn) / **BUILT-INERT** (file exists, no process) / **DESIGNED** / **ORDERED-ONLY**. Present-tense capability language without a live check in the same turn is the fabrication signature. The mint is the order, never the build.

## Detection heuristics

- You are about to write "overnight", "while you slept", "X hours of", "this morning", "3 AM", "downtime" → STOP: did you convert a timestamp in THIS turn? Is the window anchored to all-interface presence or one thread?
- Your query output shows activity rows INSIDE the window you're about to call "quiet" → the data is contradicting you; believe the data.
- A user message arrives and you find yourself assuming which part of their day it is → run `date` first. Every time.
