# Cognitive Science of Expert Academic Writing — Evidence Base

**Synthesized 2026-08-10 from OpenAlex primary-source retrieval.** Verified with
real abstracts, DOIs, and citation counts.

**CRITICAL USER PREFERENCE:** When presenting this research to the user, show
the ACTUAL papers with real abstracts, DOIs, and citation counts — NOT
generalized summaries. The user has stated emphatically (9x): "I want to see
the actual literature not your generalization." Pull from OpenAlex and Semantic
Scholar. Present primary sources, let the user interpret.

## 1. Expert writing is recursive, not single-pass

**Flower & Hayes (1981)** — "A Cognitive Process Theory of Writing" (*CCC*
32(4), 365-387). 3,512 citations. DOI: 10.2307/356600. Writing = task
environment + long-term memory + three recursive processes (Planning ->
Translating -> Reviewing). NOT linear stages — expert writers cycle constantly.

**Kellogg (2008)** — "Training writing skills: A cognitive developmental
perspective" (*J. Writing Research* 1(1)). 839 citations.
DOI: 10.17239/jowr-2008.01.01.1. Three stages: knowledge-telling (novice) ->
knowledge-transforming (competent) -> **knowledge-crafting** (expert manipulates
author content, text, AND reader's interpretation simultaneously).

## 2. Expert revision is meaning-first and multi-pass

**Sommers (1980)** — "Revision Strategies..." (*CCC* 31(4)). 753 citations.
DOI: 10.2307/356588. Students revise at word level. Experts revise at
argument/discourse level — rethink thesis, restructure, delete sections.

**Flower et al. (1986)** — "Detection, Diagnosis, and the Strategies of
Revision" (*CCC* 37(1)). 376 citations. DOI: 10.2307/357381. Three subprocesses:
Detection -> Diagnosis -> Strategy. Writers often DETECT problems they cannot
DIAGNOSE.

## 3. Pre-writing synthesis is the highest-leverage phase

**Booth, Colomb & Williams (1995)** — "The Craft of Research" (U Chicago Press).
458 citations. topic -> question -> problem -> sources -> argument -> draft ->
revision. This sequence determines quality more than any drafting decision.

## 4. Argumentation theory

**Toulmin (1958/2003)** — "The Uses of Argument" (Cambridge UP). 5,618 citations.
DOI: 10.1017/cbo9780511840005. Claim -> Grounds -> Warrant -> Backing ->
Qualifier -> Rebuttal. WARRANT is most often omitted, most important.

**Walton et al. (2008)** — "Argumentation Schemes" (Cambridge UP). 1,351
citations. 26+ argument types each with mandatory critical questions.

**Osborne et al. (2004)** — "Enhancing argumentation in school science" (*JRSS*
41(10)). 1,540 citations. DOI: 10.1002/tea.20035. Argument quality correlates
with REBUTTAL quality, not claim quality.

## 5. Evidence reporting (PRISMA)

**Liberati et al. (2009)** — "PRISMA Statement" (*PLoS Medicine*). 28,000
citations. DOI: 10.1371/journal.pmed.1000100. 27-item checklist including
risk-of-bias assessment per source.

## 6. AI-assisted writing evidence

**Doshi & Hauser (2024)** — *Science Advances*. 599 citations.
DOI: 10.1126/sciadv.adn5290. LLM improves individual quality but collapses
collective diversity. Effect strongest for LESS CREATIVE writers.

**Bastani et al. (2025)** — *PNAS*. 119 citations.
DOI: 10.1073/pnas.2422633122. AI tutoring (hints) helps. AI answers (solutions)
harms — persistently, even after AI removed.

**Lee et al. (2022)** — "CoAuthor" *CHI*. 334 citations.
DOI: 10.1145/3491102.3502030. Optimal strategy is SELECTIVE acceptance.

**Boussioux et al. (2024)** — *Org Science*. 256 citations.
DOI: 10.1287/orsc.2023.18430. AI best as collaborator generating diverse
alternatives.

**Melumad & Yun (2025)** — *PNAS Nexus*. 27 citations.
DOI: 10.1093/pnasnexus/pgaf316. LLM summaries produce shallower knowledge.
Moderated by PRIOR KNOWLEDGE.

## OpenAlex retrieval patterns (proven)

```
# OpenAlex: cross-disciplinary, no rate limit, free
curl -s "https://api.openalex.org/works?filter=title.search:QUERY&per-page=3&sort=cited_by_count:desc"
curl -s "https://api.openalex.org/works/doi:10.xxxx/xxxxx"

# Abstracts stored as inverted indexes — reconstruct to plain text
# Semantic Scholar: rate-limited (429 after 2-3 calls), use delay=4s
# arXiv API: for CS/physics/math papers
```

## Key references table (verified OpenAlex 2026-08-10)

| Researcher(s) | Year | Cites | DOI |
|---|---|---|---|
| Flower & Hayes | 1981 | 3512 | 10.2307/356600 |
| Sommers | 1980 | 753 | 10.2307/356588 |
| Kellogg | 2008 | 839 | 10.17239/jowr-2008.01.01.1 |
| Flower et al. | 1986 | 376 | 10.2307/357381 |
| Toulmin | 1958 | 5618 | 10.1017/cbo9780511840005 |
| Walton et al. | 2008 | 1351 | — |
| Osborne et al. | 2004 | 1540 | 10.1002/tea.20035 |
| Liberati et al. | 2009 | 28000 | 10.1371/journal.pmed.1000100 |
| Booth et al. | 1995 | 458 | — |
| Doshi & Hauser | 2024 | 599 | 10.1126/sciadv.adn5290 |
| Bastani et al. | 2025 | 119 | 10.1073/pnas.2422633122 |
| Lee et al. | 2022 | 334 | 10.1145/3491102.3502030 |
| Boussioux et al. | 2024 | 256 | 10.1287/orsc.2023.18430 |
| Melumad & Yun | 2025 | 27 | 10.1093/pnasnexus/pgaf316 |
