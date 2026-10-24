#!/usr/bin/env python3
"""
Perform a comprehensive cron fleet audit.

This script analyzes cron jobs for health, overlaps, and efficiency issues,
generating a detailed report with recommendations.
"""

import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from typing import List, Dict, Any, Tuple, Optional
import argparse
import re


def load_jobs(json_data: str) -> List[Dict[str, Any]]:
    """Load job data from JSON string."""
    return json.loads(json_data)


def check_erroring_jobs(jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Identify jobs with error status."""
    erroring = []
    for job in jobs:
        # Only consider jobs that have run at least once
        if job['last_run_time'] and job['last_run_time'].strip():
            if job['last_status'] != 'ok' and job['last_status'] is not None:
                erroring.append(job)
    return erroring


def check_stalled_jobs(jobs: List[Dict[str, Any]], session_data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """
    Identify jobs that show 'ok' in cron but whose session output ended mid-execution
    without producing a final summary/recommendations.
    
    Args:
        jobs: List of cron job dicts
        session_data: Optional dict mapping job_id -> session info (last message preview, etc.)
    
    Returns:
        List of jobs flagged as stalled/incomplete
    """
    stalled = []
    # Critical daily jobs that must produce output
    critical_job_keywords = [
        'v1 skill product review',
        'advisory board',
        'health insurance',
        'sentinel',
        'vitals',
        'nexus auto-remediation',
        'fleet health check',
        'fleet analytics sync',
        'forge-arbiter',
        'sibling-agent',
        'qbit-gr',
        '8d360',
        'twc',
        'builder-product',
        'scoring maturity',
        'methodology evolution',
        'veritas',
        'overnight build',
        'engine science',
        'cron audit',
        'self-healing',
        'executive task',
        'marketing',
        'product',
        'cto',
        'coo',
        'design',
        'research',
        'legal',
        'cro',
        'quarterly tech',
    ]
    
    for job in jobs:
        # Only check jobs that ran today and show 'ok'
        if (job['last_run_time'] and job['last_run_time'].strip() 
            and job['last_status'] == 'ok'
            and session_data and job['job_id'] in session_data):
           
            session = session_data[job['job_id']]
            last_msg_preview = session.get('last_message_preview', '').lower()
            job_name_lower = job['name'].lower()
            
            # Check if this is a critical daily job
            is_critical = any(kw in job_name_lower for kw in critical_job_keywords)
            
            # Check if session ended mid-execution (no final summary)
            has_final_summary = any(kw in last_msg_preview for kw in [
                'recommend', 'update', 'new skill', 'gap', 'target', 
                'drift', 'corrective action', 'summary', 'delivered',
                'completed', 'status:', 'drift against'
            ])
            
            # If critical job and session exists but no final summary, flag as stalled
            if is_critical and not has_final_summary:
                job_copy = job.copy()
                job_copy['stall_reason'] = f"Session ended mid-execution without final summary. Last preview: {last_msg_preview[:100]}"
                stalled.append(job_copy)
    
    return stalled


def check_overlapping_schedules(jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Find jobs with identical schedule strings."""
    schedule_map = defaultdict(list)
    for job in jobs:
        schedule_map[job['schedule']].append(job)
    
    overlaps = []
    for schedule, job_list in schedule_map.items():
        if len(job_list) > 1:
            overlaps.append({
                'schedule': schedule,
                'jobs': job_list
            })
    return overlaps


def check_paused_jobs(jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Find paused jobs."""
    paused = []
    for job in jobs:
        if job['state'] == 'paused':
            paused.append(job)
    return paused


def check_stale_one_shots(jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Find completed one-shot jobs that should be cleaned up."""
    stale = []
    for job in jobs:
        # One-shot jobs have repeat='0/1' and have already run
        if (job['repeat'] == '0/1' and 
            job['last_run_time'] is not None and 
            job['last_run_time'].strip() != ''):
            stale.append(job)
    return stale


def check_stale_recurring_jobs(jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Identify recurring jobs that haven't run successfully in 7+ days and aren't critical."""
    stale_recurring = []
    # Critical jobs that should not be paused even if stale
    critical_job_keywords = [
        'vitals',
        'sentinel',
        'nexus auto-remediation',
        'health insurance business findings monitor',
        'ds self-healing engine improvement cycle'
    ]
    
    now = datetime.now(timezone.utc)
    for job in jobs:
        # Only consider recurring jobs that are active
        if (job['state'] == 'active' and 
            job['repeat'] == '∞' and 
            job['last_run_time'] is not None and 
            job['last_run_time'].strip() != ''):
            
            # Parse the last run time
            try:
                # Handle ISO format with timezone offset
                last_run_str = job['last_run_time'].strip()
                # Replace space with T for ISO format if needed
                if ' ' in last_run_str:
                    last_run_str = last_run_str.replace(' ', 'T')
                last_run = datetime.fromisoformat(last_run_str)
                # Calculate days since last run
                days_since = (now - last_run).days
                
                # Check if it's been more than 7 days
                if days_since > 7:
                    # Check if it's a critical job
                    job_name_lower = job['name'].lower()
                    is_critical = any(kw in job_name_lower for kw in critical_job_keywords)
                    
                    # If not critical, add to stale recurring jobs
                    if not is_critical:
                        job_copy = job.copy()
                        job_copy['days_since_last_run'] = days_since
                        stale_recurring.append(job_copy)
            except ValueError:
                # If we can't parse the timestamp, skip this job for this check
                pass
    
    return stale_recurring


def parse_schedule_for_moving(schedule_str: str) -> Optional[List[Tuple[int, int]]]:
    """Return a list of (minute, hour) tuples that the job runs at, assuming daily.
    Returns None if the schedule is not suitable for moving (e.g., interval-based, or has complex day restrictions)."""
    if schedule_str.startswith('every '):
        return None  # skip interval-based
    parts = schedule_str.split()
    if len(parts) != 5:
        return None  # skip if not 5 fields
    minute, hour, day_of_month, month, day_of_week = parts
    # We'll skip if day_of_month, month, or day_of_week are not * (unless we want to handle specific days, but for simplicity we skip)
    # For now, we'll only move if all are * (daily)
    if day_of_month != '*' or month != '*' or day_of_week != '*':
        return None
    # Now parse minute and hour
    minute_list = []
    if minute == '*':
        minute_list = list(range(0, 60))
    elif ',' in minute:
        minute_list = [int(m.strip()) for m in minute.split(',') if m.strip().isdigit()]
    else:
        if minute.isdigit():
            minute_list = [int(minute)]
        else:
            return None
    hour_list = []
    if hour == '*':
        hour_list = list(range(0, 24))
    elif ',' in hour:
        hour_list = [int(h.strip()) for h in hour.split(',') if h.strip().isdigit()]
    else:
        if hour.isdigit():
            hour_list = [int(hour)]
        else:
            return None
    # We'll return all combinations, but we will later choose one time to move to.
    times = []
    for h in hour_list:
        for m in minute_list:
            times.append((m, h))  # (minute, hour)
    return times


def suggest_new_schedules(jobs: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Suggest new schedules for jobs to resolve collisions and meet hourly constraints.
    
    Only considers jobs with simple daily schedules (day_of_month='*', month='*', day_of_week='*').
    Attempts to resolve:
    1. Collisions (jobs at the exact same time)
    2. Hours with more than 2 jobs during daytime (6 AM - 11 PM CT)
    
    Returns a dict mapping job_id -> new_schedule string.
    """
    # Filter to jobs with movable daily schedules
    job_data = []
    for job in jobs:
        times = parse_schedule_for_moving(job['schedule'])
        if times is None:
            # Skip this job for moving
            continue
        # Convert to minutes from 00:00
        minutes = [h*60 + m for (m, h) in times]
        # Filter to daytime (6 AM to 11 PM) i.e., 360 to 1380 minutes
        daytime_minutes = [m for m in minutes if 360 <= m < 1380]
        job_data.append({
            'job': job,
            'all_times': minutes,
            'daytime_times': daytime_minutes,
            'original_schedule': job['schedule']
        })
    
    if not job_data:
        return {}
    
    # We'll now try to assign new times to each job to resolve collisions and over-hour.
    # We'll keep track of busy times (in minutes from 00:00) and hourly counts.
    busy_times = set()
    hourly_count = {h: 0 for h in range(6, 24)}  # index 0 corresponds to hour 6
    
    # We'll sort jobs by name for determinism
    job_data.sort(key=lambda x: x['job']['name'])
    
    # We'll also want to preserve the current times if possible, but we will reassign to avoid collisions.
    # We'll try to assign each job to the earliest possible 15-minute slot that doesn't cause a collision 
    # and doesn't cause any hour to exceed 2 jobs.
    # We'll allow a job to have multiple times (if it runs multiple times a day). We'll try to assign each 
    # of its times to a slot.
    # This is a bin packing problem. We'll simplify: we will assign each job to a single time (we will change 
    # the schedule to run at one time only).
    # This is a big change, but we can do it for simplicity.
    # We'll change the schedule to run at a single time (the first time in its list) but we will move that time 
    # to avoid collisions.
    # For jobs that currently run multiple times a day, we will consolidate them to run once a day.
    # This is acceptable for the purpose of reducing collisions.
    
    # We'll assume we want each job to run once a day (we will pick the first time from its list).
    # We'll then assign that time to a slot.
    
    # We'll create a list of jobs with their desired time (we will try to keep as close as possible to the original time).
    # For each job, we'll pick the first daytime time from its list as the preferred time.
    # We'll then try to assign that time, and if not available, we'll find the nearest available 15-minute slot.
    
    # We'll keep track of assignments: job_id -> new_time_in_minutes
    assignments = {}
    
    # We'll also keep track of how many times we have assigned per hour (for the new schedule)
    new_hourly_count = {h: 0 for h in range(6, 24)}
    
    # We'll sort jobs by preferred time (to try to assign in order)
    job_data_with_pref = []
    for data in job_data:
        if data['daytime_times']:
            pref = min(data['daytime_times'])  # earliest daytime time
        else:
            pref = 360  # default to 6 AM if no daytime times
        job_data_with_pref.append((pref, data))
    
    job_data_with_pref.sort(key=lambda x: x[0])
    
    # We'll define a function to find an available slot given a preferred time.
    def find_available_slot(pref_min: int, busy_times: set, new_hourly_count: Dict[int, int], step: int = 15) -> Optional[int]:
        """Return a free time in minutes from 00:00 that is not in busy_times and 
        such that adding it does not cause the hour to exceed 2 jobs.
        We'll search in increasing order of distance from pref_min."""
        # We'll check times in a range around pref_min, but we'll limit to daytime.
        max_offset = 4*60  # 4 hours in minutes
        for offset in range(0, max_offset+1, step):
            for direction in [-1, 1]:
                t = pref_min + direction * offset
                if t < 360 or t >= 1380:
                    continue
                if t in busy_times:
                    continue
                # Check hourly count
                h = t // 60
                if 6 <= h < 24:
                    if new_hourly_count[h] >= 2:
                        continue
                # If we get here, the slot is available
                return t
        return None
    
    # Now assign each job
    for pref, data in job_data_with_pref:
        job = data['job']
        job_id = job['id']
        t = find_available_slot(pref, busy_times, new_hourly_count)
        if t is None:
            # If we can't find a slot, we'll leave the job as is (but we will not move it)
            # We'll still add its current times to busy_times and hourly_count for reporting?
            # We'll skip.
            continue
        # Assign this time to the job
        assignments[job_id] = t
        # Update busy_times and hourly_count
        busy_times.add(t)
        h = t // 60
        if 6 <= h < 24:
            new_hourly_count[h] += 1
    
    # Now we'll generate the new schedules for the jobs we decided to move.
    # We'll change the schedule to run at the assigned time (minute and hour) every day.
    # We'll keep the same day_of_month, month, day_of_week as * * * (since we assumed daily).
    # We'll set the schedule to f"{minute} {hour} * * *"
    moves = {}  # dict of job_id -> new_schedule
    for job_id, t in assignments.items():
        job = next((j for j in jobs if j['id'] == job_id), None)
        if not job:
            continue
        minute = t % 60
        hour = t // 60
        new_schedule = f"{minute} {hour} * * *"
        moves[job_id] = new_schedule
    
    return moves


def calculate_health_score(
    erroring_jobs: List[Dict[str, Any]],
    overlapping_groups: List[Dict[str, Any]],
    paused_jobs: List[Dict[str, Any]],
    stale_one_shots: List[Dict[str, Any]],
    stale_recurring_jobs: List[Dict[str, Any]],
    stalled_jobs: List[Dict[str, Any]] = None
) -> int:
    """Calculate fleet health score (0-100)."""
    error_count = len(erroring_jobs)
    # Count extra jobs in overlaps (beyond the first in each group)
    overlap_count = sum(len(group['jobs']) for group in overlapping_groups) - len(overlapping_groups)
    paused_count = len(paused_jobs)
    stale_count = len(stale_one_shots)
    stale_recurring_count = len(stale_recurring_jobs)
    stalled_count = len(stalled_jobs) if stalled_jobs else 0
    
    # Weights: error: 10 points each, overlap: 5 points per extra job, paused: 2 points each, 
    # stale one-shot: 1 point each, stale recurring: 4 points each, stalled: 8 points each
    health_score = 100 - (error_count * 10) - (overlap_count * 5) - (paused_count * 2) - (stale_count * 1) - (stale_recurring_count * 4) - (stalled_count * 8)
    return max(0, min(100, health_score))


def generate_report(
    jobs: List[Dict[str, Any]],
    erroring_jobs: List[Dict[str, Any]],
    overlapping_groups: List[Dict[str, Any]],
    paused_jobs: List[Dict[str, Any]],
    stale_one_shots: List[Dict[str, Any]],
    stale_recurring_jobs: List[Dict[str, Any]],
    stalled_jobs: List[Dict[str, Any]],
    schedule_suggestions: Dict[str, str],
    health_score: int
) -> str:
    """Generate a markdown report of the audit findings."""
    report_lines = []
    
    # Header
    report_lines.append("# Cron Fleet Audit Report")
    report_lines.append(f"**Generated at:** {datetime.now().isoformat()}Z")
    report_lines.append(f"**Fleet Health Score:** {health_score}/100")
    report_lines.append("")
    
    # Erroring jobs
    report_lines.append("## Erroring Jobs")
    if erroring_jobs:
        for job in erroring_jobs:
            report_lines.append(f"- **{job['name']}** (ID: {job['job_id']})")
            report_lines.append(f"  - Last status: {job['last_status']}")
            if job['error_details']:
                report_lines.append(f"  - Error details: {job['error_details']}")
            report_lines.append(f"  - Last run: {job['last_run_raw']}")
            report_lines.append("  - Recommended action: Investigate error and consider fixing or re-running the job.")
            report_lines.append("")
    else:
        report_lines.append("No erroring jobs found.")
        report_lines.append("")
    
    # Stalled/Incomplete jobs
    report_lines.append("## Stalled/Incomplete Jobs (show 'ok' but no final output)")
    if stalled_jobs:
        for job in stalled_jobs:
            report_lines.append(f"- **{job['name']}** (ID: {job['job_id']})")
            report_lines.append(f"  - Cron status: {job['last_status']}")
            report_lines.append(f"  - Last run: {job['last_run_raw']}")
            report_lines.append(f"  - Stall reason: {job.get('stall_reason', 'Session ended without final summary')}")
            report_lines.append("  - Recommended action: Re-run the job to complete the daily cycle and emit required output.")
            report_lines.append("")
    else:
        report_lines.append("No stalled jobs detected.")
        report_lines.append("")
    
    # Overlapping schedules
    report_lines.append("## Overlapping Schedules")
    if overlapping_groups:
        for group in overlapping_groups:
            report_lines.append(f"- **Schedule:** `{group['schedule']}`")
            report_lines.append("  - Jobs:")
            for job in group['jobs']:
                report_lines.append(f"    - {job['name']} (ID: {job['job_id']})")
            report_lines.append("  - Note: These jobs are scheduled to run at the same exact time.")
            report_lines.append("  - Recommended action: Stagger schedules to avoid resource contention.")
            report_lines.append("")
    else:
        report_lines.append("No overlapping schedules found.")
        report_lines.append("")
    
    # Paused jobs
    report_lines.append("## Paused Jobs Review")
    if paused_jobs:
        for job in paused_jobs:
            report_lines.append(f"- **{job['name']}** (ID: {job['job_id']})")
            report_lines.append(f"  - State: {job['state']}")
            report_lines.append("  - Recommended action: Review if this job should be resumed, modified, or removed.")
            report_lines.append("")
    else:
        report_lines.append("No paused jobs found.")
        report_lines.append("")
    
    # Stale one-shots
    report_lines.append("## Stale One-Shot Jobs (to clean up)")
    if stale_one_shots:
        for job in stale_one_shots:
            report_lines.append(f"- **{job['name']}** (ID: {job['job_id']})")
            report_lines.append(f"  - Repeat: {job['repeat']}")
            report_lines.append(f"  - Last run: {job['last_run_raw']}")
            report_lines.append("  - Recommended action: Remove this completed one-shot job.")
            report_lines.append("")
    else:
        report_lines.append("No stale one-shot jobs found.")
        report_lines.append("")
    
    # Stale recurring jobs
    report_lines.append("## Stale Recurring Jobs (to pause)")
    if stale_recurring_jobs:
        for job in stale_recurring_jobs:
            report_lines.append(f"- **{job['name']}** (ID: {job['job_id']})")
            report_lines.append(f"  - State: {job['state']}")
            report_lines.append(f"  - Repeat: {job['repeat']}")
            report_lines.append(f"  - Days since last run: {job.get('days_since_last_run', 'unknown')}")
            report_lines.append("  - Recommended action: Pause this job as it hasn't run successfully in over 7 days and isn't critical.")
            report_lines.append("")
    else:
        report_lines.append("No stale recurring jobs found.")
        report_lines.append("")
    
    # Schedule optimization suggestions
    report_lines.append("## Schedule Optimization Suggestions")
    if schedule_suggestions:
        report_lines.append("The following schedule changes are suggested to resolve collisions and meet hourly constraints (max 2 jobs/hour during daytime):")
        report_lines.append("")
        for job_id, new_schedule in schedule_suggestions.items():
            job = next((j for j in jobs if j['id'] == job_id), None)
            if job:
                report_lines.append(f"- **{job['name']}** (ID: {job['job_id']})")
                report_lines.append(f"  - Current schedule: `{job['schedule']}`")
                report_lines.append(f"  - Suggested schedule: `{new_schedule}`")
                report_lines.append("")
    else:
        report_lines.append("No schedule optimizations suggested (either no conflicts found or no jobs with simple daily schedules).")
        report_lines.append("")
    
    # Summary and recommendations
    report_lines.append("## Summary")
    report_lines.append(f"- Total jobs audited: {len(jobs)}")
    report_lines.append(f"- Erroring jobs: {len(erroring_jobs)}")
    report_lines.append(f"- Stalled/incomplete jobs: {len(stalled_jobs)}")
    report_lines.append(f"- Overlapping schedule groups: {len(overlapping_groups)}")
    report_lines.append(f"- Paused jobs: {len(paused_jobs)}")
    report_lines.append(f"- Stale one-shot jobs: {len(stale_one_shots)}")
    report_lines.append(f"- Stale recurring jobs: {len(stale_recurring_jobs)}")
    report_lines.append(f"- Health score: {health_score}/100")
    report_lines.append("")
    
    # Health score interpretation
    if health_score >= 90:
        report_lines.append("**Health Status:** Excellent 🟢")
    elif health_score >= 70:
        report_lines.append("**Health Status:** Good 🟡")
    elif health_score >= 50:
        report_lines.append("**Health Status:** Fair 🟠")
    else:
        report_lines.append("**Health Status:** Poor 🔴")
    
    return "\n".join(report_lines)


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description='Perform cron fleet audit')
    parser.add_argument(
        '--input', '-i',
        type=str,
        help='Path to JSON file containing cron job data (if not provided, reads from stdin)'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Path to write markdown report (if not provided, prints to stdout)'
    )
    parser.add_argument(
        '--session-data', '-s',
        type=str,
        help='Path to JSON file containing session data for stalled job detection (job_id -> session info)'
    )
    
    args = parser.parse_args()
    
    # Load job data
    if args.input:
        with open(args.input, 'r') as f:
            json_data = f.read()
    else:
        json_data = sys.stdin.read()
    
    jobs = load_jobs(json_data)
    
    # Load session data if provided
    session_data = None
    if args.session_data:
        with open(args.session_data, 'r') as f:
            session_data = json.load(f)
    
    # Perform audit checks
    erroring_jobs = check_erroring_jobs(jobs)
    overlapping_groups = check_overlapping_schedules(jobs)
    paused_jobs = check_paused_jobs(jobs)
    stale_one_shots = check_stale_one_shots(jobs)
    stale_recurring_jobs = check_stale_recurring_jobs(jobs)
    stalled_jobs = check_stalled_jobs(jobs, session_data)
    schedule_suggestions = suggest_new_schedules(jobs)
    health_score = calculate_health_score(erroring_jobs, overlapping_groups, paused_jobs, stale_one_shots, stale_recurring_jobs, stalled_jobs)
    
    # Generate report
    report = generate_report(jobs, erroring_jobs, overlapping_groups, paused_jobs, stale_one_shots, stale_recurring_jobs, stalled_jobs, schedule_suggestions, health_score)
    
    # Output report
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report written to {args.output}")
    else:
        print(report)


if __name__ == '__main__':
    main()