# Cross-Disciplinary Research Discovery & Knowledge Mapping Tools

Condensed knowledge bank compiled from primary-source research (tool homepages,
pricing pages, Wikipedia, OpenAlex docs, Scite/S2 API pages, and comparison
articles from tesify.app and ponder.ing). Researched August 2026.

Use this as a starting reference when researching academic research-discovery
tools, competitive analysis in the scholarly-search space, or when building a
tool that bridges disciplines. **Re-verify pricing before citing** — SaaS
pricing changes; this snapshot is from 2026-08.

## Market structure — four tiers

| Tier | What it does | Examples |
|------|-------------|----------|
| A. Literature Mapping (visual citation graphs) | Seed paper → visual network | Connected Papers, ResearchRabbit, Litmaps, Inciteful, Open Knowledge Maps |
| B. AI Search & Synthesis | Query → ranked papers / answers | Semantic Scholar, Elicit, Consensus, Scite, Iris.ai, Paper Digest, Scinapse, AMiner |
| C. Bibliometric Network Analysis (desktop) | Build networks from your own data | VOSviewer, Cytoscape, Gephi |
| D. Open Data Infrastructure / APIs | The citation graphs everything else runs on | OpenAlex, Semantic Scholar API, Lens.org |

**Key insight:** Tier C tools are *empty canvases* (powerful viz, you bring
data). Tier A tools are *pre-populated* (citation graphs included, but
closed/paid). This is why researchers gravitate to Tier A despite Tier C being
more analytically powerful.

## Tier A — Literature Mapping (the "Connected Papers" category)

- **Connected Papers** (connectedpapers.com): single seed → force-directed
  co-citation similarity graph. Prior Works + Derivative Works panels. Semantic
  Scholar data. 5 free graphs/mo; ~$6/mo unlimited. Single-seed only, no
  alerts, no Zotero, no time-axis. Best for quick visual orientation.
- **ResearchRabbit** (researchrabbit.ai): multi-seed iterative citation +
  author networks, adaptive algorithms. 310M+ articles (S2). Now Litmaps-
  affiliated. Free: unlimited search, 50 seeds. RR+ $10/mo: 300 seeds. Best
  free all-rounder + team collaboration.
- **Litmaps** (litmaps.com): **temporal timeline** — field evolution across
  decades. OpenAlex + S2 + Crossref. Free: 1 map/100 articles. Pro $10/mo:
  unlimited + daily alerts. Best for ongoing monitoring / thesis-length projects.
- **Inciteful** (inciteful.xyz): **Literature Connector** — shortest citation
  path between ANY two papers. S2 + OpenAlex. Completely free, no account.
  Single-dev project. Closest existing tool to *cross-disciplinary* connection
  finding, but you must name both papers.
- **Open Knowledge Maps** (openknowledgemaps.org): AI-clustered concept bubble
  maps. Non-profit (Austria). BASE (300M docs) + PubMed + OpenAIRE. Free. Best
  for topic orientation / open-access discovery.

## Tier B — AI Search & Synthesis

- **Semantic Scholar** (semanticscholar.org): 237M+ papers, free AI search,
  TLDRs, "Highly Influential Citations", Research Feeds, Semantic Reader, free
  REST API. Allen Institute for AI. **The backbone everyone else builds on.**
  Entirely free. List-based (no visual graph).
- **Elicit** (elicit.com): structured data extraction, PRISMA systematic
  reviews, 138M+ papers, Research Reports. Free limited; Plus $11/mo; Pro
  $39/mo. NOT a visualization tool — for systematic extraction.
- **Consensus** (consensus.app): AI search for scientific consensus on a
  question. Cloudflare-gated (couldn't fetch primary). Free + ~$9/mo Premium.
- **Scite** (scite.ai): **Smart Citations** — 1.6B+ citations classified as
  supporting/contrasting/mentioning. 300M+ full-text (30+ publisher partners).
  $20/mo Basic; $50/mo Pro. No visual graphs; list/report-based. Best for
  citation credibility verification.
- **Iris.ai** (iris.ai): enterprise "AI knowledge foundation" (Axion/Neuralith/
  RSpace), compliance-focused. Enterprise sales only. ~10 years old.
- **Paper Digest** (paperdigest.org): auto literature-review paragraphs,
  notably **avoids LLMs** to prevent hallucination. Free 1 project; $9.99/mo.
- **Scinapse** (scinapse.io): R&D trend/expert discovery, mini-reviews.
  Freemium.
- **AMiner** (aminer.cn): Chinese academic platform + LLM/Zhipu integration.
  Free, China-focused.

## Tier C — Bibliometric Network Analysis (open source, bring your own data)

- **VOSviewer** (vosviewer.com): bibliometric networks (citation/co-citation/
  co-authorship/term co-occurrence). CWTS/Leiden. Free. Desktop + Online.
- **Cytoscape** (cytoscape.org): complex network analysis, bioinformatics
  origin. v3.10.3. LGPL. Bring your own data.
- **Gephi** (gephi.org): general graph viz, 10–10M nodes, community detection.
  v0.11.2. GPL+CDDL. Bring your own data.

## Tier D — Open Data Infrastructure / APIs

- **OpenAlex** (openalex.org / docs.openalex.org): 250M+ works, 256 disciplines,
  REST API, bulk snapshots. 100% free & open (CC0). **Replaced Microsoft
  Academic Graph** (MAG, shut down end of 2021). Launched Jan 2022 by
  OurResearch. The default open scholarly graph.
- **Semantic Scholar API** (api.semanticscholar.org): REST API over 237M+
  paper graph; embeddings, influence, TLDRs. Free (rate-limited).
- **Lens.org** (lens.org): **patents + 200M scholarly records**; unique
  patent↔scholarly linking. Non-profit (Cambia/Australia). Free search; paid
  API/bulk.
- **Microsoft Academic Graph**: DEFUNCT (shut down end of 2021). Successor =
  OpenAlex.

## Gap analysis — the underserved niches

1. **Cross-disciplinary serendipity (THE BIG GAP):** No tool finds the paper
   from field B that would transform work in field A. Inciteful's Connector is
   closest but only bridges 2 *named* papers. A "find structural holes between
   citation clusters" tool doesn't exist.
2. **Temporal + cross-disciplinary combined:** nothing shows how a concept
   *migrated across fields over time*.
3. **No open-source self-hostable discovery frontend:** Gephi/VOSviewer are open
   but empty; Connected Papers/Litmaps are populated but closed/paid.
4. **Personalized serendipity:** no tool combines your Zotero history + global
   graph to surface *personally unexpected* cross-domain connections.
5. **Multilingual cross-discovery:** cross-language concept bridging via graph
   structure (not translation) doesn't exist.
6. **Full-text concept mapping across disciplines:** most tools are metadata-
   level. Scite has full-text but uses it for citation classification.
7. **"Show me what I don't know to search for":** all tools are query- or
   seed-driven. None proactively surface transformative insights from outside
   your field.

## Recommended combined researcher workflow

1. Orientation: Open Knowledge Maps (concept overview) → Connected Papers
   (visual seed)
2. Deep mapping: Litmaps (temporal, multi-seed) + ResearchRabbit (iterative,
   free)
3. Cross-domain bridge: Inciteful Literature Connector
4. Verification: Scite (Smart Citations — supported?)
5. Extraction: Elicit (structured data for systematic review)
6. Monitoring: Litmaps alerts (Pro) or Semantic Scholar Research Feeds (free)
7. Infrastructure (if building): OpenAlex + Semantic Scholar API
