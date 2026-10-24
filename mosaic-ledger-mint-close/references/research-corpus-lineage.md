# Research corpus lineage + staleness classes

Depth for minting builds derived from the research corpus and for keeping
prior research from sitting stale. Canonical corpus:
`your-workspace/writing-studio/research_scans.db`.

## Corpus schema (verified by PRAGMA — run it before ANY insert)

`scan_results` columns: `id, topic_id, run_at, title, url, source, year,
cited_by, note, last_seen_at, seen_count`. Key facts:

- `id` is the PRIMARY key and MUST be a non-empty `sr-<slug>` seed (e.g.
  `sr-` + sha1(url)[:10]) — an autoincrement assumption fails with
  `id must be non-empty (seed with sr-<slug>)`.
- There is no `disposition`/`result_id`/`first_seen` column — triage state
  and promotion live in the note text (`REFERRAL-PROMOTE ...`) unless a
  separate triage table exists; PRAGMA first, never guess column names.
- Register referrals into the corpus in the SAME turn as the BUILD mint:
  one INSERT per finding with note = capture state + recovery path +
  mechanism summary, `seen_count=1`, `last_seen_at=now`.

## The lineage join (why builds carry sr-/st- keys)

Measured defect: the research corpus (5,000+ results) and the task ledger
shared ~4 join keys across 2,700+ tasks — research and construction were
separate islands, which is the mechanism behind "prior research sits
stale". The only durable fix is at the mint: every research-derived BUILD
detail carries `RESEARCH LINEAGE: sr-<id> st-<topic>` so the join grows
structurally. Archaeology-style backfill joins do not survive.

**False-join trap**: `detail LIKE '%st-%'` matches VERITAS stage strings
(`st-closure`, `st-ingestion`) — hundreds of false positives. Join against
real topic ids, not a substring — and take the vocabulary from
`SELECT DISTINCT topic_id FROM scan_results`, NOT from the `scan_topics`
registry table: `scan_topics` is sparse configuration (single-digit rows),
so treating it as the vocabulary silently drops most genuine joins and
makes the corpus↔ledger link look emptier than it is.

## Staleness classes (what a never-stale sweep measures)

Run retro sweeps inside the existing research tick (no new cron):

- **P1 never-triaged** — results with no triage record; the intake organ
  never touched them (hand-metabolized finds still count as untriaged).
- **P2 gone-stale high-seen** — results seen 3+ times whose `last_seen_at`
  predates a recency horizon; these are findings the scanner used to find
  and no longer does.
- **P3 promoted-unbuilt** — PROMOTE-class findings with no ledger task
  carrying their lineage keys; measure via lineage join, not title search.
- **P4 doc-drift** — long-form docs older than the newest scan result in
  their topic family.

All four counters go in the morning packet; a counter that stops falling
is itself a defect signal. Queue workdown through the gap pool, never as
side lists.

## Build-reinforcement classes (the action-side replay, P5–P7)

P1–P4 replay PERCEPTION (is research stale?); the built-thing reinforcement
pass replays ACTION — done BUILD rows re-examined against newer evidence and
their own proof obligations. Organ:
`your-workspace/organism/build_reinforcement_sweep.py`, composed into the
same research tick (no new cron), state at
`organism/build-reinforcement-state.json`.

- **P5 built-superseded** — done BUILD rows carrying a topic token where the
corpus holds evidence NEWER than the task's `done_at` (reinforce/improve
queue). Join tokens from detail against DISTINCT scan_results.topic_id
(real vocabulary, see false-join trap above).
- **P6 proof-class gap** — done rows whose own task_events admit
`P1 SUBSTANCE: 0/2 proof classes present`: claimed done, exit codes and
command output never captured. Probe:
`SELECT DISTINCT task_id FROM task_events WHERE detail LIKE '%P1 SUBSTANCE: 0/2 proof classes present%'`.
- **P7 metrics-promised-not-emitted** — done BUILDs whose GENOME `metrics=`
clause promised an emission with no post-done event recording a measurement
(detail has `metrics=`, no task_event carries `measured`). Telemetry
registered at birth but never born.

Rules: a zero P5 count is only meaningful once lineage stamps exist on done
rows (pre-stamp done rows carry no topic join at all — the zero is an
artifact, state it as such); P6/P7 findings route through the gap pool for
workdown, never as side lists; all three counters join the morning packet
and must trend to zero.

## Referral registration recipe (insert that works first try)

```python
import sqlite3, datetime, hashlib
db = sqlite3.connect('writing-studio/research_scans.db', timeout=15)
db.execute('PRAGMA busy_timeout=10000')
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
sid = 'sr-' + hashlib.sha1(b'<stable-seed>').hexdigest()[:10]
db.execute(
  "INSERT INTO scan_results (id, topic_id, run_at, title, url, source, "
  "year, note, last_seen_at, seen_count) VALUES (?,?,?,?,?,?,?,?,?,1)",
  (sid, 'st-<topic-slug>', now, title, url, source, year, note, now))
db.commit()
```

- The positional tuple must match the 10 columns exactly — building the
  row as a list-with-trailing-1 and then indexing it wrong is the classic
  `IndexError: tuple index out of range` failure; write the tuple inline.
- `note` is the durable capture: recovery path (resolved URLs, DOIs,
  mirror threads), mechanism summary, and the LAW-FOR-US — a future
  session should rebuild the whole finding from the note alone.
- Triage state lives in the note prefix (`REFERRAL-PROMOTE <date>`);
  count same-day promoted referrals with a LIKE on that prefix.
