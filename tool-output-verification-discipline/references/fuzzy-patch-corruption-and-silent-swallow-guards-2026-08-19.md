# Patterns 19-20: fuzzy-patch corruption and the guard that passed by crashing (2026-08-19)

New failure modes for the SKILL.md catalogue (body edit curator-gated
this pass; full detail here, SKILL.md patterns 19-20 pending).

## Pattern 19 — Fuzzy-match patch success corrupting the file

Two live occurrences in one session, both against a 10k-line file:

1. **Anchor matched partially.** The patch tool (fuzzy anchoring)
   reported success, but it had matched a partial region: the NEW block
   was inserted AND the surviving OLD block remained after it as dead
   code — a doubled `return` with the stale verdict logic dangling
   unreachable beneath it. Lint passed. Only a re-read of the modified
   region exposed the duplication.
2. **old_string composed from recall.** A retry wrote the anchor from
   memory and hallucinated text (`_r["title"]. UNKNOWN()`,
   `_2.connect(...)`) that matched nothing — failed loudly. The
   dangerous variant is a hallucination close enough to fuzzily match
   and silently replace the WRONG region.

Rules:
- Never compose `old_string` from recall. `read_file` the exact region
  (offset+limit) first and copy its text verbatim.
- After any code patch: re-read the modified region for duplicated/dead
  blocks, then `python3 -m py_compile`. Tool "success" + lint pass is
  not proof of a clean edit.
- Path typos in the patch `path` argument fail loudly; anchor typos fail
  silently. Treat every anchor as unverified until read back.

## Pattern 20 — A guard that "passes" by crashing (silent-swallow false PASS)

A shared duplicate-guard helper `_dup_guard(conn, title)` accessed
`_r["title"]`. One caller (`/api/research/build`) passed a raw sqlite3
connection with NO `row_factory` set → `TypeError: 'tuple' object is
not subscriptable` → the caller's `except Exception: queued = False`
swallowed it and SKIPPED the insert → endpoint returned 200-ish payload
with no row created.

The probe result looked correct (no duplicate row existed!) for the
wrong reason: the guard crashed, it didn't guard. A later re-probe with
row-level assertions caught that the FIRST insert also never landed.

Rules:
- Verify guards by the STATE CHANGE (row present/absent), never by HTTP
  status or payload alone. 200 + missing row = guard raised into a
  swallow.
- Helpers shared across call sites: positional access (`_r[0]`, not
  `_r["col"]`) or set `row_factory` inside the helper.
- Never wrap a new guard's call site in a broad `except Exception:
  pass`. A guard that dies silently is indistinguishable from one that
  passed.
- Probe BOTH polarities: the thing that must be BLOCKED and the thing
  that must SUCCEED. A broken guard often blocks everything or nothing.
