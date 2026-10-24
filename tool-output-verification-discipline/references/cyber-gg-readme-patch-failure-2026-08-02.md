# Cyber the operator agent README Patch Failure — Real Example

**Date:** 2026-08-02  
**Context:** Making the principal-ready Cyber the operator agent organism  
**Issue:** README patches claimed success but didn't actually apply

## What happened

### Attempted change
```python
patch(
  mode="replace",
  path="README.md",
  old_string="# Cyber the operator agent\n\nA fresh physiomorphic organism...",
  new_string="# Cyber the operator agent\n\nA full the operator agent organism..."
)
```

### Tool response
```json
{"success": true, "diff": "..."}
```

### My report
"✅ README updated with the principal guides"

### User feedback
"go back through and ensure this was done. it shows this was not done??"

## Root cause

1. Patch tool reported `success: true`
2. I trusted the tool output
3. I did NOT read back README.md to verify
4. Actual file content was UNCHANGED

## What was missing

**Verification step I should have done:**
```python
patch(...)

# VERIFY
actual = read_file(path="README.md")
if "full the operator agent organism" in actual.content:
    print("✅ README verified")
else:
    print("❌ Patch failed - old_string mismatch")
    # Re-read to find correct context
    full_file = read_file(path="README.md", offset=1, limit=50)
```

## How I fixed it

1. Read back README.md to see actual content
2. Found the OLD content (not updated)
3. Re-read the file to find correct `old_string` context
4. Re-applied the patch with correct context
5. Read back AGAIN to verify
6. Then committed and pushed

## Key lessons

1. **Never trust tool success** - especially for `patch` operations
2. **Always read back** to verify the change is present
3. **Check for old content** that should be gone
4. **Use different method** than the one that made the change (read vs write)
5. **When user says "not done"** - this is a verification failure, not a user error

## Pattern to avoid

```python
# WRONG
write_file(path="file.md", content=new_content)
print("✅ File updated")
```

```python
# RIGHT
write_file(path="file.md", content=new_content)
verified = read_file(path="file.md")
assert "key phrase" in verified.content
print("✅ File verified")
```
