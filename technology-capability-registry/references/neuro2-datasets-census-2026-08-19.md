# datasets.neuro2.ai — live census + DS mappings (2026-08-19)

External tool census taken from a real browser session (principal side-stream ask:
"use this tool / its graphic — don't guess"). Facts below are verified from the
live DOM; limits are stated, nothing inferred. the OS: T-260819-0052 (closed,
census run-record); follow-on specs T-260819-0053 (gap-hunter dataset axis),
T-260819-0054 (studio 3D graph view) — both open, awaiting principal go.

## What it is (verified)

Interactive 3D force-graph of open neuroscience datasets. Authors:
Nataliya Kosmyna · Eugene Hauptmann (MIT). SvelteKit app, JS-rendered
(skeleton HTML only — curl alone shows nothing; use a browser).

## Census numbers (from live page header)

- 13,255 datasets · 42 modalities · 41,102 authors · 143,724 subjects
- 123K hours (measured) · 526.7 TB total size

## Node kinds + search grammar (from live controls)

Node kinds: Datasets, Repos, GitHub users, Authors, Papers, Tasks, Institutions,
Funders, Licenses. Search scopes: Datasets / Repos / GitHub users / Authors /
Papers / All; fields: Name, Description, Authors, Institution, Funder, Task,
Modality, License, Year, Subjects, Size, Hours, Channels; modes: Text, Fuzzy,
Regex, Semantic.

Query grammar examples shown in-UI: `motor imagery (semantic)`,
`sleep staging (semantic)`, `name: resting state`, `fuzzy: parkinsn`,
`regex: epilep(sy|tic)`, `author: Obleser`, `institution: Stanford`,
`funder: NIH`, `task: n-back`, `modality: ieeg`, `license: CC0`,
`subjects > 200`, `year 2020..2023`, `size > 5GB`, `hours > 100`,
`channels 64..256`, `repo: eeg`, `repo: fmri`.

Labeling interaction worth borrowing: tick a node kind → every node of that
kind labelled, best-connected first, as many as the screen fits.

## Honest limits (verified, not assumed)

- ⤓ download button is LOGIN-WALLED — no bulk export available to us.
- Graph data endpoint not in the public page bundle (runtime-fetched, auth-gated).
- Data provenance (which archives) not verifiable without login.
- Repo openness/licensing unknown — do not claim open-source without checking.

## Grounded DS mappings (delivered to principal 2026-08-19)

1. **Gap-hunter dataset axis** (T-260819-0053): papers-hot/data-zero =
   methodological gap; data-exists/no-papers = theory gap. Both mint as tasks.
2. **Research Library cross-reference**: we index papers (arXiv/OpenAlex); this
   indexes datasets — the paper→dataset relation is missing from our library.
   Course production gains real scale citations with query links.
3. **3D force-graph genre for Research Studio** (T-260819-0054): same tech family
   as our 3d-process-flow-graph skill; point it at OUR corpus (papers, engines,
   personas), DS-branded (navy/gold, Manrope/Sora). Steal the label-by-kind
   interaction, not their data.
4. **8D health feature grounding** (research direction ONLY): sleep staging /
   motor imagery / resting-state datasets could ground normative ranges
   (e.g., sleep architecture). 8D is verified-only — nothing enters scoring
   without principal settle + source-grade checks.

## Census technique notes (for registry work)

- SPA + 3D canvas hammers the main thread: `js("document.body.innerText...")`
  can time out mid-render — retry smaller expressions or read after settle.
- SvelteKit skeleton returns 200 HTML for ANY path (data.json, api/datasets all
  return index.html) — endpoint probing is useless; read rendered DOM state.
- No public API: census numbers/grammar must come from the live page text.
