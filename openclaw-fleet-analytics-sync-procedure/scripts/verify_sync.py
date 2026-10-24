#!/usr/bin/env python3
"""
Script to verify fleet analytics sync and generate summary.
Queries agents.db for sync statistics.
"""

import sqlite3
import os
from datetime import datetime, timedelta

def get_db_connection():
    db_path = os.path.expanduser("~/.sibling-agent/workspace/intel/agents/database/agents.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def main():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Total cron jobs
    c.execute("SELECT COUNT(*) FROM cron_jobs")
    total_cron_jobs = c.fetchone()[0]
    
    # Status distribution
    c.execute("SELECT status, COUNT(*) as count FROM cron_jobs GROUP BY status")
    status_dist = {row['status']: row['count'] for row in c.fetchall()}
    
    # Enabled vs error vs disabled (using enabled column and status)
    c.execute("SELECT enabled, COUNT(*) as count FROM cron_jobs GROUP BY enabled")
    enabled_dist = {row['enabled']: row['count'] for row in c.fetchall()}
    enabled_count = enabled_dist.get(1, 0)
    disabled_count = enabled_dist.get(0, 0)
    
    # Error count from status='error'
    error_count = status_dist.get('error', 0)
    
    # Top 5 errors in last 24 hours
    yesterday = (datetime.now() - timedelta(days=1)).isoformat()
    c.execute("""
        SELECT error_type, error_message, COUNT(*) as count
        FROM cron_runs
        WHERE datetime(ended_at) >= ?
          AND (status='error' OR error_type IS NOT NULL)
        GROUP BY error_type, error_message
        ORDER BY count DESC
        LIMIT 5
    """, (yesterday,))
    top_errors = c.fetchall()
    
    # Model distribution (enabled jobs)
    c.execute("""
        SELECT model, COUNT(*) as count
        FROM cron_jobs
        WHERE enabled = 1
        GROUP BY model
        ORDER BY count DESC
    """)
    model_dist = c.fetchall()
    
    # Journal compliance: agents with entries today
    today = datetime.now().date().isoformat()
    c.execute("SELECT COUNT(DISTINCT agent_id) FROM journal_entries WHERE entry_date = ?", (today,))
    journal_agents_today = c.fetchone()[0]
    
    # Active agents
    c.execute("SELECT COUNT(*) FROM agents WHERE status='active'")
    active_agents = c.fetchone()[0]
    
    journal_compliance_pct = (journal_agents_today / active_agents * 100) if active_agents > 0 else 0
    
    # Print summary
    print("=== Fleet Analytics Sync Summary ===")
    print(f"Total Cron Jobs: {total_cron_jobs}")
    print(f"Enabled: {enabled_count}")
    print(f"Error: {error_count}")
    print(f"Disabled: {disabled_count}")
    print("\nStatus Distribution:")
    for status, count in status_dist.items():
        print(f"  {status}: {count}")
    
    print("\nTop 5 Errors (Last 24h):")
    if top_errors:
        for err in top_errors:
            print(f"  {err['error_type']}: {err['error_message']} ({err['count']})")
    else:
        print("  No errors in last 24 hours")
    
    print("\nModel Distribution (Enabled Jobs):")
    for model, count in model_dist:
        print(f"  {model}: {count}")
    
    print(f"\nJournal Compliance: {journal_compliance_pct:.1f}%")
    print(f"  Agents with journals today: {journal_agents_today} / {active_agents}")
    
    conn.close()

if __name__ == "__main__":
    main()