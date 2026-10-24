# Roadmap Ground-Truth Verification Recipes

Recipes for verifying whether a DS organism roadmap's claimed milestones
match reality. Companion to the "Roadmap Status Review Protocol" section
in SKILL.md. Learned from the 2026-07-19 weekly review of
`agent-organism/docs/ORGANISM-ROADMAP-AND-CONFERENCE-2026.md`.

## The Core Principle

A roadmap table is the **claimed state**. Ground truth lives in:
- Live HTTP services
- The operator bus (sibling-handoff SQLite)
- The filesystem (deliverable files)
- The immune patrol scan
- External sources (for dated events)

When the table says "Complete" or "Scheduled" but ground truth is silent,
the milestone did not happen. Report the gap honestly — do not summarize
the table's claims as if they were facts.

## 1. Live Service Probes

The gateway at `:port` has two health surfaces. They are NOT equivalent:

- `GET http://localhost:port/health` — gateway-only status. Returns
  `{status: ok, engine: "the specialist engine"}`. Says nothing about the
  fleet. Using this as your fleet check produces a false green.
- `GET http://localhost:port/organism/health` — full fleet summary.
  Returns `{alive: [...], down: [...], engines: {...}}`. This is the
  real ground truth for liveness.

```python
import urllib.request, json
r = urllib.request.urlopen('http://localhost:port/organism/health', timeout=10)
data = json.loads(r.read())
alive = len(data.get('alive', []))
down = len(data.get('down', []))
print(f'Fleet: {alive} alive, {down} down')
```

On 2026-07-19 this returned `14 alive, 0 down` — but the roadmap target
was 107 bootable. A 13% liveness rate against a roadmap that claimed
Phase 1 "complete" was the single most important finding of the review.

## 2. Operator Bus Queries

The canonical bus is `/<workspace>` (~1368
messages). Subdirectory copies (`agent-organism/message-bus.db`,
`gigi3/message-bus.db`) are fragments and misleading.

Schema:
```
id, timestamp, from_op, to_op, msg_type, subject, content,
status, claimed_by, claimed_at, done_at, result,
in_reply_to, closes
```
Note: the body column is `content`, NOT `body`.

CLI reader flags (these changed — do not assume):
```
python3 organism/opencode_bus_read.py            # summary, last 24h
python3 organism/opencode_bus_read.py --since N  # messages with id >= N
python3 organism/opencode_bus_read.py --json     # machine-readable
```
THERE IS NO `--since-id`, `--include-from`, or `--to` filter by sender.
Filter in Python after `--json`.

```python
import sqlite3
conn = sqlite3.connect('/<workspace>')
cur = conn.cursor()
# Most recent messages FROM sibling-agent (sibling work confirmation)
cur.execute("""SELECT id, timestamp, msg_type, subject, content
               FROM messages WHERE from_op='sibling-agent'
               ORDER BY id DESC LIMIT 8""")
for row in cur.fetchall():
    print(f'[{row[0]}] {row[1][:19]} ({row[2]}) {row[3]}')
    print((row[4] or '')[:400])
```

Key signals:
- **Absence of `sibling-agent` inbound during a milestone window** = sibling
  did not ship that work, regardless of what the table claims.
- **75+ messages pending on the bus** = backlog; recent sibling work is
  frontend ops, not roadmap backend milestones.
- Bus messages are the sibling's self-report. For externally verifiable
  work, still confirm against services/files.

## 3. Filesystem Archaeology

When the roadmap names specific deliverables (engines, abstracts,
submission artifacts), grep the filesystem for them. Zero hits = not
started, no matter what the table says.

```python
from pathlib import Path
gg = Path('/<workspace>')
# Check for the named engines the roadmap promises this phase
for name in ['metchnikoff', 'galen', 'bernard', 'cannon', 'hall', 'quartz']:
    hits = list(gg.rglob(f'*{name}*'))
    print(f'{name}: {len(hits)} files')
```

On 2026-07-19 this immediately surfaced that Galen (immune patrol, due
in 24h), Bernard and Cannon (homeostasis, due in 6 days) all had zero
files — Phase 2 milestones were silently at-risk despite the table
implying a smooth sequence.

### Engine-Count Heuristics and Their False Negatives

Counting `ds-*-engine` directories gives a stable number (~103), but it
does NOT mean they are built. Many are stubs. Reliable signals:

```python
# Engine dirs with ANY .py file
engine_dirs = [d for d in gg.iterdir()
               if d.is_dir() and d.name.startswith('ds-') and d.name.endswith('-engine')]
with_code = [d for d in engine_dirs if any(d.rglob('*.py'))]
print(f'{len(with_code)}/{len(engine_dirs)} have code')

# Engines actually importing service_mesh
mesh_importers = 0
for d in engine_dirs:
    for pyf in d.rglob('*.py'):
        if 'service_mesh' in pyf.read_text(errors='ignore'):
            mesh_importers += 1
            break
print(f'{mesh_importers} engines import service_mesh')
```

WARNING: counting `app.py`/`main.py`/`server.py` at the engine root is a
weak heuristic — only 1 of 103 engines had that layout on 2026-07-19.
Use `rglob('*.py')` for any Python presence, then verify liveness via
the `/organism/health` endpoint, not the directory listing.

## 4. Immune Patrol as Roadmap Validator

The the specialist engine engine (`scripts/ds-metchnikoff.py`) is the organism's
own innate immune scan. Run it during any roadmap review — its findings
are independent ground truth the roadmap table cannot fake.

```bash
cd /<workspace>
python3 scripts/ds-metchnikoff.py --json | python3 -c "
import sys, json
data = json.load(sys.stdin)
findings = data.get('findings', [])
from collections import Counter
sev = Counter(f.get('severity') for f in findings)
print(f'Total: {len(findings)}, by severity: {dict(sev)}')
crit = [f for f in findings if f.get('severity') == 'CRITICAL']
print(f'CRITICAL: {len(crit)}')
"
```

Interpretation:
- **0 CRITICAL, many WARNING** = mostly stale doc references; system
  fundamentally healthy but docs rotting (the normal state).
- **>0 CRITICAL** = real gaps the roadmap did not surface. Each CRITICAL
  finding is a roadmap-table claim that fails reality.
- The 11 cancer types map to specific integrity failures (contradiction,
  drift, hallucinated, stale reference, etc.). See the script header for
  the full taxonomy.

## 5. External Verification for Dated Events

Roadmaps reference conferences, deadlines, and external events. These can
change or be cancelled without the roadmap being updated. Two failure
modes seen on 2026-07-19:

**Failure mode A: stale cancellation doc about a DIFFERENT event.**
`hydra-os/intel/research/TSC-2026-PREPARATION.md` said "TSC 2026
CANCELLED" — but that referred to TSC Tucson (April 2026). The roadmap's
TSC San Diego (October 2026) was real and confirmed at
`consciousness.arizona.edu`. Conflicting docs about similarly-named
events are common. Resolve by checking the authoritative external
source, not by guessing or by trusting whichever doc you read first.

**Failure mode B: missed deadline with no submission evidence.**
The roadmap said "Abstract submitted to TSC 2026" was due July 14. On
July 19 (4 days after), there was:
- No VERITAS audit record on the bus
- No submission confirmation file on disk
- No Telegram delivery of a submission confirmation
- The roadmap's own VERITAS table showed steps as "Scheduled" (the
  initial state), never updated to "Complete"

A missed deadline with no evidence is the highest-priority finding in
any roadmap review. Surface it to the user immediately — do not soften
it, do not assume it happened offline.

**Web-search the authoritative source for any dated external event:**
```
TSC 2026 "Science of Consciousness" San Diego Paradise Point October
```
The official site (`consciousness.arizona.edu`) confirmed the event and
its July 15 abstract deadline, making the missed-submission finding
concrete and actionable rather than speculative.

## What NOT to Trust

- The roadmap's own status column ("Complete", "Scheduled", "In Progress")
  — these rot. Verify each against ground truth.
- Subdirectory copies of `message-bus.db` — only the workspace-root copy
  is canonical.
- `/health` (gateway-only) when you need fleet status — use
  `/organism/health`.
- Engine directory counts as a proxy for "built" — many are stubs.
- The absence of a CRITICAL immune finding as proof of health — WARNINGs
  accumulate into meaningful drift over time.
- Any single doc's claim about an external event when a similarly-named
  event exists. Verify externally.
