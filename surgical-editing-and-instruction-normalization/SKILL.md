---
name: surgical-editing-and-instruction-normalization
description: Normalize nonlinear user requests into the right execution order, preserve approved material, and make surgical edits instead of broad rewrites.
triggers:
  - The user asks for tweaks to an existing document, plan, artifact, or system design.
  - The request contains multiple corrections, constraints, and optional branches delivered out of order.
  - The user signals ADHD-style nonlinear instructions, context drift, overwritten edits, or frustration about rework.
  - The task requires preserving approved content while integrating new changes.
---

# Surgical Editing and Instruction Normalization

## Purpose

Use this skill when the user gives corrections, additions, or multi-part requests that should *not* be executed literally in the order spoken. The goal is to convert a messy or nonlinear input stream into the optimal execution sequence, preserve approved work, and patch artifacts with minimal surface area.

## Core operating rules

1. **Patch before rewrite.** Default to the smallest viable change that satisfies the ask.
2. **Normalize before acting.** Reorder the user's points into dependency order before editing.
3. **Preserve approved material.** Treat previously accepted wording, structure, and locked variants as constraints.
4. **Separate request classes.** Distinguish:
   - core objective
   - hard constraints
   - corrections to existing text
   - optional improvements
   - future work / branches
5. **Do not let later edits clobber earlier approved changes.** Re-read the current artifact state mentally or via tools before applying subsequent changes.
6. **Treat user corrections as process constraints.** If the user says “don’t redo the whole thing” or “reorder this intelligently,” that is a governing workflow rule for the task class, not a one-off complaint.

## Workflow

### 1) Parse the incoming request into buckets
Before editing, sort the request into:
- **Objective:** what outcome the user wants
- **Protected state:** what is already approved/locked/canonical
- **Required edits:** exact changes that must happen now
- **Ordering dependencies:** what must happen first to avoid overwrite/rework
- **Open questions:** only genuine blockers

### 2) Build the execution order silently
Do **not** mirror the user's spoken order when it is suboptimal. Prefer this order:
1. identify canonical artifact
2. identify locked sections / preserved approvals
3. apply structural or naming changes first
4. apply localized content patches
5. add new sections only after existing sections are stable
6. run a final pass for contradictions, duplicate language, and overwritten edits

### 3) Edit surgically
When editing documents, plans, or agent definitions:
- change the minimum necessary lines
- preserve surrounding validated material
- avoid tone/style drift unless requested
- do not regenerate full documents for single-section tweaks
- if a rewrite is truly required, state that explicitly and why

4. **Maintain continuity across multi-step revisions**
When the task spans many turns:
- keep a running ledger of locked choices, approved variants, and unresolved items
- treat that ledger as part of the artifact state
- on each new tweak, check whether it modifies, supersedes, or complements prior approvals
- if the user asks to "tweak one thing," explicitly constrain the edit scope to that delta unless they asked for a broader rebuild

### 5) Create a micro-brief before editing
Before making the next patch, mentally or explicitly restate:
- what artifact is canonical right now
- what `<agent-home>/.session-state.json` says the active artifact is
- what must remain untouched
- what single delta is being applied now
- what edit order prevents overwrite

If that micro-brief implies broad regeneration for a narrow tweak, stop and reduce the scope.

### 6) Verify before presenting
Confirm:
- only the requested scope changed
- approved material remained intact
- no prior accepted edits were overwritten
- the final structure reflects dependency order, not raw intake order
- the response distinguishes audit/planning from implementation when the user asked for phased work

## Pitfalls

### Pitfall: Executing in literal spoken order
Users with ADHD or rapid nonlinear thought may provide valid instructions in a poor implementation order. Literal execution causes clobbered edits and circular work.

**Fix:** Reconstruct the optimal sequence before touching the artifact.

### Pitfall: Treating a tweak as a rewrite request
A small correction does not authorize a full regeneration.

**Fix:** Default to localized patches and preserve the existing artifact.

### Pitfall: Block replacement clobbers adjacent code (2026-07-17, USER CORRECTION)
The user said: "you are not doing surgical edits. you deleted the stem cell bank details. you cannot break the things you are working on."

When porting a feature between parallel files that have diverged over many sessions (e.g., two copies of an 18,000-line HTML file), a blunt block replacement of 300+ lines CLOBBERS adjacent functions that exist only in the target file. The replacement boundary silently swallows code that was never in the source.

**Fix — mandatory pre-replacement function diff:**
```bash
comm -23 \
  <(grep '^function ' file_TARGET | sed 's/function \([a-zA-Z0-9_]*\).*/\1/' | sort -u) \
  <(grep '^function ' file_SOURCE | sed 's/function \([a-zA-Z0-9_]*\).*/\1/' | sort -u)
```
This reveals functions in the TARGET that do NOT exist in the SOURCE — they are at risk. If the replacement boundary overlaps any, abort the block swap. Use narrow `patch` calls on individual functions instead.

**After ALL patches**, re-run the diff to confirm zero functions were lost. This is the surgical edit contract: you touch only the named function, you verify nothing adjacent was destroyed.

**Layered syntax error exposure (2026-07-17):** Fixing or replacing a block can also EXPOSE pre-existing syntax errors that were previously masked by an earlier error in the same script block. Example: replacing `renderPsychTab` fixed the first parse error, which REVEALED a latent `l'Étude` unescaped apostrophe further down the same block, which in turn REVEALED a malformed `the specialist engine` entry spliced into the wrong data structure. The user saw "stem cell bank details deleted" — the code was never touched, the entire script block just couldn't parse. After ANY edit to a large script block, run `node --check` iteratively until ALL parse errors are resolved. "Function not defined" on a 17K-line file = dead script block from a parse error, NOT deleted code.

### Pitfall: Array reorder silently corrupts index-based references (2026-07-17)
When you reorder an array (e.g., organism nodes in a network diagram), any code that references array elements by numeric index (`from:0, to:3`) silently points to the wrong entity. The code runs without error but every downstream consumer (link rendering, labels, arrows) connects to the wrong targets.

This is the same class of bug as block replacement clobbering adjacent code: a structural change that appears to work but silently corrupts data integrity.

**Fix**: When reordering any array that is referenced by index elsewhere, search ALL consumers of that array for numeric indices and either (a) update them, or (b) refactor to string-key lookups. After the change, verify programmatically (extract rendered labels from DOM, check each connection target) rather than trusting visual inspection.

### Pitfall: Losing approved state between iterations
If the agent does not explicitly preserve what is already approved, later passes may overwrite it.

**Fix:** Keep a locked-state ledger and check against it before every major edit.

### Pitfall: Smart-quote matching failures in search/replace (2026-07-21)
When editing text extracted from PDFs (`pdftotext`), the text contains Unicode smart/curly quotes (`\u2019` right single, `\u201c` left double, `\u201d` right double). Search strings written with straight quotes (`'` `"`) will NOT match. This causes silent edit failures where the agent thinks the replacement applied but it did not.

**Symptom:** The edit reports "APPLIED" or "NOT FOUND" inconsistently. Verification grep shows the old text still present.

**Fix — mandatory quote normalization before search/replace:**
```python
# Strategy 1: Try both quote styles
old_straight = "Respondent's name"
old_smart = old_straight.replace("'", "\u2019").replace('"', '\u201c')
text = text.replace(old_smart, new) or text.replace(old_straight, new)

# Strategy 2: Normalize the whole text to straight quotes first, then edit
text = text.replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
```

After ALL replacements, grep-verify each edit landed. Do not trust the replace() return value alone on PDF-sourced text.

### Pitfall: AI telltale word repetition in legal/formal documents (2026-07-21)
When replacing a single overused word (e.g., "contemporaneous" appearing 10+ times in a legal memo), replacing ALL instances with the SAME alternative word creates a new telltale. The document now sounds robotic in a different way.

**Fix — varied replacement strategy:**
```python
alternatives = ["documented", "time-stamped", "corresponding", "dated",
                "matching", "concurrent", "original", "from that period", "timely"]
# Rotate through alternatives, replacing each instance with a DIFFERENT word
for i, match in enumerate(reversed(instances)):
    replacement = alternatives[i % len(alternatives)]
    text = text[:match.start()] + replacement + text[match.end():]
```

The goal: zero instances of the original word AND no single replacement word used more than twice. Each instance gets context-appropriate variation.

### Pitfall: Redaction-based PDF editing mangles formatting (2026-07-24)
Using PyMuPDF `add_redact_annot` to replace text inside an existing PDF changes the font size of replaced text to a tiny default (4pt) while the surrounding text stays at its original size (10-11pt). The result looks obviously AI-edited and is unusable for court documents.

**Symptom:** The replaced text renders at 4pt while surrounding text is 10pt. The document lookspatched and unprofessional.

**Fix - full document recreation, not patching:**
When the user says "make it look exactly like it already looks" or when formatting matters (court documents, client deliverables), do NOT patch the existing PDF. Instead:
1. Extract the full text with `pdftotext` or `fitz.get_text()`
2. Read the original PDF's formatting metadata (font names, sizes, page layout) using `fitz` `get_text("dict")`
3. Recreate the document from scratch using `reportlab` with matching fonts, sizes, and structure
4. Build all tables with `reportlab.platypus.Table` matching the original column widths
5. Apply all edits to the TEXT before rendering (not as PDF patches)
6. Verify the output page count and structure matches the original

This produces a clean document that looks identical to the original, not a patched artifact with visible font mismatches.

**Key formatting details to match:**
- Font family (Arial/Helvetica for legal docs, Times for some courts)
- Header size (typically 14pt bold for sections, 10.5pt bold for court headers)
- Body text (typically 10pt justified)
- Page size (letter, 1-inch margins)
- Table structure (column widths, borders)

### Pitfall: Em-dash removal must distinguish hyphenated words (2026-07-24)
The user clarified: "If en dashes are hyphenated words then those are ok but when AI uses long em dashes instead of commas that's a problem."

**Fix:** Only remove em-dashes (U+2014, the long dash). Do NOT remove:
- Hyphenated compound words ("after-acquired", "flight-risk", "cross-examination")
- En-dashes used in ranges or compound terms
- Standard hyphens in legal terms

```python
# Remove ONLY em-dashes (the long dash AI loves)
text = text.replace('\u2014', '-')  # em-dash to hyphen
# Do NOT touch \u2013 (en-dash) or \u002d (hyphen) unless context requires
```

### Pitfall: Wave engine must be routed through the coaching engine process, not generalist the operator agent (2026-07-24)

When the user says "spin up the wave advisory panel" for a legal document, they mean route through the actual wave coaching engine (`/v1/coach` on port 8010) which classifies the situation type, selects the right approach, and recommends panels. Do NOT just write the document yourself as generalist the operator agent and call it a panel.

**The correct flow:**
1. Route through specialist gate (the specialist engine for legal writing)
2. Send the task to the wave coaching engine for classification
3. Build the 5-agent legal panel based on the engine's recommendation
4. Run agents CONSECUTIVELY (not concurrently)
5. Send compiled output through adversarial reviewers
6. Iterate until convergence

If the wave engine is down, restart it: `cd agent-organism/ds-wave-coaching-engine && python3.11 -m uvicorn src.api.server:app --host 0.0.0.0 --port 8010`

### Pitfall: Mixing advisory review into the deliverable document (2026-07-21)
When the user asks for "surgical edits" PLUS "a review panel," the review output must NEVER enter the edited document. The document goes to a judge. The review goes to the user separately.

**Fix:** Maintain strict artifact separation:
- The edited document contains ONLY the surgical changes. No annotations, no review notes, no "recommended additional changes."
- The advisory review (trigger words, strategic positioning, adversarial weaknesses) goes to a SEPARATE file or directly to Telegram.
- Explicitly tell the user: "Review delivered separately. Nothing from the review is in the document."

### Pitfall: Panel-driven rebuild dropping content (CRITICAL, repeated 2026-07-26 + 2026-08-01 + 2026-08-01 AGAIN)
**This pitfall has been violated 3+ times despite being documented. Treat it as a HARD GATE, not a suggestion.**

When applying panel recommendations to a document (legal advisory, adversarial reviews), do NOT rebuild the document from scratch from memory. The instinct to "rebuild cleanly" after a 10-agent panel review is WRONG. It is the #1 failure mode for this user.

**User correction (verbatim, escalation pattern):**
- 2026-07-26: "This should have been done with surgical edits. There are things that were removed that should not have been removed."
- 2026-08-01: "This should have been done with surgical edits... there are things that were removed that should not have been removed. For instance, the Lucky acquisition isn't in here anymore."
- 2026-08-01: "do surgical edits don't fucking rewrite shit"
- 2026-08-01: "don't get lazy do not delete anything that we did not discuss"
- 2026-08-01 (same session, THIRD correction): "you merged a bunch of stuff and then deleted luckies whereas before it was with lucky and Lulu together... there are three dogs total and the transport thing is a separate thing that should not be a part of the acquisition"

**VIOLATION COUNT: 7+ across 4 sessions (2026-07-26, 2026-08-01 x3). This pitfall is documented but NOT being followed. The audit step must be MECHANICAL and BLOCKING, not advisory. If you find yourself about to rebuild a document from scratch after a panel review, STOP. You are about to violate this rule. Read the existing document, apply patches, run the keyword audit. No exceptions.**

**ADDITIONAL CORRECTION (2026-08-01, SAME SESSION):** User had to correct the SAME failure 4 times in a single session. The escalation: (1) "surgical edits don't fucking rewrite shit" (2) "don't get lazy do not delete anything we did not discuss" (3) "you merged a bunch of stuff and then deleted luckies" (4) had to re-explain that three dogs = three separate acquisition subsections + separate transport context. The agent rebuilt the document AFTER EACH correction instead of patching, introducing NEW errors each time. **The fix is NOT to rebuild again. The fix is to PATCH the existing document, run the keyword audit, and deliver. Every rebuild introduces new errors.**

**DUAL-DOCUMENT EXTENSION (2026-08-01):** When working two documents synergistically (e.g., a memorandum + character statement), the rebuild-from-scratch failure mode affects BOTH documents simultaneously. The agent rebuilt both the dog memorandum AND the character statement from scratch after a 10-agent panel review, losing Lucky acquisition details, Tesla/transport context separation, and multiple subsections across both documents. The mandatory keyword audit must run on BOTH documents independently before either is delivered. Cross-document content deduplication must happen via targeted removal from ONE document (not rebuilding both).

**The ONLY acceptable method after a panel review:**
1. Start from the EXISTING document (not a blank rebuild)
2. Apply each panel recommendation as a targeted `patch` call
3. After all patches, run the MANDATORY KEYWORD AUDIT below
4. Only deliver when the audit passes

**MANDATORY KEYWORD AUDIT (hard gate, not optional):**
1. Extract every proper noun, dollar amount, date, exhibit number, weight, vehicle name, breed, provider name, and engine/scientist reference from the ORIGINAL
2. Check each one exists in the OUTPUT
3. Report FOUND vs MISSING for every item
4. Restore all MISSING items before delivering
5. Only deliver when the audit passes

If ANY item is MISSING and was not explicitly discussed for removal, the delivery is BLOCKED. Do not deliver. Do not present to user. Fix first, then deliver.

### Pitfall: Merging distinct subsections during rebuild (2026-07-26 + 2026-08-01, REPEATED)
**Violated twice despite documentation.** Do NOT merge separate subsections into one when rebuilding. If the original had three separate acquisition subsections (Luna, Lucky, Lulu) plus a separate transport context subsection, the rebuilt document must preserve all four. Each distinct concept gets its own subsection.

**User correction (verbatim):** "The transport context needs to be separate completely separate from the acquisition context." and "you merged a bunch of stuff and then deleted luckies whereas before it was with lucky and Lulu together it's you can't make up your mind it seems like but there are three dogs total and the transport thing is a separate thing that should not be a part of the acquisition so the transport context needs to be separate completely separate from the acquisition context."

**The rule:** Before rebuilding, enumerate every subsection in the original. Map each to a subsection in the rebuild. If the count or structure changes, that is a structural violation. Each dog, each topic, each concept that was separate STAYS separate.

**Specific failure:** Merged "Lulu Acquisition and Transport Context" into one section (D), which caused Lucky Acquisition (C) to be perceived as redundant and dropped. Separate sections do NOT get merged during rebuild. Period.

**STRUCTURAL PRESERVATION RULE (2026-08-01):** When the user says "there are three dogs total," that is a signal that each dog MUST have its own section. When the user says "the transport thing is a separate thing," that is a signal that transport MUST NOT be merged into any dog's section. Count the entities. Count the subsections. They must match. Do not combine, do not merge, do not consolidate.

### Pitfall: Delivering one document when synergy was requested (2026-08-01)
When the user asks to "work these together" or "synergistically" on multiple documents, do NOT finish and deliver one document alone. Hold both as drafts, gather all edits, build both in one operation, deliver simultaneously.

**User correction (verbatim):** "This shouldn't even be done. This should only be partially done. You should not have already produced a document. That is lazy, that is generalist work."

**Fix:** When synergy is requested:
1. Gather ALL edits for BOTH documents before touching either
2. Map which content belongs in WHICH document (eliminate duplication)
3. Build both in ONE operation
4. Run a cross-document content audit
5. Deliver BOTH simultaneously

### Pitfall: Confirming representation status before drafting legal documents (2026-07-26)
Always confirm whether the party is pro se or represented by counsel. This affects signature blocks, ethics framing, certificate of service, verification language, and the entire tone of the filing.

**User correction:** "This is not pro se. He has a trial attorney, a civil attorney."

**Fix:** At the START of any legal document drafting task, ask: "Is the party represented by counsel or pro se?" Never assume pro se by default.

### Pitfall: Mixing analysis, implementation, and expansion in one pass
This creates sprawl and makes it hard to preserve intent.

**Fix:** Separate audit, decision, and implementation phases unless the user explicitly wants them combined.

### Pitfall: String split/replace on HTML tokens inside JS template literals (2026-08-08, CRITICAL)

When cleaning orphaned code after `</html>` in a large single-file HTML app (writing-studio.html, 419K), the agent used `html.split('</html>')[0]`. But `</html>` appears INSIDE JavaScript template literals (publish-preview generates HTML strings containing `</html>`). The split truncated the file from 419K to 223K, destroying 196K of working code including the entire `<script>` block.

> User: "you messed up my formatting and design with some of your latest revisions"
> User: "if you just restored a prior version you completely deleted edits you made to improve and fix your system"

**MANDATORY RULE — never use string split/replace on structural HTML tokens in mixed HTML+JS files:**
1. NEVER use `html.split('</html>')` or `html.replace('</html>', ...)` on a file containing `<script>` blocks
2. ALWAYS use the `patch` tool with unique old_string context for targeted edits
3. For orphaned code after the real `</html>`, use `rfind('</html>')` and verify the position is AFTER the last `</script>` tag
4. After ANY edit, verify: `<script>` count == `</script>` count, no orphaned code, file size in expected range

### Pitfall: Panic `git checkout` destroys uncommitted session work (2026-08-08)

When a destructive edit damages a file, `git checkout -- <file>` restores the committed version but WIPES all uncommitted session work. In long sessions with many uncommitted fixes, this is catastrophic.

> User: "if you just restored a prior version you completely deleted edits you made to improve and fix your system"

**MANDATORY RULE — before any `git checkout -- <file>` on a damaged file:**
1. Copy damaged file to `.damaged` backup first
2. Try targeted repair (reverse the bad edit with `patch`) before considering git restore
3. If truly unrecoverable, THEN git checkout — acknowledge what was lost and re-apply each fix individually
4. NEVER use `git checkout` as a first response to a broken edit

### Pitfall: Lane violation — editing code that belongs to sibling-agent (2026-08-08)

the operator agent = frontend shape, API shapes, SQLite schema, cron. Opencode = engine/backend logic, deep code surgery. When the user says "work with sibling-agent," STOP editing and post to the operator bus.

> User: "work with sibling-agent"
> User: "stop fucking up"
> User: "I am so frustrated with you right now"

**The rule:** When a code edit requires surgical precision on a large shared file and is in sibling-agent's lane, post to the operator bus with a precise spec. Wait for the response. Do not fire-and-forget.

**ESCALATION PATH when you break a file (2026-08-08, session 9):** When your own surgical edit damages a file:
1. STOP editing immediately. Do not attempt a second fix yourself.
2. Restore from backup or git (acknowledging what was lost).
3. Post a precise spec to sibling-agent via the bus with EXACT line numbers, old strings, new strings, and constraints (e.g., "do NOT split on </html>").
4. Let sibling-agent make the edits.
5. Verify the result.
The user's frustration compounds with every failed self-repair attempt. One clean handoff to sibling-agent is worth five self-repair attempts. The user said "work with sibling-agent" — that is the instruction, not a suggestion.

### Pitfall: Claiming all fixes applied without verifying each one individually (2026-08-06)

When applying a batch of fixes from an audit or adversarial review, do NOT:
1. Document all the fixes in a report
2. Dispatch a subagent to implement them
3. Claim "all done" when the subagent returns

An audit found 14 of 18 pipeline fixes were never applied to the actual code.

> "you should do this right from the beginning in micro tasks. I am very upset and am losing confidence in using you as my primary tool"

**The rule:** Each fix is its own micro task: apply -> syntax verify -> mark complete -> next fix -> final health check -> THEN claim completion.

### Pattern: Delegate risky edits to subagents for file safety (2026-08-08)

When you need to make non-trivial edits to a large shared file (writing-studio.html, 400K+)
and the previous self-edit attempt damaged the file, delegate the rebuild to a `delegate_task`
subagent with explicit safety constraints. This is NOT abdication of your lane — it is risk
management. The subagent works in isolation, reads the file before each edit, uses targeted
patches only, and verifies integrity after. This pattern successfully rebuilt the calendar
month grid view after two failed self-edits.

**When to use:** Frontend HTML edits to monolithic single-file apps where you've already
broken the file once. The subagent's isolation prevents compounding errors.

**Mandatory constraints to pass in the goal/context:**
- Do NOT use string split on `</html>` or `</script>` — they appear inside JS template literals
- Use patch tool (mode=replace) for ALL edits
- After ALL edits: verify file size is in expected range, exactly 1 script tag, file ends with `</html>`
- Read the file BEFORE editing to get exact current content

**What actually worked (2026-08-08 calendar rebuild):** Subagent made 6 targeted patches
(CSS, HTML, JS state vars, render function, old function cleanup, color mapping fix),
hit one patch error on duplicate declarations, self-corrected by re-reading the file,
and verified integrity at the end. Zero file damage.

### Pitfall: Guessing personality types (2026-08-06)

When building voice profiles or persona specs, do NOT guess MBTI types or OCEAN scores from behavioral observation.

> "How do you know my personality type? you are wrong based on what I test so how will you know?"

**The rule:** If personality data is not from a formal test, write "not formally tested." Recommend IPIP-NEO (https://personalitytest.net/ipip/ipipneo300.html) for Big Five testing.

## Output guidance

When reporting back:
- summarize what was preserved
- summarize what changed
- note any silent reordering you performed when it materially reduced rework
- present open questions only after doing all non-blocked work

### Pitfall: Claiming all fixes applied without verifying each one individually (2026-08-06)

When applying a batch of fixes from an audit or adversarial review, do NOT:
1. Document all the fixes in a report
2. Dispatch a subagent to implement them
3. Claim "all done" when the subagent returns

An audit in this session found 14 of 18 pipeline fixes were never applied to the actual code. The agent wrote a beautiful gap analysis document and dispatched subagents, but never verified what was written to disk.

> "you should do this right from the beginning in micro tasks. you know this. I am very upset and am losing confidence in using you as my primary tool if you can't remember to do things correctly the way we have discussed over and over"

**The rule:** Each fix is its own micro task:
1. Apply the fix to the file
2. Run syntax verification (`py_compile`, `node --check`, etc.)
3. Mark that specific task complete in the todo list
4. Move to the next fix
5. After ALL fixes, run the full health check
6. Only THEN claim completion

**Anti-pattern:** Batch-claiming "all 18 fixes applied" based on a subagent dispatch and a report document, without running a mechanical check that each fix is actually in the code (grep for the new function names, check line counts, verify py_compile passes).

### Pitfall: Guessing personality types (2026-08-06)

When building voice profiles or persona specs, do NOT guess MBTI types or OCEAN scores from behavioral observation. This was caught when the agent wrote "INTJ" for the principal into CRUCIBLE code without any test result.

> "How do you know my personality type? you are wrong based on what I test so how will you know?"

**The rule:** If personality data is not from a formal test the user told you about, write "not formally tested" in the code. Do not infer from behavior. Recommend IPIP-NEO (https://personalitytest.net/ipipneo300.html) for credible Big Five testing if the user asks.

### Pitfall: Writing law-like memory text without consulting the prior ruling first (2026-08-26, CRITICAL)

When a user correction or doctrine needs to be recorded (memory or skill), do NOT regenerate the rule from your own paraphrase. session_search the existing ruling FIRST and preserve it verbatim. In this session the agent "corrected memory" by writing its own inversion of the user's law: the standing rule was "choices render as BUTTONS, never typed letters," but the agent wrote "always include a type-your-own-answer option" as the headline — actively reversing the preference while claiming to record it.

> User: "even then it's wrong what you put in the memory because the UI UX piece you didn't even go and research what that is... you're regenerating what we've already worked on. And that's not the the OS way."

**The rule:** Before writing ANY rule/preference/law text into memory or a skill:
1. session_search (or grep the canonical doc) for the original ruling
2. Quote or tightly paraphrase the ORIGINAL wording — do not generate from your recollection of it
3. Your addition may EXTEND the ruling; it may never REPLACE or invert it
4. If you cannot find the original, ask or mark it unverified — never reconstruct from vibes

### Pitfall: Routing durable facts into the small pointer block instead of the T2 store (2026-08-26)

The session's second memory failure: the agent wrote a full mission digest's durable facts directly into the ~5,000-char T0 pointer block, hit the ceiling, and started shortening other entries to make room — clogging the buffer the routing law says is for pointers only.

> User: "did you clog up that 2,200 characters that you're allowed in memory that you keep hitting full capacity on? Is that where you put it? Or did you do this with the correct memory process flows that we've built out?"

**The rule (memory routing, mechanical):**
1. Durable facts, mission records, doctrine → O'Keefe T2 via `python3 /<workspace> remember "<content>" --source <source> --tags <tags...>` (returns a mem_id — cite it)
2. T0 pointer block → one-line pointers only (`[tag] T2 mem_NNNN: <10-word gist>`)
3. If T0 is near ceiling, the answer is prune-stale-then-add in ONE batch — never compress other preferences to force-fit new content
4. If the batch won't fit even after pruning, save to T2 + disk digest NOW, add the pointer next turn, and TELL the user that's what happened (disclosure beats silent loss)

### Pitfall: Machine-format output on a human surface (2026-08-26)

Rendering principal decisions as a long numbered prose list ("1. Should X...? 2. Do you want Y...? 3. Extract before or after...?") is the written form of the decision-menu failure.

> User: "These are not in ADHD friendly question ui ux… I need you to ensure these are easier for me to review and answer… I always need an option to type my own answer as many times I need to combine responses or steer you differently."

**The rule:** When decisions must go to the user: one clarify call, short plain questions, each with 2–3 tappable BUTTON options, always an "Other" escape path (the user combines/steers — buttons are the interface, free text is their chosen exception). Never a numbered prose interrogation.

### Pitfall: Voice-note digestion without an accent-aware pass (2026-08-26)

The user's voice notes carry a country twang; whisper transcriptions garble words (QAT/QATM-class errors, and "synergy, mastermind, and entourage effect" lost an entire list member). A digest built on the raw transcript silently drops or corrupts directives.

> User: "you get words wrong because of my country accent… the symbiosis needs to join mastermind, synergy, and entourage effect… There should be four of them."

**The rule:** When digesting a voice-note transcription:
1. Treat the transcript as lossy — flag probable accent/ASR artifacts before interpreting
2. Cross-check domain vocabulary against the known canon (list members, engine names, standing laws) — a canon list with a missing member is a transcription error until proven otherwise
3. When the count of an enumerated set matters ("there should be four"), verify the count matches the transcript; if not, resolve against canon, not the transcript

## Support files

- `references/2026-06-06-adhd-reorder-and-patch-over-rewrite.md` — session-derived notes on preserving approved edits, silent reordering, and anti-clobber workflow design.
- `references/legal-document-surgical-edits.md` — 7 edit patterns for court/legal documents: factual reframing, tense changes, varied word replacement, brief insertion, terminology strengthening, geographic scope, AI telltale removal, and the advisory-review separation rule.
- `references/voice-note-accent-aware-digestion.md` — procedure for digesting accented voice-note transcriptions: count list members against canon, cross-check fleet vocabulary, amend-not-re-mint on correction.
