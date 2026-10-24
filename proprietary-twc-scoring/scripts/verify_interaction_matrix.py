#!/usr/bin/env python3
"""
Verify interaction matrix values against proprietary TWC specification.
Run this script quarterly as part of algorithmic integrity procedures.
"""
import sqlite3
import sys

DB_PATH = '/<workspace>'

# Proprietary specification values (symmetric)
SPEC = {
    ('PSY', 'INT'): 0.85,
    ('INT', 'PSY'): 0.85,
    ('PHY', 'VOC'): 0.78,
    ('VOC', 'PHY'): 0.78,
    ('SOC', 'SPI'): 0.72,
    ('SPI', 'SOC'): 0.72,
    ('ENV', 'PHY'): 0.68,
    ('PHY', 'ENV'): 0.68,
}

def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Fetch all interaction matrix entries
    c.execute("SELECT dim1, dim2, value FROM interaction_matrix")
    rows = c.fetchall()
    
    print(f"Found {len(rows)} interaction matrix entries")
    print()
    
    deviations = []
    for dim1, dim2, value in rows:
        expected = SPEC.get((dim1, dim2))
        if expected is None:
            print(f"Unexpected pair: {dim1}-{dim2} = {value}")
            continue
        diff = abs(value - expected)
        if diff > 0:
            print(f"{dim1}-{dim2}: expected {expected:.2f}, got {value:.2f}, diff {diff:.2f}")
            if diff > 0.10:
                deviations.append(((dim1, dim2), expected, value, diff))
    
    print()
    if deviations:
        print(f"Found {len(deviations)} deviations > 0.10:")
        for (dim1, dim2), expected, actual, diff in deviations:
            print(f"  {dim1}-{dim2}: expected {expected:.2f}, got {actual:.2f} (diff {diff:.2f})")
        # Determine severity
        max_diff = max(d for _, _, _, d in deviations)
        if max_diff > 0.30:
            print("\n🚨 CRITICAL: Deviations > 0.30 indicate fundamental error in coupling matrix.")
            sys.exit(1)
        elif max_diff > 0.20:
            print("\n⚠️  WARNING: Deviations > 0.20 indicate major implementation gap.")
            sys.exit(1)
        else:
            print("\n⚠️  NOTE: Deviations > 0.10 but <= 0.20 - investigate.")
            sys.exit(0)
    else:
        print("✅ All interaction matrix values match specification within tolerance.")
        sys.exit(0)

if __name__ == '__main__':
    main()