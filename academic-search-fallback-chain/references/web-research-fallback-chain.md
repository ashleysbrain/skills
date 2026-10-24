# Web Research Fallback Chain (When Managed Web Tools Are Down)

Session-derived reference: a real research session (Aug 2026) where
`web_search` and `web_extract` both failed with Firecrawl 402 Payment
Required errors for the entire session. Full web research was still
completed using `terminal` (curl) and `browser_navigate`.

## The problem

Firecrawl-backed tools (`web_search`, `web_extract`) can fail with:

```
Payment Required: Failed to search. {
  'code': 'BILLING_ERROR',
  'message': 'Charge authorization failed',
  'upstreamStatusCode': 402,
  'details': { 'error': 'Insufficient available balance...' }
}
```

When this happens, ALL Firecrawl-backed calls fail — not just one. The
agent cannot search or extract anything via managed tools.

## The chain that works

### 1. Search engines via curl (no API key needed)

**Brave Search** (BEST tolerance, no CAPTCHAs observed across 10+ queries):

```bash
curl -sL --max-time 15 \
  -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" \
  "https://search.brave.com/search?q=your+search+terms" \
  | python3 -c "
import sys,re
t=sys.stdin.read()
t=re.sub(r'<script.*?</script>','',t,flags=re.S)
t=re.sub(r'<style.*?</style>','',t,flags=re.S)
t=re.sub(r'<[^>]+>',' ',t)
t=re.sub(r'&amp;','&',t)
t=re.sub(r'&#x27;',\"'\",t)
t=re.sub(r'&nbsp;',' ',t)
t=re.sub(r'\s+',' ',t)
print(t[:port])
"
```

Brave returns results in plain text with URLs — you can see titles,
snippets, and source domains. Use it to discover which pages to fetch.

**DuckDuckGo Lite** (works but rate-limited after ~3 rapid requests):

```bash
curl -sL --max-time 15 -A "Mozilla/5.0" \
  "https://lite.duckduckgo.com/lite/?q=your+search+terms" \
  | python3 -c "..."
```

After ~3 rapid requests, DuckDuckGo serves a CAPTCHA ("Select all squares
containing a duck"). If this happens, switch to Brave Search.

**Google/Bing via curl**: generally return JavaScript anti-bot walls.
Not recommended for curl-based research.

### 2. Page content extraction via curl + regex HTML strip

Once you have a URL from search results, fetch and extract text:

```bash
curl -sL --max-time 15 -A "Mozilla/5.0" "https://example.com/article" \
  | python3 -c "
import sys,re
t=sys.stdin.read()
t=re.sub(r'<script.*?</script>','',t,flags=re.S)
t=re.sub(r'<style.*?</style>','',t,flags=re.S)
t=re.sub(r'<[^>]+>',' ',t)
t=re.sub(r'&amp;','&',t)
t=re.sub(r'&#39;',\"'\",t)
t=re.sub(r'&quot;','\"',t)
t=re.sub(r'&nbsp;',' ',t)
t=re.sub(r'&#x27;',\"'\",t)
t=re.sub(r'\s+',' ',t)
print(t[:12000])
"
```

This works for most content sites: Wikipedia, blog platforms, news sites,
documentation sites, etc. It does NOT work for:
- Sites behind DataDome or Cloudflare bot protection
- Sites that require JavaScript rendering (return empty or "enable JS")
- Sites behind paywalls

### 2b. Batch multi-URL fetching in one execute_code call (efficiency)

When you need content from many URLs at once (5–15 pages), do NOT issue
separate `terminal` calls per URL — that's 5–15 round-trips. Instead,
batch them all in a single `execute_code` block with a Python loop:

```python
import subprocess, html, re

pages = [
    ("label1", "https://example.com/page1"),
    ("label2", "https://en.wikipedia.org/wiki/Topic"),
    ("label3", "https://arxiv.org/abs/XXXX.XXXXX"),
    # ... up to ~15 URLs
]

def clean(t):
    t = re.sub(r'<script[^>]*>.*?</script>', '', t, flags=re.S)
    t = re.sub(r'<style[^>]*>.*?</style>', '', t, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = html.unescape(t)
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

for name, url in pages:
    try:
        r = subprocess.run(
            ["curl", "-sL", "--max-time", "12", "-A", "Mozilla/5.0", url],
            capture_output=True, text=True, timeout=15
        )
        text = clean(r.stdout)
        results[name] = text[:4000] if text else "(empty)"
    except Exception as e:
        results[name] = f"ERROR: {e}"

for name, content in results.items():
    print(f"\n{'='*60}\nPAGE: {name}\n{'='*60}")
    print(content[:3500])
```

This pattern fetches ~10 URLs in ~3–6 seconds total (curl runs are
I/O-bound, so they're fast even in sequence inside one Python process).
The `html.unescape()` call handles `&amp;`, `&#39;`, etc. in one shot,
so you don't need the manual regex replacements the single-URL pattern
uses.

**Truncate aggressively** (`[:4000]`) — you usually need the first few
paragraphs, not the full page. Adjust based on the question.

**Detect missing Wikipedia articles**: curl with `-L` follows redirects
to the "Wikipedia does not have an article with this exact name" page.
Many technical topics (GraphSAGE, ForceAtlas2, PyTorch-BigGraph,
multilevel graph drawing, UCSD map of science) lack dedicated articles.
If you see that boilerplate, skip the page — the content isn't there.
Check via the REST API summary endpoint first if you're unsure:

```bash
curl -sL "https://en.wikipedia.org/api/rest_v1/page/summary/Topic_Name" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('extract','NO ARTICLE')[:200])"
```

### 3. Bot-protected sites via browser_navigate

For sites that block curl (Fast Company, Medium, etc.), use
`browser_navigate`. The browser stack has stealth features that bypass
some bot protections:

```
browser_navigate(url="https://www.example.com/protected-article")
```

The browser snapshot may be large. If it's truncated, read the full
snapshot file from the cache path provided in the output.

Note: Some sites (Fast Company with DataDome) may block even the browser.
In that case, pivot to alternative sources.

### 4. Pivot to alternative sources

The most important technique: if one source is blocked, search for the
same facts elsewhere. The web is redundant — the same information is
usually available on multiple sites with different protection levels.

Real example from Aug 2026 session:
- **Goal**: Find details about Google Earth's conference demo history
- **Blocked**: Fast Company article (DataDome), Medium (JS wall),
  CNET (404), Computerworld (404)
- **Found via Brave Search**: niche blog (maphappenings.com) had
  extensive quotes from the definitive book; Substack
  (spatialintelligence.ai) had interview transcripts; Wikipedia had
  the basic timeline; goblinhouse.net had a verified facts database
- **Result**: More comprehensive research than the blocked primary
  sources would have provided, because the niche sites had unique
  details the mainstream articles didn't cover

**OpenAlex subdomain split**: `help.openalex.org` (the help center) is
behind Cloudflare and blocks curl with a JS challenge. But
`docs.openalex.org` (the developer documentation) is NOT Cloudflare-
protected and serves content cleanly via curl. When you need OpenAlex
taxonomy/concept documentation, use `docs.openalex.org` — e.g.,
`https://docs.openalex.org/api-entities/topics` works via curl, while
`https://help.openalex.org/hc/en-us/articles/...Concepts` does not.

### 5. Academic APIs (unaffected by Firecrawl status)

OpenAlex, arXiv, Semantic Scholar, and Crossref use their own endpoints
via curl — they are completely independent of Firecrawl. For any
academic/literature search, these continue to work even when managed
web tools are down. See the main SKILL.md for the full academic chain.

## Summary: tool priority when Firecrawl is down

| Need | Tool | Notes |
|------|------|-------|
| Academic papers | curl → OpenAlex/arXiv/S2 | Unaffected by Firecrawl |
| General web search | curl → Brave Search | Best tolerance |
| Page content (simple sites) | curl + regex HTML strip | Most blogs, wikis, docs |
| Page content (bot-protected) | browser_navigate | Stealth features |
| Known blocked source | Pivot to alternative domain | The web is redundant |

## What NOT to do

- Do NOT report "no data found" when the blocker was a billing error.
  The data exists — the tool is down. Use the fallback chain.
- Do NOT keep retrying `web_search` after 3 billing errors — it will
  keep failing. Switch immediately to the curl/browser chain.
- Do NOT use Google or Bing via curl for search — they return JS walls.
  Use Brave Search instead.
- Do NOT give up if a single source is blocked — pivot to alternatives.
