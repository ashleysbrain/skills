# Release Handoff Renaming Hygiene

Use this when a skill package or release bundle is being renamed from an old label like V1/V2 into final release naming.

## Checklist
1. Rename the files first so the filesystem matches the new release identity.
2. Update inline headers and titles inside the renamed files.
3. Update any references lists in `SKILL.md` and companion docs.
4. Search the package for the old label to catch body text, headings, and filenames.
5. Re-read any paginated or partial files before overwriting them again.
6. Verify the final file list so the old filenames are actually gone.

## Common miss
It is easy to rename the path but leave the old label in body text, section headings, or reference lists. Do a text search after the rename, not before you declare success.
