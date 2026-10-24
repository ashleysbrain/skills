# Cross-Disciplinary Term Sweep

When introducing novel terminology that claims field-defining status, you must acknowledge ALL prior uses of the word across disciplines, not just within your core domain.

## Why This Matters

Hostile reviewers will search databases and find prior uses outside your discipline. Failing to cite them appears as:
- Ignorance of the literature
- Suppression of competing claims
- Overreach in novelty

## Procedure

### 1. Broad Search Strategy
Search across these domains with variations of the term:
- Psychology and cognitive science
- Biology and medicine
- Neuroscience
- Philosophy
- Your core domain (AI, CS, etc.)

Search operators:
```
"your-term" OR "your-term" -example1 -example2
site:arxiv.org "your-term"
site:pubmed.ncbi.nlm.nih.gov "your-term"
site:philpapers.org "your-term"
```

### 2. Document Every Relevant Use
For each relevant prior use, capture:
- Author(s) and year
- Title
- Venue/journal
- Context (how they used the term)
- DOI or stable URL

### 3. Distinguish Your Contribution
Explicitly state what you are claiming vs. what is prior art:

```
The term "physiomorphic" has been used in several contexts:
- Richards (1989) described psychological language derivation
- Manimaran et al. (2024) introduced "physiomorphic age" in cardiovascular risk
- Hwang et al. (2026) used it for neuromorphic biomedicine

Priority is claimed here for the formulation of Physiomorphic AI as an organism-referenced architecture paradigm with an explicit mapping object, composite measure, and disconfirmable engineering predictions.
```

### 4. Do Not Claim the Word Itself
Never claim you invented the word. Claim the specific formulation, framework, or research program built around it.

## Example: Physiomorphic AI (2026)

Searches discovered:
- Richards 1989 (psychological language)
- Manimaran 2024 (deep learning, cardiovascular age)
- Hwang 2026 (neuromorphic principles in biomedicine)
- Arbib 2025 (broader physiomorphic direction in NeuroAI)
- Niu 2017 (neuromorphic neuromechanics integration)

Paper acknowledges all five explicitly and distinguishes the new contribution.

## Pitfalls

- **Domain tunnel vision:** Only searching arXiv or CS venues
- **Assuming synonymy:** Thinking "physiomorphic" = "physiological" and skipping the term sweep
- **Overclaiming:** Saying "we introduce Physiomorphic AI" without prior-art context
- **Ignoring workshops/position papers:** These count as prior art
- **Missing preprints:** medRxiv, arXiv, SSRN matter

## Tools

- `web_search` with domain filters
- `web_extract` for paper abstracts
- Crossref API for DOI lookups
- Semantic Scholar for citation networks