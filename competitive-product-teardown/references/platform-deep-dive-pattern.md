# Platform Deep-Dive Research Pattern

When the user has a specific external platform open in their browser and wants a deep dive to understand its architecture for cloning or competitive purposes, use this single-agent research sequence.

## The pattern

### 1. Read the user's open tabs
The user says "it's open in Chrome." They mean their actual Chrome, not the puppeteer/headless browser session. To see what they have open:
```applescript
osascript -e 'tell application "Google Chrome"
set urls to {}
repeat with w in windows
  repeat with t in tabs of w
    set end of urls to (URL of t)
  end repeat
end repeat
return urls
end tell'
```
This returns every open URL. Find the one matching the platform they mentioned.

### 2. Pull the main marketing site
Navigate to the platform's main domain. Read the homepage snapshot. Extract:
- Core value proposition
- Pipeline stages (if it is a control plane or workflow tool)
- KPI metrics shown on the dashboard (these reveal what the platform measures)
- Pricing tiers and what they unlock
- Customer logos (signals target market)

### 3. Pull llms.txt (the fastest doc dump)
Most modern doc sites (Mintlify, ReadMe, etc.) expose `/llms.txt` at the root. This is a single text file listing every doc page with a one-line description. It is the fastest way to get the full platform map without clicking through a sidebar.
```
https://docs.<platform>.ai/llms.txt
```
Returns a structured list of all API endpoints, capability pages, and config docs. Parse it to identify the core primitives.

### 4. Read the key capability pages
From the llms.txt structure, navigate to the pages that describe the core primitives. For a factory/SDLC tool these are: Software Factory, Automations, AGENTS.md (or equivalent config), Skills, Hooks, Custom Subagents. Read each page's main content via the browser console:
```javascript
document.querySelector('article, main, .markdown-body, .prose')?.innerText?.slice(0, 8000) || document.body.innerText.slice(0, 8000)
```

### 5. Extract the architecture primitives
Build a map of:
- **Stages/pipeline** (the workflow layers)
- **Primitives** (the building blocks: agents, automations, skills, hooks, config files, sandboxes)
- **API surface** (from the llms.txt endpoint list)
- **Pricing model** (what is metered, what is flat)

### 6. Design the isomorphism (for clone-and-build tasks)
Map each external primitive to the user's own system:
- External stage → user's equivalent organ/engine/process
- External primitive → user's equivalent building block
- External physics → user's physics model (if applicable)

This produces the design document for building the user's own version.

## When to use this vs the full teardown skill
- `competitive-product-teardown` is for LANDSCAPE research (many products, multi-agent, PDF report).
- This pattern is for SINGLE-platform deep dive (one product, one agent, design document output).
- Use this when the user says "deep dive into [one platform]" or "build our own version of [one platform]."

## Session that established this pattern
2026-07-07: User asked for deep dive on 8090 Software Factory (factory.8090.ai / factory.ai). Chrome tab enumeration revealed the platform. Main site + 8090.ai + docs.factory.ai provided the six-stage pipeline (Triage, Code-gen, Validate, Release, Document, Monitor) and core primitives (Droids, Automations, Skills, Hooks, AGENTS.md, Droid Computers, Missions, Droid Shield, AutoWiki). llms.txt provided the full API surface. Result: design document for building the specialist engine as a biological software factory.
