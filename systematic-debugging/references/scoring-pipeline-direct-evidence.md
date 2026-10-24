# Scoring pipeline: direct-evidence notes

This session reinforced a durable rule for adaptive health scoring pipelines:

- The complex engine (`calculator.py` / `compute_twc`) is the scoring math.
- Transcript or voice-note adapters should map evidence into calculator inputs, not act as an alternate scoring layer.
- A heuristic 1–10 bridge can make the output look plausible while still being scientifically weak.
- When the live score looks "too simple," verify whether a bridge layer is inflating or distorting the evidence before touching the engine.

## Good verification sequence

1. Run the transcript adapter and inspect the emitted fields and confidences.
2. Confirm the merged calculator inputs are populated directly.
3. Run the real engine and verify the DB row stores the engine tag plus coherence/synergy/coupling metadata.
4. Compare dry-run output, persisted row, and exported/admin views for consistency.

## Red flags

- Scores that depend on keyword-only boosts rather than structured evidence.
- A bridge that creates a hidden 1–10 layer between transcript evidence and the calculator.
- DB rows that show complex metadata, but the live path still uses heuristic defaults upstream.

## Preferred fix direction

- Expand the adapter so it fills real calculator fields from evidence and baseline context.
- Gate any default/baseline values by explicit confidence.
- Keep the engine math unchanged unless you have a proven engine bug.
- When transcript evidence is thin, prefer conservative under-scoring over inventing values.
- If a score seems "too low," inspect which dimensions received no evidence before you tune the engine.

## Session note: eight-dimension coverage

In this session, the adapter was expanded to populate evidence across all 8 dimensions directly:
- Psychological: mood, anxiety, calm, awareness, support cues
- Physical: sleep, exercise, energy, nutrition, hydration, body state
- Intellectual: learning, focus, problem solving, memory, curiosity
- Social: interaction quality, close ties, support given/received, belonging
- Spiritual: meditation, purpose, gratitude, inner peace, values alignment
- Vocational: work hours, progress, skill use, challenge, achievement
- Financial: money stress / expense signals when explicit
- Environmental: organization, comfort, space, safety, light

The important lesson is not the exact keyword list; it is the architecture:
- source adapter -> real calculator fields -> complex engine -> DB row
- no hidden 1–10 bridge in the live scoring path
- confidence must be visible per field so future regressions are easy to spot
