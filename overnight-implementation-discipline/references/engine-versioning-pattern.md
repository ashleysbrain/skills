# Engine Versioning & Release Pattern

## the specialist engine Engine v2.0.0 Release (2026-06-11)

### Files Created/Modified
1. `VERSION.md` — Release notes with: what's new, test status, breaking changes, migration notes, next version plans
2. `git tag -a v2.0.0 -m "..."` — Annotated tag with full release description
3. `src/server/api.py` — Updated `version="2.0.0"` and health endpoint string

### Verification Steps
```bash
# 1. Check VERSION.md exists and has content
cat VERSION.md

# 2. Verify git tag
git tag -l v2.0.0
git show v2.0.0

# 3. Verify server version string
curl -s http://localhost:port/health | jq .engine
# Should output: "the specialist engine Engine v2.0.0"

# 4. Run full test suite
pytest tests/ -v
# Should show: 16 passed

# 5. Integration smoke test
curl -X POST http://localhost:port/v1/sessions -H "Content-Type: application/json" -d '{"user_id":"test","mode":"one_off"}'
```

### Template for Future Versions
```markdown
# the specialist engine Engine — Version X.Y.Z

**Release Date:** YYYY-MM-DD
**Codename:** <name>
**Status:** Production Ready / Beta / Alpha

## What's New in V<X>

### Core Changes
- ...

### Test Status
```
Wave Engine:        XX/XX tests passing
the specialist engine (Lattice): XX/XX tests passing  
Self-Healing:        XX/XX tests passing
```

## Breaking Changes from V<X-1>
- ...

## Migration Notes
- ...

## Next: V<X+1> (Planned)
- ...
```

### Anti-Pattern: Don't Skip Versioning
- ❌ "Just push the code, it works"
- ✅ VERSION.md + git tag + server string = auditable deployment

---

## Related: Private Repo Sync Pattern

When engine procedures update, sync to all private panel repos:
```bash
PRODUCT="/path/to/ds-wave-coaching-engine"
for d in /path/to/ds-wave-*-private; do
  cp "$PRODUCT/PROCESS.md" "$d/"
  cp "$PRODUCT/INTEGRATION.md" "$d/"
  cp "$PRODUCT/ARCHITECTURE.md" "$d/"
  cp "$PRODUCT/PERSONALITIES.md" "$d/"
  cp "$PRODUCT/PHYSICS_FIDELITY_REPORT.md" "$d/"
  cp "$PRODUCT/PRODUCT_THESIS_V1_LOCKED.md" "$d/"
  cp "$PRODUCT/COACHING_CONTEXT.md" "$d/PRODUCT_COACHING_CONTEXT.md"
  # Update manifest.yaml timestamp
  NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  sed -i '' "s/last_synced:.*/last_synced: $NOW/" "$d/manifest.yaml" 2>/dev/null || echo "last_synced: $NOW" >> "$d/manifest.yaml"
done
```