# Layered Memory Stacks

## Goal
Use a shared baseline plus per-engine overlays, then render a final engine-specific memory file with an automated merge step.

## Pattern
- `memory/HOT.md` and topic files hold shared baseline facts.
- `memory/engines/<engine>.md` holds small engine-specific deltas.
- `memory/memory-stack.json` defines the layer order.
- `scripts/render-memory-stack.py` renders the final output.
- `memory/generated/<engine>/MEMORY.md` is the rendered artifact.

## Important constraints
- Do **not** rely on recursive file includes inside memory files.
- Treat the renderer as the merge/include step.
- Keep overlays small; shared facts belong in shared topic files.

## Example commands
```bash
python scripts/render-memory-stack.py --engine aisha-md --out memory/generated/aisha-md/MEMORY.md
python scripts/render-memory-stack.py --all
```

## Practical pitfall
If a fact applies to all engines, put it in the shared layer instead of duplicating it across every overlay.
