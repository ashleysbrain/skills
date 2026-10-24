# GENOME gate, source verification, outcome honesty (2026-08-20, evening cycle)

Companion to `ledger-minting-pitfalls-2026-08-20.md` (items 1-5 there;
6-8 here were observed in the same day's later session).

## GENOME gate on kind=build (Pass 9 law, hit live)

`kind='build'` submits are rejected at the write path without a valid
GENOME block in `detail`. The ledger CLI (`gates/task_ledger.py --submit`)
has NO `--detail` flag — mint builds via the Python API:

```python
import sys; sys.path.insert(0, '/<workspace>')
import task_ledger as tl
c = tl.connect()
tid = tl.submit(c, title='...', kind='build', lane='scheduler',
    origin='research:digest:T-...', created_by='hermes', severity=2,
    actor_class='ai-or-human',
    detail='GENOME: body=nervous scientist=the specialist engine '
           'physics="unsupervised anomaly detection" 8d=adaptability')
```

Canonical vocabularies (the gate error message lists both — expect 1-2
rejections while calibrating):
- `body` = BIOLOGICAL system only: circulatory, connective, creative_visual,
  digestive, endocrine, immune, integumentary, lymphatic, memory, metabolic,
  muscular, nervous, network, nucleus, regulatory, reproductive,
  respiratory, sensory, skeletal, urinary. Repo paths like
  `your-stack/conduction` are rejected.
- `8d` for AI tasks: accuracy, adaptability, alignment, coherence,
  consensus, coordination, efficiency, latency, load_balance. Human
  dimensions (environmental, financial...) are for human-actor tasks.

## Never guess source URLs — pull them from the task row

Digest/triage tasks carry their real source URL in the task `detail` (the
minting organ recorded it there). This session: guessing arxiv IDs from
title memory returned REAL BUT WRONG papers — title-adjacent, entirely
different subject — and four triages were nearly written against fabricated
sources. Matching-looking titles are not verification. Protocol:

1. `SELECT detail FROM tasks WHERE id=?`
2. Regex `https?://\S+` out of the detail
3. Verify via `curl -sL https://export.arxiv.org/api/query?id_list=<id>`
   (https + `-L`; plain http 301-redirects and returns empty silently)
4. Only then digest/triage

A triage written against an unverified source is fabrication with extra
steps. If the URL is missing from the detail, park the task honestly
instead of guessing.

## Outcome honesty: no forward-dated claims

An `--outcome` saying "follow-on minted" written BEFORE the mint commits
is a bookkeeping lie if anything blocks the mint — the GENOME gate did
exactly this once, leaving an outcome claiming a follow-on that did not
exist until the mint was retried through the Python API. Order of
operations: mint the follow-on FIRST, capture the returned task ID, then
write the parent outcome naming that ID. Same class as the
fabricated-numbers law: ledger text references only what exists at write
time. (Same session corollary: tasks shipped in git but left `open` in
the ledger, and tasks BUILT+LIVE but closed with empty outcomes, are the
inverse lie — close bookkeeping with evidence: commit hashes, endpoint
curls, DB rows.)
