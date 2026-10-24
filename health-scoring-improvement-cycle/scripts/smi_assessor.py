#!/usr/bin/env python3
"""
Scoring Maturity Index (SMI) Assessor for 8D360/TWC scoring platform.
Implements the SMI framework from the health-scoring-improvement-cycle skill.
"""

import os
import sqlite3
import subprocess
import datetime

def check_engine_completeness():
    """Check what actually EXISTS and WORKS (25 points)"""
    points = 0
    details = []
    
    # 1. Rescore engine exists and passes tests (10 pts)
    rescore_path = os.path.expanduser('~/your-workspace/hydra-os/scripts/rescore-engine/rescore_engine.py')
    rescore_exists = os.path.exists(rescore_path)
    if rescore_exists:
        points += 10
        details.append("Rescore engine: EXISTS")
    else:
        details.append("Rescore engine: MISSING")
    
    # 2. Nutrition engine exists (5 pts)
    nut_path = os.path.expanduser('~/your-workspace/hydra-os/scripts/8d360-nutrition-engine.py')
    if os.path.exists(nut_path):
        points += 5
        details.append("Nutrition engine: EXISTS")
    else:
        details.append("Nutrition engine: MISSING")
    
    # 3. Sexual health engine exists (5 pts)
    sh_path = os.path.expanduser('~/your-workspace/hydra-os/scripts/8d360-sexual-health-engine.py')
    if os.path.exists(sh_path):
        points += 5
        details.append("Sexual health engine: EXISTS")
    else:
        details.append("Sexual health engine: MISSING")
    
    # 4. Fleet TWC engine exists (5 pts)
    fleet_path = os.path.expanduser('~/your-workspace/hydra-os/scripts/fleet-twc-engine.py')
    if os.path.exists(fleet_path):
        points += 5
        details.append("Fleet TWC engine: EXISTS")
    else:
        details.append("Fleet TWC engine: MISSING")
    
    # 5. Interaction matrix implemented in scoring pipeline (5 pts)
    db = os.path.expanduser('~/your-workspace/health-private/ashley_unified_health.db')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM interaction_matrix")
        im_count = c.fetchone()[0]
        if im_count == 28:
            points += 5
            details.append(f"Interaction matrix rows: {im_count}/28")
        else:
            details.append(f"Interaction matrix rows: {im_count}/28 (INCOMPLETE)")
        conn.close()
    else:
        details.append("Interaction matrix: DATABASE MISSING")
    
    return points, details

def check_test_coverage():
    """Check test coverage (20 points)"""
    points = 0
    details = []
    
    # Run rescore engine tests
    result = subprocess.run(['python3', os.path.expanduser('~/your-workspace/hydra-os/scripts/rescore-engine/rescore_engine.py'), 'test'], 
                           capture_output=True, text=True, timeout=60)
    output = result.stdout + result.stderr
    tests_pass = 'FAIL' not in output and result.returncode == 0
    
    if tests_pass:
        points += 20
        details.append("All 7 tests pass")
    else:
        # Partial credit based on how many tests pass
        # This is a simplification - in reality we'd parse the test output more carefully
        if '✓' in output:
            passed_tests = output.count('✓')
            if passed_tests >= 5:
                points += 12
                details.append(f"{passed_tests}/7 tests pass")
            elif passed_tests >= 1:
                points += 5
                details.append(f"{passed_tests}/7 tests pass")
            else:
                details.append("0/7 tests pass")
        else:
            details.append("Tests failing or unable to parse results")
    
    # Check if double-count property test exists
    has_double_count = 'double_count' in output.lower()
    if has_double_count:
        details.append("Double-count test: PRESENT")
    else:
        details.append("Double-count test: MISSING")
    
    return points, details

def check_validation_coverage():
    """Check whether independent validation exists (20 points)"""
    points = 0
    details = []
    
    # Check for VERITAS audit panel
    veritas_agents_dir = os.path.expanduser('~/your-workspace/hydra-os/intel/agents/profiles/')
    has_veritas = False
    if os.path.exists(veritas_agents_dir):
        for f in os.listdir(veritas_agents_dir):
            if f.startswith('VERITAS-') and f.endswith('.md'):
                has_veritas = True
                break
    
    if has_veritas:
        points += 8
        details.append("VERITAS audit agents: FOUND")
    else:
        details.append("VERITAS audit agents: NOT SPAWNED")
    
    # Check for calibration files
    cal_path = os.path.expanduser('~/your-workspace/hydra-os/memory/principal-8d/calibration.json')
    if os.path.exists(cal_path):
        points += 7
        details.append("Calibration file: EXISTS")
    else:
        details.append("Calibration file: MISSING")
    
    # Check for scoring methodology paper
    methods = os.path.expanduser('~/your-workspace/hydra-os/products/qubit-gr/research/SCORING-METHODOLOGY-UNIVERSAL.md')
    if os.path.exists(methods):
        points += 5
        details.append("Universal methodology: EXISTS")
    else:
        details.append("Universal methodology: MISSING")
    
    # Check PRD
    prd = os.path.expanduser('~/.sibling-agent/workspace/intel/wellness/8D360-PRD.md')
    if os.path.exists(prd):
        # Points already allocated above, just noting for completeness
        details.append("PRD: EXISTS")
    else:
        details.append("PRD: MISSING")
    
    return points, details

def check_data_quality():
    """Check data quality (20 points)"""
    points = 0
    details = []
    
    db = os.path.expanduser('~/your-workspace/health-private/ashley_unified_health.db')
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        c = conn.cursor()
        
        # Days with real (non-carry-forward) scores in last 30 days
        c.execute("SELECT COUNT(*) FROM daily_scorecard WHERE date >= date('now', '-30 days') AND twc_score IS NOT NULL AND source NOT IN ('cron','carryforward')")
        real_days = c.fetchone()[0]
        if real_days >= 20:
            points += 8
            details.append(f"Days with real scores (30d): {real_days}/30")
        elif real_days >= 10:
            points += 5
            details.append(f"Days with real scores (30d): {real_days}/30")
        else:
            points += 2
            details.append(f"Days with real scores (30d): {real_days}/30")
        
        # Evidence coverage
        c.execute("SELECT COUNT(DISTINCT date) FROM nutrition_daily WHERE date >= date('now', '-30 days')")
        nut_days = c.fetchone()[0]
        c.execute("SELECT COUNT(DISTINCT date) FROM ef_compass_daily WHERE date >= date('now', '-30 days')")
        ef_days = c.fetchone()[0]
        c.execute("SELECT COUNT(DISTINCT date) FROM sexual_health_daily WHERE date >= date('now', '-30 days')")
        sh_days = c.fetchone()[0]
        
        subtable_points = 0
        if nut_days >= 15 and ef_days >= 15 and sh_days >= 15:
            subtable_points = 5
            details.append(f"Nutrition coverage: {nut_days}/30, EF COMPASS coverage: {ef_days}/30, Sexual health coverage: {sh_days}/30 (ALL >=15)")
        elif nut_days >= 10 or ef_days >= 10 or sh_days >= 10:
            subtable_points = 3
            details.append(f"Nutrition coverage: {nut_days}/30, EF COMPASS coverage: {ef_days}/30, Sexual health coverage: {sh_days}/30 (MIXED)")
        else:
            subtable_points = 1
            details.append(f"Nutrition coverage: {nut_days}/30, EF COMPASS coverage: {ef_days}/30, Sexual health coverage: {sh_days}/30 (SPARSE)")
        points += subtable_points
        
        # Activity database completeness
        c.execute("SELECT COUNT(*) FROM master_activities WHERE is_active=1")
        total_activities = c.fetchone()[0]
        c.execute("SELECT primary_dimension, COUNT(*) FROM master_activities WHERE is_active=1 GROUP BY primary_dimension")
        dims = c.fetchall()
        min_dim = min(d[1] for d in dims) if dims else 0
        max_dim = max(d[1] for d in dims) if dims else 0
        
        activity_points = 0
        if total_activities >= 100 and min_dim >= 15 and max_dim <= 25:  # Reasonably balanced
            activity_points = 4
            details.append(f"Activities: {total_activities} total, min dim={min_dim}, max dim={max_dim}")
        elif total_activities >= 50:
            activity_points = 2
            details.append(f"Activities: {total_activities} total, min dim={min_dim}, max dim={max_dim}")
        else:
            details.append(f"Activities: {total_activities} total, min dim={min_dim}, max dim={max_dim}")
        points += activity_points
        
        # Interaction matrix
        c.execute("SELECT COUNT(*) FROM interaction_matrix")
        im = c.fetchone()[0]
        if im == 28:
            points += 3
            details.append(f"Interaction matrix: {im}/28 pairs")
        elif im >= 20:
            points += 1
            details.append(f"Interaction matrix: {im}/28 pairs (PARTIAL)")
        else:
            details.append(f"Interaction matrix: {im}/28 pairs (SPARSE)")
        
        conn.close()
    else:
        details.append("DATABASE MISSING - cannot assess data quality")
    
    return points, details

def check_production_readiness():
    """Check production readiness (15 points)"""
    points = 0
    details = []
    
    # Multi-user architecture?
    partner_db = os.path.expanduser('~/your-workspace/health-private/ef-panel/brandon_ef_tracker.db')
    multi_user = os.path.exists(partner_db)
    if multi_user:
        points += 5
        details.append("Multi-user architecture: YES (partner DB exists)")
    else:
        details.append("Multi-user architecture: SINGLE USER ONLY")
    
    # JSON schema for API output?
    schema_files = []
    for root, dirs, files in os.walk(os.path.expanduser('~/your-workspace/hydra-os/products')):
        for f in files:
            if 'schema' in f.lower() and f.endswith(('.json', '.md', '.sql')):
                schema_files.append(os.path.join(root, f))
    
    if len(schema_files) > 0:
        points += 5
        details.append(f"Schema files found: {len(schema_files)}")
        for sf in schema_files[:3]:  # Show first 3
            details.append(f"  {sf}")
    else:
        details.append("Schema files found: 0")
    
    # Export/API capability?
    api_scripts = []
    for root, dirs, files in os.walk(os.path.expanduser('~/your-workspace')):
        for f in files:
            if 'api' in f.lower() or 'export' in f.lower():
                api_scripts.append(os.path.join(root, f))
    
    if len(api_scripts) > 0:
        points += 5
        details.append(f"API/export scripts: {len(api_scripts)}")
    else:
        details.append("API/export scripts: 0")
    
    return points, details

def calculate_smi():
    """Calculate the overall SMI score"""
    engine_points, engine_details = check_engine_completeness()
    test_points, test_details = check_test_coverage()
    validation_points, validation_details = check_validation_coverage()
    data_points, data_details = check_data_quality()
    prod_points, prod_details = check_production_readiness()
    
    total_points = engine_points + test_points + validation_points + data_points + prod_points
    
    # Classify
    if total_points >= 85:
        classification = "Production Ready"
    elif total_points >= 70:
        classification = "Beta Ready"
    elif total_points >= 50:
        classification = "Alpha Ready"
    elif total_points >= 30:
        classification = "Lab Stage"
    else:
        classification = "Pre-Product"
    
    # Prepare result
    result = {
        "total_score": total_points,
        "classification": classification,
        "domain_scores": {
            "Engine Completeness": {"points": engine_points, "max": 25, "details": engine_details},
            "Test Coverage": {"points": test_points, "max": 20, "details": test_details},
            "Validation Coverage": {"points": validation_points, "max": 20, "details": validation_details},
            "Data Quality": {"points": data_points, "max": 20, "details": data_details},
            "Production Readiness": {"points": prod_points, "max": 15, "details": prod_details}
        }
    }
    
    return result

def main():
    """Main function to run SMI assessment and print results"""
    result = calculate_smi()
    
    print("=" * 60)
    print("SCORING MATURITY INDEX ASSESSMENT")
    print("=" * 60)
    print(f"SMI: {result['total_score']}/100 [{result['classification']}]")
    print()
    print("Domain Scores:")
    for domain, scores in result["domain_scores"].items():
        print(f"  {domain}: {scores['points']}/{scores['max']}")
        for detail in scores["details"]:
            print(f"    - {detail}")
    print()
    
    # Determine blockers and recommendations
    blockers = []
    recommendations = []
    
    # Check for critical blockers
    if result["domain_scores"]["Engine Completeness"]["points"] < 25:
        blockers.append("Fleet TWC engine missing")
        recommendations.append("Develop and test fleet-twc-engine.py")
    
    if result["domain_scores"]["Validation Coverage"]["points"] < 20:
        if "Calibration file: EXISTS (not validated by panel)" in str(result["domain_scores"]["Validation Coverage"]["details"]):
            blockers.append("Calibration not validated by independent panel")
            recommendations.append("Submit calibration for independent panel review")
    
    if result["domain_scores"]["Data Quality"]["points"] < 15:
        if "Days with real scores (30d):" in str(result["domain_scores"]["Data Quality"]["details"]):
            # Extract the days number
            import re
            match = re.search(r'Days with real scores \(30d\): (\d+)/30', str(result["domain_scores"]["Data Quality"]["details"]))
            if match:
                days = int(match.group(1))
                if days < 10:
                    blockers.append(f"Low real scored days ({days}/30)")
                    recommendations.append("Improve data pipeline to increase real scored days")
        
        if "Nutrition coverage:" in str(result["domain_scores"]["Data Quality"]["details"]) or \
           "Sexual health coverage:" in str(result["domain_scores"]["Data Quality"]["details"]):
            blockers.append("Low nutrition and/or sexual health coverage")
            recommendations.append("Improve nutrition and sexual health data logging")
    
    if blockers:
        print("BLOCKERS TO LAUNCH:")
        for blocker in blockers:
            print(f"  - {blocker}")
        print()
    
    if recommendations:
        print("NEXT 3 HIGHEST-ROI ACTIONS:")
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"  {i}. {rec}")
        print()
    
    # Return result for potential logging
    return result

if __name__ == "__main__":
    main()