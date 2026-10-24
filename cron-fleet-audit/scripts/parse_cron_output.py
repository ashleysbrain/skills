#!/usr/bin/env python3
"""
Parse hermes cron list output into structured data.

This script converts the formatted table output of `hermes cron list` 
into a list of job dictionaries for easier processing.
"""

import re
import json
from datetime import datetime
from typing import List, Dict, Any, Optional


def parse_cron_list(output: str) -> List[Dict[str, Any]]:
    """
    Parse hermes cron list output into structured job data.
    
    Args:
        output: Raw string output from `hermes cron list`
        
    Returns:
        List of job dictionaries with parsed fields
    """
    jobs = []
    
    # Split by double newline to separate job entries
    # Filter out empty entries and the header/footer
    entries = [entry.strip() for entry in output.split('\n\n') 
               if entry.strip() and not entry.startswith('┌') and not entry.startswith('│')]
    
    for entry in entries:
        job = _parse_job_entry(entry)
        if job:
            jobs.append(job)
    
    return jobs


def _parse_job_entry(entry: str) -> Optional[Dict[str, Any]]:
    """Parse a single job entry from the cron list output."""
    lines = entry.split('\n')
    
    # First line contains job ID and state
    first_line = lines[0].strip()
    if not first_line:
        return None
    
    # Extract job ID and state from first line
    # Format: "  63f5bb919948 [active]" or similar
    parts = first_line.split()
    if len(parts) < 2:
        return None
        
    job_id = parts[0]
    state_match = re.search(r'\[([^\]]+)\]', first_line)
    state = state_match.group(1) if state_match else 'unknown'
    
    # Initialize job dictionary
    job = {
        'job_id': job_id,
        'state': state,
        'name': None,
        'schedule': None,
        'repeat': None,
        'next_run': None,
        'deliver': None,
        'skills': None,
        'workdir': None,
        'script': None,
        'mode': None,
        'last_run_raw': None,
        'last_status': None,
        'last_run_time': None,
        'error_details': None
    }
    
    # Process remaining lines
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('Name:'):
            job['name'] = line.split(':', 1)[1].strip()
        elif line.startswith('Schedule:'):
            job['schedule'] = line.split(':', 1)[1].strip()
        elif line.startswith('Repeat:'):
            job['repeat'] = line.split(':', 1)[1].strip()
        elif line.startswith('Next run:'):
            job['next_run'] = line.split(':', 1)[1].strip()
        elif line.startswith('Deliver:'):
            job['deliver'] = line.split(':', 1)[1].strip()
        elif line.startswith('Skills:'):
            job['skills'] = line.split(':', 1)[1].strip()
        elif line.startswith('Workdir:'):
            job['workdir'] = line.split(':', 1)[1].strip()
        elif line.startswith('Script:'):
            job['script'] = line.split(':', 1)[1].strip()
        elif line.startswith('Mode:'):
            job['mode'] = line.split(':', 1)[1].strip()
        elif line.startswith('Last run:'):
            job['last_run_raw'] = line.split(':', 1)[1].strip()
            # Parse the last run raw to get status and timestamp
            # Example: "2026-06-10T17:40:50.828774-05:00  ok"
            # or "2026-06-10T15:11:15.930703-05:00  error: RuntimeError: ..."
            last_run_parts = job['last_run_raw'].rsplit(' ', 1)
            if len(last_run_parts) == 2:
                timestamp_str, status = last_run_parts
                job['last_run_time'] = timestamp_str
                job['last_status'] = status
                if status != 'ok' and status.startswith('error:'):
                    job['error_details'] = status[6:].strip()
            else:
                # Fallback if format is unexpected
                job['last_run_time'] = job['last_run_raw']
                job['last_status'] = 'unknown'
    
    return job


def parse_cron_list_to_json(output: str) -> str:
    """
    Parse cron list output and return as JSON string.
    
    Args:
        output: Raw string output from `hermes cron list`
        
    Returns:
        JSON string representation of the parsed jobs
    """
    jobs = parse_cron_list(output)
    return json.dumps(jobs, indent=2)


def main():
    """Main function for command-line usage."""
    import sys
    
    if len(sys.argv) > 1:
        # Read from file
        with open(sys.argv[1], 'r') as f:
            output = f.read()
    else:
        # Read from stdin
        output = sys.stdin.read()
    
    # Parse and output as JSON
    result = parse_cron_list_to_json(output)
    print(result)


if __name__ == '__main__':
    main()