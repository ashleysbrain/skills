# Common Cron Issues and Solutions

This document provides a reference for common issues encountered in cron fleets and their typical solutions.

## Issue Categories

### 1. Execution Failures

#### deepseek-r1 Context Limit Crashes on Heavy Prompts
**Symptom**: Advisory panel or multi-step synthesis jobs show `last_status: "error"` for days/weeks while other deepseek-r1 jobs run fine.
**Root Cause**: `deepseek/deepseek-r1:free` has a context window that gets exhausted by large advisory panel prompts (multi-board synthesis, cascading recommendations, long system prompts). The model truncates or errors mid-generation. This is NOT an intermittent failure — it persists every run until the model is changed.
**Fix**: Switch the job to `nvidia/nemotron-3-super-120b-a12b:free` which handles larger payloads. Update via:
```
hermes cron update <job_id> --model "nvidia/nemotron-3-super-120b-a12b:free"
```
**Observed In The Wild**: Design Advisory Board dead since June 12, Legal Advisory Panel dead since June 9 — both fixed by switching from deepseek-r1 to nemotron.
**Detection Pattern**: Any job with `last_status: "error"` + `model: "deepseek/deepseek-r1:free"` + a prompt that involves multi-board synthesis or cascading analysis is a candidate for this fix.

#### Symptom: Jobs consistently exit with error codes
**Common Causes:**
- Missing dependencies or environment variables
- Path issues (using relative paths instead of absolute)
- Permission problems
- External service downtime or API changes

**Solutions:**
- Use absolute paths for all commands and file references
- Explicitly set required environment variables in the job definition
- Add error checking and logging to scripts
- Implement retry logic for transient external failures
- Use wrapper scripts that set up the environment properly

#### Symptom: Jobs intermittently fail
**Common Causes:**
- Race conditions with other processes
- Resource exhaustion (memory, disk space, file descriptors)
- Network blips or temporary service outages

**Solutions:**
- Add lock files to prevent concurrent execution
- Monitor resource usage and add cleanup routines
- Implement exponential backoff for retries
- Add health checks for dependencies before proceeding

### 2. Scheduling Issues
#### Symptom: Jobs running too frequently or not frequently enough
**Common Causes:**
- Misunderstanding cron syntax (especially step values and ranges)
- Confusion between different cron implementations
- Daylight saving time transitions causing unexpected behavior

**Solutions:**
- Use cron expression testing tools to verify schedules
- Be explicit about time zones if your cron implementation supports it
- Consider using seconds-based schedulers for sub-minute precision needs
- Document the intended frequency in job comments

#### Symptom: Jobs running at unexpected times
**Common Causes:**
- System clock changes (NTP adjustments, manual changes)
- Timezone confusion between server and job expectations
- Daylight saving time transitions

**Solutions:**
- Monitor system clock stability
- Use UTC for all cron jobs if possible to avoid DST issues
- Clearly document timezone assumptions in job definitions

### 3. Resource Contention
#### Symptom: Jobs slowing down or failing when they overlap
**Common Causes:**
- Multiple jobs trying to access the same resource (file, database, API)
- Insufficient system resources (CPU, memory, I/O)
- Lock contention or deadlocks

**Solutions:**
- Stagger schedules to avoid overlaps (use the overlap detection feature)
- Implement proper locking mechanisms for shared resources
- Add resource usage monitoring and alerting
- Consider queuing systems for high-contention resources
- Optimize individual job performance to reduce resource footprint

### 4. Monitoring and Visibility Issues
#### Symptom: Difficulty determining if jobs are running correctly
**Common Causes:**
- Lack of logging or inadequate log retention
- Alerts not configured or sent to wrong channels
- No central dashboard for job status

**Solutions:**
- Implement structured logging with appropriate log levels
- Set up alerts for job failures, long runtimes, or abnormal behavior
- Use a central job monitoring system or build a simple dashboard
- Regularly review job logs as part of operational procedures

### 5. Security Issues
#### Symptom: Jobs running with excessive privileges or exposing secrets
**Common Causes:**
- Running jobs as root when not necessary
- Hardcoding passwords or API keys in scripts
- Insufficient access controls on job definitions or logs

**Solutions:**
- Run jobs with the principle of least privilege
- Use secure secret management systems (environment variables from secure stores, etc.)
- Regularly audit job definitions and associated files for security issues
- Implement proper file permissions and access controls

### 6. Maintenance and Technical Debt
#### Symptom: Job definitions becoming outdated or difficult to manage
**Common Causes:**
- Lack of documentation or comments
- Inconsistent naming conventions
- Accumulation of unused or obsolete jobs
- Manual changes not tracked in version control

**Solutions:**
- Implement standardized job naming conventions
- Require documentation and comments for all jobs
- Regularly review and remove obsolete jobs
- Track job definitions in version control
- Implement job templates or generators for consistency

## Diagnostic Approach

When investigating cron issues, follow this structured approach:

1. **Identify the symptom**: What exactly is going wrong?
2. **Gather evidence**: Check logs, timestamps, system metrics
3. **Reproduce if possible**: Can you make the issue happen consistently?
4. **Isolate variables**: What changed recently? What's different about failing vs. succeeding instances?
5. **Form hypothesis**: What's the most likely cause based on the evidence?
6. **Test solution**: Implement a fix and verify it resolves the issue
7. **Monitor**: Watch for recurrence over an appropriate time period
8. **Document**: Record what was found and how it was fixed for future reference

## Quick Reference: Common Fixes by Symptom

| Symptom | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| Job never runs | Incorrect schedule syntax | Verify cron expression with tester |
| Job runs twice | Overlapping schedules or DST | Check for duplicates, consider UTC |
| Job fails immediately | Missing environment | Add env vars to job definition |
| Job fails after running a while | Resource leak | Check for unclosed handles, memory leaks |
| Job runs but doesn't do anything | Silent failure | Add logging and error checking |
| Job uses too much CPU | Inefficient algorithm | Profile and optimize critical sections |
| Job misses runs during DST | Timezone issues | Consider using UTC or robust scheduler |

## Prevention Strategies
- Implement job templates with built-in best practices
- Create onboarding documentation for new cron job creators
- Regularly audit the cron fleet (monthly or quarterly)
- Use automation to deploy and manage job definitions
- Establish clear ownership for each job or job category
- Implement health checks that run as cron jobs themselves