# Briefing the Reader's Own AI Agents (worked example, 2026-08-20)

Teammates increasingly run their own agentic systems against documents you
hand them. A deliverable now has TWO audiences: the human and her agents.
Give the agents a canonical context block so they get the project right on
first contact, and give the human per-tool setup notes.

## The canonical context block (paste-ready, any agent)

Structure: (1) what the project is, (2) the core concept in a few sentences,
(3) the hard rules, (4) who approves. Rules for writing it:
- Self-contained: no references to "the doc above"
- Accurate to the deliverable body (the voice pass cross-checks this)
- Hard rules stated absolutely: claims that must NOT be made, visual cliches
  to avoid, palette/type if design-adjacent, approval chain

Worked example (poster project for a designer):

> This project: a research poster for TSC 2026 San Diego (consciousness
> science conference), presenting "Physiomorphic AI: Engineering Consciousness
> Correlates Through Biological Isomorphism" by the principal Williams, Divinity
> Science.
>
> What Physiomorphic AI is, in short: neuromorphic AI mimics the neuron;
> Physiomorphic AI mimics the whole organism. Software agents map one-to-one
> onto body systems and do that part's real job using that system's real
> equations. The first organism built this way is called the operator agent. A score called
> I(S) measures how body-like the architecture is (the operator agent scores 0.80). The
> poster's falsifiable claim: body-shaped AI survives damage better than
> randomly wired AI (early simulation: resilience advantage 0.27).
>
> Hard rules for any output: the poster must NOT imply the operator agent is conscious or
> "feels" anything. No robot chassis, no brain-in-a-jar, no glowing-blue AI
> cliches. Brand palette: gold (#e8d5a0) and deep blue (#3d5a80) on warm
> charcoal; no purple, indigo, or teal. Type: Manrope, Sora, IBM Plex Mono.
> The audience is researchers, not students. Early results are labeled as
> early. the principal approves all sketches.

## Per-tool setup notes (what each tool is FOR + first prompts + limits)

Division of labor in one line: Perplexity researches, Figma designs, Notion
tracks. You decide. Everything they produce is a draft until approved.

**Perplexity (research assistant)**
- Setup: create a Project; paste the context block into custom instructions;
  upload the deliverable documents + any conference guideline PDFs
- First prompts: current best practices for the poster class (cite sources);
  critique this layout sketch for readability at 6 feet (attach photo)
- Limits: advises and researches, does not produce design files; citations
  are leads to verify

**Figma (design collaborator)**
- Setup: frame at exact required size; define text styles FIRST (title
  100-150pt, headers 40-60pt, body 24-32pt; viewing distance drives size);
  real content in early because the AI arranges but does not know the science
- First prompts: First Draft generation with explicit grid + section order;
  Design Agent for targeted iteration ("make Results graphs 40% larger,
  align captions to grid"); variations for layout options
- Limits: never accept its generated claims, only its layout; print
  production (CMYK, bleeds, exact DPI) is manual; encode the hard rules into
  a skills file if the team uses one

**Notion (project manager)**
- Setup: project page with context block + brief; databases for Tasks,
  Assets, Feedback Log; create a custom agent, share the page and databases
  as its knowledge sources
- First prompts: does this draft align with the brief, flag anything off;
  turn feedback entries into updated tasks; weekly status + risk summary
- Limits: only knows what is shared and kept current; scoped agents burn far
  fewer credits than general chat; manages, does not design

## Research method for these notes (capability facts, Aug 2026)
Vendor help centers were JS-walled or relocated; capability pictures were
synthesized via parallel broad-brief x_search calls (one per product:
capabilities + setup workflow + limits), then load-bearing claims (exact
feature names, menu paths) marked practitioner-reported pending a direct
fetch. Full method: `direct-source-research` skill,
`references/saas-agent-capability-research.md`.
