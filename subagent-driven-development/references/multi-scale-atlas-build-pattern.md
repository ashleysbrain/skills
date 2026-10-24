# Multi-Scale Domain Atlas Build Pattern

Pattern for building large multi-scale domain reference documents (50-100+ pages) using specialist subagent delegation + programmatic PDF assembly.

## When to use
- User needs a comprehensive reference document spanning a domain from macro to micro
- The orchestrator does not have the domain expertise to write the content directly
- The domain decomposes naturally into ordered scales or chapters

## Steps

### 1. Decompose the domain into scales
Identify 8-12 scales that cover the domain from broadest to most specific. Each scale should be independently authorable.

Example (neuroscience): Macro → Cortical → Brainstem → Subcortical → Cerebellum → PNS → Connectome → Cellular → Synaptic → Integration

### 2. Delegate each scale to a specialist subagent
Fire in batches of 3, one scale per task:

```
delegate_task(tasks=[
    {
        "goal": "You are an elite [DOMAIN] specialist. Write [SCALE] reference.",
        "context": "Part of [PROJECT]. Write [SCALE] only. DO NOT USE web_search. Write entirely from expertise.",
        "toolsets": ["file", "terminal"]  # NO 'web'
    },
    # ... 2 more in parallel
])
```

**Critical:** Omit `'web'` from toolsets. Specialists writing from expertise finish in ~2 minutes; those who search take 10+ minutes and time out.

### 3. Handle timeouts
If a subagent times out at 600s:
- Check if the file was partially written: `ls -la /path/neuro-techdeep-scaleN.md`
- If the file exists and looks complete (check `tail`), accept it
- If incomplete or missing, re-fire with even tighter scope (fewer structures, lower word count target)

### 4. Write a build script
Python script that:
- Reads all scale `.md` files in order
- Converts each via `markdown.markdown(content, extensions=['tables', 'fenced_code'])`
- Wraps in branded HTML (cover page, TOC, CSS variables for palette)
- Renders to PDF via `weasyprint`

Keep the build script as the canonical artifact. Palette/typography changes = CSS variable patches in the build script, then rerun.

### 5. Verify programmatically
```python
import fitz
doc = fitz.open('output.pdf')
print(f'Pages: {len(doc)}')
# Sample background color
pix = doc[2].get_pixmap(clip=fitz.Rect(0, 0, 10, 10))
print(f'Background RGB: {pix.pixel(0,0)}')
# Check first/last page content
for i in [0, 1, 2, len(doc)-2, len(doc)-1]:
    lines = [l.strip() for l in doc[i].get_text().split('\n') if l.strip()]
    print(f'P{i+1}: {lines[0][:60] if lines else "(empty)"}')
```

### 6. PDF palette defaults
- **Light theme (default for readability):** background #faf8f3 (warm cream), text #2a2a2a, gold #8a6d1f, teal #2d6867
- **Dark theme (only if explicitly requested):** background #080d1a, text #d4d0c8, gold #c9a84c, teal #4a9d9c
- Always use light theme unless the user specifically asks for dark

## Build script template
See `/<workspace>` and `build_tech_atlas.py` for working examples.

## Session log
- 2026-06-19: Built the specialist engine (80pp, 39.5K words, 10 scales) and the specialist engine-Tech Analog Atlas (47pp, 33K words, 10 scales). Timeout mitigation (no web_search, one-scale-per-task) was the key breakthrough after initial 600s timeouts.
