# Desktop App Voice Input Debugging

When the user reports that voice input (dictation button) doesn't work in the
the operator agent One desktop (Electron) app on macOS. The backend transcription engine
is the same `transcribe_audio()` function the gateway uses, so STT config and
provider issues are ruled out by the standard diagnostic steps. The failure
mode is almost always at the audio-capture layer.

## Pipeline (how desktop voice input works)

1. User clicks mic button in the composer (`use-voice-recorder.ts` → `use-mic-recorder.ts`)
2. Renderer calls `window.hermesDesktop.requestMicrophoneAccess()` → IPC → Electron main (`systemPreferences.askForMediaAccess('microphone')`)
3. Chromium `getUserMedia({ audio: {...} })` starts a `MediaRecorder` stream
4. On stop, the audio `Blob` is POSTed to `/api/audio/transcribe` on the backend web server
5. Backend calls `transcribe_audio()` from `tools/transcription_tools.py`
6. Transcript is inserted into the composer input field

## Diagnostic: Is the request reaching the backend?

```bash
# The desktop backend writes to gui.log (NOT gateway.log)
grep -iE "transcri|audio" <agent-home>/logs/gui.log | tail -20
```

If **zero** transcription entries appear after the user tried the dictation
button, the audio never reached the backend. The failure is at audio capture
(mic permission), not transcription. Skip to "Fix: macOS Mic Permission" below.

If transcription entries DO appear but produce errors, use the standard STT
diagnostic steps (test `transcribe_audio()` directly on a cached file).

## Fix: macOS Microphone Permission (TCC)

This is the #1 root cause for desktop voice input failures on macOS.

```bash
# Reset the permission for the the operator agent bundle ID
tccutil reset Microphone com.nousresearch.hermes
```

Then tell the user to:
1. **Fully quit** the operator agent One (Cmd+Q, not just close the window)
2. **Reopen** it
3. Click the **mic button** in the chat composer
4. macOS will prompt: *"the operator agent One" Would Like to Access the Microphone* — click **Allow**

If no prompt appears, direct the user to **System Settings → Privacy & Security
→ Microphone** and toggle the operator agent One on manually.

### Confirming TCC state via system log (no user interaction needed)

Before asking the user to try the mic button, you can check whether macOS
has EVER been asked for mic permission by the operator agent. This avoids a round-trip
with the user:

```bash
# Quick check: does the operator agent appear in TCC mic logs at all?
log show --predicate \
  'process CONTAINS "the operator agent" AND eventMessage CONTAINS "kTCCServiceMicrophone"' \
  --last 2h --style compact 2>/dev/null | head -5
```

If this returns **nothing** but you DO see other TCC entries (Calendar,
Reminders, AddressBook) for the operator agent, it confirms the mic permission was
never requested OR was denied and macOS is silently blocking it (won't
re-prompt). Skip straight to the `tccutil reset` above.

Note: `log show` with `--info --debug` and a broad predicate can take 60+
seconds on macOS; keep the predicate narrow and the time window short.

## Why this happens

macOS requires explicit per-app microphone permission (TCC). The permission
can be denied or lost when:
- The user dismissed the initial prompt
- A macOS update reset TCC entries
- The app was reinstalled or updated

When permission is denied, `getUserMedia()` throws `NotAllowedError`, which
the mic recorder hook catches and surfaces as a notification ("Microphone
permission was denied"). But if the user doesn't notice the notification or
the bridge (`requestMicrophoneAccess`) silently returns false, the recording
never starts.

## Verifying the backend is not the problem

Before assuming mic permission, quickly confirm the backend works at two
levels: the Python function and the HTTP endpoint with auth.

### Level 1: Test transcribe_audio() directly

```bash
# Test transcription on a cached audio file
/<workspace> -c "
import sys; sys.path.insert(0, '/<workspace>')
from tools.transcription_tools import transcribe_audio
import glob, os
files = sorted(glob.glob(os.path.expanduser('<agent-home>/audio_cache/*.ogg')), key=os.path.getmtime, reverse=True)
if files:
    r = transcribe_audio(files[0])
    print('success:', r.get('success'))
    if r.get('success'): print('transcript:', r.get('transcript','')[:200])
    else: print('error:', r.get('error'))
"
```

### Level 2: Test the desktop backend HTTP endpoint with auth

The desktop backend runs on an ephemeral port with a random session token.
To test the exact `/api/audio/transcribe` route the renderer calls (proving
the FastAPI route + auth middleware + transcription chain all work):

```bash
# 1. Find the desktop backend PID and its ephemeral port
lsof -iTCP -sTCP:LISTEN -P -n | grep python

# 2. Extract the auth token from the process environment
PID=<pid_from_above>
TOKEN=$(ps -E -p $PID | grep -o 'HERMES_DASHBOARD_SESSION_TOKEN=[^ ]*' | cut -d= -f2)
PORT=<port_from_lsof>

# 3. Base64-encode a test audio file and POST it
AUDIO_B64=$(base64 < <agent-home>/audio_cache/audio_<hash>.ogg)
curl -s -w '\nHTTP:%{http_code}' \
  -X POST -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"data_url\":\"data:audio/ogg;base64,$AUDIO_B64\",\"mime_type\":\"audio/ogg\"}" \
  "http://127.0.0.1:$PORT/api/audio/transcribe"
```

A `HTTP:200` with a JSON transcript proves the entire backend chain is
healthy — route registration, session-token auth, and transcription all
work. The issue is then definitively at the audio-capture (mic permission)
layer.

**Shortcut:** If Level 1 succeeds, you almost never need Level 2. Reserve
Level 2 for cases where you suspect a route registration or auth middleware
regression.

## Key files in the desktop voice pipeline

| File | Role |
|------|------|
| `apps/desktop/src/app/chat/composer/hooks/use-voice-recorder.ts` | Orchestrates record → transcribe → insert |
| `apps/desktop/src/app/chat/composer/hooks/use-mic-recorder.ts` | Low-level `MediaRecorder` + `getUserMedia` |
| `apps/desktop/src/app/session/hooks/use-hermes-config.ts` | Reads `stt.enabled` → gates `sttEnabled` (defaults to `true`) |
| `apps/desktop/src/app/session/hooks/use-prompt-actions.ts` | `transcribeVoiceAudio` callback → `transcribeAudio()` |
| `apps/desktop/src/hermes.ts` | `transcribeAudio()` — POSTs to `/api/audio/transcribe` |
| `apps/desktop/electron/preload.cjs` | `requestMicrophoneAccess` IPC bridge |
| `apps/desktop/electron/main.cjs` | `systemPreferences.askForMediaAccess('microphone')` handler |
| `hermes_cli/web_server.py` | Backend `/api/audio/transcribe` endpoint |
| `tools/transcription_tools.py` | Core transcription (includes KMP fix for Intel Mac) |

## Note on Intel Mac performance

On Intel CPUs (e.g., i7-9750H), the `tiny` Whisper model takes ~5-7 seconds
per short message. This is normal for CPU inference. If the user wants faster
results, switch to Groq's free Whisper API:

```bash
hermes config set stt.provider groq
# Set GROQ_API_KEY in <agent-home>/.env (free tier available)
```

Then restart the desktop app backend.
