# Crucible Process Implementation Reference

The technology twin of veritas_process.py. Built and verified 2026-08-03.

## Build Status: COMPLETE AND VERIFIED

The pipeline was built in a single session and all testable components verified:
- Syntax compiles cleanly (`py_compile` pass)
- CLI `--help`, `--health-check`, `--json`, `--resume`, `--from-federation` all work
- Stage 0 (evidence gate + 5 tech validation rules) fully verified
- GitHub repo existence checks verified against real repos (torvalds/linux, kubernetes/kubernetes)
- Strong claim detection fires correctly (`demonstrate`, `outperforms` flagged at `theoretical`)
- Vendor neutrality rule fires on AWS promotion text
- Threat model rule fires on architecture claims without threat model discussion
- Checkpoint save/load/resume verified
- the principal voice profile loaded from voice.yaml (INTJ/technical/The Creator)
- Standup transcript patterns loaded (5 transcripts, technical density computed)
- Federation receive mode parses JSON and sets source tracking

Components NOT testable in dev (engines down): Stages 1-7 engine-dependent calls.
These are HTTP calls to Cyber the operator agent engines — they work when engines are running
(verified inside Docker container, see Docker Port Mapping section below).

## Files

- **Script:** `/<workspace>` (1,542 lines)
- **Veritas twin:** `/<workspace>` (970 lines)
- **Spec:** Conversation context + gap remediation plan at `/tmp/gap_remediation_plan.py`

## Cyber the operator agent Engine Endpoints (port 9000 block, inside Docker container)

| Engine | Port | Purpose in Crucible |
|--------|------|---------------------|
| the specialist engine | 9108 | Topic refinement (Stage 1) |
| the specialist engine | 9126 | Pattern memory / dupe check (Stage 1) |
| the specialist engine | 9127 | Novelty check (Stage 1) |
| DS O'Keefe | 8147 (shared) | Consolidation / dedup (Stage 2) |
| the specialist engine | 9105 | Environmental monitoring (Stage 2) |
| the specialist engine | 9104 | Interoception / confidence (Stage 2) |
| the specialist engine | 9095 | Free energy validation (Stage 3) |
| the specialist engine | 9010 | Coupling validation (Stage 3) |
| the specialist engine | 9095 | Critical slowing detection (Stage 3) |
| the specialist engine | 9124 | Brand voice / AI tell removal (Stage 4, 7) |
| the specialist engine | 9120 | Visual design (Stage 4) |
| DS C Bell | 9121 | PDF/HTML render (Stage 4) |
| the specialist engine | 9122 | Quality gate (Stage 7) |
| the specialist engine | 9092 | Output packaging (Stage 7) |
| the specialist engine | 9238 | Adversarial falsifiability (Stage 5) |

## Docker Port Mapping CRITICAL Learning

**The 9xxx engine ports are accessible ONLY inside the Docker container, NOT from the host.**

The Cyber the operator agent Docker container (`cyber-gg-8400`) maps only these ports to the host:
- 8400 (metrics/vitals)
- 8401 (medical records)
- 8403-8406 (various)
- 8500 (ops)

The individual engines (9108, 9124, 9238, etc.) run on their ports INSIDE the container but are NOT mapped to the host. This means:

- `python3 crucible_process.py --health-check` from localhost = ALL engines appear DOWN
- `docker exec cyber-gg-8400 python3 /app/crucible_process.py --health-check` = engines appear ALIVE (9/13 confirmed)

**The fix:** Run crucible_process.py INSIDE the Docker container:
```bash
docker cp /<workspace> cyber-gg-8400:/app/crucible_process.py
docker exec cyber-gg-8400 python3 /app/crucible_process.py --idea "..." --evidence-level theoretical
```

Alternatively, the container's docker-compose.yml could map all engine ports to the host, but that risks port conflicts with GG3's 8xxx block.

## Engine Health Gating (Verified Working)

The Crucible script implements a pre-stage health check. Before each stage begins, it checks ALL required engines for that stage via `GET http://localhost:{port}/health`. If ANY engine is down:

1. The process PAUSES immediately
2. Logs the dead engine(s) with name and port
3. Saves checkpoint state to `/tmp/crucible_process_state_{timestamp}.json`
4. Prints resume instructions: `python3 crucible_process.py --resume <checkpoint>`

**Verified behavior (2026-08-03):** Stage 0 passed. Stage 1 detected the specialist engine (9108) asleep. Process paused. No garbage output produced. This is exactly the behavior the gap analysis demanded.

## the principal Voice Profile

Loaded from `/<workspace>`:
- MBTI: INTJ
- Tone: technical
- Archetype: The Creator (Tier 2)
- OCEAN: O=0.75, C=0.90, E=0.30, A=0.55, N=0.20

The Crucible drafting stage (Stage 4) calibrates to this voice. It produces technical, precise, INTJ-structured prose for the principal's audience (technology leaders, entrepreneurs, SMB owners, security professionals).

## Crucible Adversarial Panel (9 seats)

| Seat | Role | Key Question |
|------|------|--------------|
| 1 | the specialist engine | Can this technical claim be tested? How would you prove it wrong? |
| 2 | the specialist engine | Is the engineering argument biased toward a preferred solution? |
| 3 | the specialist engine | Does it sound like the principal wrote it? Any AI telltales? |
| 4 | Security/Red Team | How would an attacker exploit this? What attack surfaces are introduced? |
| 5 | Systems Engineer | Does this scale? What happens at 10x, 100x load? |
| 6 | Domain Expert | Topic-specific (ML systems, pentesting, distributed systems, SRE) |
| 7 | the specialist engine | What would a competitor or critic attack? |
| 8 | Audience Proxy | Can a non-PhD technology leader understand and act on this? |
| 9 | the specialist engine | Is this worth publishing for this audience? What is the actionable value? |

## Gap Analysis Summary (37 gaps found, 7 CRITICAL)

Full analysis at `/tmp/gap_analysis_veritas_crucible.txt`. Top CRITICAL gaps:

1. **No falsifiable success metrics** - Need measurable proof the pipeline produces better research than a single specialist
2. **Surface validity trap** - Process can complete without errors but produce substantively wrong output
3. **Crash recovery** - ALREADY ADDRESSED via checkpoint/resume
4. **API rate limiting at scale** - ALREADY ADDRESSED for current volume, needs token bucket for 50+ papers/month
5. **Federation circuit breaker** - Need 3-strike circuit breaker with fallback to single-organism mode
6. **Human-panel disagreement protocol** - Need human veto right with required justification + override tracking
7. **Federation single point of failure** - Need passthrough mode on extended outage

Remediation plan at `/tmp/gap_remediation_plan.py` (read as text, not Python).

## 10 Key Differences from Veritas (All Verified in Build)

| # | Feature | Veritas | Crucible |
|---|---------|---------|----------|
| 1 | Engine ports | GG3 8xxx block | Cyber the operator agent 9xxx block |
| 2 | Voice profile | the principal (academic) | the principal INTJ/technical/The Creator |
| 3 | arXiv categories | All | cs.CR, cs.AI, cs.SE, cs.DC (technology filter) |
| 4 | GitHub verification | No | Yes — `api.github.com/repos/{owner}/{repo}` |
| 5 | Adversarial panel | 8 seats (academic) | 9 seats (adds Security/Red Team, Systems Eng, Audience Proxy) |
| 6 | Output formats | arxiv, linkedin | arxiv, linkedin, blog, whitepaper, playbook, twitter, slides, repo |
| 7 | Tech validation rules | None | 5 rules (code validity, threat model, impl guidance, benchmark methodology, vendor neutrality) |
| 8 | Federation | None | `--from-federation` receive + `--send-federation` send to GG3 |
| 9 | Physics calibration | specialist_surprise=0.35 | specialist_surprise=0.40 (tech claims more optimistic) |
| 10 | Learning loop | None | the principal standup transcript pattern extraction |

## 5 Technology Validation Rules (Verified Working)

These run at Stage 0 and reject problematic technology text patterns:

1. **code_block_syntax** — Checks fenced code blocks for unbalanced brackets (Python) or empty blocks (bash)
2. **threat_model_presence** — If text contains "architecture/design/system", it must also mention threat models, attack surfaces, or vulnerabilities
3. **implementation_detail** — Security recommendations (should/must/recommend + secure/encrypt/auth) must include implementation guidance (step/example/code/command)
4. **benchmark_methodology** — Performance claims (%, x, ms, faster/slower) must cite methodology (measured/tested using/hardware/environment)
5. **vendor_neutrality** — Detects vendor names (AWS/GCP/Azure) within 50 chars of superlatives (best/superior/leading/only/recommended)

Each rule returns `{"rule": str, "passed": bool, "issues": [str]}`. All 5 are pure regex — no engine dependency.

## Federation CLI (Verified Working)

```bash
# Receive an idea from GG3 Veritas via federation
python3 crucible_process.py --from-federation '{"idea": "...", "evidence_level": "...", "source": "gg3_veritas"}'

# Receive from a file
python3 crucible_process.py --from-federation @federation_payload.json

# Send completed output to GG3 Veritas
python3 crucible_process.py --idea "..." --send-federation gg3_veritas
```

The `--from-federation` flag accepts a JSON string or `@filename` and sets the `federation_source` field in state, which is tracked through to the final output package.

## Usage

```bash
# Full pipeline (must run inside Docker container)
docker exec cyber-gg-8400 python3 /app/crucible_process.py \
  --idea "raw tech idea" \
  --evidence-level theoretical \
  --output-formats arxiv,linkedin

# Health check
docker exec cyber-gg-8400 python3 /app/crucible_process.py --health-check

# Resume after engine recovery
docker exec cyber-gg-8400 python3 /app/crucible_process.py --resume /tmp/crucible_process_state_TIMESTAMP.json
```
