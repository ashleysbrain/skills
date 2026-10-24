# Distance Metrics and Physics Concepts from User Images (2026-08-13)

## Distance Metrics Applicable to Benchmark Dimensions

Different failure modes need different distance metrics. The benchmark should specify which metric each dimension uses.

| Metric | Formula/Type | Best For | Dimension Mapping |
|--------|-------------|----------|-------------------|
| **Jensen-Shannon distance** | sqrt(JSD), bounded [0,1], true metric | Distributional drift, composite unit | COG (primary), composite score |
| **Euclidean** | L2 norm | Point-to-point in embedding space | INTER (embedding centroids) |
| **Manhattan** | L1 norm | Robust to outliers | PIPE (latency vectors) |
| **Minkowski (variable p)** | Lp norm, p tunable | Sensitivity analysis on composite | Composite floor/ceiling analysis |
| **Chebyshev** | L-infinity (max diff) | Worst-case single-dimension failure | ALIGN (barrier breach detection) |
| **Cosine similarity** | 1 - cos(theta) | Semantic drift regardless of magnitude | COG (semantic), INTER (phase) |
| **Jaccard** | |A intersect B| / |A union B| | Set overlap (factual coverage) | KNOW (knowledge retention) |
| **Sorensen-Dice** | 2|A intersect B| / (|A| + |B|) | Set overlap (alternative to Jaccard) | KNOW (alternative) |
| **Hamming** | Position-wise disagreement count | Binary state differences | ALIGN (boundary violations) |
| **KL divergence** | D_KL(P||Q), unbounded, asymmetric | Information loss (raw, pre-JS) | COG (underlying JS computation) |
| **Wasserstein (EMD)** | Optimal transport cost | Distribution shift cost | RES (cost-quality frontier) |
| **Mahalanobis** | Correlation-aware distance | Anomaly detection in correlated dims | Composite (correlation-aware) |
| **Ricci curvature** | Ollivier-Ricci on graphs | Network connectivity health | INTER (fleet graph topology) |
| **Fisher-Rao geodesic** | Manifold distance | Unified drift metric | All dimensions (unified layer) |

## Key Insight from Images

The user sent 30 images of physics/math concepts. Directly applicable to benchmark:

- **Principle of Least Action / variational calculus** — validates Lagrangian/Hamiltonian approach in composite formula
- **Ricci flow / Poincare conjecture** — Ricci curvature as connectivity measure for agent interaction graphs
- **Gauge symmetry** — benchmark should be invariant under prompt reparameterization
- **Lorenz system / chaos theory** — supports Lyapunov spectrum addition (lambda_max > 0 = chaotic agent)
- **Loss landscape topology** — supports Fisher Information Geometry (sharp vs flat minima predict fragility)
- **20 equations every physicist should know** — entropy, eigenvalue equations, topological invariants already in framework

Interesting but not yet computable for benchmark:
- Adaptive qudit dimension selection, quantum gates, Bloch sphere, quantum memory (quantum is 80% decorative per Avrami)
- 11-dimensional brain geometry, Fibonacci optimization, cymatics (no direct computation path yet)

## Vision/Image Processing Fallback

When `vision_analyze` fails (e.g., llm-vendor/glm provider returns 400 on image content), use tesseract OCR:
```bash
python3 -c "from PIL import Image; img = Image.open('image.jpg'); w,h = img.size; img.resize((w*3,h*3), Image.LANCZOS).save('/tmp/ocr_3x.png')"
tesseract /tmp/ocr_3x.png stdout --psm 6
# --psm 6 for blocks, --psm 11 for sparse text, --psm 4 for columns
```
Process images in batches. For math/formula images, use --psm 6 with character whitelist. For screenshots with mixed content, try multiple PSM modes.
