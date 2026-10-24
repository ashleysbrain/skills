---
name: living-knowledge-base-management
description: Build and maintain a living, updating knowledge base with automated research pipelines, structured documentation, and preservation principles to ensure critical information is never lost or forgotten.
category: research
---

# Living Knowledge Base Management

Build and maintain a knowledge base that stays current with the latest research in a domain while following strict preservation principles (never delete, version everything) and providing both human-readable and programmatic access.

## Trigger Conditions

Use this skill when you need to:
- Create a knowledge base that must stay current with latest research/knowledge in a field
- Ensure important information, principles, or theories are never dropped or forgotten
- Provide both human-readable documentation and programmatic access (e.g., for AI agents)
- Organize knowledge by domain or topic with clear metadata
- Implement automated update pipelines to reduce manual maintenance burden
- Establish versioning and change tracking for auditability and reproducibility

## Core Principles

1. **Never Delete, Only Supersede**: When information is updated, mark the old version as `SUPERSEDED → [new reference]` rather than deleting it
2. **Everything Has a Source**: Every claim, principle, or technique must have a clear citation with date and confidence level
3. **Dual Accessibility**: Knowledge must be accessible both to humans (via structured documents) and programs (via database/query interface)
4. **Preserve Context**: Maintain not just what we know, but how we know it and when we learned it
5. **Domain Organization**: Structure knowledge by relevant domains that can expand as needed

## Implementation Steps

### 1. Define Knowledge Structure
Create a directory organization that separates concerns:
```
knowledge-base/
├── README.md                          ← Master index and usage guide
├── science/                           ← Core research findings, methods, evaluations
│   ├── [domain]-evaluation-sota.md    ← State-of-the-art techniques for domain
│   ├── [domain]-injection-methods.md  ← Personalization/style injection methods
│   └── [domain]-creative-systems.md   ← Multi-agent/system architectures
├── evaluation/                        ← Evaluation criteria and rubrics
├── rubrics/                           ← Domain-specific quality criteria
├── principles/                        ← Foundational non-negotiable principles
├── updates/                           ← Chronological log of all changes
│   └── UPDATE-LOG.md
├── roadmap/                           ← Implementation plans with dependency ordering
└── knowledge-base.db                  ← SQLite index for programmatic access
```

### 2. Establish Versioning and Preservation Policy
- Every document header includes: `**Version:** X.Y | **Date:** YYYY-MM-DD | **Confidence:** [High/Medium/Low]`
- Superseded findings are marked: `**STATUS: SUPERSEDED → see [new reference]`**
- SQLite database maintains a `superseded_by` column for programmatic tracking
- Nothing is ever deleted from the source of truth — only updated with clear references
- Update log (`updates/UPDATE-LOG.md`) maintains chronological history of all changes

### 3. Create Core Template Documents
For each knowledge type, establish a template with required metadata:
```
# [Document Title]
**Version:** 1.0 | **Date:** YYYY-MM-DD | **Confidence:** [High/Medium/Low]
**Domain:** [art-design|tech|health|...]
**Roadmap Phase:** [N] (if applicable)
[Purpose section]
[Main content with inline citations]
## Sources
1. [Paper/Source 1] - [URL] - [Key contribution]
2. [Paper/Source 2] - [URL] - [Key contribution]
```

### 4. Set Up Programmatic Access Layer
Create a SQLite database with tables for:
- **documents**: Tracks all markdown files (path, title, category, domain, description, size, dates)
- **findings**: Key research papers/citations (title, domain, category, description, source_type, URL, citation, confidence, status, tags, roadmap_phase, dates)
- **ai_tells**: Enumerated markers of AI-generated output (domain, name, description, cause, detection_method, fix, priority, dates)
- **principles**: Core design/philosophical principles (code, name, statement, category, dates)
- **update_log**: History of all updates (date, type, scope, source, findings_added, documents_modified, confidence, summary)
- **roadmap_phases**: Implementation phases with dependency tracking

### 5. Build Automated Research/Update Pipeline
Create a scheduled job (cron) that:
- Scans configured sources (e.g., arXiv) for new publications in each domain
- Uses domain-specific combined queries to respect rate limits:
  ```
  # Instead of multiple queries:
  #   search_arxiv('ti:"aesthetic"')
  #   search_arxiv('ti:"style transfer"')
  #
  # Use single combined query:
  #   '(ti:"aesthetic" OR ti:"style transfer" OR ...) AND (abs:diffusion OR abs:generation OR abs:eval)'
  ```
- Deduplicates against existing findings in the database
- Commits new findings with "pending-review" status
- Appends weekly summary to `UPDATE-LOG.md`
- Runs on defined cadence (e.g., weekly Monday 08:00)

### 6. Create Domain-Specific Evaluation Criteria
For each domain, establish:
- Quality rubrics (multi-dimensional where appropriate)
- AI-tell detection checklists (specific markers to watch for)
- Domain-specific critics that evaluate output against domain knowledge
- Pluralism metrics to prevent aesthetic/knowledge homogenization

### 7. Develop Dependency-Ordered Implementation Roadmap
Order phases by what enables what, not by logical grouping:
```
Phase 0: Knowledge Foundation ──→ (everything references this)
Phase 1: Architecture ........──→ defines the system components
Phase 2: Taste Genome ........──→ defines identity/evaluation criteria
Phase 3: Evaluation Organ ...──→ measures quality (needs Phase 0 + 1)
Phase 4: Quality Loop .......──→ living refinement cycle (needs Phase 0,1,2,3)
Phase 5: HITL Design ........──→ human governance wraps automated system
Phase 6: Refinement/Phenotype ──→ applies final touches (needs full pipeline)
Phase 7: Ethical Guardrail ....→ system-level protections (needs all previous)
```

### 8. Establish Update Cadence
Define regular maintenance intervals:
- **Weekly**: Domain-specific deep scans (rotating: art→tech→health→...)
- **Monthly**: Full knowledge base audit + cross-domain synthesis
- **Quarterly**: Strategy alignment — do principles still match the state-of-the-art?
- **On-demand**: Triggered by major breakthroughs, product launches, or market shifts

### 9. Implement Access Patterns
For agents and system components:
- **Human access**: Read markdown files directly for full context
- **Programmatic access**: Query SQLite database for structured lookup
  - *Example*: `SELECT * FROM findings WHERE domain='tech' AND category='technique' AND status='active'`
- **Latest version access**: Always resolve superseded references to get current knowledge
- **Change tracking**: Query update_log for recent modifications

### 10. Ensure Knowledge Preservation
Implement safeguards against loss:
- Never delete information — only update with clear supersession references
- Maintain complete update log with timestamps and summaries
- Regularly verify backup integrity of both document files and database
- Test recovery procedures periodically
- Document all assumptions and confidence levels explicitly

## Key Techniques

### Efficient Domain Scanning (arXiv Example)
To respect API rate limits while maintaining comprehensive coverage:
```python
def search_arxiv_domain(domain_terms, context_filter, max_results=15, days_back=7):
    """
    Scan arXiv for a domain using a single combined query.
    
    Args:
        domain_terms: List of specific topics to OR together (e.g., ['aesthetic', 'style transfer', 'human preference'])
        context_filter: AND clause to ensure relevance (e.g., '(abs:diffusion OR abs:generation OR abs:eval)')
        max_results: Maximum results to return
        days_back: How far back to search
    
    Returns:
        List of new papers not already in the knowledge base
    """
    # Build OR'd domain query
    domain_query = ' OR '.join([f'ti:"{term}"' for term in domain_terms])
    # Combine with context filter
    full_query = f'({domain_query}) AND {context_filter}'
    
    # Execute single API call
    return search_arxiv(full_query, max_results=max_results, days_back=days_back)
```

### Biological Metaphor for Knowledge Organization
Organize knowledge using the genome/phenotype metaphor:
- **Genotype** (DNA): Core principles, foundational theories, immutable truths
- **Phenotype** (Expressed traits): Applied methods, techniques, domain-specific applications
- **Epigenome** (Environmental conditioning): Context-specific adaptations, prompt templates, guidelines
- **Immune System** (Antibodies): Knowledge to reject/rebuttal (common misconceptions, AI-tells)
- **Selection Pressure** (Evolutionary fitness): Validation criteria, preference pairs, benchmark results

**Critical distinction for DS organism**: BRAND-DNA = the genome (nature /
stable inherited identity — who the organism IS). The Corpus (canon.db) =
acquired knowledge (nurture / learning — what the organism has EATEN and
DIGESTED). This is why the knowledge base cannot be named after a person
(e.g. "Da Vinci") — it's not identity, it's accumulated nutrition. The
digestive + memory + immune + circulatory systems together form the
holobiont: absorb_institutional.py = the gut, canon.db = stored memory +
immune memory, FTS queries = the bloodstream delivering nutrients on demand.

## Critical Disciplines

### Discover Before Building
Before creating a knowledge base or adding capability to one, ALWAYS inspect what already exists:
- Query the database for current tables, domains, and counts
- Read the existing sync/ingestion scripts to understand the data contract
- Check the update log to see what has been run before

This prevents duplication. If a canon.db already exists with principles, findings, techniques, sources, and ai_tells tables, BUILD ON IT rather than creating a parallel system. The user explicitly flagged this: "work with this thread not against it/yourself."

### Order Recommendations by Build Dependency, Not Impact
When presenting a set of recommendations or implementation phases, order them by what enables what — foundational layers first. The user corrected this: "I don't believe they are in the correct order for most efficient outputs." Impact-ranked order looks smart but causes rework when downstream items depend on upstream ones that haven't been built yet.

Correct order for a creative/knowledge system:
1. Architecture (the skeleton everything plugs into)
2. Identity/Taste Genome (DNA injection — without it, output is generic)
3. Evaluation (can't improve what you can't measure — but quality is relative to YOUR identity, so genome comes first)
4. Quality Loop (uses evaluation to iterate)
5. HITL Governance (wraps the autonomous loop)
6. Output Polish (requires all prior systems to be meaningful)
7. Meta-Governance (only meaningful at population scale)

### Expand Domains to Cover the Full Organism
When the knowledge base serves a multi-domain organism (creative + tech + health + behavioral), don't keep it narrowly focused on one domain cluster. Expand the domain set to cover every physiological/functional category the organism needs:
- creative-systems, human-perception, ai-tell-detection, preference-learning (creative cluster)
- health-science, neuroscience-cognition, behavioral-science (health/cognitive cluster)
- systems-architecture, data-science-ml, product-methodology (engineering cluster)
- brand-philosophy, arts-design (identity/foundation cluster)

Run `python3 science_engine.py --coverage` to detect domains with thin coverage (< 2 principles or < 1 finding) and prioritize them for the next seed.

## QUALITY AUDIT BEFORE CLAIMING DONE (from session 2026-08-07)

The user asked "Ensure this was done with best in the world credentials."
An adversarial audit of the Otlet System Phase 1 build revealed the work
was a skeleton despite being claimed "operational." Concrete gaps found:
- 35% data coverage (167/483 presenters)
- Zero concept nodes (entire concept layer empty)
- Zero citation/co-authorship/collaboration edges
- Zero embeddings or spatial coordinates
- Papers had titles only — no abstracts, DOIs, or real metadata

**Before reporting ANY knowledge system as "done" or "world-class":**

1. **Count actual vs expected.** If the source has 483 presenters and you
   ingested 167, that is 35%, not "complete."
2. **Check every layer.** A heterogeneous graph with 7 node types but only
   3 populated and 7 of 14 edge types active is a partial build.
3. **Distinguish "exists" from "populated."** A table with 0 rows exists.
   That doesn't mean the layer is functional.
4. **Run an adversarial audit BEFORE the user asks.** Write a script that
   counts NULLs, measures coverage percentages, and flags every spec'd
   feature that has zero data. Do this as the final step, not after
   being challenged.
5. **Never claim "operational" without querying it.** An API that returns
   200 on /health but serves stale data because the DB was enriched after
   the server started is NOT operational. Restart the server and verify
   the new data flows through.
6. **"Build it right not half ass" means patience.** Rate-limited? Wait
   for the throttle to reset. Subagent timed out? Run it yourself with
   proper background execution. Do not declare partial work as complete
   just because a background timer expired. "This isn't a race."

## Common Pitfalls to Avoid

### ❌ Building Without Discovering Existing Infrastructure
**Symptoms**: You create a new database, script, or pipeline that duplicates one that already exists. The user catches the duplication and is frustrated.
**Prevention**:
- Before creating anything, query the filesystem and database for existing artifacts
- Read existing scripts to understand their data contracts
- Build ON existing infrastructure, not beside it
- When multiple threads touch the same system, search session history to understand what the other thread built

### ❌ The Circulation Layer Is Silently Broken — FTS Quoting Kills Recall
**Symptoms**: The knowledge base has hundreds of principles, findings, and techniques stored, but `canon_query.py "multi word query"` returns "no canon cards matched" for every natural-language search. Single-word queries work; multi-word queries return nothing. Every organ is starving because the bloodstream (retrieval) cannot deliver knowledge.
**Root cause**: FTS5 treats a double-quoted multi-word string as an **exact phrase match** — it only matches if those exact words appear consecutively in that order. A circulation/memory system needs RECALL (surface everything relevant), not precision (exact phrase only). Wrapping queries in `"..."` starves every cell.
**Prevention**:
- Never wrap multi-word FTS5 queries in double quotes unless you explicitly want an exact-phrase match
- Tokenize multi-word queries into an OR expression (`design OR principles OR beauty`) and let BM25 ranking surface the most relevant
- Always test the bloodstream with a multi-word natural-language query before claiming the system works
- See `references/fts5-retrieval-pitfalls.md` for the full diagnosis, fix code, and verification commands

### ❌ Absorbing Everything at Once Instead of Pacing Overnight
**Symptoms**: The agent tries to absorb all queued courses in a single foreground run, bogging down the active session and frustrating the user.
**Prevention**:
- Absorption runs as a **nightly cron** (off-hours, 2 courses/night), never in the foreground during active work
- Pacing math: 2/night = ~14/week = ~700/year. Full catalog saturates in weeks with zero daytime load
- The cron uses a queue table (`absorption_queue`) with status tracking — it picks up pending items, not everything at once
- User directive: "work smarter" and "this needs to be done over time and in the background when I am not working"

### ❌ Claiming the System Works Without End-to-End Verification
**Symptoms**: The agent reports the knowledge base is "operational" but has never actually run a multi-word retrieval query through the full path. A silent retrieval bug means the system is half-built despite looking complete.
**Prevention**:
- ALWAYS run a multi-word FTS query (e.g. `canon_query.py "design principles visual composition beauty"`) before claiming the circulation layer works
- Run a faculty briefing (`canon_query.py --brief creative`) to prove the transduction path delivers real knowledge
- Check queue depth and coverage gaps with SQL queries before reporting status
- User directive: "ensure everything is operational and not half built as you have a habit of half building something then stopping"

### ❌ Letting the Knowledge Base Become Stale
**Symptoms**: Information is outdated, latest research not incorporated, principles drift from current state-of-the-art
**Prevention**: 
- Implement automated update pipeline with reliable scheduling
- Establish clear ownership and maintenance responsibilities
- Set up monitoring for knowledge freshness (alert when no updates for X days)
- Regularly audit against external sources (conference proceedings, journal releases)

### ❌ Deleting Information Instead of Versioning
**Symptoms**: Important historical context lost, unable to track evolution of ideas, reproducibility issues
**Prevention**:
- Implement strict "never delete" policy at the cultural and technical level
- Use clear supersession markers: `SUPERSEDED → [new reference]`
- Maintain complete history in update log and database
- Make deletion operations require explicit override and justification

### ❌ Poor Organization Hindering Discoverability
**Symptoms**: Users can't find relevant information, duplicate effort, inconsistent application of knowledge
**Prevention**:
- Establish clear taxonomy upfront (by domain, type, purpose)
- Use consistent naming conventions and metadata standards
- Implement both hierarchical browsing and tag-based search
- Regularly solicit user feedback on organization effectiveness
- Provide clear index/documentation (README.md) on how to navigate

### ❌ Missing Citations or Provenance
**Symptoms**: Knowledge appears as unsupported assertions, undermines credibility, creates uncertainty
**Prevention**:
- Require source, date, and confidence for every knowledge entry
- Implement template validation that rejects incomplete metadata
- Provide easy citation tools/formatters
- Make sourcing part of the knowledge contribution workflow
- Regularly audit for unsourced claims and request verification

### ❌ Manual Update Processes That Don't Scale
**Symptoms**: Updates happen inconsistently, knowledge lags, maintenance burden causes neglect
**Prevention**:
- Automate as much as possible (scanning, deduplication, commit logging)
- Make manual steps minimal and well-documented
- Schedule updates during low-activity periods
- Provide clear failure notifications and retry mechanisms
- Test the update pipeline regularly

### ❌ All Infrastructure Built, No Cron Jobs Running — The Dormant System

**Symptoms**: The canon has 1,134 entries, a science_engine.py that queries
arXiv across 12 domains, an absorption queue with 31 pending items, a corpus
watchdog, and a sync script. All well-built. But ZERO cron jobs are scheduled.
The system ate once and stopped. It looks alive on inspection but has not
grown in weeks.

**Root cause**: Building the pipeline is satisfying and visible. Scheduling it
to run unattended is invisible and easy to forget. The agent built the digestive
system, fed it once manually, and never set up the eating schedule.

**Prevention**:
- After building ANY ingestion pipeline, IMMEDIATELY create the cron job.
  This is not a separate task — it is the final step of the build.
- Verify with `crontab -l | grep -i canon` that the job exists.
- Check absorption_queue for items stuck in `pending` status — if the count
  is not changing, the cron is not running.
- The user catches this every time: "how do we make sure these are actually
  engines that are built out" — a system that does not run is not built.

### ❌ Three.js Visualization Blank — Static Files Not Served by API

**Symptoms**: The Atlas (Three.js 3D graph) loads at `http://localhost:port/atlas`
but shows a blank page. The browser console shows `THREE is not defined` and
`init` never ran.

**Root causes** (three layers, check each):
1. **CDN blocked**: `unpkg.com/three@0.160.0/build/three.module.js` with
   `type="module"` may fail to load in restricted browsers (headless,
   corporate proxy, CSP). Download `three.min.js` locally and serve it from
   the API: `<script src="/three.min.js"></script>` (not the module version).
2. **API doesn't serve static files**: FastAPI with only `FileResponse` for
   `/atlas` won't serve `/three.min.js`. Add a route:
   ```python
   @app.get("/three.min.js")
   async def serve_three():
       from fastapi.responses import FileResponse
       return FileResponse(str(Path(__file__).parent / "three.min.js"),
                           media_type="application/javascript")
   ```
3. **Race condition**: If `<script src>` loads after the inline script that
   calls `init()`, `THREE` won't be defined yet. Use a poll-wait pattern:
   ```javascript
   function startAtlas() {
     if (typeof THREE === 'undefined') { setTimeout(startAtlas, 50); return; }
     init();
   }
   startAtlas();
   ```

**Debugging sequence**:
1. `curl -s -o /dev/null -w "%{http_code}" "http://localhost:PORT/three.min.js"`
   → must be 200
2. In browser console: `typeof THREE` → must be `"object"`
3. Check `document.querySelectorAll('script')` — verify the src URL matches
   what the API actually serves
4. If page looks stale (old script tags), use cache-busting URL:
   `http://localhost:port/atlas?nocache=1`

**See**: `references/openalex-rate-limiting.md` for the companion issue
(SQLite locking when enrichment + API run concurrently).

### ❌ Overly Complex Structure Creating Maintenance Burden
**Symptoms**: System is fragile, changes are risky, knowledge contributors avoid using it
**Prevention**:
- Start simple and add complexity only when demonstrably needed
- Favor convention over configuration
- Make common operations simple and discoverable
- Regularly refactor to reduce accidental complexity
- Prioritize developer/contributor experience alongside functionality

### ❌ Lack of Clear Inclusion/Evaluation Policies
**Symptoms**: Arbitrary decisions about what gets included, inconsistent quality, bias creep
**Prevention**:
- Establish explicit criteria for what knowledge is worth preserving
- Create review process for new additions (even if lightweight)
- Document confidence levels and uncertainty explicitly
- Implement bias audits for knowledge inclusion decisions
- Regularly revisit and update policies as the field evolves

## Verification Steps

After implementing a living knowledge base, verify:

### ✅ Structural Integrity
- [ ] Directory structure follows the defined convention
- [ ] All core documents exist with proper metadata headers
- [ ] SQLite database exists with all expected tables
- [ ] Update log is being written to regularly
- [ ] README.md provides clear usage and navigation guidance

### ✅ Content Quality
- [ ] Every knowledge entry has source, date, and confidence level
- [ ] No deleted information — only superseded with clear references
- [ ] Citations are verifiable and point to actual sources
- [ ] Confidence levels are justified and not inflated
- [ ] Superseded references resolve correctly to current knowledge

### ✅ Programmatic Access
- [ ] All human-readable documents are indexed in the database
- [ ] Queries return expected results for known knowledge
- [ ] Update log entries are queryable and chronological
- [ ] Superseded references can be automatically resolved
- [ ] Performance is acceptable for expected query volumes

### ✅ Update Pipeline
- [ ] Automated job runs on schedule without manual intervention
- [ ] New findings are correctly deduplicated against existing knowledge
- [ ] Pending-review items are properly identified for human review
- [ ] Update log entries accurately summarize changes
- [ ] Rate limits are respected and errors are handled gracefully

### ✅ Access Patterns
- [ ] Humans can find relevant knowledge through browsing and search
- [ ] Agents can retrieve knowledge via SQL queries or document reads
- [ ] Latest versions are correctly resolved from superseded chains
- [ ] Cross-domain queries work as expected
- [ ] Historical knowledge remains accessible for reproducibility

## The Verification Gate (the specialist engine)

The knowledge canon is not just a passive store. It is a **verification gate**
that checks all organism output before it leaves. This is the immune system
of the knowledge base: content that contradicts established canon knowledge
is blocked before publication.

### Three-Engine Architecture

1. **the specialist engine (ingestion, port :port)** — sensory organs. Absorbs MIT OCW,
   arXiv, OpenAlex, university publications into the canon. Owns the
   absorption queue.
2. **Canon DB + DS O'Keefe (storage, port :port)** — hippocampus. The canon.db
   IS long-term memory. O'Keefe implements the trisynaptic circuit with
   pattern separation (DG), auto-associative memory (CA3), novelty detection
   (CA1). Canon entries should be queryable through O'Keefe's pattern
   completion, not just FTS5.
3. **the specialist engine (verification gate, port :port)** — immune system +
   prefrontal cortex. Before any content flows OUT of the operator agent (Veritas, Crucible,
   social media, newsletters), it passes through Ebbinghaus. Checks claims
   against canon, flags contradictions, gates output by credibility.

### Credibility Weighting System

Every source in canon.db has a numeric `credibility_weight` (REAL, 0.0-1.0).
This is NOT binary peer-reviewed vs not. It is a continuous score:

| Source type | Weight | Rationale |
|---|---|---|
| peer-reviewed-journal | 1.0 | Nature, Science, Cell, Lancet |
| peer-reviewed-conference | 0.95 | NeurIPS, ICML, CVPR, USENIX |
| peer-reviewed | 0.9 | Any peer-reviewed publication |
| institutional-ocw | 0.85 | MIT/Stanford/Harvard coursework |
| paper (arXiv/SSRN) | 0.7 | Preprints, high novelty |
| preprint | 0.6 | Non-arXiv preprints |
| conference | 0.6 | Non-peer-reviewed talks |
| article | 0.5 | Magazine/blog |
| repo | 0.5 | Code repositories |
| industry-survey | 0.4 | Possible vendor bias |
| independent | 0.3 | Non-peer-reviewed independent research |

**Corroboration bonus:** If a claim from a 0.3-weight independent source is
corroborated by a 0.9+ source, effective weight rises to 0.7. Weak signals
that match strong patterns get promoted. This is the immune system's adaptive
response.

**Ebbinghaus decay:** Principles not accessed in 90+ days have accessibility
reduced per the forgetting curve: R = e^(-t/S) where S is strength. Stale
knowledge fades unless refreshed by access or reinforcement.

### Verification Gate Flow

1. **Draft arrives** — any the operator agent output destined for public release
2. **Claim extraction** — parse into discrete factual assertions
3. **Canon query** — FTS5 search for supporting/contradicting principles
4. **Verdict per claim** — PASS (weight >= 0.7, no contradictions) /
   FLAG (novel or low-weight only, needs citation) /
   REJECT (contradicts weight >= 0.85)
5. **Gate decision** — PASS (proceed) / REVISE (return for citation) /
   REJECT (blocked, must address contradictions)
6. **Log and learn** — verification results feed back into canon

### Integration Points

- **Veritas pipeline**: Stage 5 (Drafting) -> Ebbinghaus gate -> Stage 6
  (Adversarial Panel). Panel reviews arguments; Ebbinghaus checks facts.
- **Crucible pipeline**: Same integration point.
- **Social media/external comms**: the specialist engine posts pass through Ebbinghaus.
- **TSC Constellation tool**: Researcher profiles verified against canon.

### Implementation Status (updated 2026-08-06, 2 review passes complete)

the specialist engine engine exists at `gg3-blueprint/organism/engines/ds-ebbinghaus-engine/`.
Port :port (8150 was taken by the specialist engine). 5-layer architecture with 632-line
core engine, FastAPI API server, and cognitive/methodology/philosophy/validation
layers. Endpoints: /health, /verify, /query, /canon/stats, /canon/domains,
/canon/reinforce, /canon/decay, /canon/log. See `references/ebbinghaus-verification-implementation.md`
for the full implementation details, FTS5 tokenization approach, and known issues.

**Two adversarial code review passes completed (2026-08-06).** Pass 1 found 8
issues (3 critical: broken contradiction detection, meaningless similarity
metric, miscalibrated thresholds). Pass 2 found 6 more issues (overcorrected
contradiction detection, DB connection leak, rowid vs id column confusion,
score normalization, FTS5 escaping, duplicate sentence indices). All fixed.

**Contradiction detection now uses bidirectional contextual approach:**
requires (a) at least 3 shared content tokens between claim and canon entry
(same subject matter), AND (b) negation phrases within 40-char proximity of
overlapping terms, checked in BOTH directions (claim negates canon assertion,
OR canon negates claim assertion). No more false positives from negation words
in unrelated contexts.

**Similarity metric:** Jaccard token overlap (intersection / union of content
token sets). Replaced the meaningless `1/(1+abs(rank))` BM25-based pseudo-similarity.

**Confidence thresholds recalibrated for Jaccard distribution:** HIGH=0.15,
MEDIUM=0.08, LOW=0.03 (Jaccard scores typically range 0.05-0.40 for topical
matches). The old thresholds (0.8/0.5/0.2) were set for a different scoring
system and blocked almost everything.

**Verification logging:** `verification_log` table records every verify call
with draft_hash, claim_text, verdict, confidence, match_count, contradiction_count.
GET /canon/log endpoint returns recent logs for learning analytics.

### Known Architectural Gaps (identified 2026-08-06) → RESOLVED by Otlet System

The canon was a flat document store with keyword search. Six structural gaps
prevented it from being a living knowledge graph. ALL SIX are resolved by
the Otlet System architecture (2026-08-07):

1. **No relationship graph** → RESOLVED: Otlet adds 14 typed edge types across 5 toggleable layers (citation, concept, social, event, organizational).
2. **No semantic embeddings** → RESOLVED: SPECTER 2 + GraphSAGE fused embeddings (768-dim).
3. **No provenance chains** → RESOLVED: Heterogeneous graph supports forward traversal (person → paper → concept → institution → event).
4. **No freshness signal** → RESOLVED: Daily cron absorption + the specialist engine verification gate.
5. **No hierarchical taxonomy** → RESOLVED: Inherit OpenAlex topic hierarchy (4 domains → 26 fields → 360 subfields → 4,500 topics).
6. **No graph query capability** → RESOLVED: Heterogeneous graph with 7 node types, queryable by type/edge/layer.

### THE OTLET SYSTEM (2026-08-07) — canon.db evolution

The flat knowledge canon evolved into **The Otlet System**: a living 3D
heterogeneous knowledge graph of ALL science. Named after Paul Otlet
(1868-1944) who envisioned the Mundaneum — a global repository of all
knowledge connected by links — in 1934. The name "Knowledge Canon" was
RETIRED by the user ("I don't like that fucking name, rename that shit").

The Otlet System is NOT just a renamed canon. It is a fundamentally richer
architecture:

- **7 node types**: paper, concept, person, institution, research_lab, event, venue
- **14 edge types** across 5 toggleable layers (citation, concept, social, event, organizational)
- **Google Earth zoom**: Z1 (universe) → Z2 (field) → Z3 (subfield) → Z4 (topic) → Z5 (ground/paper)
- **5-layer architecture**: Ingestion → Graph DB → Embedding Engine → Layout Engine → Otlet Atlas (Three.js 3D visualization)
- **Tech**: SQLite+FTS5 (MVP) → DuckDB/Neo4j at scale. SPECTER 2 embeddings. UMAP 3D layout. Three.js WebGL rendering.

**Key user insight that shaped the architecture:** The graph must be
HETEROGENEOUS — connecting not just papers to papers, but people to
institutions, events to presenters, labs to papers. "If two people are
connected to the same university, what university published what research?"
This means drill-down works from conference event → person → institution →
lab → paper → concept, with any layer toggleable.

**Seed dataset:** TSC 2026 (483 presenters, ~3000-7000 nodes, Oct 11-16).
Spec at `/<workspace>`.
API port :port. the operator agent owns ingestion/embeddings/DB/API. Opencode owns
Three.js frontend (Bus 1523).

canon.db (481p/338f/143s) folds into the Otlet System as seed data.

### Public Data Principle

User correction (2026-08-05): "This information is public. They are publishing
their research publicly." Publications, abstracts, poster titles, ORCID
profiles are PUBLIC. Pre-building profiles from scraped public data is NOT
spying — every academic search engine (Google Scholar, OpenAlex, ResearchGate)
already does this. Add a confirm-or-edit flow at claim time, but do not
require opt-in-before-build. The pre-built card REDUCES friction because
people edit faster than they create from scratch.

## References and Inspiration

0. **The Corpus / the specialist engine (reference)**: `references/ds-knowledge-canon-architecture.md` — real implementation at `/<workspace>` with working `science_engine.py`, `sync_canon.py`, `absorb_institutional.py`, 12-domain schema, and the ordered build recommendations. Data file is `canon.db` (do NOT rename — breaks cron/scripts). An earlier creative-only sidecar named "Da Vinci" is DEAD (empty scan script, crons paused 2026-06-19); always use The Corpus path. **Note:** canon.db is being absorbed into the Otlet System (see next reference).

0a. **FTS5 retrieval pitfalls**: `references/fts5-retrieval-pitfalls.md` — the quoting bug that silently broke knowledge circulation (multi-word queries returned nothing), full diagnosis path, fix code, and verification commands. Read this before modifying any `fts_search()` function or building a new FTS5-backed query interface.

0b. **The Corpus Nervous System (canonical)**: `/<workspace>` — the canonical map of how acquired knowledge flows through the the operator agent organism: the five-body-system holobiont (appetite → digestion → memory → circulation → transcription), brain-region mappings, faculty pull commands, absorption cron schedule, three-tier retrieval, and the ordered expansion path from MIT-arts to all subjects. Read this before designing any new faculty, engine, or knowledge flow.

0c. **Otlet System Architecture**: `references/otlet-system-architecture.md` — the evolution of the flat canon into a living 3D heterogeneous knowledge graph of ALL science (2026-08-07). 7 node types, 14 edge types, 5 toggleable layers, Google Earth zoom (Z1-Z5), Three.js WebGL visualization. Named after Paul Otlet (Mundaneum, 1934). Full spec at `/<workspace>`. Seed: TSC 2026 (483 presenters). API :port. canon.db folds into this as seed data.

0d. **Otlet Build Status**: `references/otlet-system-build-status.md` — live build status, DB stats (3,559 nodes/6,617 edges as of 2026-08-11), API endpoints, what's built vs in-progress vs not started. Updated each build session.

0e. **STAGE 0 Seed Design**: `references/otlet-stage0-seed-design.md` — pre-launch seed spec with real numbers (queried from live DB). Three enrichment targets (papers 706→2,200, citations 109→8-12K, concept domains 85% orphans→95% covered), ~2,300 OpenAlex API calls, and the pre-compute vs lazy-compute decision rule. Read before sizing any seed corpus or deciding what to materialize at build time vs query time.

0f. **STAGE 2 Lazy Growth Engine**: `references/otlet-stage2-lazy-growth-engine.md` — how a living knowledge graph compounds as users join: co-citation materialization (the compound interest), embedding propagation via confidence-decaying BFS rings from user-deposited ground truth, and a 7-tier trigger taxonomy with a priority function. The generalizable pattern for lazy enrichment of any graph too large to batch-embed (OpenAlex 250M+). Read before designing growth/compounding for any user-populated KB.

0g. **OpenAlex Rate Limiting**: `references/openalex-rate-limiting.md` — observed throttle behavior (429 after ~300 calls, IP-level, hours to reset), recommended config (1s sleep, linear backoff), enrichment script architecture (phase separation, resumability, NONE-marking for unmatched), SQLite concurrency patterns (WAL + busy_timeout), overnight cron pattern.
1. **Divinity Science Principles**: Treat knowledge as science — every claim sourced, dated, versioned, never deleted
2. **arXiv API**: Efficient programmatic access to latest research papers
3. **SQLite**: Lightweight, reliable, zero-configuration database for structured storage
4. **Markdown**: Human-readable, version-control friendly documentation format
5. **Cron**: Reliable job scheduling for automated updates
6. **Biological Metaphor**: Genome/phenotype/epigenome/immune system/selection pressure framework for knowledge organization
7. **Software Version Control Principles**: Never delete history, clear commit messages, traceable evolution
8. **Scientific Method**: Falsifiability, reproducibility, evidence-based progression
9. **Knowledge Management Systems**: Wikis, document management systems, research information systems
10. **Digital Preservation Standards**: OAIS model, fixity checks, provenance tracking

## Related Skills

- **arxiv**: For efficient paper searching when building the update pipeline
- **technical-research-planning**: For planning research directions to scan for
- **writing-plans**: For creating the implementation roadmap with dependency ordering
- **universal-evidence-based-scoring-system**: For building evaluation components of the knowledge base
- **obsidian**: For personal knowledge management that might feed into or consume from the living KB
- **source-driven-report-rebuild**: For generating reports from the knowledge base for stakeholders

---
*This skill enables building knowledge systems that grow wiser over time rather than decaying or forgetting critical insights.*