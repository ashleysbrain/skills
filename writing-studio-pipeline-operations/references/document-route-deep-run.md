# Document-route deep run (manual unified pipeline)

When `POST /api/drafts/document` cannot compose a large payload (skeleton/placeholder
drafts, `degraded_deterministic`), drive the same organs directly and keep the
lineage: same engine, same panel seats, same Bell render — only the wrapper is
replaced, with the compose step split in two.

## 1. Split-pass compose

```python
sys.path.insert(0, '<workspace>/agent-organism/ds-wernicke-engine/src')
from wernicke.core.semantic_network import generate_technical_document
mid = len(outline)//2
for o_half, ff in ((outline[:mid], findings[:len(findings)//2]),
                   (outline[mid:], findings[len(findings)//2:])):
    r = generate_technical_document(topic, question, audience,
        outline=o_half, sources=ALL_SOURCES,   # full list both passes
        context={'key_findings': ff, 'gaps': gaps, 'architecture_claims': []},
        voice_def={'label': 'internal', 'badge': 'b'})
    sections += r['sections']          # pass 0 also gives headline/subtitle
```

- Each pass must stay small enough to finish < 60s (the provider clamp);
  ~35-55s per half is normal.
- Verify before proceeding: zero `(composed from supplied context)` substrings,
  section bodies are prose (1k+ chars), not digest echoes.
- Panel revision rounds: feed `comment_agent.panel_failure_manifest(panel)` back
  as `context['revise_instructions']` with `prior_sections`, re-running the same
  split passes; cap at 3 revisions (pipeline contract).
- Guard the revision re-compose for None. Revision payloads GROW (prior_sections
  + revise_instructions can push past the provider clamp the first pass fit
  under) — on a None return keep the prior sections and flag the missed revision
  in the run log; letting the exception crash the chain kills a run whose
  earlier stages were already good.
- Voice constraint lives IN the spine: `question` (and `topic`) must carry
  "Write in first-person singular (I/my) throughout. Never we/our." — the
  generator defaults to committee voice on multi-source prompts and the voice
  seat REVISEs on any we/our. Verify the stitch before gating: regex-count
  `\bwe\b|\bour\b|\bus\b` (want 0) against `\bI\b|\bmy\b|\bme\b`.
- The spine itself is a versioned JSON in scratch; split-compose, the panel
  runner, and the design pass all `json.load` the SAME file. Never restate the
  directive inline in a stage script — rounds drift apart silently.

## 2. Bell render payload contract (:port/v1/render)

```python
{'title': headline, 'subtitle': subtitle, 'sections': sections,
 'palette': {'secondary': '#f5c518', 'accent': '#f5c518', 'teal': '#f5c518',
             'font_family': 'Manrope', 'font_display': 'Sora', 'font_mono': 'Manrope'},
 'theme': 'da_vinci', 'doc_type': 'report', 'brand_name': 'Divinity Science'}
```
Wrong shape (e.g. `headline` key, missing `brand_name`) returns `pdf_error: None`
with HTTP 200 — a contract error, not an engine failure.

## 2b. Design pass via `html_override` (when the default template fails the seat)

Bell's RenderRequest carries `html_override: str` — full art-directed HTML
rendered verbatim (the specialist engine lane). Build the HTML to the design seat's probes:

| probe | passes when |
|---|---|
| phi-structure-declared | HTML contains `1.618` or `61.8` or `phi` |
| phi-column-layout | `flex` AND (`61.8%` or `38.2%` or `grid`) |
| figures-present-svg | `count('<svg') >= 3` |
| callouts-sidebars-takeaways | `callout` AND (`takeaway` OR `sidebar` OR `key-takeaway`) |
| clickable-citations | an `href="https://doi.org/` or `href="https://arxiv.org/` |
| paragraph-walls | no `<p>` body text over 900 chars (hard-wrap long paragraphs into <850-char sentence chunks) |

- Figures must be REAL content (a levels stack, a dispute timeline, a data
  swing), not decorative arcs — the seat's LLM judgement reads past box-ticking.
- Every figure caption must be UNIQUE and name its own source with a verified
  canonical link for THAT source (resolve each doi.org/arxiv.org URL
  individually) — a shared caption across figures, or one arXiv link standing
  in for every reference, fails the seat's traceability read. Name the section
  the figure summarizes when the figure condenses a specific passage.
- Truncation checks measure element text length, never substring presence —
  grepping the whole HTML for a suspected cut phrase hits unrelated body prose
  and reports false truncations.
- Callout/takeaway cards: build one per section from that section's OWN
  closing line, capped ~420 chars by splitting at sentence boundaries — never
  mid-word. The two failure shapes the seat catches are shared hand-written
  callout text reused across sections and mid-word truncations; deriving each
  card from its section keeps them unique and complete by construction.
- Map figures/callouts to sections by substring match on the heading; exact-key
  dicts drop every figure when compose output headings drift from the outline.
- After EVERY edit to the design builder, re-run it and count the probes in the
  EMITTED HTML (svg count, callout count, arxiv/doi links, paragraphs over 900)
  — a patch can apply cleanly to the script while a figure never reaches the
  artifact (dict key never matched, insertion landed inside a quoted block).
  Verify the artifact's counts, not the script text.
- Keep every section's paragraphs under 900 chars at build time (split on
  sentences), or the walls probe fails on honest prose. Split on SENTENCE
  boundaries at ~540 chars — splitting only on blank-line seams leaves
  single-block paragraphs untouched, and most long paragraphs contain no
  paragraph break to split on.
- Target ~620-char paragraphs (about 8 rendered lines) even though the wall
  probe only hard-fails at 900: the seat's LLM judgement flags visual walls
  below the deterministic threshold.

## 3. run_panel manual invocation

- Read the canonical values from pipeline_api.py: `_DOC_VOICE_STANDARD` and
  `_DOC_VOICE_EXEMPLAR` (first-person organism-author standard; exemplar is a
  measurement-discipline passage). Both are REQUIRED — None crashes
  `seat_voice_checker` (`exemplar[:2000]` TypeError).
- `design_html=` must be the Bell-rendered HTML string or the design seat
  auto-REJECTS (fail-closed).
- `artifact_kind='document'`, `author='the specialist engine'`, `ground_truth=` verified
  architecture claims only.
- `source_text` (what the fact seat verifies against) uses [:1200]-char source
  abstracts, same as the pipeline; [:400] truncation makes supported claims fail
  UNSUPPORTED with an empty quote. Claims living in the paper BODY verify EMPTY
  against abstract-only `source_text` — extract verbatim body passages (strip
  markdown link syntax to plain text first), save them to a quotes JSON, and
  append them to `source_text` as labeled quotes so the seat can see the support.
  Absence-claims ('the paper never…', 'does not model…') have no quotable
  support by nature: reframe as the author's first-person observation rather
  than a paper-attributed claim, or the seat fails them every round.
  Seat verdicts come back in `panel['seats']` as
  `{seat, verdict, notes, evidence[]}` — fact-checker is majority-of-3 draws;
  read the failing seat's evidence list before deciding input-fix vs defect.

## 4. Studio stores map (where things actually live)

- `writing-studio/drafts.db` — table `drafts`: NO `status` column; state is
  `stage` + `review_state`; panel results live in the `metadata` JSON
  (`panel_unanimous`, `panel_seats`), NOT in the custody file.
- Registering a delivered draft by direct INSERT into `drafts`: the table
  accepts a NULL `id` silently and nothing errors — set `id` explicitly in the
  INSERT, or mint one (`str(uuid.uuid4())[:13]`) via UPDATE immediately after;
  a NULL-id row is invisible to every later lookup-by-id and custody reference.
- Custody JSON (next to the Bell PDF) carries organs chain + citation_qa only.
- `writing-studio/research_scans.db` — `scan_topics`, `scan_results`;
  `POST /api/scan` does not exist (404). Register by direct idempotent INSERT:
  check `scan_results WHERE topic_id=? AND url=?` before insert, keying rows
  `sr-<sha1(topic_id+url)[:12]>`.
- Drafts.db reads under load: open with `mode=ro` URI + `busy_timeout=60000`.

## 5. Verification checklist before delivering

1. Draft content length + placeholder count = 0.
2. `panel_unanimous` from the LAST panel round (non-unanimous = iterate, do not
   deliver 'with warnings' unless the principal accepts that state). Re-read the
   verdict JSON fresh at every run completion — seat evidence carried in from an
   earlier round belongs to that round and misdirects the next repair.
3. `citation_qa.all_verified: true` in custody; every source URL fetched live this
   session (register in research_scans.db with notes).
4. Contested-science claims carry the dispute, not a verdict.
5. PDF opens at `pdf_path`; custody JSON written next to it.
