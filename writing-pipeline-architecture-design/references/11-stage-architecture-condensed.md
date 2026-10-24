# 11-Stage Architecture Condensed Reference

Full architecture: `/<workspace>` (435 lines)

## 7 Design Principles

| # | Principle | Paper | Fixes |
|---|---|---|---|
| P1 | Recursive, not linear | Flower & Hayes 1981 (3,512) | No backward flow in pipeline |
| P2 | Pre-writing synthesis = highest leverage | Booth et al. 1995 (458); Flower & Hayes 1981 | No synthesis phase before drafting |
| P3 | Progressive drafting | Kellogg 2008 (839) | Single-shot generation |
| P4 | Multi-pass revision by level | Sommers 1980 (753); Flower et al. 1986 (376) | Single undifferentiated revision |
| P5 | Audience simulation required | Kellogg 2008 (839) | No audience model |
| P6 | AI scaffolds, never substitutes | Bastani 2025 (119, PNAS); Lee 2022 (334, CHI); Melumad & Yun 2025 (27, PNAS Nexus) | AI does cognitive work |
| P7 | Anti-homogenization | Doshi & Hauser 2024 (599, Science Advances) | No convergence safeguard |

## 11 Stages

```
0:  EVIDENCE GATE
1:  TOPIC → QUESTION → PROBLEM (Booth)
2:  RESEARCH + EVIDENCE TRIAGE (PRISMA / Liberati)
3:  SYNTHESIS + ARGUMENT ARCHITECTURE [NEW] — Toulmin skeleton
4:  PHYSICS/METHODOLOGY VALIDATION
5:  ADVERSARIAL PANEL — reviews skeleton, NOT draft (Walton)
6:  PROGRESSIVE DRAFTING — 3 passes (Kellogg)
7:  AUDIENCE SIMULATION [NEW] — reader modeling
8:  LEVELED REVISION — 3 levels × Detection/Diagnosis/Strategy
9:  HUMAN CHECKPOINT + ANTI-HOMOGENIZATION GATE
10: MULTI-FORMAT OUTPUT + SUBMISSION
```

## Toulmin Skeleton (Stage 3)

For central claim + each sub-claim, BEFORE any prose:
1. Claim (C): proposition asserted
2. Grounds (G): evidence mapped to sources
3. Warrant (W): inference rule G→C
4. Backing (B): foundation for warrant
5. Qualifier (Q): claim strength
6. Rebuttal (R): conditions where claim fails

Plus: claim dependency graph, evidence coverage map, Walton scheme classification.

## 3-Pass Progressive Drafting (Stage 6)

| Pass | Kellogg Stage | Goal | AI Role |
|---|---|---|---|
| 1 Knowledge-Telling | Novice | Externalize skeleton to prose | Constrained drafting |
| 2 Knowledge-Transforming | Competent | Discover/reshape argument | Scaffold — may modify skeleton |
| 3 Knowledge-Crafting | Expert | Manipulate reader model | Simulate reader trajectory |

## 3-Level Revision (Stage 8)

| Level | Question | Who Diagnoses |
|---|---|---|
| 1 Discourse | Does argument hold across document? | HUMAN |
| 2 Paragraph/Section | Does each unit serve the argument? | HUMAN |
| 3 Sentence | Is each sentence clear/precise? | Engine (automatable) |

Each level: Detection → Diagnosis → Strategy (Flower et al. 1986).
Order is strict: Level 2 cannot start until Level 1 signed off (Sommers Principle).

## Bastani Boundary

| Engine CAN | Engine CANNOT |
|---|---|
| Surface candidate sources | Decide which sources matter |
| Detect missing Toulmin components | Write the warrant |
| Generate Walton critical questions | Answer the critical questions |
| Simulate reader confusion | Decide how to address it |
| Detect revision problems | Diagnose/strategize fixes (Levels 1-2) |
| Generate sentence-level rewrites | Decide argument structure |
| Flag homogenization | Choose author's voice |
| Run physics validation | Interpret results for argument |

## CRUCIBLE Differences (4)

1. Toulmin for design decisions (claim = "build X this way")
2. 7 engineering Walton schemes: consequences, commitment, expert opinion, analogy, correlation-to-cause, waste, threshold
3. 9-seat panel (+ Security/Red Team + Systems Engineering + Bentham)
4. Technical audiences: implementing engineer, security reviewer, CTO/VP, future maintainer

## 32-Row Traceability Matrix (Complete)

| Design Decision | Paper(s) |
|---|---|
| Feedback loops all stages | Flower & Hayes 1981 |
| Synthesis/Argument Architecture stage | Booth 1995; Flower & Hayes 1981; Toulmin 1958 |
| Toulmin skeleton pre-drafting | Toulmin 1958; Osborne 2004 |
| Walton critical questions | Walton 2008 |
| PRISMA evidence triage | Liberati 2009 |
| Progressive drafting 3 passes | Kellogg 2008 |
| Knowledge-transforming modifies skeleton | Kellogg 2008; Sommers 1980 |
| Audience simulation stage | Kellogg 2008 |
| Leveled revision | Sommers 1980 |
| Detection→Diagnosis→Strategy | Flower et al. 1986 |
| Human Diagnosis+Strategy L1-2 | Bastani 2025; Lee 2022 |
| Sentence-level automatable | Flower et al. 1986 |
| Engine detects, doesn't fix | Lee 2022; Bastani 2025 |
| Panel reviews skeleton not draft | Osborne 2004; Walton 2008 |
| Panel deliberation synthesis call | Gap analysis M2 |
| Human cognitive checkpoint | Bastani 2025 |
| Anti-homogenization audit | Doshi & Hauser 2024 |
| Voice injection | Doshi & Hauser 2024 |
| Diversity sampling | Doshi & Hauser 2024 |
| No source pre-digestion | Melumad & Yun 2025 |
| Sources with metadata not summaries | Melumad & Yun 2025 |
| Structured search collaboration | Boussioux 2024 |
| CRUCIBLE Toulmin adaptation | Toulmin 1958; Walton 2008 |
| CRUCIBLE engineering Walton schemes | Walton 2008 |
| CRUCIBLE 9-seat panel | Boussioux 2024 |
| CRUCIBLE audience profiles | Kellogg 2008; Boussioux 2024 |
| Bastani Boundary table | Bastani 2025; Lee 2022 |
| Revision level ordering | Sommers 1980 |
| Crash recovery | Gap #3 |
| Rate limiting | Gap #4 |
| Human escalation/veto | Gap #7 |

## Verified Paper List (14, all citation counts via OpenAlex)

**Cognitive Science:** Flower & Hayes 1981 (3,512), Sommers 1980 (753), Kellogg 2008 (839), Flower et al. 1986 (376)
**AI Writing:** Doshi & Hauser 2024 (599), Bastani et al. 2025 (119), Lee et al. 2022 (334), Boussioux et al. 2024 (256), Melumad & Yun 2025 (27)
**Argumentation:** Osborne et al. 2004 (1,540), Toulmin 1958 (5,618), Walton et al. 2008 (1,351), Liberati et al. 2009 (28,000), Booth et al. 1995 (458)
