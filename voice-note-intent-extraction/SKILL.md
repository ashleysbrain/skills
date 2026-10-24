---
name: voice-note-intent-extraction
description: Transcribe voice notes, separate the user’s actual ask from surrounding context, and return a clean request-versus-background summary.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [voice, transcription, intent, extraction, summarization, note-taking]
---

# Voice Note Intent Extraction

## Overview

Use this skill when a user shares a voice note, transcript, or mixed brain dump and wants the *actual request* extracted without the surrounding implementation chatter.

The goal is not just transcription. The goal is **intent separation**:
- what the user wants done
- what is merely background context
- what constraints they explicitly added
- what should be ignored because it is scaffolding, explanation, or engine-building detail

## When to Use

Use when the user:
- shares an audio note and asks for what they “specifically need”
- says to ignore the build and focus on the coaching / request / outcome
- wants a summary of their true ask from a long rambly memo
- corrects you for expanding into implementation when they only wanted the target use case

Do not use for:
- generic meeting summaries where there is no request to extract
- pure STT troubleshooting with no intent analysis
- one-line messages that do not need segmentation

## Core Workflow

### 0. Post-compaction voice note scan (Mandatory after context compression)

After context compaction, the conversation summary may have buried or omitted the user's most recent voice note. Before continuing ANY work from the "Historical Task Snapshot":

1. Check `<agent-home>/audio_cache/` for files modified after the last assistant response timestamp
2. Transcribe any unprocessed notes with: `whisper <path> --model base --language en`
3. Compare the voice note content against the task snapshot — they may diverge completely
4. If the voice note redirects away from the stale tasks, follow the voice note, not the snapshot

**The compaction summary is reference only. The user's latest voice note is the active request.**

### 1. Locate the source

#### 1a. User asks about a specific voice note by time (e.g., "Did you get my voice note from 9:20?")

When the user references a voice note by timestamp rather than attaching one explicitly, search `<agent-home>/audio_cache/` by modification time:

```bash
ls -lt <agent-home>/audio_cache/*.ogg <agent-home>/audio_cache/*.mp3 2>/dev/null | head -5
```

Match the file closest to the user's stated time. Files are named `audio_*.ogg` with mtime matching when the note was received. Once you've identified the right file, transcribe it (step 1b below).

**Do NOT say "I don't see a voice note" if you haven't checked audio_cache first.** The file is almost certainly there.

#### 1b. Explicit audio attachment

When the user sends an audio file through the operator agent messaging platforms, the attachment comes in this format:

```
[The user sent an audio file attachment: 'audio_abc123.mp3'. It is saved at: /<workspace> Its content is not inlined here.]
```

**The file IS there.** The path is real. Do NOT tell the user "I don't see a voice note" or "I don't have the audio file." The path in that message is a real file on disk that you can read with terminal tools.

**Transcribe immediately using whisper CLI:**

```bash
whisper /<workspace> \
  --model base --output_format txt \
  --output_dir /tmp/whisper_out --language en
```

Then read the transcript:
```bash
cat /tmp/whisper_out/audio_abc123.txt
```

**Pitfall:** If you receive the attachment format above and respond "I don't see a voice note, please resend," the user will have to send the message multiple times with growing frustration. The file path is valid. Use it.

Other source locations to check if no explicit path:
- recent audio cache or archive folders (`<agent-home>/audio_cache/`)
- any already-generated transcript files
- session context or saved memo text

If a transcript already exists, use it. Only transcribe if needed.

#### 1d. No audio file present (diagnostic path)

When the user says "pick up the voice message I just sent" but there is no file in `<agent-home>/audio_cache/` newer than the last assistant response, do NOT immediately tell the user "I don't see your voice note." Run the diagnostic first — the message is almost certainly in transit, in the wrong session, or the polling has stalled.

**Diagnostic sequence (in order):**

1. **Confirm the newest file timestamp.** `ls -lat <agent-home>/audio_cache/ | head -6`. If the newest file is hours or days old, no new voice has arrived in the cache.
2. **Check whether the gateway is alive and polling.** `ps aux | grep -iE "gateway|telegram" | grep -v grep`. The gateway process should be running. If it isn't, the message is queued on the Telegram side but not being pulled.
3. **Tail the gateway log for recent message-receipt entries.** `grep -iE "voice|audio|ogg|received.*message|Cached user voice" <agent-home>/logs/gateway.log | tail -15`. A "Cached user voice" entry confirms receipt; its absence confirms non-receipt.
4. **Determine which of three situations you are in and tell the user explicitly:**
   - **(a) Sent to Telegram, but this is a different chat surface (desktop app, CLI, etc.).** The voice is sitting in the Telegram bot's session, not this one. The user must either tell you which bot/channel, or switch into the Telegram session.
   - **(b) Sent inside the current surface but the attachment never landed.** The desktop/CLI surfaces may not pass audio attachments the same way Telegram does. Ask the user to drag-drop the file, save it to `<agent-home>/audio_cache/` manually, or type the key points.
   - **(c) Still uploading / network lag.** Unlikely if the gateway has been quiet for more than a minute, but possible. Set up a background watcher (see below) rather than polling manually.
5. **If awaiting arrival, set up a background watcher** so you are notified the moment the file lands, instead of blocking on repeated manual polls. **Match ALL audio extensions**, not just `.ogg` — Telegram can deliver `.ogg`, `.opus`, `.mp3`, `.m4a`, `.webm`, or `.wav` depending on the source device and encoding. A watcher hardcoded to `*.ogg` will silently miss an `.mp3` that landed minutes ago. Use `find` with an explicit OR-list (NOT zsh glob expansion, which floods the log with `no matches found` for each missing extension on every loop iteration):
   ```bash
   # Background watcher — silent until a new voice arrives. Matches ALL audio extensions.
   NEWEST_BASE=$(find <agent-home>/audio_cache -type f \( -name "*.ogg" -o -name "*.opus" -o -name "*.mp3" -o -name "*.m4a" -o -name "*.webm" -o -name "*.wav" \) 2>/dev/null | xargs ls -t 2>/dev/null | head -1)
   for i in $(seq 1 720); do
     sleep 10
     NEWEST_NOW=$(find <agent-home>/audio_cache -type f \( -name "*.ogg" -o -name "*.opus" -o -name "*.mp3" -o -name "*.m4a" -o -name "*.webm" -o -name "*.wav" \) 2>/dev/null | xargs ls -t 2>/dev/null | head -1)
     if [ "$NEWEST_NOW" != "$NEWEST_BASE" ] && [ -n "$NEWEST_NOW" ]; then
       echo "NEW VOICE DETECTED: $NEWEST_NOW"
       exit 0
     fi
   done
   ```
   Run via `terminal(background=true, notify_on_complete=true)` so you can keep working and are alerted on arrival.

**Pitfall — false-negative "I don't see it":** The single most frustrating failure mode is telling the user their voice note didn't arrive when in fact it went to a different session or is still in flight. Always run the diagnostic and name the specific situation (a/b/c) before asking the user to resend. They almost always did send it; the question is where it landed.

### 1c. faster-whisper Python API (fallback for long audio or when whisper CLI is unavailable)

The local STT stack uses `faster-whisper` (not the OpenAI `whisper` CLI package). The Python venv is at `/<workspace>`.

```python
from faster_whisper import WhisperModel
model = WhisperModel('base', device='cpu', compute_type='int8')
segments, info = model.transcribe('/path/to/audio.wav', beam_size=3, language='en')
for seg in segments:
    print(seg.text, end='', flush=True)
```

**Pitfall — timeout on long audio with `small` model:** A 194-second .ogg file with the `small` model timed out at 120s. The fix is a multi-part workaround:

1. **Convert to WAV first** — `faster-whisper` handles .ogg but converting to 16kHz mono WAV via ffmpeg speeds up decoding:
   ```bash
   ffmpeg -y -i audio_input.ogg -ar 16000 -ac 1 -f wav /tmp/audio_output.wav
   ```
2. **Downgrade to `base` model** — `small` is ~2x slower on CPU; `base` with `int8` quantization is the sweet spot for files under ~4 minutes. For 5-10 minute audio, `base` with `beam_size=3` and `vad_filter=True` completes in ~225s.
3. **Extend terminal timeout to 300s** — set `timeout=300` on the terminal call for any audio over 120 seconds.

**Always stream with `flush=True`** to get partial output even if the process is cut short.

**Pitfall — NumPy 2.x version conflict between venvs:** The the operator agent agent has two venvs with conflicting NumPy versions. `/<workspace>` fails with `ctranslate2` import errors because `venv-embed` (which has torch) was compiled against NumPy 2.x, causing `A module that was compiled using NumPy 1.x cannot be run in NumPy 2.4.3`. The **working** venv for faster-whisper is:

```bash
/<workspace> /tmp/transcribe_voice.py
```

This venv has `faster-whisper`, `torch`, and compatible NumPy. The `hermes-agent/venv` path picks up `venv-embed`'s torch and crashes on import. If you see the NumPy 1.x/2.x warning followed by a `ctranslate2` import traceback, switch to `venv-embed` immediately.

**Recommended transcription script** (`/tmp/transcribe_voice.py`):

```python
import time
start = time.time()
from faster_whisper import WhisperModel
print(f'[init] Loading model... elapsed={time.time()-start:.1f}s', flush=True)

model = WhisperModel('base', device='cpu', compute_type='int8')
print(f'[init] Model loaded. elapsed={time.time()-start:.1f}s', flush=True)

segments, info = model.transcribe(
    '/tmp/voice_msg.wav',
    language='en',
    beam_size=3,
    vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=500)
)
print(f'[info] Duration: {info.duration:.1f}s, lang={info.language}', flush=True)

for seg in segments:
    print(f'[{seg.start:.0f}-{seg.end:.0f}] {seg.text.strip()}', flush=True)

print(f'[done] Total elapsed: {time.time()-start:.1f}s', flush=True)
```

### 3. Segment the transcript
Split the content into five buckets:
- **Request**: the thing the user wants done
- **Context**: background, rationale, story, domain framing
- **Constraints**: explicit exclusions, naming rules, scope boundaries
- **Operating mode**: one-time answer vs persistent / ongoing support vs background monitoring
- **Noise**: repetition, digressions, implementation scaffolding that does not change the ask

### 3b. Multi-intent voice notes with corrections

When a voice note contains BOTH task requests AND personal corrections/frustrations, extract BOTH as separate intents. Do not let the task request bury the correction.

Example pattern: "Start my principal brief. Also, stop saying I haven't been doing X — we already scratched that item and I called attention to it."

Extract as:
- **Request 1**: Start principal morning brief
- **Correction**: Remove [item] from pending/overdue lists — it was previously scratched by user decision
- **Emotion signal**: Frustration at being credited for work not done

The correction is NOT context for the request — it is its own action item. Corrections about "stop doing X" or "stop saying Y" are workflow preferences that may need to be saved to memory or patched into a skill, not just acknowledged.

### 3c. If the note is about a panel, roster, or advisor decision

When the voice note is really asking for a *panel design* rather than a literal transcript summary, extract the following explicitly:
- the target panel class (e.g. product, health, strategy, growth)
- the mission or product family it must support
- the recurring decision it should improve
- the functional lanes needed on the panel
- which parts of the transcript are STT noise versus stable intent
- whether the user wants *direction/trajectory* only, or implementation/build help too
- whether the panel should answer individually first and then synthesize without deleting any major points

For noisy voice notes, prefer stable *theme clusters* over word-level transcription artifacts. If the same conceptual cluster appears multiple times in different garbled forms, treat that as signal. If a phrase is too broken to survive paraphrase, move it to noise.

### 4. Prefer the latest direct instruction
If the user later says “ignore the engine,” “just the principal context,” or “I only want the ask,” treat that as the active scope and suppress unrelated material.

### 5. Return only what is needed
When the user asks for the actual ask, respond with:
- a concise “what you want” section
- a short “what is just context” section only if helpful
- no full transcript unless explicitly requested

## Output Pattern

A strong output usually looks like:
- **What you want**
- **What is context**
- **What to ignore**
- **My confidence / ambiguity note** if needed

Keep the answer short, concrete, and faithful to the user’s scope.

## Persistent support requests

Sometimes the user's "ask" is not just a one-time answer. It may be a request to turn the topic into an always-on or long-term support loop.

When the voice note includes language like:
- 24/7
- active in the background
- ongoing coach
- continuous updates
- latest information
- research refresh
- keep it warm
- background continuity

Treat that as part of the actual request, not as incidental implementation chatter.

Extract it explicitly as a requirement such as:
- persistent mode
- monitoring / freshness tracking
- background continuity
- proactive but non-spammy updates

### Coaching-loop preference
If the user is asking for a recurring advisor, daily check-ins, or a panel that monitors their work over time, do **not** narrow the first prompt to a single-day recap unless the user explicitly asks for that. Prefer a broader intake window and enough context for meaningful synthesis, such as:
- the last 7–14 days
- what has been built recently
- what has stalled
- what is working vs. not working
- current constraints, energy, and disability load

This prevents the extraction from collapsing a durable coaching requirement into a one-off response request.

Reference: `references/persistent-support-requests.md`
Reference: `references/coaching-loop-check-in-prompts.md`

## Common Pitfalls

1. **Telling the user you can't see their audio file**
   - When the operator agent delivers an audio attachment path, the file EXISTS on disk. Use whisper CLI to transcribe it. Never ask the user to "resend" or "type out what was said."

2. **Following the stale task snapshot after context compaction (CRITICAL)**
   - After context compaction, the summary includes a "Historical Task Snapshot" and "In-Progress State." These are REFERENCE ONLY. They are NOT the user's latest request.
   - The user's most recent voice note — which may have been sent DURING the compacted window — is the actual active request. It may not appear in the compaction summary at all.
   - **Before doing ANY work after compaction**, check `<agent-home>/audio_cache/` for files newer than the last assistant response. Transcribe any unprocessed voice notes. The voice note may completely redirect the session away from the stale task list.
   - Real example: user sent a voice note at 7:08 PM asking for a PDF. Context compacted. Agent continued engine fixes from the task snapshot for several tool calls. User said "This isn't what I asked for in my last voice note." The fix: always re-scan audio_cache after compaction before continuing any task snapshot work.

3. **Repeating the engine-building story back to the user**
   - If the user says they do not need help building the engine, do not keep resurfacing engine design.

4. **Treating every named entity as the request**
   - A name may be just a label for a later system, not the actual ask.

5. **Inventing a new engine when the user is correcting an existing one**
   - When the user says "that's the one we already created" or similar, pause the invention instinct and verify the existing artifact first (session history, files, or known docs) before naming or redesigning anything.

6. **Mixing request and context into one blob**
   - Separate "what they want" from "why they want it."

7. **Over-explaining the transcript**
   - If the user wants extraction, give extraction.

8. **Ignoring correction signals**
   - If the user narrows scope mid-thread, reset the frame immediately.

9. **whisper `small` model timeout on long audio (>120s)**
   - The `small` model can exceed the default 120s terminal timeout on audio files over ~2 minutes.
   - Fix: convert to 16kHz mono WAV with ffmpeg, use `base` model with `int8` compute, extend terminal timeout to 300s.
   - See step 1c above for the full faster-whisper Python API pattern.

10. **Watcher hardcoded to one audio extension (Caught 2026-07-21)**
    - A background watcher built with `ls -t <agent-home>/audio_cache/*.ogg` missed a `.mp3` voice note that had landed 2 hours earlier, causing a false "no voice has arrived" report and a user-facing "I don't see it" message.
    - Telegram delivers voice notes as `.ogg` OR `.mp3` OR `.opus`/`.m4a`/`.webm`/`.wav` depending on the source device and encoding. Never assume a single extension.
    - Additionally, zsh glob expansion (`*.ogg *.mp3 *.m4a` in a loop) prints `no matches found` for every missing extension on every iteration, flooding the watcher log and masking real output.
    - Fix: use `find <agent-home>/audio_cache -type f \\( -name "*.ogg" -o -name "*.opus" -o -name "*.mp3" -o -name "*.m4a" -o -name "*.webm" -o -name "*.wav" \\) 2>/dev/null | xargs ls -t 2>/dev/null | head -1`. `find` handles missing extensions gracefully.

11. **Parallel-session drop (Caught 2026-08-21 — FIRST-CLASS)**
    - A voice note is processed by whichever the operator agent session receives it, which may be a PARALLEL session that dies mid-answer (model timeout, user redirect). The note never gets answered anywhere, and sessions that never saw it conclude "nothing new."
    - When the user says "you missed things from my voice note": `session_search(query="<topic>", sort="newest")` to find the note in the raw DB, scroll forward past it to check whether ANY final answer followed. If the trail ends in a timeout/interrupt + next-message redirect, the note was DROPPED — treat its full transcript as the active task list and execute it.
    - Do not re-litigate what WAS answered; diff the note's asks against what got answered and act only on the deltas.

12. **Acting on a voice transcript without checking if sibling sessions already did the work (Caught 2026-07-21 — FIRST-CLASS)**
    - A voice note sent via Telegram is typically processed by the Telegram-the operator agent session BEFORE the Desktop-the operator agent session sees it. If Desktop-the operator agent transcribes the note and immediately proposes work (a panel, a plan, a deliverable) based on the transcript, it will almost certainly DUPLICATE work Telegram-the operator agent already completed minutes earlier.
    - User signal: "Telegram the operator agent already transcribed and actioned, right??? don't duplicate work."
    - This is the EXCHANGE step of the SOLVE protocol applied to cross-session voice notes. The Mastermind Protocol requires reading sibling work before producing your own — this applies across session surfaces, not just within one.
    - **Rule:** After transcribing a voice note and BEFORE proposing any panel, plan, or deliverable based on its content, run `session_search` for the voice note's key topic with `sort="newest"` and check whether another session (especially Telegram source) produced the deliverable in the past 2-4 hours. Read the found work fully, then BUILD ON IT (extend, iterate, review) rather than rebuilding from scratch. Tell the user what you found and what you're adding — not what you're starting.

13. **Garbled transcript ≠ bad audio — verify the file before treating content as noise (Caught 2026-08-28 — FIRST-CLASS)**
    - A 2-minute principal voice note transcribed as "(sad music)" ×4 via the hardcoded `tiny` whisper model. The operator nearly discarded it as "transcription artifact or accidental send" — but the AUDIO was fine on disk (125.9s, intact).
    - **Rule:** when a transcript looks like nonsense (music tags, repeated fragments, non-words) but a real voice note was expected, FIRST verify the audio file exists and its true duration (`afinfo <file> | grep duration`), THEN re-transcribe with escalating model size. The failure is almost always the MODEL (tiny garbles this user's accent — known root cause), not the audio.
    - **Escalation path on this hardware:** `tiny` → garble; `base` → partial (opening + ~1:00 mark only, middle lost); `small` → accurate but slow (~10 min for 2 min audio on CPU — ALWAYS run as `terminal(background=true, notify_on_complete=true)`, never foreground; it WILL blow a 420s foreground timeout).
    - Duration mismatch is a second signal: the user said "over 2 minutes," the fragment played back was 29 seconds — upstream clipping plus model garble compound. When the user reports the transcript doesn't match what they said, trust their testimony over the transcription (testimony > sensors).
    - The accent-vs-model failure has a standing root-cause fix in the Glial lane (adaptive STT routing); until it ships, assume `tiny` output from this user is unreliable and escalate models proactively rather than asking the user to repeat themselves.
    - **The reverse case — audio that really IS mostly music (2026-08-28):** sometimes the garble is honest. Forensic sequence when escalation keeps producing garbage: (1) `ffmpeg -i <file> -af volumedetect -f null -` — mean volume near −50dB means the mic barely captured voice; (2) boost and re-run (`-af "highpass=f=80,lowpass=f=7500,volume=30dB,loudnorm" -ar 16000`); (3) if the strong model then emits a HALLUCINATION LOOP (the same short phrase repeating — "It's a B" over dozens of 2-second segments), that is Whisper's signature on non-speech audio, not an accent problem. Real speech exists only in the fragments that STAY STABLE across model sizes (here: the opening "So, I want you to look at…" and one line near 1:00). Verdict pattern: background music with snatches of voice (pocketed phone, mic covered, music over speech). Correct response: ask for a re-record with mic clear — NEVER reconstruct intent from two fragments plus a guess. Also flag to the user when playback duration ≠ file duration (a 2:06 file served back as a 29-second clip = upstream clipping, a separate defect worth logging).

## Verification

Before finalizing, ask:
- Did I capture the user’s actual desired outcome?
- Did I suppress implementation detail when asked?
- Did I preserve important constraints and names?
- Did I avoid turning the extract into a plan unless asked?

## References

- See `references/transcript-segmentation.md` for a compact request-vs-context rubric and a worked example.
- See `references/product-panel-voice-note-notes.md` for a concise extraction guide when the voice note is noisy but the ask is really about building a product/advisor panel.
- See `references/engine-correction-handling.md` for a session-based note on correcting invented engine names and re-centering on the existing artifact.
- See `references/post-compaction-request-recovery.md` for the protocol to recover the user's actual latest request after context compaction has buried it.
