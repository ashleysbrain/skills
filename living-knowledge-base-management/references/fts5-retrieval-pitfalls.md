# FTS5 Retrieval Pitfalls — How a Quoting Bug Starved Every Organ

Diagnosed and fixed 2026-06-19 in `/<workspace>`.

## The Bug

`fts_search()` wrapped multi-word queries in double quotes before passing
them to FTS5's MATCH operator:

```python
# BROKEN — turns "design principles beauty" into an exact-phrase search
if " " in q and not q.startswith('"'):
    q = '"' + q.replace('"', '""') + '"'
```

FTS5 interprets `"design principles beauty"` as: match rows where those
three words appear **consecutively in that exact order**. Since no stored
principle contains that exact phrase, every natural-language query returned
zero results. The knowledge was in the database but unreachable.

## Diagnosis Path

```bash
cd /<workspace>

# 1. Confirm data exists (it did — 94 rows in canon_search)
sqlite3 canon.db "SELECT COUNT(*) FROM canon_search;"

# 2. Single-word query works (no quoting triggered)
python3 canon_query.py "design" --limit 3    # returns results

# 3. Multi-word query fails (quoting turns it into exact phrase)
python3 canon_query.py "design principles visual composition beauty" --limit 3
# -> "*(no canon cards matched 'design principles visual composition beauty')*"

# 4. Raw FTS with implicit-AND (space-separated, unquoted) works
sqlite3 canon.db "SELECT title FROM canon_search WHERE canon_search MATCH 'beauty proportion' LIMIT 5;"
```

Steps 2 vs 3 are the tell: if single words match but natural-language
phrases don't, the quoting logic is the culprit.

## The Fix

Tokenize multi-word queries into an OR expression so FTS5 surfaces anything
matching any token, then let BM25 ranking (`ORDER BY rank`) float the most
relevant to the top. This optimizes for **recall** — which is what a
memory/circulation system needs:

```python
import re as _re

# If caller supplied an explicit quoted phrase, honor it verbatim
if q.startswith('"'):
    fts_query = q
else:
    tokens = [t for t in _re.split(r"[\s,]+", q) if t]
    cleaned = [_re.sub(r"[^\w\-]+", "", tok) for tok in tokens]
    cleaned = [t for t in cleaned if t]
    if not cleaned:
        return []
    fts_query = " OR ".join(cleaned)
```

Then pass `fts_query` to the MATCH parameter. The fallback LIKE branch
should also tokenize rather than searching the raw multi-word string.

## Why OR Not AND

A knowledge circulation system is not a search engine optimizing for
precision. It is a **memory system** optimizing for recall — its job is to
surface every potentially relevant card so the consuming cell (the
prefrontal-cortex equivalent) can decide what matters. OR + BM25 ranking
achieves this: broad recall, relevance-ranked delivery, sub-second.

AND semantics would silently drop cards that match 4 of 5 query tokens but
not the 5th — exactly the starvation pattern that broke the organism.

## Verification (run after any change to fts_search)

```bash
cd /<workspace>

# Must return ranked results, not "no matches"
python3 canon_query.py "design principles visual composition beauty" --limit 4

# Faculty briefing must return substantive knowledge, not empty sections
python3 canon_query.py --brief creative

# All four faculties must return content (even if thin for non-creative)
for f in creative health engineering identity; do
    python3 canon_query.py --brief $f | head -4
done
```

## Generalization

This pitfall applies to ANY FTS5-backed knowledge base where the query
interface constructs MATCH strings programmatically. The rule:

- **Exact phrase** (caller wants a specific quote): wrap in `"..."`, pass through
- **Topic search** (caller wants everything relevant): tokenize to OR, rank by BM25

Never auto-quote multi-word topic queries. The default for a memory system
is recall, not precision.
