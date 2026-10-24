# Competitive Landscape Research — curl-Only Technique

When Firecrawl-backed tools (web_search, web_extract) are down (402 billing
error) AND browser search engines (Google, DuckDuckGo, Brave) serve CAPTCHAs,
you can still conduct full competitive landscape research using three curl
channels: Wikipedia API, direct product URLs, and raw.githubusercontent.com.

This reference captures the working patterns from a session that scanned
40+ projects/products across 10 categories with zero functioning web tools.

## Channel 1: Wikipedia API (term/product definitions)

### Single-call pattern (with rate-limit protection)

```python
from hermes_tools import terminal
import json, time

def wiki_single(title):
    t = title.replace(" ", "_")
    cmd = f'''curl -sL --max-time 15 -H "User-Agent: HermesResearchBot/1.0" \
      "https://en.wikipedia.org/w/api.php?action=query&titles={t}&prop=extracts&exintro=true&explaintext=true&format=json"'''
    result = terminal(command=cmd, timeout=20)
    raw = result.get('output', '').strip()
    if not raw:
        return title, "(empty — likely rate limited)"
    try:
        outer = json.loads(raw)
        if 'output' in outer:          # unwrap terminal wrapper
            inner = json.loads(outer['output'])
        else:
            inner = outer
        pages = inner.get('query', {}).get('pages', {})
        for pid, page in pages.items():
            return page.get('title', title), page.get('extract', '(no extract)')[:1200]
    except Exception as e:
        return title, f"PARSE ERROR: {e} | {raw[:200]}"
    return title, "(no data)"

# CRITICAL: space calls 2-3s apart to avoid rate limiting
for i, t in enumerate(titles):
    title, extract = wiki_single(t)
    print(f"### {title}\n{extract}\n")
    if i < len(titles) - 1:
        time.sleep(2)
```

### Batch API pattern (fewer calls, but also rate-limited under load)

```bash
curl -sL --max-time 20 \
  "https://en.wikipedia.org/w/api.php?action=query&titles=TermA|TermB|TermC&prop=extracts&exintro=true&explaintext=true&format=json&exlimit=max"
```

Returns empty body under rate-limit pressure. Fallback to single calls with
delays.

## Channel 2: Direct product URLs (HTML stripping)

For product/company pages that don't need JavaScript rendering:

```python
def fetch_site(url, max_chars=2000):
    cmd = f'''curl -sL --max-time 15 -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" "{url}" 2>/dev/null | python3 -c "
import sys, re, html
text = sys.stdin.read()
text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL|re.IGNORECASE)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL|re.IGNORECASE)
text = re.sub(r'<[^>]+>', ' ', text)
text = html.unescape(text)
text = re.sub(r'\\s+', ' ', text).strip()
print(text[:{max_chars}])
"'''
    result = terminal(command=cmd, timeout=20)
    raw = result.get('output', '')
    try:
        outer = json.loads(raw)
        return outer.get('output', raw)[:max_chars]
    except:
        return raw[:max_chars]
```

### What works vs what doesn't via curl

| Site type | curl result |
|---|---|
| Wikipedia API | ✅ Clean JSON |
| raw.githubusercontent.com | ✅ Clean markdown |
| Static product pages (ollama.com, localai.io, jan.ai) | ✅ Stripped HTML |
| GitHub rendered pages (github.com/org/repo) | ❌ JS nav chrome only |
| Sites with Cloudflare JS challenge (digi.me) | ❌ "Enable JavaScript" |
| ArXiv search pages | ✅ Stripped HTML with results |
| Notion/SaaS dashboards | ❌ JS-rendered |

## Channel 3: GitHub raw READMEs (project descriptions)

```python
def fetch_github_readme(owner_repo, max_chars=2000):
    for branch in ['main', 'master']:
        for fname in ['README.md', 'readme.md']:
            cmd = f'curl -sL --max-time 10 "https://raw.githubusercontent.com/{owner_repo}/{branch}/{fname}" 2>/dev/null | head -c {max_chars}'
            result = terminal(command=cmd, timeout=15)
            raw = result.get('output', '')
            try:
                outer = json.loads(raw)
                text = outer.get('output', '')
            except:
                text = raw
            if text and not text.startswith('{') and len(text) > 50:
                return text[:max_chars]
    return "(no readme found)"
```

**Key insight:** GitHub's rendered pages (github.com/org/repo) return only
navigation chrome via curl. Always use `raw.githubusercontent.com`.

## Recommended execution strategy

1. **Group titles by channel** — Wikipedia terms together, GitHub repos together,
   product URLs together.
2. **Use `execute_code` to batch** — one script per channel, with `time.sleep()`
   between calls within each script.
3. **Rate-limit management**: Wikipedia API needs 2-3s between calls.
   raw.githubusercontent.com and direct product URLs can be called faster (1s).
4. **Graceful degradation**: note which sites returned JS challenges and could
   not be fetched, rather than silently skipping them.

## Session evidence

This technique successfully researched 40+ projects across:
- Personal AI OS (Rabbit, Humane, Apple Intelligence, Gemini Nano, Galaxy AI)
- Composable AI (LangChain, LlamaIndex, AutoGPT, BabyAGI, OpenHands, Devin)
- User data platforms (Solid, Nextcloud, Digi.me, Mydex, OwnYourData)
- Agent platforms (LangGraph, CrewAI, AutoGen, MetaGPT, AgentScope, Swarm)
- Distributed computing (Plan 9, Inferno, 9front)
- Edge/IoT (Greengrass, Azure IoT Edge, Home Assistant)
- Open-source AI infra (Ollama, LM Studio, LocalAI, AnythingLLM, Jan)
- Academic papers (arXiv search via curl)
- PKM tools (Notion, Obsidian, Roam)
