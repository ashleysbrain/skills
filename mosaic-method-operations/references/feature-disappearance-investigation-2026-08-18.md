# Feature-Disappearance Investigation — "what happened to X???" (2026-08-18)

The principal asked "what happened to brainstorming??? mosaic os". Five tool
turns of hunting later the answer was: **nothing happened to it — I was
grepping the wrong workspace.** The trap and the recipe, so the next
session answers in one turn.

## The trap (three stacked)

1. **Cross-workspace split.** The your-stack package (laws, gates,
   ledger, audit records at `~/your-org/your-stack/`)
   references studio runtime code BY NAME in its run-records, but the
   code itself lives in `~/your-workspace/` (`pipeline_api.py`,
   `writing-studio.html`, `writing-studio/*.db`). Grepping only the
   package repo returns ZERO hits → reads as "feature deleted".
2. **Audit-trust inversion.** The run-record claimed "WORKBENCH BUILT ...
   8 routes ... E2E 10/10 green" — and it was TRUE, but only findable
   elsewhere. Run-records are pointers, not locations. Never conclude
   "gone" from a grep of one repo when the claim's artifact lives in a
   sibling workspace.
3. **Nav-tab assumption.** The feature was never a left-nav tab — it is
   the Compose section, reachable via the dashboard's primary CTA
   ("Brainstorm" button) and 11 other `switchView('compose')` entry
   points. Before calling a feature hidden/missing, enumerate ALL entry
   points, not just the nav rail. Verify against a pre-change backup
   (`writing-studio-backups/ws-good-*.html`) to distinguish "cut by a
   subtractive pass" from "never was a tab".

## The recipe (answers "what happened to X" in ~3 turns)

1. **Grep BOTH workspaces first**, scope by kind, before any conclusion:
   `grep -rl "X" ~/your-org/your-stack ~/your-workspace \
     --include="*.py" --include="*.js" --include="*.html" | grep -v node_modules`
   (scoped: `*.py` = backend routes, `*.html` = UI surface). A find
   across home times out — stay in the two known roots.
2. **Is the server live?** `lsof -nP -iTCP:port -sTCP:LISTEN` → PID →
   `ps -p <PID> -o lstart=,command=`. Compare process start time vs
   code mtime (`stat -f "%Sm %N"`) — server older than code means a
   stale process may be serving old routes (restart before judging).
3. **Probe the live API, authenticated.** Token lives in
   `~/your-workspace/.env` as `WRITING_STUDIO_TOKEN`; pass as query
   param: `curl "http://localhost:port/api/X?token=$TOK"`. 401
   {"detail":"Unauthorized"} = auth needed, NOT missing route. 404
   {"detail":"Not Found"} = route truly absent — but check route NAMES
   first (guessing route paths wastes a turn; list them:
   `grep -n '@app\.\(post\|get\|put\|delete\)("/api/X' pipeline_api.py`).
4. **Check the DB directly** (server restart wipes nothing, but zero
   rows in one DB ≠ zero data — tables were consolidated):
   `sqlite3 writing-studio/drafts.db "SELECT ... FROM brainstorms"` —
   the brainstorm tables (brainstorms, brainstorm_links, angle_evidence,
   angle_threads) all live in drafts.db since bus-1978 consolidation.
5. **Answer has three parts**: (a) current live state with evidence,
   (b) what looks-like-disappearance actually was (design choice /
   planned absorption / wrong workspace), (c) the plan if one exists
   (here: Thinkery LOCK-2/LOCK-4, T-0153, PLAN ONLY status).

## Generic lesson

"Feature X disappeared" is a location question, not a status question.
Resolve location first (which workspace, which process, which DB), then
status. The plan docs (DISTRIBUTION-AND-EVOLUTION-SPEC.md,
THINKERY-DESIGN-REVIEW-v2.md) tell you what is SUPPOSED to happen to a
feature — check them before answering, because "it's queued to be
absorbed by Thinkery" was the real answer to "what happened".

## Session evidence (2026-08-18)

- Server: PID 59501, port 8310, `pipeline_api.py --port 8310` (hermes venv).
- 23 brainstorm routes live; 2 saved sessions in drafts.db
  (bs-85703d72-2 "B2BU organism writing-style memory" starred;
  bs-e88436d3-f QA probe); 2 links (builds_on + reference pair).
- Compose view at writing-studio.html:1899; nav rail never had a
  compose tab (verified against ws-good-20260818-092142.html backup).
- Thinkery plan (T-0153): LOCK-2 compose → thinkery seed box; LOCK-4
  research = brainstorm unity. PLAN ONLY, zero code.
