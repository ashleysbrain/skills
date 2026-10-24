# Abstract Compression and Citation Audit

Use this when converting a full academic abstract into a shorter portal version or assembling its references.

## Short-Abstract Preservation Gate

Compression must preserve the scientific load-bearing elements, not merely the topic.

1. **Field definition:** retain the coined term, defining distinction, and architecture class.
2. **Taxonomy fit:** use the portal’s exact intellectual category in the prose when natural (for example, “cognitive architecture”).
3. **Venue contribution:** preserve the sentence explaining why the work belongs at the target conference.
4. **Quantitative interpretability:** every number needs its scale, unit, or denominator.
   - `I(S) = 0.80` → `I(S) = 0.80 on a zero-to-one scale`
   - `advantage of 0.27` → state normalized-capacity units or the verified percentage equivalent.
5. **Falsifiability:** retain both the prediction and the failure condition. A result without the prediction it tests reads as descriptive engineering.
6. **Evidence calibration:** measurements stay preliminary; design goals remain “designed to,” “intended to,” or “predicted to.”
7. **Scope firewall:** architecture/resilience evidence must not be presented as consciousness evidence.
8. **Scholarly signal:** preserve at least the principal originators for the central consciousness theories (for example, Tononi; Baars and Dehaene), even when secondary names must be removed.
9. **Claim softening under compression:** do not strengthen “models or approximates a function” into “performs the biological function.”
10. **Safety margin:** target 8–10 words below the portal limit because portal tokenization may differ from `wc -w`.

## Citation Completeness: Two Different Lists

Do not confuse these:

### Claim-proximal abstract bibliography
Include the primary or canonical source for every named framework, scientist, metric, or technical mechanism actually invoked in the abstract. This list should be tight and directly traceable.

### Full science-to-technology provenance bibliography
For the poster or manuscript, also include foundational lineages that the implementation depends on even if their authors are not named in the abstract, such as:
- neuromorphic computing origins;
- cybernetics and homeostasis;
- emergence and complexity;
- autopoiesis/biological organization;
- multi-agent systems;
- falsifiability;
- embodied/interoceptive consciousness.

A longer list is not automatically more complete. Every added source must pass a relevance test: identify the exact claim, design principle, or lineage it supports. Remove prestige citations with no traceable role.

## Adversarial Citation Panel

Run independent reviewers with distinct attack roles:

1. **Bibliographic verifier:** authors, year, title, venue, volume/issue, pages, DOI/ISBN.
2. **Claim-source mapper:** every claim has a source; every source supports a real claim.
3. **Primary-source critic:** rejects reviews where an original formulation is available, while allowing a canonical modern review as a second citation.
4. **Scope critic:** identifies important scientific foundations omitted from the bibliography.
5. **Inflation critic:** removes tangential references added only to make the bibliography look substantial.

Output a claim-to-source matrix and separate findings into MUST-FIX, SHOULD-FIX, and OPTIONAL.

## Oxford Abstracts Packaging

Inspect the live form. If it requests references, provide a plain copy/paste list in the form’s accepted style and character limit. If no style is specified, use one consistent compact author–date format with DOI URLs. Do not assume references are excluded merely because many conference portals omit them.
