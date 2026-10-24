# Phase 2 Backend Build Pattern: 25 Endpoints in One Session

How to rapidly build, test, and verify a large batch of API endpoints with
shared DB tables. This pattern was used to build all 10 Phase 2 writing
pipeline features (MT9-MT18) in a single session.

## The Pattern

### Step 1: DB Init Function (runs once at import time)

Create a `_p2_init()` function that creates ALL tables upfront. Call it
immediately after definition (module-level, not inside a route). This ensures
tables exist before any request arrives.

```python
def _p2_db():
    _db_path = WORKSPACE / "writing-studio" / "drafts.db"
    _db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(_db_path))
    conn.row_factory = sqlite3.Row
    return conn

def _p2_init():
    conn = _p2_db()
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS revision_findings (...)")
    c.execute("CREATE TABLE IF NOT EXISTS dialectical_records (...)")
    # ... all tables
    conn.commit()
    conn.close()

_p2_init()  # Run at import time
```

**Pitfall:** Do NOT reference `DB_PATH` as a global unless it's defined at
module level. The existing pipeline_api.py uses `WORKSPACE / "writing-studio" /
"drafts.db"` pattern. Match it.

### Step 2: Shared Helpers

```python
def _uid():
    return hashlib.md5(f"{datetime.now(timezone.utc).isoformat()}".encode()).hexdigest()[:12]

def _now():
    return datetime.now(timezone.utc).isoformat()
```

### Step 3: Batch Endpoint Registration

Write ALL routes before the `if __name__ == "__main__"` block. Each feature
gets: a GET (list/retrieve), POST (create), and PATCH (update). Group them
with comment headers for navigability.

### Step 4: Install Missing Dependencies

Before restarting the server, check if new imports need installation:
```bash
<agent-home>/hermes-agent/venv/bin/pip install sse-starlette matplotlib -q
```

### Step 5: Automated Endpoint Testing

Use a Python script (via execute_code) that hits every endpoint with curl and
checks the JSON response. This is faster than testing manually and catches
syntax errors, missing tables, and route conflicts immediately.

```python
def test(name, method, path, body=None):
    cmd = ["curl", "-s", "-X", method, f"{BASE}{path}", "-H", AUTH, "-H", "Content-Type: application/json"]
    if body: cmd += ["-d", json.dumps(body)]
    r = subprocess.check_output(cmd, text=True, timeout=10)
    d = json.loads(r)
    results[name] = "PASS" if not d.get("error") else f"FAIL"
```

**Pitfall:** matplotlib import is slow on first run (font cache build). The
figure generation endpoint may time out on the first call. Increase the curl
timeout to 30s for that endpoint, or pre-import matplotlib at server startup.

### Step 6: Restart Server and Verify

```bash
PID=$(lsof -i :port -t | head -1) && kill $PID && sleep 2
<agent-home>/hermes-agent/venv/bin/python3 -B pipeline_api.py --port 8310 &
sleep 4
curl -s -o /dev/null -w '%{http_code}' http://localhost:port/
```

## Table Schema Patterns

### Progressive Disclosure (MT9 Revision Findings)

Findings have levels (1=discourse, 2=paragraph, 3=sentence). Levels unlock
sequentially — Level 2 only shows when Level 1 is 50%+ resolved. Max 7 findings
visible at once (Sweller cognitive load limit). Cognitive load indicator
(green/yellow/red) based on unresolved count.

### Structured Dissent (MT10 Dialectical Records)

Objection types: objection, confusion, gap, alternative, question
Response types: conceded, defended, deferred, escalated
Bastani trigger: 3+ defended objections on the same claim triggers cognitive
checkpoint for both authors.

### Figure Generation (MT13)

Generates PNG + source data CSV + generation code as a bound triple.
Weissgerber rules enforced: no dual-axis, raw data shown, colorblind-safe palette.
Uses DS brand colors (#c9a96e gold, #3d8b8b teal, #0a0c12 dark surface).

## Common Pitfalls

1. **NameError: DB_PATH** — The existing pipeline_api.py does not define
   `DB_PATH` as a global. Use `WORKSPACE / "writing-studio" / "drafts.db"`.
2. **sse-starlette not installed** — SSE streaming requires `pip install
   sse-starlette`. Install before restarting server.
3. **matplotlib timeout on first call** — Font cache build takes 10-15s on
   first import. Either pre-import at startup or increase client timeout.
4. **Typo in variable name** — When writing 600+ lines in one patch, check
   variable name consistency. `weissberber_ok` vs `weissgerber_ok` caused a
   silent failure that only surfaced in endpoint testing.
