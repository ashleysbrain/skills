# Daily Intelligence Scan Findings — June 25, 2026

Key findings from the June 25, 2026 daily intelligence scan. Future sessions should verify whether these are still current and build on them rather than rediscovering from scratch.

## Major Competitor Moves (Since June 19)

### Mayo Clinic + Microsoft — Frontier Health AI Model
- **Announced**: June 2, 2026
- **What it does**: Custom foundation model trained on Mayo's clinical knowledge, deployed through Microsoft infrastructure. Domain-specific health AI.
- **Significance**: Validates domain-specific health AI thesis. Now the most significant platform infrastructure play in institutional health AI. DS should NOT compete here but should ensure coaching engines can run on top of this class of model.
- **Source**: news.microsoft.com/source/2026/06/02/

### Anthropic — Claude Fable 5
- **Released**: June 9, 2026 (Mythos-class, positioned above Opus 4.8)
- **Specs**: >10% higher than Opus 4.8 on some benchmarks. Adaptive thinking API, 1M-token context window.
- **Relevance**: Adaptive thinking API matches coaching engine workload pattern (simple queries use less compute, complex ones use more). Worth benchmarking for coaching generation.
- **Source**: aiflashreport.com

### PointClickCare — AI-Informed SNF Discharge Planning (announced June 2026)
### Lumeris — Tom Symptom-Checking for high-risk patients
### Midjourney — Medical AI Scanner (June 18, 2026), moving into medical devices

## Regulatory Landscape Updates (Since June 19)

### FDA CDS Guidance — Town Hall Clarification (March 11, 2026)
- **Key change**: A single clinically appropriate recommendation is now acceptable under enforcement discretion (previously FDA expected multiple options).
- **Implication**: Wellness-scored coaching recommendations that present a single best behavioral action can fit within the CDS exemption if framed for clinician/user review.
- **Source**: fda.gov/medical-devices, faegredrinker.com, arnoldporter.com

### FDA General Wellness Guidance (January 6, 2026, further clarified)
- FDA struck language treating risk scores as devices.
- Expanded list of low-risk products exempt from review.
- 8D360/TWC scoring positioned as wellness assessments falls squarely in exemption zone.
- **Source**: ropesgray.com, berkleyls.com

### FDA-CMS TEMPO Pilot (accepting statements of interest since January 2, 2026)
- Technology-Enabled Meaningful Patient Outcomes pilot.
- Allows certain chronic condition digital health devices real-world use before full FDA authorization.
- Bridge to Medicare/Medicaid reimbursement.
- **Source**: gtlaw.com, hoganlovells.com, researchgate.net

### CMS Digital Health App Library for Medicare (announced March 2026)
- Curated list of approved tools for Medicare-eligible users.
- DS should pursue inclusion.

## AI Model Landscape (Updates Since June 19)

### Claude Fable 5 (Anthropic, June 9, 2026)
- Mythos-class, above Opus 4.8. Adaptive thinking API. 1M-token context.

### GPT-5.5 (OpenAI, April 2026)
- Strongest on agentic workflows and structured output. Now widely available.

### Open-weight models
- Llama 4, Mistral 3, DeepSeek series, Zhipu AI LLM-4.7 now within 5-10% of proprietary frontier on most benchmarks.
- Cost differential remains 10-15x.
- Recommendation unchanged: fine-tune open model for 80-90% of production queries, use frontier model as fallback.

## Behavioral Science Research (Updates Since June 19)

### Johns Hopkins — Habits Form via Sudden Neural Switch (Nature Communications, June 3, 2026)
- **Finding**: Transition from goal-directed to habitual behavior is a phase shift (sudden neural "switch"), NOT a gradual slope.
- **Implication**: Coaching sprint timelines should be redesigned around "switch detection" rather than fixed day counts. Context stability (not repetition count) is the strongest predictor of when the switch occurs.
- **JPSP April 2026**: Confirmed context stability trumps repetition frequency for habit formation speed. Especially relevant for ADHD users.
- **DS action**: Remove hardcoded day-count milestones. Add context stability scoring. Design coaching around detecting the automaticity switch.
- **Source**: hub.jhu.edu, scitechdaily.com, nature.com

## Funding Signals (Updates Since June 19)

### Q1 2026 Overall
- $4B across 110 deals. 59% concentrated in 12 mega rounds ($100M+).
- Highest mega-round concentration since pandemic peak.
- **Source**: fiercehealthcare.com, rockhealth.com

### Notable Recent Rounds
- Qualified Health — $125M Series B (AI safety infrastructure for health systems). Signals market need for safety wrappers.
- OpenEvidence — $250M Series D (clinician AI medical search).
- Talkiatry — $210M Series D (psychiatric telehealth).
- Honest Health — $140M (value-based care enablement).
- Clair Health — $11.6M Seed (women's health hormone-monitoring wearable, Khosla/a16z).

## the specialist engine (from June 25 analysis)

- FDA wellness exemption is actively exploitable right now. DS should ship non-diagnostic coaching features without waiting for premarket review.
- Mayo-Microsoft frontier model validates domain-specific health AI. DS coaching engine should be model-agnostic to avoid platform dependency.
- JHU habit switch study requires coaching engine update: detect switch, don't count days.
- No public outcome evidence exists for DS coaching. Cohort analysis needed by July 15.
- Open-source model fine-tuning for production inference is now the recommended path (10-15x cost savings).
- On-device inference (LLM-4.7 Flash MoE architecture) worth evaluating for Divinity Health mobile app for both cost and state-level privacy compliance.
