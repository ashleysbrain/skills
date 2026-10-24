# Direct Input Evidence Scoring Notes

Session lesson:
- Keep the transcript adapter focused on evidence extraction.
- Feed the real calculator inputs directly.
- Do not insert a hidden 1–10 bridge in front of a complex engine.
- If the database schema still requires bounded legacy columns, clamp only at write time and preserve raw outputs in metadata.

Verification pattern that worked:
1. `python -m py_compile` on the touched modules.
2. Run the live scoring entrypoint in dry-run mode with representative transcript text.
3. Inspect the real calculator output and engine tag.
4. Confirm the DB row stores the expected score engine/version/baseline metadata.

Field groups that were expanded directly from transcript cues:
- Physical: sleep, exercise, hydration, pain, energy.
- Intellectual: learning hours, focus, problem solving, curiosity, memory.
- Social: interactions, close ties, support, belonging, loneliness.
- Spiritual: meditation, mindfulness, purpose, meaning, gratitude, connection.
- Vocational: work hours, quality, progress, learning, satisfaction.
- Environmental: home comfort, organization, light, space, safety.
