# Pending SKILL.md Body Items (curator read-tracker blocked the patches)

Session 2026-08-18 produced four SKILL.md body edits that could not be
applied: the background curator's patch path refused with
"current SKILL.md content has not been loaded in this review turn"
despite a fresh skill_view load (3 argument variants, identical refusal;
write_file path worked). Foreground session or `hermes curator` should
apply these to software-development/your-stack-operations/SKILL.md,
then delete the duplicated lines from this file.

## 1. Trigger section — canonical path
Replace:
  Trigger: "Run the OS", "the OS methodology", "the OS", or ANY work
  inside the package at `~/your-org/your-stack/`.
With:
  Trigger: "Run the OS", "the OS methodology", "the OS", or ANY work
  inside the package. Canonical home: `~/your-org/your-stack/`
  (org repo; relocated 2026-08-18, task T-0136). The old
  `~/your-org/your-stack/` path is a dead stub — never
  work there.

## 2. CI discipline section — macOS timeout pitfall
Append:
  macOS pitfall: there is NO GNU `timeout` binary on this machine.
  Wrapping gate selftests in `timeout 60 …` fails every gate spuriously
  (observed 19/19 FAIL with zero real defects, then 19/19 PASS bare).
  Run gates bare: `python3 gates/<gate>.py --selftest`.

## 3. Standing directives section — per-person protection
Append:
  - Per-person protection directives live in `stores/people.json` as
    `standing_directives` on the member's P-* entry — data, not code.
    Precedent 2026-08-18 (a teammate, P-NANDITA): "Contributions IMMUTABLE:
    additive/surgical edits only, never delete or overwrite her work".
    Mint the person id at directive time, never defer to chat memory.

## 4. References section — pointer to new reference
Append:
  - `references/notion-team-ingest-2026-08-18.md` — prerequisites for
    ingesting team input from Notion into the ledger: integration
    share-wall mechanics, ntn CLI quirks, page-ID recovery without API
    access, MCP token wiring, unlock-watcher pattern, and the
    where-fix-is-performed vs whose-action-it-is framing law.

(That reference file itself WAS written successfully — no duplication
needed here, only the pointer line above.)
