# the specialist engine — Architecture and Implementation

Real implementation at `/<workspace>`.
Built June 2026, verified working.

## System Architecture

Three scripts work together as a digestive system:

### science_engine.py (arXiv Harvester)
Queries the arXiv API across all organism domains using domain-specific search
terms. Outputs structured paper lists (`latest_scan.json`) for agent review.
Tracks coverage gaps.

```bash
python3 science_engine.py                    # scan all domains
python3 science_engine.py --domain health-science  # scan one
python3 science_engine.py --coverage         # show gaps
python3 science_engine.py --report           # canon summary
```

Key design: `DOMAIN_QUERIES` dict maps each domain name to 2-3 arXiv search
strings. Adding a new domain = add an entry to the dict + a row in the
domains table. No code changes needed.

### sync_canon.py (Injection Engine)
Processes `pending_updates.json` (flat JSON array) and ingests new
principles/findings/techniques/sources/ai_tells into canon.db. Handles:
- Deduplication (checks existing by title before inserting)
- Updates (if title exists, updates body/implications rather than duplicating)
- FTS5 index rebuild after insertion
- Markdown regeneration from DB
- Update logging

**Format gotcha**: sync_canon.py expects a FLAT JSON ARRAY of entries, not a
dict with an "entries" key. If you write `{"entries": [...]}` it crashes on
`e.get("domain")` because it iterates over dict keys, not dicts.

### absorb_institutional.py (Curriculum Ingestion)
Absorbs MIT OCW / Stanford / Yale course material. Idempotent (INSERT OR
IGNORE). Produces knowledge cards in the principles/findings/techniques
tables with 8D dimension tags and organ mappings.

## Database Schema (canon.db)

| Table | Purpose | Key columns |
|-------|---------|-------------|
| `domains` | Knowledge domains (12 organism-wide) | name, display_name, active |
| `principles` | Transferable truths | domain_id, title, body, implications, scientist, confidence, tags, superseded_by |
| `findings` | Empirical observations | domain_id, principle_id, title, body, action_text, confidence, tags |
| `techniques` | Implementable methods | domain_id, name, category, implementation, organ_mapping, maturity |
| `sources` | Citations | title, authors, venue, year, url, arxiv_id, doi |
| `ai_tells` | AI-generated output markers | tell, category, detection_method, fix, false_positive_rate, severity |
| `update_log` | Change history | run_type, domains_scanned, counts, notes, ran_at |

FTS5 virtual table `canon_search` indexes all text for full-text search.

## The 12 Organism Domains

| Cluster | Domains |
|---------|---------|
| Creative | creative-systems, human-perception, ai-tell-detection, preference-learning |
| Health/Cognitive | health-science, neuroscience-cognition, behavioral-science |
| Engineering | systems-architecture, data-science-ml, product-methodology |
| Foundation | brand-philosophy, arts-design |

## Cron Job

Weekly the operator agent cron (job ID `fe4aa67d3210`, Monday 6 AM):
1. Runs science_engine.py to scan arXiv across all domains
2. Runs targeted web_search for domains with coverage gaps
3. Synthesizes findings into pending_updates.json
4. Runs sync_canon.py to ingest
5. Reports what was added

The cron prompt is self-contained and includes the domain list, the sync
format warning, and the instruction to never use Anthropic models.

## Pending Updates Format

Flat JSON array. Each entry is one of:

```json
[
  {"type": "source", "title": "...", "authors": "...", "venue": "...", "year": 2025, "arxiv_id": "..."},
  {"type": "principle", "domain": "health-science", "title": "...", "body": "...", "implications": "...", "scientist": "...", "confidence": "high", "tags": "..."},
  {"type": "finding", "domain": "health-science", "title": "...", "body": "...", "action_text": "...", "confidence": "high", "tags": "..."},
  {"type": "technique", "domain": "creative-systems", "name": "...", "category": "...", "description": "...", "organ_mapping": "...", "maturity": "production"}
]
```

## Ordered Build Recommendations (Architecture → Pluralism)

The canonical build order for a creative organ system, ordered by dependency:

1. **Architecture** — Multi-agent organ system (CREA pattern). Skeleton first.
2. **Taste Genome** — LoRA (genotype) + IP-Adapter (phenotype) + negative embeddings (immune system) + DPO/HPSv3 (selection pressure).
3. **Evaluation Organ** — HPSv3 + CREA six-principle rubric + anti-tell scanner. Portfolio of evaluators, never a single scalar.
4. **Quality Loop** — CoHP iterative refinement (generate -> score -> select -> refine).
5. **HITL Gates** — Brief-first, component-level, review checkpoints between stages.
6. **Imperfection Injection** — Grain, wobble, phi-based deviation. Requires all prior systems to make imperfection meaningful.
7. **Aesthetic Pluralism** — Divergent references, bias audit, portfolio scoring. Only meaningful at population scale.

Full detail in `/<workspace>`.
