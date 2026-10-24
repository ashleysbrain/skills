# Baseline-First Gate and File Write Guidelines

## Overview

the operator agent includes a "baseline-first gate" mechanism that prevents accidental overwrites of important files or artifacts. When you attempt to write to a file that the system detects might be an existing artifact (based on path, content, or context), you'll receive an error like:

```
Baseline-first gate blocked a new file write to /path/to/file.ext. This turn looks like an edit to an existing artifact. Inspect and patch the baseline first, or explicitly switch the canonical artifact in the session state before creating a new path.
```

This protection helps prevent unintended modifications to session outputs, skills, or other important files.

## Understanding the Gate

The baseline-first gate activates when:
- Attempting to write to certain protected paths (like session outputs, skill files, or configuration files)
- The target file resembles an existing artifact in the system
- The write operation appears to be creating a new file where one might already exist conceptually

## Proper File Write Procedures

### Option 1: Inspect and Patch Existing Files (Recommended for Updates)

If you need to modify an existing file:
1. First, inspect the file using `read_file` or `skill_view` (for skills)
2. Use `patch` or `write_file` with appropriate context to make targeted changes
3. For skills, use `skill_manage(action='patch')` to update specific sections

### Option 2: Switch Canonical Artifact (For New Versions)

If you intend to replace an existing artifact:
1. Use the appropriate tool to switch the canonical artifact (e.g., for skills, this might involve versioning)
2. Then proceed with the write operation

### Option 3: Use Alternative Paths (For Truly New Files)

When creating genuinely new files:
1. Choose paths outside protected areas (e.g., `/tmp/`, your project directories, or `<agent-home>/` subdirectories that aren't monitored)
2. Use descriptive timestamps or version indicators in filenames
3. Consider using the `skills` system for reusable procedures instead of one-off files

## Best Practices for Documentation and Briefs

### Creating Architecture Briefs
1. **For session-specific details**: Save as a reference file under a relevant skill using `skill_manage(action='write_file', file_path='references/<topic>.md')`
2. **For reusable templates**: Save as a template file under a skill using `file_path='templates/<name>.<ext>'`
3. **For executable procedures**: Save as a script file under a skill using `file_path='scripts/<name>.<ext>'`
4. **For session transcripts**: Use `session_search()` to recall past work rather than duplicating files

### Working Within Session Constraints
- Prefer updating existing skills over creating new one-off documents
- Use the skill library's hierarchical structure (class-level umbrellas with references/templates/scripts)
- Leverage `session_search` for historical context instead of saving lengthy transcripts
- When creating CTO briefs or executive summaries, consider saving them as skill references with clear versioning

## Troubleshooting Common Scenarios

### "I just want to create a simple text file"
If you need temporary storage:
```bash
# Use /tmp for truly temporary files
terminal(command="echo 'content' > /tmp/myfile.txt")

# Or use hermes tools for session-scoped temporary work
execute_code(code="import tempfile; print(tempfile.gettempdir())")
```

### "I need to save this for future reference"
If the information should persist:
1. Determine if it belongs in memory (user preferences, environment facts)
2. Determine if it belongs in a skill (reusable procedures, workflows)
3. For session-specific context, trust that `session_search` will retrieve it later

### "This is a skill update"
Use the proper skill management tools:
- `skill_view(name)` to read
- `skill_manage(action='patch')` to update
- `skill_manage(action='create')` for new skills (only for class-level umbrellas)

## Related References
- See `references/layered-memory-stacks.md` for memory organization concepts
- See `references/launch-path-verification.md` for validating file operations
- See the "Adding a Tool" and "Adding a Slash Command" sections in the main hermes-agent skill for proper extension patterns