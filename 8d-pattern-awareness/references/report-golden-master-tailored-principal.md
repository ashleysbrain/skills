# Tailored Golden-Master Report Reproduction

This reference captures the exact reproducibility contract for a general-user tailored 8D Pattern Awareness PDF, so a future agent can recreate the same tailored document, not just a visually similar one.

## Canonical source
- Editable source: `references/user-facing-report-tailored-principal.md`
- Renderer: `scripts/render_user_facing_report.py`
- Required command shape:
  ```bash
  python scripts/render_user_facing_report.py \
    --source references/user-facing-report-tailored-principal.md \
    --output /tmp/8d-pattern-awareness-professional-report-tailored-principal.pdf \
    --timestamp '2026-05-31 20:00 CDT'
  ```

## Tailored output
- Approved PDF: `/tmp/8d-pattern-awareness-professional-report-tailored-principal.pdf`
- SHA256: `26f470da9e0374c081ca62a7c44ae053952d0f00445d807d83744e20e2e93337`

## Reproduction rule
To reproduce this exact tailored document, the agent must use:
1. the exact markdown source above
2. the exact timestamp above
3. the exact renderer script above
4. the same output target or a byte-identical re-render target

If any of those inputs change, the output is no longer this tailored golden master and must be re-approved.

## Verification step
After rendering, compute the SHA256 of the PDF and compare it to the tailored hash above before claiming exact reproduction.

## Notes
- The footer timestamp is part of the document identity.
- The content is intentionally neutral and general-user facing; any person-specific example is only a temporary sample variant.
- Any source edit, even a minor wording change, invalidates this exact reproduction record.
