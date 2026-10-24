# Desktop Audio Output (TTS Playback) Debugging

When voice conversation mode in the the operator agent One desktop app activates the mic
but no sound plays back (TTS). The backend generates audio fine; playback
fails silently in Chromium's audio service.

## The TTS Playback Chain

```
Renderer (voice-playback.ts)
  → speakText() → window.hermesDesktop.api({path: '/api/audio/speak'})
    → Electron IPC (main.cjs) → backend (web_server.py:2452)
      → text_to_speech_tool() → Edge TTS → returns base64 data_url
  ← new Audio(data_url).play()  ← FAILURE POINT
```

The backend always works. The failure is in Chromium's audio output path.

## Diagnostic Path

### Step 1: Check macOS Console for AudioConverter errors

```bash
log show --predicate 'process CONTAINS "the operator agent"' --last 30m \
  2>/dev/null | grep -iE "audio|AudioConverter|coreaudio" | tail -20
```

If you see lines like:

```
the operator agent Agent Helper: (AudioToolboxCore) AudioConverter -> 0x...:
  The <private> SetProperty call returned 1886547824 for property 1936876385 with size 4.
```

Chromium's audio service is failing to configure the sample-rate converter
for the output device. This is a SILENT failure — `new Audio().play()`
fires the `error` event but the user sees nothing.

### Step 2: Decode the CoreAudio error codes

The error codes are OSType fourcc values (big-endian uint32 → ASCII):

```python
codes = [1886547824, 1936876385, 1936876401, 1886547309]
for c in codes:
    fourcc = ''.join(chr((c >> (8*i)) & 0xFF) for i in range(3, -1, -1))
    print(f'  {c} = {repr(fourcc)}')
# 1886547824 = 'prop'  ( SetProperty itself failed )
# 1936876385 = 'srca'  ( sample-rate converter complexity )
# 1936876401 = 'srcq'  ( sample-rate converter quality )
# 1886547309 = 'prmm'  ( prime method )
```

If you see `srca` / `srcq` / `prmm` — the sample-rate converter is rejecting
the output device configuration. This points to a Bluetooth HFP issue.

### Step 3: Check output device for Bluetooth HFP mode

```bash
system_profiler SPAudioDataType 2>/dev/null | \
  grep -A5 "Default Output\|Output:\|SampleRate\|Channels\|Transport"
```

**Red flags (indicates HFP mode):**
- `Current SampleRate: 24000` (normal is 44100 or 48000)
- `Output Channels: 1` (normal stereo is 2)
- Device name contains "AirPods" or "Bluetooth"

When voice-conversation mode activates the microphone, Bluetooth headphones
(AirPods) switch from high-quality A2DP stereo (48kHz) to bidirectional
Hands-Free Profile (HFP) at 24kHz mono. macOS 26+ rewrote CoreAudio
("HostedDSP") and the new implementation rejects the SRC property set for
this Bluetooth HFP configuration → silent playback failure.

### Step 4: Verify the installed app is the official build

```bash
# Check version
defaults read "/Applications/the operator agent One.app/Contents/Info" CFBundleShortVersionString

# Check if it's a third-party fork (NOT the official Nous Research build)
cat "/Applications/the operator agent One.app/Contents/Resources/app-update.yml" | grep "owner"
```

If `owner:` is NOT `nousresearch` (e.g., `fathah`), the user is running a
third-party fork that may be stale (old Electron/Chromium with worse macOS
26 compatibility). The official source is at `<agent-home>/hermes-agent/apps/desktop`.

### Step 5: Rule out backend failure

Test the TTS endpoint directly with the dashboard session token:

```bash
# Find the active token (embedded in dashboard HTML served by the gateway)
curl -s http://127.0.0.1:<gateway_port>/ | grep -o 'sessionToken.*' | head -1

# Test the speak endpoint with auth
curl -s -X POST "http://127.0.0.1:<gateway_port>/api/audio/speak" \
  -H "Content-Type: application/json" \
  -H "X-the operator agent-Session-Token: <token>" \
  -d '{"text":"test"}' | python3 -m json.tool
```

If this returns `{"ok": true, "data_url": "data:audio/mpeg;base64,..."}` —
the backend is fine, the problem is purely in the renderer/device output.

**Note:** A manual unauthenticated curl returns `{"detail":"Unauthorized"}`.
This is expected — the desktop app authenticates via IPC-injected session
token. The 401 does NOT indicate an auth problem in the running app.

## Fixes

### Immediate (no rebuild needed)

Switch the macOS audio output device:

**System Settings → Sound → Output → MacBook Pro Speakers**

Or switch the microphone to the MacBook Pro built-in mic so Bluetooth
headphones stay in high-quality A2DP stereo mode instead of HFP.

If TTS plays after switching output devices, diagnosis confirmed: it was
the Bluetooth HFP + CoreAudio interaction, not a code bug.

### Permanent (rebuild official app)

If the installed app is a stale third-party fork:

```bash
# 1. Install root deps (desktop build needs vite at workspace root)
cd <agent-home>/hermes-agent
npm install

# 2. npm 11+ blocks native dep install scripts by default.
#    node-pty, electron, esbuild all need their postinstall scripts to run.
#    If the build fails with "stage-native-deps: source missing at
#    node_modules/node-pty", the scripts were blocked. Force rebuild:
cd <agent-home>/hermes-agent
npm rebuild node-pty electron esbuild

# 3. Build + package the macOS app
cd <agent-home>/hermes-agent/apps/desktop
npm run dist:mac

# 4. Install the .dmg from apps/desktop/dist/
```

The official source (v0.15.1+ on Electron 40 / Chromium ~134) has far
better macOS 26 audio compatibility than older third-party builds (e.g.,
the `fathah` fork at v0.6.1).

**npm approve-scripts gotcha:** On npm 11+, `npm install` reports
`allow-scripts` warnings for packages with postinstall scripts but does
not run them. `npm approve-scripts <pkg>` returns `ENOMATCH`. The working
fix is `npm rebuild <pkg>` which runs the install scripts directly.
Verify native binaries exist: `ls node_modules/node-pty/prebuilds/`
(should show `darwin-arm64`) and `ls node_modules/electron/dist/`
(should show Chromium files).

**No backend or renderer code change fixes this** — it is an OS-layer
CoreAudio property rejection for a specific device profile. The format
is already MP3 (not OGG); the failure is output-side sample-rate
conversion, independent of the decoded source format.

## Key Insight

"Audio doesn't work in the desktop app" has THREE distinct failure modes,
each requiring a different fix:

| Failure mode | Where | Cause section |
|---|---|---|
| Mic input (no transcription) | getUserMedia blocked by macOS TCC | Cause F (in SKILL.md) |
| TTS playback (no sound) | CoreAudio rejects Bluetooth HFP | This reference |
| Gateway voice messages (no transcription) | Polling stall / provider config | Causes A-E (in SKILL.md) |

Always determine which of the three before debugging. The backend
(`/api/audio/transcribe` and `/api/audio/speak`) is almost never the
problem — test it to rule it out, then focus on the OS/device layer.
