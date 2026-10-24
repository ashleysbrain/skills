# Document Cache Lookup Pattern

When user sends resume/cover letter via Telegram or mentions existing documents:

## Step 1: Check Document Cache
```bash
# List recent .docx files
ls -lt <agent-home>/document_cache/*.docx | head -10

# Search for the principal's documents
ls -lt <agent-home>/document_cache/ | grep -i "principal\|resume"
```

## Step 2: Extract Content
```python
read_file(path='/<workspace> Williams - Resume.docx')
```

## Step 3: Verify Before Using
- Check that dates match user's corrections
- Verify job titles are exact
- Confirm location (Houston, TX, not San Francisco)
- Ensure no invented facts

## Step 4: Cross-Check Corrections
User's factual corrections from career sessions:

| Fact | Correct Value | Source |
|------|---------------|--------|
| Location | Houston, TX | User correction |
| VMware end date | 2018 (not "Present") | User correction |
| Teleperformance | Compensation Analyst (5/2021 - 9/2023) | User timeline |
| Alliance One | Workday Admin (10/2022 - 9/2023) | User timeline |
| TWC metric | wellness coherence SCORE | User correction |
| Neuromonster | Conference in Rome (June 2026) | User correction |

## Step 5: Ask for Missing Info
If source lacks dates, titles, or achievements:

```python
clarify(question="What are the correct dates for your role at [Company]?")
```

## NEVER Invent Facts
- No awards/certifications not in source
- No job titles that weren't actual titles
- No dates or durations not explicitly stated
- No achievements without source backing

## Example from Session Failure
❌ Wrong: "Applied for NIH R21 neuroscience grant ($275K)"
✅ Right: "Developed TWC wellness coherence score for individual health assessment. Accepted to Neuromonster conference (Rome, June 2026) to present TWC wellness coherence score."

The NIH grant was invented — not in source document, not true.
The Neuromonster conference is documented and verified by user.