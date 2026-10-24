---
name: ai-tell-removal-gate
description: Mandatory pre-presentation cleanup gate. Removes AI telltales from any document before it reaches the user. Applied to all team-facing, customer-facing, or PDF-rendered documents.
category: brand-voice
---

# AI Tell Removal Gate

## When to Apply
Apply this gate to ANY document before presenting it to the user or rendering it as a branded PDF. This is non-negotiable. If you skip this and the user catches an AI telltale, that is a gate failure on your end.

## The Telltale Checklist

Run a regex/keyword scan on the document text. FAIL the document if any of these are present:

### Punctuation Tells
- Em dashes (—, U+2014). Use colons, periods, or commas instead.
- En dashes used as pauses (–, U+2013). Acceptable for number ranges only (2–3, 2020–2024).
- Triple dots used as thinking pauses (...). Acceptable in quoted speech only.

### LLM Phrasing Tells
- "walk you through"
- "I want to" / "Let me" (when used as document openers)
- "single highest impact" / "highest-impact"
- "don't touch it" / "keep as-is" used as commands
- "start there" / "start here"
- "decoration" / "just paint on"
- "exactly where" / "precisely when"
- "in other words" / "to put it simply"
- "it's worth noting" / "it's important to note"
- "reach out" / "reaching out"
- "dive in" / "dive deeper"
- "game-changer" / "game-changing"
- "leverage" (as a verb, when "use" works)
- "robust" / "seamless" / "comprehensive"
- "delve" / "delving"
- "navigate" (as metaphor)
- "tapestry" / "landscape" (as metaphor)
- "underscore" / "underscored"
- "nuance" / "nuanced"
- "realm" / "spheres"
- "elevate" / "elevated"
- "in today's" / "in the world of"
- "crucial" / "vital" / "essential" (when used as filler)

### Structural Tells
- Headers that start with "How to" or "Why" followed by a colon (overused LLM pattern)
- Bulleted lists with bold lead-ins on every bullet (LLM formatting tic)
- Paragraphs that summarize what the next paragraph will say (signposting)
- "TL;DR" sections (use a clean summary header instead)
- Every paragraph starting with the same word or pronoun (learned 2026-07-10: user flagged "every paragraph starts with I and that sounds very odd for science"). Vary openers. Reserve first-person "I" for the single most important claim in the document. Other paragraphs should open with their subject: the system name, the concept, the method, or the finding.

## Cleanup Procedure

1. Read the full document.
2. Run the telltale scan on the **entire file**, not just the body the user will paste.
   - Markdown headers, status lines, table cells, and footnotes count.
   - Learned 2026-07-09: a company LinkedIn post body was clean while `## Primary post (company page — copy/paste)` still held em dashes and failed `scan_ai_tells.py`.
3. For each hit, rewrite the sentence in plain English.
   - Em dash → period (split into two sentences) or comma or colon.
   - "walk you through" → "this is the reference for"
   - "single highest impact" → "highest impact" or just describe the impact.
   - "don't touch it" → "leave it as-is" or "keep this component"
   - "start there" → "those are the first two changes"
   - "decoration" / "just paint" → "surface features" or omit.
4. Re-scan. Document passes when zero hits remain.
5. Only then render the PDF or present to the user.

## Visual AI Tells (learned 2026-07-15)

Emoji icons are an AI tell in production interfaces. User said "you've gone
away from our design look to an ai generated design" and "I want custom icons
for all the things." Emoji render inconsistently across platforms, look
unprofessional, and signal "AI generated this."

### Visual Tell Checklist
- **Emoji icons** in buttons, headers, nav items, or status indicators.
  Replace ALL with inline SVG (`viewBox="0 0 24 24"`, `stroke="currentColor"`).
  Audit regex: `[\x{1F300}-\x{1F9FF}]|[\x{2600}-\x{26FF}]|[\x{2700}-\x{27BF}]`
- **System font fallbacks** (`-apple-system`, `ui-monospace`, `SF Mono`).
  These render as system default (SF Pro on macOS) instead of the intended
  brand font (Inter/JetBrains Mono). Strip them from all CSS font stacks.
- **Default/generic color schemes** that don't match the brand phenotype.
  the operator agent phenotype: `#080d1a` dark, `#e8d5a0` moonlight, `#6366f1` indigo.
- **CSS `content:` with emoji** in pseudo-elements. Remove emoji, keep text.

### SVG Icon Pattern
```html
<svg width="16" height="16" viewBox="0 0 24 24" fill="none"
     stroke="var(--moonlight)" stroke-width="1.5"
     style="vertical-align:middle">
  <path d="..."/>
</svg>
```

When replacing emoji in JS that sets `.textContent`, change to `.innerHTML`
because SVG markup must be parsed as HTML, not text.

## Enforcement

This gate runs BEFORE the PDF render step. The render script should not be called until the scan returns clean. If you write the document and immediately render without scanning, you have skipped the gate.

## Authoritative Voice

The document should sound like a specific human (the principal, or the routed specialist's persona) wrote it on a specific day. Not like a language model summarized a knowledge base. Plain declarative sentences. Specific facts. No hedging, no meta-commentary about the document itself.

## Pitfalls

- Do NOT replace em dashes with en dashes. That just moves the telltale. Use periods or commas.
- Do NOT strip all formatting. Structure (headers, bullets, bold) is fine when it serves clarity. The tell is when formatting is used as decoration.
- Do NOT over-correct into terse fragments. Plain English sentences have subjects and verbs.
- The scan is a floor, not a ceiling. If a sentence reads as LLM-generated even without matching the checklist, rewrite it anyway.
- Do NOT claim PASS after scanning only the copy-paste body. The scanner runs on the whole path. Headers with em dashes fail the gate even when social body text is clean.

## GATE ORDERING (learned 2026-07-07)

The gate runs BEFORE the first presentation, not as cleanup after the user catches telltales. The failure pattern:
1. Write document via subagent.
2. Render PDF and present to user.
3. User catches em dashes and LLM phrases.
4. Scramble to rewrite and re-render.

Correct pattern:
1. Write document via subagent.
2. Run `scan_ai_tells.py` on the markdown.
3. If FAIL, fix hits and re-scan.
4. Only render PDF and present after PASS.

The scanner is AUTHORITATIVE. In the 2026-07-07 session, the scanner caught a telltale ("just paint on") that survived a manual read. Your eyeballs are the floor; the script is the gate. Never present without running it.

## Subagent delegation rule

When delegating document writing to a subagent, include the full telltale checklist in the context field. Subagents do not load this skill. If you only say "no AI telltales" without listing the specific phrases, they will produce em dashes and LLM phrasing. List them explicitly in the delegation context.
