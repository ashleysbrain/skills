# Voice note kills the gateway — STT provider native-abort class (2026-08-24)

## Symptom signature
- principal sends voice notes; gateway log shows `inbound message: ... msg=''` (empty text = voice), then
  the gateway process dies UNCLENANLY and reconnects (`✓ telegram connected` bursts), restart-loop
  breaker TRIPPED (`3 chained restart-interrupted gateway boots`).
- `<agent-home>/logs/gateway.error.log` contains a native crash dump with the chain:
  `transcribe_audio -> _transcribe_prepared_audio -> _dispatch_stt_provider -> _transcribe_local
  -> _load_local_whisper_model -> from faster_whisper import WhisperModel -> ctranslate2 import`
  preceded by the NumPy banner "A module that was compiled using NumPy 1.x cannot be run in NumPy 2.4.3".
- NOT a polling stall, NOT a restart storm. A holding restart-ceasefire changes nothing —
  the gateway is self-destructing on every voice note.

## Root cause
`stt.provider: local` (built-in) always wins dispatch and goes to faster_whisper. The venv had
`ctranslate2 4.8.1` (compiled against numpy 1.x) under `numpy 2.4.3` → native abort inside the
gateway process → whole process dies mid-transcription → note orphaned.

## Why the env-var fix was dead code
`HERMES_LOCAL_STT_COMMAND` was set in `<agent-home>/.env`, but:
1. The launchd-supervised gateway process env does NOT include it. Verify:
   `ps eww <gateway_pid> | tr ' ' '\n' | grep STT` → empty.
2. Even if present, it only fires for provider `local_command`, which config never selected
   (`stt.provider: local` short-circuits to the faster_whisper handler first).
3. With the var absent at dispatch, the gateway's binary discovery (`_find_whisper_binary`) can
   spawn reference `/usr/local/bin/whisper` at ~237% CPU, unniced → load 50+ → watchdog cascade
   class. (Separate CPU-storm failure mode, same config knob.)

## Fix (config-native, per repo law: .env = secrets only)
```yaml
stt:
  provider: whisper_cpp
  providers:
    whisper_cpp:
      type: command
      command: /<workspace> {input_path} {output_dir} {language}
      timeout: 1800
      format: txt
```
Set via `hermes config set stt.providers.whisper_cpp.type command` etc. (chained one-liners can
trip the terminal hardline payload parser — write a /tmp script and `bash` it, per the block
message's own recovery note). The `⚠ not a recognized config key` notice on `stt.providers.*`
keys is benign (static registry); verify with a YAML parse.

Key properties:
- `_load_stt_config()` re-reads config.yaml on EVERY transcription (no cache) → the switch takes
  effect on the NEXT voice note with ZERO gateway restart. Ceasefire-preserving.
- Command-provider placeholder grammar: `{input_path}` `{output_path}` `{output_dir}` `{format}`
  `{language}` `{model}` — shell-quote-aware; doubled braces `{{x}}` stay literal.
- Timeout in the command-provider path is an IDLE timeout (reset on child output); the whisper.cpp
  wrapper is silent, so set it generously (1800s) for long notes.
- Child env is scrubbed of the operator agent secrets by the runner → the wrapper must use ABSOLUTE binary
  paths (it does) to survive the scrub.
- Wrapper contract: `$1` input audio (handles .ogg via own ffmpeg stage), `$2` output dir,
  `$3` language; writes `$2/transcript.txt`, exit non-zero on failure, `nice -n 10` inside.

## E2E falsifiable rerun (do this before claiming fixed)
```bash
cd /<workspace> && venv/bin/python3 -c "
import sys; sys.path.insert(0,'.')
from tools.transcription_tools import transcribe_audio, _load_stt_config, _resolve_command_stt_provider_config
cfg=_load_stt_config(); print('provider:',cfg.get('provider'))
rc=_resolve_command_stt_provider_config('whisper_cpp',cfg); print('resolves:',rc is not None)
r=transcribe_audio('/<workspace><file>.ogg', source='e2e-test')
print(r.get('success'), r.get('provider'), (r.get('transcript') or '')[:200])"
```
Expected: `provider: whisper_cpp / resolves: True / True whisper_cpp <text>`.

## Recovery + delivery pattern
- Voice notes survive in `<agent-home>/cache/audio/*.ogg` even when transcription died — recover by
  running the wrapper directly on the cached file (`/tmp/vnote-<HHMM>/transcript.txt`).
- Deliver recovered transcripts to the user via `hermes send -t telegram --file <path> -s "subject"`
  (no LLM, no agent loop). Verify a send confirmation before telling the user anything landed.
- Check for redundant transcription burn before/after: `pgrep -fl "bin/whisper"` — kill manual
  reference-whisper runs on already-recovered content (237% CPU each); attribution via
  `ps -o ppid` → parent shell's `eval` comment shows the launching agent's intent.

## Handoff notes (sibling lane)
- The numpy/ctranslate2 ABI landmine stays armed in the venv — anyone reverting
  `stt.provider` to `local` re-arms the gateway-killer. Pin or rebuild ctranslate2 against
  numpy 2.x, or leave `local` permanently dark.
- `HERMES_LOCAL_STT_COMMAND` in `.env` is dead weight once the config provider is live.
