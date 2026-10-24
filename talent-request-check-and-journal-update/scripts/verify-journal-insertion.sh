#!/bin/bash
# verify-journal-insertion.sh
# Verify that journal markdown files for FORGE and ARBITER exist for today.

set -euo pipefail

JOURNAL_BASE=~/.sibling-agent/workspace/intel/agents/journal
TODAY=$(date '+%Y-%m-%d')

echo "Checking journal markdown files for $TODAY..."

# Function to check markdown file for an agent
check_agent_journal() {
    local agent_type=$1  # Either "FORGE" or "ARBITER"
    local journal_dir="$JOURNAL_BASE/$agent_type"
    local journal_file="$journal_dir/$TODAY.md"

    if [[ ! -d "$journal_dir" ]]; then
        echo "WARNING: Journal directory for $agent_type not found: $journal_dir"
        return 1
    fi

    if [[ ! -f "$journal_file" ]]; then
        echo "WARNING: No journal markdown file found for $agent_type on $TODAY: $journal_file"
        return 1
    else
        # Optionally check if file is not empty
        if [[ ! -s "$journal_file" ]]; then
            echo "WARNING: Journal markdown file for $agent_type on $TODAY is empty: $journal_file"
            return 1
        else
            echo "OK: Found journal markdown file for $agent_type on $TODAY: $journal_file"
            return 0
        fi
    fi
}

check_agent_journal "FORGE"
check_agent_journal "ARBITER"

echo "Verification complete."