# Journal Compliance Calculation

Journal compliance percentage = (Number of distinct agents with a journal entry for today) / (Number of active agents) * 100

Where:
- Agent is considered active if status = 'active' in agents table.
- Journal entry date matches today's date in UTC (YYYY-MM-DD).
- Each agent only counted once regardless of number of entries.

If there are no active agents, compliance is 0%.

Improvements:
- Ensure agents are writing journals daily.
- Verify journal entries are being indexed correctly (see sync_journals() function).