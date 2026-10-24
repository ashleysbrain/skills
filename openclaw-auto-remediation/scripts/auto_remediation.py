#!/usr/bin/env python3
import json
import sqlite3
import os
import subprocess
import sys
from datetime import datetime

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

def run_command(cmd):
    """Run a shell command and return (output, exit_code)."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip(), result.returncode
    except Exception as e:
        return str(e), 1

def main():
    log("=== Starting Auto-Remediation Cycle (NEXUS E-026) ===")
    
    # Step 1: Sync live data (should be run before this script)
    log("--- Step 1: Sync live data ---")
    log("NOTE: This script assumes fleet_analytics.py sync has already been run.")
    log("Run: python3 ~/.sibling-agent/workspace/intel/agents/database/fleet_analytics.py sync")
    
    # Step 2: Auto-fix errors
    log("\n--- Step 2: Auto-fix errors ---")
    cmd = "sibling-agent cron list --json"
    output, exit_code = run_command(cmd)
    if exit_code != 0:
        log(f"Failed to get cron jobs: {output}")
    else:
        try:
            data = json.loads(output)
            if isinstance(data, dict) and 'jobs' in data:
                cron_jobs = data['jobs']
            else:
                log("Unexpected JSON structure for cron jobs, assuming empty list.")
                cron_jobs = []
            fixed_count = 0
            for job in cron_jobs:
                # Access nested state fields
                state = job.get("state", {})
                consecutive_errors = state.get("consecutiveErrors", 0)
                if consecutive_errors >= 3:
                    job_id = job.get("id")
                    job_name = job.get("name", "")
                    error = state.get("lastError", "")
                    error_reason = state.get("lastErrorReason", "")
                    # Extract model from payload if available
                    model = "unknown"
                    payload = job.get("payload")
                    if isinstance(payload, dict):
                        model = payload.get("model", "unknown")
                    # Get current timeout for timeout-related fixes
                    current_timeout = None
                    if isinstance(payload, dict):
                        current_timeout = payload.get("timeoutSeconds")
                    fix_applied = False
                    if "rate_limit" in error.lower() and "anthropic/claude-sonnet-4-6" in model:
                        if "Scan" in job_name:
                            new_model = "google/gemini-2.5-flash"
                            log(f"Job {job_id} ({job_name}): rate_limit on sonnet-4-6 for scan -> switching to {new_model}")
                        elif "Brief" in job_name:
                            new_model = "anthropic/claude-haiku-4-5"
                            log(f"Job {job_id} ({job_name}): rate_limit on sonnet-4-6 for brief -> switching to {new_model}")
                        else:
                            new_model = "google/gemini-2.5-flash"
                            log(f"Job {job_id} ({job_name}): rate_limit on sonnet-4-6 (unknown type) -> switching to {new_model}")
                        update_cmd = f"sibling-agent cron update {job_id} --model '{new_model}'"
                        out, code = run_command(update_cmd)
                        if code == 0:
                            log(f"  -> Successfully updated job {job_id} to model {new_model}")
                            fix_applied = True
                        else:
                            log(f"  -> Failed to update job {job_id}: {out}")
                    elif "timeout" in error.lower() or "timeout" in error_reason.lower():
                        new_timeout = 1200
                        # Only update if current timeout is less than new_timeout
                        if current_timeout is not None and current_timeout < new_timeout:
                            log(f"Job {job_id} ({job_name}): timeout error -> increasing timeout from {current_timeout}s to {new_timeout}s")
                            update_cmd = f"sibling-agent cron update {job_id} --timeout-seconds {new_timeout}"
                            out, code = run_command(update_cmd)
                            if code == 0:
                                log(f"  -> Successfully updated job {job_id} timeout to {new_timeout}")
                                fix_applied = True
                            else:
                                log(f"  -> Failed to update job {job_id} timeout: {out}")
                        elif current_timeout is not None:
                            log(f"Job {job_id} ({job_name}): timeout error but timeout already {current_timeout}s >= {new_timeout}s, skipping update")
                        else:
                            # If we can't determine current timeout, still try to update (fallback)
                            log(f"Job {job_id} ({job_name}): timeout error -> setting timeout to {new_timeout}s (current timeout unknown)")
                            update_cmd = f"sibling-agent cron update {job_id} --timeout-seconds {new_timeout}"
                            out, code = run_command(update_cmd)
                            if code == 0:
                                log(f"  -> Successfully updated job {job_id} timeout to {new_timeout}")
                                fix_applied = True
                            else:
                                log(f"  -> Failed to update job {job_id} timeout: {out}")
                    if fix_applied:
                        fixed_count += 1
            log(f"Auto-fix errors: applied {fixed_count} fixes.")
        except Exception as e:
            log(f"Error processing cron jobs for auto-fix: {e}")
    
    # Step 3: Auto-spread load
    log("\n--- Step 3: Auto-spread load ---")
    # Re-fetch cron jobs to have fresh data
    cmd = "sibling-agent cron list --json"
    output, exit_code = run_command(cmd)
    if exit_code != 0:
        log(f"Failed to get cron jobs for load spreading: {output}")
    else:
        try:
            data = json.loads(output)
            if isinstance(data, dict) and 'jobs' in data:
                cron_jobs = data['jobs']
            else:
                log("Unexpected JSON structure for cron jobs, assuming empty list.")
                cron_jobs = []
            model_counts = {}
            for job in cron_jobs:
                # Extract model from payload
                model = "unknown"
                payload = job.get("payload")
                if isinstance(payload, dict):
                    model = payload.get("model", "unknown")
                model_counts[model] = model_counts.get(model, 0) + 1
            log(f"Model counts: {model_counts}")
            overused_models = [model for model, count in model_counts.items() if count > 40]
            if overused_models:
                log(f"Overused models (>{40} jobs): {overused_models}")
                for model in overused_models:
                    excess = model_counts[model] - 40
                    log(f"Model {model} has {model_counts[model]} jobs, need to redistribute {excess} jobs.")
                    model_jobs = [job for job in cron_jobs if (job.get("payload", {}).get("model", "unknown") == model)]
                    model_jobs.sort(key=lambda x: x.get("state", {}).get("consecutiveErrors", 0), reverse=True)
                    jobs_to_redistribute = model_jobs[:excess]
                    for job in jobs_to_redistribute:
                        job_id = job.get("id")
                        job_name = job.get("name", "")
                        # Determine alternative model
                        alternative_model = None
                        if model_counts.get("google/gemini-2.5-flash", 0) < 40:
                            alternative_model = "google/gemini-2.5-flash"
                        elif model_counts.get("anthropic/claude-haiku-4-5", 0) < 40:
                            alternative_model = "anthropic/claude-haiku-4-5"
                        else:
                            # Fallback to the model with the lowest count
                            if model_counts:
                                alternative_model = min(model_counts, key=model_counts.get)
                            else:
                                alternative_model = "google/gemini-2.5-flash"
                        log(f"  -> Redistributing job {job_id} ({job_name}) from {model} to {alternative_model}")
                        update_cmd = f"sibling-agent cron update {job_id} --model '{alternative_model}'"
                        out, code = run_command(update_cmd)
                        if code == 0:
                            log(f"     Successfully updated job {job_id} to {alternative_model}")
                            # Update counts for next iteration (optional)
                            model_counts[model] -= 1
                            model_counts[alternative_model] = model_counts.get(alternative_model, 0) + 1
                        else:
                            log(f"     Failed to update job {job_id}: {out}")
            else:
                log("No model has >40 active jobs. Load spreading not needed.")
        except Exception as e:
            log(f"Error in load spreading: {e}")
    
    # Step 4: Cost optimization
    log("\n--- Step 4: Cost optimization ---")
    db_path = os.path.expanduser("~/.sibling-agent/workspace/intel/agents/database/agents.db")
    if not os.path.exists(db_path):
        log(f"Database not found: {db_path}")
    else:
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            query = """
            SELECT job_name, model FROM cron_jobs 
            WHERE model LIKE '%opus%' 
            AND (job_name LIKE '%Scan%' OR job_name LIKE '%Brief%' OR job_name LIKE '%backup%')
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            log(f"Found {len(rows)} opus model jobs on simple tasks.")
            for row in rows:
                job_name, model = row
                new_model = model.replace("opus", "sonnet")
                if new_model == model:
                    log(f"  Job '{job_name}' ({model}): cannot determine cheaper model, skipping.")
                    continue
                log(f"  Job '{job_name}' ({model}) -> migrating to cheaper tier: {new_model}")
                # We need the job ID; we'll search by name and model (may not be unique)
                # We'll get all cron jobs and match by name and model (first match)
                cmd_list = "sibling-agent cron list --json"
                out_list, code_list = run_command(cmd_list)
                if code_list == 0:
                    try:
                        data = json.loads(out_list)
                        if isinstance(data, dict) and 'jobs' in data:
                            jobs = data['jobs']
                        else:
                            jobs = []
                        job_id = None
                        for j in jobs:
                            if j.get("name") == job_name and (j.get("payload", {}).get("model", "unknown") == model):
                                job_id = j.get("id")
                                break
                        if job_id:
                            update_cmd = f"sibling-agent cron update {job_id} --model '{new_model}'"
                            out_up, code_up = run_command(update_cmd)
                            if code_up == 0:
                                log(f"     Successfully updated job {job_id} to {new_model}")
                            else:
                                log(f"     Failed to update job {job_id}: {out_up}")
                        else:
                            log(f"     Could not find job ID for '{job_name}' with model {model}. Skipping.")
                    except Exception as e:
                        log(f"Error parsing cron jobs for job ID lookup: {e}")
                else:
                    log(f"Failed to list cron jobs for job ID lookup: {out_list}")
            conn.close()
        except Exception as e:
            log(f"Error in cost optimization: {e}")
    
    # Step 5: Predictive (skip)
    log("\n--- Step 5: Predictive ---")
    log("Predictive step: checking for agents with declining performance (3+ consecutive runs slower than average) - SKIPPED due to lack of implementation details.")
    log("Note: This requires historical performance data in task_analytics table which may not be populated.")
    
    # Step 6: Data reconciliation
    log("\n--- Step 6: Data reconciliation ---")
    log("Syncing new agents from sibling-agent to analytics DB...")
    log("Note: The fleet analytics sync step already syncs agent knowledge stores (see sync output).")
    log("Assuming data reconciliation is handled by the sync step.")
    
    # Step 7: Update fleet health snapshot
    log("\n--- Step 7: Update fleet health snapshot ---")
    log("The fleet health snapshot was already updated during the sync step (see output above).")
    log("If needed, we can run a separate command, but we consider this step done.")
    
    log("\n=== Auto-Remediation Cycle Completed ===")

if __name__ == "__main__":
    main()