# Internal Release Flow for Skill Update Engine

This reference captures the internal-first release flow used to test skill updates on us before any public packaging.

## Release identity
Use explicit release metadata for every shipped skill or support artifact:

`[Family] — [Release Class] — v[SemVer] — [Release Date]`

Release classes:
- `core` — primary user-facing skill
- `support` — reference, guide, QA, or helper layer
- `bridge` — compatibility, translation, or migration layer
- `fork` — derivative variant of an existing family member
- `ops` — internal workflow or fleet utility

SemVer rules:
- `patch` = wording fixes, references, examples, non-breaking clarifications
- `minor` = additive workflow steps, new guidance, new helper/reference behavior
- `major` = breaking workflow change, renamed contract, or redesigned output shape

## Internal flow
1. **ARBITER** dispatches the scan.
2. **FORGE** collects candidate signals.
3. **SCOUT** scores and maintains the watchlist.
4. **NEXUS** drafts patches and assigns release identity.
5. **PARALLAX** reviews medium/low-confidence candidates.
6. **SENTINEL** verifies version integrity and boundary safety.
7. **Human review** selects the top 3 eligible candidates daily.

## Ship rule
A patch is not shippable unless:
- the skill frontmatter version moves forward
- the release identity is explicit
- the candidate passes anti-duplication and boundary checks
- near-misses stay alive in revise-and-resubmit rather than being dropped

## Report format
If the update engine produces a human-readable report, generate it as PDF when available. Use Markdown only as a fallback when PDF is unavailable.
