# Evidence-Gate Hardening — 10-Brain Panel That Broke Its Own Gate (2026-08-25)

Session: the specialist engine fresh-brain pass → 10-brain panel (Popper, Shannon, Tanenbaum, Shewhart, Bridgman, Scheffer, Lyapunov, Saltzer, Ravine, Nullius) → findings gated LIVE through the specialist engine replay gate. The panel found the gate's own defects mid-run. Final self-QA 9/9 with zero placeholder assertions.

## Defect 1: Absence claims cannot be proven with presence evidence

**What happened:** 7 of 11 blind findings rejected by the gate. Verdict audit showed **5 of the 7 rejections were TRUE findings** — all absence claims ("X is never run", "no process reads Y back", "gonna/gotta missing") filed with presence-style evidence pointers (grep for the pattern). A grep that finds nothing = "not verified" under a presence-only schema, so every true negative claim died as a "hallucination."

**Fix (durable):** every evidence type accepts `"expect_absent": true`, which inverts the verdict:
```python
expect_absent = bool(evidence.get("expect_absent", False))
# per-branch: return (not ok) if expect_absent else ok
```
Replay note says `(absence proven)` when the absence claim holds.

**Law:** an adversarial gate without an absence-proof mode will systematically kill exactly the findings that say "this claimed integration doesn't exist." Write-only telemetry, never-invoked audit paths, and missing readers are all absence claims.

## Defect 2: DANGEROUS wordlist false-positives on language builtins

**What happened:** a legitimate read-only probe `python3 -c "...open('file').read()..."` was rejected as "not read-only-safe" because the wordlist blocks bare `open` (the macOS launcher command).

**Fix (durable, two layers):**
1. Mask python-builtin call syntax before scanning: `probe = re.sub(r"open\(", "OPENPAREN", cmd)` — then scan the masked string. Bare `open <url>` as a command stays blocked.
2. Don't broaden the wordlist; mask the collision class.

## Defect 3: shlex destroys nested quotes in `python3 -c` evidence

**What happened:** `shlex.split()` stripped the inner quotes from `python3 -c "print(open('file')...)"`, so the file path arrived unquoted and python exited 1 (NameError on `your-stack`). The gate then scored a correct probe as "rc=1 not verified."

**Fix (durable):** special-case whole-string argv for code strings:
```python
if cmd.startswith("python3 -c "):
    argv = ["python3", "-c", cmd[len("python3 -c "):]]
else:
    argv = shlex.split(cmd)
```

## Defect 4: remediation nouns mint false tasks (keyword routing)

**What happened:** intake routing treated any occurrence of `fix|repair|resolve|patch` as a BUILD mint. "the quick fix menu at the diner" and "patch notes for version 2" minted defect tasks. AND the same bare words lived in TWO layers (remediation law + BUILD keyword table) — fixing one layer left the false positive alive.

**Fix (durable):** verb-object pattern, applied to EVERY layer that matches:
```python
r"\b(fix|repair|resolve|patch|debug)\s+(the|a|an|my|it|that|this|up)"
```
Regression probes must include noun-usage negatives ("quick fix menu", "patch notes") not just verb positives ("fix the login crash"). Health keywords still outrank remediation ("fix after doctors visit" → 8D-HUMAN).

## Defect 5: placeholder assertions in verification batteries

**What happened:** an earlier "9/9 PASS" battery contained `check("...", lambda: True)` — a literal True logged as PASS. The panel's Nullius seat filed it as a sev-1 finding against the battery itself, correctly.

**Law:** a check that does not execute the thing is not a check. Any `lambda: True`, `assert True`, or count-only verification in a QA battery is a fabrication surface. Every named check must run a real probe.

## Process pattern: gate-attacks-itself (the panel must include the gate)

The 10-brain panel included the specialist engine (the gate's own seat) and the specialist engine (builder's blind spots). Two of twelve findings were aimed at the verification machinery itself — and both were the highest-value findings of the run. **Standing rule: when reviewing a verification/QA system, at least one panel seat must attack the verification system itself, and the verdict audit (checking rejections are RIGHT, not just accepted findings) is mandatory.** A gate that only ever sees agreeable evidence pointers is untested.

## Also verified this session

- Roles derived from ORGANS.json at runtime (registry change auto-propagates; hardcoded brain-name lists go stale the moment a seat is minted).
- Stamp-at-birth: tasks get a collaboration-category stamp when minted; the audit that consumes stamps must itself be wired into a daemon pass or the falsifiability law is violated (write-only telemetry = unverified claim).
- Name-collision discipline extends to fleet SEATS, not just engines: the specialist engine already existed as QA-fleet PM seat (IMM-13.08.01) when a the specialist engine adversarial engine was minted. Resolution: rename the new seat to the teacher — the specialist engine (invented the control chart Deming popularized; lineage-correct, collision-free).
