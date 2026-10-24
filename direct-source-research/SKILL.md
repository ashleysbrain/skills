---
name: direct-source-research
description: Fetch content via curl when web tools are down.
version: 1.0.0
author: the operator agent
license: MIT
metadata:
  hermes:
    tags: [research, web-fallback, curl, wikipedia-api, github-raw]
    category: research
    related_skills: [duckduckgo-search, technical-research-planning, grounded-citations]
---

# Direct-Source Research (curl fallback)

When managed web tools (`web_search`, `web_extract`) return billing errors,
CAPTCHAs, or are otherwise unavailable, `curl` in `terminal` fetches clean
structured data directly from authoritative sources — no browser stack, no API
keys, no Firecrawl dependency.

## MANDATORY: subagent dispatch injection block (principal directive 2026-08-20)

Dispatched subagents do NOT inherit loaded skills. Any dispatch whose goal
involves web research MUST paste this block into the goal/context verbatim:

```
TOOL FALLBACK PROTOCOL (mandatory, use immediately on first failure):
- If web_search/web_extract errors ("not configured"/billing): do NOT report
  a blocker. Pivot at once to curl in terminal: curl -sL -m 15 "<url>"
- Discovery when SERPs block: x_search tool (tool_search "x search" ->
  tool_describe -> tool_call), batch 2-3 broad brief-style questions.
- News discovery: Google News RSS https://news.google.com/rss/search?q=<q>
  and Bing News RSS .../search?q=<q>&format=RSS (never captcha-gated).
- Clean definitions: Wikipedia API action=query&prop=extracts&exintro=1.
- Open-source docs: raw.githubusercontent.com/<org>/<repo>/main/<path>.
- Blocked/404/paywalled page: Wayback archive.org/wayback/available?url=<URL>,
  then archive.ph/.md/.li/.is rotation; cite snapshot dates.
- HTML strip: remove <script>/<style> BEFORE tags; extract <meta> tags for
  JS-rendered SPAs.
- Verify every fetch: check body contains expected terms, not just HTTP 200.
```

Failure pattern this kills (2026-08-20, poster census): subagent burned 40+
API calls fighting CDP/Bing, hit its iteration cap, and delivered a truncated
census — while the entire fallback chain sat unused in the parent's skill
library. Tool failure is NEVER a research blocker; it is a routing event.

This skill complements `duckduckgo-search` (which covers the *search* layer)
and `technical-research-planning` (which covers the *planning* layer). This
skill covers the *data-retrieval* layer: getting actual page content when the
managed extraction pipeline is down.

## When to use

- `web_search` / `web_extract` return 402 billing errors or CAPTCHA blocks
- You need clean JSON definitions (Wikipedia API)
- You need raw markdown from open-source project docs (GitHub)
- You need to batch-fetch multiple definitions in one call
- Browser navigation is too heavy for a simple text fetch

## Core techniques

### 0. `x_search` (xAI/Grok) — live-research fallback when search engines block

When you need *research answers* (not specific pages) and every search engine
is bot-blocking curl, the deferred `x_search` tool is often the strongest
fallback — stronger than scraping SERPs. It runs the query through xAI's
built-in X/live-web search and returns a synthesized, citation-backed answer
with inline X-post links (Grok reasoning model under the hood).

Load via `tool_search("x search")` → `tool_describe("x_search")` → `tool_call`.

Best practices (validated 2026-08-14, AI-eval market research session where
DDG/Bing/Mojeek/Brave ALL blocked curl and web_search/web_extract were down):
- **One broad research-brief question per call beats several narrow ones.**
  Frame it like a brief: "What are the documented failure modes of X? Include
  statistics and named studies."
- Answers include practitioner-survey stats and named studies (e.g., "306
  practitioners, 20 case studies, 26 domains") with X-post citations in
  `x.com/<handle>/status/<id>` form.
- Calls are independent — **batch 2-3 in parallel** in one turn.
- Caveats: individual X-post citations are not independently verified — treat
  cited stats as practitioner-reported and say so in your output. Read-only
  discovery only (no posting).
- Uses separate xAI credentials, so it works even when `web_search`/
  `web_extract` return the Firecrawl "not configured" billing error.

### 1. News RSS search — Google News RSS + Bing News RSS (PRIMARY discovery fallback)

When every SERP bot-blocks curl, news RSS endpoints do NOT captcha and are the
fastest discovery surface for current-events / market / landscape research.
This outperformed every SERP scraper in the 2026-08-14 AI-eval market session
(~20 queries, zero blocks).

```bash
curl -sL "https://news.google.com/rss/search?q=AI+evaluation+market&hl=en-US&gl=US&ceid=US:en"
# append +when:1y / +when:7d to the query for recency windows
curl -sL "https://www.bing.com/news/search?q=<query>&format=RSS"
```

Key mechanics:
- Google News item links are base64url redirects — decode the segment after
  `articles/` (pad with `=`, regex out first non-Google https URL). NEVER
  fetch the redirect itself (JS interstitial).
- Bing News item links are `apiclick.aspx` redirects with the real URL in the
  percent-encoded `url=` param — easiest URL recovery when Google's decode fails.
- Publisher feeds bypass search entirely: TechCrunch `/search/<q>/feed`,
  WordPress sites `/?s=<q>&feed=rss2`, any site `/feed/`.
- Workflow: 6-10 headline sweeps across query angles → fetch direct URLs for
  only the 3-5 articles that matter. Headlines carry most of the value.
- CAUTION: multi-group `.*?` regexes over 100-600KB SERP/article HTML cause
  catastrophic backtracking (killed a 300s execute_code budget). Use linear
  href-iteration with fixed byte windows.

Full code + pitfalls: `references/news-rss-search-fallback.md`.

### 2. Wikipedia REST API — clean JSON intro extracts

Returns the first paragraph(s) of any Wikipedia article as plain text. This is
the fastest way to get canonical definitions for technical terms.

```bash
curl -sL --max-time 15 \
  "https://en.wikipedia.org/w/api.php?action=query&titles=Test_harness|Service_mesh|Data_mesh&prop=extracts&exintro=1&explaintext=1&format=json" \
  | python3 -c "
import json,sys
d=json.load(sys.stdin)
for pid,page in d['query']['pages'].items():
    print('===',page.get('title','?'),'===')
    print(page.get('extract','')[:1200])
    print()
"
```

Key params:
- `titles=A|B|C` — pipe-separate multiple titles in one call (batch)
- `exintro=1` — intro section only (concise definitions)
- `explaintext=1` — plain text, no wiki markup
- `prop=extracts` — get article extracts

For full-page content (not just intro), drop `exintro=1`.

### 3. raw.githubusercontent.com — project docs and READMEs

Most open-source project docs live as markdown in GitHub repos. Fetch directly:

```bash
curl -sL --max-time 15 \
  "https://raw.githubusercontent.com/kubernetes/website/main/content/en/docs/concepts/extend-kubernetes/operator.md"
```

**URL pattern:** `https://raw.githubusercontent.com/<org>/<repo>/<branch>/<path>`

Common docs repos to know:
- `kubernetes/website` — Kubernetes docs
- `istio/istio.io` — Istio docs
- `langchain-ai/langgraph` — LangGraph docs (under `docs/`)
- `microsoft/autogen` — AutoGen README and docs
- `EleutherAI/lm-evaluation-harness` — LM eval harness
- `<org>/<repo>` — any project's README.md at repo root

Returns raw markdown — no HTML stripping needed.

### 4. Plain HTML pages (product sites, blogs, docs)

For pages without an API or raw markdown, curl + HTML stripping.
**Critical for modern product/marketing sites:** strip `<script>` and `<style>`
blocks *before* tag removal — otherwise the output is dominated by embedded JS
bundles and CSS (Sunsama, Motion, Reclaim, Linear, etc. all ship 100KB+ of
inline JS that drowns the actual content).

```bash
curl -sL --max-time 15 "https://www.usemotion.com/" \
  | python3 -c "
import sys, re, html
text = sys.stdin.read()
# Strip scripts and styles FIRST (before tag removal)
text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.S|re.I)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.S|re.I)
# Then strip remaining tags
text = re.sub(r'<[^>]+>', ' ', text)
text = html.unescape(text)
text = re.sub(r'\n\s*\n', '\n', text)
text = re.sub(r'  +', ' ', text)
# Print only non-trivial lines
lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 2]
print('\n'.join(lines[:100]))
"
```

**Batch-fetching multiple product pages** (efficient for competitive research —
single terminal call, multiple URLs, parallel-safe since curl calls are
independent):

```bash
for url in \
  "https://www.sunsama.com/" \
  "https://www.usemotion.com/" \
  "https://linear.app/" \
  ; do
  echo "===== $url ====="
  curl -sL --max-time 15 "$url" | python3 -c "
import sys, re, html
text = sys.stdin.read()
text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.S|re.I)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.S|re.I)
text = re.sub(r'<[^>]+>', ' ', text)
text = html.unescape(text)
text = re.sub(r'\n\s*\n', '\n', text)
text = re.sub(r'  +', ' ', text)
lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 2]
print('\n'.join(lines[:80]))
"
done
```

This pattern was validated across 10+ SaaS product sites (2026-08-09) in a
single session — extracted feature lists, pricing, and product positioning
from Sunsama, Motion, Reclaim, Linear, OmniFocus, Things 3, Akiflow, Routine,
and Taskwarrior docs pages, producing a full competitive gap analysis with zero
web_search/web_extract calls (all three were down with billing errors).

### 5. Multi-term batch lookup pattern

For definition-disambiguation tasks (like "what exactly does X mean across N
sources?"), batch the lookups:

1. Single Wikipedia API call with pipe-separated titles (one HTTP request)
2. Parallel `curl` calls for independent GitHub raw URLs (batch in one terminal call)
3. Aggregate results into a comparison table with sources cited

Example — batch fetch 5 Wikipedia terms + 3 GitHub repos in two terminal calls:

```bash
# Call 1: Wikipedia batch
curl -sL "https://en.wikipedia.org/w/api.php?action=query&titles=Term1|Term2|Term3|Term4|Term5&prop=extracts&exintro=1&explaintext=1&format=json" | python3 -m json.tool

# Call 2: GitHub batch (parallel-safe, no dependencies)
for url in \
  "https://raw.githubusercontent.com/org1/repo1/main/README.md" \
  "https://raw.githubusercontent.com/org2/repo2/main/docs/concepts.md" \
  "https://raw.githubusercontent.com/org3/repo3/main/index.md"; do
  echo "=== $url ==="
  curl -sL --max-time 10 "$url" | head -80
  echo
done
```

## When to prefer curl vs browser_navigate vs ddgs

| Situation | Prefer |
|---|---|
| Firecrawl/web_search/web_extract down | `curl` (this skill) |
| Need clean JSON (Wikipedia API) | `curl` + `python3 -m json.tool` |
| Fetching raw markdown (GitHub) | `curl` raw URL |
| Need to discover URLs first | `ddgs` (duckduckgo-search skill) |
| Need to click/fill forms/render JS | `browser_navigate` |
| Page requires auth/cookies | `browser_navigate` |

## Advanced technique: parallel batch fetching via execute_code

For fetching 10+ independent URLs, use `execute_code` with
`concurrent.futures.ThreadPoolExecutor` instead of sequential shell loops.
This is 5-10x faster than the `for url in ...; do curl ...; done` shell pattern
because curl calls are I/O-bound and fully parallel-safe.

```python
import subprocess, re, html, concurrent.futures as cf

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"

def fetch(url, timeout=25):
    try:
        out = subprocess.run(["curl","-sL","--max-time",str(timeout),"-A",UA,url],
                             capture_output=True, text=True, timeout=timeout+5).stdout
        return url, out
    except Exception as e:
        return url, f"ERR: {e}"

def clean(raw):
    raw = re.sub(r'<script[\s\S]*?</script>', ' ', raw, flags=re.I)
    raw = re.sub(r'<style[\s\S]*?</style>', ' ', raw, flags=re.I)
    text = re.sub(r'<[^>]+>', ' ', raw)
    text = html.unescape(text)
    return re.sub(r'\s+', ' ', text).strip()

urls = ["https://...", "https://...", ...]
with cf.ThreadPoolExecutor(max_workers=10) as ex:
    for url, raw in ex.map(fetch, urls):
        print(f"=== {url} ===\n{clean(raw)[:800]}\n")
```

Also extract `<meta>` tags before stripping — see SPA-site pitfall below.

## Pitfalls

- **Search-engine query endpoints captcha-gate programmatic requests**: DuckDuckGo (`duckduckgo.com/html/?q=...`) and Bing (`bing.com/search?q=...`) both detect and block automated search queries — DDG returns its homepage with no results, Bing returns a "solve the challenge" captcha page. This is structural bot detection, not a transient failure. **Alternative:** fetch known source URLs directly (product homepages, Wikipedia articles, docs pages) — direct URL fetches are NOT captcha-gated. If you need to *discover* URLs and ddgs/search are blocked, use your existing knowledge of likely domains (e.g., `tool-name.com`, `en.wikipedia.org/wiki/Tool_Name`) rather than relying on a search query.
- **Every SERP scraper blocks quickly, and blocks are IP-level (learned 2026-08-14)**: in one session, DuckDuckGo served an `anomaly.js` bot page, Bing soft-blocked after ~3 parses (valid HTML, zero `b_algo` results), Mojeek returned `403 Forbidden — your network appears to be sending automated queries` after ~6 queries even with 2s spacing, and Brave served a captcha then redirected results to `tb-manual.torproject.org` — a 20s cooldown did NOT lift the block. Lessons: (1) harvest whatever the first 1-2 successful SERP responses contain before burning more queries; (2) don't burn turns retrying engines with delays — switch strategies to direct URL fetches or `x_search` (technique #0); (3) Bing redirect URLs decode via `u=a1<base64url>` in the href.
- **SPA / JS-rendered sites return empty body text**: Connected Papers, Consensus.app, and many modern SaaS sites are single-page apps where curl gets only a `<div id="app">` shell with no content. **Extract `<meta>` tags** — they carry `description`, `og:title`, `og:description` populated server-side for SEO/social sharing, even when the body is JS-rendered. Extract BEFORE stripping tags:
  ```python
  meta = re.findall(r'<meta\s[^>]*(?:name|property)=["\']([^"\']+)["\'][^>]*content=["\']([^"\']*)["\']', raw, flags=re.I)
  ```
  This recovered Connected Papers' tagline, description, and feature positioning from a page whose body text was just "Please enable JavaScript."
- **Cloudflare JS challenge per-site**: Consensus.app and Scholarcy return "Just a moment... Enable JavaScript and cookies to continue." These sites cannot be fetched via curl at all — note them and seek alternative sources (Wikipedia, comparison articles, review sites) rather than retrying.
- **Third-party comparison articles are often richer than primary sources**: for competitive landscape research, articles like tesify.app or ponder.ing that compare multiple tools side-by-side yield more structured data (pricing tables, feature matrices, limitations) than individual tool homepages. When a tool's own page is JS-gated, a comparison article that covers it is the best fallback.
- **Wikipedia article-page fetches may return "does not have an article"**: fetching `en.wikipedia.org/wiki/Some_Tool_Name` for a tool with no Wikipedia article returns a 200 with a "look for this title" stub page. Check for this marker before trusting the extract; the Wikipedia REST API (technique #1 above) is more reliable for existence checking.
- **Rate limiting**: add `--max-time 15` to avoid hanging on slow/dead servers
- **Wikipedia API rate limiting (learned 2026-08-08)**: rapid sequential calls (~4-5 within seconds) hit "You are making too many requests to the API." The batch API (`titles=A|B|C&exlimit=max`) also returned empty responses under load. **Fix:** add `time.sleep(2)` between sequential calls in `execute_code`, and retry the batch with longer delays if empty. The `User-Agent` header does not prevent rate limiting. For large lookups (10+ terms), space calls ~2-3s apart or split into smaller batches of 3-4 titles.
- **GitHub rendered pages return only nav chrome**: fetching `github.com/org/repo` via curl or browser returns JavaScript-rendered navigation boilerplate, not README content. **Always use `raw.githubusercontent.com/org/repo/main/README.md`** for actual content. If `main` 404s, try `master`.
- **Terminal output double-unwrap in execute_code**: when calling `terminal()` from an `execute_code` script, the return is `{"output": "<curl_output>", "exit_code": 0}`. If the curl output itself is JSON (e.g., Wikipedia API), you must `json.loads()` twice — first to unwrap the terminal wrapper, then to parse the inner JSON. See the patterns in `references/competitive-landscape-curl-only.md`.
- **404s on raw GitHub URLs**: the branch might be `main` or `master`, and the
  path structure varies per repo. If a raw URL 404s, check the repo's file tree
  to find the right path and branch.
- **Redirects**: always use `-L` flag to follow redirects
- **Large pages**: pipe through `head` or use Python slicing to avoid flooding
  context with massive pages
- **Wikipedia title mismatches**: `Erlang/OTP` has no Wikipedia article — the
  article is `Erlang_(programming_language)`. Use the Wikipedia search API or
  guess the canonical title. Pipe-separated titles that don't match just return
  empty extracts, they don't error.
- **JavaScript-rendered pages**: curl gets the raw HTML only. If content is
  client-rendered (Next.js SSR apps like docs.langchain.com), the body may be
  JSON RSC payloads, not readable text. Fall back to `browser_navigate`.

## Reference files

- `references/task-planning-product-gap-analysis.md` — competitive gap analysis of 10 task-management/weekly-planning products (Sunsama, Motion, Reclaim, Linear, OmniFocus, Things 3, Akiflow, Routine, Taskwarrior, + weekly review frameworks). Includes reusable gap-analysis output structure, Taskwarrior urgency formula coefficients, AI-agent dual-lane pattern, and weekly review framework summaries.
- `references/architecture-term-definitions.md` — condensed comparison tables for harness, mesh (cross-discipline: software + networking protocols + topology + geometry + physics + biology + hardware + physical device meshing), platform/framework/runtime/orchestrator/registry/connector/adapter, and composable-OS layer patterns. Includes the Three-Layer Mesh Model (Physical / Logical / Semantic) for composable OS architecture, the network-vs-topology-vs-fabric distinction, and a cross-discipline mapping table. All sourced from primary references.
- `references/competitive-landscape-curl-only.md` — full working patterns for conducting large-scale competitive research (40+ projects, 10 categories) using only curl when web_search, web_extract, AND browser search engines are all unavailable. Includes Wikipedia API rate-limit management, direct product URL fetching, GitHub raw README patterns, and terminal output double-unwrap technique.
- `references/research-discovery-tools-landscape.md` — condensed knowledge bank of the cross-disciplinary research discovery & knowledge mapping tools market (20+ tools across 4 tiers: literature mapping, AI search, bibliometric network analysis, open data infrastructure). Includes pricing, capabilities, limitations, and a 7-point gap analysis identifying cross-disciplinary serendipity as the key underserved niche. Re-verify pricing before citing (2026-08 snapshot).
- `references/ai-evaluation-market-pain-points.md` — knowledge bank of AI-evaluation practitioner pain points (2026-08-14, x_search-sourced): eval statistics (75% no formal benchmarks, ~88% agent pilots fail, 37% benchmark-to-production drop), silent-failure/trajectory-integrity findings, LLM-as-judge and METR/RE-Bench benchmark criticisms, enterprise trust requirements, and the diagnosed market gap (post-deployment diagnostic layer between monitoring and benchmarking). Stats are practitioner-reported, unverified — re-check before external citing.
- `references/news-rss-search-fallback.md` — full working code for the Google News RSS / Bing News RSS / publisher-feed discovery chain (2026-08-14): base64url decoding of Google redirect links, `url=` param recovery from Bing apiclick redirects, TechCrunch/WordPress search feeds, the headline-sweep-then-deep-fetch workflow, and the regex-backtracking timeout pitfall. Use when SERPs block but you need current-news discovery, not just known-URL fetches.

## Verification

- Confirm each curl returned exit code 0 (non-zero = network/HTTP error)
- Spot-check that extracted text contains expected terms
- For definition research, cross-reference at least two independent sources
  (e.g., Wikipedia + project docs) before citing
