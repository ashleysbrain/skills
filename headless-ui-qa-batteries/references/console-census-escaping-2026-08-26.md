# the OS Console session — 2026-08-26

Task Console v1→v2 (`~/your-workspace/relabel-work/task_console.py`, launchd
`com.divinity.task-console`, :port). Four defect classes, all found live:

## 1. Escaping collapse through Python→JS→HTML→prose
Prose apostrophe (`organism's`) inside a JS single-quoted string inside a
Python string: source `\\'` reached the browser as `'` → whole-page
`Unexpected identifier 's'`. Source-file read looked FINE; only SERVED bytes
broke. Fix: apostrophe-free copy + served-bytes gate (already in SKILL.md) +
source-vs-served byte-compare as the 10-second localizer:
```python
src = open(page_py,'rb').read().split(b'<script>')[1].split(b'</script>')[0]
served = curl_bytes.split(b'<script>')[1].split(b'</script>')[0]
# first differing byte IS the bug
```
Line-wise `new Function` prefix scans gave FALSE failures mid-function
(a prefix cut inside a multi-line return expression is not valid JS). Do not
use them as locators.

## 2. Truncate-display-not-parse
Fleet census scored 19/21 engines "down": probe did `json.loads(r.read().decode()[:400])`
— longer /health payloads failed parse → marked dead. Real state 21/21 (and
85/86 on the full ECS registry). Parse full, truncate only display strings.

## 3. kickstart vs bootout on stale daemons
`launchctl kickstart -k <label>` re-execed the OLD module once (err log still
showing pre-patch line numbers). Escalation ladder: kickstart → verify served
marker → if stale, `launchctl bootout gui/$(id -u)/<label>` + `bootstrap`.

## 4. Registry census discipline (principal correction)
First census hardcoded ~14 "known" engines (wrong). Second parsed
`agents.yaml` (21 — one operator's owned-organs list, not the organism).
principal: "21 organs????? ... way more than this". Canonical source:
`your-org/organism/ENGINE_REGISTRY.yaml` — 96 engines across 15 body
systems, generated from `agent-organism/ecs.py`. Census = canonical registry,
never memory, never a single operator's manifest. Related registries in the
same body: flows (55, stores/flow-registry.json), laws (10 pinned,
stores/law-block.md), equations (12), isomorphisms (13), personas/engines.json
(27), ledger tasks (2,100+).

## Scope correction (same session)
principal rejected a single-purpose queue page as "way off — content and features":
surface family must fold multi-organism views, calendar, OS chat, research.
Typography (14px/13.5/11.5, -apple-system, dark #141312/#7bb8a1 accent) was
explicitly approved and is the house style for these consoles. Build ON the
existing platform family (hydra-os/gg-ops-platform.html :port/:port/:port,
circadian conductor :port, Simard :port) — census before build.

## Write-path battery (three assertions, one POST)
`POST /api/decide {approve}` → assert (a) `tasks.state='done'` + outcome,
(b) `task_events` row `ceo-approve` actor `ceo/human`,
(c) `message-bus.db` messages row `[console] principal approve on <id>` (msg #4268
verified). Carrier post wrapped in try/except so bus-down degrades to
`bus_msg: null` without blocking the ruling.
