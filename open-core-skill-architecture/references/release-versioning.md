# Release Versioning Reference

Use this reference when naming, ranking, or packaging a skill family.

## Release identity format
Use:

`[Family] — [Release Class] — v[SemVer] — [Release Date]`

Examples:
- `8D Pattern Awareness — core — v1.0.0 — 2026-06-01`
- `8D Executive Function Brief — core — v2.0.0 — 2026-06-08`
- `External Content QA Pipeline — support — v1.0.0 — 2026-06-08`

## Release classes
- `core` — primary user-facing skill
- `support` — QA, guide, reference, helper layer
- `bridge` — migration, compatibility, redaction, connector
- `fork` — derivative variant of an existing skill
- `ops` — internal workflow or fleet utility

## Ranking rule
Do not hardcode coherence to the first release in a family.

Instead, rank candidates against the **current stable core anchor** for that family.

When a new core release ships:
- update the anchor
- re-score support and bridge candidates against the new anchor
- keep the family coherent rather than scattering releases across unrelated labels

## Packaging rule
A release can be useful without being the primary core release.
Support and bridge releases should be treated as first-class family members, but clearly labeled so users know they are companions rather than the main artifact.
