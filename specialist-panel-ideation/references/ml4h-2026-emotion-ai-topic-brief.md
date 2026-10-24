# ML4H 2026 CFP Digest + Emotion-AI Hotness Bank (2026-08-14)

Session-specific detail for the ML4H 2026 research-topic brainstorm.
Source: live fetch of https://ml4h.ahli.cc/submit/call-for-papers/ (curl,
Firecrawl down) + 3 x_search (grok-4.20-reasoning) hotness queries.

## Venue mechanics (verified from CFP)

- ML4H 2026, Sydney, Dec 6-7 2026. OpenReview submission.
- Dates (AoE): Aug 10 site opens; **Sep 10 paper deadline** (no abstract
  deadline); Oct 5 reviews out; Oct 12 rebuttal ends; Oct 22 decisions;
  Nov 7 camera-ready (tentative).
- Tracks: **Proceedings** (8pg, archival PMLR, technical novelty) and
  **Findings** (4pg, non-archival: novel datasets, negative results,
  preliminary results, reproducibility studies, opinion/critique pieces;
  dual submission allowed; can later publish elsewhere). Proceedings
  rejects auto-roll to Findings.
- Areas: A1 Models and Methods (algorithms/inference/estimation; synthetic
  data allowed; health-motivated but real health data NOT required);
  A2 Applications and Practice (datasets, sim frameworks, benchmarks,
  tools, telehealth/remote monitoring); A3 Impact and Society (policy,
  public health, bias/equity, responsible AI, deployment barriers).
- Reciprocal reviewing: >=1 author per submission must review 3 papers
  (needs 1 prior archival publication, else exemption form).
- LLM policy: allowed, must be documented if significant to method;
  authors fully responsible for reference accuracy.

## 2026 hotness signals (x_search, mid-2026; practitioner-reported)

1. **Anthropic "functional emotions" interpretability (Apr 2026)** —
   emotion-concept vectors in Claude that causally influence outputs;
   fierce debate: genuine functional emotion vs pattern-matching hype
   (Capraro "seven fault lines"). Hot angle: do LLMs understand vs
   simulate emotion.
2. **LLM affective vulnerability in agents** — COLM 2026 Iowa Gambling
   Task paper (arXiv ~2607.12631): anger induction reduces penalty
   sensitivity, causes early lock-in. Agent-safety framing.
3. **AI journaling / companion app discourse** — Stanford Character.AI
   study (>413k msgs, >1.1k users): companion-framed use correlates with
   lower wellbeing; UK teen study (1 in 5 boys 12-16 have/know AI
   girlfriend); sycophancy distorts relationship expectations. China
   regulating companion bots. Privacy-first/on-device journaling apps
   surging (Daysi, Nexomind, MirrorMind, DAWN).
4. **EU AI Act Article 5(1)(f)** — prohibits emotion inference in
   workplaces/education; boundary debates (behavior vs emotion), GDPR
   consent layers. Regulation-driven relevance for any emotion-AI paper.
5. **Multimodal emotion SOTA movement** — discriminative hidden-state
   readout from omni-modal LLMs beating generative decoding (arXiv
   2606.05713); OneEmo unified emotion reasoning (2608.06013);
   multilingual emotion neurons in audio LLMs (2608.08772); HCEP open-set
   multimodal emotion; LLM perceptual geometry of emotion peaks in
   intermediate layers (ICML 2026 workshop). Open problems: open-set
   emotions, context-vs-modality disentanglement, cultural
   generalization, eval benchmarks for video LLMs, multimodal privacy.
6. **Benchmark validity critiques** — Arena "Sentiment Control" (tone
   inflates leaderboards); LLM-as-annotator reliability debates; Western/
   Ekman-centric dataset bias; low-resource language emotion gaps.

## Constraint rulings for DS-authored topics (this session)

- No clinical/diagnostic claims (no medical authority) — behavioral
  science / wellbeing framing only.
- No new IRB collection inside the 27-day window — public datasets,
  synthetic/LLM-generated data, or re-analysis only.
- Bias toward 4-page Findings track given deadline proximity.

## Panel dispatch pattern that worked

Sequential single dispatches; 2-3 seats per subagent; 3 ideas/seat;
"under 900 words" goal cap + "under 90 words per idea" context cap;
81s completion vs 482-731s timeouts on the fat prompts. Full transcripts:
deleg_b579fafc (Pennebaker/Picard/Jurafsky), deleg_ddb3d8e9 (Onnela/Liang).
