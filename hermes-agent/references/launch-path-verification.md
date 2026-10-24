# Launch path verification for runtime docs

Use when a runtime-facing agent/doc pair needs a canonical startup path.

## What to check
- The wrapper names the correct system/engine in the title and labels.
- `START-HERE.md` exists and is the shortest launch path.
- Any checklist doc the wrapper points to actually exists on disk.
- The read order is linear and does not include a self-reference that makes the checklist recurse.
- The wrapper points to canonical engine docs, not to an alias that hides the real system name.

## Common pitfall found in practice
A wrapper or start page can point to `LAUNCH.md` before that file exists. When that happens:
1. Create the missing checklist file.
2. Make the checklist a linear read order, not a loop.
3. Re-verify every referenced file path.
4. Confirm the docs still use the canonical engine/system name.

## Good final check
Read the chain once from wrapper to core docs and make sure every file in the sequence exists and is reachable without a dead link.
