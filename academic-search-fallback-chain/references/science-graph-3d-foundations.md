# 3D Graph of All Science — Mathematical Foundations

Condensed knowledge bank (Aug 2026). Reference data for building a
connected graph representation of all scientific knowledge. Covers
taxonomies, graph embeddings, 3D layout algorithms, and scale limits.

## 1. Taxonomies & Ontologies of Science

### OpenAlex (PRIMARY — CC0, fully open)
- 250M+ works, 13M+ authors, billions of citation edges
- Topic hierarchy (2023+): 4 domains → ~26 fields → ~360 subfields → ~4,500 topics
- Entity graph: works, authors, sources, institutions, topics, publishers, funders
- Successor to Microsoft Academic Graph (MAG, discontinued Dec 2021)
- API: free ($1/day); full DB snapshot downloadable quarterly

### UCSD Map of Science (Börner, scimaps.org)
- 13 major domains, ~554 subdisciplines
- Derived from ~7K journals' cross-citation via force-directed layout
- Journal-level (not paper-level), 2D

### MeSH (NLM)
- ~30,000 descriptors, 16-branch hierarchical tree
- Medicine/biology only; used by PubMed/MEDLINE/ClinicalTrials.gov

### ACM CCS (2012)
- 4-level hierarchical tree, CS only (~11 top-level categories)

### Dewey Decimal (OCLC, proprietary)
- 10 main classes; 500=science, 600=technology. Too coarse for research.

### Recommended taxonomy stack
OpenAlex Topics (backbone) → MeSH (biomedicine depth) → ACM CCS (CS) → arXiv (physics/math) → Wikidata (entities)

## 2. Graph Embeddings for Scientific Literature

| Method | Year | Core Idea | Inductive? | Practical Scale |
|--------|------|-----------|------------|-----------------|
| node2vec | KDD 2016 | Biased random walks → Word2Vec | No | ~100K nodes |
| GraphSAGE | NeurIPS 2017 | Sample + aggregate neighborhood features | Yes | ~1M+ nodes |
| SPECTER | ACL 2020 | Transformer on citation triplets | Semi | ~136K corpus |
| PyTorch-BigGraph | 2019 | Distributed embedding | Yes | 2B+ edges |

### node2vec (arXiv:1607.00653)
- `p` (return) / `q` (in-out) tune BFS vs DFS; defaults: dim=128, walk=80, num_walks=10
- O(|V| × d × walks × walk_length). Best for: structural similarity, link prediction

### GraphSAGE (arXiv:1706.02216)
- Aggregators: Mean, LSTM, Pool. Learns a function → generalizes to unseen nodes
- O(|V| × K × d × S). Best for: evolving networks, recommendation

### SPECTER (ACL 2020.acl-main.207)
- Title+abstract → SciBERT; citation links as triplet loss signal
- Task-agnostic document embeddings without fine-tuning

### Recommendation
SPECTER2 (text) + GraphSAGE (graph structure) → fused

## 3. 3D Layout Algorithms

| Algorithm | Complexity | Practical Max | Strength |
|-----------|------------|---------------|----------|
| Fruchterman-Reingold | O(n²) | ~10K | Classic |
| ForceAtlas2 | O(n log n) BH | ~100K | Scale-free (Gephi default) |
| SFDP (Graphviz) | O(n log n) | ~500K | Multilevel convergence |
| OpenOrd | O(n log n) | ~1M+ | Massive graphs |
| t-SNE (Barnes-Hut) | O(n log n) | ~1M | Local neighborhoods only |
| UMAP | O(n^1.14) | ~1M+ | Global + local |
| LargeVis | O(n) | ~10M+ | Best for massive scale |
| 3D-Force-Graph (JS) | GPU | ~10-50K | Browser WebGL interactive |

### Force-directed (3D)
- Hooke's spring (attractive) + Coulomb (repulsive) → energy minimization
- Barnes-Hut octree approximation: O(n²) → O(n log n)

### UMAP (arXiv:1802.03426)
- Riemannian geometry + algebraic topology; fuzzy topological structure
- 3D: `n_components=3`. Better global structure than t-SNE, faster, stable

### LargeVis (arXiv:1602.00370)
- (1) Approximate k-NN graph → (2) Layout via async SGD. Linear time, millions of points

## 4. What Breaks at 1M+ Nodes

1. **Memory**: O(n²) adjacency = 1TB+. Must use sparse/CSR + approximate methods
2. **Force-directed hairball**: Dense regions collapse; convergence fails without multilevel coarsening
3. **t-SNE**: O(n²) infeasible; Barnes-Hut reaches ~1M but hours-days; global structure destroyed
4. **Rendering**: WebGL collapses ~50-100K nodes; sub-pixel nodes; LOD/tiling mandatory
5. **Interactivity**: Need hierarchical clustering + semantic zoom
6. **Embedding quality**: node2vec sparse coverage; GraphSAGE misses long-range structure

### Recommended architecture for 1M+ science graph
1. Data: OpenAlex snapshot → Parquet/DuckDB
2. Embeddings: SPECTER2 + GraphSAGE fused; cuGraph or PyTorch-BigGraph
3. Layout: UMAP 3D (NNDescent) or LargeVis for 10M+
4. Hierarchy: 4 domains → 26 fields → 360 subfields → 4,500 topics → papers (on demand)
5. Rendering: ThreeJS InstancedMesh + LOD; ≤10-50K nodes per zoom level

## 5. Cross-Disciplinary Bridge Detection

The core differentiator for science-graph discovery tools (Constellation/Otlet).
Surfaces connections between disciplines that researchers would never think
to look for — "bridge nodes" connecting two otherwise distant clusters.

### Bridge scoring formula

```
bridge_score(node) = betweenness_centrality(node)
                   × embedding_distance(cluster_A, cluster_B)
                   × normalized_degree(node)
```

A high bridge-score node is a concept, method, or paper that is the hidden
link between two fields. Example: "coherent energy transfer" bridges
neuroscience (microtubule coherence) to physics (quantum decoherence).

### Implementation approach

1. Compute node embeddings (SPECTER 2 for papers, aggregate for concepts)
2. Cluster the graph by discipline (HDBSCAN or k-means on embeddings)
3. Compute betweenness centrality for all nodes (NetworkX)
4. For each pair of clusters, find the highest-bridge-score nodes connecting them
5. Surface as "surprise connections" in the UI (golden/highlighted edges)

### Why this is a moat

No existing tool (Google Scholar, Connected Papers, Semantic Scholar, OpenAlex)
detects and surfaces cross-disciplinary bridges. They all search within a
discipline or show citation neighborhoods. Bridge detection across embedding
space + graph structure is the unique value proposition.

## 6. Credibility Scoring for Science Graphs

7-factor model (0-100 score per paper) for ranking sources:

| Factor | Weight | Source |
|--------|--------|--------|
| Venue impact factor / quartile | 25% | OpenAlex venue data |
| Citation count (log-normalized) | 20% | OpenAlex `cited_by_count` |
| Author h-index (max across authors) | 15% | OpenAlex `summary_stats` |
| Peer-reviewed vs preprint | 15% | OpenAlex `type` field |
| Recency decay (newer = less proven) | 10% | Publication year |
| Retraction status | 10% | Retraction Watch DB, OpenAlex `retracted` flag |
| Open access status | 5% | OpenAlex `open_access` |

Display: node color intensity ∝ score; credibility filter slider; retracted
papers get visual marker; hover shows score breakdown.

## 7. Proven Heterogeneous Graph Schema (Otlet System)

Tested at 3,559 nodes / 6,617 edges (TSC 2026 consciousness science corpus):

### 7 node types
paper, concept, person, institution, research_lab, event, venue

### 14 edge types across 5 toggleable layers
- **Citation:** cites (paper→paper)
- **Concept:** discusses (paper→concept), subconcept_of (concept→concept)
- **Social:** authored, affiliated_with, member_of, collaborated_with, institution_collab
- **Event:** presented_at, presented_at_event, hosted_event
- **Organizational:** hosts, lab_produced, published_in

### Key insight: the concept layer is the cross-disciplinary backbone
With 2,285 concepts spanning 11 domains and 4,901 `discusses` edges linking
papers to cross-domain concepts, the concept layer carries the latent
cross-disciplinary structure. Bridge detection operates on this layer.
