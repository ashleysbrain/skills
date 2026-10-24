# Database-scored vs display-layer terminology

Session-derived correction:

- Do **not** describe the native engine inputs as normalized to 0-1, 1-10, or 0-100.
- The engine should be described as **database-backed scoring first**: evidence is collected, scored into native dimension outputs, then combined into TWC.
- Only **after TWC** should the product convert the result into a presentation format such as 0-100 or 1-10.
- If the product needs a decimal/percentage bridge, it belongs strictly at the final presentation boundary, not in the scientific input layer.

Teaching order for docs and briefings:
1. Raw evidence and source adapters
2. Database-scored native dimension outputs
3. Baseline comparison and confidence
4. Coupling / balance / composite score (TWC)
5. Presentation conversion for users

Use this wording when the goal is to educate engineers, product, or investors:
- "database-backed scoring layer"
- "native score"
- "display conversion after TWC"
- "presentation layer"

Avoid these phrases for the engine layer:
- "normalized inputs"
- "0-1 native scale"
- "1-10 as the input"
- "display score as the source of truth"
