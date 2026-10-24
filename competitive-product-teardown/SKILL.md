---
name: competitive-product-teardown
description: Multi-agent competitive landscape research across multiple product categories. Delegate teardowns to specialist agents, compile into a unified report with inline screenshots, and deliver as PDF.
tags: [competitive, research, teardown, landscape, multi-agent, product-analysis]
---

# Competitive Product Teardown

## When to use
- User asks for competitive landscape research, market analysis, or product teardowns across multiple apps/products/categories.
- The research spans enough territory that a single agent would time out (5+ products, multiple dimensions/categories).
- The final deliverable is a report (markdown + PDF) with inline product screenshots.

## Core pattern

### 1. Define categories and scope
Break the landscape into discrete categories (one per agent or 2–3 per agent). Examples:
- By domain (sleep apps, fitness trackers, mental health platforms, financial wellness)
- By user segment (consumer, clinical, enterprise)
- By dimension (if the product has dimensional scoring, one agent per dimension)

Each category becomes one delegated task.

### 2. Design the teardown template
Create a standard template each agent fills for every product:

```markdown
## [Product Name]
- **Company:** parent company, location
- **Funding:** total raised, latest round, investors
- **Tech stack:** what powers it (ML models, sensors, APIs)
- **Core algorithms:** what scoring/recommendation methods they use
- **UX / design language:** clean/clinical/gamified, key UX patterns
- **Market position:** target user, pricing tier, differentiator
- **Screenshot:** ![Product screenshot](assets/product-name.png)
- **Relevance to our product:** what to adopt, avoid, or differentiate from
```

### 3. Delegate with skeleton-first discipline
Each agent must:
1. Write a skeleton file (headings + first facts) after the first 2–3 searches.
2. Expand each section iteratively.
3. Stay within scope (2–3 products per agent max for deep teardowns).

If an agent times out with a partial file, spawn a follow-up to expand the skeleton rather than re-running the full scope.

### 4. Collect screenshots inline
- Capture screenshots during research (browser tools) or pull from public sources.
- Each screenshot goes into an `assets/` directory under the report folder.
- **Critical:** embed screenshots inline in the markdown next to the product analysis that discusses them. Never group all screenshots in an appendix at the end.

### 5. Compile and render PDF
1. Concatenate all category markdown files into one master file in the correct order.
2. Add a front summary/navigation page with section links.
3. Convert: pandoc markdown → html5 → weasyprint PDF.
4. Use CSS `@page { margin: 2.5cm; }` for readable mobile margins.
5. Use `img { max-width: 100%; height: auto; }` for responsive images.
6. Verify file size is proportional to input (not blank/tiny).

**Compact delivery option:** If the user wants the PDF condensed (fewer pages, same content), rebuild with compact CSS (0.4in margins, 7.5pt body) from the markdown source. See `ocr-and-documents` skill → Method A. Typical result: 60–65% page reduction at readable 7.5pt fonts. Always offer this after delivering the full-size report.

### 6. Deliver
Send the PDF via `MEDIA:/absolute/path/to/report.pdf` in the user's messaging platform.

## Chunk sizing rules
- **2–3 products per agent** for deep teardowns (300+ lines per product).
- **1 product per agent** when each requires extensive web research.
- Scopes wider than 3 products per agent consistently hit timeout ceilings.
- If the user's list has 5+ products, split into part-1/part-2 tasks automatically.

## Sequential vs parallel
- Default: sequential (one agent at a time) — prevents API rate-limit issues and lets each agent build on a shared understanding.
- Parallel only if the user explicitly requests it or the categories are truly independent with no shared analysis.

## Report structure
1. Summary/navigation page
2. Executive overview of the landscape
3. One section per category, each containing:
   - Category overview
   - Per-product teardown (company, tech, algorithms, UX, market, screenshot, relevance)
   - Category-level takeaways
4. Cross-category synthesis
5. Strategic recommendations for the user's product

## Clone-and-Enhance Strategy (for DS products)

When the user wants to ship a product by cloning an existing app and enhancing with 8D/PIML:

### Mandatory Phase Order (user enforced)
1. **Research** — Identify top clone targets. Multi-agent competitive research across the market.
2. **Select** — User picks the app. Do NOT proceed to panel/fleet until user confirms.
3. **Define Panel** — Spin up advisory board specific to the selected app.
4. **Define Fleet** — Spin up elite DS agents for implementation.
5. **Build** — Execute through the the specialist engine engine (phase-gated, no step runs until prior completes).
6. **Ship** — App Store submission.

**Rule:** Do NOT execute any step until the step before it is complete. The user was explicit about this. Research first → panel second → fleet third → build fourth → ship fifth. No skipping ahead.

### Clone Research Requirements
- Top 10 apps ranked by: revenue × clonability × 8D dimension fit
- Deep dive on anchor app (features, pricing, retention hooks, tech stack, vulnerabilities)
- PIML enhancement potential analysis (which physics can amplify each category)
- All three research streams should run in parallel as delegated subagents

## Pitfalls
- **Finding the right document:** when the user says "you created it last night" or "the document you sent me," use `session_search` with a date-filtered query (e.g. "competitive landscape report") to find the exact file path from the prior session — do NOT guess from filesystem filenames and page counts.
- **Appendix screenshots:** user has corrected this multiple times — screenshots MUST be inline, not appended. Remove any "Visual Survey" or "Screenshot Appendix" section once images are moved inline.
- **Narrow margins:** default PDF margins are too tight for mobile review. Always set >=2.5cm.
- **Agent timeout with no file:** enforce skeleton-first write. If agent still times out, re-dispatch with smaller scope.
- **Missing screenshots:** some sites block automated browsers. Note which products couldn't be captured rather than leaving blank space silently.
- **Orphan appendix:** if you move screenshots inline, delete the appendix section entirely. Partial moves are worse than no move.
- **Firecrawl/web_search billing exhaustion (learned 2026-08-08, refined 2026-08-08):** The Firecrawl backend powering web_search and web_extract can hit a 402 "insufficient funds" billing error that affects ALL three tools simultaneously (web_search, web_extract, AND subagent web_search calls — they share the same backend). When this happens, `browser_navigate` (Browser Use) is a separate backend and continues working for **direct site navigation** (product pages, pricing, docs). Browser snapshots return rich structured data. **BUT search engines (Google, DuckDuckGo, Brave) ALL serve CAPTCHAs via the browser too** — you cannot use the browser as a search-discovery fallback. When web_search is down, use `curl` + Wikipedia API for term discovery and `curl` direct URLs for product pages, and `raw.githubusercontent.com` for GitHub repos. See `direct-source-research` skill for the full curl-only technique. **Fallback chain:** web_search/web_extract -> curl (Wikipedia API + direct URLs + raw.githubusercontent.com) -> browser_navigate for direct pages only (NOT search) -> browser_snapshot (full=true) -> note as inaccessible.

## Reference files
- `references/8d360-competitive-research-session.md` — full session pattern for the 8D360 nine-dimension competitive teardown (14 markdown files, 26 inline screenshots, 210-page PDF).

## Related skills
- `agent-delegation-discipline` — when to delegate vs do yourself
- `telegram-pdf-bundle-delivery` — PDF rendering and delivery pipeline

## Single-platform deep dives
For researching ONE platform in depth (the user has it open in Chrome and wants a deep dive to clone or build their own version), use the platform deep-dive pattern instead of the full multi-agent teardown:
- `references/platform-deep-dive-pattern.md` — AppleScript Chrome tab enumeration, llms.txt doc dump, dashboard KPI extraction, architecture primitive mapping, and isomorphism design. Use when the user says "deep dive into [one platform]" or "build our own version of [one platform]."
