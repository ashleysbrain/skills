# Human Touch Research — Building Taste Into AI Creative Systems

Condensed findings from a June 2026 research sweep of AI design tools, aesthetic evaluation models, taste injection techniques, and human-in-the-loop creative workflows. Directly informs how phenotype specs should handle visual personality and quality gates.

---

## 1. AI Tells — What Makes Output Look Generated

The tells are **no longer technical failures (hands, text) but aesthetic defaults**. These are concretely enumerable:

### The 15 Design Markers (axbrief, 500-project analysis, April 2026)
- Most reliable single signal: a specific colored accent on the **LEFT BORDER** of content blocks (like the em-dash of visual design)
- ~5-10% false-positive rate on that one marker alone
- High overlap across multiple markers = near-certain raw LLM output
- Market implication: "lack of effort in presentation is read as proxy for lack of effort in engineering"

### The 6 Visual Cliches (image domain)
1. Plastic/poreless skin — fix by prompting "natural skin texture, visible pores"
2. Everything-is-golden-hour lighting regardless of scene logic
3. Dead-center, perfectly symmetrical composition (humans use rule-of-thirds, negative space, imbalance)
4. Over-detailed everything — no focal hierarchy
5. Generically beautiful faces — no distinctive features
6. Unmotivated background blur — bokeh with no optical justification

### Text Tells
Em-dashes instead of hyphens, excessive blank lines, periods after every list item, rigid template structures, overuse of "delve," "tapestry," "vibrant," "realm," "cutting-edge."

### The Anti-AI Aesthetic ("Dirty Minimalism," Lucky Graphics, April 2026)
- Post-digital grain: ink-bleed, canvas texture, 2% paper-grain overlay
- Hand-drawn/wobbly SVG vectors with slight irregularities = 30% higher trust rating
- Off-white "milkcoat" backgrounds
- **Core thesis: AI can generate beauty but cannot generate meaningful imperfection. Imperfection is now the premium authenticity signal.**

### Academic Framing — Aesthetic Bias (Declos, JAAC Oxford 2026)
AI models systematically privilege beauty, spectacle, saturation, symmetry and marginalize the rest. These biases "disguise aesthetic preferences as neutrality" and homogenize artistic production.

**ACTION FOR PHENOTYPE SPECS:** Build an explicit anti-tell checklist into the visual personality section. Enumerate: symmetry score, border-accent pattern, skin-smoothness, golden-hour lighting, em-dash density, template-structure rigidity.

**CRITICAL — Imperfection must be SURGICAL, not random.** Inject imperfection as a deliberate phenotype trait, but EVERY deviation from perfection must be phi-calculated. Off-center placement at 0.382 from edge (not "about 15%"). Grain opacity at phi^-3 = 2.36% (not "about 5%"). Line weights on phi scale (1.0, 1.618, 2.618px). The user was explicit: "we don't want to just make things randomly off balance. It needs to be mathematical, not just throw this weird thing over here." Random imperfection looks sloppy. Phi-justified imperfection looks handcrafted. This is the difference.

---

## 2. Aesthetic Evaluation Models — Can AI Critique Its Own Work?

Yes, and SOTA is genuinely close to human judgment:

| Model | Correlation w/ Human | Notes |
|-------|---------------------|-------|
| LAION Aesthetic Predictor | Moderate | Linear head on CLIP embeddings; cascades into SD training data curation |
| ImageReward | Higher | BLIP-based, widely cited baseline |
| PickScore | Higher | Pick-a-Pic dataset |
| HPS/HPSv2 | Strong | Stable Diffusion Discord preferences |
| **HPSv3** (ICCV 2025) | **Spearman r = 0.94** | **Current SOTA.** Qwen2-VL VLM backbone + MLP + uncertainty-aware ranking loss |

### HPSv3 Key Innovations
- HPDv3 dataset: 1.08M image-text pairs, 1.17M pairwise comparisons, 9-19 annotators/prompt
- Uncertainty-aware ranking loss — accounts for annotator disagreement
- CoHP (Chain-of-Human-Preference): generate variants → reward-select → img2img refine → loop. Improves quality without extra training data
- Works as RLHF reward signal (validated with DanceGRPO)
- `pip install hpsv3`

### Critical Caveat — The Algorithmic Gaze (FAccT 2026)
LAP disproportionately filters IN images of women, filters OUT men and LGBTQ+ people. Rates Western + Japanese landscapes highest. Reinforces imperial and male gazes of Western art history.

**ACTION:** Adopt HPSv3 architecture as primary aesthetic-critique organ. Use CoHP-style iterative refinement. CRITICALLY: do NOT use a single scalar aesthetic score as sole gate — run a portfolio of evaluators (HPSv3 + anti-tell detector + domain-specific critics) to avoid homogenization.

---

## 3. Taste/Preference Modeling & Style Injection

### Image Domain Personalization Techniques

| Technique | What It Does | Best For |
|-----------|-------------|----------|
| **DreamBooth** | Full fine-tune on 3-5 images; class-specific prior-preservation loss | Max fidelity (faces, objects) |
| **LoRA** | Low-rank adapter; DreamBooth-compatible; parameter-efficient | Swappable style/persona layers |
| **Textual Inversion** | Learns new embedding for a token; model weights frozen | Lightweight style/concept injection; also negative embeddings |
| **IP-Adapter** | Image-encoder features → new cross-attention layers; UNet frozen | **Style transfer from reference image at inference — most taste-injection-friendly primitive** |
| **Midjourney --sref** | Extract palette/texture/atmosphere from reference | Production style consistency |
| **ControlNet** | Structural conditioning (pose, depth, edges) | Composition/layout control |

### RLHF/Preference Learning for Creative Tasks
- Standard RLHF pipeline: reward model on pairwise comparisons → RL fine-tuning
- ICPL (In-Context Preference Learning): LLM converts human preferences into reward-function code; orders of magnitude more efficient than vanilla RLHF
- DPO (Direct Preference Optimization): dominant 2025+ simplification, skips explicit reward model
- For images: HPSv3/ImageReward as reward signal → DanceGRPO fine-tuning

### Mapping to Biological Metaphor (the specialist engine)

| Biological Concept | AI Equivalent | the specialist engine |
|-------------------|--------------|-----------------|
| Genotype (DNA) | LoRA/style-tuning weights | Design-token genome + learned Style Profile |
| Phenotype (expression) | IP-Adapter refs + --sref at inference | Rendered output with product phenotype applied |
| Immune system | Negative embeddings + prompt blacklists | Anti-tell detectors, banned vocabulary lists |
| Selection pressure | DPO/HPSv3 preference pairs | User approval/rejection training the Style Profile |

**ACTION:** A "taste genome" should be a layered artifact: (a) LoRA/style weights = genotype; (b) IP-Adapter refs/--sref = expressed phenotype; (c) negative embeddings/blacklist = immune system; (d) preference pairs → DPO/HPSv3 reward = selection pressure.

---

## 4. Human-in-the-Loop Creative Workflows — What Works

### What Works
1. Treat AI as junior designer, not creative director. Request component variations, not whole finished products.
2. Human-in-the-loop checkpoints at every stage: ideation → concept → production → atomize → distribute → measure
3. Brief-first, not prompt-first. Every asset must fit brand, channel, and goal.
4. Workflow redesign > tool adoption. 93% of enterprises report workforce barriers. The bottleneck is process design, not tool access.
5. Maturity: Manual → AI-assisted → orchestrated multi-agent pipelines with HITL checkpoints

### What Doesn't Work
- End-to-end "AI, build my whole app" prompts → generic, soulless output
- Generating without a brand/style system → homogenized slop
- Skipping human review gates → quality/ethics failures

**ACTION:** The creative organ system should expose structured HITL checkpoints, not just generation. Brief-first inputs, component-level generation requests, review gates where a human (or critic-agent proxying human taste) culls before the next stage.

---

## 5. Multi-Agent Creative Systems — Direct Precedents

### CREA (Virginia Tech, arXiv:2504.05306)
The most directly relevant system found. Collaborative multi-agent framework emulating the human creative process with specialized roles:
- Creative Director + Prompt Architect → pre-generation planning
- Generative Executor → diffusion models / ControlNet
- Art Critic (multimodal LLM) → post-generation evaluation on six principles
- Refinement Strategist → iterative improvement loops

**The Six-Principle Creativity Index:**
1. Originality — fresh or rehash?
2. Expressiveness — communicates emotion and meaning?
3. Aesthetic appeal — meets phi-based threshold?
4. Technical execution — craft precise and polished?
5. Unexpected associations — connects ideas non-obviously?
6. Interpretive depth — rewards sustained attention?

**ACTION:** Adopt CREA's specialized-role structure as the organ blueprint and the six-principle Creativity Index as the evaluation rubric.

### Creativity in LLM-based MAS Survey (arXiv:2505.21116)
First survey dedicated to creativity in multi-agent systems. Taxonomy of agent proactivity & persona design, generation techniques (divergent exploration, iterative refinement, collaborative synthesis), key open challenges (inconsistent evaluation, insufficient bias mitigation, coordination conflicts, lack of unified benchmarks).

### Microsoft Multi-Agent Reference Architecture (github.com/microsoft/multi-agent-reference-architecture)
Production-grounded guide: agent registry, memory, communication, observability, evaluation, security, governance, "designing for change."

### Biological Metaphor Validation (MIT Tech Review, arXiv:2407.15908)
"Genome = compressed generative data that produces an organism with significant variation — not a blueprint." Genome = training data + generative model; phenotype = output; epigenetics/environment = conditioning/prompt. Directly validates DS organism framing.

---

## Key Papers/Repos

- HPSv3 / HPDv3 — arXiv:2508.03789, github.com/MizzenAI/HPSv3, `pip install hpsv3`
- CREA — arXiv:2504.05306, crea-diffusion.github.io
- Creativity in MAS Survey — arXiv:2505.21116
- Aesthetic Bias — Declos, JAAC Oxford 2026
- LAP Algorithmic Gaze audit — FAccT 2026, arXiv:2601.09896
- LAION Aesthetic Predictor — github.com/LAION-AI/aesthetic-predictor
- DreamBooth — arXiv:2208.12242
- IP-Adapter — arXiv:2308.06721
- ICPL — OpenReview ICLR 2025
- Microsoft Multi-Agent Reference Architecture — github.com/microsoft/multi-agent-reference-architecture
