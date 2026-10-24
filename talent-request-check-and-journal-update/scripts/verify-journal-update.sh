#!/bin/bash
# Verification script for talent request check and journal update

# Check if journal directories exist
if [[ ! -d ~/.sibling-agent/workspace/intel/agents/journal/FORGE ]]; then
  echo "ERROR: FORGE journal directory not found"
  exit 1
fi

if [[ ! -d ~/.sibling-agent/workspace/intel/agents/journal/ARBITER ]]; then
  echo "ERROR: ARBITER journal directory not found"
  exit 1
fi

# Get today's date in YYYY-MM-DD format
TODAY=$(date -u +'%Y-%m-%d')

# Check if today's journal files exist
if [[ ! -f ~/.sibling-agent/workspace/intel/agents/journal/FORGE/${TODAY}.md ]]; then
  echo "WARNING: FORGE journal for today not found"
  # Not exiting with error because it might be okay if the script hasn't run yet
else
  echo "INFO: FORGE journal for today exists"
fi

if [[ ! -f ~/.sibling-agent/workspace/intel/agents/journal/ARBITER/${TODAY}.md ]]; then
  echo "WARNING: ARBITER journal for today not found"
else
  echo "INFO: ARBITER journal for today exists"
fi

# Check if the talent requests directory exists
if [[ ! -d ~/.sibling-agent/workspace/intel/agents/talent-requests ]]; then
  echo "ERROR: Talent requests directory not found"
  exit 1
fi

echo "Verification completed"
exit 0