# Silent STT skip — stale boot-time GatewayConfig (2026-08-25)

Day-2 follow-on to `voice-note-process-death-stt-provider-2026-08-24.md`. The
command-provider fix was E2E-proven through the real dispatch chain, yet the
next morning 10/10 voice notes were still not transcribed — with replies
going out. The principal's "hello???" was the only signal.

## Symptom signature
- `Cached user voice at /<workspace>*.ogg` lines all day.
- `inbound message: ... msg=''` for each note.
- ZERO `Transcribing ... via command STT provider` / `Voice transcription failed` lines.
- `response ready: ... response=N chars` still appears — the agent replied to nothing.
- User perception: "talking to a wall" — replies that ignore every voice note.

## Root cause (two config layers, one process)
- `_load_stt_config()` re-reads config.yaml per dispatch (mtime/size-keyed
  cache) — hot pickup IS real for the provider dispatch layer.
- BUT the `stt_enabled` gate in `_enrich_message_with_transcription_inner`
  reads `self.config.stt_enabled` — a GatewayConfig object built ONCE at
  boot. The gateway had booted 10 minutes BEFORE the config fix landed, and
  its in-memory object never saw it. Disk parsed True; the process behaved
  as False.
- "Zero restart needed" was a half-truth that cost a full day. After ANY
  `stt.*` config change, restart the gateway at a safe window.

## Forensic census (isolate without trusting logs)
1. `grep -c "Cached user voice at" gateway.log` today vs transcription lines.
2. Wrapper temp dirs: `/tmp/stt-wcpp-*`, `/tmp/hermes-cmd-stt-*`,
   `/tmp/hermes-local-stt-*` — absent ⇒ wrapper never ran.
3. `stat -f "%Sa" <agent-home>/models/whisper-cpp/ggml-tiny.bin` — frozen at the
   last real run.
4. `stat` on `<agent-home>/state/stt-inflight/` — dir mtime touched at the
   note's inbound timestamp ⇒ the enrichment choke point RAN (marker
   write+unlink in the finally block) and skipped dispatch. Only the
   `stt_enabled == False` branch produces exactly this silence.
5. Parse test against disk truth:
   `cd <agent-home>/hermes-agent && venv/bin/python3 -c "from hermes_cli.config import load_config; from gateway.config import GatewayConfig; print(GatewayConfig.from_dict(load_config()).stt_enabled)"`
   True on disk + skip behavior live ⇒ stale process config ⇒ restart.

## Fix + verification
- ONE sanctioned restart: `hermes gateway restart`. Safe window = stt-inflight
  marker dir empty + no whisper process (`pgrep -fl whisper`).
- The restart path itself defers while stt-inflight markers exist (bus 3394
  fix) — check the dir first, never force.
- LIVE-FIRE verification only: a real voice note that transcribes. Config
  state, module imports, and dispatch tests do NOT prove the running gateway
  will transcribe. Ask the user for one test note and offer batch recovery of
  the backlog from `<agent-home>/cache/audio/*.ogg` (wrapper handles them
  directly; ~25s per 4-min note, niced).

## Distinguish from neighbors
- Polling-stall wedge: NO inbound lines at all. Here inbound flows.
- ABI gateway-killer: gateway DIES on each note (crash dumps). Here it lives.
- This mode: everything looks healthy, transcription simply never fires.
