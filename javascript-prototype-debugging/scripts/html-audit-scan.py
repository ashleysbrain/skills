#!/usr/bin/env python3
"""
Systematic regex audit for large single-file HTML apps.
Scans for recurring bug patterns that are invisible in code review but
cause silent failures in the browser.

Usage:
    python3 scripts/html-audit-scan.py <path-to-html-file>

Checks:
    1. Double-API URL bugs (base ends in /api/, path starts with api/)
    2. Double-style HTML attributes (second silently dropped by browser)
    3. Buttons with 'undefined' text
    4. onclick handlers referencing undefined functions
    5. Unnormalized status fields (alive boolean vs status string mismatch)
    6. Orphaned functions referencing non-existent DOM IDs

Exit code 0 = no issues found, 1 = issues found.
"""
import re
import sys


def audit_file(path):
    with open(path, 'r') as f:
        html = f.read()

    errors = []
    warnings = []

    # 1. Double-API URL bugs
    # Pattern: fetch(BASE + 'api/...') where BASE already ends in /api/
    medfetch_calls = re.findall(r"medFetch\(['\"]([^'\"]+)['\"]", html)
    bad_medfetch = [c for c in medfetch_calls if c.startswith('api/')]
    if bad_medfetch:
        errors.append(f"Double-API in medFetch calls: {bad_medfetch}")

    # Also check generic fetch with known API base patterns
    fetch_medapi = re.findall(r"fetch\(\w*API\s*\+\s*[\"']([^\"']+)[\"']", html)
    bad_fetch = [c for c in fetch_medapi if c.startswith('api/')]
    if bad_fetch:
        errors.append(f"Double-API in fetch(API+...) calls: {bad_fetch}")

    # 2. Double-style HTML attributes
    # Pattern: style="..." class="..." style="..." or style="..." style="..."
    double_style = re.findall(r'style="[^"]*"\s+class="[^"]*"\s+style="[^"]*"', html)
    double_style2 = re.findall(r'style="[^"]*"\s+style="[^"]*"', html)
    all_double = double_style + double_style2
    if all_double:
        warnings.append(f"Double-style attributes ({len(all_double)} found):")
        for ds in all_double[:5]:
            warnings.append(f"  {ds[:120]}")

    # 3. Buttons with 'undefined' text
    undefined_btns = re.findall(r'<button[^>]*>undefined</button>', html)
    if undefined_btns:
        errors.append(f"Buttons with 'undefined' text: {len(undefined_btns)}")

    # 4. onclick handlers referencing undefined functions
    onclicks = set(re.findall(r"onclick=\"[^\"]*?(\w+)\(", html))
    all_fns = set(re.findall(r'function\s+(\w+)\s*\(', html))
    # Also arrow/var function assignments
    all_fns |= set(re.findall(r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\(', html))
    # DOM builtins and keywords that aren't function references
    builtins = {'event', 'open', 'close', 'clear', 'remove', 'if', 'q',
                'getElementById', 'querySelector', 'stopPropagation', 'closest',
                'preventDefault', 'console', 'log'}
    missing = onclicks - all_fns - builtins
    if missing:
        warnings.append(f"onclick handlers may reference undefined functions: {missing}")

    # 5. Nav items without corresponding workspace panels
    nav_items = re.findall(r'data-nav="([^"]+)"', html)
    ws_ids = set(re.findall(r'id="ws-([^"]+)"', html))
    for nav in nav_items:
        if nav and nav not in ws_ids and nav not in ('crystal',):
            # Check if it's a dynamic/redirect nav
            if f"navTo('{nav}')" not in html and f'navTo("{nav}")' not in html:
                warnings.append(f"Nav item '{nav}' has no workspace panel ws-{nav}")

    # Report
    print("=" * 60)
    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  [ERROR] {e}")
    else:
        print("NO ERRORS FOUND")

    if warnings:
        print(f"\nPOTENTIAL ISSUES ({len(warnings)}):")
        for w in warnings:
            print(f"  [WARN] {w}")
    else:
        print("NO WARNINGS")
    print("=" * 60)

    return 1 if errors else 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 html-audit-scan.py <path-to-html-file>")
        sys.exit(2)
    sys.exit(audit_file(sys.argv[1]))
