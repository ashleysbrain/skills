---
name: debug-voice-transcription-gateway
description: "Debug voice message transcription AND audio playback issues in the operator agent gateway and desktop app. Covers STT transcription failures (gateway polling, provider config, macOS OMP/TCC) and TTS playback failures (macOS CoreAudio + Bluetooth HFP). Three failure modes — gateway voice messages, desktop mic input, desktop audio output."
tags: [debugging, gateway, voice, stt, transcription, hermes-agent]
version: 1.0
---

# Debug Voice Transcription in Gateway

## When to Use

User reports voice messages are not being transcribed, agent doesn't respond to voice content even though STT is configured, OR the dictation/mic button in the the operator agent One desktop app doesn't produce text, OR TTS playback produces no sound in the desktop app. Covers three failure modes that share the same desktop app and voice pipeline but have different root causes — gateway voice messages (Causes A-E), desktop mic input (Cause F), and desktop audio output (Cause G).

## Symptoms

- User sends voice messages via Telegram/Discord/WhatsApp
- Agent responds as if no voice was sent
- No voice content appears in agent responses
- User believes transcription is broken

## Diagnostic Approach

**FIRST: Determine whether the problem is message reception or transcription.** These are different failure modes with different root causes.

- **Reception failure** (gateway polling stalled): No "Cached user voice" entry near the user's reported send time. No inbound messages at all. Gateway process is alive but silent. See **Cause D**.
- **Transcription failure** (message received but not transcribed): "Cached user voice" IS in the log, but no "Processing audio" or "Detected language" follows. See **Cause B2** (most common on macOS) or **Cause C2**.

### Step 1: Check Gateway Health (reception vs transcription)

Look for transcription activity in gateway logs:

```bash
tail -200 <agent-home>/logs/gateway.log | grep -i "voice\|transcri\|audio"
```

**Key indicators:**
- `[Telegram] Cached user voice at` → Voice messages ARE being received
- `Processing audio with duration` → Transcription IS running  
- `Detected language 'en'` → Transcription completed successfully

**What absence means:**
- No "Cached" → Voice not reaching gateway
- "Cached" but no "Processing" → Transcription failed silently
- "Processing" but no "Detected" → STT provider issue

### Step 2: Find Cached Audio

```bash
ls -lt <agent-home>/audio_cache/*.ogg | head -10
```

This shows recent voice messages. If files exist, voice reception works.

### Step 3: Manual Transcription Test

Create test script to verify transcription engine works:

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, str(__file__).replace('test.py', '.hermes/hermes-agent'))

from tools.transcription_tools import transcribe_audio

# Test most recent voice file
result = transcribe_audio("/path/to/audio_file.ogg")
print("Success:", result.get("success"))
if result.get("success"):
    print("Transcript:", result.get("transcript")[:200])
else:
    print("Error:", result.get("error"))
```

**Interpretation:**
- ✅ Transcript prints → Transcription works, bug is in gateway→agent handoff
- ❌ Error prints → STT provider needs configuration

### Step 4: Test Multiple Messages

Batch test to find patterns:

```python
from pathlib import Path
audio_dir = Path.home() / ".hermes/audio_cache"
recent = sorted(audio_dir.glob("*.ogg"), 
                key=lambda x: x.stat().st_mtime, 
                reverse=True)[:5]

for f in recent:
    result = transcribe_audio(str(f))
    print(f"{f.name}: {'✓' if result.get('success') else '✗'}")
```

## Common Root Causes

### Cause A: Gateway→Agent Context Handoff Bug

**Signature:**
- ✅ Logs show transcription completed
- ✅ Manual test produces transcript
- ❌ Agent doesn't see voice content

**Root cause:** Enriched message text with transcript not passed to agent loop.

**Location to check:** `gateway/run.py` function `_enrich_message_with_transcription` around line 2347-2349 and 4694-4775.

**Fix:** Verify enriched `message_text` is used in agent call, not original message.

### Cause B: STT Not Configured

**Signature:**
- ❌ No "Processing audio" in logs
- ❌ Manual test fails with "No STT provider"

**Fix:** Install faster-whisper or configure API provider in the operator agent config.

### Cause B2: macOS Intel OMP Conflict (SILENT KILLER)

**Signature:**
- ✅ Voice messages ARE cached in audio_cache
- ✅ STT is configured (stt.enabled: true, provider: local)
- ✅ faster_whisper is installed
- ❌ NO "Processing audio" or "Detected language" in logs — ever
- ❌ Agent receives placeholder text instead of transcript
- ❌ Manual `transcribe_audio()` test crashes with: `OMP: Error #15: Initializing libiomp5.dylib, but found libiomp5.dylib already initialized`

**Root cause:** On macOS (especially Intel), faster-whisper/ctranslate2 loads Intel's OpenMP runtime (`libiomp5.dylib`), which clashes with another copy already loaded by NumPy or another library. The error is FATAL — it kills the transcription thread silently. The exception gets caught by the gateway's `except Exception` block, so it looks like transcription "ran" but produced nothing.

**Fix (already applied in tools/transcription_tools.py):** `os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")` at module top, before any faster_whisper import. Also add to launchd plist EnvironmentVariables + `launchctl setenv KMP_DUPLICATE_LIB_OK TRUE` for belt-and-suspenders.

**How to verify:** Run `transcribe_audio()` on any .ogg in audio_cache in a clean subprocess (no KMP env pre-set). If it returns a transcript, the fix is live.

### Cause C2: STT Provider Set to Cloud with Empty API Keys

**Signature:**
- ✅ Voice messages ARE cached in audio_cache
- ✅ `stt.enabled: true` in config.yaml
- ❌ Provider is `openai` (or `groq`, `mistral`, `elevenlabs`) but the corresponding API key in `.env` is **empty**
- ❌ Gateway log shows: `Skipping legacy unprefixed voice mode key` warning, then gateway restarts/crashes
- ❌ Inbound message shows `msg=''` (empty — no transcript was prepended)

**Root cause:** STT provider is configured to use a cloud API (OpenAI whisper-1, Groq, etc.) but the API key environment variable is empty. Every voice note triggers a transcription attempt that fails immediately, and the enriched message arrives as empty text.

**How to diagnose:**
```bash
# Check which provider is configured
grep -A5 "^stt:" <agent-home>/config.yaml

# Check if the corresponding key is set
grep -i "VOICE_TOOLS_OPENAI_KEY\|OPENAI_API_KEY\|GROQ_API_KEY" <agent-home>/.env
```

If the key line shows `KEY=` with nothing after the equals, that's the problem.

**Fix — switch to local provider (free, no API key):**
```bash
hermes config set stt.provider local
```

Then verify faster-whisper is installed in the the operator agent venv:
```bash
/<workspace> -c "import faster_whisper; print('OK')"
```

If missing:
```bash
/<workspace> -m pip install faster-whisper
```

Restart the gateway after switching providers.

**When to keep cloud instead:** Only switch to `local` if you don't have API keys. If you DO have a valid OpenAI key, set it in `.env` as `VOICE_TOOLS_OPENAI_KEY=sk-...` and keep the `openai` provider. Local whisper uses CPU and is slower but free.

### Cause C3: faster-whisper Installed in Wrong Venv (2026-07-12)

**Signature:**
- STT provider is `local` in config
- faster-whisper IS installed (but in system Python or venv-embed, not the the operator agent venv)
- Transcriptions still fail silently or timeout
- `python3 -c "from faster_whisper import WhisperModel"` works but the operator agent can't import it

**Root cause:** the operator agent runs from `<agent-home>/hermes-agent/venv` (Python 3.11). If faster-whisper was installed via `pip3 install faster-whisper` it goes to system Python (3.14), NOT the the operator agent venv. The the operator agent process cannot see it.

**Fix:**
```bash
<agent-home>/hermes-agent/venv/bin/pip install faster-whisper
```

Then verify:
```bash
<agent-home>/hermes-agent/venv/bin/python -c "from faster_whisper import WhisperModel; print('OK')"
```

**System Python 3.14 cannot install faster-whisper** because the `av` dependency fails to build on 3.14. The the operator agent venv (3.11) builds it fine. Do NOT attempt to install into system Python.

**After installing, the running the operator agent process must restart** to pick up the new module. If you cannot restart, use the fallback whisper binary as a manual transcription bridge until the next restart.

### Cause C: Audio Corruption

**Signature:**
- ✅ Voice cached
- ❌ Transcription fails with format error

**Check:** Verify audio files are valid Ogg/Opus format with file command.

### Cause D: Gateway Polling Stall (SILENT — no error, no messages received)

**Signature:**
- ❌ No "Cached user voice" entry near the timestamp the user reported sending
- ❌ No inbound messages in gateway.log for an extended period
- ✅ Gateway process IS alive (`ps aux | grep "gateway run"`)
- ❌ Cron ticker and kanban dispatcher entries stopped appearing in gateway.log
- ❌ No error or traceback in gateway.error.log — the stall is completely silent

**Root cause:** The Telegram `python-telegram-bot` Updater can enter a wedged state where `Updater.running=True` but the underlying long-poll consumer task is dead. No `error_callback` fires in this state, so the reconnect ladder never engages. The gateway process stays alive but stops receiving ALL messages — voice, text, everything — indefinitely.

Before the watchdog fix (Jun 2026), Telegram had only a one-shot health probe (`_verify_polling_after_reconnect`) that runs once 60s after a reconnect. It did NOT continuously monitor polling health. Slack already had `_socket_watchdog_loop`; Telegram did not. This asymmetry meant Telegram could silently die while Slack self-healed.

**Diagnostic steps:**

1. **Check if gateway is alive but stalled:**
```bash
ps aux | grep "gateway run" | grep -v grep
```
Process exists? It may be stalled, not crashed.

2. **Check last activity timestamp vs current time:**
```bash
tail -20 <agent-home>/logs/gateway.log
```
If the last log entry is more than 5-10 minutes old and no "Cron ticker" entries are recent, the event loop or polling is wedged.

3. **Check audio_cache for the missing message:**
```bash
ls -lt <agent-home>/audio_cache/ | head -10
```
If the user's message isn't here, it was never received (polling was already dead). If it IS here but no inbound message follows in gateway.log, it was cached by a dying gateway right before the stall completed — Telegram marked it delivered and won't redeliver.

4. **Confirm no crash:**
```bash
grep -i "error\|traceback\|exception" <agent-home>/logs/gateway.error.log | tail -10
```
Silent stall = no error entries at the stall time.

**Fix:**
- **Immediate:** `hermes gateway restart` to clear the wedge.
- **Permanent (already in main post-Jun 2026):** The `_polling_watchdog_loop` in `gateway/platforms/telegram.py` runs every 5 minutes, probes `Updater.running` + `getMe()` with a tight timeout, and triggers reconnect on failure. If this method doesn't exist in the codebase, the fix hasn't been applied yet — see `references/telegram-polling-watchdog-fix.md` for the patch.

**Critical:** Messages sent during a polling stall are acknowledged by Telegram before the gateway processes them. After restart, Telegram will NOT redeliver them. You must manually transcribe from audio_cache if the file landed there, or ask the user to resend.

See `references/telegram-polling-watchdog-fix.md` for the full code patch that prevents this stall.

### Cause F: Desktop App Voice Input — macOS Microphone Permission (TCC)

**Surface:** the operator agent One desktop (Electron) app, NOT the messaging gateway. The
dictation button in the chat composer produces no text or silently fails.

**Signature:**
- ✅ Backend transcription works (test `transcribe_audio()` on a cached file — succeeds)
- ✅ STT config is correct (`stt.enabled: true`, `provider: local`)
- ❌ Zero transcription requests appear in `<agent-home>/logs/gui.log` after the user tries the mic button
- ❌ Audio never reaches the `/api/audio/transcribe` endpoint

**Root cause:** macOS TCC microphone permission for `com.nousresearch.hermes`
was denied, dismissed, or reset by an OS update. When `getUserMedia()` is
blocked, the recording never starts and no audio is sent to the backend.

**Fix:**
```bash
tccutil reset Microphone com.nousresearch.hermes
```
Then have the user fully quit (Cmd+Q) and reopen the app. The macOS mic
prompt will appear on first dictation attempt — click **Allow**.

If no prompt appears, direct the user to **System Settings → Privacy &
Security → Microphone** and toggle the operator agent One on manually.

**Diagnostic shortcut:** If the backend transcription test succeeds but
`gui.log` shows zero transcription requests, skip straight to the TCC reset.
See `references/desktop-voice-input-debugging.md` for the full pipeline
trace, key file map, and Intel Mac performance notes.

### Cause G: Desktop App Audio Output — TTS Playback Fails (macOS CoreAudio + Bluetooth)

**Surface:** the operator agent One desktop (Electron) app, voice conversation mode.
The mic works (transcription succeeds), but no sound plays back when the
assistant tries to speak. The backend generates audio fine.

**Signature:**
- ✅ Backend TTS works (agent.log shows `.ogg`/`.mp3` generated)
- ✅ `/api/audio/speak` returns valid base64 audio when tested with auth
- ✅ Mic input works (transcription requests appear in `gui.log`)
- ❌ No sound from the desktop app during voice conversation
- ❌ macOS Console shows `AudioConverter SetProperty returned ...` errors

**Root cause:** When voice-conversation activates the mic, Bluetooth
headphones (AirPods) switch to Hands-Free Profile (HFP) at 24kHz mono. On
macOS 26+, the rewritten CoreAudio rejects the sample-rate-converter
properties for this Bluetooth HFP configuration, causing `new Audio().play()`
to fail silently.

**Diagnostic shortcut:** Run `log show --predicate 'process CONTAINS
"the operator agent"' --last 30m | grep -iE "AudioConverter"` and check
`system_profiler SPAudioDataType` for `SampleRate: 24000` + `Channels: 1`
(HFP mode). Also check `app-update.yml` in the installed app for fork
identity — stale third-party builds have worse macOS 26 compatibility.

**Fix (immediate, no rebuild):** Switch audio output from AirPods to
MacBook Pro Speakers. Or switch the mic to the built-in mic so AirPods
stay in A2DP stereo. **System Settings → Sound → Output.**

**Fix (permanent):** Rebuild the official desktop app from source if
running a stale third-party fork (`cd apps/desktop && npm ci && npm run dist:mac`).

No backend or renderer code change fixes this — it is an OS-layer CoreAudio
property rejection. See `references/desktop-audio-output-debugging.md` for
the full diagnostic path, CoreAudio error-code decoding, and the three
failure-mode classification table.

### Cause E: Gateway Process Killed by System (OOM/Killer)

**Signature:**
- ❌ No "Cached user voice" entry near the timestamp the user reported sending
- ❌ No inbound messages in gateway.log for an extended period
- ❌ Gateway process NOT alive (`ps aux | grep "gateway run" | grep -v grep` shows nothing)
- ✅ Evidence in logs of process being killed by signal (SIGTERM, SIGKILL) or OOM killer
- ❌ Cron ticker and kanban dispatcher entries stopped appearing in gateway.log
- ✅ High system load reported in logs just before process death

**Root cause:** The gateway process consumes too much memory or CPU, causing the operating system to kill it. On macOS, this can happen when system load average gets very high (consistently > number of CPU cores). The kernel's OOM killer or launchd/watchdog may terminate the process.

**How to diagnose:**
1. Check if gateway process is running:
   ```bash
   ps aux | grep "gateway run" | grep -v grep
   ```
2. Look for kill signals in logs:
   ```bash
   grep -i "signal\\|SIGTERM\\|SIGKILL\\|killed\\|exited with code" <agent-home>/logs/gateway.log | tail -10
   ```
3. Check for high load averages just before death:
   ```bash
   # Look for load warnings in logs
   grep -i "loadavg\\|load average" <agent-home>/logs/gateway.log | tail -10
   ```
4. Verify audio files exist for the missing time period:
   ```bash
   ls -lt <agent-home>/audio_cache/ | head -10
   ```

**Fix:**
- **Immediate:** `hermes gateway restart` to bring the gateway back online.
- **Diagnose resource usage:** Monitor memory and CPU usage of the gateway process over time.
- **Reduce load:** If running heavy workflows, consider:
  - Spreading out cron jobs
  - Reducing concurrent agent tasks
  - Increasing system resources (RAM/CPU)
  - Optimizing heavy skills/workflows
- **Check for memory leaks:** Look for steadily increasing memory usage in gateway logs

**Note:** Messages sent during the downtime when the gateway was killed are acknowledged by Telegram before the gateway processes them. After restart, Telegram will NOT redeliver them. You must manually transcribe from audio_cache if the file landed there, or ask the user to resend.

## Resolution Verification

1. Send test voice message
2. Check logs for full transcription pipeline
3. Verify agent response references voice content
4. Look for enrichment markers in logs

## Key Insight

Voice transcription often works perfectly but fails to reach agent due to context handoff bugs, not STT failures. Test the full pipeline, not just transcription in isolation.

## Intent Extraction from Mixed Voice Memos

When a user asks you to pull *only* the target context from a voice memo, do not mirror the whole transcript back. Split the memo into:
- **target need** — the actual thing the user wants built, decided, or solved
- **architecture/context** — implementation notes, background rationale, and system design discussion
- **explicit exclusions** — what the user said they do *not* want included

For coaching- or role-selection memos, keep only the role, scope, and outcome language. Strip out engine-build talk unless the user explicitly asked for architecture details.

See `references/voice-note-context-extraction.md` for a compact extraction pattern and a worked example.

## Proactive Fallback: Scan audio_cache When Voice Notes Go Missing

When the user says "you're not transcribing my voice notes" or "I sent a voice note at [time]" and no audio attachment appeared in the message context, the file almost always still landed in `<agent-home>/audio_cache/`. Do NOT tell the user you didn't receive it. Do the following immediately:

### Step 1: Scan audio_cache by timestamp

```bash
ls -lt <agent-home>/audio_cache/ | head -20
```

Match the file timestamp to the time the user reported. Files are named `audio_<hash>.ogg` or `audio_<hash>.mp3`. The most recent file is usually the one they're referring to.

### Step 2: Transcribe with whisper CLI (fallback)

```bash
whisper <agent-home>/audio_cache/audio_<hash>.ogg \
  --model tiny --output_format txt \
  --output_dir /tmp/whisper_out --language en
```

**Use `--model tiny` first** — it's much faster and usually sufficient for clear single-speaker notes. Fall back to `--model base` only if tiny produces garbage. The `base` model can take 2+ minutes on a 5-minute note on CPU.

### Step 3: Action the transcript

Read the transcript, itemize the asks, and start working on them. Do not ask the user to resend.

### Why this matters

The user sends voice notes as their primary input method. When the gateway transcription pipeline fails silently (handoff bug, provider timeout, model download), the audio file is still cached. The agent should proactively scan and transcribe rather than reporting "no audio received." The user's explicit correction: "You're not transcribing my voice notes anymore. You're broken." This is a first-class workflow failure, not a minor inconvenience.

## Direct Python Transcription (for long voice notes or gateway bypass)

When the gateway transcription pipeline is unreliable and you need to
manually transcribe a long voice note (5+ minutes), use a standalone
Python script with faster-whisper. This bypasses the gateway entirely
and gives you the full transcript in one shot.

### Step 1: Convert ogg to wav with ffmpeg

faster-whisper works more reliably on converted WAV:

```bash
ffmpeg -i <agent-home>/audio_cache/audio_<hash>.ogg \
  -ar 16000 -ac 1 -y /tmp/voice_msg.wav
```

16kHz mono is the optimal format for whisper. This takes seconds.

### Step 2: Write a transcription script

```python
#!/usr/bin/env python3
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
print(f'[info] Duration: {info.duration:.1f}s', flush=True)

full_text = []
for seg in segments:
    print(f'[{seg.start:.0f}-{seg.end:.0f}] {seg.text.strip()}', flush=True)
    full_text.append(seg.text.strip())

print('\n=== FULL TRANSCRIPT ===')
print(' '.join(full_text))
```

### Step 3: Run with the correct Python venv

**CRITICAL**: The the operator agent venv (`<agent-home>/hermes-agent/venv/bin/python3.11`)
may have NumPy version conflicts that cause silent crashes. Use the
embed venv instead:

```bash
<agent-home>/venv-embed/bin/python3 /tmp/transcribe_voice.py
```

**If venv-embed also fails** with `NumPy 1.x cannot run on NumPy 2.x`,
the conflict is between ctranslate2 (compiled against NumPy 1.x) and
the venv's NumPy 2.x. The fix: use `compute_type='int8'` (pure CPU,
no NumPy tensor operations) and ignore the warning. The transcription
will still work despite the NumPy compatibility warning.

**Key parameters for long audio (5+ minutes):**
- `vad_filter=True` — essential, skips silence, 3-4x faster
- `vad_parameters=dict(min_silence_duration_ms=500)` — avoids splitting on natural pauses
- `beam_size=3` — good accuracy/speed tradeoff (default 5 is slower)
- `language='en'` — skip language detection, saves time
- `model='base'` — good balance. Use `'tiny'` for quick scan, `'small'` for accuracy on poor audio
- Timeout: a 10-minute audio file takes ~3-4 minutes with `base` model on CPU

### Step 4: Background execution for long audio

For audio files over 3 minutes, run in background with notification:

```bash
terminal(
  background=True,
  notify_on_complete=True,
  command="<agent-home>/venv-embed/bin/python3 /tmp/transcribe_voice.py"
)
```

The notification fires when transcription completes. Do NOT block
the foreground on audio over 5 minutes — it will timeout at 300s.

### When to use whisper CLI vs direct Python

- **whisper CLI** (`whisper file.ogg --model tiny`): Quick, one-off,
  audio under 2 minutes. Requires whisper installed in system PATH.
- **Direct Python** (faster-whisper script): Long audio (2+ minutes),
  need VAD filtering, need timestamped segments, gateway is unreliable.
  Use the embed venv to avoid NumPy conflicts.

## Pitfalls

- Don't assume transcription is broken - verify it's running first
- **Don't assume the message was received** — if there's no "Cached user voice" entry near the user's reported timestamp, the gateway polling is stalled (Cause D), not transcription
- Gateway logs split between gateway.log and gateway.error.log
- Old successful transcriptions don't prove current ones work
- Provider changes require gateway restart
- First faster-whisper use downloads models (~100MB)
- **NEVER** tell the user you didn't receive a voice note without first checking audio_cache — the file is almost always there
- **ALWAYS** use `--model tiny` before `--model base` for fallback transcription — base model times out on longer notes (120s+)
- **Messages sent during a polling stall are NOT redelivered** by Telegram after restart. The gateway acknowledged them before dying. Transcribe from audio_cache or ask user to resend.
- **Polling stalls produce NO error logs** — checking gateway.error.log and finding nothing does NOT mean the gateway is healthy. Check gateway.log for recent activity timestamps instead.
- **Desktop voice input failure is almost always macOS mic permission (TCC), not the transcription backend.** Before debugging STT config, check `gui.log` for transcription requests. Zero requests = audio capture blocked = `tccutil reset Microphone com.nousresearch.hermes` + app restart. See Cause F.
- **Desktop audio output failure (TTS playback) is almost always a Bluetooth HFP/CoreAudio issue, not the TTS backend or the renderer code.** Before debugging the Electron audio chain, check macOS Console for `AudioConverter SetProperty` errors and `system_profiler SPAudioDataType` for 24kHz mono HFP mode. The backend almost always works — test `/api/audio/speak` with auth to rule it out, then focus on the OS/device layer. See Cause G and `references/desktop-audio-output-debugging.md`.
- **"Audio doesn't work" has THREE distinct failure modes.** Determine which before debugging: (1) gateway voice messages not transcribed → Causes A-E, (2) desktop mic not capturing → Cause F, (3) desktop TTS not playing → Cause G. All three share the voice conversation feature but need completely different fixes.
- **faster-whisper must be installed in the operator agent's own venv (`<agent-home>/hermes-agent/venv`), NOT system Python.** System Python 3.14 cannot build the `av` dependency. If STT provider is `local` but transcriptions silently fail, verify the install with `<agent-home>/hermes-agent/venv/bin/python -c "from faster_whisper import WhisperModel"`. See `references/faster-whisper-venv-fix.md` for the full diagnosis chain and the image-reading curl fallback for vision_analyze failures.
- **Bulk voice message loss is detectable via state.db audit (2026-07-16).** When the user reports missing instructions and you suspect lost voice messages, query `state.db` directly: `SELECT count(*) FROM messages WHERE content = '[voice message could not be transcribed]' AND timestamp > strftime('%s', '2026-07-14')`. A count > 5 signals a transcription pipeline failure during that window. These messages represent LOST user instructions that were never processed. The audio files may still be in `<agent-home>/audio_cache/` — scan and manually transcribe them.
