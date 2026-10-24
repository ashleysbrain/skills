---
name: da Vinci-style-resume-cover-letter
description: Generate professional resume and cover letter PDFs using Da Vinci yellow theme styling (Merriweather/Roboto fonts, compact formatting, technological language). Focus on AI system architecture roles (OpenAI Model Designer, multi-agent systems).
tags: [documents, pdf, resume, cover-letter, job-application, weasyprint, productivity]
version: 1.0.0
---

# Da Vinci-Style Resume & Cover Letter Generation

Use this when the user needs a professional resume and cover letter for AI system architecture roles, particularly OpenAI Model Designer or multi-agent system positions. This skill applies Da Vinci creative production styling (yellow theme) with compact, professional formatting.

## When to use

- User needs a resume and cover letter for OpenAI Model Designer role
- User needs AI system architecture job application materials
- User wants Da Vinci yellow theme styling (not green cover)
- User needs compact formatting to keep documents to 1-2 pages each

## Core workflow

1. **Gather 100% accurate facts**
   - Get correct dates for all work experience (user corrections are authoritative)
   - Get correct phone number (don't guess, ask user)
   - Get correct location (user is Houston, TX, not San Francisco)
   - Get correct certifications, conferences, research
   - NEVER claim skills user doesn't have (e.g., Python if they use AI tools instead)

2. **Apply Da Vinci yellow theme styling**
   - Font: Merriweather (headings) + Roboto (body) — NOT Crimson Pro/Inter
   - Accent color: #f7b731 (yellow/gold)
   - Body background: #faf9f5 (light cream)
   - Highlight boxes: #fef9e7 background with #f7b731 left border
   - Compact formatting: 9pt font size, 1.3 line-height, narrow margins (0.35in)
   - Portrait A4 or letter size

3. **Use technological analogs (NOT biological isomorphisms)**
   - Organism → Multi-agent system / Collaborative AI system
   - Engines → Agents / Specialized agents
   - Thalamocortical routing → Context-aware dispatch / Intelligent routing
   - Physics-informed quality gates → Predictive quality control frameworks
   - Organism brain → Central coordination system / Coordination layer
   - Creative engines → Specialized generation systems
   - Taste → Excellence / Quality standards

4. **Content structure**

   **Resume:**
   - Header: name, email, phone, LinkedIn, location
   - Summary: 2-3 sentences highlighting multi-agent system architecture and research recognition
   - Experience: chronological, most recent first, with dates
   - Education: degrees with dates
   - Skills: grouped by category, use AI tools language not direct coding skills

   **Cover letter:**
   - Header: name, email, phone, LinkedIn, location, date
   - Recipient: "To the OpenAI Model Designer Hiring Team"
   - Salutation: "Dear Hiring Team,"
   - Quote from job description to frame the conversation
   - Body: how agents work together, how system was built, research recognition
   - Closing: "Sincerely," + signature

5. **Render with WeasyPrint**
   - Use Python HTML→PDF rendering with WeasyPrint
   - Verify page count (target: 1-2 pages per document)
   - Open PDFs for user review
   - Regenerate based on user feedback

## Critical pitfalls (user-corrected issues)

### Font preferences
- **WRONG:** Crimson Pro/Inter (user rejected this)
- **RIGHT:** Merriweather (headings) + Roboto (body)

### Page count
- **WRONG:** 5 pages (user said "way too many pages here shouldn't be five pages")
- **RIGHT:** 1-2 pages (compact formatting: 9pt font, 1.3 line-height, narrow margins)

### Line spacing
- **WRONG:** Wide line spacing (user said "too far apart")
- **RIGHT:** Tight line-height (1.3 for resume, 1.6 for cover letter)

### Margins
- **WRONG:** 0.75in margins on cover letter (user said "too narrow, widen those margins")
- **RIGHT:** 0.6in margins for cover letter, 0.35in for resume

### Skills claims
- **WRONG:** "Python, FastAPI, API integration" when user doesn't know Python
- **RIGHT:** "AI-powered development environment, Microsoft Office/Excel, Smartsheets, JIRA"
- **CRITICAL:** User said "I don't know Python. I don't know these things. They are through AI that I use most of those tools."

### Terminology
- **WRONG:** "Organism, engines, thalamocortical routing, physics-informed quality gates, taste"
- **RIGHT:** "Multi-agent system, agents, context-aware dispatch, predictive quality control frameworks, excellence"
- **CRITICAL:** User said "use the technological analog for that, right? So don't use the body is a more biological isomorphism. Use the technological analogs"

### Date formats
- **WRONG:** En dash (–) that renders as "forged andight" in some PDF readers
- **RIGHT:** "to" (e.g., "March 2016 to 2018")

### Research/conference claims
- **WRONG:** "Neuromatch Summer School" (doesn't exist)
- **RIGHT:** "Neuromonster conference (Rome, June 2026) — invited to present TWC wellness coherence score"
- **CRITICAL:** User corrected "Neuromonster was a conference in Rome that I got invited to speak to, that I didn't, but it was in June of 2026"

### Wellness score
- **WRONG:** "TWC wellness coherence sport"
- **RIGHT:** "TWC wellness coherence SCORE"
- **CRITICAL:** User corrected "you know that it's not sport, you know that it is score"

### Job end dates
- **WRONG:** "Present" when user is no longer at the job
- **RIGHT:** Actual end year (e.g., VMware: "March 2016 – 2018")
- **CRITICAL:** User corrected "I ended VMware in 2018"

### Cover letter emphasis
- **WRONG:** Generic praise without specific technical details
- **RIGHT:** Detailed explanation of "how the engines work together"
- **CRITICAL:** User said "we really speak to what I've built with all these engines and the way they work together. So, make sure that we play that up"

## Content emphasis guidelines

### "We figured it out" callout
User wants this called out explicitly in resume and cover letter. In highlight box:
> We figured it out — this system produces output with human-level quality.

### Creative workflow explanation
User wants more than just bullet points. Explain:
- How specialized agents collaborate
- How the coordination layer routes work
- How feedback loops improve quality over time
- How quality control frameworks enforce excellence at each stage

### Technical architecture emphasis
- Multi-agent system architecture (not just "built AI systems")
- Context-aware routing and dispatch
- Predictive quality control frameworks
- Observability and monitoring infrastructure
- Human-AI interaction paradigms

### Research recognition
- TWC wellness coherence score
- Neuromonster conference acceptance (Rome, June 2026)
- This demonstrates research methodology applied to human-AI interaction design

## HTML/CSS template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>the principal M. Williams - Resume</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700;900&family=Roboto:wght@400;500;700&display=swap');

        @page {
            size: letter;
            margin: 0.35in;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 9pt;
            line-height: 1.3;
            color: #1a1a1a;
            background: #faf9f5;
        }

        .container {
            max-width: 7.5in;
            margin: 0 auto;
            background: white;
        }

        .header {
            border-bottom: 2px solid #f7b731;
            padding-bottom: 0.25in;
            margin-bottom: 0.35in;
        }

        .name {
            font-family: 'Merriweather', Georgia, serif;
            font-size: 22pt;
            font-weight: 900;
            color: #1a1a1a;
            margin-bottom: 0.12in;
            letter-spacing: 0.3px;
        }

        .contact {
            font-size: 9pt;
            color: #555;
            margin-bottom: 0.03in;
            font-weight: 500;
        }

        .location {
            font-size: 9pt;
            color: #f7b731;
            font-weight: 700;
        }

        .summary {
            font-family: 'Merriweather', Georgia, serif;
            font-size: 10pt;
            line-height: 1.45;
            color: #333;
            margin-bottom: 0.35in;
            font-style: italic;
        }

        h1 {
            font-family: 'Merriweather', Georgia, serif;
            font-size: 11pt;
            font-weight: 700;
            color: #f7b731;
            border-bottom: 1px solid #e0e0e0;
            padding-bottom: 0.1in;
            margin-top: 0.45in;
            margin-bottom: 0.25in;
            letter-spacing: 0.8px;
            text-transform: uppercase;
        }

        .highlight-box {
            background: #fef9e7;
            border-left: 3px solid #f7b731;
            padding: 0.12in 0.2in;
            margin: 0.2in 0;
            font-size: 9pt;
            line-height: 1.35;
            color: #333;
        }

        @media print {
            body {
                background: white;
            }
        }
    </style>
</head>
<body>
    <!-- Content goes here -->
</body>
</html>
```

## Python rendering script

```python
from weasyprint import HTML

# Render resume
HTML('resume.html').write_pdf('the principal-Williams-Resume-OpenAI.pdf')

# Render cover letter
HTML('cover_letter.html').write_pdf('the principal-Williams-Cover-Letter-OpenAI.pdf')
```

## Verification checklist

- [ ] Page count is 1-2 pages per document (not 5+ pages)
- [ ] Font is Merriweather/Roboto (not Crimson Pro/Inter)
- [ ] Yellow theme used (#f7b731 accent, no green cover)
- [ ] Dates use "to" not en dash
- [ ] Phone number is correct (ask user, don't guess)
- [ ] Location is Houston, TX (not San Francisco)
- [ ] No biological isomorphisms (use technological analogs)
- [ ] Skills are accurate (AI tools, not Python user doesn't know)
- [ ] Research claims are accurate (Neuromonster, not Neuromatch)
- [ ] Wellness score is "score" not "sport"
- [ ] "We figured it out" callout included
- [ ] Cover letter explains how agents work together
- [ ] Margins are correct (0.35in resume, 0.6in cover letter)
- [ ] Open PDFs for user review

## Support files

- `references/openai-model-designer-role-analysis.md` — OpenAI Model Designer job requirements and how this resume addresses them
- `templates/resume-template.html` — Reusable HTML template with Da Vinci yellow theme styling
- `templates/cover-letter-template.html` — Reusable cover letter HTML template with Da Vinci styling

## User preferences (critical corrections)

**Font and formatting:**
- Merriweather/Roboto fonts (not Crimson Pro/Inter)
- Compact: 9pt font, 1.3 line-height, narrow margins
- Target: 1-2 pages per document (not 5+)

**Skills accuracy:**
- User doesn't know Python — use "AI-powered development environment"
- User uses AI tools for development, not direct coding
- Microsoft Office/Excel, Smartsheets, JIRA, ATS systems are user's tools

**Terminology:**
- Use technological analogs, not biological isomorphisms
- Don't reveal human body inspiration for system architecture
- "Multi-agent system" not "organism", "agents" not "engines"

**Facts accuracy:**
- Location: Houston, TX (not San Francisco)
- Phone: 346-796-3778 (don't guess)
- Neuromonster conference (Rome, June 2026), not Neuromatch
- TWC wellness coherence SCORE (not sport)
- VMware: March 2016 to 2018 (not Present)

**Content emphasis:**
- Explain how agents work together
- Call out "We figured it out"
- Emphasize multi-agent system architecture
- Include research recognition