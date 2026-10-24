---
name: brand-naming-ideation
description: Generate and refine branded name options, especially coined variants and semantically consistent name families, with compact meanings.
category: creative
---

# Brand Naming Ideation

Use when the user asks for names, codenames, brand labels, product names, agent names, or wants “more like X”, “more dark”, “more scientific”, “more divine”, etc.

## Operating rules
1. Preserve the semantic lane of the best seed name. When the user says “similar to the specialist engine,” mutate suffixes/prefixes/phonemes — do not restart from scratch.
2. Return options with one-line coined meanings. If the name is invented, label the meaning as an intended interpretation, not etymology.
3. Prefer compact bullet lists. Avoid tables.
4. If the user rejects a batch, respond with a fresh batch in the same family first; don’t explain the old batch.
5. Offer 5-10 names unless the user asks otherwise.
6. Match the requested tone: darker, scientific, divine, elegant, etc. Keep the rest stable.
7. Give one or two best picks if the user asks for judgment, but do not dominate the reply with analysis.
8. Avoid generic or over-literal names unless the user explicitly wants them.

## Naming patterns
- For one seed name, generate:
  - close phonetic cousins,
  - same-root variants,
  - suffix-shift variants,
  - meaning-shift variants.
- Maintain consistent structure where possible (e.g. `DS` + coined stem).
- If the user wants a “system,” suggest a family scheme rather than one-off names.
- If the user distinguishes an *agent* from a *system*, return both layers explicitly.
- For AI health / coaching products, keep the system name and the agent name separate when the user asks for both.
- If the user wants an 8D-related line, keep the 8D marker in the system name family unless the user explicitly wants it on the agent name too.
- Prefer names that make the role obvious at a glance, especially when the user is designing a multi-part architecture (e.g. agent, engine, system, module).

## Agent/system split
- Use the agent name for the persona or operator that manages the workflow.
- Use the system name for the underlying engine, platform, or product layer.
- When the user assigns both, preserve the mapping and do not merge them into one label.
- Return a clean architecture suggestion if the naming space is getting crowded: `agent -> system -> module`.

### Reference
- See `references/close-variant-patterns.md` for the Quorinth-style variant pattern and sample response rules.
- See `references/agent-system-naming.md` for a session note on separating agent names from system names in 8D AI product architecture.
- If the user is naming a product adjacent to an existing engine, first separate the semantic lane: coach/orchestrator, AI health, maintenance/operator, or specialist module. Do not reuse the same core brand token across distinct lanes.
- For AI-health engines, favor 8D-linked names that feel system-level rather than human-behavior-literal.

## Session reference
- See `references/ds-wave-vs-ai-health-naming.md` for the the specialist engine vs AI-health naming distinction and preferred 8D naming patterns.
- See `references/process-naming-etymology.md` for the Veritas/Crucible naming session (2026-08-03): metallurgical depth bar, generic name rejection, etymological family expansion pattern.
- See `references/real-word-acronym-naming.md` for the the OS OS naming session (2026-08-08): real-word acronym pattern for products/categories, rejection of coined neologisms, naming hierarchy by component type.

## Output format
- Name
- Meaning (one line)
- Optional note if pronunciation or connotation matters

## Pitfalls
- Do not over-explain word origins for coined names.
- Do not introduce a totally new aesthetic after user rejection unless asked.
- Do not mix unrelated naming styles in one batch.
- Do not drift out of the user’s requested industry/brand lane when they narrow it (e.g. keep science/health if that is the stated brand identity).
- Avoid generic AI-product vibes when the user is trying to build a distinctive science/health brand.
- Do not use tables in Telegram-facing responses.
- **Generic name rejection (learned 2026-08-03):** When the user says "Not any of these generic ai names. Find something intriguing and unique," they mean: common tech words (CIPHER, FORGE, BRIDGE, VAULT, SHIELD, AEGIS) are REJECTED on sight. The user wants names with ETYMOLOGICAL DEPTH — real origins in Latin, Greek, metallurgy, mathematics, or historical engineering. Every candidate must have a traceable origin story, not just a "cool sounding" word. When the user says "give me more like X," mutate within the same etymological family (e.g. if CRUCIBLE was liked, explore ANNEAL, TEMPER, BESSEMER — same metallurgical depth, not generic tech words). The rejection of generic names is a QUALITY BAR, not a preference for a different style.
- **AI-generated neologisms are REJECTED (learned 2026-08-08):** When the user says "those are terrible AI-generated names," they mean coined words with Latinate suffixes (Holonos, Kompoza, Composon, Weavos, Stakos) SOUND like AI output and are REJECTED. For PRODUCT and CATEGORY names (not engine/agent names), the user prefers ACRONYMS FROM REAL DESCRIPTIVE WORDS where the acronym spells a real word related to the concept. the OS = "Modular Open System for AI Interconnectivity and Composition" — accepted immediately. CORAL, SCION, LOOM, SPINE were also well-received candidates. This is a different preference from engine naming (which uses real scientist names). Product names = real-word acronyms; engine names = scientist names; process names = metallurgical etymology.
- **Whois rate-limiting produces FALSE AVAILABLE results (learned 2026-08-11):** When checking domains with `whois -h whois.verisign-grs.com`, Verisign and nic.io THROTTLE under parallel load and return a short (~150-char) response with NO registration data AND NO "no match" availability marker. Naive inline classification logic that treats "not taken => available" will FALSELY mark registered domains as AVAILABLE (shuttle.com, lumens.com, traverse.com all came back as false AVAILABLEs during a rate-limited batch). The bundled `scripts/domain-availability-check.py` now (a) forces short responses to UNKNOWN, (b) retries UNKNOWNs with backoff, and (c) caps parallelism at 8 workers. ALWAYS use the script, not inline whois logic. And when writing inline checks, never infer availability from absence of registration data alone — require an EXPLICIT availability marker.

## Domain availability checking (when names are for a real brand/company)
When the user wants company/product names they can actually register, check domain availability in the SAME pass — don't hand back a name whose domains are all squatted.

**Critical technique — do NOT use plain `whois <domain>`:** On macOS the default whois client hits the IANA server and returns the generic *registry* record (e.g. `domain: COM`), not the registrar record for the specific domain. Every domain looks identical, so naive classification marks 100% as taken. Query the authoritative registry servers directly:

- `whois -h whois.verisign-grs.com <name>.com` → available marker: `no match for domain`
- `whois -h whois.nic.io <name>.io` → available markers: `domain not found` / `is free`
- `whois -h whois.nic.ai <name>.ai` → available markers: `domain not found` / `not found`

Run all lookups **in parallel** (`concurrent.futures.ThreadPoolExecutor`) — serial whois over 20+ name×TLD combos takes minutes and frequently times out.

**Variant choice:** use `.com` / `.io` / `.ai` as variants. Do NOT check `<name>.labs.com` or other subdomains — whois cannot resolve arbitrary subdomains (they aren't separately registered) and returns the parent's registry record, producing false results.

**Naming implication (learned 2026-08-11):** literal Latin/Greek dictionary words (aletheia, episteme, gnosis, numen, telos) are essentially 100% squatted across all TLDs. Coined/derivative names from roots (eidolio from eidos, daedral from Daedalus, alethian from aletheia) are the ones with available domains — the Palantir/Anduril/Anthropic coined-from-roots pattern is not just aesthetic, it's what makes .com/.io obtainable. Generate the coined layer, not the raw dictionary word.

**Use the bundled checker:** `scripts/domain-availability-check.py` runs the parallel check correctly. Call `check(["name1","name2",...])` or run `python3 scripts/domain-availability-check.py name1 name2`. Only surface candidates with ≥1 AVAILABLE domain; re-query UNKNOWNs once before reporting.

## Diverse-source naming (for subsidiaries / real companies)
When the user wants company/subsidiary names that must be REGISTERABLE and asks for DIVERSE SOURCES (not one root family), pull from multiple concrete domains in the same batch: craft/trade, architecture, navigation/cartography, structural biology, chemistry/materials, music/acoustics, optics/light. NOT Greek/Latin philosophy, NOT generic tech words.

**The availability gradient (learned 2026-08-11) — critical for real-registration requests:**
1. Common single dictionary words (kiln, gimbal, marrow) → 100% squatted across .com/.io/.ai (registered 1990s). Never surface as primary candidates.
2. Obscure single real words (osteons, azeotrope, voussoir) → often available on .io/.ai, rarely .com.
3. **Coined two-word compounds (bindweft, ropesand, codexwork) → most likely to have .com available.** This is the Stripe/Vercel/Anthropic pattern: recognizable real-word components, unique combination. Lead with these when domains matter.

See `references/diverse-sources-naming.md` for the full candidate pool, availability table, and source-category checklist.

## Scope narrowing
- If the user rejects several batches in a row, treat that as a constraint refinement, not just a preference for "better names."
- Re-anchor on the strongest explicit brand axis first (industry/domain), then the tone axis, then the phonetic/style axis.
- If the user says "stay with X brand," keep every new option inside X before trying further aesthetic variation.

## Company names vs product names (learned 2026-08-11)

The real-word acronym pattern (the OS, CORE, LENS) applies to **PRODUCT and CATEGORY names**, not **COMPANY names**. When the user asks for a company name for a subsidiary/LLC:

- Do NOT default to acronyms. The user explicitly corrected: "The real-world acronym pattern does not need to be followed on this task."
- DO think Palantir / Anduril / Stripe / Anthropic / Vercel — real, memorable, brandable words or coined-from-roots.
- Pull from DIVERSE sources (nature, engineering, music, chemistry, cartography, craft, light, literature) — NOT just Greek/Latin philosophy. User said the Greek/Latin batch was "incredibly siloed."
- Generate HIGH VOLUME (15+ per batch). The user said: "I just need a lot to choose from as nothing stands out yet. When I know I'll know."
- Check domain availability IN THE SAME PASS. Don't hand back names whose domains are all squatted.
- Don't over-narrow to one aesthetic lane. Cast wide, let the user react and narrow.

## Falsification discipline for naming sessions (learned 2026-08-11)

**The competitive scan MUST happen in the SAME dispatch as name generation, not as a separate follow-up task.** In this session, names were generated first, then a separate competitive-scan subagent was dispatched. The user caught this as wrong sequencing: "Why are you having to do this again? You just said that you were having an agent go and do that. Did you do this in the wrong order?"

**The rule:** When dispatching name ideation, the subagent MUST (1) generate names AND (2) check domain availability via `whois` against authoritative registry servers in the SAME task. Never split these into sequential tasks — it doubles the token cost and produces names that are already squatted.

**Also:** The orchestrator should NOT be doing competitive/trademark checks itself with `terminal` commands after the subagent finishes. That is specialist work done in the wrong place. If the subagent's scan was incomplete, re-dispatch the subagent with tighter instructions, don't do it yourself.

## Reference
- See `references/close-variant-patterns.md` for the Quorinth-style variant pattern and sample response rules.
- See `references/diverse-sources-naming.md` for the full subsidiary/company naming candidate pool (2026-08-11 session).
