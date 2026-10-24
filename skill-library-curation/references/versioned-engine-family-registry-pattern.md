# Versioned Engine Family Registry Pattern

Use this pattern when a user asks to "version each engine" or apply a Qubit-style version system across a related documentation family.

## Durable pattern

1. Create a **shared registry file** for the whole engine family.
   - Use one ledger for the canonical spec, runtime wrapper, support docs, and schema bundle.
   - Keep release state explicit (`Draft`, `Frozen`, etc.).
   - Use one version format consistently across the family.

2. Add a **Version Control System** section to each canonical doc.
   - Include the current version.
   - Include the registry link.
   - Add a short version history note.
   - Keep the section near the top-level structure or after the TOC.

3. Update the **docs index / catalog** so the registry is discoverable.
   - Add a row or bullet for the registry file.
   - Update freshness / last-updated metadata when appropriate.

4. Verify the result with **read-back and diff checks**.
   - Re-read the edited docs to confirm headings, links, and version strings landed correctly.
   - Use git diff/stat to confirm only the intended files changed.

## Pitfalls

- Do not invent separate version systems for each doc unless the user explicitly wants separate lifecycles.
- Do not add a version block to a supporting doc without linking it back to the shared registry.
- Do not leave the docs index unaware of the registry, or the version system becomes hard to find.
- Keep release state and version number distinct; `v1.0.0` is not the same thing as `Draft` or `Frozen`.

## Verification checklist

- [ ] Registry file exists
- [ ] Core docs link to the registry
- [ ] Current version strings match across the family
- [ ] Docs index mentions the registry
- [ ] Git diff shows only intended files
