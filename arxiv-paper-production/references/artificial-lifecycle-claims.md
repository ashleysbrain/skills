# Artificial Lifecycle Claims in Physiomorphic-AI Papers

Use this reference when a manuscript discusses DNA, genomes, heredity, development, epigenetics, reproduction, offspring, or evolution in software or multi-agent systems.

## Core separation

Architecture and lifecycle are independent axes:

- A system may be physiomorphic without reproducing.
- A self-replicating digital system may have no organism-level anatomical mapping.
- Product generation is not organism reproduction.
- Update distribution is not evolution.

## Operational claim gate

| Term | Minimum defensible computational referent | Common false positive |
|---|---|---|
| Digital genotype | Versioned, heritable generative specification used to instantiate derived systems | Calling an arbitrary repository or config file "DNA" |
| Phenotype | Instantiated architecture and observable behavior under a stated environment | Treating every output file as a phenotype without a genotype-expression relation |
| Development | Stage-dependent expression with measurable commitment, differentiation, or context sensitivity | Renaming a linear deployment pipeline after embryology |
| Epigenetic state | Persistent expression control that changes active capability without changing genotype | Any runtime configuration or feature flag |
| Reproduction | Creation of a new independently addressable system from inherited specification | Generating a report, product, feature, or ordinary clone |
| Offspring | Inherited specification, distinct identity/state, recorded lineage, capacity for variation or divergence | Calling products or deployments "children" without lineage semantics |
| Evolution | Population-level heritable variation and differential retention across generations | Parent-to-child updates, optimization, or version upgrades |

## Manuscript wording discipline

Prefer:
- "digital genotype" over unqualified "DNA"
- "derived system instance" until offspring criteria are met
- "staged instantiation" until developmental criteria are measured
- "update distribution" or "inheritance management" until evolutionary selection exists

Do not infer literal life, autonomy, reproduction, or consciousness from biological naming.

## Literature anchors

- Stanley, K. O., & Miikkulainen, R. (2003). *A Taxonomy for Artificial Embryogeny*. Artificial Life, 9(2), 93–130. DOI: 10.1162/106454603322221487.
- Ofria, C., & Wilke, C. O. (2004). *Avida: A Software Platform for Research in Computational Evolutionary Biology*. Artificial Life, 10(2), 191–229. DOI: 10.1162/106454604773563612.
- Fortuna, M. A., Zaman, L., Ofria, C., & Wagner, A. (2017). *The Genotype–Phenotype Map of an Evolving Digital Organism*. PLOS Computational Biology, 13(2), e1005414. DOI: 10.1371/journal.pcbi.1005414.

## Pre-delivery questions

1. Are lifecycle terms defined operationally rather than rhetorically?
2. Does each claim have a measurable criterion and disconfirmation condition?
3. Is the system being described as an artifact where artifact is the more accurate word?
4. Are biological and computational mechanisms clearly separated?
5. Has the revised lifecycle section passed a hostile review at the manuscript's required threshold?
6. If "development" is defined with stage-dependent expression criteria, is prior art from artificial embryogeny (Stanley & Miikkulainen 2003 and successors) acknowledged? Physiomorphic AI's contribution is organism-level mapping, not staged expression itself.
