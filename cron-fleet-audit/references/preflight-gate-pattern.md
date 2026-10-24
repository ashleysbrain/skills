# Preflight Gate Pattern for Cron Jobs

Remediation technique: gate LLM-spawning cron jobs so they only burn tokens when there's actual work to do. Developed 2026-06-18 during fleet-wide P0/P1 optimization.

## Core Concept

A cron job that spawns an LLM agent has two costs: tokens and API rate budget. Most fleet jobs run on a schedule regardless of whether anything changed since last run. A **preflight gate** is a lightweight script that runs *before* the LLM agent starts, checks whether work exists, and injects its verdict into the prompt. The LLM sees the verdict and either proceeds or skips immediately.

**Anatomy:**
```
cron tick
  → preflight script runs (exit 0 = work exists, exit 1 = no work)
  → script stdout injected into prompt context
  → LLM reads prompt, sees script output
  → if "NO_WORK": responds "Skipped" and stops (minimal tokens)
  → if "WORK": proceeds with full task (normal tokens)
```

## The Gate Script (`cron_preflight.py`)

Location: `/<workspace>`

Six gate primitives:

| Primitive | Use Case | Example |
|-----------|----------|---------|
| `files-newer --path DIR --since-hours N` | Has any file in DIR changed in the last N hours? | Advisory boards: skip if no coach/context files changed |
| `exists --path FILE` | Does a required input file exist? | Builder: skip if spec file doesn't exist |
| `nonempty-dir --path DIR` | Does a work queue directory have items? | Talent processor: skip if no requests queued |
| `git-commits --repo DIR --since-hours N` | Have there been commits? | Code audit: skip if no code pushed |
| `db-rows --db FILE --query SQL` | Are there new rows matching a query? | Analytics: skip if no new data |
| `hash-changed --path FILE --cache /tmp/X.hash` | Has a specific file changed since last run? | Remediation: skip if upstream findings unchanged |

Exit codes: **0 = work exists (proceed)**, **1 = no work (skip)**. Both print a human-readable verdict to stdout.

## Three Remediation Patterns

### Pattern 1: `no_agent` Conversion (Zero Tokens)

When an LLM cron job's only job is to narrate/format a script's output, the LLM is unnecessary. Convert the job to `no_agent: true` and point the `script` field at the script directly. Output is delivered verbatim. **Zero tokens, zero model calls.**

```python
# Before: LLM runs the script and narrates the output (~2k tokens)
# After:
cronjob update <job_id> no_agent=True script="python3 /path/to/script.py 2>&1"
```

**Test the script standalone first** — it must produce clean, complete output without the LLM wrapping it.

### Pattern 2: File-Based Preflight Gate

For LLM jobs that reason over workspace files (advisory boards, audits). Add a `script` field that checks for recent changes, and prepend a gate instruction to the prompt.

Script:
```bash
python3 /path/to/cron_preflight.py files-newer --path /workdir --since-hours 24 2>&1 || true
```

Prompt prefix:
```
PREFLIGHT GATE: A preflight check ran before this prompt. Its output appears above.
If it says "NO_WORK", respond with exactly: "Skipped — no new inputs since last run."
and STOP. Do not call any tools.

---
```

### Pattern 3: Hash-Based Gate (Chain Dependency)

For jobs that should only fire when a specific upstream output changed. Example: the specialist engine (remediation) should only run when the specialist engine (audit) produced new findings.

```bash
python3 /path/to/cron_preflight.py hash-changed \
  --path /path/to/upstream-output.md \
  --cache /tmp/upstream-output.hash 2>&1
```

The script stores a hash of the file on each run. If the hash matches last run's, it exits 1 (no change → skip).

## Critical Pitfalls

### 1. The `|| true` Requirement
`cron_preflight.py` exits **1** when there's no work (standard Unix convention: non-zero = "nothing to do"). But the the operator agent cron system may interpret non-zero exit as a script failure. For advisory board gates, **always append `|| true`** to force exit 0:
```bash
python3 cron_preflight.py files-newer --path DIR --since-hours 24 2>&1 || true
```
The LLM still sees the "NO_WORK" message in stdout and skips. Without `|| true`, the job may show as errored.

For `no_agent` jobs, do NOT use `|| true` — the script's own exit code doesn't matter since there's no LLM to interpret it.

### 2. Do NOT Gate Web-Research Jobs
Jobs that perform daily web searches (e.g., Research Advisory Board, market intelligence scans) should NOT have file-based gates. Their work is external (the web changes daily regardless of local files). A `files-newer` gate would incorrectly skip them every day the local workspace didn't change.

**Rule:** Only gate jobs whose inputs are local files. If the job's primary function is external data gathering, leave it ungated or use a different gate signal.

### 3. Test Scripts Standalone Before `no_agent` Conversion
Before converting an LLM job to `no_agent`, run the script manually and verify:
- It exits 0
- Output is clean (no tracebacks, no debug noise)
- Output is complete (the LLM was adding formatting/narration — make sure the raw script output is sufficient)
- The script doesn't need any LLM reasoning to produce correct output

### 4. Gate + Frequency Reduction for Rate-Limited Jobs
When a job is hitting 429 rate limits (too many API calls), apply BOTH:
- Preflight gate (skip when no work)
- Frequency reduction (e.g., every 4h → every 6h)

The gate alone helps, but if the model is rate-limited even on legitimate runs, reducing frequency is also needed.

## Measured Impact (2026-06-18 Fleet)

| Metric | Before | After | Reduction |
|--------|--------|-------|-----------|
| LLM runs/day | ~46 | ~20 | -56% |
| Blind runs (nothing changed) | ~35/day | ~8/day | -77% |
| 429 error loops | 2 | 0 | Eliminated |
| Token cost on idle days | Wasted | $0 | $0 |

## Jobs Modified (Reference)

### P0: `no_agent` Conversions (6 jobs)
- OpenRouter free model sync, Model compliance check, Fleet analytics sync, Obsidian sync, Executive task manager, the operator agent research pipeline

### P0: Gated + Frequency Reduction (2 jobs)
- the specialist engine: gate on `files-newer` for engine source dirs, schedule `*/4h` → `*/6h`
- the specialist engine: gate on `hash-changed` for Popper findings, schedule `*/4h` → `*/6h`

### P1: File-Based Gates (7 advisory boards)
- principal AM/PM, Marketing, Product, CTO, COO, Design — all gated on `files-newer --since-hours 24`

### P1: Excluded from Gate (1 job)
- Research Advisory — does daily web searches, file-based gate inappropriate

### P1: Specialty Gates (3 jobs)
- Talent Processor: `nonempty-dir` gate on request queue
- Engine Builder: `hash-changed` gate on SCIENCE_LAYERS.md
- SENTINEL: `files-newer` gate on audit directory
