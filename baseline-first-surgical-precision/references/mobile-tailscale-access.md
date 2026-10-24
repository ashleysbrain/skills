# Mobile Tailscale Access to Local Servers

## The Problem
Local dev servers started with `python -m http.server` or `uvicorn` often bind to `localhost` or `127.0.0.1` only. This means Tailscale-connected mobile devices cannot reach them. The page loads as a white screen or fails silently.

## The Fix
Always bind servers to `0.0.0.0` (all interfaces) when they need to be reachable from Tailscale.

### Python http.server
```bash
# WRONG (localhost only):
python3 -m http.server 8304

# RIGHT (all interfaces including Tailscale):
python3 -m http.server 8304 --bind 0.0.0.0
```

### Python http.server with chdir
```python
import http.server, socketserver, os
os.chdir('/path/to/html')
handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(('0.0.0.0', 8304), handler) as httpd:
    httpd.serve_forever()
```

### Uvicorn / FastAPI servers
```bash
# WRONG:
uvicorn src.api.server:app --host 127.0.0.1 --port 8010

# RIGHT:
uvicorn src.api.server:app --host 0.0.0.0 --port 8010
```

## Verification
1. Get the Tailscale IP: `tailscale ip` (returns IPv4 like `100.107.113.11`)
2. Test from the machine: `curl http://100.107.113.11:PORT/path`
3. Test from phone: open `http://100.107.113.11:PORT/path` in Safari

## IPv6 Gotcha
Python's http.server defaults to IPv6 (`*` wildcard on IPv6) when no bind address is specified. This can cause Tailscale (which uses IPv4) to fail. Always specify `--bind 0.0.0.0` to force IPv4.

## Killing Stale Servers
When a port is already in use by a stale process:
```bash
lsof -i :PORT
kill -9 PID
lsof -i :PORT
```

## HTML JavaScript URL Bug Pattern
When building HTML that makes API calls from a phone, ensure the JavaScript API URL uses the correct Tailscale IP. A common bug: the HTML hardcodes `http://100.0.0.1:PORT` (wrong placeholder) instead of the actual Tailscale IP. The page loads fine but API calls fail silently on mobile while working on desktop.
