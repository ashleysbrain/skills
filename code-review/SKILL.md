---
name: code-review
description: Guidelines for performing thorough code reviews with security and quality focus
---

# Code Review Skill

Use this skill when reviewing code changes, pull requests, or auditing existing code.

## Review Checklist

### 1. Security First
- [ ] No hardcoded secrets, API keys, or credentials
- [ ] Input validation on all user-provided data
- [ ] SQL queries use parameterized statements (no string concatenation)
- [ ] File operations validate paths (no path traversal)
- [ ] Authentication/authorization checks present where needed

### 2. Error Handling
- [ ] All external calls (API, DB, file) have try/catch
- [ ] Errors are logged with context (but no sensitive data)
- [ ] User-facing errors are helpful but don't leak internals
- [ ] Resources are cleaned up in finally blocks or context managers

### 3. Code Quality
- [ ] Functions do one thing and are reasonably sized (<50 lines ideal)
- [ ] Variable names are descriptive (no single letters except loops)
- [ ] No commented-out code left behind
- [ ] Complex logic has explanatory comments
- [ ] No duplicate code (DRY principle)

### 4. Testing Considerations
- [ ] Edge cases handled (empty inputs, nulls, boundaries)
- [ ] Happy path and error paths both work
- [ ] New code has corresponding tests (if test suite exists)

## Review Response Format

When providing review feedback, structure it as:

```
## Summary
[1-2 sentence overall assessment]

## Critical Issues (Must Fix)
- Issue 1: [description + suggested fix]
- Issue 2: ...

## Suggestions (Nice to Have)
- Suggestion 1: [description]

## Questions
- [Any clarifying questions about intent]
```

## Common Patterns to Flag

### Python
```python
# Bad: SQL injection risk
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# Good: Parameterized query
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

### JavaScript
```javascript
// Bad: XSS risk
element.innerHTML = userInput;

// Good: Safe text content
element.textContent = userInput;
```

### Web App Data Contract Issues

When reviewing server + client code, check for mismatches in API contracts:

**Problem**: Server returns enum values but client expects different keys
```javascript
// Server returns: {"icon": "db", "icon": "pipeline", "icon": "monitor"}
// Client expects: {database: "...", cicd: "...", monitoring: "..."}

// Bug: Icons break in UI
var TYPE_ICONS = {
  database: '...',
  api: '...',
  cicd: '...',
  monitoring: '...',
  // Missing: db, pipeline, monitor
};
```

**Fix strategy**: Either add missing keys to client:
```javascript
var TYPE_ICONS = {
  database: '...',
  db: '<path d="..."/>',  // ADD
  api: '...',
  cicd: '...',
  pipeline: '<path d="..."/>',  // ADD
  monitoring: '...',
  monitor: '<path d="..."/>',  // ADD
};
```

Or change server to use client's canonical names.

**How to catch it**:
```bash
# Check server returns
grep -r "icon.*:" organism/server.py

# Check client expects
grep -A 10 "TYPE_ICONS" html/app.js
```

## Tone Guidelines

- Be constructive, not critical
- Explain *why* something is an issue, not just *what*
- Offer solutions, not just problems
- Acknowledge good patterns you see
