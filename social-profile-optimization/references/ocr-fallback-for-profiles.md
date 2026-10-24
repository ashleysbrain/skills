# OCR Fallback for Profile Screenshots

When `vision_analyze` is quota-blocked (429 on LLM-5V-Turbo), use `tesseract` CLI as a fallback for reading user-provided screenshots of social profiles.

## Command
```bash
tesseract /path/to/screenshot.jpg stdout 2>/dev/null
```

## What works
- LinkedIn profile screenshots (headline, about section, experience)
- Twitter/X profile screenshots
- Most readable text at standard mobile screenshot resolution
- Available on macOS at `/usr/local/bin/tesseract` (v5.5.2 as of 2026-06)

## Limitations
- Accuracy degrades on stylized text, very small fonts, or overlay text on images
- May miss Unicode symbols (bullets, em dashes)
- Run on ALL screenshots the user sends — don't skip any
- Compare OCR output across multiple screenshots of the same profile for consistency

## Pattern
```python
# Batch OCR all screenshots
for img in screenshots:
    text = subprocess.run(['tesseract', img, 'stdout'], capture_output=True, text=True).stdout
```
