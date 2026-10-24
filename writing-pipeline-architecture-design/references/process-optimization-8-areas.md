# Process Optimization: 8 Areas (Section 21)

## 21.1 Concurrent Drafter + Reader Model

Stage 6 Pass 3 runs the reader model CONCURRENTLY with generation via a shared
live document buffer.

**Coordination protocol:**
- Drafter generates one section, writes to shared buffer
- Reader model polls at section boundaries (NOT mid-paragraph — paragraph
  atomicity prevents race conditions)
- Reader flags comprehension problem in Section N → drafter receives finding
  BEFORE starting Section N+1
- Drafter revises Section N, then proceeds

**Why section-boundary, not character-level:** Character-level coordination
creates more race conditions than insight. Section boundaries are natural
cognitive checkpoints. Engineering decision grounded in cognitive principle.

Grounded in: Flower & Hayes (1981), Kellogg (2008).

## 21.2 Model Routing

| Stage | Model | Why |
|---|---|---|
| 0: Evidence Gate | Flash 4.5 | Mechanical metadata check |
| 1: Topic → Problem | Human + Flash 4.5 | Human thinks; engine checks scope |
| 2: Research Gathering | Flash 4.5 (search) + 5.2 (triage) | Search mechanical, triage judgment |
| 3: Argument Architecture | LLM-5.2 (16k) | Deep reasoning — highest-stakes task |
| 4: Physics Validation | LLM-5.2 | Domain reasoning |
| 5: Panel (per seat) | Flash 4.5 (mechanical), 5.2 (domain) | Mix by seat type |
| 6 Pass 1: Knowledge-telling | Flash 4.5 | Fast generation |
| 6 Pass 2: Knowledge-transforming | LLM-5.2 (16k) | Contradiction detection |
| 6 Pass 3: Knowledge-crafting | LLM-5.2 + concurrent reader | Both need depth |
| 7: Audience sim | Flash 4.5 | Pattern matching |
| 8 L1-2: Detection | LLM-5.2 | Structural analysis |
| 8 L3: Sentence polish | Flash 4.5 | Mechanical editing |
| 9B: Homogenization | Flash 4.5 + Python | Computational metrics |
| 10: Output | Flash 4.5 + Python | Formatting |

**Cost impact:** ~40% token cost reduction, ~50% wall-clock time reduction.

## 21.3 Confidence Scoring

Graduated confidence (0.0-1.0) per artifact:
- Toulmin skeleton: each claim/warrant/grounds has confidence score
- Panel verdict: weighted aggregate of seat confidences
- Revision findings: each finding has severity AND confidence

**Confidence drives behavior:**
- Revision prioritizes LOW-confidence areas first
- Claims < 0.4 → auto-flagged for human diagnosis
- Claims > 0.8 with no panel objections → fast-path (skip L1-2 revision)

## 21.4 Cross-Paper Learning

After Stage 10, extract process metrics to pipeline-memory database:
- Which Walton schemes fail most often → flag early
- Which evidence sources reused → trusted-source list
- Which voice patterns flagged → update voice profile
- Which Stage 1 formulations led to clean pipelines

Feedback: Stage 2 auto-prioritizes trusted sources, Stage 3 flags high-failure
schemes, Stage 9B calibrates thresholds from accumulated data.

## 21.5 Adaptive Depth

| Paper Type | Full | Light | Skip |
|---|---|---|---|
| Full research paper | All 11 | — | — |
| Conference abstract | 0,1,3(light),10 | 5(2 seats) | 2(light),6(1 pass),7,8(L3),9B |
| Position paper | 0,1,3,5,6(2),8(L1),10 | 2 | 7,9B |
| Review article | 0,1,2(deep),3,5,6(3),7,8,10 | — | — |
| CRUCIBLE spec | 0,1,3,4,5(11),6,8,10 | 2 | 7(opt) |

## 21.6 Streaming Progress

- Stage 5: Panel seats deliver verdicts as they complete
- Stage 6: Draft streams word-by-word into Writing Studio
- Stage 8: Revision findings appear as detected
- Stage 2: Search results stream as each API responds
- Human can intervene mid-stage (pause, comment)

## 21.7 Enhanced Evidence Fusion

```
score = 0.30 * RRF_rank_score
      + 0.25 * (citation_authority / max_citations)
      + 0.20 * recency_bonus
      + 0.25 * toulmin_role_match
```

Toulmin role match: sources filling under-filled roles get fusion bonus.

## 21.8 Citation Graph Integration

Within the gathered-paper subgraph:
- **Indegree:** Cited BY many gathered papers → foundational → auto-include
- **Outdegree:** CITES many gathered papers → likely review → flag
- **Bridge papers:** Connect two clusters → interdisciplinary connectors
- **Citation context:** Classify edges as supporting/contrasting/mentioning
