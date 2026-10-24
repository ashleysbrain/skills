# Citation Grounding: The Three-Disconnected-Systems Bug

## The Problem

After 6 passes of pipeline runs, metrics looked healthy (8 citation markers,
9 sections, 0 em dashes, 2,789 words). But reading the ACTUAL PROSE revealed
the citations were completely fabricated from LLM training memory.

Three citation systems existed in the pipeline, none connected:

1. **Stage 2 (Research Gathering):** Gathers real papers via OpenAlex/CrossRef/arXiv.
   Stores as flat dicts: `{"source": "crossref", "title": "...", "doi": "...", ...}`
2. **Stage 3 (Toulmin Skeleton):** Uses abstract ref_ids: `S001`, `S002`, `S008`.
   These ref_ids reference the Stage 2 papers but there is NO MAPPING.
3. **Stage 4.6 (Progressive Drafting):** LLM receives skeleton + citations but
   the citation context uses DIFFERENT numbering `[1]-[6]` than the skeleton's
   `S001-S008`. The LLM cannot resolve the mapping, so it invents real-sounding
   citations from training memory (Barrett 2015, Friston 2010, etc.).

The draft's References section listed papers that were NEVER in the gathered
evidence. They are real papers the LLM knows from training, but they are not
the papers the pipeline actually found.

## Root Cause

The `_progressive_draft` method built `cite_context` by indexing citations as
`[1], [2], [3]...` while the Toulmin skeleton used `S001, S002, S003...` as
ref_ids. The LLM prompt showed both systems simultaneously with no mapping
between them. The LLM resolved the ambiguity by ignoring the evidence list
entirely and generating citations from memory.

## The Fix (4-part)

### Part 1: Keyword Relevance Filter (removes arxiv spam)

5 of 10 gathered citations were physics papers ($B^0_s$ decay, ATLAS detector,
gravitational waves, neutrinos) from arXiv searches that matched keywords
poorly. Filter by checking title+abstract against idea keywords:

```python
keywords = {word for word in idea.lower().split() if len(word) > 4}
relevant = []
for c in self.state.citations[:12]:
    combined = (c.get("title","") + c.get("abstract","")).lower()
    matches = sum(1 for kw in keywords if kw in combined)
    if matches >= 2 or any(kw in combined for kw in domain_terms):
        relevant.append(c)
```

### Part 2: Full Citation Metadata in Prompt (not just ref_id)

Pass the actual title, authors, year, DOI to the draft prompt — not abstract
ref_ids the LLM cannot resolve:

```python
cite_context.append(f"[{i+1}] {first_name} ({year}). {title}. {abstract[:120]}\n    DOI: {doi}")
```

### Part 3: Explicit Citation Prohibition in Pass 1 Prompt

```
CRITICAL CITATION RULES:
- You may ONLY cite papers from the EVIDENCE list below.
- Do NOT invent, fabricate, or recall references from memory.
- In the References section, list ONLY papers that appear in the evidence list.
- If you need a citation for a claim and no evidence paper supports it,
  state the claim WITHOUT a citation marker.
```

### Part 4: Pass 2 Preservation Rule

Pass 2 (knowledge-transforming) was stripping citations during restructuring.
Added explicit rules: "Preserve ALL [N]. Do NOT add new citations that were
not in the original draft."

## The Verification Technique

Metrics inspection is INSUFFICIENT for citation quality. You must READ THE
ACTUAL PROSE and check:

1. Do the draft's [N] markers match the gathered citations?
2. Does the References section list ONLY papers from the evidence pool?
3. Are the cited papers' findings actually engaged with (not just name-dropped)?

```python
# Check if draft citations match gathered evidence
draft_markers = re.findall(r'\[(\d+)\]', draft)
gathered_titles = [c.get("title","")[:40] for c in state["citations"]]
refs_section = draft.split("## References")[1] if "## References" in draft else ""
# If refs_section contains author names NOT in gathered_titles, they're fabricated
```

## The Breakthrough: Post-Draft Programmatic Citation Stripping (Pass 8-9)

The prompt-layer fixes (parts 1-4) reduced fabrication but didn't eliminate it.
The LLM still generated 23 markers for 5 evidence papers. The real fix was
PROGRAMMATIC — strip hallucinated markers AFTER each pass, inject References
from the evidence list.

### Part 5: Post-Pass Citation Stripping (Pass 8, commit 23569d4)

After EVERY pass (1, 2, and 3), run this on the draft text:

```python
n_citations = len(cite_context)  # actual evidence count
import re as _re

# Strip any [N] marker where N exceeds the evidence count
def _fix_marker(m):
    n = int(m.group(1))
    if n > n_citations:
        return ""  # Strip entirely
    return m.group(0)
draft = _re.sub(r'\[(\d+)\]', _fix_marker, draft)
draft = _re.sub(r' {2,}', ' ', draft)  # clean double spaces

# Inject References section from actual evidence (replaces LLM-generated one)
ref_lines = ["## References", ""]
for entry in cite_context:
    ref_lines.append(entry.split(" DOI:")[0])  # strip DOI prefix from display
ref_text = "\n".join(ref_lines)

if "## References" in draft:
    draft = draft.split("## References")[0].rstrip() + "\n\n" + ref_text
else:
    draft = draft.rstrip() + "\n\n" + ref_text
```

This runs at TWO points: after Pass 1 (before Pass 2 receives it) and after
Pass 3 (before the draft enters Stage 5). Even if the LLM invents citations
during transformation, they get stripped before the draft moves forward.

### Verified Result (Pass 9)

- 5,109 words, 8 sections, 5 grounded citations [1]-[5]
- References section lists ONLY actual gathered papers
- 0 fabricated citations, 0 hallucinated metrics
- All citation markers map to real evidence from Stage 2

## Commit Reference

- Commit `6ce9bdd`: Fixed citations flat dict, Pass 3 shrinkage, Stage 6 dict overwrite
- Commit `f9b477c`: Citation grounding — filter arxiv spam, map ref_ids, forbid fabrication
- Commit `4927027`: Pass 2 preserves citations, Pass 3 timeout 120s→180s
- Commit `23569d4`: Post-Pass3 citation grounding — strip hallucinated markers + inject References
