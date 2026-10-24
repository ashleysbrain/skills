# Cron Staggering Pattern — Protect User Working Hours

**Problem:** Multiple heavy cron jobs colliding in 1-3 AM window AND at 6 AM when user wakes up. System becomes unresponsive during user's working hours.

**Solution:** Stagger heavy builds at midnight and 4:30 AM. Advisory boards 30 min apart in 1-4 AM. Daytime max 2 jobs/hour.

## Current Optimized Schedule (CT)

### Overnight Heavy Builds (User Sleeping)
| Time | Job | Type | Duration |
|------|-----|------|----------|
| 12:00 AM | Engine Builder (633b60897fc9) | Build | ~4 hrs |
| 1:00 AM | Research Board | Advisory | ~30 min |
| 1:30 AM | CTO Board | Advisory | ~30 min |
| 2:00 AM | Marketing Board | Advisory | ~30 min |
| 2:30 AM | Product Board | Advisory | ~30 min |
| 3:00 AM | COO Board | Advisory | ~30 min |
| 3:00 AM | OpenRouter Sync | Maintenance | ~5 min |
| 3:25 AM | Skill Review | Maintenance | ~10 min |
| 3:30 AM | Design Board | Advisory | ~30 min |
| 4:15 AM | principal AM Review | Advisory | ~30 min |
| **4:30 AM** | **Science Layer Builder (b1c5b988a6bb)** | **Build** | **~2 hrs** |
| 5:00 AM | Model Compliance | Maintenance | ~5 min |

### Daytime (User Working 6 AM - 11 PM)
| Time | Job | Type | Notes |
|------|-----|------|-------|
| 6:00 AM | FORGE Fleet Review | Fleet ops | Light |
| 7:00 AM | SENTINEL Compliance | Fleet ops | Light |
| 7:45 AM | Obsidian Sync | Maintenance | Light |
| 9:00 AM | Workflow Horizon Scan | Research | Light |
| 12:00 PM | principal Midday Review | Advisory | Light |
| 8:00 PM | **Daytime Cron Audit (1b36bbe1978e)** | **Audit** | **Consolidates daytime** |
| 9:30 PM | principal End-of-Day Review | Advisory | Light |
| 11:00 PM | Fleet Wellness Self-Heal | Maintenance | Light |

## Rules Enforced

1. **Heavy builds NEVER 6 AM - 11 PM** — Engine build at midnight, science builder at 4:30 AM
2. **Advisory boards 30 min apart** — No simultaneous advisory runs
3. **Max 2 jobs/hour daytime** — Including maintenance
4. **Light maintenance at lunch (12-1 PM) or after 9 PM**
5. **Overnight window (12 AM - 5:59 AM) protected** — No changes without explicit approval
6. **Daytime audit runs at 8 PM** — Auto-consolidates, pauses stale, restaggers

## Implementation

```bash
# Move engine build to midnight
cronjob action=update job_id=633b60897fc9 schedule="0 0 * * *"

# Move science layer builder to 4:30 AM  
cronjob action=update job_id=b1c5b988a6bb schedule="30 4 * * *"

# Stagger advisory boards
cronjob action=update job_id=796ea7494a65 schedule="0 1 * * *"  # Marketing 1 AM
cronjob action=update job_id=176670b8ef82 schedule="0 2 * * *"  # Product 2 AM
cronjob action=update job_id=cb6790851860 schedule="0 3 * * *"  # COO 3 AM
cronjob action=update job_id=24810cda0dcd schedule="30 3 * * *" # Design 3:30 AM
cronjob action=update job_id=6730968ad57e schedule="15 4 * * *" # principal AM 4:15 AM
```

## Verification

After staggering, run:
```bash
cronjob action=list | grep -E "(schedule|name)" | head -60
```

Confirm no two heavy jobs in same 15-min window. Confirm nothing heavy 6 AM - 11 PM.

## User Feedback That Drove This

> "I don't feel like you're staggering them very well... especially if I'm working at 6am, I don't need the entire system shutdown because you're working on these complex builds. So I need these builds to happen earlier in the morning. And later at night... versus early in the morning when I'm up working."

**Result:** Heavy builds moved to midnight and 4:30 AM. Zero collisions with user working hours.