# Time-Perception Failures — Presence Inference vs Testimony (2026-08-27)

Three incidents in ~36 hours, escalating severity. All are temporal-claim Grade
C failures — time-based claims asserted without conversion or verification.

## The three incidents

1. **"Busiest hour is 3 AM"** — bus timestamps stored in UTC were read as user
   local time. The work was real; the hour was wrong by 5 hours.
2. **"Good morning" brief at 8:39 PM** — principal's message after a gap was
   pattern-matched to "morning stir." Live clock check (one `date` call) would
   have shown evening. No sleep gap had occurred.
3. **"2 hours of downtime" — INVENTED.** Reported bus silence "after 01:32" as
   a 2-hour overnight gap. 01:32 was UTC = 8:32 PM local — EIGHT minutes before
   the principal's message. The bucket query output was in the transcript and showed
   continuous traffic; the claim was never checked against it. This is the
   worst class: a fabricated finding with a number attached, from healthy data.

## Standing rules (now hard pre-send checks)

1. **Every time/duration claim gets a live clock check in the same turn** —
   `date` for "what time is it now", explicit UTC→local conversion for every
   stored timestamp quoted. Never quote a raw bus/DB timestamp unconverted.
2. **Thread silence is not sleep evidence.** Presence must be checked across
   ALL interfaces, not inferred from the reporting thread's quiet spell. A
   message gap means "no messages in this thread", nothing more.
3. **User testimony beats sensor inference.** If the user says "I was up until
   4 AM", that IS ground truth; the system refines its sensors, never argues
   its inferred window against the user's stated reality.
4. **When testimony and sensors conflict, surface the conflict** — do not
   silently pick one. Report: "sensors say X, you say Y, using Y."

## Why orchestrators are prone to this

Overnight reports invite narrative framing ("while you slept..."). The
narrative pressure precedes the data check. The fix is mechanical: conversion
and clock checks are pre-send gates, not judgment calls. A duration claim
computed from unconverted timestamps is already wrong when written.
