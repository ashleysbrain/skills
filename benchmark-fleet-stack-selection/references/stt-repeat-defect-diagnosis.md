# STT Repetition-Defect Diagnosis (transcribed but garbage)

Depth for the repeat/hallucination complaint class. SKILL.md carries the always-on rules; this file carries the procedure.

## Symptom
Transcripts repeat phrases/sentences far beyond the speaker's natural repetition. User-visible: "it's repeating stuff… not this much."

## Root-cause families
1. **Decode under CPU starvation** — concurrent decodes or other CPU-heavy agents (git pack jobs, other agent CLIs, MCP daemons) push load far past core count. Whisper's temperature fallback re-decodes windows; stretched/silent audio then yields looping n-grams.
2. **Duplicate pipeline passes** — the same note processed twice upstream and the two transcripts concatenated.
3. **Genuine model defect** — silence-looper models hallucinate loops even on a calm machine without VAD.

## Procedure

1. **Locate the exact note.** Match `[Telegram] Cached user voice at <path>` in gateway.log to the report time. The cache dir is whatever that logged path says (`<agent-home>/cache/audio/` and `<agent-home>/audio_cache/` both exist in the wild) — never assume the directory.
2. **Read the live STT config** out of config.yaml (`stt.providers.<name>.command`, model file, flags). The production entrypoint may have been switched since the complaint — verify against the log timeline, not memory.
3. **Replay in isolation.** Convert with the same ffmpeg normalization the production script uses (16kHz mono), invoke the EXACT production script with its exact model and prompt flags, sequentially, `nice -n 19`, background + notify. Check `uptime` first and note load.
4. **Score both transcripts** with the repeat-audit scorer: consecutive n-gram loop runs (n=3,6), immediate-echo rate (n=1,3), unique-token ratio, plus keyword recall for names/terms known to be in the note.
5. **Branch on the result:**
   - Clean isolated + dirty live → live-path defect: reconstruct load at the original decode time (log timestamps, other processes), and grep the pipeline for double-processing of the same file.
   - Dirty in both → engine/config defect: enable VAD, or bench an alternate model per the fleet procedure.
6. **Fix and gate:** sequential decode discipline, VAD on silence-looper models, repeat-audit as a standing gate on the production path if the pipeline supports hooks.

## Scorer thresholds (calibrate per speaker)
Unique-token ratio below ~0.30, echo-1 above ~0.08, or any 3-gram loop run ≥3 = FAIL. A natural speaker's baseline must be measured once on known-clean transcripts — the speaker's own repetition style sets the bar, not a generic number.

## Timing notes
A ~60s note at large-v3-turbo q5_0 on a loaded Intel-class machine runs 3–10 min wall; do not foreground-wait it. One decode saturates the cores — never launch a second candidate until the first exits (the notification is the signal).
