# Fleet Analytics Script Deprecation Warnings

The fleet analytics sync script (`fleet_analytics.py`) may emit deprecation warnings similar to:

```
DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
```

These warnings do not affect the functionality of the script. The script continues to work correctly and produces the expected output.

The warnings are due to the use of `datetime.datetime.utcnow()` in several places in the script. While the script should eventually be updated to use the recommended timezone-aware approach, the current implementation is stable for operational use.

No action is required from users of the skill when these warnings appear.