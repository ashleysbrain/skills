# Release ladder for skill-update-engine

Use the same release identity convention everywhere:

`[Family] — [Release Class] — v[SemVer] — [Release Date]`

## Recommended ladder

1. **core** — the public update-engine workflow itself
   - daily scan/synthesize/ship cadence
   - anti-duplication rules
   - current-anchor coherence

2. **support** — reference files, QA schema, metrics templates
   - pipeline metrics
   - engine config
   - dedup protocol

3. **bridge** — migration/routing helpers
   - profile-to-topic routing
   - compatibility shims between versions

4. **ops** — internal automation helpers
   - cron manifests
   - analytics sync
   - backlog compaction

5. **fork** — specialized variants
   - narrow workflows for one domain or one profile
   - only when the domain diverges enough to justify a new lineage

## Ranking rule

Compare candidate releases against the **current stable core anchor** for the family.
Do not compare everything to a fixed first version if the family has already moved on.
