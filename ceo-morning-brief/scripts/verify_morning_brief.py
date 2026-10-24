#!/usr/bin/env python3
"""
Verification script for principal Morning Brief format.
This script checks if a morning brief follows the required format.
"""

import re
import sys

def verify_morning_brief_format(content):
    """
    Verify that the morning brief follows the required format.
    
    Args:
        content (str): The morning brief content to verify
        
    Returns:
        tuple: (bool, list) - (is_valid, list_of_errors)
    """
    errors = []
    
    # Check for required format markers
    if not content.strip().startswith('---'):
        errors.append("Missing opening '---'")
    
    if not content.strip().endswith('---'):
        errors.append("Missing closing '---'")
    
    # Check for required sections
    required_sections = [
        '## principal Morning Brief —',
        '### THE ONE THING',
        '### TODAY\'S PRIORITY STACK (ranked)',
        '### WHAT\'S OFF THE LIST (and why)',
        '### COMMITMENT CHECK',
        '### DECISIONS NEEDED FROM ASHLEY'
    ]
    
    for section in required_sections:
        if section not in content:
            errors.append(f"Missing required section: {section}")
    
    # Check THE ONE THING is one sentence
    the_one_thing_match = re.search(r'### THE ONE THING\s*\n\s*(.+?)\s*\n\s*###', content, re.DOTALL)
    if the_one_thing_match:
        the_one_thing_content = the_one_thing_match.group(1).strip()
        # Count sentences by looking for periods followed by space or end of string
        sentence_count = len(re.findall(r'[.!?]+(?:\s|$)', the_one_thing_content))
        if sentence_count != 1:
            errors.append(f"THE ONE THING should be exactly one sentence, found {sentence_count}")
    else:
        errors.append("Could not find THE ONE THING section")
    
    # Check TODAY'S PRIORITY STACK has 3-5 items
    priority_stack_match = re.search(r'### TODAY\'S PRIORITY STACK \(ranked\)\s*\n\s*(.+?)\s*\n\s*###', content, re.DOTALL)
    if priority_stack_match:
        priority_stack_content = priority_stack_match.group(1).strip()
        # Count numbered items
        numbered_items = re.findall(r'^\s*\d+\.\s*\*\*', priority_stack_content, re.MULTILINE)
        item_count = len(numbered_items)
        if item_count < 3 or item_count > 5:
            errors.append(f"TODAY'S PRIORITY STACK should have 3-5 items, found {item_count}")
    else:
        errors.append("Could not find TODAY'S PRIORITY STACK section")
    
    # Check for AI telltales to avoid
    ai_telltales = [r'—', r'Furthermore', r'Moreover']
    for telltale in ai_telltales:
        if re.search(telltale, content):
            errors.append(f"AI telltale found: {telltale}")
    
    return len(errors) == 0, errors

def main():
    if len(sys.argv) != 2:
        print("Usage: python verify_morning_brief.py <morning_brief_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    is_valid, errors = verify_morning_brief_format(content)
    
    if is_valid:
        print("✅ Morning brief format is valid!")
        sys.exit(0)
    else:
        print("❌ Morning brief format has errors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

if __name__ == "__main__":
    main()