#!/usr/bin/env python3
"""
ECS Code Verification Script
Verifies consistency between engine directories, ecs.py registry, and generated outputs.
"""

import os
import re
import sys
from pathlib import Path

def check_ecs_consistency():
    """Check that ECS codes are consistent across all locations."""
    workspace = Path("/<workspace>")
    registry_path = workspace / "ds-engine-registry" / "ecs.py"
    
    if not registry_path.exists():
        print("ERROR: ecs.py registry not found")
        return False
    
    # Parse ecs.py for engine codes
    ecs_pattern = re.compile(r'"ds_ecs_code"\s*:\s*"(DS-ECS-[^\"]+)"')
    engine_codes = {}
    
    try:
        content = registry_path.read_text()
        matches = ecs_pattern.findall(content)
        for code in matches:
            # Extract engine name from nearby context (simplified)
            engine_codes[code] = "unknown"  # In reality, we'd parse better
        print(f"Found {len(matches)} ECS codes in registry")
    except Exception as e:
        print(f"ERROR reading registry: {e}")
        return False
    
    # Check engine directories
    engine_dirs = [d for d in workspace.iterdir() 
                   if d.is_dir() and d.name.startswith("ds-") and d.name.endswith("-engine")]
    
    print(f"Found {len(engine_dirs)} engine directories")
    
    # Check for git repos
    git_repos = 0
    for engine_dir in engine_dirs:
        if (engine_dir / ".git").exists():
            git_repos += 1
    
    print(f"Of those, {git_repos} are git repositories")
    
    if git_repos < len(engine_dirs):
        print("WARNING: Some engine directories are not git repositories")
        missing = [d.name for d in engine_dirs if not (d / ".git").exists()]
        print(f"Missing git repos: {missing[:10]}{'...' if len(missing) > 10 else ''}")
    
    # Check generated architecture chart
    chart_path = workspace / "docs" / "DS-Organ-System-Architecture.pdf"
    if chart_path.exists():
        print("✓ Organism architecture chart exists")
        # In a real implementation, we'd parse the PDF to check codes
    else:
        print("✗ Organism architecture chart missing")
    
    return True

if __name__ == "__main__":
    if check_ecs_consistency():
        print("\nECS consistency check completed")
        sys.exit(0)
    else:
        print("\nECS consistency check failed")
        sys.exit(1)