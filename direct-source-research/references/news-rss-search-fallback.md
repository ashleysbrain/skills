# News RSS as a search surface (verified 2026-08-14)

When every SERP (DDG, Bing, Brave, Mojeek, Startpage) serves bot challenges,
**news RSS endpoints do not captcha** and are the fastest reliable discovery
surface for current-events / market / landscape research. This was the
breakthrough of the 2026-08-14 AI-eval market research session: ~20 queries,
zero blocks, full headline+date coverage of the topic.

## 1. Google News RSS search (primary)

```bash
curl -sL "https://news.google.com/rss/search?q=AI+evaluation+market+funding&hl=en-US&gl=US&ceid=US:en"
```

- Returns up to ~100 `<item>` blocks: `<title>`, `<link>`, `<pubDate>`.
  Title carries the source suffix (e.g., "... - TechCrunch").
- Append `+when:1y` / `+when:7d` to the query for recency windows.
- Queries work like Google: quoted phrases, multiple terms (AND).

**Decoding item links:** `<link>` values are Google News redirect URLs
(`news.google.com/rss/articles/<base64url>`). Fetching them returns a JS-only
interstitial — never fetch them. Decode instead:

```python
import base64, re
def decode_gnews(url):
    s = re.search(r'articles/([^?]+)', url).group(1)
    s += "=" * (-len(s) % 4)          # pad
    raw = base64.urlsafe_b64decode(s)
    for u in re.findall(rb'https?://[^\x00-\x1f\x22\x27\\]+', raw):
        u = u.decode('utf-8', 'ignore')
        if 'google' not in u and 'gstatic' not in u:
            return u                    # first non-Google URL = article
```

Works most of the time; when it fails, use technique 2 or the title's source
suffix to guess the publisher and fetch its own search feed (technique 3).

## 2. Bing News RSS (secondary; easiest URL recovery)

```bash
curl -sL "https://www.bing.com/news/search?q=<query>&format=RSS"
```

Item links are `bing.com/news/apiclick.aspx?...&url=https%3a%2f%2fventurebeat.com%2F...`
redirects — **the real article URL is in the `url=` percent-encoded param**,
trivially decodable. When Google's base64 decode fails, search the same query
on Bing News RSS and read the `url=` param.

## 3. Publisher feeds direct (bypass search engines entirely)

Content sites captcha their search pages but leave RSS/WordPress endpoints open:

| Publisher | Endpoint | Notes |
|---|---|---|
| TechCrunch | `https://techcrunch.com/search/<urlencoded>/feed` | full direct links |
| Any WordPress site | `https://site.com/?s=<query>&feed=rss2` | works on most WP |
| Any site | `https://site.com/feed/` | latest ~10 posts, direct links |
| VentureBeat | `https://venturebeat.com/feed/` | CDATA descriptions ~400 chars — article bodies themselves sit behind a Vercel bot checkpoint on direct fetch, but the feed summaries are usable |

## 4. Extraction pipeline shape that worked

```python
def gnews(query, n=8, when="1y"):
    rss = fetch(f"https://news.google.com/rss/search?q={query.replace(' ','+')}+when:{when}&hl=en-US&gl=US&ceid=US:en")
    return [(title, link, date) for title, link, date in
            re.findall(r'<item><title>(.*?)</title><link>(.*?)</link>.*?<pubDate>(.*?)</pubDate>', rss)[:n]]
```

Loop: run 6-10 headline sweeps across query angles (market size, funding,
viral, demand, competitors) → pick high-value articles by title → fetch
direct URLs via curl + tag-strip → only extract bodies for the 3-5 articles
that matter. Headlines alone carry ~60% of the research value at ~5% of the
fetch cost.

Pair with `x_search` (SKILL.md technique 0) for viral/sentiment signals and
money flow — RSS gives the facts, X gives the temperature.

## Pitfalls from this session

- **Regex catastrophic backtracking**: SERP/article HTML is 100-600KB. A
  multi-group regex with `.*?` between href/title/snippet groups pegged the
  CPU and killed a 300s execute_code budget. Use linear scanning: iterate
  `href="..."` matches, take a FIXED byte window after each (e.g. 3000 bytes),
  strip tags, use window text as pseudo-snippet. Never `.*?` across raw page
  bodies.
- **Market-research SEO sites** (market.us, dataintelo etc.): numbers split
  across spans or behind Cloudflare. Extract sentences matching
  `[^.]*(USD|CAGR|billion)[^.]*\.` instead of structured fields; dataintelo
  was fully Cloudflare-blocked.
- **Vercel Security Checkpoint** on some publisher article pages (VentureBeat
  orchestration section, Aug 2026): direct curl gets a 167-byte challenge. The
  site's own `/feed/` still works — use feed descriptions or Bing News RSS
  snippets for those stories.
