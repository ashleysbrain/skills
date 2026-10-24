# Adversarial Engines Catalog

## Engine #1: DS ATC-01 Competitive Analysis

**DS-ECS:** DS-ECS-ATK-01-01-v1.0.0
**Port:** 8201
**Scientists:** Michael Porter + Richard Rumelt
**Domain:** Competitive intelligence
**Primary Frame:** Porter's Five Forces + Rumelt's Strategy Kernel

### Specializations

| Methodology | Code | Best For |
|-------------|------|----------|
| Five Forces Analysis | ATC-M01 | Competitive intelligence, market research, threat assessment |
| Value Chain Analysis | ATC-M02 | Margin analysis, activity analysis, cost structure |
| Competitive Advantage Framework | ATC-M03 | Strategy evaluation, competitive positioning, market share |
| Strategy Kernel Evaluation | ATC-M04 | Strategy evaluation, coherence check, feasibility analysis |
| Strategic Groups Mapping | ATC-M05 | Market positioning, strategic groups, market share |

### Personalities

- The Porter Analyst (Porter's Five Frames)
- The Rumelt Skeptic (Strategy kernel critic)
- The Value Chain Hacker (Margin analyst)
- The Market Positioner (Share analyst)
- The Five Forces Stalker (Threat analyst)

### 5-Seat Adversarial Panel

1. Porter Seat — Five Forces Analysis
2. Porter Seat — Competitive Advantage Framework
3. Porter Seat — Value Chain Analysis
4. Porter Seat — Market Positioning
5. Rumelt Seat — Strategy Kernel Evaluation

### Status

✅ Built and tested
✅ Registered in ENGINE_REGISTRY.yaml
✅ Executed on the specialist engine strategy (2026-07-02)

### Vulnerabilities Found (2026-07-02 Execution)

| # | Vulnerability | Severity |
|---|---------------|----------|
| V1 | Substitute threat is VERY HIGH (free AI scoring) | CRITICAL |
| V2 | Competitive rivalry is VERY HIGH (building ON competitors) | CRITICAL |
| V3 | "Proprietary scoring" moat is weak (12-18 month replication) | HIGH |
| V4 | Buyer power is HIGH (low switching costs) | HIGH |
| V5 | No coherent guiding policy | MEDIUM |

---

## Engine #2: DS ATC-02 Regulatory Attack

**DS-ECS:** DS-ECS-ATK-02-01-v1.0.0
**Port:** 8202
**Scientists:** David Kessler (former FDA Commissioner)
**Domain:** Regulatory compliance
**Primary Frame:** FDA Medical Device Classification + FTC Health Claims + HIPAA

### Specializations

| Methodology | Code | Best For |
|-------------|------|----------|
| FDA Medical Device Classification | ATC-M11 | Medical device determination, regulatory pathway |
| FTC Health Claim Substantiation | ATC-M12 | Health claim evidence review, enforcement risk |
| HIPAA Compliance Audit | ATC-M13 | PHI handling, data security, breach risk |

### Personalities

- The Kessler Regulator (FDA enforcer)
- The FTC Lawyer (Health claim prosecutor)
- The HIPAA Auditor (Data privacy enforcer)

### 5-Seat Adversarial Panel

1. Kessler Seat — FDA Medical Device Classification
2. Kessler Seat — FTC Health Claim Substantiation
3. Kessler Seat — HIPAA Compliance
4. Porter Seat — Regulatory Moat Analysis
5. Rumelt Seat — Regulatory Strategy Kernel

### Status

✅ Built and tested
✅ Registered in ENGINE_REGISTRY.yaml
⏳ Pending execution on the specialist engine strategy

---

## Engine #3: DS ATC-03 Moat Stress-Test

**DS-ECS:** DS-ECS-ATK-03-01-v1.0.0
**Port:** 8203
**Scientists:** Warren Buffett + Charlie Munger
**Domain:** Moat vulnerability
**Primary Frame:** Buffett's Moat Analysis + Munger's Lollapalooza Effect

### Specializations

| Methodology | Code | Best For |
|-------------|------|----------|
| Moat Analysis | ATC-M21 | Moat strength, durability, types |
| Lollapalooza Effect Analysis | ATC-M22 | Advantage compounding, virtuous cycles |
| Value Vulnerability Analysis | ATC-M23 | Moat strength vs valuation |

### Personalities

- The Buffett Moat Hunter (Moat analyst)
- The Munger Lollapalooza Analyst (Advantage compounder)
- The Graham Value Skeptic (Value investor)

### 5-Seat Adversarial Panel

1. Buffett Seat — Moat Analysis
2. Munger Seat — Lollapalooza Effect
3. Graham Seat — Value Vulnerability
4. Fisher Seat — Scuttlebutt (customer/competitor intelligence)
5. Peter Lynch Seat — Growth Moat

### Status

✅ Built and tested
✅ Registered in ENGINE_REGISTRY.yaml
⏳ Pending execution on the specialist engine strategy

---

## Engine #4: DS ATC-04 Timeline Hack

**DS-ECS:** DS-ECS-ATK-04-01-v1.0.0
**Port:** 8204
**Scientists:** Fred Brooks
**Domain:** Timeline feasibility
**Primary Frame:** Brooks' Law + No Silver Bullet

### Specializations

| Methodology | Code | Best For |
|-------------|------|----------|
| Brooks' Law Analysis | ATC-M31 | Timeline multiplier, realistic timeline |
| No Silver Bullet Analysis | ATC-M32 | Essential vs accidental work, complexity growth |
| Software Estimation Error Analysis | ATC-M33 | Realistic estimate, error factor, confidence |

### Personalities

- The Brooks Skeptic (Timeline realist)
- The No Silver Bullet Hunter (Essential vs accidental work analyzer)
- The Conway Law Critic (Organizational structure analyst)

### 5-Seat Adversarial Panel

1. Brooks Seat — Brooks' Law Analysis
2. Brooks Seat — No Silver Bullet Analysis
3. Conway Seat — Conway's Law (organizational structure = software architecture)
4. Myers Seat — Software Estimation Error
5. Lynn Conway Seat — VLSI Design Complexity

### Status

✅ Built and tested
✅ Registered in ENGINE_REGISTRY.yaml
⏳ Pending execution on the specialist engine strategy

---

## Engine #5: DS ATC-05 Customer Psychology Breaker (PLANNED)

**DS-ECS:** DS-ECS-ATK-05-01-v1.0.0
**Port:** 8205
**Scientists:** Daniel Kahneman + Richard Thaler
**Domain:** Customer psychology
**Primary Frame:** Cognitive Biases + Nudge Economics

### Planned Specializations

| Methodology | Code | Best For |
|-------------|------|----------|
| Loss Aversion Analysis | ATC-M41 | Loss aversion, framing effects, risk aversion |
| Nudge Effect Analysis | ATC-M42 | Default options, behavioral interventions |
| Cognitive Bias Detection | ATC-M43 | Bias identification, behavioral deviation |

### Status

⏸️ Planned (not yet built)

---

## Execution Priority

1. **ATC-01** — Competitive Analysis (✅ EXECUTED)
2. **ATC-02** — Regulatory Attack (⏳ PENDING)
3. **ATC-03** — Moat Stress-Test (⏳ PENDING)
4. **ATC-04** — Timeline Hack (⏳ PENDING)
5. **ATC-05** — Customer Psychology Breaker (⏸️ PLANNED)

## Cross-Engine Coordination

Engines can be executed in parallel (delegate_task) for comprehensive adversarial coverage, or sequentially for deeper dive into specific vulnerabilities.

Each engine produces:
- Engine metadata (get_engine_info())
- Selected methodology and personality (select_methodology())
- Adversarial context (attack_type, seat_count, primary_frame, secondary_frame)
- Vulnerability list (severity, fix required)

## Adversarial Attack Workflow

See `references/adversarial-execution-pattern.md` for detailed execution workflow.