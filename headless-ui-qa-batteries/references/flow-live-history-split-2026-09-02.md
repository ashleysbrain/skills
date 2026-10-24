# FLOW live/history view split + header law — 2026-09-01/02

## The two principal orders

1. "why are there done items in the flow ledger? this is not efficient.
   done items should be archived in historical records if they are truly
   done... but you must be sure and I don't truyst you rn."
2. "you r headers are also still not fixed... they are just a summary.
   i told you that isn't what i wanted."

## Implementation (verified live)

**API** — `conduction_daemon.py` `/api/flows/tasks` (~line 1800):
```python
_arch = (parse_qs(urlparse(self.path).query).get("archive") or ["0"])[0] in ("1", "true")
_where = ("state IN ('done','cancelled')" if _arch
          else "state IN ('open','claimed','blocked')")
# … WHERE " + _where + " ORDER BY created_at DESC LIMIT ?
```

**Front-end** — `conductor_screen.py`: header `<span id="ft-live-count"></span>
active · done archived, in history · <a …history</a>`; `ftShowArchive(ev)`
toggles FTARCHIVE, refetches with/without `&archive=1`, re-renders, shows
the `#ft-archbanner` (gold, "HISTORY — done and cancelled records
(archived, read-only). back to live work"). Count span re-written on load
AND on toggle (the number must describe what's on screen NOW).

**Pitfall fixed en route:** a patch that moved `lim = int((parse_qs…
.get("limit") or ["300"]))[0])` left a paren mismatch — py_compile is the
pre-deploy gate; the JS side needs `node --check` on the extracted
`<script>` block (regex-extract all script bodies, write to /tmp, check).

## Truly-done receipt audit (the trust leg)

```sql
SELECT e.event, COUNT(*) FROM tasks t JOIN task_events e ON e.task_id=t.id
WHERE t.state='done' AND e.ts > t.done_at GROUP BY e.event;
```
Result: repair|8 minted|8 amend|7 note|5 ceo_note|5 tri-advance|2 corrected|2
claimed|2 verified|1 ts-normalize|1. Reading the details showed taxonomy
migrations ("kind qa->verify…"), future-fit amends, principal directives stamped
as notes — bookkeeping AFTER completion, tasks never reopened. Zero
archived rows lacked a done_at receipt.

## Verification battery (all four legs green)

1. API: live 400 rows states ⊆ {blocked,claimed,open}; archive 400 ⊆
   {cancelled,done}; done-polluting-live count = 0.
2. DOM: `FLOWTASKS.slice(0,4).map(t=>t.state)` = ['open'×4] live, ['done'×4]
   after `ftShowArchive(null)`.
3. Pixel: screenshots of both modes, vision audit — banner present, rows
   clean, no overlap/clipping.
4. Ledger: state/stage counts post-deploy (kickstart conduction-daemon).

Trap from the first pixel pass: the row-state check indexed the wrong
column (lane text, not state cell) and BOTH modes printed identical
columns while the banner toggled — looked like a re-render failure.
Assert on the DATA array (FLOWTASKS) or the exact state cell, never a
column you didn't verify the index of.
