# Daily Intelligence Scan Findings — June 26, 2026

Key findings from the June 26, 2026 daily intelligence scan. Future sessions should verify whether these are still current and build on them rather than rediscovering from scratch.

## Major Competitor Moves (Since June 25)

### Google AMIE — Disease Management in Nature (June 17, 2026)
- **Published**: Nature, June 17, 2026
- **What it does**: Longitudinal disease management — multi-visit reasoning, symptom tracking, medication plan adjustment, drug formulary reasoning. Matches 21 primary care physicians in overall management reasoning. Scores higher on treatment plan appropriateness measures.
- **Significance**: AMIE has crossed from diagnostic demo to treatment-planning system. Google's pattern: research validates, then Google Health productizes. DS must position coaching engine as behavioral layer above clinical AI, not competing with clinical reasoning.
- **Source**: Nature (June 17, 2026), research.google.com

### Anthropic — Claude Fable 5 Suspended (June 12, 2026)
- **Launched**: June 9, 2026 (Mythos-class, above Opus 4.8, adaptive thinking API, 1M-token context)
- **Suspended**: June 12, 2026 — US government export-control directive restricting foreign national access. Anthropic disabled both Fable 5 and Mythos 5 for ALL customers globally.
- **Significance**: Confirms frontier model dependency is a live production risk, not theoretical. One government order shut down production for a model that existed for 4 days.
- **DS action**: Accelerate fine-tuned open-weight model for production inference. Model-agnostic architecture now urgent.
- **Source**: anthropic.com, smartscope.blog

### Perplexity Health — Accelerating
- **Launched**: March 19, 2026
- **Status**: Live for Pro and Max subscribers as of May 1. Apple Health integration + b.well EHR connectors (1.7M providers).
- **Significance**: This is the Perplexity Health-style UI the principal is building. Perplexity shipped 3 months ago with distribution. DS should evaluate partnership/integration rather than competing UI.
- **Source**: perplexity.ai, thenextweb.com

### Kimi K2.7 Code (Moonshot AI, June 12, 2026)
### NVIDIA Nemotron 3 Ultra 550B (recent)

## Regulatory Landscape Updates (Since June 25)

### MHRA AI Airlock Phase 2 Report (June 9, 2026)
- UK's regulatory sandbox for AI medical devices published comprehensive Phase 2 report.
- 7 case studies tested. Key finding: current medical device frameworks work for some AI products but not all. Continuous learning systems need new regulatory approach.
- Collaboration model between innovators and regulators works and should be expanded.
- **Implication**: Template for how health AI products will be evaluated going forward. US FDA is adapting similar sandbox approach.
- **Source**: gov.uk

### FDA QMSR Effective (February 2, 2026)
- Quality Management System Regulation aligned with ISO 13485:2016.

### FDA Warning Letters to Telehealth Companies (Mid-2026)
- FDA returned with coordinated wave of warning letters for false claims. Signals enforcement activity ramping back up.

## AI Model Landscape (Updates Since June 25)

### Claude Fable 5 — SUSPENDED
- Mythos-class, launched June 9, suspended June 12. DO NOT use as primary model.

### GPT-5.5 (OpenAI, April 2026)
- "Spud." First fully retrained base model since GPT-4.5. Strongest on agentic workflows and structured output.

### Open-weight models
- Llama 4, Mistral 3, DeepSeek, Zhipu AI LLM-4.7, Kimi K2.7 — all within 5-10% of proprietary frontier on most benchmarks.
- New models arriving every ~2 days.
- LLM-4.7 Flash (MoE architecture) worth evaluating for on-device inference — small active parameter count during inference.

## Behavioral Science Research (Updates Since June 25)

### KCC2 Protein — Neural "Habit Button" (Late 2025, implications rippling 2026)
- **Finding**: Brain protein KCC2 controls how environmental cues link to rewards. Small shifts in KCC2 levels reshape habit formation speed and strength.
- **Implication**: Provides neurobiological mechanism for context stability driving habit formation (validates JHU switch study from June 3, 2026). Context stability > repetition count.
- **DS action**: Add context stability scoring to coaching engine. Surface to users. Intervene when stability drops.
- **Source**: entechonline.com, sciencedaily.com

### Wendy Wood — Habit Science Practical Application (APA Monitor, January 2026)
- Focus on environmental design over tracking. Apps that modify environment produce behavior change. Apps that only track produce awareness.
- **DS action**: Review prompt design — is coaching engine modifying environment or just giving advice?

### Physical Activity Habit Longitudinal Study (Behavioral Sciences, 2026)
- Confirmed 59-66 day median for habit formation. Large individual variation. Validates removing hardcoded day-count milestones.

## Funding Signals (Updates Since June 25)

### Q1 2026
- Digital health funding: $7.4B (rebound driven by AI mega-rounds and M&A)
- US Health Management Solutions: $4.5B in 2025 (1.8x YoY growth). 83% directed to AI-powered ventures in Q1 2026.
- Vertical AI absorbed largest share of growth-stage venture capital in 2025, continuing into 2026.

### Notable Recent Rounds (carry-forward from June 25)
- Qualified Health — $125M Series B (AI safety infrastructure for health systems)
- OpenEvidence — $250M Series D (clinician AI medical search)
- Talkiatry — $210M Series D (psychiatric telehealth)

## the specialist engine (from June 26 analysis)

- Google AMIE validates domain-specific health AI but occupies clinical reasoning layer. DS occupies behavioral coaching layer. These are complementary, not competing. DS should explore integration with AMIE-class systems rather than competing.
- Claude Fable 5 suspension makes model-agnostic architecture urgent. Fine-tuned open-weight production model + frontier fallback. No exceptions.
- KCC2 research adds neurobiological mechanism to context stability thesis. Coaching engine needs context stability scoring.
- Three things to do NOW: (1) Ship under FDA wellness exemption, (2) Instrument acceptance rate tracking, (3) Begin open-weight fine-tuning.
- Measurement gap remains the biggest analytics blind spot. No public data on DS coaching acceptance rate, retention, or habit completion.
