---
name: publication-opportunity-discovery
description: Find publication opportunities by field via live APIs.
version: 1.0.0
category: research
---

# Publication Opportunity Discovery

Find **real, live** publication opportunities by research field. Every result comes from a verified-live API call — no training-memory hallucination.

## When to Use
- User asks "where can I publish my research on X?"
- Need to find journals, conferences, grants, or preprint servers for a field
- Want to discover non-traditional / social publication venues they didn't know existed
- Need to verify a journal is legitimate (OA status, DOI check)
- Expanding publication strategy beyond obvious venues

## The Tool

**Location:** `/<workspace>`

### CLI Usage
```bash
# Full discovery for a field
python3 research_hub/tools/publication_opportunity_discovery.py "neuroscience" "all"

# Single category
python3 research_hub/tools/publication_opportunity_discovery.py "machine learning" "conferences"
python3 research_hub/tools/publication_opportunity_discovery.py "public health" "grants"
python3 research_hub/tools/publication_opportunity_discovery.py "economics" "journals"
python3 research_hub/tools/publication_opportunity_discovery.py "psychology" "preprints"
python3 research_hub/tools/publication_opportunity_discovery.py "philosophy" "social"
```

### Python API
```python
import sys
sys.path.insert(0, "/<workspace>")
from publication_opportunity_discovery import PublicationDiscovery

pd = PublicationDiscovery()
results = pd.discover(field="neuroscience", opp_type="all")
# opp_type: "all" | "journals" | "conferences" | "preprints" | "grants" | "social"

# Check if a specific paper DOI is open access
oa = pd.check_oa_status("10.1038/nature12373")
```

## Verified API Sources (tested live 2026-08-12)

### Tier 1 — Free, no key, JSON (production-ready)
| Source | What it finds | Endpoint |
|--------|--------------|----------|
| OpenAlex | 324M works, 255K journals, 45K funders | api.openalex.org |
| DOAJ | 20K+ open-access journals by subject | doaj.org/api |
| Crossref | Journals + proceedings + funders | api.crossref.org |
| arXiv | Preprints (physics, CS, math, biology, econ) | export.arxiv.org/api |
| bioRxiv | Biology/medicine preprints | api.biorxiv.org |
| DBLP | CS conference proceedings | dblp.org/search/publ/api |
| NIH RePORTER | Active US biomedical grants (POST) | api.reporter.nih.gov |
| NSF Awards | US science grants | api.nsf.gov |
| OSF | Multidisciplinary preprints | api.osf.io |
| Europe PMC | OA papers, broad coverage | ebi.ac.uk/europepmc |
| Unpaywall | OA status check by DOI | api.unpaywall.org |
| ROR | Research institutions | api.ror.org |

### Tier 2 — Free API key needed
| Source | What it finds | How to get key |
|--------|--------------|----------------|
| Semantic Scholar | Paper search + citation graph (429 without key) | semanticscholar.org/product/api |
| Sherpa Romeo | Journal self-archiving policies | sherpa.ac.uk/romeo/apiformat.php |

### Tier 3 — Web scraping (no API, needs HTML parsing)
| Source | What it finds | Notes |
|--------|--------------|-------|
| WikiCFP | Active calls-for-papers | HTML only, needs parsing |
| SCImago SJR | Journal ranking metrics | XLS export, blocks bots (403) |
| Conference-Alerts | Conference listings | HTML scraping |

## Discovery Categories

### 1. Journals
DOAJ (OA only) + OpenAlex (all types). Shows OA status, APC cost, works count, ISSN, homepage.

### 2. Conferences
Crossref proceedings (deduped by venue) + DBLP CS conferences. Shows year, DOI, sample title.

### 3. Preprints
Field-aware: arXiv (category-mapped), bioRxiv (bio/neuro/med), OSF preprints.

### 4. Grants
NIH RePORTER (POST, active funded projects) + NSF awards + OpenAlex funders. Shows agency, amount, year.

### 5. Social/Non-traditional Venues
The "venues they may not have known existed":
- **The Conversation** — academic-to-public writing (editorial reviewed)
- **Substack** — subscription research newsletters
- **OSF Registries / AsPredicted** — preregistration
- **Figshare / Zenodo** — DOI-minting for datasets, figures, posters
- **PsyArXiv / SocArXiv / LawArXiv** — field-specific preprints
- **Europe PMC OA** — shows field OA paper count
- **Spreaker podcasts** — research communication/guest opportunities

## Pitfalls
- **NIH RePORTER text search is broken via POST API.** Criteria fields like `keywords`, `projecttitle`, `abstract` are silently ignored — all queries return 2.9M unfiltered results. Only structured filters work: `agencies` (institute codes like NINDS, NCI, NIMH), `fiscal_years`, `org_names`, `pi_names`, `project_nums`. Tool maps common fields to NIH institute codes via `NIH_AGENCY_MAP`. Unmapped fields skip NIH entirely to avoid returning misleading results.
- **OpenAlex funders endpoint: `grants_count` and `works_count` are NOT valid `select` fields.** Valid select fields: `id, display_name, homepage_url, description, country_code, alternate_titles`. Using invalid select fields returns HTTP 400.
- **Source diversity: without capping, one source fills the entire limit.** Tool uses `per_source = limit // 3` to ensure NIH, NSF, and OpenAlex all appear in grant results.
- **Semantic Scholar returns 429 without API key.** Add key for volume queries.
- **bioRxiv total can be string or int.** Tool handles both via int() coercion.
- **OpenAlex renamed "venues" to "sources".** Use `/sources` endpoint.
- **Crossref proceedings have duplicate venue names.** Tool dedupes by venue.
- **WikiCFP/SCImago have no JSON API.** Need HTML scraping for structured CFP data.
- **arXiv category mapping is manual.** Only common fields mapped (9 entries). Unmapped fields skip arXiv.
- **DBLP is CS-only.** Won't find biology/chemistry/humanities conferences.

## Calendar Integration (Organism Calendar Harness)

The discovery tool is wired into the existing Organism Calendar via:
- **PublicationOpportunityAdapter** — 5th calendar adapter (alongside Cron, Engine, Pipeline, Writing)
- **publication_deadlines.db** — stores CFP deadlines, grant due dates, writing placeholders
- **Writing Studio bridge** — `/api/publications/write-for` creates draft + placeholder + deadline in one call

### Adding a Publication Deadline to the Calendar
```python
import sys; sys.path.insert(0, "/<workspace>")
from organism_calendar import add_publication_deadline

add_publication_deadline(
    venue_name="CCN 2026",
    venue_type="conference",
    field="neuroscience",
    deadline="2026-09-15T23:59:00Z",
    url="https://ccneuro.org/2026/",
    source="discovery",
    notes="Abstract submission deadline"
)
# → surfaces as "Deadline: CCN 2026" in calendar mesh (human lane, expedite if past)
```

### Adding a "Want to Write For X" Placeholder
```python
from organism_calendar import add_writing_placeholder

add_writing_placeholder(
    title="Physics-informed neural decoding methods",
    venue_name="Nature Neuroscience",
    venue_type="journal",
    field="neuroscience",
    notes="Target methods paper"
)
# → surfaces as "Write: <title>" in calendar mesh (AI lane)
```

### Full Bridge: Write-For-Venue (draft + placeholder + deadline in one call)
```bash
# Via API (creates Writing Studio draft + calendar item + placeholder)
curl -X POST http://localhost:port/api/publications/write-for \
  -H "Content-Type: application/json" \
  -d '{"title":"Neural decoding paper","venue_name":"Nature Neuroscience","venue_type":"journal","field":"neuroscience","deadline":"2026-12-01"}'
```

### API Endpoints (pipeline_api.py :port)
| Method | Path | Purpose |
|--------|------|---------|
| GET | /api/publications/discover?field=X&opp_type=all | Live discovery |
| POST | /api/publications/deadline | Add CFP/grant deadline to calendar |
| POST | /api/publications/write-for | Create draft + placeholder + deadline |
| GET | /api/publications/opportunities | List tracked deadlines + placeholders |
| PATCH | /api/publications/opportunities/{id} | Update status (submitted, drafting, etc.) |

### API Endpoints (gg3_gateway.py calendar UI)
| Method | Path | Purpose |
|--------|------|---------|
| GET | /api/calendar/publications | List for calendar UI |
| POST | /api/calendar/publications/deadline | Add deadline from calendar |
| POST | /api/calendar/publications/write-for | Write-for from calendar |
| PATCH | /api/calendar/publications/{id} | Update status from calendar |

## Workflow
1. Run `discover(field, "all")` for a full sweep of live opportunities
2. Review journals for OA + APC fit
3. Check conference deadlines on venue websites
4. Cross-reference grants with eligibility (citizenship, career stage)
5. Recommend social venues based on communication goals
6. Use `check_oa_status(doi)` to verify paper accessibility
7. **Add deadlines to calendar** via `add_publication_deadline()` so they appear on the timeline
8. **Create writing placeholders** via `write_for_venue` when user says "I want to write X for venue Y" — creates draft + calendar item automatically
9. **Update status** as work progresses: discovered → drafting → submitted → accepted → published
