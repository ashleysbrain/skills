# Pydantic Optional[Dict] Bug Pattern

## The Bug
In FastAPI request models, when a field is `Optional[Dict] = None`, omitting the field in the request makes it `None` — not an empty dict `{}`.

```python
# Request model
class SessionCreate(BaseModel):
    user_id: str
    mode: str = "one_off"
    dimensions: Optional[Dict] = None  # ← None when omitted!

# Handler code (CRASHES)
def start_session(self, user_id: str, mode: str = "one_off",
                  dimensions: Optional[Dict] = None) -> CoachingSession:
    for dim in DIMENSIONS:
        session.dimensions[dim] = dimensions.get(dim, {...})  # AttributeError: 'NoneType' has no attribute 'get'
```

**Error:** `AttributeError: 'NoneType' object has no attribute 'get'`

## The Fix
```python
def start_session(self, user_id: str, mode: str = "one_off",
                  dimensions: Optional[Dict] = None) -> CoachingSession:
    dims = dimensions or {}  # ← Normalize None to empty dict
    for dim in DIMENSIONS:
        session.dimensions[dim] = dims.get(dim, {...})
```

## Test to Verify Fix
```bash
# Request WITHOUT dimensions field
curl -X POST http://localhost:port/v1/sessions \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","mode":"one_off"}'

# Should return 200 with session_id, not 500 Internal Server Error
```

## General Rule
**Always normalize `Optional[Dict]` / `Optional[List]` to empty container before using `.get()` / `.append()` / iteration.**

```python
# Pattern for any optional collection
def handler(items: Optional[List] = None):
    items = items or []  # Normalize
    for item in items:   # Safe
        ...

def handler(config: Optional[Dict] = None):
    config = config or {}  # Normalize
    value = config.get("key")  # Safe
```

## Related: FastAPI Optional Fields
- `Optional[str] = None` → `None` when omitted ✓ (strings don't have `.get()`)
- `Optional[int] = None` → `None` when omitted ✓
- `Optional[Dict] = None` → `None` when omitted ✗ (crashes on `.get()`)
- `Optional[List] = None` → `None` when omitted ✗ (crashes on iteration)
- `List = []` (default factory) → `[]` when omitted ✓ (but mutable default warning)
- `Dict = {}` (default factory) → `{}` when omitted ✓ (but mutable default warning)

**Best practice:** Use `Optional[Dict] = None` + `config = config or {}` pattern. Explicit, no mutable default issues.