---
name: official-docs-product-research
description: Research current capabilities, limits, pricing tiers, sharing/export behavior, and privacy posture for SaaS products by pulling directly from official help/docs pages when search engines are noisy or blocked.
version: 1.0.0
author: the operator agent
license: MIT
metadata:
  hermes:
    tags: [research, product-analysis, documentation, saas, support-pages]
---

# Official Docs Product Research

Use this when the goal is to produce an implementation brief, capability assessment, or operational recommendation for a product like NotebookLM, Notion, Workspace, etc., and you need current facts more than broad web commentary.

## When to use
- User asks for "current capabilities," "limits," "setup requirements," "best practices," or "what should/should not this be used for"
- Search engines are blocked by CAPTCHAs, rate limits, or noisy SEO pages
- Official help/support pages are likely the highest-quality source
- You need exact limits/tables, not just a narrative summary

## Workflow

1. Start from the vendor help center or official docs root
   - Prefer URLs like `support.google.com/...`, `help.notion.so/...`, `docs.vendor.com/...`
   - Use browser navigation for page discovery if needed
   - Avoid relying on general web search unless official docs are hard to find

2. Map the likely subtopics before diving in
   Common buckets:
   - overview / product basics
   - setup / eligibility / availability
   - limits / quotas / plans / pricing tiers
   - source/file/input types
   - sharing / collaboration / permissions
   - export / portability
   - citation / provenance / accuracy behavior
   - privacy / training / data handling
   - feature-specific pages (audio, video, reports, etc.)

3. Use browser tools for discovery, then direct fetch/parsing for extraction
   - Browser snapshot is good for finding article links and confirming page structure
   - If long pages are truncated in browser snapshots, fetch the page HTML with `execute_code` + `requests`
   - Parse tables/rows with regex or lightweight HTML cleanup if BeautifulSoup is unavailable

4. Extract exact facts, not impressions
   Capture concrete items like:
   - supported source/file types
   - per-item size/token/word limits
   - per-user or per-day quotas
   - plan-tier differences
   - whether exports sync back or not
   - sharing limitations by account type
   - privacy/data-use distinctions between consumer and enterprise/workspace plans

5. Normalize the findings into operational guidance
   Translate product facts into:
   - what it should be used for
   - what it should not be used for
   - fastest path to value
   - target operating model
   - phased rollout plan

6. Separate product truth from operating recommendations
   Structure output as:
   - verified platform facts
   - implications for the user's environment
   - recommended workflow / governance model

## Tactics that worked

### If search engines fail
- Go directly to the official help center homepage
- Browse topic categories manually
- Open likely pages such as "Learn about", "Upgrade", "Use with work or school account", "Add sources", etc.

### If browser snapshots truncate long pages
Use `execute_code` with `requests` to fetch the help page HTML and then extract tables/snippets.
Example pattern:

```python
import requests, re
from html import unescape
text = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"}).text
rows = re.findall(r'<tr>(.*?)</tr>', text, re.S)
for row in rows:
    cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', row, re.S)
    cleaned = []
    for c in cells:
        c = re.sub(r'<br\\s*/?>', ' | ', c)
        c = re.sub(r'</p>', '\n', c)
        c = re.sub(r'<.*?>', ' ', c)
        c = unescape(c)
        c = ' '.join(c.split())
        cleaned.append(c)
    if cleaned:
        print(' || '.join(cleaned))
```

### If package availability is limited
- Do not assume `bs4` or `ddgs` is installed
- Fall back to stdlib + `requests` + regex cleanup
- Treat browser navigation + direct fetch as the robust default

## Output template

1. Executive decision
2. Current capabilities relevant to the user
3. What the product should be used for
4. What it should not be used for
5. Fastest path to operational value
6. Target operating model
7. Phased rollout plan
8. Licensing/account recommendation if relevant
9. Bottom line
10. Source notes used

## Pitfalls
- Do not over-trust third-party blogs when official help pages exist
- Do not assume exports round-trip back into the product
- Do not confuse consumer sharing behavior with Workspace/enterprise behavior
- Do not treat usage limits as universal; capture tier-specific differences
- Long official help pages often hide the most important limits inside tables far below the fold

## Validation checklist
- Have you verified limits from an official page rather than inferred them?
- Have you checked account-type differences (consumer vs workspace/enterprise)?
- Have you captured sharing/export/privacy constraints?
- Have you translated product facts into a concrete operating model for the user?
