# Canonical term renaming workflow

Use this when a product or agent name is being normalized across a document set (for example, replacing an old multi-word brand and its abbreviation with a new canonical name).

## Durable pattern
1. Search the whole package for both:
   - the full old phrase
   - the legacy abbreviation / acronym
2. Replace content in bulk across all mirrored source trees before doing manual cleanup.
3. Patch templates separately so future generated files inherit the new canonical name.
4. Rename filenames and folder labels when the user asked for a full brand normalization, not just in-body text edits.
5. Verify the cleanup with a second search that returns zero hits for both the full phrase and abbreviation.
6. If the workspace has synced duplicates (for example, local source + cloud vault copy), verify both locations.

## Practical note
A single clean text search is not enough after a brand rename. File names, headings, template placeholders, and linked examples can all preserve the old identity even when the main prose looks clean.
