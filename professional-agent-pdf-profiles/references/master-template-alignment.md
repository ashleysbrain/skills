# Master Template Alignment Notes

Session-derived guidance for keeping agent-profile work aligned with the house template and the live DB.

## Canonical reference order
1. Talent Gate Protocol / master template basis
2. Existing canonical profile examples
3. Live DB row for the agent/persona
4. Rendered PDF verification against the updated source

## What must be visible in the profile
- The profile should expose professional, educational, and certification-style credential sections explicitly.
- If external human credentials are not known, use auditable internal/role-relevant credentials instead of inventing institutions or certifications.
- Keep the credentials visible in the markdown *and* in the rendered PDF; do not rely on hidden metadata.

## Model policy sync
- If the user’s fleet policy changes the allowed model family, update both the profile markdown and the DB-backed model fields before rendering.
- Do not leave the PDF showing a stale model line after the DB has been updated.

## Verification step that matters
- After rendering, extract text from the PDF and confirm the credential section and current model line are actually present.
- File existence or file size alone is not enough proof that the rendered artifact matches the source.

## Layout discipline
- Preserve the master-template section order unless the user explicitly requests a structural rewrite.
- When the user asks for a surgical revision, change only the requested field(s) and keep the baseline layout stable.
- When a profile still feels off, compare it directly to the Talent Gate master template before rewriting again.
