# Manifest Reconciliation Commands

Concrete commands for the manifest integrity scan described in §5 of the engine skill.

## Extract inline references from SKILL.md

**the operator agent-native (preferred — works on all platforms):**
```
search_files(target='content', path='SKILL.md', pattern='`(references|templates|scripts|attachments)/[^`]+`', output_mode='content')
```
Then extract paths from the match output. This avoids shell-compatibility issues entirely.

**Linux (GNU grep):**
```bash
grep -oP '(?<=`)(references|templates|scripts|attachments)/[^`]+(?=`)' SKILL.md | sort -u
```

**macOS (BSD grep — no `-P` flag):**
```bash
grep -oE '`(references|templates|scripts|attachments)/[^`]+`' SKILL.md | sed 's/^`//;s/`$//' | sort -u
```
Or use `egrep -o` with a simpler pattern. The key difference: BSD grep lacks Perl lookbehind (`(?<=`)`), so capture the backticks in the match and strip them with `sed`.

> **Pitfall:** Do NOT use `grep -oP` on macOS — it will fail with `invalid option -- P`. This is the most common cross-platform breakage in manifest reconciliation commands. The `search_files` tool is the safest default inside the operator agent.

## List files on disk per directory

```bash
for dir in references templates scripts attachments; do
  if [ -d "$dir" ]; then
    echo "=== $dir ==="
    ls "$dir/" | sort
  fi
done
```

## Diff manifest vs. disk

**the operator agent-native (preferred):** Use `search_files` to extract inline paths (see above), then compare against `terminal` ls output. No shell portability issues.

**Linux (GNU grep):**
```bash
MANIFEST=$(grep -oP '(?<=`)(references|templates|scripts|attachments)/[^`]+(?=`)' SKILL.md | sort -u)
ON_DISK=$(for dir in references templates scripts attachments; do [ -d "$dir" ] && ls "$dir/" | sed "s|^|$dir/|"; done | sort)

# Unlisted files (on disk but not in manifest):
comm -23 <(echo "$ON_DISK") <(echo "$MANIFEST")

# Dead links (in manifest but not on disk):
comm -13 <(echo "$ON_DISK") <(echo "$MANIFEST")
```

**macOS:** Replace the `grep -oP` line with the BSD grep pattern from the extraction section above. The rest of the pipeline (`comm`, process substitution) works identically on macOS bash/zsh.

## Count references per skill (R13 threshold)

```bash
# Count reference files for a skill:
ls references/ 2>/dev/null | wc -l

# Flag skills exceeding the 15-file threshold:
for skill_dir in skills-library/*/*/; do
  count=$(ls "$skill_dir/references/" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$count" -gt 15 ]; then
    echo "$count $skill_dir"
  fi
done | sort -rn
```

## Batch manifest check across all skills

```bash
for skill_dir in skills-library/*/*/; do
  skill_name=$(basename "$skill_dir")
  manifest=$(grep -oP '(?<=`)(references|templates|scripts|attachments)/[^`]+(?=`)' "$skill_dir/SKILL.md" 2>/dev/null | sort -u)
  on_disk=$(for dir in references templates scripts attachments; do [ -d "$skill_dir/$dir" ] && ls "$skill_dir/$dir/" | sed "s|^|$dir/|"; done | sort)
  
  unlisted=$(comm -23 <(echo "$on_disk") <(echo "$manifest") | head -5)
  dead=$(comm -13 <(echo "$on_disk") <(echo "$manifest") | head -5)
  
  if [ -n "$unlisted" ] || [ -n "$dead" ]; then
    echo "=== $skill_name ==="
    [ -n "$unlisted" ] && echo "  UNLISTED: $unlisted"
    [ -n "$dead" ] && echo "  DEAD LINKS: $dead"
  fi
done
```

## Three-Way Inconsistency: Manifest + Body Citation + Missing File

When a dead manifest entry is found (file listed in the manifest bullet list but not on disk), the same filename is frequently cited **inline in the SKILL.md body text** too. Removing only the manifest entry leaves a dead body citation pointing nowhere.

**Detection:** Before fixing a dead manifest entry, grep the SKILL.md body for the filename (without the `references/` prefix) to find all citations:
```bash
# Find all body-text citations of a dead-referenced file:
grep -n '<filename-stem>' SKILL.md
```

**Dual-fix workflow (mandatory):**
1. Remove the manifest bullet entry.
2. Redirect every body-text citation to an existing reference that covers the same topic (or remove the citation if no equivalent exists).
3. Bump the version field (patch bump for manifest corrections).
4. Run post-patch verification (see `scripts/verify-patch-manifest.sh`).

**Observed instance (2026-07-06):** `8d-pattern-awareness` v1.1.7 listed `references/report-header-box-coverage-and-editable-rebuild.md` in the manifest (line 37) AND cited it in body text (line 203), but the file did not exist on disk. Fixed by removing the manifest entry and redirecting the body citation to the existing `references/report-editing-constraints.md`. Bumped to v1.1.8.

## Redundant Section Detection (intra-document duplicate listings)

Some skills accumulate multiple sections that list the same support files — e.g., a "Manifest" section near the top AND a "References" section at the bottom with identical file lists. This is structural bloat, not dead links: the files exist on both sides, but the redundancy inflates SKILL.md length and confuses the agent about which section is canonical.

**Detection (the operator agent-native):**
```
# Extract all bullet-listed file paths from SKILL.md:
search_files(target='content', path='SKILL.md', pattern='^\\s*-\\s*`(references|templates|scripts|attachments)/[^`]+`', output_mode='content')
```
If the same file path appears in two distinct sections (e.g., lines 28–50 "Manifest" and lines 232–244 "References"), flag as a consolidation candidate. The fix is to collapse the duplicate section into a single pointer ("See the Manifest section above") and update the version.

**Observed instance (2026-06-29):** `8d-snapshot-report` v1.0.13 had a 13-file "References" section that was a verbatim duplicate of the 13-file "Manifest" section. Patched to a two-line pointer; bumped to v1.0.14.

**Fix pattern:** Keep one canonical listing (prefer "Manifest" as the section name). Replace the duplicate with a one-liner: `See the **Manifest** section above for the complete file listing.` If a "Reference Bundle" section provides curated descriptions, that stays — only remove the raw file list duplication.

## Tool-Usage Pitfall: `search_files` vs `ls` for Directory Listing

**Pitfall:** `search_files(target='files', pattern='.')` can return 0 results for directories that clearly contain files. This was observed on macOS when scanning skill reference directories — `search_files` returned `total_count: 0` while `ls` in the same directory listed 21 files.

**Cause:** The `search_files` glob engine may not match dotfile-free directories correctly with a bare `.` pattern, or there may be permission/visibility differences between the search index and the filesystem.

**Rule:** When verifying manifest contents (listing files on disk for comparison against SKILL.md), always use `ls` via `terminal` — never rely on `search_files(target='files')` for directory enumeration. Use `search_files(target='content')` only for extracting inline paths from SKILL.md text.

## Notes

- **The `-oP` flag uses Perl-compatible regex (GNU grep only).** macOS BSD grep does not support `-P`. Use the `grep -oE | sed` pattern shown above, or better yet, use `search_files` from inside the operator agent which avoids all shell-compatibility issues.
- Always run from the skill directory root (the directory containing `SKILL.md`).
- The `attachments/` directory is non-standard but must be included in the scan to catch R11 drift.
- When a skill uses both a bullet manifest list and inline backtick references, the inline extraction may produce duplicates — `sort -u` handles this.
- The `search_files` tool is the safest and most portable approach when running inside the operator agent. Prefer it over shell grep for manifest reconciliation.
- **Do NOT use `search_files(target='files')` for directory enumeration.** Use `ls` via `terminal` instead. The search index can return 0 results for populated directories (observed 2026-06-29 on macOS).
