# Faster-Whisper Venv Fix (2026-07-11, updated 2026-07-12)

## Problem

STT provider is set to `openai` (or `local`) but voice messages are not transcribing. The root cause chain:

1. `stt.provider: openai` but `VOICE_TOOLS_OPENAI_KEY` is empty in `.env`
2. Switch to `stt.provider: local` but `faster_whisper` module not found
3. The whisper binary exists at `/usr/local/bin/whisper` (Homebrew install) but the operator agent cannot import it because it runs in its own venv
4. The whisper binary is too slow for long messages (10+ min audio times out on CPU)

## Root Cause: Wrong Venv

the operator agent runs in `<agent-home>/hermes-agent/venv` (Python 3.11), NOT system Python 3.14.

```bash
cat /<workspace>
# exec "/<workspace>" "$@"
```

The `faster_whisper` package must be installed in the operator agent's venv, not system python or venv-embed.

## Fix

```bash
<agent-home>/hermes-agent/venv/bin/pip install faster-whisper
<agent-home>/hermes-agent/venv/bin/python -c "from faster_whisper import WhisperModel; print('OK')"
# config.yaml: stt.provider: local
```

After installing, the running the operator agent process must restart to pick up the new module. Until restart, use the manual fallback below.

## Why System Python Fails

System Python 3.14 cannot build the `av` dependency (PyAV/FFmpeg bindings, no wheel for 3.14). the operator agent venv uses Python 3.11 where wheels are available.

## Provider Fallback Chain

When `stt.provider: local`: (1) try `faster_whisper` import, (2) fall back to whisper binary auto-detect, (3) return "none". Binary is too slow for long messages on CPU. faster-whisper with int8 is dramatically faster.

## Manual Transcription (when the operator agent process hasn't restarted)

The the operator agent process loads modules at startup. If you install faster-whisper mid-session, the running process still can't import it. As a bridge until the next restart:

```bash
# Transcribe the most recent voice message
RECENT=$(ls -t <agent-home>/audio_cache/*.ogg | head -1)
<agent-home>/hermes-agent/venv/bin/python -c "
from faster_whisper import WhisperModel
model = WhisperModel('tiny', device='cpu', compute_type='int8')
segments, info = model.transcribe('$RECENT', language='en')
text = ' '.join([s.text for s in segments])
print(text)
"
```

Use `beam_size=1` for faster processing on long messages (5+ minutes).

## No Cloud STT Available (2026-07-11)

llm-vendor: "Unknown Model" for whisper. NVIDIA NIM: zero audio models. OpenRouter: 403 key limit exceeded. Only working path is local faster-whisper in the operator agent venv.

## Image Reading Fallback (vision_analyze blocked)

vision_analyze fails with llm-vendor (LLM-5V-Turbo not in plan). NVIDIA NIM vision works via curl:

```bash
curl -s https://integrate.api.nvidia.com/v1/chat/completions \
  -H "Authorization: Bearer $NIM_KEY" \
  -d '{"model":"meta/llama-3.2-90b-vision-instruct","messages":[{"role":"user","content":[{"type":"text","text":"Read all text"},{"type":"image_url","image_url":{"url":"data:image/jpeg;base64,'$(base64 -i image.jpg)'"}}]}],"max_tokens":3000,"temperature":0.1}'
```
