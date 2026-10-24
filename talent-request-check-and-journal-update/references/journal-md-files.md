# Journal Approach: Markdown Files in Journal Directories

For the FORGE and ARBITER talent request processing cron job, journal entries are maintained as markdown files in the respective agent's journal directory rather than database entries.

## Why Markdown Files?

1. **Readability**: Markdown files are human-readable and easy to review directly
2. **Version Control**: Changes are naturally tracked by git
3. **Simplicity**: No need for SQL queries or database schema management
4. **Standard Practice**: Aligns with how other agent activities are journaled in the OpenClaw system

## File Structure

Journal entries are stored as:
- `~/.sibling-agent/workspace/intel/agents/journal/FORGE/YYYY-MM-DD.md`
- `~/.sibling-agent/workspace/intel/agents/journal/ARBITER/YYYY-MM-DD.md`

Where YYYY-MM-DD is the current date in ISO format.

## Content Format

Each journal entry should follow this general structure:

```markdown
# [AGENT_TYPE] Journal - YYYY-MM-DD

## [Section Header]
- Bullet point describing what was done
- Another bullet point for additional details

## [Another Section Header]
- More bullet points as needed

## [AGENT_TYPE] Journal Processing Cron Job (Completed at)
[Day Mon DD HH:MM:SS UTC YYYY]
```

## Advantages Over Database Approach

- No need to manage agent IDs for journal entries
- No database schema migrations required
- Easy to backup and restore via standard file operations
- Can be viewed directly on GitHub or other git interfaces
- Familiar format for engineers and operators

## Migration Note

If there are existing journal entries in the database, they can be left as-is for historical reference. New entries should follow the markdown file approach.