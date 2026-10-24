# principal-Forwarded Content Intake: Extraction Fallback Chain (2026-08-21)

Live-verified protocol for turning a forwarded link or screenshot into a
Research Library filing. Session: Chandrankunnel holographic-emergence
essay + the "two crystals" A→B/B→A crossing-region post.

## Link extraction fallback chain (LinkedIn/social)

1. `web_extract` — FAILS on LinkedIn Pulse (keyless Firecrawl returns
   500). Do not retry it more than once; switch tools, not tactics.
2. `browser_exec` — works, with these handling rules:
   - First call may die on `Target.createTarget` IPC timeout or
     `document.readyState` Runtime.evaluate timeout (stale harness
     daemon). **Retry once** — the second call has consistently worked.
   - After navigation, `time.sleep(5)` before reading DOM.
   - Use a selector cascade, take the FIRST match with >300 chars:
     `.article-body`, `div[class*="article-body"]`, `main article`,
     `main`, `section[class*="pulse"]`, `div[class*="feed-shared"]`,
     else `document.body.innerText` truncated.
   - LinkedIn article pages render fine without login for Pulse essays.

## Screenshot OCR chain (vision unavailable / image opaque)

1. Copy the image out of `<agent-home>/cache/images/` with PIL into a
   workable directory — the filesystem MCP server only reads within its
   allowed dirs, and `vision_analyze` may not be wired.
2. `/usr/local/bin/tesseract <img> stdout --psm 4` — phone-screenshot
   post text extracts cleanly (~1.7k chars from a 590x1280 shot,
   including the numbered question structure).
3. Do NOT attempt Swift Vision inline scripts (`swift /tmp/ocr.swift`) —
   first compile takes >120s in the sandbox and times out. Tesseract is
   already installed at `/usr/local/bin/tesseract`.

## Intake semantics (what "add this to our research for theories" means)

- One `sources` row per forwarded item (dedupe by URL/title first).
- One `findings` row per distinct claim or question, tagged — use
  `open-question` for theory questions the principal forwarded; they are
  invitations to research, not settled facts.
- `update_log` entry with `run_type='manual-ceo-intake'` naming the principal
  as provenance.
- Full capture archived to `research-library/archive/<year>/` as
  markdown: metadata, why-it-matters mapped to DS concepts, candidate
  theory leads for the next research pass.
- Report back with the intake map: what was filed, where, open
  questions raised. Ambiguous shorthand ("the a/b thing I sent") may
  reference forwarded-media content, not testing jargon — resolve it by
  OCR/searching forwarded items BEFORE answering status questions about
  it. In this session, "a/b" meant an A→B vs B→A regime-crossing
  physics question, not an A/B test.
