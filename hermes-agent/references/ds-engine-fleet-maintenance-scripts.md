# the specialist engine Maintenance Scripts

## fix_layer4_final.py
Automates the Layer 4 methodology mounting fix for DS engines.
- Finds and relocates the mount_methodology_endpoints block
- Moves it AFTER app = FastAPI(...) creation
- Preserves __future__ imports at top of file
- Validates syntax after changes
- Processes all 22 engines requiring fixes

Usage: `python3 fix_layer4_final.py`

## restart_and_verify.py
Restarts engines and verifies Layer 4 endpoints return populated data.
- Kills existing processes on engine ports
- Starts each engine from its directory
- Waits for startup
- Verifies /v1/layers returns institutions > 0
- Reports results for each engine

Usage: `python3 restart_and_verify.py`

## Individual Engine Fix Template
For manual fixing of a single engine:

```bash
# 1. Backup
cp src/api/server.py src/api/server.py.bak

# 2. Edit server.py to move mount block after app creation
#    (see references/ds-engine-fleet-maintenance.md for pattern)

# 3. Verify syntax
python3 -c "compile(open('src/api/server.py').read(), 'src/api/server.py', 'exec')"

# 4. Restart engine
lsof -ti :<PORT> | xargs kill -9 2>/dev/null || true
cd <ENGINE_DIR>
source venv/bin/activate 2>/dev/null
nohup python -m uvicorn src.api.server:app --host 127.0.0.1 --port <PORT> > /dev/null 2>&1 &
cd ..

# 5. Verify
curl -s -m 5 http://127.0.0.1:<PORT>/v1/layers | python3 -c "import sys,json; d=json.load(sys.stdin); l4=d.get('layer_4',{}); print(f'inst={l4.get(\"institutions\",0)}')"
```