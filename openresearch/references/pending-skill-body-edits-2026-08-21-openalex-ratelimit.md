# Pending SKILL.md body edit — OpenAlex rate-limit correction (2026-08-21)

STATUS: patch refused by the curator read-before-write gate (6th live
confirmation of the hook bug: fresh full-content skill_view in the same
review turn does not register the read for a background patch; also note
patch(name='research/openresearch') fails name resolution while
skill_view(name='research/openresearch') succeeds). Apply at next
foreground curator pass.

## Edit — replace the paragraph under "## Ad-hoc retrieval: OpenAlex API"

OLD (currently in SKILL.md):

    When the OpenResearcher receptor is unavailable OR the topic is non-STEM
    (neuroscience, medicine, social science, interdisciplinary), use the
    OpenAlex API directly for paper retrieval. OpenAlex covers 250M+ works
    across ALL disciplines, requires no API key, and does not rate-limit like
    Semantic Scholar (which 429s after 2-3 rapid calls) or bot-block like
    Google Scholar.

NEW:

    When the OpenResearcher receptor is unavailable OR the topic is non-STEM
    (neuroscience, medicine, social science, interdisciplinary), use the
    OpenAlex API directly for paper retrieval. OpenAlex covers 250M+ works
    across ALL disciplines, requires no API key, and does not bot-block like
    Google Scholar. RATE-LIMIT CORRECTION (proven live 2026-08-21): OpenAlex
    429s HARD on verification bursts (~50% of queries at 0.35-10s spacing,
    even with the mailto param + exponential backoff 8/16/24s). For
    bibliographic VERIFICATION (does this instrument/paper exist, who cited
    it), the Crossref polite pool is the reliable fallback — 8/8 queries OK
    at 4s spacing:

        https://api.crossref.org/works?query.bibliographic=<q>&rows=4&select=title,author,published,DOI,is-referenced-by-count,container-title&mailto=<email>

    Pattern: OpenAlex for broad discovery passes (tolerate 429s + retry
    ladder), Crossref for anchor-verification bursts. Blocked primary pages
    (e.g. consumerfinance.gov 403s bots): verify the instrument via its
    PUBLISHED validation records instead of scraping the primary page —
    never fabricate snippet text from a blocked fetch.

## Optional second edit (same session's evidence) — append to Hard rules:

    - Gate invocation path (2026-08-21): openresearch_ingest.py only works
      from a workspace root that HAS veritas_engine.py at root. Canonical
      working entry: /<workspace>
      Smoke-test with --no-consolidate first; verify consolidation by the
      okeefe_memory_count delta + :port /health, never rc=0 alone. Full
      transcript: your-stack-operations/references/
      financial-research-veritas-pass2-2026-08-21.md.

Cross-reference: primary session record lives at
software-development/your-stack-operations/references/
financial-research-veritas-pass2-2026-08-21.md (landed on disk).
