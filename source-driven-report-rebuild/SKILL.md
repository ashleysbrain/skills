---
name: source-driven-report-rebuild
description: Rebuild team-facing reports, decks, and document packs from source files, then verify the rendered artifact and deliver the actual file.
---

# Source-driven report rebuild

Use this skill when the user asks you to *show*, *refresh*, *regenerate*, or *package* a team-facing document, HTML artifact, slide deck, or PDF from existing source material.

## Core principle
Do not stop at a plan or a summary. Produce the actual artifact, verify it rendered correctly, and deliver the file path or media output.

## Workflow
1. **Find the source of truth**
   - Locate the repo files, templates, and existing artifacts.
   - Prefer source docs and existing generated assets over memory.

2. **Preserve scope before you improve presentation**
   - If the user asks to combine documents, merge them into one coherent artifact *without deleting information* unless the user explicitly asks for pruning.
   - Keep the requested family/subcategory structure intact; do not collapse distinct topics into one generic bucket.
   - Preserve the user's requested ordering when it matters: if they say a support family must appear directly after the core metric, do that rather than leaving it buried later in the deck.
   - When a doc spans multiple algorithm families, keep each family visibly separated with its own header, status, and provenance labels.
   - Put the status marker on *each* algorithm or calculation section, not only in the opening summary.
   - When the document mixes standard science with proprietary product logic, label provenance at the *formula level* so each equation is visibly marked as published science or Divinity Science / product-defined logic.
   - When the user says "don't delete anything," treat that as a hard preservation constraint: add a cover/front-matter and merge around the originals instead of pruning sections out.
   - For agent-fleet or roster dossiers, use the full active + inactive source set when the user asks for "all agents" or says the visible roster is incomplete; do not silently narrow to the currently surfaced subset.
    - If a field family is inherently multi-point (for example 5WH-style time, where/location, distance, or path inputs), show the sub-points and intermediate calculations instead of flattening them into one scalar.

3. **Match the requested visual or editorial pattern**
   - If the user asks for “the same layout” or “showable to the team,” mirror the established structure, palette, spacing, and card pattern instead of inventing a new look.
   - Preserve the product language the user requested; avoid broad generalizations.
   - If a section header or badge is hard to read, fix contrast/color in the rendered artifact and re-check the PDF/HTML rather than relying on source markup alone.
   - If the user says the original/base algorithm must be in the document, front-load it as a visible early section or cover callout before the family stack so it is impossible to miss in review.
   - Keep the original family numbering/order intact; surface the base as an anchor, not as a replacement for the family structure.

4. **Edit surgically**
   - Make small, targeted changes.
   - Keep generated prose and structure aligned with the source docs.
   - If the user wants an actual deliverable, produce the file directly rather than describing what would be done.
   - Call out what is *science-based* versus *proprietary / product-defined* when the source mixes standard formulas with custom scoring logic.

5. **Generate the artifact**
   - Build the HTML/PDF/deck from the edited source.
   - If the build fails, inspect the rendered/layout cause before retrying.
   - For combined technical decks, add a short overview that explains how the pieces layer together and how they connect to the surrounding architecture/open-core stack.
   - If a monolithic HTML-to-PDF rebuild becomes unstable for a combined deliverable, generate a small front-matter cover separately and merge the original PDFs with `pypdf` so the source artifacts remain intact.

6. **Verify the output**
   - Confirm the file exists and has nonzero size.
   - Open the HTML/artifact in a browser when possible.
   - Use screenshot or vision review for presentation-quality work.
   - Do not claim success until the rendered artifact has actually been checked.
   - Verify status labels on *each* calculation card/section, not just the top-level summary.
   - For merged PDFs, verify the cover page, the source-document boundary, and the final pages so you know the originals were preserved in full.
   - When rebuilding a large report from markdown, run a text-layer verification pass on the final PDF (for example with `pypdf`) to confirm newly added sections/terms actually made it into the artifact and note their page numbers.
   - If the PDF engine emits pre-existing anchor or layout warnings but still produces an artifact, distinguish those warnings from blockers: verify the actual rendered output before deciding whether the rebuild failed.
## Pitfalls

- **Condensed-artifact substitution**: if the user asked for the full persona/profile pack, do not deliver a summary or lock-in-only artifact; preserve the elite credential stack and full variation detail in the rebuilt output.
- **WeasyPrint empty-page failures**: complex nested grid/flex layouts and page wrappers with `min-height: 100vh` can trigger `page_is_empty` on the first page.
  - Fix by flattening the top-level layout to block flow.
  - Remove page-level `min-height`.
  - Add explicit spacing between sections after flattening.
  - See `references/weasyprint-layout-pitfalls.md`.
- **Versioned naming for Telegram deliverables.** Every PDF sent to Telegram must follow the naming convention: `{DOC_TYPE}_v{MAJOR}.{MINOR}_{YYYY-MM-DD}T{HHMM}.pdf` (e.g., `THESIS_v1.0_2026-06-10T1145.pdf`, `BRIEF_v1.0_2026-06-10T0600.pdf`, `CHECKLIST_v1.0_2026-06-10T0800.pdf`). This allows searching Telegram history by doc type and date. See `references/document-versioning.md` for full convention. (2026-06-10)
- **"Looks right in HTML" but fails in PDF**: browser layout and PDF layout can diverge. Always verify the PDF itself.
- **Concatenated-master anchor trap**: when you rebuild a large master markdown/PDF from many source files and add a front summary or section map, do not rely on guessed heading slugs. Add explicit `{#anchor}` IDs to the sections you link to, then rebuild and verify the links resolved without missing-anchor errors.
- **Local-asset embedding trap**: when a rebuilt markdown references downloaded local screenshots or appendix images, render with an explicit resource path (for example `pandoc --resource-path=.` from the doc directory, or the equivalent absolute path) so the PDF engine can actually embed the files instead of silently replacing them with alt text.
- **Scope drift in composite decks**: if the user asks for a subset of algorithms, do not preserve unrelated families from earlier drafts. Re-check the requested scope before generating the final artifact.
- **Roster recreation trap**: when building an agent dossier or roster evolution pack, revise and reclassify existing agents before inventing new identities; preserve lineage and show current vs proposed roles explicitly.
- **Elite credential trap**: if the user says the earlier work included elite credentials or calls out missing credentials, do not deliver a condensed roster summary; rebuild or send the full persona-profile artifact with the credential stack, variation overlays, and operating rules visible.
- **Fleet scope trap**: when the user says the fleet is "almost 80", "way more than 22", or similar, verify the source dashboard's fleet summary and distinguish the active roster from the larger Target-tier systems-health cohort; do not silently shrink the artifact to only the visible active agents.
- **Deprecated scoring language**: if the user has already rejected a mapping style (for example 1–10 language in Qubit docs), search for it explicitly and replace it before rebuilding.
- **Pointer-only delivery**: if the user expects an attached artifact, include the actual file/media path, not just a description.
- **Recreating existing artifacts**: before building a PDF/HTML/deck, check whether the artifact already exists on disk. If the user asks to "put this into a PDF" and one already exists from a prior turn, open it rather than rebuilding. The user gets frustrated when work is repeated unnecessarily.
- **Calculation grouping**: when a product doc contains multiple calculation families, keep each core equation on its own card or sub-section; do not bundle several formulas into one combined block if the user asked for them separately.
- **Status indicators**: if the user asks whether a calculation is live or still in development, add an explicit stage badge per formula/card (for example LIVE / DEV / SPEC) instead of leaving that status implicit in body text.
- **Readability pass**: if a section header is hard to read, adjust the color/contrast before delivery and re-check the rendered PDF, not just the HTML source.
- **Dark-background PDF readability**: users reading PDFs on dark-mode displays cannot read dark-background documents. Default to a **light warm-cream background** (#faf8f3) with dark text (#2a2a2a), not the DS brand dark palette (#080d1a). When using CSS variables in a build script, swap the `:root` palette block: dark backgrounds become cream, light text becomes dark text, gold/teal accents darken for contrast on light. Verify with pixel sampling — sample the page background RGB and center text RGB in the rendered PDF to confirm the theme actually applied. (2026-06-19)
- **Companion-document pattern for additive content**: when the user asks to add a new layer of content (e.g., technology mappings) to an existing reference document (e.g., a neuroscience atlas), create a **separate companion PDF** rather than modifying the original — especially when the user says "don't delete any content." The original stays untouched; the companion has its own cover, TOC, and branding. This respects surgical precision while delivering the new layer as its own artifact. (2026-06-19)
- **Combined document preference**: when the user asks to merge multiple related calculation docs, produce one coherent source-driven artifact with a clear section/status map rather than two loosely related PDFs.
- **Multi-point fields**: if the source logic treats 5WH-style inputs as more than one point per label, make that explicit in the formulas and callouts; do not flatten sequences/paths into single scalars.
- **Stack explanation**: for technical audiences, add a short “how it layers together” section that explains status, open-core layers, and how the algorithms connect to the surrounding architecture.
- **Companion-doc pattern**: when the user asks for a second document to accompany a main algorithm deck, build it as a sibling artifact with its own status key, architecture stack, open-core vs proprietary split, FAQ, and suggested next pages instead of burying the explanation inside the primary PDF.
- **Cross-link the pair**: add a visible link back to the main algorithm artifact and, when useful, a reciprocal link from the main document back to the companion so the two PDFs/readme pages function as one system.
- **Algorithm interlock map**: when the companion explains gamification or productization, include a short mapping section that names each algorithm family from the primary doc and explains how it changes quests, XP, difficulty, or safety behavior.
- **Finite methodology detail**: for technical audiences, include concrete examples, XP/level drafts, and an engineering appendix so the docs explain calculations at a finite level instead of only describing concepts.
- **Math inclusion requirement** (learned 2026-07-07): when the user asks for a document describing a system, always include the actual math formulas verified from source code. Do not paraphrase formulas from memory. Read the source `.py` files (`grep -n "def.*formula\|def.*energy\|def.*score\|base_xp\|multiplier"`) and copy the real expressions into code blocks in the document. The team needs to see `F = cost - T * info_gain`, not "the task has an energy score." This applies to any document describing a built system: gamification, scoring pipelines, engine design, etc.
- **Engine attribution requirement** (learned 2026-07-07): when describing a multi-component system, name the specific engine and DS-ECS code that powers each component. The user builds by assembling existing parts. Include a table mapping each process stage to its engine name and ECS code. Example: "Action Selection: the specialist engine (DS-ECS-SUB-04.11.01-v1.1.0)". Pull codes from `agent-organism/ecs.py`.

## Session-specific lessons
- `references/qubit-twc-layout-lessons.md` for a compact checklist from the Qubit TWC rebuild session, including the nutrition-family addition, the separate-equations requirement, the per-calculation status indicators, the content-scope correction, and the combined-doc/readability updates.
- `references/combined-master-pdf-editing-lesson.md` for the team-ready combined-PDF pattern: remove meta commentary, merge related docs into one release artifact when requested, keep per-section status labels, and preserve clear layering notes.
- `references/combined-algorithm-master-session-lessons.md` for the merged algorithm-master pattern: one document can hold future and in-progress calculations, but every algorithm still needs its own status, provenance, and layering callout.
- `references/combined-twc-front-loading-lesson.md` for the session where the original TWC base had to be front-loaded visibly before the family stack so reviewers could immediately see the base and beginning of everything.
- `references/combined-algorithm-master-panel-review-2026-06-02.md` for the panel-review rebuild pass that emphasized additive-only edits, explicit per-algorithm status, low-contrast header fixes, evolving formulas, multi-point 5WH-style fields, and text-layer verification for dense repair pages.
- `references/f-string-math-escape.md` for the Python f-string escape pattern used when a builder emits HTML/math text with literal braces or set notation; escape braces first, then `py_compile`, then rebuild.
- `references/vertical-stack-pdf-layout-lesson.md` for the PDF layout repair pattern used when dense card lists (interlock maps, quest examples) need to stay vertically stacked in the final render instead of splitting into a right-side column.
- See `references/divinitygr-companion-doc-lessons.md` for the companion-document pattern used when building DivinityGR as a sibling artifact to the main algorithm deck, including cross-links, status/provenance labels, goal-vs-quest-vs-XP separation, and human-friendly quest naming.
- `references/algorithm-step-containment-map.md` for the step-by-step containment pattern used when the user wants to know which algorithms live inside each step and why.
- `references/per-calculation-provenance-status.md` for the per-equation tagging checklist: status on every calculation, provenance on every layer, multi-point 5WH inputs, and readable header contrast.
- `references/combined-algorithm-master-session-lessons.md` for the combined-deck presentation lessons from the merged algorithm master and gamification docs: no stray team framing, explicit per-card status, readable badges, intentional out-of-order family numbering, and formatted cascade/quest sections.
- `references/sibling-agent-agent-roster-evolution.md` for the agent-dossier pattern that preserves lineage, includes active + inactive roster sources, and recommends revised personas/credentials/skills for existing agents instead of recreating them.
- `references/elite-credential-pack-lesson.md` for the reminder that the full persona-profile pack, not the condensed summary, is the correct deliverable when elite credentials and operating rules matter.
- `references/fleet-target-vs-active-roster-note.md` for the rule that OpenClaw fleet-health rebuilds must distinguish the visible active roster from the larger Target-tier systems-health fleet.
- `references/master-markdown-nav-and-asset-embedding.md` for the concatenated-master report pattern: explicit heading anchors for front summary links, `pandoc --resource-path=.` for local screenshots, and rebuild verification that confirms images embedded instead of collapsing to alt text.

- **Concatenated-master + section-source sync trap**: when a report exists both as per-section source files and as a generated/concatenated master markdown, update the canonical section source *and* the current master artifact if the user needs the PDF refreshed immediately. Otherwise the section source and the shipped report drift apart.
- **Rendered-success vs warning-noise trap**: markdown→PDF pipelines can emit pre-existing internal-anchor or CSS warnings even when the PDF is usable. Do not stop at the warnings; verify the rebuilt PDF's text layer and page hits for the newly added content before reporting success or failure.
- **Text-layer verification gap**: after content additions near the end of a large report, use `pypdf` (or equivalent) to confirm the new headings/terms appear in the final PDF and capture the page numbers for the user.
- `references/competitive-report-master-sync-and-pdf-verification-2026-06.md` for the report-maintenance pattern: patch both section source and master when both are live, treat PDF-engine warnings as data not verdicts, and verify new content in the final PDF text layer.

## Team onboarding / overview documents (learned 2026-07-08)

When writing an onboarding or overview document for a new team member:

1. **Include the COMPLETE engine fleet.** The first onboarding doc listed ~20 engines when 57 exist in the registry. Query `agent-organism/ecs.py` and list EVERY engine grouped by body system. Do not hand-pick a subset. The user caught this: "You only have like a handful of the engines in there and that is not factual. We've got like 100 engines."

2. **8D Technologies, NEVER AD Technologies.** The 8 is the number 8, D is David. This is a recurring error across sessions. Always write 8D.

3. **Female pronouns for all operators.** the operator agent is SHE. Opencode is SHE. Not he, not it. The user corrected this directly.

4. **Include ALL architectural pieces, not just the ones you find interesting.** The first onboarding doc omitted: firewalls/security boundaries, potency tiers and sterility rules, how organisms communicate in the forest, the reproductive process flow (birth canal stages). These are not optional. A new team member needs the complete picture.

5. **Distinguish who drives what.** B2B organisms are driven by the business and its employees. B2C organisms are driven by the individual user (it is THEIR organism). Products are tools born from organisms. This distinction matters for understanding the system.

6. **Include the reproductive process flow.** The birth canal stages (gametogenesis through birth, with physics at each stage) ARE the product creation pipeline. Do not omit them. Do not call it "software factory" in external-facing documents.

7. **Redo fully when the user says it is wrong.** Do not patch a fundamentally incomplete document. The user said "go and do this again" because the first version was missing too many pieces. A redo is a full rewrite, not incremental fixes.

## Delivery checklist
- Source updated
- Artifact generated
- Visual/layout check completed
- Final file path or MEDIA attachment ready for the user

## Related support files
- `references/weasyprint-layout-pitfalls.md`
- `references/playwright-visual-asset-capture.md` — Playwright CLI page-screenshot capture for embedding local visuals in PDF reports (no Node API required).
- `references/combined-algorithm-master-2026-06-02.md`
