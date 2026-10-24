# Conductor screen batteries (the OS OS conductor, :port) — 2026-08-19

Session-specific record of the live-browser battery pattern used to verify the
conductor screen v1→v3. Extends SKILL.md rules 6 (asset-load assertions) and
7 (node --check embedded JS), born from this session's catches.

## The two catches that forced new rules

1. **Silent font fallback (rule 6 origin).** The screen's `@font-face` pointed
   at `/fonts/Manrope.ttf`; the daemon never served `/fonts/*` → every request
   404'd → every render silently fell back to system-ui. Every offsetWidth
   check PASSED. The principal read the result as "super AI generated". Typography
   verdicts require load-status assertions, never geometry alone.
2. **Stackless syntax error (rule 7 origin).** A JS ternary
   (`+'</div>'':'';`) inside the served HTML threw in-page "Unexpected string"
   with NO stack. Browser-level pageerror gave no line. Extracting the script
   block and running `node --check` printed the exact line immediately.

## Battery shape (Python, reused 3× this session)

```python
import asyncio, json
from playwright.async_api import async_playwright
EXE = ("/<workspace>"
       "chrome-headless-shell-mac-x64/chrome-headless-shell")
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=EXE)
        pg = await b.new_page(viewport={"width":1440,"height":940})
        errs, failed = [], []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("requestfailed", lambda r: failed.append(r.url[-40:]))
        await pg.goto("http://127.0.0.1:port/", wait_until="networkidle")
        await pg.wait_for_timeout(2200)   # let polls land
        fonts = await pg.evaluate("""async () => {
          await document.fonts.ready;
          const out = {};
          for (const f of ['Manrope','Sora','IBM Plex Mono'])
            out[f] = document.fonts.check('13px "'+f+'"');
          out._faces = [...document.fonts].filter(x=>x.status==='loaded').length;
          return out; }""")
        # ... view-toggle clicks, drawer drill-down, row counts ...
        ok = (fonts["Manrope"] and errs == [] and failed == [])
        print("VERDICT:", "LIVE" if ok else "FAIL")
asyncio.run(main())
```

## Assertions that earned their place

- `document.fonts.check('13px "Family"')` per family + loaded-face count ≥ 4
- `page.on("requestfailed")` — catch 404'd subresources (the font bug's class)
- `page.on("pageerror")` with `errs == []` in the verdict
- View toggles: click each `.tgl[data-view=...]`, assert target
  `offsetWidth > 0` AND siblings' `offsetWidth === 0`
- Drawer drill-down: real click on a bus row → drawer classList contains
  `open`, drawer offsetWidth == CSS width (440), body textContent length > 20
- Screenshot to stores/ every pass (principal-visible artifact)

## Workflow note: QA passes must rotate brains

principal standing preference: each "another QA pass" runs the full live battery
end-to-end and rotates a DIFFERENT specialist (Goethe→Luria→Bell...), folding
findings into the SAME doc/artifact — never a "done" claim without output
inspection. A `qa-log/` file inside the product repo (findings + open items
per pass) makes the screen's QA accumulate instead of restarting.

## Failure classification seen this session

- Playwright `Executable doesn't exist ... 1234` → version drift, pin
  executable_path to an installed shell (do NOT `playwright install` blindly)
- Probe file write blocked by baseline-first gate → overwrite the existing
  battery file for the same surface instead of minting parallel ones
- Terminal inline-heredoc blocklist fired on nested quotes → write the script
  to a file first, run the file
