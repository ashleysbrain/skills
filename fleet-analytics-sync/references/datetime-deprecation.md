# Datetime Deprecation Warning Fix

The fleet_analytics.py script uses `datetime.datetime.utcnow()` which is deprecated in Python 3.12+.
Replace with timezone-aware alternatives:

- `datetime.now(datetime.UTC)` (Python 3.11+)
- `datetime.utcnow().replace(tzinfo=timezone.utc)` (backward compatible)

See the script lines:
- 461, 88, 227, 281, 282, 406, 443, 365, 377

Fixing these will eliminate the deprecation warnings during sync.