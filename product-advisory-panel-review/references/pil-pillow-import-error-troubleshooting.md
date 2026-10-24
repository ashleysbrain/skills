# PIL/Pillow Import Error Troubleshooting

## Symptom

When running the PDF generation script:
```bash
python3 /<workspace> /tmp/product-review-2026-07-15.md /tmp/product-review-2026-07-15.pdf "Product Advisory Panel" "AM"
```

Error occurs:
```
Traceback (most recent call last):
  File "/<workspace>", line 69, in <module>
    generate_pdf(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    ...
  from PIL.ImageCms import ImageCmsProfile
  File "/<workspace>", line 28, in <module>
    from . import Image
  File "/<workspace>", line 95, in <module>
    from . import _imaging as core
ImportError: cannot import name '_imaging' from 'PIL' (/<workspace>)
```

## Root Cause

Corrupted or incompatible Pillow installation in the the operator agent venv. The `_imaging` module is a compiled C extension that may not be properly built or may be mismatched with the Python version.

## Resolution (For Cron Runs)

Do NOT attempt to fix the environment during a cron run. The correct action is:

1. **Deliver markdown content directly** — The markdown report is the primary deliverable
2. **Note the failure briefly** — Add a footer line like `(PDF generation failed: PIL/_imaging import error)`
3. **Proceed without PDF** — PDF is a convenience format, not the core output

## Resolution (For Maintenance)

To fix this for future runs (outside of cron job execution):

```bash
# Reinstall Pillow in the the operator agent venv
source <agent-home>/hermes-agent/venv/bin/activate
pip uninstall Pillow -y
pip install Pillow
```

Or if that fails, reinstall the entire venv:
```bash
rm -rf <agent-home>/hermes-agent/venv
# the operator agent will recreate the venv on next command
```

## Context

First observed: July 15, 2026
Status: Environment issue, not code issue
Impact: PDF generation fails, but markdown content is still delivered