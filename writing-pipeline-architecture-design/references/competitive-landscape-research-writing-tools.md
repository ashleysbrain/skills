# Competitive Landscape: Research & Writing Tools

Condensed knowledge bank from a systematic landscape review (Aug 2026) of 25+
real products. Use to benchmark VERITAS/CRUCIBLE against the market, prioritize
gap work, and avoid re-implementing what existing tools already do well.

This is the **external competitive view** — complementing
`advanced-capabilities-gaps.md` (the internal audit). Several gaps overlap; the
value here is seeing *which real product exposes each gap* and *what they get
right*.

## Categories Covered
1. AI-native academic writing (Elicit, Jenni, Writefull, Paperpal, Scite, Consensus)
2. Research automation (Covidence, Rayyan, DistillerSR, Nested Knowledge, Elicit SR)
3. Literature mapping (Connected Papers, Litmaps, Inciteful, Research Rabbit)
4. AI research agents (Stanford STORM, Co-STORM, GPT-Researcher)
5. Collaborative writing (Overleaf, Curvenote, Authorea)
6. Reference/knowledge management (Zotero, Obsidian, Roam, Logseq, Notion)

## What The Landscape Gets Right (Pipeline Should Learn From)
- **PRISMA compliance** (Elicit, Covidence): systematic-review methodology is
  the gold standard. Elicit validated at 95% recall / 97% abstract / 99%
  full-text / 96% extraction across 994 Cochrane reviews. Stage 2 should
  optionally support PRISMA-grade workflows.
- **Smart Citations** (Scite): classifies every citation as supporting /
  contrasting / mentioning. 1.6B+ Smart Citations across 300M+ articles, 30+
  publisher partnerships (Wiley, SAGE). We gather papers but never assess
  citation *context* — a real epistemological gap.
- **Source-grounded writing** (Jenni AI): every AI-generated claim traceable
  inline to a source PDF. Should be mandatory in Stage 6 drafting.
- **Multi-agent writing roles** (GPT-Researcher): 8 specialized agents — Chief
  Editor, Researcher, Editor, Reviewer, Revisor, Writer, Publisher, Human — with
  defined handoffs via LangGraph. Validates our panel approach; shows we need
  specialized roles in the *writing* stage (6/8), not just review (5).
- **Multi-perspective research** (STORM, arXiv:2402.14207): multiple agents
  research from different stakeholder viewpoints, then synthesize. Broader
  coverage than single-pass search. Key STORM innovation — adopt for Stage 2.
- **Citation network analysis** (Connected Papers, Litmaps): co-citation +
  bibliographic coupling find related work semantic search misses.
- **Living monitoring** (Litmaps, Scite Collections): alerts when new papers
  cite your evidence base — essential for keeping research current.
- **Modular components** (Curvenote): figures/datasets/methods as reusable,
  DOI'd, version-controlled building blocks via MyST + Jupyter + GitHub.

## What No Tool Does (Our Genuine Differentiators)
- **Toulmin argumentation** (claim-data-warrant-backing-qualifier-rebuttal) — our Stage 3
- **Audience simulation** (expert/practitioner/skeptic/novice) — our Stage 7
- **Anti-homogenization** (detect/remediate generic AI voice) — our Stage 9 gate
- **Confidence scoring** on claims/arguments (Elicit scores extraction accuracy, not argument strength)
- **Cross-paper learning** (no tool learns from prior papers to improve the next)
- **Physics-based validation** (free energy, Kuramoto, critical slowing, Bayesian) — our Stage 4
- **Structured adversarial panel** (Popper, Kahneman, Wernicke, Luria, Goethe,
  Bell, Harvey). GPT-Researcher's Reviewer and STORM's multi-perspective are
  shallower analogues.

## Top 10 Gaps Exposed By This Review (with exposing product)
1. No citation network analysis — co-citation, bibliographic coupling, temporal
   maps (Connected Papers, Litmaps, Inciteful)
2. No smart citation context — supporting/contrasting classification (Scite)
3. No PRISMA-compliant systematic-review mode (Elicit, Covidence)
4. No persistent knowledge base — amnesiac per run; no bidirectional
   claim/evidence links (Zotero, Obsidian)
5. No multi-perspective research gathering — single-pass search only (STORM)
6. No human-in-the-loop steering / interactive checkpoints (Co-STORM)
7. No section-specific handling — intro/methods/results/discussion need
   different criteria (real lab workflows: MIT CSAIL, Stanford AI Lab, DeepMind)
8. No reproducibility enforcement — code/data/experimental-detail checks (DeepMind)
9. No rebuttal phase — can't respond to peer review (all real workflows)
10. No multi-format academic output — no LaTeX, no journal/conference templates
    (Overleaf)

## Key Tool Snapshots (what / gets-right / gets-wrong)
- **Elicit** — semantic search 138M papers + 545K trials; PRISMA 2020 SR module
  (screens 5k–40k papers); Research Agent (cited artifacts); API v2 + MCP server.
  No writing/drafting/argumentation. $11–89/mo. Life-sciences-biased.
- **Jenni AI** — inline source-grounded autocomplete + PDF chat (up to 1000pp).
  Sentence-level only; no argumentation, no revision stages. $12–29/mo.
- **Scite.ai** — Smart Citations on 1.6B+ citations; full-text search via 30+
  publisher agreements; reference check w/ retraction flagging; MCP server.
  Discovery only, no writing. STM-biased.
- **Paperpal** — search→write→submit pipeline; plagiarism + AI-detection +
  reference-hallucination checks; 1,500+ journals trust (Cactus, 24yr).
  No argumentation, no multi-draft.
- **Writefull** — language models trained on journal articles; Overleaf/Word
  plugins; Title/Abstract/TeXGPT widgets. Surface-level only. 1500+ institutions.
- **Consensus** — evidence synthesis (what does the literature collectively say).
  Search/synthesis only; no API/MCP.
- **Covidence** — Cochrane standard SR platform since 2015; PRISMA flow,
  multi-reviewer screening, risk-of-bias. 35% time reduction. Manual-first,
  no AI, no writing, no API. Non-profit.
- **Rayyan** — AI-assisted SR screening prioritization; free tier; mobile.
  Screening only.
- **STORM** (arXiv:2402.14207, NAACL 2024, 30.9K★) — multi-perspective
  pre-writing research → outline → Wikipedia-style article. Explicitly NOT
  publication-ready. Source bias transfer + over-association noted as problems.
- **Co-STORM** (arXiv:2408.15232, EMNLP 2024) — human-in-the-loop,
  unknown-unknowns discovery, dynamic mind map. 70% prefer over search engine.
- **GPT-Researcher** (28.9K★) — Plan-and-Solve; LangGraph multi-agent mode
  (8 roles); PDF/DOCX/MD output; Claude Skill + MCP. Web-focused, not academic.
- **Overleaf** — 25M users; real-time collaborative LaTeX; track changes; 9k+
  styles; templates; now adding AI. No argumentation, no research.
- **Curvenote** — Scientific CMS; MyST+Jupyter+GitHub; modular DOI'd components.
  Content management, not writing/research. Enterprise focus.
- **Connected Papers** — co-citation + bibliographic coupling visualization.
  JS-only, no API, discovery only.
- **Litmaps** — temporal citation maps + living monitoring. 350k researchers.
  Visualization only.
- **Research Rabbit** — Spotify-like paper recommendations; Zotero sync; free.
  1M+ researchers, 310M papers. Discovery only.
- **Zotero** — open-source reference manager; browser auto-capture; 9k+ styles;
  group libraries; plugin ecosystem. No AI, no writing, no discovery.
- **Obsidian** — local-first bidirectional-link knowledge graph; plugins.
  General-purpose, not academic-specific.

## Strategic Positioning
VERITAS/CRUCIBLE occupies a genuinely novel position: NO existing tool combines
Toulmin argumentation + physics-based validation + adversarial panel + audience
simulation + anti-homogenization + confidence scoring + cross-paper learning.
Closest competitors:
- **ELICIT** (research automation + extraction, but no writing/argumentation)
- **STORM/GPT-RESEARCHER** (multi-agent research + writing, but no academic rigor)
- **JENNI/PAPERPAL** (AI writing with citation, but no deep research/validation)

Advantage = DEPTH (physics validation, adversarial panel, argumentation theory).
Risk = BREADTH (missing citation networks, SR methodology, knowledge
persistence, collaborative interfaces).

## Data Sources (Direct HTTP via urllib; web_search/web_extract unavailable)
elicit.com (+docs,+blog), consensus.app, scite.ai (+/features,/data,/assistant),
jenni.ai (+/pricing), writefull.com (+/for-institutions), paperpal.com (+/blog),
overleaf.com (+/for/universities), curvenote.com (+/features),
connectedpapers.com, litmaps.com, inciteful.xyz, researchrabbit.ai, zotero.org,
obsidian.md, roamresearch.com, logseq.com, covidence.org (+/about),
storm.genie.stanford.edu, github.com/stanford-oval/storm (README),
github.com/assafelovic/gpt-researcher (README + multi_agents/README),
arxiv.org (2402.14207, 2408.15232, 2305.04091), notion.so/templates/research.
