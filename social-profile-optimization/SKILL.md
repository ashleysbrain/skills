---
name: social-profile-optimization
description: Revamp founder/principal social media profiles (LinkedIn, Twitter/X) with positioning-informed copy. Pulls marketing docs, applies category-play language, drafts multiple versions for user selection.
tags: [linkedin, twitter, x, profile, bio, headline, about, founder, ceo, marketing, positioning]
---

# Social Profile Optimization

Optimize founder and company social media profiles using brand positioning documents, category-play language, and multi-option drafting.

## When to Use
- User asks to revamp, update, or fix their LinkedIn profile
- User asks for a better bio/headline for any social platform
- User wants Twitter/X profile updated to match brand positioning
- User says their current profile "doesn't feel right" or "isn't working"
- Any request to make a social profile more authoritative, catchy, or on-brand

## Workflow

### 1. Gather Current State (ACTUAL text, not cached guesses)
**Priority order for getting the real current profile:**
1. **User-provided screenshots** — if the user sends screenshots, OCR them immediately using `tesseract <path> stdout` (available on macOS). This is the ground truth.
2. **web_search** — search `site:linkedin.com/in "Name" "Company"` for indexed/cached text. WARNING: this can be stale. The Google snippet may show an old version of the bio.
3. **Browser navigation** — LinkedIn redirects to login for private profiles, so this usually fails. Only useful for public profiles.
4. **Session history** — check if a prior session recorded the profile text.

**Always capture the FULL current text** of every section (banner, headline, about, positions) before drafting anything. If you can only get partial text, ask the user to send screenshots or paste it.

If the user mentions a past change they dislike, note exactly what went wrong.
Check session history for any prior profile edits.
Flag any **deprecated brand names** in the current profile (e.g., "QUBIT" is deprecated for DS — maps to "Divinity Health" or removed entirely).

### 2. Pull Brand Positioning Docs
Before drafting ANY copy, find and read:
- **Pitch documents** (one-liner, 50-word, 150-word versions)
- **Marketing advisor reviews** (April Dunford positioning, Steve Krug clarity, etc.)
- **Company context summaries** (brand architecture, key differentiators)
- **Category-play language** (the words the brand OWNS vs avoids)
- **Social post drafts** (already-approved voice/tone samples)

Key directories to check:
- `/<workspace>` for DS positioning
- `/<workspace>` for board reviews
- Corresponding workspace dirs for other brands

### 3. Draft Multiple Options (NEVER just one)
For each profile section, produce **at least 3 versions**:
- A "category play" version (plants the category flag)
- A "founder story" version (personal, builder energy)
- A "short punch" version (scroller-stopper, leaves them wanting more)

Each version gets a one-line recommendation rationale.

### 4. Cover All Profile Elements
Don't stop at the bio. Address:
- **Headline** (LinkedIn: 120 chars; Twitter: display name)
- **About/Bio section** (LinkedIn: 2,600 chars max; Twitter: 160 chars max)
- **Current position title + description**
- **Featured section** (what to pin/link)
- **Skills/Expertise list** (LinkedIn top 10)
- **Custom button** (LinkedIn: label + URL)
- **Location** (keep consistent across platforms)
- **Website** (link to landing page or latest launch)

### 5. Document and Deliver as PDF
**The user needs a document they can read, not a chat summary.** Every profile revamp MUST produce a PDF.

**Format requirements:**
- **Side-by-side layout:** Show the CURRENT (live) profile text in a distinct "old" box (red/warning styling) next to each NEW option in a "new" box (green/accent styling). The user needs to see what they're replacing.
- **Full copy-paste text:** Every version must contain the COMPLETE text, word for word, ready to paste. No summaries. No "Version 1 is about X." The user reads the document, not your explanation of it.
- **Character counts** on every headline and bio to confirm platform limits.
- **"What to fix" notes** between old and new sections explaining why the current text is wrong (specific lines, not vibes).
- **Recommendation section** at the end with the preferred combo.

**PDF generation pipeline:**
1. Write styled HTML to `/tmp/<brand>-profile-revamp.html` with the old/new boxes, labels, and formatting
2. Render with `weasyprint <html> <pdf>` (installed at `/usr/local/bin/weasyprint`)
3. Deliver via `MEDIA:<pdf-path>` in the response

Also save the markdown source to the brand's marketing workspace under `profiles/` or `07-profiles/` for archival.

## Critical Preferences

### Tone (the principal/DS specifically)
- **Authoritative, powerful, "we're onto something"** — the profile should signal momentum and conviction
- **Catchy** — every sentence should be a hook worth reading
- **No generic corporate language** — avoid "interdisciplinary mission," "redefine," "innovative solutions"
- **Category-creating** — use the brand's category language, not the competitor's category
- **April Dunford rule: NEVER use the competitor's category word even to argue against it.** If the category is "wellness app," the word "wellness" must not appear. Plant the new category instead.
- **Author name:** the principal Williams only (never invent "Wallace")
- **Physiomorphic claim (approved):** Divinity Science is the founding research lab and home of Physiomorphic AI; the operator agent is she/her; no consciousness claims
- **Personal About scope:** all-encompassing founder thesis first (coupled human systems + multi-agent AI + product parent), then call out Physiomorphic AI / the operator agent. Not one-topic-only when user wants overall.
- **Low AI-tell structure:** avoid stacked "Not X. Not Y. Not Z." brochure blocks; varied sentence length; real hot terms only
- **Canonical pack:** `your-org-marketing/07-profiles/LINKEDIN-BIOS-PHYSIOMORPHIC-AI.md`
- **PDF:** branded profile PDF only when the principal explicitly asks; otherwise markdown + full paste text

### Workflow Rules
- **User reviews BEFORE deployment.** Never push profile changes without explicit approval.
- **Multiple options always.** The user picks. The agent does not decide solo.
- **Cross-platform consistency.** When doing LinkedIn, also draft Twitter/X in the same pass.
- **Include deployment notes.** The user may need to copy-paste manually (LinkedIn requires authenticated session).

## Pitfalls

- **Don't work from stale cached text.** Google snippets can show an old version of the bio. If there's any doubt, ask the user to send a screenshot or paste the current text. Working from wrong current state means your "before" comparison is wrong and your critiques miss the mark.
- **Don't describe versions without showing them.** The user needs FULL copy-paste text in a document, not descriptions of what each version is "about." If you catch yourself writing "Version 1 focuses on X," stop and write the actual text instead.
- **Don't skip the PDF.** This user works from documents. A chat message with bullet points is not a deliverable.
- **Don't show only the new options.** The user needs to see their CURRENT text alongside the replacements to compare. Side-by-side or sequential old→new is required.
- **Don't scrape LinkedIn without auth.** It redirects to login. Use web_search to find cached/indexed profile content instead.
- **Don't position inside the old category.** If the brand has a category-play strategy, the profile must reflect the NEW category. Every use of the old category word (even in the "About" section) is a loss.
- **Don't write one version and ask "how's this?"** Always present options.
- **Don't update the profile live without review.** The user had a previous session where the profile was changed to something they didn't like. Always draft, present, get approval, THEN deploy.
- **Don't forget the other platforms.** If doing LinkedIn, Twitter/X should be in the same document. If doing Twitter, check LinkedIn consistency.
- **Don't use AI telltales.** No em dashes, no "reaching out," no "passionate about," no "dedicated to." The profile must sound human.
- **Don't leave deprecated brand names.** Check the current profile for any names the user has deprecated (e.g., QUBIT → removed) and flag them in the "what to fix" notes.

## Platform Constraints

| Element | LinkedIn | Twitter/X |
|---------|----------|-----------|
| Headline | 120 chars | 50 chars (display name) |
| Bio/About | 2,600 chars | 160 chars |
| Skills | Up to 50, top 3 visible | N/A |
| Featured | Up to 5 items | Pinned tweet |
| Custom link | 1 button | 1 website URL |
| Location | City/region | Text field |

## Related Skills

- **`social-content-pipeline`** — Generate batches of social media posts from the same positioning docs you used for the profile revamp. When the user finishes approving a profile update, they often want matching content to post. Load `social-content-pipeline` and generate a batch using the same source material.

## Support Files

- **`references/ocr-fallback-for-profiles.md`** — Using tesseract CLI when vision_analyze is quota-blocked
- **`templates/profile-revamp-pdf.html`** — Styled HTML template for the side-by-side old/new PDF. Fill in placeholders, render with `weasyprint`.
