# Journal Update Commands for Cron Mode

These commands are used to create timestamped journal entries for FORGE and ARBITER when no talent requests are found.

## FORGE Journal Update
```bash
# Ensure directories exist
mkdir -p ~/.sibling-agent/workspace/intel/agents/journal/FORGE
mkdir -p ~/.sibling-agent/workspace/intel/agents/journal/ARBITER

# Get current date in YYYY-MM-DD format
DATE=$(date -u +'%Y-%m-%d')

# Run fleet analytics sync to get agent counts (optional, can be done before or after)
# For simplicity, we assume the sync has been run and we have the numbers.
# In the actual skill procedure, the numbers are included when creating the file.

# Create FORGE journal entry with placeholder for agent count (to be replaced after sync)
cat > ~/.sibling-agent/workspace/intel/agents/journal/FORGE/${DATE}.md << 'EOF'
# FORGE Journal — ${DATE}

## Talent Request Processing

### No new talent requests found.

## Fleet State

- Total active agents: [to be filled from fleet analytics sync]
- New agents this session: 0
- Requests processed: 0
- Dispatches (no spawn): 0
- Spawns: 0
EOF
```

## ARBITER Journal Update
```bash
# Ensure directories exist (if not already done)
mkdir -p ~/.sibling-agent/workspace/intel/agents/journal/FORGE
mkdir -p ~/.sibling-agent/workspace/intel/agents/journal/ARBITER

# Get current date in YYYY-MM-DD format
DATE=$(date -u +'%Y-%m-%d')

# Create ARBITER journal entry
cat > ~/.sibling-agent/workspace/intel/agents/journal/ARBITER/${DATE}.md << 'EOF'
# ARBITER Journal — ${DATE}

## Talent Request Processing

### No new talent requests found.

## Fleet State

- Total active agents: [to be filled from fleet analytics sync]
- New agents this session: 0
- Requests processed: 0
- Dispatches (no spawn): 0
- Spawns: 0
EOF
```

## Notes
- The journal entries are created as markdown files in the respective agent's journal subdirectory.
- The date format in the filename and header is YYYY-MM-DD.
- After creating the journal entries, run the fleet analytics sync to update the agent counts, then optionally update the journal files with the actual numbers (though in practice, the numbers are added directly in the write_file command as shown in the skill procedure).
- The example above uses placeholders; in the actual skill procedure, the fleet analytics numbers are incorporated when creating the file.