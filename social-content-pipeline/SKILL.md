---
name: social-content-pipeline
description: Generate batches of social media posts (Twitter/X, LinkedIn) from marketing positioning documents. Covers post types, cadence planning, image concept research, PDF delivery, and the approval-before-posting workflow.
tags: [twitter, x, social-media, content-generation, marketing, positioning, posts, batch, cadence, pipeline]
---

# Social Content Pipeline

Generate batches of on-brand social media posts from marketing positioning documents, deliver as copy-paste-ready PDFs, and set up recurring content pipelines where agents generate content and the user approves before posting.

## When to Use
- User asks to "generate posts" or "write tweets" for any brand
- User wants a batch or queue of social media content
- User asks to set up a recurring content generation pipeline
- User says "I need posts for Twitter" or "give me content for this week"
- After completing a profile revamp and the user wants posts to match

## Workflow

### 1. Gather Positioning Source Material
Before writing ANY posts, find and read the brand's marketing docs:
- **Pitch documents** (one-liner, 50-word, 150-word versions)
- **Social post drafts** (previously approved voice/tone samples)
- **Company context summaries** (brand architecture, differentiators)
- **Category-play language** (words the brand OWNS vs avoids)
- **Positioning reviews** (advisor feedback on voice, category, claims)

Key directories to check:
- `/<workspace>` for DS positioning
- `/<workspace>` for board reviews
- Corresponding workspace dirs for other brands

**Never write posts from memory alone.** Always read the source docs first. The posts must reflect the brand's current positioning, not a generic version of it.

### 2. Generate a Batch (minimum 8-10 posts)
Cover multiple post types so the user has variety for the week:

| Post Type | Purpose | Example Hook |
|-----------|---------|-------------|
| Curiosity Hook | Stop the scroll with a surprising connection | "Your sleep and your bank account are the same problem." |
| Data Insight | Credibility through science/research | "The INTERHEART study found 90% of heart disease risk is modifiable." |
| Personal Story | Vulnerability + "I learned the hard way" | "I built an AI that told me X. I ignored it." |
| Category Break | Define what you are by what you're NOT | "Most apps pick one thing. We track the pull." |
| Founder Origin | Why you built this for yourself first | "My brain doesn't run default settings." |
| Build Progress | Building in public updates | "Week 1: built the coupling engine." |
| Competitive Reframe | Handle the "so you're like X?" question | "Noom optimizes habits. We optimize the system." |
| Community Question | Engagement hook, gets replies | "What's the one thing that, when it breaks, everything falls apart?" |
| Worldview | Philosophy without sounding like a mission statement | "Healthy people build better worlds." |

Each post should be:
- **Under 300 characters** for Twitter/X (280 is the real limit, leave room for URLs)
- **Self-contained** (works without context from previous posts)
- **Compounding** (by the end of the batch, someone who saw all of them has the full picture)
- **Free of AI telltales** (no em dashes, no "furthermore/moreover/additionally," no three-item parallel lists)

### 3. Research Image Concepts
For each post or post group, identify what visual would make it hit harder.

**Preferred image types (in order):**
1. **Field-intro / brand heroes (when user asks for world-class image)** — Fine-art scientific Grok Imagine work (`ai-image-generation` + `references/grok-xai-image-path.md`). Process-flow and coupling motifs inspire; **never clone Fleet Atlas PDF covers**. Landscape 16:9 LinkedIn default. Prompt budget ~900 tokens.
2. **Data visualizations** — Network graphs, heatmaps, bar charts based on real studies or real product math
3. **System diagrams** — Cascade flows, coupling matrices (no secret coeffs in public), ripple diagrams
4. **Comparison splits** — "How everyone else does it" vs "How we do it" side by side
5. **Infographics** — Research findings visualized (e.g., INTERHEART study breakdown)

**NOT preferred:**
- Generic stock AI clichés (neon brains, purple cyberpunk, equal hub-spoke webs)
- Fleet Atlas brochure / PDF cover layouts on social
- Flowchart boxes + labeled arrows as "the art"
- Generic stock photos
- Text-on-gradient quote cards

For each image concept, specify:
- What data or concept it visualizes
- What tool creates it (Grok Imagine quality, D3, matplotlib, Figma, etc.)
- Which posts it pairs with
- Key design elements (color coding, dimensions, labels)
- For Grok heroes: point at the locked prompt pack in the post markdown when one exists

**Physiomorphic LinkedIn hero (2026-08-02):** extend canonical file section **LinkedIn hero image — Grok prompt pack**; asset example `02-social-posts/assets/physiomorphic-ai-linkedin-hero-v1.png`. Details in `references/physiomorphic-linkedin-pair-and-audience.md`.

### 4. Deliver as PDF
**The user works from documents, not chat messages.** Every content batch MUST produce a PDF.

**Format requirements:**
- Each post in its own styled box with a post number and type label
- Full copy-paste text (not summaries of what the post is "about")
- Character count on every post
- Tags on standout posts (e.g., "starter," "strongest," "engagement")
- Image concepts section with clear descriptions
- Cadence recommendation (which post on which day)

**PDF generation pipeline:**
1. Write styled HTML to `/tmp/<brand>-content-batch-N.html`
2. Render with `weasyprint <html> <pdf>`
3. Deliver via `MEDIA:<pdf-path>` in the response

Also save the markdown source to the brand's marketing workspace under `02-social-posts/` or equivalent.

### 5. Set Up Recurring Pipeline (when requested)
When the user wants agents generating content regularly:

1. **Confirm posting tool is authed** — check `xurl auth status` (xurl is the official X platform CLI, installed at `/usr/local/bin/xurl`). If no apps registered, the user must complete one-time OAuth setup outside the agent session (see `xurl` skill for steps).
2. **Define cadence** — recommend 1 post/day, Mon-Fri, rotating through post types (see cadence table below)
3. **Set up cron job** — agent generates content batch weekly, delivers PDF for approval, then posts on schedule after approval
4. **Approval gate is mandatory** — never post without explicit user approval. The pipeline generates and queues; the user approves.

**Recommended weekly cadence (Sahil Bloom pattern):**
- Monday: Curiosity/pattern hook
- Tuesday: Data/science angle
- Wednesday: Personal story or founder moment
- Thursday: Build progress or competitive reframe
- Friday: Community question or worldview

## Critical Preferences

### Task Deferral Discipline

**NEVER defer social content generation without capturing it in the task tracking system.**

If the user requests content and you propose doing it "tomorrow" or "overnight" or via a cron job, you MUST:

1. Capture the deferred task in the todo list first using `todo(todos=[{...}])`
2. Include the full scope: platform, quantity, brand positioning sources, deliverable format
3. Then propose the deferral strategy (cron job, overnight batch, etc.)

When deferring, the todo entry `content` field must include:
- Platform(s) (LinkedIn, Twitter/X, both)
- Quantity (minimum 8-10 posts)
- Brand positioning sources to read
- Deliverable format (PDF, markdown, both)
- Timeframe (by when)

Example todo entry:
```
{
  "id": "linkedin-content-week-1",
  "content": "Generate LinkedIn content batch (8-10 posts) for next week: AI modeled on human biology, 8D wellness, health-tech alignment. Read positioning docs from /<workspace>, deliver as PDF with post text, cadence recommendations, image concepts.",
  "status": "pending"
}
```

Only defer when genuinely justified (late hour, creative task requiring fresh perspective). If the task can be done now, do it now.

### Tone (the principal/DS specifically)
- **Authoritative, builder energy, "we're onto something"**
- **No generic corporate language** — avoid "redefine," "innovative solutions," "interdisciplinary"
- **Category-creating** — use the brand's category language, never the competitor's
- **April Dunford rule: NEVER use the competitor's category word even to argue against it.** If the category is "wellness," the word "wellness" must not appear. Plant the new category.
- **No clinical labels** — for DS, use "my brain doesn't run default settings" instead of naming diagnoses
- **No deprecated brand names** — "QUBIT" is deprecated for DS, "Qubit" maps to Divinity Health

### the principal personal voice lock (binding · 2026-08-02)
User correction after LinkedIn personal lead-in failed (chat-lowercase + slang-casual):

the principal does **not** speak with poor grammar. She is **eloquent and simple**: intelligent without academic density or exclusivity; clear to any level (student, clinician, coach, researcher, builder) in the same draft.

| ALLOWED | FORBIDDEN |
|---|---|
| Correct grammar always | Chat-lowercase ("i did not…", all-lowercase paragraphs) |
| Capital pronoun **I**; capital sentence starts | Slang-as-personality ("okay real talk") |
| Warm, plain, precise | Careless "casual" as quality excuse |
| Short clear sentences | Paper-abstract / methods-section mirror |
| Informal = approachable | Informal = broken English |

`scan_ai_tells.py` does **not** catch lowercase "i". Manual grammar pass is mandatory before presenting any the principal-facing social copy even when the scanner PASSes. If a draft sounds like Gen-Z chat OR like a paper, rewrite.

See `references/physiomorphic-linkedin-pair-and-audience.md` for DS+repost pair, adaptive methodology block, and field-implications checklist (v5/v6 pair).
### Workflow Rules
- **User approves before ANY posting.** Always.
- **Deliver full copy-paste text in workspace markdown + chat.** Produce branded PDFs only when the principal explicitly asks (standing preference). Social skill historically preferred PDF-first; that yields to: PDF on request.
- **Batch size: 8-10 posts minimum.** Enough for a full week plus spares.
- **Include image concepts.** Even if images aren't ready, spec them so the user can commission them.
- **Cross-platform awareness.** If generating Twitter posts, check LinkedIn consistency and vice versa.

## Founding-Lab / Field Launch (Physiomorphic AI)

When introducing a **new field**, naming an organism, or establishing Divinity
Science as founding lab: process first, not a normal post batch.

1. Positioning lock → 2. VERITAS claim ledger → 3. Academic → Substack → LinkedIn → atoms → 4. Approval

| Role | Value |
|---|---|
| Field | Physiomorphic AI |
| Lab | Divinity Science (founding research lab **and home** of the field) |
| Founder | the principal Williams (never invent surnames; not Wallace) |
| Organism | the operator agent (she/her) |
| Defining sentence | Neuromorphic mimics the neuron. Physiomorphic mimics the organism. |

Forbidden: the operator agent is conscious; trademark granted until true; calling DH products "DS products".

**Approvals 2026-07-09:** founding lab + home; the operator agent she/her; same-day abstract+Substack; personal About = overall founder thesis then Physiomorphic callout.

Package paths under `your-org-marketing/`:
- `04-long-form/PHYSIOMORPHIC-AI-FOUNDING-LAB-LAUNCH.md`
- `05-newsletter/PHYSIOMORPHIC-AI-FOUNDING-ESSAY-SUBSTACK.md`
- `02-social-posts/PHYSIOMORPHIC-AI-LAUNCH-BATCH-1.md` (approved personal / L-series)
- `02-social-posts/DIVINITY-SCIENCE-LINKEDIN-the operator agent-PHYSIOMORPHIC.md` (company v5 + personal repost v6 + AIEO FAQ + image noodles; extend this file)
- `07-profiles/LINKEDIN-BIOS-PHYSIOMORPHIC-AI.md` (personal + company About)
- `PHYSIOMORPHIC-AI-SAME-DAY-LAUNCH-KIT.md`

User correction: field launch is not a Wernicke-only job — use marketing metabolism process flow.

### Company page vs founder page (learned 2026-07-09)

| Surface | Voice | Pattern |
|---|---|---|
| Divinity Science company LinkedIn | **we** | Lab claim + field definition + the operator agent as first organism |
| the principal personal LinkedIn | **I** | Naming the field + sole architect + Substack/TSC URL |
| X pin | Short lock pair | Defining sentence + lab + the operator agent |

Do not ship a personal "I am naming a field" post from the company page. Do not invent a parallel field claim that drifts from the locked table. Read the approved batch + bios + launch kit **before** drafting; extend those files rather than freewriting from memory.

### Source-first for the operator agent / Physiomorphic requests

If the ask is "LinkedIn post introducing the operator agent and Physiomorphic AI":
1. Read launch kit + launch batch + company section of LinkedIn bios
2. Confirm company page vs founder page
3. Prefer editing approved copy over greenfield drafts
4. Run `ai-tell-removal-gate` on the **full** markdown path (headers included)
5. Save under `02-social-posts/`; present full copy-paste text in chat
6. Auto-post forbidden; the principal presses publish

Specialist note: the specialist engine may route "LinkedIn" situations toward the specialist engine (palette). For brand-voice social copy, wear **the specialist engine** and use the marketing metabolism process for field launch, not visual-cortex palette generation.

### Mixed professional room (learned 2026-08-02)

the principal's LinkedIn network is **not** a pure AI-builder feed. Typical room: medical, psychology, pro sports / performance science, students, Harvard/MIT-linked researchers, plus tech. Field intros must speak to that room **indirectly**.

**Hard correction:** first Physiomorphic "world intro + performance" draft read like a **mirror of the scientific paper/abstract** (numbered performance list, isomorphism jargon dump, builder-only close). Rejected as not sociable enough for the real audience.

**Rules for field-intro LinkedIn:**
1. **Shared pattern first, job titles never as targeting.** Open on a lived cascade (sleep → attention → patience → decisions; load management). Clinic, sport psych, classroom, and lab all recognize the same pattern without being name-checked as segments.
2. **Sociable + informative + enticing, not paper tone.** One clean idea in the body. Short paragraphs. Invitation to comments beats abstract structure. Heat without hype words.
3. **No school name-drops** (Harvard, MIT, etc.) in the body. Elite-adjacent people should feel the seriousness from clarity and category lock, not flattery.
4. **Split human post vs AIEO pack.** Main post = story + locked defining sentence + lab/the operator agent + why it matters in life/work. Put dense extractable entities (what/who/where/the operator agent/performance/terms) in the **first comment FAQ** so AI answer engines still get clean attribution without making the feed post sound like a paper.
5. **Field implications are required** when the ask is "introduce to the world" / methodology / performance. Map what changes if the methodology lands for: medicine/clinical, psychology/behavioral, sport science/high performance, AI multi-agent engineering, students/early researchers, labs/universities/R&D. Keep each block 2-4 plain sentences. Do not dump paper mechanisms.
6. **Hashtags mix rooms.** Not all-tech. Include performance/health/sport/cognitive/medical tags alongside PhysiomorphicAI, MultiAgentSystems, AIArchitecture.
7. **Image noodles before design.** For field-intro heroes: Grok fine-art scientific (coupling network + cascade, not Fleet Atlas PDF). Also: cascade card; neuron|organism split; carousel A→B→quote+entities for saves+AIEO. Avoid paper-figure dumps, neon brain cliches, stock sport photos, soft "wellness" pastels, flowchart brochure layouts. Full entity lock in alt text. See `references/physiomorphic-linkedin-pair-and-audience.md` image section + `ai-image-generation` grok path.
8. **Canonical path:** extend `02-social-posts/DIVINITY-SCIENCE-LINKEDIN-the operator agent-PHYSIOMORPHIC.md` rather than greenfield files when baseline-first gate is on.

### DS company + founder repost pair (learned 2026-08-02)

When the principal wants a lab post **and** a personal statement:

| Order | Surface | Job |
|---|---|---|
| 1 | Divinity Science company (**we**) | Full public definition + **adaptive methodology** + field implications + the operator agent + non-claim + enticing close |
| 2 | Company first comment | AIEO FAQ (implications-by-field + adapts-to-user + entities) |
| 3 | the principal personal | **Repost/share** DS with a **thought on top** (reader sees personal first, then embedded DS) |
| 4 | Optional | Short/ultra personal thought if primary is too long |

**Personal thought rules:**
- Sits **above** the DS post. Different capture angle: why she cares + handoff. Does **not** re-teach definition/implications.
- Voice = the principal personal voice lock (eloquent + simple). Not chat-casual. Not paper.
- Offer primary + short + ultra-short.
- Same day: do **not** also ship a second long personal primary essay unless she explicitly wants two full posts.

**Company adaptive block (when personalization is in scope):**
- **It adapts to the user:** personalization, customization, ease of use by experience level.
- Beginner clarity + advanced depth without drowning beginners. Teams shape to sport/clinic/lab/workflow.
- Personalization is not a skin. Customization is not a settings graveyard. Ease of use is not dumbing science down.
- Fold adaptivity into field blocks (clinician vs trainee; athlete-simple vs staff-deep).

**Canonical file:** extend  
`your-org-marketing/02-social-posts/DIVINITY-SCIENCE-LINKEDIN-the operator agent-PHYSIOMORPHIC.md`  
(COMPANY v5 · PERSONAL REPOST v6 · FIRST COMMENT · IMAGE NOODLES).

Detail banks: `references/physiomorphic-founding-lab-launch.md`, `references/physiomorphic-linkedin-pair-and-audience.md`.

### LinkedIn program architecture (RE-ARCHITECTED by principal · 2026-08-16, supersedes the two-newsletter pair)

**COLLAPSED DECISION:** Divinity Science COMPANY page hosts the newsletter(s). the principal PERSONAL page runs regular standalone posts engineered for virality: each post delivers full value alone (no subscription required) but synergizes with the newsletter via last-line handoffs, first-comment questions, and selective company reposts (company reposts personal ONLY when a handoff became a real lab milestone; never Field Breaker posts, company owns the definition).

Cadence: 2-3 personal posts/week max (1-2 viral candidates + 1 connective tissue; 48-hour rule between candidates). Viral post system with 6 archetypes, standalone test, and corrected first-five sequence: `THREAD-4-VIRAL-POST-SYSTEM.md` in the workspace. Newsletter editorial architecture and format skeletons: `THREAD-4-LINKEDIN-NEWSLETTER-PLAN.md` (post-audit edition). Platform facts table (verified live against LinkedIn Help 2026-08-16: personal profiles get newsletter access unconditionally; company Pages need 150+ followers + content history to be evaluated; 5 newsletters max; 2-week create/delete cooldown): same plan doc section 0.

Newsletter drafts must never quote the corrupted variant of the defining sentence ("Neuromingular"); reconstruct to "Neuromorphic mimics the neuron. Physiomorphic mimics the organism."

### Brainstorm and plan BEFORE writing (hard correction 2026-08-16)

"i want to see the topic ideas first as a brainstorm before you actually write them... we must build the plan." Topic pools go to the principal as an adjustable batch FIRST. No drafting, no pipeline runs, until topic verdicts come back. A premature pipeline launch this session failed the gates twice and wasted both runs.

### Deliverables live in the Writing Studio UI, not chat (hard correction 2026-08-16)

"why don't i see it in my ui? i need to work on these from the writing studio" + "I want these to be in drafts in a batch and each topic needs to be adjustable." Topic ideas go into the DRAFTS table (POST /api/drafts, stage=ideation), NOT the brainstorms table and NOT chat-only markdown. Each topic draft carries metadata: batch_id, batch_name, dedup_key, launch_mode=solo, remains_linked_to_batch, surface (company|personal), pillar, evidence_grade (A/B/C), trajectory_role {role, phase, rationale}. The principal edits, re-scopes, and kills in the Workshop view.

### Batches launch solo with lineage + posting intelligence (2026-08-16)

principal requirement: items "launch solo in the system but still link to the batches... ensure we don't duplicate and we post intelligently based on what we have posted in the past and our future trajectory and desire to go viral." Full data model spec: `THREAD-4-POSTING-INTELLIGENCE-SPEC.md` (post_batches, posting_memory, calendar_slots, trajectory_phases; 3-gram Jaccard dedup with 180-day block / 365-day fresh-angle thresholds; 7-factor virality rubric scored at approval and re-scored from engagement; principal approval hard-gated before any scheduled state).

### Adversarial pre-read gate (standing 2026-08-16)

"do another pass to ensure quality of content before I read. adversarials." Before presenting ANY plan or content batch: (a) mechanical scan (em dashes, banned words, fabrication-residue regex, metadata/tag grade consistency), (b) the specialist engine falsification dispatch reading the actual docs and drafts against live state. Fix everything both find, THEN present. The mechanical pass alone caught fabricated claims still asserted inside a draft brief after the metadata downgrade, and missing graduation conditions on two C-grade briefs.

### Delegate outputs get fabrication-screened (2026-08-16)

A specialist spec re-injected the fabricated 48h sleep/finance claims FOUR HOURS AFTER the audit caught them, in the same program, marked [NEEDS DATA] in a footer but presented as fact in the table. Screen every panel/delegate output against the known-false list before folding into plan docs. See `claim-evidence-grading` skill. Also scrub delegate outputs for em dashes and non-English leakage (one spec shipped two Chinese lines; caught and translated).

## Pitfalls

- **Don't write posts from memory.** Read the source marketing docs first. Generic posts that don't reflect the brand's actual positioning are wasted effort.
- **Don't invent Physiomorphic/the operator agent language when approved copy exists.** Founding claims are locked (2026-07-09). Freehand drafts create claim drift.
- **Don't mix company-page "we" with founder "I" on the wrong account.** Company announces the lab and field; founder carries sole-architect and academic path.
- **Don't describe posts without showing full text.** "Post 4 focuses on category positioning" is useless. Show the complete copy-paste text.
- **Don't force PDF when the principal did not ask.** Branded PDFs only on explicit request; default is markdown + chat paste.
- **Don't default every image to "no AI art" or to Fleet Atlas PDF grammar.** (2026-08-02) Field-intro heroes may be fine-art Grok Imagine work with constrained prompts. Banned: generic AI clichés and document clones. Prefer coupling/cascade scientific art; load `ai-image-generation` + grok-xai path. Still prefer real data viz for weekly batch posts when the ask is not a brand hero.
- **Don't post without approval.** Even if xurl is authed and ready, every post goes through the user first.
- **Don't use AI telltales.** Zero em dashes. Zero "furthermore/moreover/additionally." Varied sentence lengths. Fragments are good. Scanner runs on the **full** markdown path (headers and image-option titles included). Midpoint dashes in `### Option A — Title` fail the gate; use `### Option A: Title`.
- **Don't reuse deprecated terms.** Check the marketing docs for current vs deprecated brand names.
- **Don't forget LinkedIn when doing Twitter (or vice versa).** Social content should be cross-platform aware even if the immediate request is for one platform.
- **Don't mirror the TSC abstract / academic paper on LinkedIn.** (2026-08-02) Numbered performance mechanisms, isomorphism jargon blocks, and builder-only CTAs fail a mixed medical/psych/sports/student room. Sociable cascade opener + defining sentence + first-comment AIEO FAQ instead.
- **Don't segment-target in body copy.** No "for Harvard and MIT professionals" or job-title laundry lists as the pitch. Indirect shared pattern only.
- **Don't put the entire AIEO entity dump in the main post.** Keep the feed human; park What/Who/Where/the operator agent/Terms in the first comment.
- **Don't skip cross-field implications on world-intro posts.** (2026-08-02) User asked explicitly for methodology implications across fields. Company post must include medicine, psych, sport/performance, AI engineering, students, labs/R&D in plain language.
- **Don't make the personal piece a second full essay when she is reposting DS.** Personal = commentary thought on the share. Lab carries definition + implications.
- **Don't ship company "I founded" voice or personal "we the lab" voice.** Surfaces stay split even in the pair workflow.
- **Don't use chat-lowercase or slang-casual as "less formal."** (2026-08-02) the principal rejected lowercase "i" and "okay real talk." Eloquent + simple only. Scanner PASS is not enough without a manual grammar pass.
- **Don't omit adaptivity on world-intro / methodology posts when she asks for personalization.** Experience-level ease of use and customization belong in the DS body and field blocks.

### The topic-batch discipline (learned 2026-08-16, principal correction)

principal correction: "I want them batched together in the workshop as we are working on them so this running list doesn't run forever... this is a lot of content we will be writing so we need to organize appropriately."

The failure: topic drafts accumulated across three rebuild iterations (12 + 5 + 5 scattered drafts with different batch IDs), producing an ever-growing list instead of a working set the principal can review.

**The rules:**
1. **ONE active topic batch in the Writing Studio at a time** (e.g. BATCH-1-LINKEDIN-LAUNCH). Before creating a new batch, archive every draft of the old one. A running list that never ends is disorganization, not a backlog.
2. **Slot cap per batch** (10 default). A new topic requires a slot to open: a topic published, killed, or merged. The cap forces curation decisions instead of accumulation.
3. **Evolution = edit in place.** When reality changes (new product, new milestone, corrected claim), edit the existing draft's brief. NEVER append a new draft for the same topic. Every brief carries the rule so any future agent reads it.
4. **Uniform metadata keys on every batch draft**: batch_id, batch_name, surface (company|personal), content_type (newsletter|viral_post), evidence_grade, source_asset (the disk artifact proving the facts), voice_protocol, launch_mode: solo. Uniform keys make the batch filterable and joinable by the posting-intelligence layer.
5. **Attribution rule for first-person titles** (the subtlest fabrication class, caught 2026-08-16): "I built a fact-checker" is FALSE when the lab's agent pipeline built it under her direction. Personal I-voice may claim only verbs the human performed: founded, named, submitted, defined, directed, chose, specified. Lab work executed by agents under her direction is we-voice or "under my direction." Check every personal title verb against who actually performed it.

### Never guess personality type or psychometric scores (learned 2026-08-05)

the principal's tested MBTI is **ENFP-A (Assertive variant), self-described ambivert
leaning introverted.** OCEAN is **not formally tested.**

An earlier session fabricated an INTJ/INFJ hybrid MBTI and invented OCEAN
percentile scores based on behavioral observation. the principal caught it:
"How do you know my personality type? you are wrong based on what I test."

Rules:
- **Never invent psychometric data.** If you do not have tested results,
  say "not formally tested" or ask. Do not back-fill from behavior.
- MBTI and OCEAN are different frameworks. MBTI does not imply OCEAN scores.
- If scores are needed for a voice profile or engine config, recommend a
  credible free test: **IPIP-NEO** (Johnson's hosted version at
  https://personalitytest.net/ipip/ipipneo300.html, ~300 items, public
  domain, the academic gold standard). Not 16Personalities for OCEAN (it
  is MBTI-based).
- When web search is credit-blocked, give the recommendation from domain
  knowledge. Do NOT skip the recommendation because you cannot search.

### Never invent founder interiority (learned 2026-08-16, fabrication class 3)

the principal's correction, near-verbatim: "you're making things up about me that are
not factual. take what i have worked on and use it and don't make shit up.
i want to be authentic as authenticity is an incredibly powerful vibration
in the world."

The failure: personal-page topics carried agent-authored feelings, reactions,
and history ("I ignored the warning signal for three weeks"). None of it
happened. Well-voiced fabrication is worse than none: it borrows her identity
to lie.

**The founder-content protocol (binding):**
1. Every personal topic is built from VERIFIED events/artifacts only: git
   history, submitted abstracts, live code, logged runs, dated documents.
   The scaffold lists the facts and cites the artifact.
2. The brief carries a **[principal VOICE SLOT]**: the feelings, the why, the
   reactions are HER words, supplied by her (voice note or draft). The agent
   writes facts and structure, never interiority.
3. First-person claims without a verified event behind them are not B-grade
   (rewordable). They are disqualified entirely.
4. Her authentic voice EXISTS in the record: read the canonical TSC abstract
   for register (precise, self-caveating: "These are initial results; further
   testing will refine methodology"). That is the real the principal: a scientist
   who grades her own claims down. The slot exists so THAT voice fills the
   personal posts, not an agent's imitation of warmth.
5. Purge rule: when agent-invented interiority is found in any personal
   draft, archive the draft and rebuild from the verified record. Do not
   patch the lie in place.

### TSC / academic announcement posts (learned 2026-08-03)

When writing a conference acceptance, research announcement, or academic
milestone post for the principal's personal LinkedIn:

**Terminology locks (binding, triple-adversarial-cleared):**
- Say "present my research" — NEVER "poster," "poster number," or "775"
- the operator agent is **software**, not a living organism. "An architecture that adopts the organizational structure of a biological body, not just a brain."
- Use **"engines"** not "agents" — these are full systems, not task workers
- Use **"architecture"** not "operating system" — OS implies kernel/syscall semantics
- **"More than a multi-agent framework"** not "Not a multi-agent framework" — the operator agent IS multi-agent; denying it is technically false
- **"structured to mirror the systemic role"** not "running operational principles" — implies functional equivalence
- Never use **"substrate"** — loaded in consciousness science (physical substrate of consciousness / NCC)
- Never use **"genuinely"** — AI tell that performs sincerity

**Consciousness claim discipline (triple-adversarial-cleared):**
- Self-regulation and adaptive response are NOT consciousness indicators. They come from physiology/immunology.
- Integration and differentiation ARE from consciousness theory (IIT/GWT).
- Never list all four as "indicators consciousness science has been developing."
- Correct framing: "Integration and differentiation come from consciousness theory. Self-regulation and adaptive response come from the rest of biology."
- Never claim the operator agent is a "substrate to test consciousness theories against" — it is "a system where those properties can be measured together, on some thing you can actually instrument."

**Medical/clinical claim discipline:**
- NEVER list "drug interactions" — zero pharmacological basis, screengrabbable, devastating if quoted
- "Cascade failures in complex systems" not "in the body" — it is software, not biological cascade
- Always add: "Not in patients, not yet, and maybe not ever."
- "Built on biological coordination principles" not "models how biological systems coordinate"

**Narrative discipline:**
- NO fabricated origin stories. No "two years ago I was building AI like everyone else." No assumed timelines.
- Excitement must be grounded in facts: what was built, what was accepted, what is coming.
- Conversational over academic density for LinkedIn (drop the 0.80 number, say "real and measured")

**CTA + hashtags:**
- NO "bring your hardest objection" — rejected by user. Clean CTA only: "my inbox is open."
- Hashtags must have actual search volume. No niche academic tags (#Falsifiability = zero reach).
- Use high-volume: #AI #ArtificialIntelligence #Innovation #Tech #MachineLearning #Neuroscience #Future #Science #Research #Startup #EmergingTech #AIArchitecture #Biotech #Computing #TechCommunity

**Adversarial review workflow for science posts:**
- Run a minimum of 2 adversarial passes via `delegate_task` with the specialist engine panel
- Include consciousness scientist, medical/research scientist, and Popper falsification auditor seats
- Apply ALL fixes before presenting to user
- The ai-tell-removal-gate scanner catches "reach out" and "genuinely" — run it every time

**Graphic pairing:**
- HTML/CSS rendering is minimum quality bar (Pillow rejected 6x)
- Golden ratio / Da Vinci composition required
- Quote cards that just display text are rejected — graphics must COMMUNICATE
- Render final HTML to PNG via Chrome headless for upload: `--headless --screenshot --window-size=1920,1080 --force-device-scale-factor=2`

## Posting Tool Reference

- **xurl** (installed, official X platform CLI): posting, search, media upload, DMs. Auth via OAuth 2.0 PKCE. See `xurl` skill for full command reference.
- **x-cli** (NOT installed): older alternative wrapped by `xitter` skill. Do not use.
- **Always verify auth status first** with `xurl auth status` before attempting any write operations.

## Support Files
- **`references/verified-founder-corpus-map.md`** — The disk-verified map of the principal's real work record (8D foundation, TSC abstract, organism, the OS OS, naming, honesty system, scale) plus the STRUCK list (autonomic layer, fabricated lag claims) and the principal voice-slot question bank. Read BEFORE drafting any personal post. (2026-08-16)

- **`references/batch-template.md`** — Template for generating a content batch with post types, cadence, and image concepts
- **`references/post-type-catalog.md`** — Full catalog of post types with examples, hooks, and pairing guidance
- **`references/physiomorphic-founding-lab-launch.md`** — Locked Physiomorphic AI founding claims, same-day launch, LinkedIn About pattern, mixed-audience field intro + AIEO split + image noodles (2026-08-02)
- **`references/physiomorphic-linkedin-pair-and-audience.md`** — DS+personal repost pair, the principal voice lock, adaptive methodology, field-implications checklist, grammar gate beyond scanner (2026-08-02)
- **`references/physiomorphic-newsletter-program.md`** — Locked editorial architecture for the two-newsletter LinkedIn program: segment structure, skeletons, division-of-labor table, six-issue arcs, sibling-line choreography, newsletter voice pitfalls (2026-08-16)
- **`references/tsc-announcement-adversarial-protocol.md`** — 5-seat adversarial review protocol for science/conference announcement posts. Terminology locks, consciousness/medical claim traps, z.ai 429 retry rule. (2026-08-03)
- **`references/html-graphic-production-pipeline.md`** — HTML/CSS-to-PNG social graphic production via Chrome headless. Design corrections, user feedback patterns, crop discipline, golden ratio composition. (2026-08-03)

## Related Skills

- **`social-profile-optimization`** — Profile revamps (bio, headline, about). Run profile revamp and content generation together for a full social media overhaul.
- **`xurl`** — X/Twitter API CLI for posting, search, and media. Required for automated posting.
- **`external-content-qa-pipeline`** — QA review for all external-facing content. Run on every content batch before delivery.
