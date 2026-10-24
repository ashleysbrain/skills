# Prior-Art and Competitive Term Sweep

Full methodology for establishing whether a term or concept already exists
in any domain. Developed during the "physiomorphic AI" competitive sweep
(2026-07-09) and updated after the premature-zero failure in the same
session.

## When to use

- User asks "is anyone using term X in field Y?"
- User has coined a neologism and wants to know if it is truly novel
- You need to defend a novelty claim with evidence
- User challenges your findings and you need to re-verify

## Phase 1: Broad sweep (all databases in parallel)

Run all of these in parallel via one `execute_code` block. Each takes 2-5s.

### Academic databases

```python
import subprocess, json

term = "physiomorphic"  # replace with your term

queries = {
    "arxiv": f'curl -sL "https://arxiv.org/search/?query={term}&searchtype=all"',
    "openalex": f'curl -sL "https://api.openalex.org/works?search={term}&per-page=10&sort=relevance_score:desc" -H "User-Agent: Mozilla/5.0"',
    "crossref": f'curl -sL "https://api.crossref.org/works?query={term}&rows=5" -H "User-Agent: Mozilla/5.0"',
    "semantic_scholar": f'curl -sL "https://api.semanticscholar.org/graph/v1/paper/search?query=%22{term}%22&limit=10&fields=title,year,venue" -H "User-Agent: Mozilla/5.0"',
}

for name, cmd in queries.items():
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
    print(f"\n=== {name} ===")
    try:
        data = json.loads(r.stdout)
    except:
        print(r.stdout[:500])
```

### Non-academic databases (patents, trademarks, lexicon, dictionary)

```python
extra_queries = {
    "google_patents": f'curl -sL "https://patents.google.com/xhr/query?url=q%3D%2522{term}%2522%26num%3D10&exp=" -H "User-Agent: Mozilla/5.0"',
    "datamuse_spelling": f'curl -sL "https://api.datamuse.com/words?sp={term}" -H "User-Agent: Mozilla/5.0"',
    "datamuse_meaning": f'curl -sL "https://api.datamuse.com/words?ml={term}" -H "User-Agent: Mozilla/5.0"',
    "wikipedia": f'curl -sL "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={term}&format=json"',
}
```

### Web search (via native tool, NOT browser)

Use `web_search` for:
- `site:collinsdictionary.com {term} "new word suggestion"`
- `site:uspto.report {term}` (trademark check)
- `"{term}" {target_field}` (exact phrase in target field)

## Phase 2: Intersection searches (MANDATORY before claiming novelty)

**This is the step that was skipped in the 2026-07 session, causing a
false "zero results" declaration. The user had to correct it.**

Before declaring a term novel in field Y, run at least 3 intersection
searches that pair the term with plausible adjacent fields. The user
might be thinking of a usage you haven't considered. Brainstorm
intersections from the term's morphology:

- `{term} {target_field}` — the obvious one
- `{term} {adjacent_field_1}` — e.g. if the term has "physio," try medicine, digital twin, cardiology
- `{term} {adjacent_field_2}` — e.g. if the term has "morphic," try robotics, hardware, neuromodulation
- `{term} {method}` — e.g. "deep learning," "neural network," "closed-loop"

Use `web_search` for each intersection. If ANY intersection returns
results in the target domain, you have NOT established novelty. Read
those results before reporting.

### Worked example

Term: "physiomorphic" | Target field: AI/computing

| Intersection search | Result | Lesson |
|---------------------|--------|--------|
| `"physiomorphic" AI` | Zero relevant (Oakley sunglasses, Collins dictionary submission) | Broad field — not enough |
| `"physiomorphic" digital twin medical` | **HIT**: arXiv:2603.27716 (NPBH workshop report, 6 uses) | Biomedical engineering usage |
| `"physiomorphic" neuromodulation` | **HIT**: Same paper, Denison attribution | Coined in neuromodulation context |
| `"physiomorphic age" cardiology` | **HIT**: Manimaran et al. medRxiv 2024 | Active cardiology research line |

Without Phase 2, I declared "zero in AI." With Phase 2, the competitive
landscape revealed two active research uses the user already knew about.

## Phase 3: Full-text PDF mining

Academic APIs search titles and abstracts, not full paper bodies. A term
used deep in a workshop report, methods section, or discussion will be
invisible to metadata search. When Phase 1+2 give ambiguous results, or
when a search result looks like it MIGHT contain the term, download the
PDF and grep:

```bash
curl -sL "https://arxiv.org/pdf/XXXX.XXXXX" -o /tmp/paper.pdf
pdftotext /tmp/paper.pdf /tmp/paper.txt
grep -n -i -B3 -A3 "TERM" /tmp/paper.txt
```

This technique found 6 uses of "physiomorphic" inside a 56-page arXiv
workshop report (arXiv:2603.27716) that the arXiv search API did not
surface for the term. The term appeared in body text but not in the
title, abstract, or subject keywords.

When to use PDF mining:
- A search result title looks adjacent but doesn't contain your term
- The user says "I saw it in a paper about X" — find likely papers about X and mine them
- The term is recent (last 12 months) and may be in preprints not yet well-indexed
- A workshop report or conference proceeding covers the topic (these often have 40+ pages with terms deep in the body)

## Phase 4: Classification and novelty assessment

Compile all hits into this table format:

| Database | Total hits for term | Any in target field? |
|----------|--------------------|-----------------------|
| arXiv (metadata) | 0 | N/A |
| arXiv (full-text PDF) | 6 in 1 paper | YES — biomedical engineering |
| OpenAlex | 137 | None directly, some biomedical |
| Crossref | 21 | None in AI/computing |
| Semantic Scholar | 32 | None in AI/computing |
| Google Patents | 0 | N/A |
| Wikipedia | No article | N/A |

Then for each hit that DOES exist, classify by domain:
- What field uses it?
- What does it mean in that field?
- Is the meaning the same as the user's coinage? (collision vs coincidence)
- Who is the attributed coiner? (matters for IP/trademark strategy)

## Defending against user challenges

When the user says "I found it on Google" — this is a SIGNAL, not an
attack. It means you missed something. Two possible scenarios:

### Scenario A: User is conflating terms (hold your ground)
Run the EXACT-PHRASE quoted search. Show them the ACTUAL result titles.
Identify the likely confusion (visually similar term, different concept).
Example: "Physical AI" (NVIDIA/IBM/WEF term about robots in physical
world) vs "Physiomorphic AI" (organism-mimicking AI architecture).
Google floods results for the former.

### Scenario B: You missed a domain intersection (acknowledge and fix)
This is what happened 2026-07. The user said "digital twins and
physiomorphic AI as it relates to understanding medical information on a
human." That specific intersection was searchable and produced real
results. When the user gives you a MORE SPECIFIC description of what they
saw, search THAT intersection immediately. Do not re-litigate the broad
search — pivot to the intersection they described.

**The lesson: when the user challenges your "zero results," treat their
challenge as a search vector, not a debate. They may know an intersection
you didn't try.**
