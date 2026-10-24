# Authwall recovery ladder + burst-pipeline order (referral depth)

Depth for metabolizing walled or semi-walled research referrals (LinkedIn
posts and their outbound artifacts). Governing skill: `operations/
mosaic-ledger-mint-close` (the referral BUILD lane); the research-intake
skill owns corpus classification.

## Resolution ladder (cheapest first, proven under fire)

1. **Short link -> canonical URL**: `curl -s -o /dev/null -w
   '%{redirect_url}' <lnkd.in short>`. Works even when the body is walled.
2. **Meta-tag capture**: fetch the full post URL with a desktop UA; pull
   `og:description` + `<title>` FIRST — public posts serve the complete
   announcement text in those tags. Capture before anything else; a later
   fetch of the same URL can bounce to the signup wall (walls vary between
   fetches of the same URL, so treat the FIRST successful capture as the
   artifact of record).
3. **Outbound `lnkd.in/e...` / fresh `lnkd.in/p...` shorts resolve
   200-without-redirect**: fetch the body, grep for the first
   non-LinkedIn URL (GitHub, project page, arXiv, vercel demo, DOI) — do not
   retry header-based resolution and do not conclude the link is dead.
4. **arXiv / bioRxiv abstracts are open**: `citation_*` meta tags give
   title/authors/DOI; the abstract block needs no auth.
5. **Journal pages behind Cloudflare (403 to curl on the `.full.pdf`)**:
   the DOI usually has a preprint twin — search the exact title on bioRxiv
   and read the abstract there. Cite the journal DOI in the corpus row; the
   preprint is the readable mirror.
6. **Publisher redirect shorteners (`rdcu.be/...`) return HTTP 202 with an
   empty body to every curl UA and stall the automation browser** — that is
   the Springer/Nature bot gate, not a dead link. Resolve by searching the
   open web for article title + first author: the article page is usually
   indexable and the author's own publications page confirms title, venue,
   and DOI. Do not burn attempts cycling UAs against the redirect.
7. **X thread mirror** of the same announcement (`r.jina.ai/https://
   x.com/<user>/status/<id>`) often carries the repo link and the
   multi-tweet technical detail the LinkedIn wall truncates.

Only after ALL rungs fail does the link go to the walled-links ledger.

## Just-released projects (unindexed repos)

An open-source release announced hours ago may not be in GitHub search yet.
Do not guess a lookalike repo (name-collision repos exist for common words —
always read the description before accepting a search hit). Capture the
project site + announcement thread, file the corpus row with a
`repo-when-indexed` follow-up key inside the note, and pull mechanism facts
from the mirror meanwhile. Unindexed is not unavailable.

## Burst pipeline order (binding)

1. Resolve ALL short links first (parallel).
2. Register ALL corpus rows in ONE script (positional tuples, PRAGMA-read
   schema; the insert recipe is references/research-corpus-lineage.md).
3. Gate + mint ALL BUILDs in one loop.
4. ONE bus post with all T-ids — LAST, never interleaved with step 2: a bus
   summary posted ahead of a failed registration reports work that did not
   land. When a registration errors mid-pipeline, finish the INSERT first,
   then post; annotate the late-registration on the minted row.

## Binding-count failure (the classic registration bug)

`Incorrect number of bindings supplied. The current statement uses 9, and
8 supplied` means the VALUES list and the tuple disagree — almost always a
row built as a variable list then indexed with stale positions
(`IndexError: tuple index out of range` is the same bug one step later).
Write the INSERT tuple INLINE in the execute call, literal `1` for
seen_count, and the same `now` for run_at and last_seen_at; re-run the whole
script on failure (the INSERT is atomic — a failed run leaves no partial
rows to double-file).
