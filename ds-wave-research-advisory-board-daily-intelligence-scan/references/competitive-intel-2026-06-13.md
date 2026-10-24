# Competitive Intelligence Snapshot — June 13, 2026

Key findings from the June 13, 2026 daily intelligence scan. Future sessions should verify whether these are still current and build on them rather than rediscovering from scratch.

## Major Competitor Moves (2026 H1)

### OpenAI — ChatGPT Health
- **Launched**: January 7, 2026
- **What it does**: Dedicated health tab in ChatGPT. Syncs lab results, medical records, wellness app data. Health chats encrypted and isolated from training data.
- **Distribution**: 40 million daily users ask health questions (1 in 5 ChatGPT users ask health questions weekly).
- **Institutional**: ChatGPT for Healthcare deployed to AdventHealth, Baylor Scott & White, Boston Children's, Cedars-Sinai, HCA Healthcare, Memorial Sloan Kettering, Stanford Medicine Children's Health, UCSF.
- **Tier 2**: ChatGPT for Clinicians launched April 22, 2026 — free for verified individual doctors, NPs, PAs, pharmacists.
- **Key gap**: No behavioral coaching engine. Data aggregation and summarization only.
- **Source**: openai.com/index/introducing-chatgpt-health/, CNBC, Medical Economics

### Anthropic — Claude for Healthcare
- **Launched**: January 11, 2026 (JPM conference)
- **What it does**: HIPAA-ready tools for providers/payers. Personal health integrations for individual users through Apple Health, Android Health Connect, Function, HealthEx.
- **Distribution**: Apple Health and Android Health Connect partnerships. Dedicated healthcare team.
- **Key gap**: Clinical workflow and documentation tool. No behavioral coaching.
- **Source**: anthropic.com/news/healthcare-life-sciences, Fierce Healthcare

### Mayo Clinic + Microsoft — Frontier Health AI Model
- **Announced**: June 2, 2026
- **What it does**: Custom foundation model trained on Mayo's clinical knowledge, deployed through Microsoft infrastructure. Domain-specific health AI.
- **Significance**: Validates domain-specific health AI thesis. Sets market expectation for institutional health AI.
- **Source**: news.microsoft.com, Modern Healthcare

## AI Model Landscape (Relevant to Coaching Engine)

### MiniMax M2.7
- **Released**: April 11, 2026 (open-sourced)
- **Specs**: 56.22% SWE-Pro, 57.0% Terminal Bench 2. Agentic workflows.
- **Pricing**: $0.30/M input, $1.20/M output tokens (10-15x cheaper than Claude Opus 4.6)
- **Relevance**: Worth benchmarking for coaching engine inference at scale. Open-weight, runs locally.
- **Source**: marktechpost.com, developer.nvidia.com, datacamp.com

### LLM-4.7 Flash (Zhipu AI)
- **Released**: January 23, 2026
- **Specs**: Mixture of Experts, runs locally without server farm. 59.2% SWE-bench.
- **Relevance**: On-device inference architecture for health coaching. Small enough for phone deployment.
- **Source**: Reddit r/rpgc_official, HuggingFace

## Regulatory Landscape

### FDA 2026 Guidance Updates (January 6, 2026)
- Updated CDS software and general wellness product guidance
- Direction: clearer regulatory lines, expanded pathway for low-risk digital health tools
- Low-risk products can reach market without premarket review
- Key distinction: wellness tool vs. clinical decision support determines regulatory burden
- **Sources**: berkleyls.com, lw.com, nixonpeabody.com, faegredrinker.com

### Digital Health in Clinical Investigations
- Federal Register notice March 31, 2026: advancing use of digital health technologies in clinical investigations for drugs and biological products

## Funding Signals

### Q1 2026 Health Tech
- $4 billion across 110 deals
- 59% concentrated in 12 mega rounds ($100M+)
- Highest mega-round concentration since pandemic peak
- Investors consolidating bets on platform winners
- **Source**: emarketer.com, allhealthtech.com

## Behavioral Science Research

### Habit Formation Timeline (Johns Hopkins, June 3, 2026)
- Habits form faster than the old "66 days" (Lally et al. 2010) assumption
- Implications: the specialist engine coaching timelines may be too conservative
- Test shorter coaching sprints (7-14 days)
- **Source**: hub.jhu.edu

### Habit Degradation Strategies (Nature Human Behaviour, March 2026)
- Three specific strategies for weakening unhealthy habits
- Active degradation outperforms passive approaches for early habit strength reduction
- Implications: DS should add "habit degradation" mode to coaching engine
- **Source**: nature.com/articles/s44271-026-00432-9

### Context Stability vs Repetition (JPSP, April 2026)
- Context stability, not repetition frequency, strongest predictor of habit formation
- Particularly relevant for ADHD users
- **Source**: journals.sagepub.com

## the specialist engine (from June 13 analysis)
- The coaching moat (behavioral intervention engine) is real but has no public evidence
- OpenAI and Anthropic have distribution but not coaching depth
- Data integration (Apple Health, Android Health Connect, FHIR) is now table stakes, not differentiating
- Open-source models (M2.7, LLM-4.7 Flash) offer 10-15x cost savings over proprietary APIs
- No public benchmarks exist comparing DS coaching outcomes to any external standard
