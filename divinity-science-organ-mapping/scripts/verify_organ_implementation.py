#!/usr/bin/env python3
"""
Organ Implementation Verification Script
Checks that organ classes follow the Divinity Science naming conventions
"""

import sys
import os
import re
import ast
import importlib.util
from typing import Dict, List, Tuple, Optional

def check_organ_class(file_path: str) -> Tuple[bool, List[str]]:
    """
    Check if an organ class file follows DS naming conventions
    Returns (is_valid, list_of_issues)
    """
    issues = []
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Parse the Python file
        tree = ast.parse(content)
        
        # Find class definitions
        class_defs = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        
        organ_classes = []
        for class_def in class_defs:
            # Check if it looks like an organ class (has expected attributes)
            has_name = any(isinstance(node, ast.Assign) and 
                          any(isinstance(target, ast.Name) and target.id == 'name' 
                              for target in node.targets)
                          for node in class_def.body)
            has_scientist = any(isinstance(node, ast.Assign) and 
                               any(isinstance(target, ast.Name) and target.id == 'scientist' 
                                   for target in node.targets)
                               for node in class_def.body)
            
            if has_name and has_scientist:
                organ_classes.append(class_def)
        
        if not organ_classes:
            issues.append("No organ class found with required 'name' and 'scientist' attributes")
            return False, issues
        
        # Check each organ class
        for organ_class in organ_classes:
            class_name = organ_class.name
            
            # Extract attribute values
            attributes = {}
            for node in organ_class.body:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            attr_name = target.id
                            if isinstance(node.value, ast.Constant):
                                attributes[attr_name] = node.value.value
                            elif isinstance(node.value, ast.Str):  # Python 3.7 compatibility
                                attributes[attr_name] = node.value.s
            
            # Check required attributes
            required_attrs = ['name', 'scientist', 'scientist_full', 'discovery']
            for attr in required_attrs:
                if attr not in attributes:
                    issues.append(f"Class {class_name} missing required attribute: {attr}")
            
            # Check scientist format
            if 'scientist' in attributes:
                scientist = attributes['scientist']
                if not re.match(r'^DS\s+[A-Z][a-z]+$', scientist):
                    issues.append(f"Class {class_name} scientist '{scientist}' doesn't match format 'DS [LastName]'")
            
            # Check that name is reasonable
            if 'name' in attributes:
                name = attributes['name']
                if not name or len(name.strip()) == 0:
                    issues.append(f"Class {class_name} has empty name")
                    
    except SyntaxError as e:
        issues.append(f"Syntax error in {file_path}: {e}")
        return False, issues
    except Exception as e:
        issues.append(f"Error checking {file_path}: {e}")
        return False, issues
    
    return len(issues) == 0, issues

def check_registry_file(file_path: str) -> Tuple[bool, List[str]]:
    """
    Check that organ registry uses scientist-based keys
    """
    issues = []
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Look for ORGANS dictionary
        if 'ORGANS' not in content:
            issues.append("No ORGANS dictionary found")
            return False, issues
            
        # Check for scientist-based keys (this is a simplified check)
        # In practice, you'd want to parse this more carefully
        lines = content.split('\n')
        in_organs_dict = False
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('ORGANS:'):
                in_organs_dict = True
                continue
            elif in_organs_dict and stripped.startswith('}'):
                break
            elif in_organs_dict and ':' in stripped and not stripped.startswith('#'):
                # Check if it looks like a dictionary entry
                if '"' in stripped or "'" in stripped:
                    # This is a simplistic check - in reality you'd parse the dict
                    if 'ds_' not in stripped.lower():
                        issues.append(f"Registry entry may not use scientist-based key: {stripped}")
                        
    except Exception as e:
        issues.append(f"Error checking registry file {file_path}: {e}")
        return False, issues
    
    return len(issues) == 0, issues

def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_organ_implementation.py <organ_class_file> [registry_file]")
        sys.exit(1)
    
    organ_file = sys.argv[1]
    registry_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"Checking organ class: {organ_file}")
    is_valid, issues = check_organ_class(organ_file)
    
    if issues:
        print("ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("Organ class check: PASSED")
    
    if registry_file:
        print(f"\nChecking registry file: {registry_file}")
        is_valid_reg, issues_reg = check_registry_file(registry_file)
        
        if issues_reg:
            print("ISSUES FOUND:")
            for issue in issues_reg:
                print(f"  - {issue}")
        else:
            print("Registry check: PASSED")
    
    if issues or (registry_file and issues_reg):
        sys.exit(1)
    else:
        print("\nAll checks PASSED!")
        sys.exit(0)

if __name__ == "__main__":
    main()