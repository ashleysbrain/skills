# Terminal-Generated File Corruption Scan

Observed 2026-06-17 during 8D Sleep Project Document creation/verification.

## Context

A 542-line engineering document (`8D-SLEEP-PROJECT.md`) was created via a
terminal Python heredoc workaround in a prior context window. When resuming
post-compression, the file existed on disk but contained two corruption bugs
that were invisible at generation time:

1. **Shell interpolation artifact** — line 542 contained literal `$(date)`
   instead of the interpolated date string `2026-06-17`. The Python heredoc
   generation path leaked shell expansion syntax into the output.

2. **Encoding corruption** — line 326 contained Chinese characters
   `privacy说明` where the intended text was `privacy disclosure`. The
   word "说明" (meaning "explanation/instructions") replaced "disclosure"
   due to an encoding or clipboard pipeline mismatch.

## Why this happens

Terminal workarounds (cat heredoc, Python script via write_file+terminal)
are used when the baseline-first gate blocks `write_file` on new markdown
files. These paths introduce failure modes that `write_file` does not:

- **Shell expansion leakage**: `$(...)`, `${...}`, backtick expressions
  can survive into the output if the heredoc delimiter quoting is imperfect
  or if Python f-strings/subprocess calls interpolate shell syntax.
- **Encoding mismatches**: locale settings, clipboard encoding, or
  UTF-8/ASCII boundary errors can inject unexpected characters.
- **Truncation**: large content via heredoc may silently truncate.

## Verification procedure (post-generation AND post-compression)

After writing a file via any terminal workaround, OR after resuming a
session where a file was created via terminal workaround in a prior context:

1. **Check line count and byte count** match expectations:
   ```bash
   wc -l <file> && wc -c <file>
   ```

2. **Scan for shell interpolation artifacts**:
   ```bash
   # Search for unexpanded shell syntax
   grep -n '\$(' <file>
   grep -n '\${' <file>
   grep -n '`' <file>
   ```

3. **Scan for non-ASCII characters in English documents**:
   ```bash
   # Find lines with non-ASCII characters
   grep -nP '[^\x00-\x7F]' <file>
   ```

4. **Read the file end-to-end** — the most reliable check. Read in
   paginated chunks if large (use `read_file` with offset/limit), and
   pay attention to the first line, last line, and any table cells.

5. **Fix with targeted `patch`** — never regenerate the whole file for
   a corruption fix. Patch the specific corrupted strings in place.

## Related skill sections

- Baseline-First Surgical Precision > Pitfalls > "Terminal-generated file
  corruption"
- Baseline-First Surgical Precision > Workarounds A/B/C (terminal heredoc
  generation methods)
- Baseline-First Surgical Precision > Pitfalls > "Compression amnesia"
