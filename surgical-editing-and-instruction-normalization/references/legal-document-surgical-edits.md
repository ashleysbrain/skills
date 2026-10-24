# Legal Document Surgical Edits - Session Notes (2026-07-21)

## Context
Editing a Texas family court memorandum (Cause No. 26-05-07480, Montgomery County) for temporary possession of three dogs. User is the respondent's partner, not a party. The document goes to a judge.

## 7 Edit Types Applied

### 1. Factual reframing without admitting weakness
**Request:** Reword the Luna plane ticket section so the ticket IS the exchange for Luna's purchase, without calling attention to missing documentation.
**Pattern:** Replace "does not presently rely on" language with affirmative framing: "This travel booking corresponds to the same timeframe and reflects the parties' arrangement."
**Principle:** Never say "we lack proof." Say "the arrangement was X" and reserve the right to supplement.

### 2. Tense/ownership word changes
**Request:** Vet records are in Respondent's name but were changed after an incident. Do not call attention to the change.
**Pattern:** Remove "maintained" (implies long-term active stewardship that could be questioned). Use "in Respondent's name" (states current fact without history).
**Principle:** State the current fact. Do not describe how it got there.

### 3. AI telltale word replacement (varied)
**Request:** "Contemporaneous" appears 10+ times. Replace with different words in each instance.
**Pattern:** See SKILL.md pitfall on varied replacement. Used: documented, time-stamped, corresponding, dated, matching, concurrent, original, from that period, timely.
**Principle:** No single word repeated. Each instance gets context-appropriate variation.

### 4. Brief factual insertion
**Request:** Add petitioner's physical incapacity to the grooming section. Brief, not a new paragraph.
**Pattern:** Append to existing comma-separated list: "...as Petitioner's documented injuries and medical restrictions rendered her physically unable to perform these tasks."
**Principle:** Surgical insertion into existing sentence structure. No new paragraph needed.

### 5. Terminology strengthening
**Request:** Change neutral language to "witness coaching" instead of describing the behavior neutrally.
**Pattern:** "Petitioner sought a statement after supplying material facts" -> "Petitioner engaged in witness coaching, supplying material facts and the requested conclusion before obtaining..."
**Principle:** Use precise legal terminology that frames the behavior without overreach. "Witness coaching" is accurate. "Tampering" would be overreach (criminal connotation the user explicitly rejected).

### 6. Geographic scope expansion
**Request:** "Montgomery County" -> "Montgomery County and surrounding counties" in removal restrictions.
**Pattern:** Only change REMOVAL RESTRICTION mentions. Do not change court venue references (those must stay Montgomery County).
**Principle:** Distinguish between jurisdiction (venue, stays Montgomery County) and practical activity restrictions (can expand to surrounding counties for vet visits, dog parks).

### 7. AI telltale removal
**Request:** Remove all em dashes, en dashes, bullet characters that signal AI generation.
**Pattern:** `text.replace('\u2014', '-').replace('\u2013', '-').replace('\u25cf', '-')`
**Principle:** Court documents must look human-authored. No Unicode formatting artifacts.

## Advisory Review Separation Pattern
- Surgical edits go into the document file (saved to Desktop)
- Advisory review (trigger words, strategic recommendations, adversarial weaknesses) dispatched to separate delegation
- Review delivered via Telegram, NOT in the document
- User reviews recommendations before any further edits beyond surgical

## Smart Quote Handling
PDF-extracted text uses Unicode curly quotes. Search strings with straight quotes fail silently.
Always normalize quotes before search/replace on PDF-sourced text.

## Multi-Document Synergy Failures (2026-07-26)

### Merging separate sections during rebuild
When rebuilding a document with distinct subsections (e.g., per-dog acquisition evidence), do NOT merge them. If the original had three dogs as three separate acquisition subsections, the rebuild must also have three. Do not combine "Lulu Acquisition" with "Transport Context."

### Deleting content the panel did not recommend cutting
When applying 10-agent panel recommendations, you will accidentally drop content NO panel member said to remove. This is the #1 failure mode.

**Fix - mandatory pre/post audit:** Before rebuilding, extract every factual claim into a checklist. After rebuilding, diff the checklists. Every item in original but NOT in rebuild is either (a) intentionally cut per panel, or (b) accidentally lost. If (b), restore immediately.

**User correction (verbatim):** "This should have been done with surgical edits. There are things that were removed that should not have been removed."

### Producing one document when working a pair
When two documents must work synergistically (mastermind principle), do NOT finish one and deliver it before the other is done. The user said: "This shouldn't even be done. This should only be partially done."

Both documents must be rebuilt TOGETHER. Deliver BOTH simultaneously.

### Payment language reframing without user approval
The panel unanimously said to reframe "$7,500 paid under duress." But the user corrected: "delete the sentence that says he paid anything under duress for the dogs." Do NOT invent framing the user did not approve. ASK how payment should be handled.

### ADHD timeline deadlines
Never use 24-hour or 72-hour deadlines in court orders. Use "seven (7) days" or "reasonable time." The user said: "72 hours just doesn't leave room for error."

### Pattern evidence in wrong subsection
Pattern evidence (counseling for lying, relationship-wide behavior) must go in its own subsection, not merged into veterinary record restriction or other topical subsections.

### Text-message party admissions are NOT HIPAA
Text messages from a party voluntarily admitting something are party admissions under TRE 801(e)(2)(A), NOT medical records. Do NOT flag them as privilege landmines.

### Represented counsel signature blocks
Check whether party is PRO SE or REPRESENTED before building documents. If represented, signature blocks show counsel name + bar number, NOT "Pro Se."

## Session Notes (2026-08-01) - Panel-Driven Content Loss (3rd Violation)

### The hardest lesson: DO NOT REBUILD FROM SCRATCH AFTER A PANEL REVIEW

**User correction (verbatim):** "do surgical edits don't fucking rewrite shit"

The 10-agent elite legal panel (5 legal agents + 5 adversarial reviewers) produces recommendations. Those recommendations are EDITS, not a blueprint for a new document. The correct flow:

1. Keep the existing document
2. Apply each recommendation as a targeted patch
3. Run keyword audit
4. Deliver

The WRONG flow (what happened 3 times):
1. Read panel recommendations
2. Rebuild document from memory incorporating recommendations
3. Lose 10+ items nobody mentioned
4. User catches it

### Section structure preservation audit

Before and after any edit pass, verify section COUNT and structure matches:

```
ORIGINAL sections:    A, B, C (Lucky), D (Lulu+Transport), E (Objective)
REBUILT sections:     A, B, C (Luna), D (Lulu+Transport)    <- LOST: Lucky, merged D
CORRECT sections:     A, B, C (Luna), D (Lulu), E (Transport), F (Objective)
```

Each subsection in the original MUST map to a subsection in the output. Count them. If count drops, something was lost.

### Timeline deadline changes from this session

- 24 hours -> seven (7) days (user: "72 hours just doesn't leave room for error")
- Arbitrary 14-day windows -> "until the Court enters a transition or preservation order"
- Never use tight timelines that could cause a party with ADHD to lose possession due to a missed administrative deadline

### Specific factual corrections from this session

- Extortion escalated from $5K to $7.5K to $10K (not just $7.5K)
- Pool house: December 20-24 ONLY, not "month of December"
- "Paid for" -> "paid for or reimbursed for most every visit"
- "Dog" -> "animal" for prior pull incident (could have been squirrel/cat)
- "Always" -> "at times" (too strong a word)
- "After dark" -> "after Respondent left" (timing is what matters, not darkness)
- "Contacted police" -> "spoke with police" (mother didn't initiate contact)
- Add "allegedly" before all injury claims when truthfulness is uncertain

### Pregnancy claims: include but brief

Panel said cut pregnancy claims entirely (worst cost/benefit). User overruled: "we have to put it in because this is absolutely in the character." When panel recommendations conflict with user's explicit judgment, the user WINS. Panel recommendations are advisory, not commands.

### January 9, 2023 Michigan incident

Established the pattern of using dogs as leverage. Petitioner took dogs to Michigan, refused to return them unless Respondent took her back. This predates the 2025 events and must be included as pattern evidence. Also shows same wife/pregnancy claim pattern with a different woman (2023 vs 2025 with the principal).
