# Golden-Master Report Reproduction

This reference captures the exact reproducibility contract for the approved 8D Pattern Awareness PDF so a future agent can recreate the same document, not just a similar one.

## Canonical source
- Editable source: `references/user-facing-report-example.md`
- Renderer: `scripts/render_user_facing_report.py`
- Required command shape:
  ```bash
  python scripts/render_user_facing_report.py \
    --source references/user-facing-report-example.md \
    --output /tmp/8d-pattern-awareness-professional-report-example-v27.pdf \
    --timestamp '2026-05-31 19:54 CDT'
  ```

## Golden output
- Approved PDF: `/tmp/8d-pattern-awareness-professional-report-example-v27.pdf`
- SHA256: `b8e5d8b93ee2629f3663bd7127a458079880a8cf6ae36b44b67ecc25687e4d08`

## Reproduction rule
To reproduce this exact document, the agent must use:
1. the exact markdown source above
2. the exact timestamp above
3. the exact renderer script above
4. the same output target or a byte-identical re-render target

If any of those inputs change, the output is no longer the golden master and must be re-approved.

## Verification step
After rendering, compute the SHA256 of the PDF and compare it to the golden hash above before claiming exact reproduction.

## Notes
- The footer timestamp is part of the document identity.
- Any source edit, even a layout-only tweak, invalidates this exact reproduction record.
- If the document is intentionally revised, regenerate a new golden-master reference instead of overwriting this one without versioning.
