# Human-AI Interaction Design: The Experience Layer (Round 4)

Round 4 of the writing pipeline audit. The mechanical architecture (stages,
contracts, feedback loops) was complete through 23 sections. What was missing
was the HUMAN EXPERIENCE of working inside the pipeline. A pipeline that is
mechanically perfect but cognitively overwhelming, emotionally crushing, or
creatively deadening will be abandoned.

## Papers Grounding This Layer

| Paper | Cites | Key Finding |
|---|---|---|
| Sweller, Ayres & Kalyuga (2011) Cognitive Load Theory | 2,064 | Working memory limited to 4±1 items. Exceeding it collapses performance. |
| Logg, Minson & Moore (2019) Algorithm Appreciation | — | Humans show bipolar trust with AI (over-trust or under-trust). |
| Dietvorst, Simmons & Massey (2015) Algorithm Aversion | — | People reject algorithms after seeing ONE error. |
| Tversky & Kahneman (1974) Heuristics and Biases | 54,000+ | First output anchors all subsequent thinking. |
| Csikszentmihalyi (1990) Flow | — | Optimal creative state needs challenge-skill balance. |
| Amabile (1983) Social Psychology of Creativity | — | Environment affects intrinsic motivation. |
| Zimmerman (2002) Self-Regulated Learning | — | Metacognitive awareness is teachable and is the key expert-novice differentiator. |
| Katz & Martin (1997) Research Collaboration | — | Collaboration creates conflicts needing resolution mechanisms. |

## The 10 Interaction Design Dimensions

### 1. Cognitive Load Management — Progressive Disclosure Protocol
Revision findings NEVER shown all at once. Level 1 (discourse) max 5 findings.
Level 2 (paragraph) one section at a time. Level 3 (sentence) batch-accepted.
Green/yellow/red cognitive load indicator.

### 2. Trust Calibration — Show Your Work Protocol
Every verdict includes a reasoning trace. "Citation [3] claims Friston 2010
supports active inference. Bigram overlap: 0.12. Verdict: unsupported." Per-seat
trust history tracked across papers.

### 3. Creative Friction Budget
Productive friction stages (1, 2, 3, 5, 8L1, 9A): human REQUIRED to engage.
Unproductive friction (8L3, 10, formatting): engine handles automatically.
Flow protection mode during Stage 6 drafting: all notifications silenced.

### 4. Anti-Anchoring — Blank-First Protocol
Stage 3 begins with BLANK CANVAS. Engine asks Socratic questions BEFORE
generating skeleton. Human's independent intent captured. Only then engine
generates candidates. Divergences surfaced.

### 5. Authorship Identity Preservation
Every paragraph tagged: human_seed, engine_generated, human_revised,
human_authored. Introduction and Discussion ALWAYS human-seeded (first 200
words). Target: 30%+ human-authored content. Below 30% triggers warning.

### 6. Collaborative Conflict Resolution — Structured Dissent
Margin comment types: objection, confusion, gap, alternative, question.
Response types: conceded, defended, deferred, escalated. 3+ unresolved
defended objections on same claim triggers Bastani gate for BOTH authors.

### 7. Pipeline as Coach
Personal Writing Report after each paper. Pattern tracking across papers
("your warrants are challenged 60% of the time"). Skill progression mapped to
Kellogg stages. Suggested exercises for weaknesses.

### 8. Emotional Intelligence in Feedback
Strengths first. Findings framed as opportunities not errors. Progress
visualized. Blocking findings paired with suggested fixes. NEVER more than 7
findings visible at once.

### 9. Creative Environment
Three modes: FOCUS (only current task), REVIEW (split text+findings), OVERVIEW
(full dashboard). Manrope+Sora fonts. Dark warm surfaces (#0a0c12). Moonlight
gold. NO purple/indigo. Circadian rhythm integration (the specialist engine).

### 10. Metacognitive Prompts
One mandatory question per stage transition:
- 1→2: "What do you EXPECT to find? What would surprise you?"
- 3→5: "If the panel rejects your claim, what's the most likely reason?"
- 6→8: "What part are you LEAST confident about?"
- 8→9: "Has your thinking changed from your original intent?"
- 9→10: "Explain this paper to a non-expert in one sentence."

## Runtime Verification (This Session)

All 16 Writing Studio endpoints verified returning HTTP 200. Pipeline produces
3,648 words, 12 unique [N] citations across 9 gathered papers, 0 phantom
citations, 0 fabricated metrics, 0 em dashes, 0 AI telltales. Server (:port)
and gateway (:port) both healthy.

## Delegation Pattern Lesson

Specialists repeatedly timed out (600s) during deep reasoning passes on this
architecture work. Pattern: specialist reads full doc (fast), then spends the
rest of its time reasoning through complex multi-dimensional analysis and never
writes output. When this happens, the parent agent should do the synthesis work
itself rather than re-dispatching. The specialist's VALUE was in the research
gathering (finding papers, extracting findings), not in the final synthesis.
Parent agent has full context and can write faster than re-dispatching.
