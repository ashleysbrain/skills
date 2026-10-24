---
name: institutional-knowledge-absorption
description: >
  Absorb curriculum and research from elite institutions (MIT OCW, Stanford,
  Yale, etc.) into The Corpus (the specialist engine / canon.db). The organism's digestive
  system: external knowledge goes in as raw material, comes out as queryable
  knowledge cards that ALL organism faculties (creative, health, engineering,
  business, neuroscience, etc.) query on demand before producing output.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [research, knowledge-base, learning-agent, mit-ocw, canon, creative-faculty]
---

# Institutional Knowledge Absorption

## What this does

Takes external knowledge "food" (MIT OCW courses, Stanford lectures, papers)
and converts it into body-usable knowledge cards in The Corpus (canon.db).
Because ALL organism faculties query `canon.db` on demand before producing
output, absorbed knowledge AUTO-DISTRIBUTES — no separate broadcast step.
The Corpus is universal: creative, health, engineering, business, behavioral,
neuroscience — every faculty draws from the same digestive system.

> **Naming**: The knowledge base is called **The Corpus** (the specialist engine internally).
> The data file stays `canon.db` (technical layer — do NOT rename, breaks
> cron/scripts). An earlier creative-only sidecar named "Da Vinci" is DEAD
> (empty scan script, 3 crons paused 2026-06-19). See Pitfalls below.

## The body-metaphor mapping (holobiont model)

See `docs/EXTERNAL-ENGINES-METAPHOR.md` for the canonical four-ring model.

| Stage | Bio equivalent | DS system | Ring |
|-------|---------------|-----------|------|
| Food source | The world you eat from | MIT OCW, Stanford, external institutions | Ring 4: Ecosystem |
| Ingestion + digestion | Gut + microbiome break food into nutrients | Research agent reads course, distills into cards | Ring 3: Microbiome (scripts/) |
| Assimilation + storage | Nutrients absorbed into tissue, immune memory formed | Cards inserted into canon.db (principles/findings/techniques) | Ring 1→2: Body + Immune Memory |
| Circulation | Bloodstream delivers nutrients on demand | Organism organs query canon.db at brief time | Ring 1: Body (blood flow) |

This is the **digestive system** of the organism. The existing weekly
`sync_canon.py` is the basal metabolic rate (arXiv scanning). This engine is
**eating a meal** — deliberately choosing high-value institutional curriculum
and converting it to structured knowledge.

## The template (knowledge card format)

Every absorbed course produces cards in this shape. The engine
(`absorb_institutional.py`) handles the DB insertion; the agent's job is to
DISTILL real course material into this format.

### Course dict structure
```python
COURSE = {
    "course_code": "4.175",          # institutional course code
    "title": "Case Studies in City Form",
    "url": "https://ocw.mit.edu/courses/...",
    "year": 2005,
    "authors": "Prof. X; Prof. Y",
    "institution": "MIT OCW",         # must exist in INSTITUTIONS dict
    "domain": "arts-design",          # canon domain (created if new)
    "dim": "intellectual",            # primary 8D axis
    "archive_path": "archive/mit-ocw/4-175-....md",
    "principles": [ ... ],            # transferable truths, not restatements
    "findings": [ ... ],              # specific empirical/historical cases
    "techniques": [ ... ],            # implementable methods mapped to organs
}
```

### Principle card (the core unit)
- **title**: one-sentence truth, stated as a claim
- **body**: what the principle IS (2-4 sentences, grounded in the source)
- **implications**: what it means for the DS organism (which organ, what decision)
- **scientist**: who established it (may be None)
- **confidence**: high / medium / low
- **tags**: MUST include `8d:<dimension>` + domain + granular topics

**Critical rule:** A principle is NOT "the course teaches X." It IS X — the
transferable truth stripped of its pedagogical wrapper. Bad: "MIT 4.175 covers
urban form analysis." Good: "Form is understood by analysis, drawing, and
comparison — not description."

## The multi-axis taxonomy (scales to "everything in life")

| Axis | Tag prefix | Example | Purpose |
|------|-----------|---------|---------|
| 8D dimension | `8d:` | `8d:intellectual` | Top-level life bucket (8 canonical) |
| Domain | domain column | `arts-design` | Discipline |
| Institution | source.venue | `MIT OCW` | Provenance |
| Topic | free text | `proportion`, `precedent` | Granular search |

Query any slice: `WHERE tags LIKE '%8d:intellectual%' AND domain='arts-design'`

## No-bloat retrieval (three tiers)

| Tier | What | Size | When loaded |
|------|------|------|-------------|
| Tier 0 | FTS5 search index (`canon_search`) | <1MB | Always queryable |
| Tier 1 | Distilled card rows (principles/findings/techniques) | KB each | On-demand by tag/domain query |
| Tier 2 | Raw archive markdown (`archive/`) | 5-20KB each | NEVER auto-loaded; deep-dive only |

The organism never bloats because:
1. Raw course material stays in Tier 2 (disk only, never in context)
2. Tier 1 cards are ~200 words each, loaded selectively by tag query
3. FTS5 returns snippets, not full rows, so even search results are compact

## Staged absorption discipline ("work smarter")

The user's explicit correction: absorb ONE course at a time, not a firehose.
Each run distills ~3 transferable principles from a single course. This keeps
cards dense and queryable rather than noisy and shallow.

**Anti-pattern:** trying to absorb 10 courses at once produces shallow cards,
overwhelms the review step, and the user will flag it. The digestive tract
works one meal at a time.

Correct staging:
1. Pick ONE course with the highest strategic fit to the current organism need
2. Distill ~3 transferable principles (not the whole syllabus)
3. Verify FTS search finds them by topic keyword
4. Move to the next course only when the previous absorption is verified
5. Expand to the next domain/faculty only when the current one has solid coverage

## Process flow (per absorption)

```
1. SELECT  — research agent identifies a high-value course (by topic fit
             to current organism need)
2. EXTRACT — pull real course content (web_extract or browser for JS pages)
3. DISTILL — convert to knowledge cards (principles/findings/techniques)
             using the template above. Every card must pass:
             ✓ Is it a transferable truth (not a restatement)?
             ✓ Does it have organ implications?
             ✓ Is it tagged on all 4 axes?
4. SEED    — add course dict to COURSES list in absorb_institutional.py
             (or call absorb_course() directly)
5. ARCHIVE — raw markdown to archive/<institution>/<course>.md (Tier 2)
6. VERIFY  — run --report, confirm FTS search finds the new cards
```

## Running the engine

```bash
cd /<workspace>

python3 absorb_institutional.py            # absorb all configured + rebuild FTS
python3 absorb_institutional.py --fts-only # rebuild search index
python3 absorb_institutional.py --report   # current state of the canon
```

## Adding a new institution

1. Add to the `INSTITUTIONS` dict in `absorb_institutional.py`:
   ```python
   "Stanford Online": {
       "venue": "Stanford Online",
       "license": "CC BY-NC-SA 4.0",
       "source_type": "institutional-stanford",
       "base_url": "https://online.stanford.edu",
   },
   ```
2. Absorb courses using `"institution": "Stanford Online"` in the course dict.

## Adding a new domain

Domains are created on-demand by `ensure_domain()`. No ALTER needed.
Example: absorbing an economics course creates a `financial-science` domain
with a single INSERT.

## Recurring ingestion — three-cron staggered schedule (operational)

The engine is idempotent (INSERT OR IGNORE). Absorption runs **off-hours via
three staggered crons** — never in the foreground during active work. The
user's explicit directive: "this needs to be done over time and in the
background when I am not working" and "don't ever over cron the system at one
time. stagger them so we don't break anything."

### The five crons (all workdir: knowledge-canon/)

| Cron | Schedule | Provider | What It Does |
|------|----------|----------|--------------|
| **Nightly Absorption** | daily 1:30 AM CT | gemini-3.1-pro / google-gemini-cli | Absorbs **2 courses** from `absorption_queue` (status='pending') into canon.db. Silent local delivery. |
| **Weekly Discovery** | Sunday 2:00 AM CT | gemini-3.1-pro / google-gemini-cli | Finds NEW courses from MIT/Stanford/Yale and adds to queue (does NOT absorb). Uses browser toolset. |
| **Weekly Science Sync** | Monday 6:00 AM CT | (script-only, no_agent) | Runs `science_engine.py` arXiv scan across all 12 domains + ingests via `sync_canon.py`. |
| **Health Watchdog** | every 4h | (script-only, no_agent) | Runs `corpus_health_audit.py` + `corpus_auto_fixer.py`. Auto-repairs stale claims and failed items. Escalates to user only when agent intervention needed (RERUN_DISCOVERY, RERUN_ABSORPTION). Created 2026-07-06. |
| **Fixer Agent** | every 8h | glm-5.2 / llm-vendor-glm | Specialized agent that repairs failed discovery/absorption runs. Browses catalogs or manually absorbs stuck courses when watchdog escalates. Created 2026-07-06. |

**Pacing math:** 2 courses/night = ~14/week = ~700/year. Full catalog saturates
in weeks with zero daytime load. This is the "work smarter" answer.

See `references/corpus-pipeline-resilience.md` for the 3-script
audit→fixer→watchdog architecture that makes the pipeline self-healing.

### Cron staggering discipline (user-enforced rule)

When creating or modifying ANY organism cron, you MUST verify it does not
collide with existing crons. The methodology:

1. List all active crons (`cronjob action=list`)
2. Map each to its time slot — flag any two crons in the same 15-minute window
3. If collision risk exists, shift to a different time slot OR use a different
   model provider (avoids rate-limit contention between concurrent runs)
4. Absorption crons use Z.AI (glm-4.6) specifically — NOT OpenRouter free
   models that the advisory boards use — so they never contend for the same
   rate-limited pool
5. Off-hours only: 1 AM–6 AM CT for absorption, never during active work hours

See `references/corpus-cron-schedule.md` for the full collision-check methodology
and verification commands.

### How to execute Weekly Discovery (the discovery agent workflow)

The Weekly Discovery cron (Sunday 2 AM CT) or a manual discovery dispatch follows
this exact sequence. See `references/discovery-workflow.md` for the full
step-by-step with browser extraction recipes and catalog URLs.

**Summary:**
1. `python3 canon_queue.py stats` — check pending count (SKIP if 30+ pending)
2. Query existing URLs from `canon.db` → `absorption_queue` table for dedup
3. Browse each institution's catalog page (MIT OCW by department, Yale OYC
   table, Stanford SEE)
4. Extract course data via browser JS console (snapshots don't expose course
   cards — see pitfall below)
5. Target underrepresented domains for diversity (check stats first)
6. Add via `canon_queue.py add --url --title --institution --domain --course-code --priority`
7. Max 15 new courses per run. Priority 3 for core creative/health, 5 default.
8. Report and run `stats` for final state.

**Browser extraction pitfall:** MIT OCW search results pages render courses
dynamically in a React table that does NOT appear in the accessibility-tree
snapshot. The snapshot shows only the department filter checkboxes and a result
count, not the course list. You MUST use `browser_console` with a JS extraction
query to pull `a[href*="/courses/"]` links and their card text. See the
reference file for the exact JS snippets that work.

### Queue-based absorption seeding (the seeding pattern)

Instead of editing `COURSES` in `absorb_institutional.py` directly, seed courses
into the `absorption_queue` table. This lets the nightly cron pick them up
automatically at a controlled pace.

1. Create a JSON seed file (e.g. `seed-mit-faculty-phase2.json`) with verified
   course dicts — each must have: title, url, institution, course_code, domain,
   faculty, dimension_8d, priority, tags
2. Insert into `absorption_queue` via SQL (check for duplicate URLs first):
   ```sql
   INSERT INTO absorption_queue
   (title, url, source_type, institution, course_code, domain, faculty,
    dimension_8d, priority, tags)
   VALUES (?, ?, 'institutional-ocw', ?, ?, ?, ?, ?, ?, ?)
   ```
3. The nightly cron picks `WHERE status='pending' ORDER BY priority DESC LIMIT 2`
4. Verify: `sqlite3 canon.db "SELECT faculty, COUNT(*) FROM absorption_queue GROUP BY faculty;"`

**Critical:** Always verify course URLs are real before seeding — use
`web_search` to confirm each `ocw.mit.edu/courses/...` URL actually resolves.
Never fabricate URLs.

### The expansion path (Phase 1 → 4)

The canonical expansion roadmap lives in
`/<workspace>` § 6. Summary:

| Phase | Focus | Status |
|-------|-------|--------|
| Phase 1 — DEPTH | MIT arts → creative faculty saturation | Active (11 queued + 1 absorbed) |
| Phase 2 — FACULTIES | Seed health, engineering, identity queues | Seeded 2026-06-19 (8 courses across health + engineering) |
| Phase 3 — INSTITUTIONS | Beyond MIT: Stanford, Yale, Coursera, arXiv | Discovery cron targets MIT/Stanford/Yale already |
| Phase 4 — 8D COMPLETENESS | Tag everything by 8D dimension | Ongoing via seed file `dimension_8d` field |

## Pitfalls

### 'Da Vinci' is a dead creative-only sidecar — do not use
An earlier attempt built a separate creative-only knowledge base named "Da
Vinci" with `davinci-kb-scan.sh` (an empty 0-byte file). Its 3 cron jobs
never ran and were paused 2026-06-19. The Corpus replaces it entirely. If you
see references to "Da Vinci KB" in cron jobs, scripts, or docs, retire them
and point everything at The Corpus (`knowledge-canon/`).

### sync_canon.py expects a FLAT JSON ARRAY
`pending_updates.json` must be `[...]` (a flat array of entry objects), NOT
`{"entries": [...]}`. The sync engine iterates the top-level structure
directly. A dict wrapper causes every entry to be silently skipped — no error,
no data. Always validate the file is a bare array before syncing.

### Entries missing the `domain` field cause "Unknown domain: None"
Every entry in `pending_updates.json` must have a `domain` key matching an
existing domain in the `domains` table. Missing domain produces silent errors
logged as "ERROR: Unknown domain: None" in the update_log. Always validate
that `domain` is set on every entry before syncing. Run `--report` afterward
and check the update_log for this error string.

### Corrupted absorb_institutional.py — orphaned duplicate fragments
If `absorb_institutional.py` fails with `IndentationError`, the likely cause
is orphaned duplicate fragments from a bad edit (stray closing brace,
duplicate field, dangling list opener). Diagnose by checking for a premature
`}` that closes a course dict before its findings/techniques sections. Fix:
remove the orphaned lines and stitch the dict back together. Always
`py_compile` after editing, then `python3 -c "import absorb_institutional as a; print(len(a.COURSES))"`
to verify course count before running the full absorption.

### Cron collision — scheduling absorption during active work or on top of other crons
The user's explicit, repeated directive: "don't ever over cron the system at
one time. stagger them so we don't break anything." Scheduling absorption crons
during active work hours (7 AM–11 PM CT) or in the same time slot as advisory
board crons causes rate-limit contention and system slowdown.
**Prevention:**
- Absorption crons fire only in the 1–6 AM CT window
- Use Z.AI (glm-4.6) for absorption — different provider pool from the OpenRouter-based advisory fleet
- Always run `cronjob action=list` and check for time-slot collisions before creating new crons
- See `references/corpus-cron-schedule.md` for the full staggered schedule and collision-check methodology

### Cron provider failover silently hits depleted accounts (HTTP 402)
When a cron job's primary provider (e.g. google-gemini-cli) fails, the the operator agent
cron runtime can silently fall back to OpenRouter. If OpenRouter credits are
depleted, the job dies with `HTTP 402: This request requires more credits`.
This is invisible until the user notices work didn't happen.

**What actually occurred (2026-07-05):** Discovery job configured for
google-gemini-cli failed and fell back to OpenRouter (0 credits), producing
HTTP 402. The nightly absorber survived because it was lighter and didn't
trigger the fallback path. Discovery silently failed for a full week.

**Prevention:**
- Pin fixer/repair agents to llm-vendor-glm (different pool, never OpenRouter)
- Run the Health Watchdog every 4h — it detects `last_status: error` and escalates
- When the watchdog reports RERUN_DISCOVERY, dispatch the fixer agent (not
  the original cron) using llm-vendor-glm to avoid the same failover trap
- See `references/corpus-pipeline-resilience.md` for the full audit→fixer→watchdog chain

### Stale `canon_queue.db` — always query `canon.db`, never `canon_queue.db`
There is a 0-byte stale file `canon_queue.db` in the knowledge-canon directory
left over from an earlier migration. It has no tables. Querying it produces
`sqlite3.OperationalError: no such table: courses`. The real absorption queue
table (`absorption_queue`) lives in **`canon.db`** (1.2MB+). The `canon_queue.py`
CLI already uses `canon.db` correctly — always use the CLI, not raw SQLite
against the wrong file. If you need raw SQL, connect to `canon.db`.

### Script WORKDIR when deploying to <agent-home>/scripts/ (2026-07-06)
When cron scripts live in `<agent-home>/scripts/` but operate on files in a
different directory (like `knowledge-canon/`), the scripts MUST hardcode
WORKDIR to the target directory, NOT use `Path(__file__).parent`. 

`Path(__file__).parent` resolves to `<agent-home>/scripts/` where no `canon.db`
exists. The audit silently returns `"queue": {"error": "canon.db not found"}`
and health CRITICAL while the canon-directory copy returns WARNING. Both copies
disagree, and the watchdog fires false escalations.

**Rule:** Scripts deployed to `<agent-home>/scripts/` that reference external
data files MUST use absolute paths:
```python
WORKDIR = Path("/<workspace>")  # CORRECT
# NOT:
WORKDIR = Path(__file__).parent  # WRONG — resolves to <agent-home>/scripts/
```

Keep the canon-directory copies using `Path(__file__).parent` (correct there).
But the `<agent-home>/scripts/` copies need absolute paths. Always run both copies
and verify they produce the same health verdict.

### Queue items stuck in 'claimed' state when absorption dies mid-process
When the nightly absorber claims a course (`status='claimed'`) but dies before
completing (provider timeout, crash, context overflow), the item stays claimed
indefinitely. Stale claims block the absorber from picking up new items because
it selects `WHERE status='pending' ORDER BY priority DESC`.

**What actually occurred (2026-07-06):** Two items stuck for 5–13 days
(Beginning Costume Design claimed July 1, Artificial Intelligence claimed
June 23). The absorber kept working on other items but these two were dead.

**Fix:** The Health Watchdog auto-resets claims older than 48h:
```bash
python3 corpus_auto_fixer.py unstuck
```
The schema column is `retry_count` (NOT `attempts`). Never decrement
non-existent columns in UPDATE statements.

### Stanford `online.stanford.edu/free-courses` returns 403 Forbidden
The URL `https://online.stanford.edu/free-courses` returns a 403 page when
accessed by the browser tool. Do NOT use it for discovery. Instead, use
**`https://see.stanford.edu/Course`** (Stanford Engineering Everywhere), which
renders a simple course list with direct links. Note: SEE has a limited catalog
(~9 courses: CS106A, CS106B, CS107, CS223A, CS229, EE261, EE263, EE364A,
EE364B). Yale OYC (`oyc.yale.edu/courses`) has a clean HTML table that scrapes
perfectly with a single JS query.

## Pipeline health and self-healing

> **Reference:** `references/discovery-workflow.md` — full operational guide for
> the Weekly Discovery agent (browser extraction recipes, catalog URLs, domain
> mapping, JS snippets). Read this before running discovery manually or via cron.

The absorption pipeline is unattended. When a job fails, nobody notices for
days. The solution is a 3-layer audit→fixer→watchdog chain that runs without
tokens and escalates only when an agent is genuinely needed.

### The three scripts (all in knowledge-canon/)

1. **`corpus_health_audit.py`** — Diagnoses everything: checks discovery and
   absorption job status from `<agent-home>/cron/jobs.json`, scans the queue for
   stale claims (>48h), lists failed items, verifies DB integrity (FTS index,
   orphaned sources, pragma integrity_check). Outputs JSON with `health`
   (HEALTHY/WARNING/CRITICAL) and `actions_needed` array.

2. **`corpus_auto_fixer.py`** — Mechanical repairs needing no agent:
   `unstuck` (reset stale claims), `retry-failed` (reset failed items to
   pending), `integrity` (full DB check), `rebuild-fts` (rebuild search index).

3. **`corpus_watchdog.py`** — Orchestrator. Runs audit, auto-applies safe
   fixes, re-audits, and either stays silent (everything resolved) or prints
   an escalation alert. Runs as `no_agent: true` cron every 4h — zero tokens.

### Actions taxonomy

| Action | Who handles | Requires agent? |
|--------|------------|-----------------|
| UNSTUCK_CLAIMS | Auto-fixer | No (mechanical SQL) |
| RETRY_FAILED_ITEMS | Auto-fixer | No (mechanical SQL) |
| RERUN_DISCOVERY | Fixer Agent cron | Yes (browser + LLM) |
| RERUN_ABSORPTION | Fixer Agent cron | Yes (web_extract + LLM) |

The Fixer Agent cron (every 8h, llm-vendor-glm) handles the agent-required actions.
It reads the audit output, browses catalogs or manually absorbs stuck courses,
and re-runs the audit to verify health is restored.

### When to dispatch manually vs let cron handle it

- **Let cron handle it:** stale claims, failed items, discovery/absorption
  provider errors. The watchdog catches these within 4h and the fixer agent
  resolves within 8h. Do nothing.
- **Dispatch manually (delegate_task):** when the user asks "ensure anything
  missed gets done NOW." Dispatch a leaf subagent with the discovery or
  absorption prompt, pinning to llm-vendor-glm to avoid the OpenRouter failover trap.

See `references/corpus-pipeline-resilience.md` for the full architecture
diagram, the scripts' command interface, and reproduction instructions for
applying the same pattern to other cron pipelines.

See `references/allostasis-regulatory-integration.md` for how the watchdog
POSTs vitals to the specialist engine (:port) as a monitored subsystem, and how to
generalize the audit→fixer→watchdog pattern to ANY cron pipeline.

## Verification checklist

- [ ] Course content extracted from real source (not invented)
- [ ] Every card has `8d:` dimension tag
- [ ] Every card has domain + topic tags
- [ ] Source row registered with correct institution + license
- [ ] Archive markdown written to correct path
- [ ] `--report` shows the new domain/cards
- [ ] FTS search finds the new cards by topic keyword
- [ ] `update_log` row records the absorption
