# Advanced Capabilities Gaps (Round 3 Audit)

Verified gap analysis of 10 advanced capabilities that leading research systems
provide but the 11-stage architecture does NOT. Each entry: (1) what it is,
(2) whether we have it, (3) what others do, (4) whether we need it, (5) how to
add it. All citations verified against Crossref (with live citation counts) or
arXiv abstracts on 2026-08-10.

This is the knowledge bank behind a proposed architecture expansion (Stages 6.5,
10.5, 11, and overlays). It does not change the current 11-stage spec; it
documents what the next design round must address.

## Proposed New Stages (synthesis of the 10 gaps)

| New Stage | Covers gaps | Placement |
|---|---|---|
| Stage 6.5 Computational Artifact Bind | reproducibility, figures | after Stage 6 drafting, before Stage 8 |
| Stage 6.5 Figure Generation + QA | figures | (same insertion point, parallel to artifact bind) |
| Stage 5.1 Venue Rubric Overlay | peer-review rubrics | runs as additional pass after Stage 5 personas |
| Stage 0.5 Pre-Registration (OPTIONAL) | pre-registration | branch off Stage 0, only for confirmatory empirical |
| Stage 10 Open-Science Compliance Gate | FAIR/ORCID/OA/TOP | gate inside Stage 10, HARD FAIL per §9.2 |
| Stage 10 Multi-Artifact Package | supplementary materials | expands Stage 10 from one doc to a manifest |
| Stage 10.5 Submission Connector Layer | external integrations | write-side adapters, post-package |
| Stage 11 Post-Submission Lifecycle | post-publication, versioning | new terminal stage |

---

## Gap 1 — Reproducibility & Computational Notebooks

- **HAVE IT:** NO. CRUCIBLE §16.2 has a "Reproducibility Gate" but it only
  checks whether spec claims are *testable* (Popperian falsifiability), NOT
  executable computational reproducibility. VERITAS emits prose LaTeX/PDF only.
- **OTHERS DO:** Curvenote (live-verified) is a "Scientific Content Management
  System" making data/methods/models "modular components" that "carry their
  source history." Jupyter = "a publishing format for reproducible computational
  workflows" (Kluyver 2016, **524 cites**). Sandve et al. 2013 "Ten Simple
  Rules for Reproducible Computational Research" PLoS Comp Bio
  (**674 cites**, 10.1371/journal.pcbi.1003285) is the canonical checklist.
  Open Science Collaboration 2015, Science (**5,454 cites**,
  10.1126/science.aac4716) made reproducibility a field-defining crisis.
- **NEED IT:** YES — first reviewer question for any quantitative paper is "can
  I reproduce this number." Prose-only fails FAIR/reproducibility norms; this is
  the same risk class as POP-011 (surface validity trap).
- **HOW:** Add **Stage 6.5 Computational Artifact Bind** — every quantitative
  claim bound to an executable cell (notebook hash + dataset DOI + commit SHA);
  Stage 10 emits a computational appendix (Jupyter/Quarto/Curvenote) alongside
  the PDF. Gate fails if any cited number lacks provenance binding. Ground in
  Sandve 2013 + Wilkinson 2016 FAIR "Reusable" principle.

## Gap 2 — Peer Review Rubrics

- **HAVE IT:** PARTIAL. Stage 5's 8/11-seat panel are *personas* grounded in
  argumentation theory (Popper, Kahneman, Walton, Toulmin) — NOT mapped to real
  journal reviewer rubrics. Only PRISMA is touched, only at Stage 10, only for
  systematic reviews. No Nature reporting-summary check, no NeurIPS
  reproducibility checklist, no ICML soundness/significance/contribution grid.
- **OTHERS DO:** **RubricReviewer** (arXiv 2608.00005, 2026) makes rubric
  generation an *explicit intermediate step* so review + final assessment are
  conditioned on paper-adaptive rubrics. **PeeriScope** (arXiv 2604.24071,
  2026) is a "rubric-guided LLM assessment" platform with a public API. Nature
  mandates a reporting-summary PDF (live-verified, 1.6MB). ICML/NeurIPS use a
  1–10 soundness/significance/contribution/confidence grid via OpenReview.
- **NEED IT:** YES — a paper that survives our persona panel can still fail real
  review on rubric items we never test (data availability, ethics, statistical
  rigor, figure quality).
- **HOW:** Add **Stage 5.1 Venue Rubric Overlay** — per-target-venue criteria
  grid (Nature / NeurIPS / ICML / PRISMA) applied as an additional deterministic
  pass over persona findings; each item pass/fail/pass-with-caveat independent of
  personas. Design pattern: RubricReviewer's "explicit rubric as intermediate
  artifact."

## Gap 3 — Data Visualization & Figure Generation

- **HAVE IT:** NO. Zero figure-generation capability. Only mentions: "Is Figure 1
  compelling?" (audience sim) and "visual palette" (the specialist engine/the specialist engine =
  render/typography aesthetics, not data-viz). Stage 6 drafts prose; no figure
  stage.
- **OTHERS DO:** Rougier et al. 2014 "Ten Simple Rules for Better Figures" PLoS
  Comp Bio (**102 cites**) — canonical figure-quality rubric. Weissgerber et al.
  2015 "Beyond Bar and Line Graphs" PLOS Biology (**588 cites**) — most papers
  hide raw data behind bar charts. Wilkinson "Grammar of Graphics" 1999
  (**182 cites**) underpins ggplot/Plotly. Mercury = notebooks → interactive
  dashboards. Datawrapper = no-code charts.
- **NEED IT:** YES, critically — the single largest functional hole. A paper
  without figures is not submittable.
- **HOW:** Add **Stage 6.5 Figure Generation** — per quantitative claim, generate
  figure spec (type chosen via Weissgerber "show raw data" rule + Rougier
  rules), execute via matplotlib/Plotly, store figure+source-data+gen-code as a
  bound triple. Add a **Figure QA gate** (axes/legend/colorblind/dual-axis/
  raw-data-shown) before Stage 8. Ground in Rougier 2014 + Weissgerber 2015.

## Gap 4 — Supplementary Materials & Appendices

- **HAVE IT:** NO. Stage 10 emits single-document formats. No SI document, no
  code-repo packaging, no data-deposit linkage, no extended-methods appendix, no
  cover letter.
- **OTHERS DO:** PLOS ONE (live-verified) has a full "Supporting Information" +
  "Data Availability" + "Code Sharing" policy. Nature/Cell require SI as a
  separate edited document. TOP guidelines + FAIR require code in a citable repo
  (Zenodo/GitHub+DOI) and data in a domain repository.
- **NEED IT:** YES — most journals reject main-text-only submissions.
- **HOW:** Extend Stage 10 into **Multi-Artifact Package Assembly** —
  manifest-driven emitter: (a) main text, (b) SI (auto-split when over limits),
  (c) code repo (from Stage 6.5 bindings, CITATION.cff + Zenodo DOI),
  (d) data-deposit manifest with repository DOIs, (e) cover letter +
  reviewer-response template.

## Gap 5 — Pre-Registration & Hypothesis Registration

- **HAVE IT:** NO. Stage 0 "Evidence Gate" is a *pre-writing* filter, not
  hypothesis pre-registration. No Stage-1-acceptance workflow, no frozen analysis
  plan, no confirmatory/exploratory distinction.
- **OTHERS DO:** COS/OSF (live-verified) — preregistration "distinguishes planned
  from unplanned work." Nosek 2018 "The Preregistration Revolution" PNAS
  (**1,437 cites**, 10.1073/pnas.1708274114). Registered Reports format conducts
  peer review *before* data collection; provisionally accepts high-quality
  protocols.
- **NEED IT:** CONDITIONAL — not for theory/CRUCIBLE, but YES for any empirical
  VERITAS paper in psychology/medicine/social science (increasingly mandatory).
  Without it we cannot support Registered Reports submissions.
- **HOW:** Add **optional Stage 0.5 Pre-Registration** branch — if
  empirical-confirmatory, freeze a timestamped analysis plan (hypotheses +
  outcomes + analysis + sample size + exclusion rules) to OSF before Stage 2;
  mark every downstream claim confirmatory (matches plan) or exploratory
  (deviation). Registered-Reports mode: Stage 5 panel runs on the *protocol* for
  in-principle acceptance before results. Ground in Nosek 2018.

## Gap 6 — Post-Publication Lifecycle

- **HAVE IT:** NO. Architecture explicitly terminates at Stage 10. No Stage 11.
- **OTHERS DO:** Altmetric/Priem track post-pub attention. OpenAlex/Crossref
  expose citation counts over time. PubPeer/F1000 provide post-publication peer
  review. bioRxiv tracks preprint revisions (Abdill 2021 "Over and Over: Preprint
  revisions on bioRxiv"). McNutt 2014 "Reproducibility" Science (**244 cites**,
  10.1126/science.1250475).
- **NEED IT:** YES — the common real workflow is submit → reviews → revise →
  resubmit; our pipeline has no representation, so every revision is a manual
  cold restart.
- **HOW:** Add **Stage 11 Post-Submission Lifecycle**, three sub-modes:
  (a) REVISION — ingest reviewer comments as a structured payload, map each to a
  Stage-8 finding, re-run affected stages (reuses existing §8 feedback-loop
  mechanics); (b) MONITORING — poll OpenAlex/Crossref for citations, Altmetric
  for attention; (c) CORRECTION — erratum via constrained Stage-6 pass.

## Gap 7 — Multi-Lingual & Translation

- **HAVE IT:** NO. "Translation"/"multilingual" appears nowhere in 1,253 lines.
- **OTHERS DO:** DeepL Pro + LLMs handle academic translation; Crossref 2026
  hits compare "ChatGPT vs. DeepL vs. Google Translate" for academic
  multiword-expression quality.
- **NEED IT:** LOW priority — relevant only for non-English venues or bilingual
  publications. Phase-3 nicety, not a Phase-1 gap.
- **HOW (if needed):** Optional **Stage 10b Translation Pass** — run finalized
  English draft through domain-calibrated translation model, then re-run
  Stage 7 audience sim + Stage 8 L3 sentence revision *in the target language*
  to preserve academic register. Bastani Boundary (P6) still requires a
  human fluent in the target language at Stage 9.

## Gap 8 — Accessibility & Open Science

- **HAVE IT:** NO. FAIR, ORCID, open-access, TOP all absent. Stage 2 *reads* open
  APIs but enforces no open-science *output* requirements.
- **OTHERS DO:** Wilkinson 2016 FAIR Guiding Principles, Scientific Data
  (**14,670 cites** — most-cited paper in the entire analysis,
  10.1038/sdata.2016.18) defines the data standard. ORCID = universal author ID.
  TOP guidelines tier compliance. Plan S mandates open access. OSF/Zenodo/Figshare
  provide deposit infra.
- **NEED IT:** YES — increasingly *legally mandatory* (Plan S, funder policies).
  Non-deployable for grant-funded research without it.
- **HOW:** Add **Stage 10 Open-Science Compliance Gate** — checklist: datasets
  have DOI+license+repo (FAIR F1/A1/R1); all authors have ORCID; license is
  CC-BY (or funder-specified); code in DOI'd repo; TOP-tier self-assessment
  attached. HARD FAIL per §9.2 if any funder-mandated item missing.

## Gap 9 — Versioning & Reproducible Versions

- **HAVE IT:** PARTIAL/NO. Architecture versions *internal artifacts*
  (schema_version on contracts, versioned Toulmin skeletons for audit) but NO
  paper-level version lifecycle. No "this is V2 responding to Reviewer 2" state,
  no diff V1→V2, no comment-to-change mapping.
- **OTHERS DO:** arXiv/bioRxiv keep every version (v1, v2…) with public diffs.
  OpenReview tracks all rebuttal/revision rounds. Conference versioning is
  explicit (submission → rebuttal → camera-ready). Crossref supports
  version-of relationships.
- **NEED IT:** YES — without it every reviewer-driven revision is a stateless
  manual rewrite, losing the audit trail of *what changed and why* (which
  reviewers demand). Connects to existing gap M5 "Revision Tracking" in the
  VERITAS roadmap.
- **HOW:** Add **paper_version field** to top-level run state; on each
  Stage 11-REVISION entry, snapshot prior version, compute structural diff
  (section/paragraph/claim-level), emit a **response-to-reviewers document**
  auto-mapping each comment → revised passage (by ref_id) → diff hunk. Ground in
  OpenReview/arXiv conventions.

## Gap 10 — External Service Integrations

- **HAVE IT:** NO (read-only). Stage 2 *reads* arXiv/Crossref/OpenAlex. ZERO
  write integrations; Stage 10 "submission" = human manual upload.
- **OTHERS DO / API STATUS (all live-verified 2026-08-10):**
  - **Crossref deposit API** — available for DOI registration + metadata deposit.
  - **bioRxiv API** — `api.biorxiv.org/details/biorxiv/{from}/{to}/{cursor}/json`
    WORKS (returns JSON of preprint metadata/revisions). Read-side.
  - **arXiv submission** — MANUAL TeX upload via web form. **No public
    auto-submit API.** Do not promise automated arXiv submission; generate the
    TeX bundle + fill the web-form fields, human clicks submit.
  - **OpenReview API** — auth-gated (HTTP 403 without venue credentials). Needs
    a per-venue token.
  - **Zenodo** — REST API for data+code deposit (mints DOI).
  - **ORCID** — work-add via OAuth.
- **NEED IT:** YES for an elite pipeline — auto-deposit of DOIs/data and
  one-click preprint submission eliminate the highest-friction manual steps.
- **HOW:** Add **Stage 10.5 Submission Connector Layer** with adapters: Crossref
  DOI deposit (metadata XML), Zenodo data+code deposit (REST), bioRxiv metadata
  prefetch (read API), ORCID work-add (OAuth), OpenReview submission
  (auth-gated, needs venue token). arXiv = manual-assist. Each adapter is a thin
  wrapper over a verified endpoint; failures degrade gracefully (manual queue)
  per existing §4.6 crash-recovery pattern.

---

## Research Technique: Open Scholarly APIs for Citation Verification

When full web tooling (web_search / web_extract) is unavailable, scholarly
verification can still be done by direct HTTP to these permanently-open APIs
(no key required). This is a reusable research pattern, not a workaround for a
specific outage.

- **Crossref REST API** (`api.crossref.org/works?query=…&rows=N`) — paper search
  with `is-referenced-by-count` (live citation count). For single-work DOI
  lookup use `/works/{doi}` — NOTE: the `select` parameter is **not allowed** on
  single-work lookups (returns validation-failure); drop it. Rate limit: back
  off on HTTP 429 (polite pool ~50 req/min, add `mailto` in User-Agent for the
  polite pool). Always pass a descriptive `User-Agent`.
- **arXiv export API** (`export.arxiv.org/api/query?search_query=…&max_results=N`)
  — returns Atom XML; parse `<entry>`, `<title>`, `<id>`, `<summary>`,
  `<published>`. Use HTTPS. Good for recent-paper abstracts and verifying
  arXiv IDs.
- **bioRxiv/medRxiv API** (`api.biorxiv.org/details/{server}/{from}/{to}/{cursor}/json`)
  — JSON, no auth. `{server}` = `biorxiv` or `medrxiv`. Dates must be
  `yyyy-mm-dd`.
- **Direct page fetch** for journal guidelines (Nature, PLOS) — many render
  server-side; strip `<script>`/`<style>` tags then unescape HTML. Some
  (science.org, nips.cc current paths) return 403/404 — these are JS-gated;
  note the failure and fall back to API data or skip, do not assume the content
  doesn't exist.

Verification protocol for any claim grounding the architecture:
1. Resolve the DOI via Crossref `/works/{doi}` → confirm title, authors, year,
   container, and capture `is-referenced-by-count`.
2. For arXiv-only work, fetch the abstract via the export API and cite the ID.
3. Record the citation count in the traceability matrix alongside the paper —
   this is how the architecture earns the "literature-grounded" label.
