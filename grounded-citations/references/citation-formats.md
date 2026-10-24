# Citation formats per output target

The ledger is format-agnostic: `sources.py render --style ...` emits the block,
this file says where it goes and what the inline marker looks like.

## Style authority (binding, studied 2026-08-14)

The canonical university authority is the **Purdue OWL Research and Citation
wing** (owl.purdue.edu/owl/research_and_citation/) — 48 live sub-pages covering
APA 7th, MLA 9th, Chicago 18th (17th-ed pages retired by OWL as of 2026),
IEEE, AMA, ASA, plus quoting/paraphrasing/summarizing and plagiarism rules.
Its 2024 comparative citation chart is saved locally at
`references/owl-2024-citation-chart.pdf`. When a format question is not
answered here, defer to the corresponding OWL page — never to memory.

Which style per output type:

| Output | Style | Anchor rules (captured from OWL 2026-08-14) |
|---|---|---|
| Physics/eng/ML papers, tech reports | IEEE numeric | `[1]` in order of citation, never alphabetical; "in [1]" not "in reference [1]"; pinpoints inside brackets: `[6, Sec. VI]`, `[6, Fig. 5]`, `[6, pp. 8-10]`; 3+ consecutive ids collapse with en-dash: `[3]–[5]`; authors surname+initials, ≤6 all / 7+ et al.; months 3-4 letters; online: `[Online]. Available: URL. Accessed: month day, year.` |
| Health/social-science/clinical docs | APA 7th author-date | `(Jones, 1998)`; direct quotes add `p.`/`pp.` with en-dash ranges: `(Jones, 1998, pp. 199–201)`; reference list hanging indent, names inverted w/ initials, up to 20 authors, `&` before last; web sources: no "Retrieved from" (retrieval date only for changing content, e.g. wikis), `(n.d.)` if undated, group author = site name → omit site name |
| Humanities PDFs, books, legal/history | Chicago 18th (2024) | Notes-Bibliography or Author-Date; follow OWL CMOS 18th-ed pages |
| MLA contexts (lit/education) | MLA 9th | Works Cited; follow OWL MLA pages |
| Chat/markdown/social/Telegram/slides | House numeric | `[n]` per sentence + Sources block from the ledger (below) — house style deliberately mirrors IEEE's bracketed-number behavior |

Mechanical rules that apply to every style: quotations match the source
word-for-word and are attributed; paraphrases change the wording AND keep the
attribution; summaries attribute too. Every in-text marker must resolve to
exactly one list entry and vice versa (APA states this explicitly; IEEE
enforces it by order-of-citation numbering).

## Markdown / chat answers

Inline `[n]` immediately after the sentence. Block at the end:

```
## Sources

[1] https://example.com/a — Page title
[2] https://example.com/b
```

`--style plain` gives a bare `Sources:` header for chat replies where a
markdown heading would be noise.

## PDF via LaTeX (`latex-pdf-report` skill)

Use `--style footnotes` and map each id to `\footnote{}` at first use, or keep
numeric markers and emit an endnotes section. For a bibliography-shaped report,
`--style bibtex` writes `@misc` entries keyed `source<N>`; cite them with
`\cite{source3}` and let BibTeX render the list.

Do not mix: either numeric `[n]` + a Sources section, or `\cite{}` + BibTeX.
Two numbering systems in one document is worse than none.

## Word (.docx, `docx` skill)

Real footnotes are preferred over inline brackets in prose documents intended
for human editing — reviewers expect Word footnotes. Keep the ledger ids as the
footnote numbers so `verify` still works on a markdown source-of-truth, and
generate the .docx from that markdown.

## Slides (.pptx, `powerpoint` skill)

Inline `[n]` in the bullet, one "Sources" slide at the end rendered with
`--style plain`. Never put a URL in a body bullet — it wrecks the layout and
can't be clicked in a projected deck.

## Spreadsheets (.xlsx)

Add a `source` column holding the id, plus a `Sources` sheet built from
`render --style plain`. Do not paste URLs into data cells.

## Wiki / multi-page output (`llm-wiki`, Obsidian)

Per-page Sources block, ids shared across pages from one ledger. Because ids
are ledger identities, `[7]` means the same page everywhere in the wiki — that
consistency is the reason not to reset the ledger between pages of one build.

## Research papers

Hand off to the `research-paper-writing` skill. Export with
`--style bibtex` into `references.bib`, then follow that skill's citation
verification (it greps `\cite{...}` against the .bib). The ledger's job ends at
producing verified URL entries; venue formatting is that skill's domain.

## Code and config artifacts

No citations inside generated code. If provenance matters, put it in the
commit message, the PR body, or a doc header — not in comments scattered
through source.
