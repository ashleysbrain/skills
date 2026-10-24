# Grok Imagine / xAI image path

## When
- LinkedIn / launch / brand hero images
- User asks for Grok / xAI / \"best in the world\" quality
- the operator agent `image_generate` returns FAL/Nous HTTP 402

## Invoke
```bash
cd <agent-home>/hermes-agent && ./venv/bin/python3.11 <<'PY'
import os, sys, json
sys.path.insert(0, '.')
os.environ.setdefault('XAI_IMAGE_MODEL', 'grok-imagine-image-quality')
from plugins.image_gen.xai import XAIImageGenProvider
p = XAIImageGenProvider()
res = p.generate(prompt=PROMPT, aspect_ratio='landscape')  # or square|portrait
print(json.dumps(res, indent=2)[:2000])
PY
```

## Models
| ID | Use |
|----|-----|
| `grok-imagine-image` | Fast drafts (~5–10s) |
| `grok-imagine-image-quality` | Brand heroes, LinkedIn (~10–20s) |

Overrides: env `XAI_IMAGE_MODEL`, or `image_gen.xai.model` / `image_gen.xai.resolution` (`1k`|`2k`) in config.yaml.

## Prompt budget
- Under ~900 tokens / ~3,500 chars
- One concept · one composition · one mood · one reject block
- Skeleton: quality bar → concept → phi composition + hex palette → style accents → light/mood → lockup or no-text → strict avoids

## DS social-hero visual law (2026-08-02)
**Inspire from:** coupling network, cascade-under-load, process-flow energy, Gestalt whole, Corpus design principles (MIT visual composition).

**Do not clone:** Fleet Atlas PDF covers, white report pages, flowchart boxes, org charts, stock neural nets, cyberpunk purple, SaaS dashboards.

**Canvas accents:** navy-teal void `#0a1e2e`–`#062323`, gold nodes `#c9a227`/`#ffd700`, teal breath, unequal filament weights, cascade rings, Da Vinci construction ghosts, Mucha line, Klimt flecks on nodes only, film grain.

## Canonical organism structure (2026-08-02)
**11 Biological Organ Systems (gold nodes):**
1. Integumentary (skin/boundary)
2. Skeletal (structure)
3. Muscular (force)
4. Nervous (signal/cognition)
5. Endocrine (hormones/regulation)
6. Cardiovascular (circulation)
7. Lymphatic/Immune (defense)
8. Respiratory (gas exchange)
9. Digestive (nutrient processing)
10. Urinary (filtration/fluid balance)
11. Reproductive/Genetic (birth/heredity)

**Diagnostic Infrastructure (separate node):**
- 12th node, distinct from the 11 biological systems
- Position slightly apart from main cluster
- Color: cool teal-gold patina (not gold)
- Spans all systems, not one of them — clinical reasoning, imaging, technology monitoring

**Fungal Network Context (zoomed-out view):**
- Extremely faint mycelial filaments at far background/edges (opacity 5-8%, very thin)
- Suggest connection to other distant organisms
- This organism is part of a larger connected ecosystem
- Never explicit/labeled; abstract filament only
- No literal fungi/mushroom shapes or trees

Source: `DS-ECS-SPEC.md` (Domain Registry) — canonical source of truth for organism architecture.

## Deliver
1. Prefer local download of CDN URL into brand assets dir. Result key is **`image`** (also `public_url`), not `url`.
2. `MEDIA:/absolute/path.png`
3. Honest critique: hits vs gaps vs world-class; offer next pass only if asked or clearly weak
4. **Concept heroes must teach.** If a first-time viewer cannot state the idea in 3 seconds, reject even if beautiful. Decorative organism nets (unlabeled gold webs) are mood-only, not lead LinkedIn visuals (the principal correction 2026-08-02).

## Canonical prompt pack
`your-org-marketing/02-social-posts/DIVINITY-SCIENCE-LINKEDIN-the operator agent-PHYSIOMORPHIC.md` → section **LinkedIn hero image — Grok prompt pack** + **TEACHING VISUAL PIVOT**
- Mood-only (rejected as lead): `physiomorphic-ai-linkedin-hero-v1.png`, `...-v2.png`
- Teach lead: `physiomorphic-ai-linkedin-teach-v3-split.png` (neuron | organism)
- Teach why: `physiomorphic-ai-linkedin-teach-v3-cascade.png` (Sleep/Focus/Mood/Decision)
