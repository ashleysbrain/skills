# Texas Family Court Legal Document Formatting

## When to use
When rebuilding ANY legal document for Texas family court from scratch (pro se filings, memoranda, affidavits, character statements, motions).

## Source
Lesson from 2026-07-26 session: User asked for surgical edits to a legal memorandum. PyMuPDF redaction produced mismatched font sizes. User said: "the text is like in four point font when the rest of it's in eight nine. It looks ridiculous." Then asked for an editable Word doc that "must reflect as such and be formatted by the best in the world."

## Required formatting (python-docx)

### Fonts
- Body: Times New Roman 12pt (STANDARD for Texas courts)
- Court caption: Times New Roman 12pt bold
- Section headings: Times New Roman 12pt bold, underlined, CENTERED
- Subsection headings: Times New Roman 12pt bold

### Spacing
- Body paragraphs: DOUBLE-SPACED (line_spacing = 2.0)
- First line indent: 0.5 inches
- Section headings: 18pt before, 12pt after
- Subsection headings: 12pt before, 6pt after

### Court caption block (top of document)
```
Cause No. [NUMBER]
IN THE MATTER OF THE MARRIAGE OF
[PETITIONER NAME]
AND
[RESPONDENT NAME]

IN THE [NUMBER]TH JUDICIAL DISTRICT COURT
[COUNTY] COUNTY, TEXAS

[horizontal line]
```

### Section numbering
- Roman numerals for main sections: I, II, III, IV...
- Letters for subsections: A, B, C...
- Numbers for items within: 1, 2, 3...

### Signature block (REPRESENTED BY COUNSEL)
```
Respectfully submitted,

/s/ [Counsel Name]
[Counsel Name]
State Bar No. [______]
Attorney for Respondent
the principal Dwight Gilchrist
27125 Pyeatt Lane
Oak Ridge North, Texas 77385
```

### Signature block (PRO SE)
```
Respectfully submitted,

/s/ [Name]
[Full Name]
[Role, e.g., Respondent, Pro Se]
[Address]
[City, State ZIP]
```

**CRITICAL:** Confirm representation status before choosing which block to use. A document signed "Pro Se" when the party is represented by counsel is a material misrepresentation to the tribunal.

### Certificate of Service
Required at the end of every filed document:
```
CERTIFICATE OF SERVICE
I certify that a true and correct copy of this instrument was served on
opposing counsel on this the _____ day of _____________, 2026, via
electronic filing and/or hand delivery.
```

## Page margins
- 1 inch all sides (top, bottom, left, right)

## AI telltale removal (MANDATORY)
- No em-dashes. Use regular hyphens or restructure sentences.
- No en-dashes in narrative text.
- No "furthermore," "moreover," "additionally" (AI favorites).
- Legal documents must sound like a lawyer wrote them, not an AI.
- Run ai-tell-removal-gate scan before delivery.

## Court-specific knowledge
- Montgomery County 410th Judicial District: standard Texas family court formatting
- Pro se filings: same formatting requirements as attorney filings
- Temporary orders hearings: judge reads the document before oral argument. First impressions matter.
