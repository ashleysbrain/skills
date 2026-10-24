# arXiv full-text fetch without web tools (validated 2026-08-20, papers 2608.13331 + 2608.03702)

## The chain

```bash
# 1. Metadata (title/authors/abstract) — arXiv export API, no key:
curl -sL "http://export.arxiv.org/api/query?id_list=2608.03702"
# Parse with regex on <title>/<summary>/<published>/<name>.
# Drop the FIRST <title> — it is the feed title, not the paper's.

# 2. Full paper HTML — arXiv HTML5 render (most 2024+ papers), 200-500KB:
curl -sL -m 25 -o /tmp/paper.html "https://arxiv.org/html/<ARXIV_ID>"

# 3. Fallback if /html/<id> 404s (no HTML5 render): /pdf/<id> via PDF
#    extraction, or export API abstract only.
```

## Clean-text extraction

Standard strip (script/style before tags, unescape, whitespace collapse) lands
at 50-110KB clean text for a typical paper.

## THE PITFALL — TOC duplication

arXiv HTML pages carry the full table of contents at the top. So:

```python
txt.find("Abstract")      # hits the TOC entry, NOT the abstract body
txt.find("Conclusion")    # same
```

Fix — take the SECOND occurrence, or anchor on body-unique text:

```python
idxs = [m.start() for m in re.finditer("Conclusion", txt)]
body = txt[idxs[1]:idxs[1]+2200] if len(idxs) > 1 else ""
# Or anchor on the abstract's first sentence (unique to the body):
i = txt.find("Quantum optimal control is a key tool")  # body-unique phrase
```

Symptom if ignored: every "extracted section" is the same TOC string, and the
digest silently loses all section content.

## Session record (2026-08-20)

- 2608.13331 (Training AI Scientists to Replicate Research, Inherent Labs):
  fetched full HTML via this chain while Firecrawl was down; second-occurrence
  extraction recovered Methods/Results/Discussion bodies after TOC trap hit.
- 2608.03702 (Inverse Design of Quantum Control Sequences with FNOs,
  UCLA/Caltech/NVIDIA): 109,821 clean chars; API metadata + /html/ body;
  TOC pitfall navigated on first attempt.
