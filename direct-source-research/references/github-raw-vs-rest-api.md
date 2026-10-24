# GitHub content fetch: raw URLs vs the REST API (2026-08-17)

For fetching GitHub-hosted content (READMEs, docs) when web tools are down:

**Use raw URLs — not the REST API — for content:**

```bash
curl -s --max-time 15 "https://raw.githubusercontent.com/Genesis-Embodied-AI/Genesis/main/README.md"
```

**Observed 2026-08-17** (external-technology-registry seeding session, web_search
and web_extract both returning Firecrawl "not configured" errors):

- `raw.githubusercontent.com/<org>/<repo>/main/README.md` → full markdown, worked first try.
- Unauthenticated `api.github.com/repos/<org>/<repo>` → empty body, `None` for
  description/stars/updated fields when parsed. Same minute, same network.

Conclusions:

1. Raw URLs are the reliable content path (already the standing guidance for
   rendered-page nav chrome; this extends it to the REST API).
2. Treat `api.github.com` as best-effort metadata only — it rate-limits hard
   unauthenticated (60 req/hr) and returned empty bodies rather than errors,
   which is worse: a parser sees valid JSON-shaped nothing instead of a failure.
3. Verify REST-API parses against a known-good field before trusting `None`s —
   empty could mean "no data" or "blocked", and you cannot tell them apart.

Companion keyless endpoints that DID work in the same session:
`https://huggingface.co/api/models?search=<q>&author=<org>&limit=20` (live
downloads, no key) — see `references/hf-arxiv-keyless-landscape.md`.
