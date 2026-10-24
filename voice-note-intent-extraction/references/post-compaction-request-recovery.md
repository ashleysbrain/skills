# Post-Compaction Request Recovery

## The Problem

Context compaction summarizes earlier conversation turns. The summary includes:
- "Historical Task Snapshot" — what the agent was doing
- "Historical In-Progress State" — work in progress
- "Historical Pending User Asks" — outstanding requests

These sections are labeled "REFERENCE ONLY" and the compaction note says to "respond ONLY to the latest user message." But in practice, the agent often treats the task snapshot as the active work queue and continues it without checking what the user actually wants NOW.

The user's most recent voice note may have been sent DURING the compacted window. It may not appear in the summary at all, or may be buried under "Historical Pending User Asks." The voice note may completely redirect the session.

## Session Example (2026-06-17)

**What happened:**
1. Agent was doing engine fixes (Layer 4 methodology deployment across Da Vinci organs)
2. Context compacted mid-work
3. The compaction summary preserved the engine-fixing task list
4. User had sent a voice note at 7:08 PM asking for a PDF explaining all engines and methodologies
5. After compaction, the agent continued the engine fixes for several tool calls
6. User said: "This isn't what I asked for in my last voice note I sent at 7:08"
7. The voice note was in `<agent-home>/audio_cache/audio_48001c848e9c.ogg` — fully recoverable

**Root cause:** The agent followed the stale task snapshot instead of scanning audio_cache for the latest unprocessed voice note.

## Recovery Protocol

After context compaction, before doing ANY work:

```bash
# 1. Find voice notes newer than the last assistant response
ls -lt <agent-home>/audio_cache/*.ogg <agent-home>/audio_cache/*.mp3 2>/dev/null | head -5

# 2. Check timestamps — anything within the last 30 minutes may be unprocessed
# 3. Transcribe the most recent ones
/usr/local/bin/whisper <agent-home>/audio_cache/<latest_file> --model base --language en

# 4. Compare against the task snapshot
#    - If the voice note asks for something different, FOLLOW THE VOICE NOTE
#    - If the voice note confirms the current direction, continue
#    - If no new voice notes found, proceed with the task snapshot
```

## Decision Rule

The compaction summary's task list is NEVER more authoritative than the user's latest direct communication. Voice notes are direct communication. Task snapshots are historical state.

When in doubt: transcribe first, work second.
