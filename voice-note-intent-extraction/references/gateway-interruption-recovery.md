# Gateway-Interruption Voice Note Recovery

## The Problem

A the operator agent gateway restart can kill the session BETWEEN the voice note arriving
on disk and it being surfaced to the conversation. The next session boots with
no memory of the note, and the user asks "did you get my voice note?"

This is the third drop-class occurrence (parallel-session drop 2026-08-21,
in-transit drop 2026-07-21, gateway-interruption drop 2026-08-24). The drop
classes differ; the recovery discipline is the same: answer from DISK, never
from memory.

## TWO cache locations (critical)

1. `<agent-home>/audio_cache/` — the documented primary
2. `<agent-home>/cache/audio/audio_*.ogg` — the secondary that the primary-only
   check misses

When location 1 shows nothing new, check location 2 BEFORE concluding
non-receipt. The 2026-08-24 note lived ONLY in location 2.

Same-size duplicate pairs minutes apart = sender retries (the note was sent
twice because the first delivery produced no acknowledgment). Transcribe the
newer file; the content is identical.

## Recovery sequence (proven 2026-08-24)

```bash
# 1. Find recent audio in BOTH caches
find /<workspace> /<workspace> \
  -type f -mmin -180 2>/dev/null

# 2. Transcribe — MUST run in terminal background mode, NOT foreground
#    (foreground whisper dies to SIGTERM when the gateway restarts again;
#    exit 143 / signal 15)
# Start with tiny for speed, escalate to base if quality insufficient
whisper /<workspace><id>.ogg \
  --model tiny --output_format txt --output_dir /tmp/vnote --language en
```

Rules learned the hard way:
- **Foreground transcription is restart-fragile.** Two foreground whisper
  runs died to SIGTERM during successive gateway interruptions. The third
  run, dispatched via `terminal(background=true, notify_on_complete=true)`,
  completed cleanly.
- **Do NOT use `nohup ... &` shell wrappers.** The terminal tool rejects
  shell-level background wrappers with a blocking error. Use the tool's own
  background mode.
- `--model tiny` transcribed a 4-minute note adequately for intent
  extraction; escalate to `base` only if the user's numbers/names matter.
- whisper writes progress to stderr with semaphore-cleanup warnings on exit —
  a clean `.txt` in the output dir is the success signal, not exit codes.

## After recovery: ADHD full-capture law

The principal's standing instruction for recovered brain-dump notes: "take
everything I mentioned, every single piece and ensure it is action or put
away for future action... they're all important."

Number EVERY ask in the transcript (the 2026-08-24 note carried nine), write
each into the evidence pack with an action or an explicit shelve, and say so
in the reply. Recovery without full capture = recovery of the audio but loss
of the asks.

## Systemic fix owed

Recovery-by-spelunking is the workaround, not the cure. The durable fix
(treating voice-intake robustness as a QA defect, not a footnote) belongs to
the QA fleet build; this reference documents the manual path until then.
