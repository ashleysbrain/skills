# SaaS Agent-Capability Research via x_search (2026-08-20 session)

## Situation
Team deliverable needed current (2026) setup instructions for a designer's own AI
agents: Perplexity, Figma, Notion. Vendor help centers were JS-walled
(Perplexity hub: Cloudflare "Just a moment..."; Notion help: relocated product
pages returning 404; Figma Learn: article 404s).

## Working method (validated)
1. Batch 2-3 `x_search` calls IN PARALLEL, one per product, each framed as a
   single broad brief:
   "<Product> AI 2026 current capabilities: <named features>. How should a
   <role> set up <specific workflow>? What works, what are the limits?"
2. Each answer returned: feature inventory, step-by-step setup, concrete prompt
   patterns, and an honest limits section — everything the vendor pages would
   have shown, synthesized in minutes with practitioner citations.
3. Cross-check: run one direct curl of each vendor help page in the same turn.
   Fetches failed (challenge/404), which confirmed x_search as the only live
   source that day; load-bearing claims (exact feature names like "Projects
   (evolution of Spaces)", "custom workspace agents", "First Draft / canvas
   Design Agent") were marked practitioner-reported in internal notes.

## Findings bank (Aug 2026 snapshot, practitioner-sourced — re-verify before citing externally)
- Perplexity: Projects = Spaces evolution; custom instructions + file uploads +
  persistent memory ("Brain") + agentic Computer/Deep Research. Limits: no
  design-file output; citations are leads, not final.
- Figma: First Draft generates native layers/components; canvas Design Agent
  (2026) does targeted iteration + critique; variations for layout options;
  "skills" markdown files can encode team design rules. Limits: will invent
  wrong science content (layout only), print production manual (CMYK/bleeds).
- Notion: custom workspace agents with scoped knowledge sources (share page
  with agent), instructions, DB read/write actions, Slack/Calendar, scheduled
  runs. Limits: only knows shared+current sources; credits; manages not designs.

## Rules learned
- One broad brief-question per call beats several narrow ones (re-validated).
- Verify load-bearing x-sourced claims with a direct fetch before republishing
  as instructions.
- Team-facing deliverables NEVER mention the research workaround/outage state
  (principal 2026-08-20: "work around the problem don't whine about it in the
  outputs").
