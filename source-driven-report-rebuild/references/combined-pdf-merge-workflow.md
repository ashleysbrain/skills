# Combined PDF merge workflow

Session lesson: when the user wants two finished technical PDFs combined into one presentation artifact *without deleting anything*, the safest path can be:

1. Create a short front-matter cover page separately.
2. Preserve the original PDFs unchanged.
3. Merge cover + source PDFs with `pypdf` rather than forcing a single regenerated HTML-to-PDF build.
4. Verify the merged output by checking page count and extracting text from representative pages at the start, boundary, and end.

## Why this works
- It preserves every original page and section from each source artifact.
- It avoids renderer edge cases from very large combined HTML/CSS documents.
- It keeps the merged file easy to distribute while leaving the source artifacts intact for maintenance.

## Practical notes
- Use `reportlab` for the cover page if the combined HTML renderer becomes unstable.
- Use `pypdf.PdfReader` / `PdfWriter` to append existing PDFs in order.
- After merging, confirm the cover page is first and the original documents remain in full.
- If the user asked for “don’t delete anything,” treat that as a preservation constraint: combine by adding structure around the originals, not by pruning sections out of them.
