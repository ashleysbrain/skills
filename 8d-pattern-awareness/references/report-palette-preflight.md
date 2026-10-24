# Report Palette Preflight

Use this checklist before rendering or recoloring any user-facing 8D report PDF.

## Purpose
Prevent repeated wrong-color iterations by confirming the palette source of truth before editing.

## Checklist
1. Locate the documented palette reference used by the current report family.
2. Extract the exact hex values for:
   - primary/base color
   - background/soft surface color
   - restrained accent color
   - any optional secondary signal colors
3. Confirm whether the user asked for:
   - exact palette matching
   - a narrow color swap only
   - preserved geometry / preserved page structure
4. Compare the intended accent against the actual PDF output before sending.
5. If the user says the delivered PDF still looks wrong:
   - stop iterating from memory
   - re-open the palette reference
   - verify the rendered pixels or source color mapping
   - regenerate only after the source of truth is confirmed

## Common failure to avoid
Do not assume a bright yellow accent just because the prior output looked gold-ish. If the documented accent is a muted gold or another restrained tone, use that exact value.

## Verification standard
A corrected output should satisfy both:
- the page geometry matches the approved baseline
- the accent colors match the documented palette, not a guessed approximation
