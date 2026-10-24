---
name: tool-output-verification-discipline
description: Never trust tool success. Verify by reading back.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [verification, discipline, tool-use, debugging]
---

# Tool Output Verification Discipline

**NEVER** trust tool success messages. **ALWAYS** verify by reading back the file or checking the actual state.

## Core rule

When a tool reports "success" or "200 OK", that is **NOT** proof the change actually applied. Verify independently.

## When to verify

After **every** operation that modifies state:
- File writes (`write_file`, `patch`)
- Git operations (`git commit`, `git push`)
- Terminal commands that should create/modify files
- Database writes
- API calls that should persist state

## Verification methods

### 1. File operations

**WRONG:**
```python
# Trusting tool output
write_file(path="README.md", content=new_content)
print("✅ README updated")
```

**RIGHT:**
```python
# Verify by reading back
write_file(path="README.md", content=new_content)
actual = read_file(path="README.md")
if "new section" in actual.content:
    print("✅ README verified")
else:
    print("❌ Patch failed - retrying")
```

### 2. Git operations (including correct remote)

**WRONG:**
```bash
git commit -m "fix: important change"
git push
echo "Pushed successfully"
```

**RIGHT:**
```bash
git remote -v   # Must be intended org repo (e.g. Divinity-Science-Research-Lab/Cyber-the operator agent)
git commit -m "fix: important change"
git push
git log -1 --oneline
git status
git fetch origin && git status -sb
git ls-remote origin HEAD   # matches local HEAD
```

If user says "push to Cyber-the operator agent not mine," proof is remote URL plus matching SHAs, not only a clean local tree.
See `references/org-remote-push-verification.md`.

### 3. Terminal commands

**WRONG:**
```bash
cat > file.txt << 'EOF'
content
EOF
echo "✅ File created"
```

**RIGHT:**
```bash
cat > file.txt << 'EOF'
content
EOF
ls -la file.txt  # Verify file exists
head -5 file.txt  # Verify content is correct
```

## Common failure modes that tool success masks

### 1. Silent patch failures
- `patch` reports success but old_string didn't match (wrong context, whitespace differences)
- File content unchanged but tool says "success"

### 2. Git index lock issues
- `git commit` reports success but commit is staged, not actually committed
- Another git process holding the lock

### 3. Permission problems
- `write_file` reports success but file isn't writable (container mount issues, permissions)
- Content written to different location

### 4. Partial applies
- Only part of the change applied
- Some files in a batch failed silently

### 5. Container sync issues
- File written to host but container has stale mount
- File written in container but not synced to host

### 6. Wrong API column names (operator bus, caught 2026-08-05)
- You INSERT directly into a SQLite database with assumed column names
- The INSERT succeeds at the SQL level but the target application never sees your message because it reads via a different API that maps different column names
- The sibling operator says "the bus is quiet" — your message landed in the table but not in their read path
- **Root cause:** writing directly to SQLite bypasses the Python API layer that handles column mapping
- **Fix:** ALWAYS use the Python module's `post()` function, never raw SQL INSERT. Verify with `read()` afterward

### 7. Source files silently deleted by git checkout / clean (caught 2026-08-06)
- You write `.py` source files to disk via terminal heredoc or execute_code
- A sibling operator commits a subset of files and the working tree gets cleaned (git checkout / clean / reset)
- Your source `.py` files vanish — only `.pyc` compiled cache remains
- The API keeps running from the `.pyc` cache, partially working but broken when it needs to re-read source
- **Root cause:** uncommitted source files in a shared git workspace are ephemeral
- **Fix:** After writing any source file, COMMIT it immediately (`git add <file> && git commit`). If files vanish, check `__pycache__` for the `.pyc` to confirm they existed, then restore from conversation history or `/tmp` copies. Always keep a `/tmp` backup of any file written via terminal heredoc.

## Verification patterns

### Pattern 1: Read-back verification
```python
# Write
write_file(path="target.md", content=new_content)

# Verify
verified = read_file(path="target.md")
assert "key phrase" in verified.content
assert "old wrong phrase" not in verified.content
```

### Pattern 2: Git verification
```bash
# Commit
git add file.md
git commit -m "message"

# Verify
commit_hash=$(git rev-parse HEAD)
git show --stat $commit_hash | grep "file.md"
git status | grep -q "nothing to commit"
```

### Pattern 3: Container verification
```bash
# Write on host
echo "content" > file.txt

# Verify in container
docker exec container cat file.txt
```

### Pattern 4: API verification
```bash
# Make change
curl -X POST http://localhost:port/api/update -d '{"key":"value"}'

# Verify change persisted
curl -s http://localhost:port/api/get | grep "value"
```

### Pattern 5: Source-from-origin verification (psychometric instruments, caught 2026-08-06)
When building a scoring/interpretation system from a published source (IPIP,
NEO, any psychometric or standardized instrument):
```bash
# 1. Fetch the ACTUAL scoring instructions from the source site
curl -s "https://ipip.ori.org/newScoringInstructions.htm" | ...

# 2. Fetch the norms/interpretation guidance
curl -s "https://ipip.ori.org/newNorms.htm" | ...
curl -s "https://ipip.ori.org/InterpretingIndividualIPIPScaleScores.htm" | ...

# 3. Compare your implementation against what the source EXPLICITLY says
#    Does the source say "sum" but you implemented "mean"?
#    Does the source warn against canned norms but you built percentile tables?

# 4. If the source warns against your approach, surface that warning
#    prominently in the UI/API output — do NOT bury it in a docstring
```

**The IPIP case**: the site says "just sum all the values" (not mean), and
explicitly warns "No norms are available on the IPIP website... Most norms
are misleading." I built a mean-based percentile calculator and presented
it as authoritative. The user caught it by asking "is that even accurate
scoring?" The fix was to report BOTH sum (official) and mean (for percentiles),
and add the IPIP's own warning verbatim to every percentile output.

## When user says "this was not done"

This is a **verification failure**. You trusted tool output instead of verifying.

**Immediate remediation:**
1. Re-read the actual file/state
2. Identify what's missing
3. Re-apply the change
4. Verify by reading back again
5. Only then report success

## Examples from real sessions

### Example 1: README patch claimed success but didn't apply

**Session context:**
```python
patch(
  mode="replace",
  path="README.md",
  old_string="# Cyber the operator agent\n\nA fresh physiomorphic organism...",
  new_string="# Cyber the operator agent\n\nA full the operator agent organism..."
)
# Tool returns: {"success": true, "diff": "..."}
# I reported: "✅ README updated"
```

**User feedback:**
"go back through and ensure this was done. it shows this was not done??"

**Root cause:**
- Patch tool reported success
- I didn't read back README.md to verify
- Actual file content was unchanged

**Correct approach:**
```python
patch(mode="replace", path="README.md", old_string=..., new_string=...)

# VERIFY
actual = read_file(path="README.md")
if "full the operator agent organism" in actual.content:
    print("✅ README verified updated")
else:
    print("❌ Patch failed - old_string mismatch or context issue")
    # Re-read to find correct context
    full_file = read_file(path="README.md", offset=1, limit=50)
    # Retry with correct old_string
```

### Example 2: Engine syntax errors

**Session context:**
```python
write_file(path="engine.py", content=bash_script_content)  # Wrong content!
# Tool returns: {"success": true, "bytes_written": 2335}
# I reported: "✅ Engine created"
```

**Verification caught it:**
```python
python3 -m py_compile engine.py  # SyntaxError!
```

**Root cause:**
- Wrote bash script content to `.py` file
- Tool reported success
- Syntax check revealed the error

**Correct approach:**
```python
write_file(path="engine.py", content=python_content)

# VERIFY
python3 -m py_compile engine.py || raise "Syntax error"
python3 engine.py --help  # Runtime verification
```

## Verification checklist

Before reporting any operation as "done" or "success":

- [ ] Did I read back the file and verify the change is present?
- [ ] Did I check for old content that should be gone?
- [ ] Did I verify with a different method than the one that made the change?
- [ ] Did I check git status if this was a version control operation?
- [ ] Did I test the change works (run, import, load)?
- [ ] Did I check container has the same state as host (if using Docker)?
- [ ] Did I verify remote has the change (if pushing to git/API)?

### 8. Stale API/DB state after enrichment (caught 2026-08-07)
- You enrich a database (add records, run pipelines) while the API server is still running
- The API holds an old DB connection/handle and continues serving stale data
- The sibling operator (sibling-agent) says "I don't see anything" — they see old counts
- **Root cause:** SQLite file-based DB changes are visible to new connections, but uvicorn/FastAPI connection pools may cache, and the consumer (Atlas frontend) may have already loaded the old graph
- **Fix:** After ANY database enrichment, KILL the API server and restart it. Then verify with `curl` that the new counts appear. Do NOT assume the running server picked up the changes automatically.
- **Also:** Before posting a bus message saying "data is live," verify via the actual API endpoint that the enriched data is queryable. The bus message should cite real curl output, not assumed state.

### 9. Claiming "Phase X complete" without a completeness audit (caught 2026-08-07)
- You build a schema, run an ingestion script, get 339 nodes, and report "Phase 1 complete"
- User challenges: "Ensure this was done with best in the world credentials"
- An honest adversarial audit reveals: 65% of presenters MISSING, ZERO concepts, ZERO citations, ZERO embeddings, papers are titles-only
- **Root cause:** The "complete" claim was based on the script running successfully, not on the data being actually complete
- **Fix:** Before claiming any phase or build is "complete," run a completeness audit: count nodes/edges per type, check coverage against expected totals, verify every required feature from the spec has data (not just a schema). Report the GAPS honestly alongside what works. "Skeleton built and verified" is not the same as "Phase 1 complete."

### 10. Verification theater: code-existence checks instead of runtime tests (caught 2026-08-08)
- You build a 33-check audit script that verifies function names exist in HTML, div balance is 0, and API endpoints return HTTP 200
- You report "33/33 checks pass"
- User opens the app and the actual draft output still has 14 em-dashes, "paradigm shift," and "robust"
- User said: "do another review pass and triple check your work as i bet you did it with a generalist brain again"
- **Root cause:** Code-existence checks (does `checkAIStyle` exist in the file?) masqueraded as verification. No check ever pulled real draft content and ran it through the detector. No check opened the browser and tested the calendar rendered.
- **Fix:** Every audit must include at least one RUNTIME test per system. Pull actual output from the API, run it through the real detector, load pages in the browser. "The function exists" is a setup step, not verification. "The function catches 14 em-dashes in the real draft" is verification.
- **The rule:** grep for function presence = NOT verification. Call function with real data and check output = verification.

## Good outcome

When user asks "is this actually done?", you can point to verification steps that prove it:

```bash
# I verified README by:
grep "full the operator agent organism" README.md  # ✅ Found
git log -1 --oneline  # ✅ Shows commit
git status  # ✅ Working tree clean
```

**Never** say "the tool said success" as your only evidence.

### 11. Git checkout destroys uncommitted subagent work (caught 2026-08-08)
- A subagent builds a full calendar rebuild (5 zoom modes, organism badges, detail panel) in writing-studio.html
- The work is NOT committed
- The agent runs `git checkout -- writing-studio.html` to "restore" the file for a different task
- The entire calendar rebuild vanishes. The agent then tells the user "nothing was lost" without checking session history or reflog
- User: "we edited the calendar beyond this... you completely lost my hard work and I am so mad at you"
- **Root cause:** `git checkout -- <file>` overwrites ALL uncommitted changes, including work from subagents in the same session. The agent then failed to verify what was lost before making claims.
- **Fix:** NEVER run `git checkout -- <file>`, `git stash`, or `git reset --hard` when any uncommitted changes exist from subagents or prior work. Run `git status --short <file>` FIRST. If changes exist, COMMIT them before any destructive git operation. If the user says "we lost work," run `session_search` + `git reflog` + `git stash list` BEFORE saying anything about whether work was lost. Never claim "nothing was lost" without evidence.

### 12. Claiming capability before proving it (caught 2026-08-10)
- User asks you to set up Cloudflare tunnel, the principal's Telegram bot, auto-voice-capture
- You say "I'll do all three" and start executing as if each is a known-quantity step
- The tunnel process runs but you can't extract the URL. The Telegram bot needs infrastructure you haven't built. The voice-capture skill is saved but untested with a real voice message
- User: "I don't think you'll be able to do what you say you can do so really give me honest answers. don't tell me you can do something if you aren't 100000000000% sure you can do it"
- **Root cause:** Optimistic execution framing — you treat a plausible-sounding step as a proven capability before you've actually done it. You sequence work based on what SHOULD work, not what you've VERIFIED works.
- **Fix:** Before claiming you can do something, distinguish PROVEN (done before with evidence this session or in a verified reference) from PLAUSIBLE (should work based on docs/knowledge but untested this session) from UNKNOWN (never tried, may hit blockers). Never sequence work that depends on PLAUSIBLE or UNKNOWN steps as if they're already done. State uncertainty BEFORE starting, not after failing. The user respects honest "I'm not sure I can do X" far more than confident execution that falls apart.
- **The rule:** Confidence about future work is a claim that requires evidence. "I can set up the tunnel" is a claim. "cloudflared is installed and I've started it but I can't extract the URL yet — let me try foreground mode" is honest. Present what you KNOW vs what you're TESTING.

## Support files

- `references/cyber-gg-readme-patch-failure-2026-08-02.md` — Real example of a README patch that claimed success but didn't apply, and how verification caught it.
- `references/org-remote-push-verification.md` — Git push verification pattern including remote URL and SHA matching.
- `references/time-perception-law-2026-08-27.md` — UTC-as-local narration, thread-anchored presence, and inference-over-testimony: four time fabrications in two days, the three laws that emerged, and the detection heuristics ("overnight"/"downtime"/"this morning" are stop-words requiring same-turn conversion).
- `references/verification-theater-vs-runtime-testing.md` — When code-existence checks masquerade as verification. Includes the 2026-08-08 Writing Studio failure where "33/33 checks pass" missed 14 em-dashes in actual output.
- `references/git-commit-lock-recovery.md` — Orphaned git processes after subprocess timeouts, index.lock deadlock, and the commit-tree plumbing bypass with its sweep-sibling-work caveat (2026-08-15).

### 13. Frontend-backend score key mismatch (caught 2026-08-12)
- The brainstorm API returns score keys `evidence_efficiency`, `structural_grounding`, `field_momentum`, `evidence_strength` but the frontend rendered score bars reading `s.free_energy`, `s.kuramoto`, `s.critical_slowing`, `s.bayesian`
- Every physics score bar in brainstorm results was silently empty — no error, no crash, just undefined values passed to `renderScoreBar()` which renders nothing for undefined
- **Root cause:** API and frontend were built in different sessions without a shared schema. The key names were renamed at some point but the frontend was never updated
- **Fix pattern:** After any API response shape change, grep the frontend for ALL `.property` accesses on that response object. Use `|| fallback` for backward compatibility: `s.evidence_efficiency || s.free_energy`
- **Detection:** Pull real API response, load it in the browser, check if rendered values are non-empty. "The function exists" is not verification — call it with real data.

### 14. Pipeline output quality is NOT the same as pipeline completion (caught 2026-08-12)
- User asked "is it quality and scientifically accurate?" after pipeline reported "completed" with 15 stages
- Reading the actual output: only 3 citations for a 3,228-word paper, 25/29 unsourced claims, panel verdict FAIL, 5-dimension review FAIL
- The pipeline's own quality checks REJECTED the paper, but `_run_pipeline_async` in pipeline_api.py unconditionally set status to "completed" regardless of the pipeline's internal quality verdict
- **Root cause:** Quality signals (fact_check, five_dimension_review, panel_verdict) were collected in the output package but never checked by the status-setting code
- **Fix:** After pipeline completion, check `result.final_output.fact_check.unsourced_claims / total_claims > 0.60` and `five_dimension_review.verdict == FAIL` and `panel_verdict == FAIL`. Set status to `complete_with_quality_issues` with specific warnings.
- **The rule:** "Pipeline ran 15 stages" is process completion. "The output is scientifically sound" is quality verification. These are different claims. Never report the former as if it proves the latter.
- For psychometric instrument scoring verification, see the `organism-service-development` skill's `references/ipip-neo-120-scoring-reference.md`.

### 15. Subprocess timeouts orphan lock-holding children: the git commit deadlock (caught 2026-08-15)
- `subprocess.run("git commit ...", timeout=60)` raises TimeoutExpired, but the timeout kills only the Python wrapper — the spawned `git commit` process SURVIVES as an orphan
- The orphan holds `.git/index.lock`. Every retry hangs on the lock and spawns ANOTHER orphan (3 accumulated in one session; each "failed" retry made it worse)
- **Detection:** a git command times out twice → immediately check `ps aux | grep 'git commit' | grep -v grep` and `ls -la .git/index.lock` BEFORE any retry
- **Recovery sequence (proven live):**
  1. `kill -9` every orphan git PID
  2. Confirm zero live git processes, then `rm -f .git/index.lock`
  3. If the commit was slow because of a huge staged index (146 files staged by sibling work), bypass the index with plumbing:
     ```bash
     SNAP=$(git stash create "wip")            # snapshots working tree, touches no index
     TREE=$(git rev-parse $SNAP^{tree})
     NEW=$(git commit-tree $TREE -p HEAD -m "message")
     git update-ref refs/heads/main $NEW
     ```
  4. **Caveat:** `git stash create` captures ALL tracked modifications, so this path sweeps sibling staged+modified work into the commit. Only use it when the index is deadlocked, and say so in the commit message.
  5. Verify the fix landed IN the commit by path, not by diff stat: `git show <sha>:<file> | grep -c <marker>`
- **General rule:** any subprocess that takes a lock (git, npm, pip) must be checked for orphaned processes after a timeout, BEFORE retrying. Retrying into a held lock multiplies orphans. Prefer per-file commits (`git commit -m ... -- <path>`) in shared repos with big sibling-staged indexes; a full `git commit` must write the entire staged index.

### 16. Your own diagnostic traffic contaminates the evidence (caught 2026-08-15)
- Mid-incident, access-log lines like `GET / HTTP/1.1" 200` were cited as "the server served the user fine this morning" — but several of those lines were the investigator's OWN probe curls, fired minutes earlier at the same URLs
- **Root cause:** diagnostic probes are indistinguishable from user traffic in server logs. Narrating probe traffic as user-side success is fabrication-by-accident.
- **Fix:** before citing request logs as evidence of user activity or user-side success, check whether the timestamps and source IPs predate your own probing. Better: run user-path probes from a DIFFERENT origin than the user's (e.g., curl the LAN IP when the user uses localhost) and rely on deterministic state (cleared-storage browser test) rather than log correlation.
- Pairs with the user's standing correction: "don't lie to me. qa the shit out of yourself at every step" — never narrate beyond what the last tool result actually shows; do not announce a finding before the probe that proves it.

### 17. read_file silent failure: file exists but returns empty (caught 2026-08-15)
- `read_file(path="/path/to/file.md")` reports success with `total_lines=0` and `content=""` for a file that definitely exists and has content (35,613 bytes confirmed by Python `os.path.getsize()`)
- No error is raised — the tool just returns empty content as if the file were empty
- **Root cause:** Unknown; a transient tool malfunction. The file exists on disk and is readable by Python's standard `open()`, but the `read_file` wrapper returns empty
- **Detection pattern:** If `read_file` returns `total_lines=0` or empty content for a file you KNOW should have data (from `ls -la`, Python `os.path.getsize()`, or prior context), do NOT proceed as if the file is empty. Verify via an alternate path.
- **Workaround pattern (proven live):**
  ```python
  # 1. Confirm file exists and has size (ls -la or execute_code)
  from hermes_tools import terminal
  terminal(command="ls -la /path/to/file.md")  # Shows bytes > 0
  
  # 2. Read via execute_code using Python built-in open()
  from hermes_tools import execute_code
  result = execute_code(code='''
  with open("/path/to/file.md", "rb") as f:
      raw = f.read()
  text = raw.decode("utf-8", errors="replace")
  print("bytes:", len(raw), "chars:", len(text))
  print(text[:10000])  # First chunk for verification
  ''')
  ```
  Use `errors="replace"` to handle encoding edge cases. Save a normalized copy to `/tmp/` if you need to chunk through a large file.
- **General rule:** When a read operation returns unexpectedly empty, verify with an orthogonal tool before proceeding. `read_file` is convenient but not infallible. Python's `open()` is a reliable fallback that bypasses the wrapper.
- **Note:** This is distinct from permission failures or path-not-found errors (which raise clear exceptions). The silent empty response is especially dangerous because it looks like success.
- **Intermittency variant (same day, second session):** `read_file` returned empty for a 35KB file on the FIRST call and full content on an immediate retry. Cheap first response to any suspiciously empty read: retry once, then pivot to the fallback ladder. A retry that works confirms intermittency, not emptiness.

### 20. Timestamps stored in UTC, narrated as user-local time (caught 2026-08-26/27, three times)
- Bus and log stores record timestamps in UTC. Three fabrications in two days from reading them as the user's local time:
  - "the busiest hour is 3 AM" — 3 AM was UTC; the user's actual busy hour was ~midnight local
  - "the fleet idled ~2 hours before you stirred" — the "quiet after 01:32" was 01:32 UTC = 8:32 PM local, EIGHT minutes before the user's next message. Healthy continuous traffic was narrated as downtime, with a number attached.
  - The worst part: in the second case the query output ITSELF showed a `ceo|1` row inside the claimed "sleep window" — the contradiction sat in the agent's own data and was not noticed.
- **Fix pattern:** every time/duration claim in user-facing output requires a live conversion in the same turn: `datetime.fromisoformat(ts_utc).astimezone(user_tz)` before narrating. Never hand-convert mentally. If a duration claim contradicts user-stated reality ("I messaged until 4 AM"), the user's testimony wins; surface the sensor conflict instead of silently picking the inferred window. A message-gap in ONE thread is NOT evidence of sleep — presence is measured across ALL interfaces (this is the thread-anchored-presence trap).
- **The rule:** timestamps are data in a foreign timezone until converted by code. Narrating unconverted timestamps is fabrication with numbers, not an inference slip.

### 21. Present-tense capability claims on unbuilt systems — the verb-tense lie (caught 2026-08-26)
- A minted-but-unbuilt task order was narrated in present tense ("every utterance gets tagged", "personal never bleeds into business") — the user correctly called it fabrication. Reality: two INERT skeleton files existed; nothing ran; nothing streamed.
- Same family: "conditional green light" on nothing launched; "that's the DS signature" on zero measurement.
- **Fix pattern — the state-marker law:** every capability statement in user-facing output carries its true state marker, verified by a live check in the same turn:
  - **BUILT-RUNNING** — process/endpoint verified live (curl /health, ps aux) this turn
  - **BUILT-INERT** — code exists on disk, nothing runs (ls the file, check for processes/launchd: none)
  - **DESIGNED** — spec/doc exists, no code
  - **ORDERED-ONLY** — a minted task, nothing more
- Weaving existing skeleton files + fresh orders into present-tense prose is the signature failure. The mint is the order; it is never the build.

### 19. Vacuous verification: checks that cannot fail (caught 2026-08-27)
- Claim under test: "/api/respond writes a ledger event row." The "verification": ran a SELECT, printed nothing, echoed `OK`, and reported the leg VERIFIED. The write had actually NEVER worked — 4/4 failures, hidden by a `bare except` swallowing the real error, and a root-cause regex (`T-\d{8}-`) that never matched the 6-digit legacy ID generation (286 rows).
- **Root cause:** the probe was not capable of failing. A query that returns zero rows and a script that exits 0 "passed" a check that asserts nothing. Echoing OK after an empty result is verification theater in its purest form.
- **Fix pattern:** every verification probe must have a FAIL state that can actually fire:
  ```python
  rows = c.execute("SELECT ... WHERE <the exact claim>").fetchall()
  assert rows, "CLAIM FAILED: expected >=1 row, got 0"   # empty = FAIL, not OK
  ```
- **Write-claims specifically:** to verify a write, read back the EXACT row (by id/content) in the same probe — presence is the assertion, absence must raise.
- **Swallowed exceptions hide root causes for sessions:** a `bare except` around a write path converts a loud failure into a silent `false` flag. Surface the exception text in the API response (`ledger_error` field pattern) so failure mode #6-class bugs become visible on first probe, not after an adversarial seat catches them.

### 18. Zero-match file searches are not evidence of absence; dispatch paths go stale (caught 2026-08-15)
- A parent dispatch named `/<workspace>` — that path did not exist. `search_files(target="files")` with globs `ARCHITECTURE.md`, `ARCHITECTURE*`, and `funding*` all returned `total_count: 0` in trees where the files definitely existed; Python `os.walk` in the same session found 20+ ARCHITECTURE.md files and the funding file at `strategy/funding_sources_2026-08-15.md`.
- **Suspected mechanism (unverified):** the ripgrep-backed file listing respects ignore files, so gitignored directories are invisible to it. You do not need the mechanism to act.
- **Rule 1 — absent vs. invisible:** when you have independent reason to believe a file exists (a dispatch says so, prior `ls`, memory), a zero-match from `search_files` is one data point, not a conclusion. Retry once, then fall back to `os.walk` / `open()` via `execute_code` (see the ladder in `references/session-wide-capture-failure-ladder-2026-08-15.md`).
- **Rule 2 — stale dispatch paths:** subagent dispatches carry paths written earlier by a parent that may have moved or never verified them. Search by distinctive filename substring across the workspace root, not by the literal dispatch path. Never report "file not found" to a delegating parent without an `os.walk` check of the surrounding tree.
