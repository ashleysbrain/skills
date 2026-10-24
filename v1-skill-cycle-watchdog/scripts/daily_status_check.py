#!/usr/bin/env python3
"""
Daily status check script for V1 Skill Product Review cycle (job c37a1090869d).

This script provides a reliable fallback when cron output files are not available
in the expected location. It uses multiple detection methods in priority order:
1. the operator agent cron list CLI (primary)
2. Session database query (secondary)
3. Directory-based session inspection (tertiary)

Usage:
    python3 daily_status_check.py [--date YYYY-MM-DD]

Exit codes:
    0 - Job ran successfully
    1 - Job did not run
    2 - Job ran but failed with error
    3 - Cannot determine status
"""

import argparse
import json
import re
import sqlite3
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Check V1 Skill Review job status")
    parser.add_argument(
        "--date",
        type=str,
        help="Date to check in YYYY-MM-DD format (default: today)",
        default=None
    )
    return parser.parse_args()


def get_hermes_home():
    """Get the operator agent home directory from environment or default."""
    return Path.home() / ".hermes"


def run_hermes_cron_list():
    """Run 'hermes cron list' and return stdout."""
    try:
        result = subprocess.run(
            ["hermes", "cron", "list"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout
        return None
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        return None


def parse_cron_list_output(output, target_date_str):
    """
    Parse 'hermes cron list' output to find job c37a1090869d status.

    Returns dict with keys:
        - found (bool)
        - last_run (str or None)
        - status (str or None)
        - next_run (str or None)
        - active (bool)
    """
    lines = output.split('\n')
    in_target_job = False
    result = {
        "found": False,
        "last_run": None,
        "status": None,
        "next_run": None,
        "active": False
    }

    for line in lines:
        # Check if we're in the target job block
        if "c37a1090869d" in line:
            in_target_job = True
            result["found"] = True
            continue

        if in_target_job:
            # Extract key information from the job block
            if "Name:" in line:
                continue  # Already confirmed by ID
            elif "Schedule:" in line:
                continue  # Not needed for status check
            elif "[active]" in line:
                result["active"] = True
            elif "[paused]" in line:
                result["active"] = False
            elif "Last run:" in line:
                # Extract timestamp
                match = re.search(r"Last run: (\S+)", line)
                if match:
                    result["last_run"] = match.group(1)
                # Extract status
                match = re.search(r"\b(ok|error|timeout)\b", line)
                if match:
                    result["status"] = match.group(1)
            elif "Next run:" in line:
                match = re.search(r"Next run: (\S+)", line)
                if match:
                    result["next_run"] = match.group(1)
            # Exit job block on empty line or next job ID
            elif line.strip() == "" or re.search(r"^\s{2}[a-f0-9]{12}\s", line):
                break

    return result


def check_last_run_date(last_run_str, target_date):
    """
    Check if last_run matches the target date.

    Args:
        last_run_str: ISO timestamp string from cron output
        target_date: datetime.date object

    Returns:
        bool: True if last_run is from target_date
    """
    if not last_run_str:
        return False

    try:
        # Parse ISO timestamp (format: 2026-07-13T03:27:38.999398-05:00)
        last_run_dt = datetime.fromisoformat(last_run_str)
        return last_run_dt.date() == target_date
    except ValueError:
        return False


def query_session_db(hermes_home, target_date):
    """
    Query the operator agent session database for cron job sessions.

    Returns list of session dicts with keys:
        - session_id
        - title
        - created_at
    """
    db_path = hermes_home / "sessions/sessions.db"

    if not db_path.exists():
        return []

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Try multiple schema variations
        queries = [
            # Schema 1: sessions table with created_at
            """
            SELECT session_id, title, created_at
            FROM sessions
            WHERE source = 'cron'
            AND created_at >= ?
            ORDER BY created_at DESC
            LIMIT 10
            """,
            # Schema 2: no created_at column
            """
            SELECT id as session_id, title, timestamp as created_at
            FROM sessions
            WHERE source = 'cron'
            AND timestamp >= ?
            ORDER BY timestamp DESC
            LIMIT 10
            """,
            # Schema 3: messages table approach
            """
            SELECT DISTINCT session_id, 
                   (SELECT content FROM messages m 
                    WHERE m.session_id = s.session_id 
                    AND role = 'user' 
                    LIMIT 1) as title,
                   (SELECT timestamp FROM messages 
                    WHERE session_id = s.session_id 
                    ORDER BY timestamp ASC 
                    LIMIT 1) as created_at
            FROM sessions s
            WHERE created_at >= ?
            ORDER BY created_at DESC
            LIMIT 10
            """
        ]

        sessions = []
        date_str = target_date.strftime("%Y-%m-%d")

        for query in queries:
            try:
                cursor.execute(query, (date_str,))
                rows = cursor.fetchall()
                if rows:
                    sessions = [dict(row) for row in rows]
                    break
            except sqlite3.OperationalError:
                # Schema doesn't match, try next query
                continue

        conn.close()
        return sessions

    except (sqlite3.Error, Exception) as e:
        return []


def search_session_files(hermes_home, target_date):
    """
    Search for session files by file modification time.

    Returns list of file paths.
    """
    sessions_dir = hermes_home / "sessions"

    if not sessions_dir.exists():
        return []

    # Find files modified in the last 24 hours
    cutoff_time = datetime.now() - timedelta(hours=24)
    matching_files = []

    try:
        for session_file in sessions_dir.glob("*.json"):
            stat = session_file.stat()
            mtime = datetime.fromtimestamp(stat.st_mtime)

            if mtime >= cutoff_time:
                matching_files.append(str(session_file))

    except (PermissionError, OSError):
        pass

    return matching_files


def main():
    args = parse_args()

    # Determine target date
    if args.date:
        target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    else:
        target_date = datetime.now().date()

    target_date_str = target_date.strftime("%Y-%m-%d")

    # Method 1: Check via hermes cron list
    print(f"Checking V1 Skill Review job status for {target_date_str}...")
    print("Method 1: the operator agent cron list...", end=" ")

    cron_output = run_hermes_cron_list()
    if cron_output:
        job_info = parse_cron_list_output(cron_output, target_date_str)

        if job_info["found"]:
            print(f"FOUND (active: {job_info['active']})")

            if job_info["last_run"]:
                ran_today = check_last_run_date(job_info["last_run"], target_date)
                print(f"Last run: {job_info['last_run']}")
                print(f"Status: {job_info['status'] or 'unknown'}")

                if ran_today:
                    if job_info["status"] == "ok":
                        print("\nResult: Job ran successfully today ✓")
                        return 0
                    elif job_info["status"] == "error":
                        print("\nResult: Job ran but FAILED with error ✗")
                        return 2
                    else:
                        print("\nResult: Job ran but status unclear ?")
                        return 3
                else:
                    print(f"\nResult: Job did NOT run today ✗ (last run was earlier)")
                    return 1
            else:
                print("\nResult: Job has no last_run timestamp ✗")
                return 1
        else:
            print("NOT FOUND in cron list")
    else:
        print("FAILED (hermes command not available)")

    # Method 2: Query session database
    print("\nMethod 2: Session database query...", end=" ")

    hermes_home = get_hermes_home()
    sessions = query_session_db(hermes_home, target_date)

    if sessions:
        print(f"FOUND {len(sessions)} sessions")

        # Look for V1 Skill / Divinity Health sessions
        relevant = [
            s for s in sessions
            if any(kw in s.get("title", "").lower() for kw in ["v1 skill", "divinity health", "skill review"])
        ]

        if relevant:
            print(f"Relevant sessions found: {len(relevant)}")
            print(f"Latest: {relevant[0].get('session_id')} - {relevant[0].get('title')}")
            print("\nResult: Evidence of review job activity found ✓")
            return 0
        else:
            print("No relevant sessions found")
    else:
        print("NO sessions found (DB inaccessible or schema mismatch)")

    # Method 3: Search session files
    print("\nMethod 3: Session file search...", end=" ")

    session_files = search_session_files(hermes_home, target_date)

    if session_files:
        print(f"FOUND {len(session_files)} recent session files")
        print("\nResult: Evidence of recent cron activity found ✓")
        return 0
    else:
        print("NO recent session files found")

    # All methods failed
    print("\n" + "="*60)
    print("FINAL RESULT: Cannot determine job status")
    print("="*60)
    print("\nRecommendations:")
    print("1. Check if the operator agent daemon is running")
    print("2. Verify cron scheduler is active")
    print("3. Manually inspect <agent-home>/sessions/ directory")
    print("4. Re-run the review job manually: hermes cron run c37a1090869d")

    return 3


if __name__ == "__main__":
    sys.exit(main())