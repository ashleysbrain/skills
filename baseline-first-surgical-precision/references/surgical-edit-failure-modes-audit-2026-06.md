# Surgical Edit Failure Modes — Audit 2026-06-06

Source: COO/AI orchestration audit of session `20260605_165342_89cf52` (101 messages).

## Failure modes observed

### FM-1: Full-document rewrite instead of surgical edit
User approved a 165-page fleet PDF and requested surgical category edits. Assistant generated a new condensed 5-page summary PDF instead of patching the existing artifact. MEMORY.md already contained "prefers patching existing docs over rewrites" and the `baseline-first-surgical-precision` skill was loaded. Neither was enforced at action-time.

### FM-2: Overreading a one-line autocorrect correction
User sent "veins = crons" (autocorrect fix). Assistant spent 4 turns interpreting, re-explaining, and offering menus. User had to say "No" and "Read my prior message" before it stopped.

### FM-3: Compression-induced context amnesia
Aggressive compression (target_ratio 0.2, protect_last_n 20) lost the specific artifact identity post-compaction. After compaction, the assistant generated the wrong artifact because the compaction summary preserved task state but not which exact file was the baseline.

### FM-4: Memory loaded but not enforced
Preferences present in MEMORY.md and skills loaded into context were treated as advisory, not mandatory. No pre-flight gate checked them before artifact generation.

### FM-5: Poor ordering of multi-part requests
User sent 3 directives in one message (surgical edits + don't rename + remove cribs). Assistant jumped to execution without decomposing into an ordered task list. No skill addressed instruction decomposition for multi-part requests.

### FM-6: Circular work / artifact proliferation
Session produced 8+ PDF artifacts for the same fleet document. Multiple versions sent to Telegram. `sibling-agent-fleet-lock-in` skill was created mid-session to lock the canonical source, but damage was already done.

## Repairs applied to skills

| Skill | Repair | Section added |
|---|---|---|
| `baseline-first-surgical-precision` | Mandatory pre-flight constraint gate | New section after Core rule |
| `baseline-first-surgical-precision` | Compression amnesia + artifact proliferation pitfalls | Extended Pitfalls section |
| `sibling-agent-fleet-lock-in` | Lock-state persistence to MEMORY.md | New section |
| `sibling-agent-fleet-lock-in` | Anti-proliferation rule (1 file per deliverable) | New section |
| `adhd-executive-function-support` | Multi-part request decomposition pattern | New section |
| `adhd-executive-function-support` | Noise-correction silent absorption | New subsection |

## Config-level findings (not patched here — require manual config edit)

- Compression settings too aggressive for precision work: `target_ratio: 0.2` → recommend 0.35, `protect_last_n: 20` → recommend 35
- Session model `gpt-5.4-mini` may be underpowered for large-artifact surgical editing
- No smart model routing for editing sessions

## Overlap note

`baseline-first-surgical-precision` and `execution-over-documentation` overlap on "don't over-engineer, just do the minimal thing." Both skills are class-level umbrellas that govern edit discipline from slightly different angles. A future consolidation pass could merge their shared rules.
