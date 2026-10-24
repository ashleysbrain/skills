# Credential Inference Poisoning

## Incident Summary

| Field | Value |
|-------|-------|
| **Wrong data** | User name recorded as "the principal Wilson" |
| **Correct data** | User name is **Aisha** |
| **Source of poison** | `principal.williams@divinityscience.com` in gcloud credential path |
| **Duration** | March 2026 through July 10, 2026 (~4 months) |
| **Corrections ignored** | Multiple sessions where user said "my name is not the principal" |
| **Root cause** | A session inferred identity from infrastructure credentials and wrote it to USER.md without verification |

## How It Happened

1. **March 25, 2026** — A session needed gcloud authentication. Found credentials at `/<workspace>@divinityscience.com/adc.json`. The agent assumed "principal.williams" was the user's real name.

2. **The inference was baked into USER.md** as "the principal Wilson. Inventor of Physiomorphic AI..." — a confident, declarative identity entry.

3. **For four months**, every session that read USER.md saw "the principal Wilson" as the user's name. The name appeared in cron jobs, email signatures, agent profiles, standup briefs, and health reports.

4. **User corrected it multiple times.** Each time, the correction was treated as a one-off fix rather than a root-cause investigation. The wrong name kept coming back because:
   - The audit methodology had no step to verify identity facts
   - Session corrections didn't trigger a USER.md audit
   - The entry was confidently written, so it looked authoritative

## Evidence That Was Always Available (But Never Checked)

| Evidence | Points To |
|----------|-----------|
| `~/your-workspace/` — primary workspace directory | Name is Aisha |
| `AISHA-MD` — personal health agent named after the user | Name is Aisha |
| `aisha` — username/handle in multiple system paths | Name is Aisha |
| Session history with explicit corrections | Name is NOT the principal |

## General Pattern

Credential inference poisoning happens when:

1. An agent encounters an email, username, or account name in infrastructure
2. It assumes that name is the user's personal identity
3. It writes the inference to a high-trust memory slot (USER.md)
4. The entry looks authoritative (declarative, confident) so future agents treat it as verified
5. The user corrects it, but the correction doesn't propagate because:
   - No audit step checks identity against environment
   - The correction is handled as a memory swap, not a root-cause investigation

## Prevention Rules

1. **Infrastructure credentials are NEVER identity evidence.** Email accounts, git configs, API keys, and service accounts reflect whoever set them up, not who the user is.

2. **Identity facts require environmental cross-check.** Before writing a name, role, or company to USER.md, verify against:
   - Workspace directory names
   - Agent/health system names
   - Session history corrections
   - The user's own words in conversation

3. **Corrections trigger audits.** When a user says "my name is not X" or "stop calling me Y", that is not just a memory swap — it triggers an identity fact verification (Step 2.6 of the audit methodology).

4. **Search before assuming.** Before accepting any identity fact from a credential path, run `session_search` for corrections: `"my name is not"` / `"stop calling me"` / `"it's not"`.

## Resolution

On July 10, 2026, the wrong name was finally scrubbed from both USER.md and MEMORY.md. The correct name (Aisha) was confirmed from workspace evidence and locked in. This reference file exists to prevent recurrence.
