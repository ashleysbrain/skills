# Wave Engine Micro-Task Routing Map

Added 2026-07-23. The full mapping of every v2.2 coaching micro-task to the specialist fleet engine that should own it.

## Principle

A coaching engine is an orchestrator, not a compute engine. the specialist engine receives input, the specialist engine dispatches each diagnostic to the right specialist, the specialist does the cognition, the result returns to Wave for synthesis. No monolith.

## The Routing Table

| v2.2 Step | Micro-Task | Engine | Scientist | Port | Why |
|---|---|---|---|---|---|
| Input | Voice transcription | the specialist engine | Thomas Edison | 8101 | Audio input (Whisper, diarization) |
| Input | Text intake + OCR | the specialist engine | Gutenberg | 8102 | Text/vision input (eyes) |
| Classify | Situation type scoring | the specialist engine | Roger Sherman | internal | Thalamocortical routing |
| Complexity Gate | Cognitive load | the specialist engine | Peter Sterling | 8091 | Free Energy Principle |
| Complexity Gate | Distress detection | the specialist engine | Sherrington | 8104 | Interoception |
| Step 2 Motivation | Language signal extraction | the specialist engine | Carl Wernicke | 8124 | Voice/language engine |
| Step 2 Motivation | Autonomy directive | the specialist engine | Broca | 8139 | Motor planning (output shaping) |
| Step 3 Efficacy | Confidence signals | the specialist engine | Sherrington | 8104 | Interoception |
| Step 3 Efficacy | Mastery staging | the specialist engine | the principal Williams | internal | 8D health specialist |
| Step 4 Mindset | Language detection + directive | the specialist engine | Wernicke | 8124 | Language pattern analysis |
| Step 5 Framing | Prevention/promotion | DS MacLean | Paul MacLean | 8125 | Limbic approach/avoidance |
| Step 6 Habit | Cue stability | the specialist engine | W.L. Bragg | 8150 | Task lattice recurrence |
| Step 6 Habit | Frequency from history | the specialist engine | Scoville | 8142 | Episodic memory |
| Step 6 Habit | Effort estimation | the specialist engine | Sterling | 8091 | Free energy (allostatic cost) |
| Step 7 Multi-Persp | Structure detection | the specialist engine | Roger Sperry | 8123 | Spatial architecture |
| Step 7 Multi-Persp | Panel composition | the specialist engine | Gazzaniga | 8127 | Corpus callosum synthesis |
| Step 8 If-Then | Trigger extraction | the specialist engine | Wernicke | 8124 | Language parsing |
| Step 8 If-Then | Plan attachment | the specialist engine | Bragg | 8150 | Task lattice |
| Step 9 MAP | Motivation verification | the specialist engine | Sherrington | 8104 | Interoception |
| Step 9 MAP | Ability verification | the specialist engine | Williams | internal | 8D capacity assessment |
| Step 9 MAP | Prompt verification | the specialist engine | Eccles | internal | Cerebellar comparator |
| PERMA (conditional) | 5-domain scoring | the specialist engine | Williams | internal | 8D wellbeing constructs |
| Directive Builder | Synthesis | the specialist engine | Gazzaniga | 8127 | Corpus callosum |
| Directive Builder | Jargon stripping | the specialist engine | Wernicke | 8124 | Voice engine |
| LLM Generation | Coaching text | the specialist engine | Andreasen | 8108 | Creative cortex |
| LLM Generation | Brand voice | the specialist engine | Wernicke | 8124 | Voice membrane |
| MAP Gate | Gap detection | the specialist engine | Eccles | internal | Comparator |
| MAP Gate | Step revision | the specialist engine | Broca | 8139 | Motor re-planning |
| Output Layer 1 | Coaching response | the specialist engine | Wernicke | 8124 | Final language |
| Output Layer 2 | Science trace | the specialist engine | Karl Popper | 8238 | Falsifiability metadata |
| Quality Gate | AI-tell removal | the specialist engine | Wernicke | 8124 | Language pattern |
| Quality Gate | Coherence check | the specialist engine | Kuramoto | 8010 | Phase synchronization |
| Checkpoint | FR acknowledgment | the specialist engine | Schultz | 8253 | Reward prediction error |
| Session State | Diagnostic persistence | the specialist engine | Scoville | 8142 | Episodic memory |
| Session State | Conversation history | the specialist engine | Scoville | 8142 | Episodic memory |
| Session State | Next checkin scheduling | the specialist engine | Jeffrey Hall | 8089 | Circadian clock |

## Advisory Panel Seats (sequential dispatch when multi-voice fires)

| Seat | Engine | Port | Lane |
|---|---|---|---|
| principal Advisory | the specialist engine | 8014 | Product genesis, strategy |
| Product Advisory | the specialist engine | 8014 | MVP and feature strategy |
| Marketing Advisory | the specialist engine | 8116 | Positioning and narrative |
| Design Advisory | the specialist engine | 8120 | Aesthetic, brand consistency |
| Research Advisory | the specialist engine | internal | Evidence evaluation |
| Legal Advisory | the specialist engine | 8109 | Regulatory and risk |
| Quality Gate | the specialist engine | 8122 | Prefrontal quality gate |
| Adversarial Review | the specialist engine | 8238 | Falsifiability gate |
| Synthesis | the specialist engine | 8127 | Integrates all advisor outputs |

## Migration: monolith to orchestration

Three changes required:

1. Wave becomes orchestrator. Python modules become reference implementations.
2. the specialist engine gets a COACHING_ROUTES dispatch table.
3. Each specialist gets a `/v1/coach/<micro-task>` endpoint. Standard contract: input (text, classification, diagnostics_so_far, context) to output (result, confidence, citation, framework_classification).

## Summary

22 specialist engines own 35+ micro-tasks. Wave is the orchestrator. Sherman is the dispatcher. Each specialist does ONE thing with its own methodology.
