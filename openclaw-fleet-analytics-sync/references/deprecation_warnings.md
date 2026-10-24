The fleet_analytics.py script produces deprecation warnings about datetime.utcnow() due to using deprecated methods.
These warnings are non-critical but indicate the script should be updated to use timezone-aware datetime objects for future compatibility.
See: https://docs.python.org/3/library/datetime.html#datetime.datetime.utcnow