# Security falsification battery — server-side gates (PASS-4, 2026-08-19)

Session: adversarial QA rotation on pipeline_api.py /api/build-queue +
/api/research/build (Writing Studio). PASS-3 (Luria) had claimed hardening;
PASS-4 (Tanenbaum) falsified 3 of its claims live. This file is the reusable
battery structure, not the narrative.

## Battery shape (Python, urllib, token from <agent-home>/.env)

```
P1  auth            : POST each write endpoint WITHOUT token   → expect 401
P2  XSS storage     : POST payload in a free-text field (kind/title) → expect 200 (stored)
P3  dup evasion     : NFC title → 200, then NFD form (unicodedata.normalize("NFD", t))
                      → expect 409; both-200 = guard defeated
P4  gate bypass     : POST the gated item kind through EVERY insert path with no
                      verdict token → expect 422; any 200 = bypass
P5  echo            : GET full body (no [:N] truncation!) → raw payload must be ABSENT
P6  sink (Playwright): inject a raw legacy row straight into the DB, load the real
                      view → payload renders as text, no element, no fire, container
                      offsetWidth > 0
P7  honest path     : scan → queue with server-issued verdict → expect 200
```

## Findings that generalize

1. **Gate on one endpoint ≠ gate on the invariant.** The INSERT census
   (`grep -n "INSERT INTO build_queue"`) is step zero; fire the gated request at
   every path found. Second raw-INSERT path created course items with zero
   novelty verdict.
2. **`.upper()`/`.lower()` normalization is not Unicode-safe.** NFC vs NFD
   confusables (café: precomposed é vs e + U+0301) split one duplicate into two
   rows. Fix: one shared helper — `NFC normalize → casefold() → " ".join(split())`
   — called at every guard site, never re-implemented inline.
3. **Truncated probe reads fabricate evidence.** `.read()[:500]` made the XSS
   echo look absent (payload stored under other rows). Scan the FULL response
   body; also verify with a direct sqlite read of the stored row.
4. **Escape at INSERT ≠ safe.** Legacy rows stored raw before the fix stay armed;
   the renderer must escape too (`_esc()` on every interpolated field), verified
   by injecting a raw row and proving it renders inert.
5. **Free-text fields that reach titles/tags are XSS carriers** even when the
   endpoint looks internal — check what the frontend interpolates into
   innerHTML (`grep -n "innerHTML" *.html` then trace each field back to storage).
6. **Find the DB via the code's constant** (`grep -n "PUB_DB = "`), never by
   filename guess — publications.db existed in two dirs; only
   writing-studio/publications.db held the table.
7. **Purge hygiene**: delete probe rows by prefix, then run a leftover COUNT
   query and print it (expect 0). An uncounted purge is an unverified purge.

## Honest-gap disclosure pattern

Disclose unfixed limits in the report (process-local verdict store, unbounded
dict, opaque 422 when claim text differs from scanned claim). Adversarial passes
that end with "all green, no gaps" are the tell of a shallow pass.
