# principal Interface Incidents & Overnight Contracts — 2026-08-27/28 session

Session detail for the laws patched into SKILL.md. Read when handling
principal-facing surfaces, overnight runs, or mint-gate failures.

## 1. The ratification-vs-decision button incidents (3 strikes, one fix)

Three separate times the principal opened the :port surface to ruling buttons
with no context. Two distinct root causes:

**Incident 1+2 (empty fallback):** `conduction_daemon.py` builds
`ceo_brief` per ruling card; the screen (conductor_screen.py lines
~816-825) renders What/Why/If-approved/If-rejected ONLY when the fields
exist. When a task was minted without a brief, the fallback left
`if_approved`/`if_rejected` EMPTY → title + buttons + nothing. Fix:
fallback always fills all four fields from the task record; then
restart daemon (`launchctl kickstart -k gui/$(id -u)/
com.your-org.conduction-daemon`), then LIVE-VERIFY via
`curl localhost:port/api/immune` checking every `rulings_pending[]`
entry has all four ceo_brief fields true. Note: /needs-you,
/api/decisions, /api/rulings are all unknown paths — the payload rides
`/api/immune` as `rulings_pending`.

**Incident 3 (wrong class entirely):** principal-verbatim orders minted as
kind=decision auto-rendered as pending rulings — re-asking permission
already given. Fix: ratification-vs-decision law (SKILL.md). Immediate
relief SQL: `UPDATE tasks SET state='done', detail = detail || ' |
ACK-AT-MINT ...' WHERE id IN (...)` — do NOT try actor_class='fleet'
(CHECK constraint rejects it).

**Lesson that generalizes:** when a principal defect reaches the principal twice,
the first fix dispatched targeted the wrong layer. Root-cause in the
LIVE EMITTER code before dispatching a fix.

## 2. Overnight / morning-delivery contract

- Overnight P0s (e.g. B2C provider-report pipeline before a 12:45
  appointment) are minted with the deadline INSIDE the task detail
  ("due before principal wakes 04:00-06:00 CDT").
- Morning packet = report draft + training report (what the system
  learned) + status report (shipped/healed/evolved), pushed on STIR
  DETECTION (presence law), not a blind cron.
- principal vocabulary: "AI timeline" = the OS OS timeline (event-driven,
  continuous). Never human meeting cadence.

## 3. Adversarial-heavy architecture panels

Trigger phrases: "don't tell me what I want to hear", "is this a good
design?", "I need more adversarial reviews". Shape: attack seats
outnumber research seats (~15+ vs ~8); the orchestrator states its own
preliminary lean, labels it preliminary, and puts it on the attack
list; verdict format = what each option LOSES. Worked example: per-
engine-memory vs shared-hippocampus question — neuroscience mirror
(brain = ONE hippocampus indexing distributed cortical storage) vs the
H.M. SPOF counterattack against the orchestrator's own lean.

## 4. Mint-gate failure chain (five attempts, one mint)

GENOME gate rejections in order: (1) apostrophe inside physics string
broke the regex → "no GENOME block"; (2) `body=clinical guardian` —
space; body must be single token; (3) `body=placenta` not in canonical
systems list → use `reproductive`; (4) `8d=privacy` not canonical →
use `accuracy`; (5) success. Debug path that worked: read the actual
GENOME_RE regex from ~/your-org/organism/genome_gate.py — the
error message lists all legal values anyway. Fix the named field; do
not retry blindly.

## 5. Vision analysis fallback chain (unresolved → not saved as method)

Auxiliary vision (NVIDIA NIM llama-3.2-90b-vision) returned 401 with
the config API key; llm-vendor LLM-4.5V also 401 (stale placeholder keys).
No working vision path was found this session — the image was never
analyzed. NOT captured as a skill rule (may be env-fixable); recorded
here only so a future session knows the attempt chain: config keys at
<agent-home>/config.yaml providers section were stale for both providers.

## 6. Downtime measurement pattern (reusable)

Backlog attribution: query message-bus timestamps, find gaps > 30min,
convert to America/Chicago, sum. Proven: 5.5h real downtime (4 gaps)
on 2026-08-27 — the backlog cause the principal correctly named vs my wrong
"principal volume" framing. Code sketch in the SKILL.md availability law;
gotcha: `timezone(timedelta(hours=-5))` not `astimezone(timedelta)`.
