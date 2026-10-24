---
name: resume-and-career-applications
description: Class-level skill for resume writing, cover letters, and job applications with 100% factual accuracy, Da Vinci formatting, and source-document verification
category: productivity
version: 1.0.0
---

# Resume and Career Applications

Class-level umbrella for resume writing, cover letters, and job application document generation. Enforces 100% factual accuracy, Da Vinci formatting, and source-document verification before any output.

## When to Use

- User asks for resume updates or tailoring for a specific role
- User needs cover letter or application materials generated
- User asks for LinkedIn profile updates for job applications
- User requests portfolio case studies or professional artifacts

## CRITICAL PITFALLS (User Corrections)

### Pitfall 1: Never Make Up Facts

The most common failure mode — and one the user has corrected multiple times — is generating resumes or application materials with invented dates, titles, or achievements. This violates the user's trust and wastes time.

**MANDATORY workflow:**

1. **Locate the source of truth** — ALWAYS use the user's actual resume, not memory or assumptions:
   - Check document cache: `<agent-home>/document_cache/` for cached resume files
   - Search workspace: `find /<workspace> /<workspace> -name "*resume*" -o -name "*cv*"`
   - Ask user for correct document if not found

2. **Verify every fact** before including it:
   - Job titles (exact, no embellishments)
   - Dates (start/end, verify "Present" is accurate)
   - Company names (exact spelling)
   - Achievements (must be in source document)

3. **Ask, don't assume** for missing facts:
   - If dates are missing, ask user — don't invent
   - If titles are unclear, ask for clarification
   - If achievements are vague, ask for specifics

4. **Never create new facts** that aren't in the source:
   - No invented awards, certifications, or recognitions
   - No exaggerated achievements or metrics
   - No implied roles that weren't actual titles

**Examples of failures to avoid:**
- ❌ "Applied for NIH R21 grant" — not in source document
- ❌ "VMware: 3/2016 – Present" — user corrected: ended 2018
- ❌ "San Francisco Bay Area" — user corrected: Houston, TX
- ❌ "TWC wellness coherence sport" — user corrected: SCORE
- ❌ "Neuromatch Summer School" — user corrected: Neuromonster conference in Rome

### Pitfall 2: NO DASHES — "Looks too AI"

User strongly corrected: "No I don't want any dashes… it looks too ai"

**Mandatory formatting rules:**
- ❌ NO hyphens or en dashes in sentences (e.g., "human-AI" → "human AI")
- ❌ NO em dashes for emphasis (use periods instead)
- ✅ Dashes ONLY in phone numbers (e.g., 346-796-3708)
- ✅ Spaces instead of dashes for compound words
- ✅ "to" instead of em dashes for date ranges (e.g., "March 2016 to 2018")

**Pattern:** Always search the HTML/Python generator for dashes before rendering PDF.

### Pitfall 3: Technological Language, Not Biological

User corrected: "don't use the body is a more biological isomorphism. Use the technological analogs in this instead of the body parts."

**MUST use technological language for AI systems:**

| Biological Isomorphism (WRONG) | Technological Analog (CORRECT) |
|-------------------------------|--------------------------------|
| Organism | Multi-agent system / Collaborative AI system |
| Engines | Agents / Specialized agents |
| Thalamocortical routing | Context-aware dispatch / Intelligent routing |
| Physics-informed quality gates | Predictive quality control frameworks |
| Organism brain | Central coordination system / Coordination layer |
| Creative engines | Specialized generation systems |
| Taste | Excellence / Quality standards |

### Pitfall 4: Incorrect Timeline Claims

User corrected: "I have only been working and researching ai since 2023. Change my 8+ years statement"

**Correct timeline pattern:**
- "8+ years experience in enterprise systems design. Since 2023, focused on AI system design including..."

**Pattern:** Always separate total career timeline from AI-specific timeline.

### Pitfall 5: Missing Role-Specific Terminology

User corrected for OpenAI roles: "I need you to mention harnesses" and "The role description says nothing about evaluation harnesses"

**CRITICAL:** Always verify what the role description actually says. Do NOT assume terminology.

**Role-specific terminology to use:**

**OpenAI Model Designer:**
- "evaluation harnesses", "quality control frameworks", "observability"
- "context-aware routing", "behavioral constraint frameworks"

**OpenAI Researcher, Agent Post-Training, Personality:**
- "evals" (NOT "evaluation harnesses")
- "training data"
- "reward signals"
- "model improvements"
- "thoughtful, clear, perceptive, appropriately proactive, genuinely easy to work with"
- "agent personality"
- "post-training alignment"
- "exceptional collaborators"
- "layered agent systems" (WITHOUT revealing organism architecture)

**General AI roles:**
- "harnesses", "evaluation", "alignment", "trust"
- "collaboration patterns"
- "rigorous methodology", "peer review", "data-driven"
- "frameworks", "systems", "architecture"

**Pattern:** Always analyze job description and use its exact terminology.

## Source Document Extraction

When the user sends resume or cover letter files via Telegram or upload:

1. **Document cache is canonical** — files auto-save to `<agent-home>/document_cache/`
2. **Extract with read_file** — supports .docx, .pdf, .txt
3. **Parse structure** — identify sections: header, summary, experience, education, skills
4. **Verify each line** — cross-check against source to avoid transcription errors

**Pattern:**
```python
# Find cached resume
search_files(target='files', pattern='*resume*', path='<agent-home>/document_cache')

# Extract content
read_file(path='/<workspace> Williams - Resume.docx')
```

## Da Vinci Formatting Preferences

User prefers Da Vinci creative formatting for professional documents:

**Theme:**
- Yellow accent color (`#f7b731`) — NOT green covers
- Serif + sans-serif font pairing (Crimson Pro + Inter or Merriweather + Roboto)
- Clean, professional aesthetic with subtle branding

**CRITICAL: NO DASHES Rule**

User strongly corrected: "No I don't want any dashes… it looks too ai"

**Mandatory formatting rules:**
- ❌ NO hyphens or en dashes in sentences (e.g., "human-AI" → "human AI")
- ❌ NO em dashes for emphasis (use periods instead)
- ✅ Dashes ONLY in phone numbers (e.g., 346-796-3708)
- ✅ Spaces instead of dashes for compound words
- ✅ "to" instead of em dashes for date ranges (e.g., "March 2016 to 2018")

**Examples:**
- ❌ "Multi-Agent System Architect" → ✅ "Multi Agent System Architect"
- ❌ "decision-making" → ✅ "decision making"
- ❌ "We figured it out — this system" → ✅ "We figured it out. This system"
- ❌ "human-AI interaction" → ✅ "human AI interaction"

**When user says "Da Vinci process":**
1. Use Python data-driven HTML generator → WeasyPrint pipeline
2. Inline CSS styling (not external stylesheets)
3. Landscape for dense content, portrait for standard resumes
4. Print-friendly `-PRINT.pdf` auto-generated
5. Merriweather (headings) + Roboto (body) font pairing

**See:** `ds-fleet-atlas-update-via-davinci` skill for full Da Vinci pipeline details

## Language Style: Technological, Not Biological

User corrected: "don't use the body is a more biological isomorphism. Use the technological analogs in this instead of the body parts."

**MUST use technological language for AI systems:**

| Biological Isomorphism (WRONG) | Technological Analog (CORRECT) |
|-------------------------------|--------------------------------|
| Organism | Multi-agent system / Collaborative AI system |
| Engines | Agents / Specialized agents |
| Thalamocortical routing | Context-aware dispatch / Intelligent routing |
| Physics-informed quality gates | Predictive quality control frameworks |
| Organism brain | Central coordination system / Coordination layer |
| Creative engines | Specialized generation systems |
| Taste | Excellence / Quality standards |

**Why:** User does not want to reveal the biological inspiration behind the system design. Documents must speak in pure technical terms to avoid "AI-tell" signals.

**Pattern:** Always search the HTML/Python generator for biological terms and replace before rendering PDF.

## Tailoring for Specific Roles

When tailoring a resume for a specific job posting:

1. **Analyze the job description** first:
   - Extract key responsibilities and requirements
   - Identify must-have vs nice-to-have skills
   - Note specific keywords for ATS matching

2. **Map experience to requirements**:
   - Find source document entries that match
   - Prioritize relevant experience (chronological or functional)
   - Add role-specific achievements from source

3. **Emphasize relevant skills**:
   - Pull from source, don't invent
   - Quantify when source provides metrics
   - Use exact terminology from job description

4. **Address gaps honestly**:
   - If source lacks something, don't invent it
   - Ask user if they have relevant experience not in source
   - Frame gaps as opportunities to discuss in interview

5. **Use role-specific terminology**:
   - For AI roles: "harnesses", "evaluation", "alignment", "collaboration"
   - For engineering roles: "frameworks", "systems", "architecture"
   - For research roles: "methodology", "data-driven", "peer review"
   - Match job description language exactly

6. **Clarify AI vs non-AI timeline**:
   - User's pattern: "8+ years experience in X. Since 2023, focused on AI Y"
   - Don't claim AI experience before actual AI work (2023+)
   - Be specific about when AI work began

**OpenAI Model Designer example:**
- Source has 50+ engine AI organism → emphasize model behavior design
- Source has Workday HCM experience → tie to human-AI interaction
- Source has TWC wellness coherence score → link to research-driven design
- Emphasize: "evaluation harnesses", "quality control frameworks", "observability"

**OpenAI Researcher, Agent Post-Training, Personality example:**
- Source has 50+ agent collaborative system → emphasize "exceptional collaborators"
- Source has behavioral constraint frameworks → emphasize "post-training alignment"
- Source has TWC wellness coherence score → demonstrate "rigorous evaluation methodology"
- Emphasize: "agent personality", "collaboration patterns", "evaluation harnesses", "trust"

## Terminology Accuracy

User has corrected specific terminology:

| Wrong | Correct | Context |
|-------|---------|---------|
| TWC wellness coherence sport | TWC wellness coherence SCORE | Health metric |
| Neuromatch Summer School | Neuromonster conference | Rome, June 2026 |
| San Francisco Bay Area | Houston, TX | User location |
| VMware: 3/2016 – Present | VMware: 3/2016 – 2018 | Employment dates |
| NIH grant application | None (not in source) | Avoid invention |
| Biological isomorphisms (organism, engines, brain) | Technological analogs (multi-agent systems, agents, coordination layer) | AI system description |
| "8+ years AI experience" | "8+ years enterprise systems. Since 2023, focused on AI" | Timeline accuracy |
| Phone: 346-796-3708 | Phone: 346-796-3708 (corrected 2026-07-01) | Contact information |

## Cover Letter Writing

Cover letters must be 100% consistent with resume facts:

1. **Start from resume source** — use same job titles, dates, companies
2. **Tell the narrative** — connect experience to role requirements
3. **Avoid hype** — no "passionate," "excited" without source evidence
4. **Specific examples** — pull from source achievements
5. **Address the company** — research their actual mission and products

**CRITICAL formatting rule:** Cover letters use regular paragraphs ONLY — NO bullet points. User corrected: "regular paragraphs (NO bullet points)"

**CRITICAL pronoun rule:** Use "I" not "we". User corrected: "change 'we', and, um, delete the how and, and just describe it"

**Pattern:**
- Opening: Why this role (from job description analysis)
- Body paragraphs: 2-3 source-backed achievements relevant to role (regular paragraphs, no bullets)
- Closing: What user brings (from source) + call to action

**OpenAI Agent Post-Training Personality cover letter emphasis:**
- "layered agent systems" (WITHOUT revealing organism architecture)
- "thoughtful, clear, perceptive, appropriately proactive, genuinely easy to work with"
- "evals, training data, reward signals, model improvements"
- "exceptional collaborators"

## Verification Checklist

Before delivering ANY resume or cover letter:

**Facts & Content:**
- [ ] Source document located and extracted
- [ ] Every job title verified against source
- [ ] Every date verified (start/end, no false "Present")
- [ ] Every achievement exists in source document
- [ ] Location correct (Houston, TX, not San Francisco)
- [ ] Timeline clear: "8+ years X. Since 2023, focused on AI Y" pattern
- [ ] No invented facts, awards, or recognitions
- [ ] Consistent with user's actual employment timeline
- [ ] Phone number correct (346-796-3708)

**Terminology:**
- [ ] TWC wellness coherence SCORE (not sport)
- [ ] Neuromonster conference in Rome, June 2026 (not Neuromatch Summer School)
- [ ] No biological isomorphisms (organism, engines, brain, etc.)
- [ ] Technological analogs used instead (multi-agent systems, agents, coordination layer)
- [ ] Role-specific terminology matches job description
- [ ] For OpenAI Agent Post-Training Personality: "evals, training data, reward signals, model improvements" (NOT "evaluation harnesses")
- [ ] For agent collaboration roles: "exceptional collaborators", "layered agent systems"

**Formatting:**
- [ ] NO dashes in sentences (hyphens, en dashes, em dashes)
- [ ] Spaces instead of dashes for compound words
- [ ] "to" instead of dashes for date ranges
- [ ] Dashes ONLY in phone number
- [ ] Yellow accent color (#f7b731), NOT green
- [ ] Merriweather + Roboto font pairing
- [ ] Compact, not verbose

**Cover Letter Specific:**
- [ ] Regular paragraphs ONLY (NO bullet points)
- [ ] "I" not "we" throughout
- [ ] No "how we do it" descriptions - focus on results

**Role-Specific:**
- [ ] "harnesses" mentioned for AI post-training roles
- [ ] "evaluation" terminology for research roles
- [ ] "collaboration" emphasis for agent roles
- [ ] Job description keywords included
- [ ] Achievements mapped to job requirements

## Workflow

### Step 1: Locate Source Document
```bash
# Check document cache
ls -lt <agent-home>/document_cache/*.docx

# Search workspace
find /<workspace> /<workspace> -name "*resume*" -o -name "*the principal*"
```

### Step 2: Extract and Parse
```python
# Read source
read_file(path='/path/to/resume.docx')

# Parse sections into structured data
header = parse_header(content)
experience = parse_experience(content)
education = parse_education(content)
skills = parse_skills(content)
```

### Step 3: Verify Facts
```python
# Ask user for missing/unclear facts
clarify(question="What are correct dates for X job?")

# Cross-check against source
assert all_dates_exist_in_source()
assert all_titles_match_source()
```

### Step 4: Tailor (if specific role)
```python
# Analyze job description
job_reqs = extract_requirements(job_posting)

# Map source experience to requirements
relevant_experience = filter_by_relevance(experience, job_reqs)

# Generate tailored content
tailored_resume = format_resume(relevant_experience)
```

### Step 5: Format and Generate
```python
# Use Da Vinci pipeline
generate_html(resume_data)
render_pdf_via_weasyprint(html_file)
```

### Step 6: Deliver
```python
# Open for review
open('the principal-Williams-Resume.pdf')

# Or send via Telegram
send_telegram_media(file='the principal-Williams-Resume.pdf')
```

## References

- `ds-fleet-atlas-update-via-davinci` — Full Da Vinci formatting pipeline
- `telegram-artifact-delivery` — Sending documents via Telegram
- `print-friendly-pdf-ocg` — Dual print/screen PDF generation

## Related Skills

- `powerpoint` — When user requests slide-based resume or presentation
- `nano-pdf` — For minor PDF edits (typos, titles)
- `telegram-pdf-bundle-delivery` — Multi-document application packages