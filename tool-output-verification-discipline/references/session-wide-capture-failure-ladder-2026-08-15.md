# Session-Wide Tool Output Capture Failure + the Orthogonal Ladder (2026-08-15)

Companion case to SKILL.md items 17 (read_file silent empty) and 12 (never
claim unread verdicts). In this session the failures stacked: this is the
generalized pattern.

## Symptom signature

- `terminal` returned `{"output": "", "exit_code": 0}` for EVERY command —
  even `echo ALIVE`. Commands actually EXECUTED (files landed, gate/router
  side effects were real) — only output capture was down.
- The `terminal()` helper inside `execute_code` showed the same empty capture.
- `read_file` (per item 17) simultaneously reported an existing 4.7KB file as
  `total_lines=0, content=""` while Python `os.path.getsize()` confirmed bytes.
- A delegation summary echo showed a trimmed head/tail with a pointer to an
  on-disk summary file — the file was real and complete.

## Detection probe (one call, run early)

A single `echo` command. Empty output + exit 0 on an echo = capture layer is
down. Do NOT interpret subsequent empty outputs as "the command produced
nothing," and never narrate a verdict you could not read.

## The orthogonal fallback ladder (all proven live this session)

| Need | Broken path | Working path |
|---|---|---|
| Shell command output | `terminal` | `execute_code` with raw `subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=...)` |
| File reads | `read_file` | `execute_code` with `open(path, encoding="utf-8", errors="replace")` |
| Web fetches | `web_search` / `web_extract` | `execute_code` with `urllib.request` (+ `re` tag-strip) |
| Delegation results | inline echo (may be trimmed/corrupted) | read `<agent-home>/cache/delegation/subagent-summary-*.txt` and `delegation/live/<id>/task-0.log` from disk |

## Two dangers unique to this mode

1. **Scripts that run but whose verdict you cannot see.** Gate/router scripts
   executed with real side effects. Re-running them via the fallback path is
   safe and cheap; CLAIMING their verdict without reading it is fabrication
   (pairs with item 16: never narrate beyond what the last tool result shows).
2. **Corrupted dispatch echoes.** The delegate_task result echo can arrive
   garbled (duplicated lines, unrelated session text). The on-disk live
   transcript is the ground truth — read it before declaring a child's output
   dead.

## General rules

- Empty output + success status = one data point, not a conclusion. Probe
  once, then pivot the whole session's read path to the ladder.
- Filesystem state (os.path.getsize, open().read) is the referee when wrapper
  tools disagree — it reads the same bytes any later process will.
- Capture failures can be intermittent and tool-selective: verify each NEW
  tool's first read with a known-content probe before trusting it for
  verdicts.
