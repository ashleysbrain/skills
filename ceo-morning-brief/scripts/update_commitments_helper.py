#!/usr/bin/env python3
"""
Helper script for updating COMMITMENTS.md according to principal Advisory Board standards.
"""

import re
import sys
from datetime import datetime

def parse_commitments(content):
    """Parse COMMITMENTS.md into sections."""
    sections = {
        'header': '',
        'active_commitments': {
            'date': '',
            'today': [],
            'deferred': [],
            'this_week': [],
            'completed': []
        },
        'footer': ''
    }
    
    # Simple parsing - in reality would be more robust
    lines = content.split('\n')
    current_section = None
    
    for line in lines:
        if line.startswith('# Active principal Commitments'):
            current_section = 'header'
            sections['header'] += line + '\n'
        elif line.startswith('## Format'):
            current_section = 'format'
            sections['header'] += line + '\n'
        elif line.startswith('## Active Commitments —'):
            current_section = 'active_commitments_date'
            # Extract date
            date_match = re.search(r'## Active Commitments — (.+)', line)
            if date_match:
                sections['active_commitments']['date'] = date_match.group(1)
            sections['active_commitments'][current_section] += line + '\n'
        elif line.startswith('### 🔥 TODAY (Do these in order)'):
            current_section = 'today'
            sections['active_commitments'][current_section] += line + '\n'
        elif line.startswith('### DEFERRED FROM TODAY (do this week, not today)'):
            current_section = 'deferred'
            sections['active_commitments'][current_section] += line + '\n'
        elif line.startswith('### THIS WEEK'):
            current_section = 'this_week'
            sections['active_commitments'][current_section] += line + '\n'
        elif line.startswith('### ✅ COMPLETED'):
            current_section = 'completed'
            sections['active_commitments'][current_section] += line + '\n'
        elif line.startswith('## How This Works'):
            current_section = 'footer'
            sections['footer'] += line + '\n'
        elif current_section:
            sections['active_commitments'][current_section] += line + '\n'
        else:
            # Default to header if not in a known section
            sections['header'] += line + '\n'
    
    return sections

def format_commitments(sections):
    """Format sections back into COMMITMENTS.md content."""
    output = sections['header']
    
    output += f'## Active Commitments — {sections["active_commitments"]["date"]}\n\n'
    output += '### 🔥 TODAY (Do these in order)\n'
    for item in sections['active_commitments']['today']:
        output += f'{item}\n'
    output += '\n'
    
    output += '### DEFERRED FROM TODAY (do this week, not today)\n'
    for item in sections['active_commitments']['deferred']:
        output += f'{item}\n'
    output += '\n'
    
    output += '### THIS WEEK\n'
    for item in sections['active_commitments']['this_week']:
        output += f'{item}\n'
    output += '\n'
    
    output += '### ✅ COMPLETED\n'
    for item in sections['active_commitments']['completed']:
        output += f'{item}\n'
    output += '\n'
    
    output += sections['footer']
    
    return output

def update_commitments(current_content, updates):
    """
    Update COMMITMENTS.md with new information.
    
    Args:
        current_content (str): Current COMMITMENTS.md content
        updates (dict): Dictionary with keys:
            - 'move_to_completed': list of items to move to completed
            - 'keep_active': list of items to keep in their current sections
            - 'mark_stale': list of items to mark as stale/scratched with reasons
            - 'add_new': list of new items to add to TODAY
    
    Returns:
        str: Updated COMMITMENTS.md content
    """
    sections = parse_commitments(current_content)
    today_date = sections['active_commitments']['date']
    
    # For simplicity, we'll just rebuild the TODAY section with new items
    # and move specified items to completed
    # In a real implementation, this would be more sophisticated
    
    # Move items to completed
    completed_items = sections['active_commitments']['completed'] + updates.get('move_to_completed', [])
    sections['active_commitments']['completed'] = completed_items
    
    # Add new items to TODAY
    today_items = sections['active_commitments']['today'] + updates.get('add_new', [])
    sections['active_commitments']['today'] = today_items
    
    # Keep other items as-is (in a real implementation, we'd handle marking stale, etc.)
    
    return format_commitments(sections)

def main():
    if len(sys.argv) < 2:
        print("Usage: python update_commitments_helper.py <commitments_file> [--add item1 item2 ...] [--move-to-completed item1 item2 ...]")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    # Parse command line arguments
    updates = {
        'add_new': [],
        'move_to_completed': [],
        'keep_active': [],
        'mark_stale': []
    }
    
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--add':
            i += 1
            while i < len(sys.argv) and not sys.argv[i].startswith('--'):
                updates['add_new'].append(sys.argv[i])
                i += 1
        elif sys.argv[i] == '--move-to-completed':
            i += 1
            while i < len(sys.argv) and not sys.argv[i].startswith('--'):
                updates['move_to_completed'].append(sys.argv[i])
                i += 1
        else:
            i += 1
    
    try:
        with open(filename, 'r') as f:
            current_content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    updated_content = update_commitments(current_content, updates)
    
    # In a real tool, we would write back to the file
    # For this helper script, we'll just output to stdout
    print(updated_content)

if __name__ == "__main__":
    main()