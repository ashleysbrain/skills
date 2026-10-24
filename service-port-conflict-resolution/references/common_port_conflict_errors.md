# Common Port Conflict Error Messages and Their Meanings

This reference documents typical error messages encountered when diagnosing port conflicts in the DS engine ecosystem, along with their likely causes and suggested investigations.

## Error Messages and Diagnosis

### 1. "Address already in use" (EADDRINUSE)
**Where it appears:** Engine logs, startup script output, or when attempting to bind a socket.
**Likely Cause:** 
- Another process is already bound to the target port.
- A previous instance of the same engine did not shut down cleanly and still holds the port.
- Two engines in the ecosystem are configured for the same port.
**Investigation Steps:**
- Run `sudo lsof -iTCP:<port> -sTCP:LISTEN -nP` to identify the occupying process.
- Check if the process is a legitimate engine instance or a leftover zombie.
- Verify port assignments in all engine configuration files.

### 2. "Connection refused" (ECONNREFUSED)
**Where it appears:** When a client (e.g., Scanner, Physician, or another engine) attempts to connect to an engine's expected port.
**Likely Cause:**
- The target engine is not running.
- The engine is bound to a different port than expected.
- Firewall or network policy is blocking the connection (less common in localhost).
**Investigation Steps:**
- Verify the target engine is running: `ps aux | grep <engine_name>` or check its startup logs.
- Confirm the engine's actual bound port: `sudo lsof -iTCP -sTCP:LISTEN -nP | grep <engine_name>`.
- Check the engine's configuration for correct port binding.
- Ensure the client is configured to connect to the correct port.

### 3. "Timeout" or "No response"
**Where it appears:** Health check curls or inter-engine communication attempts that hang or timeout.
**Likely Cause:**
- Engine is bound to the correct port but is overloaded or deadlocked.
- Engine is bound to the correct port but is not listening (e.g., crashed after binding).
- Network namespace or container isolation issue (if applicable).
**Investigation Steps:**
- Check engine logs for errors or stack traces.
- Verify engine process is still alive: `ps -p <PID>`.
- Check resource usage (CPU, memory) of the engine process.
- Attempt to connect via `telnet 127.0.0.1 <port>` to see if TCP handshake succeeds.

### 4. "Port in use by unknown process"
**Where it appears:** During lsof/ss checks, a port shows as LISTEN but the process name is unrecognizable or PID does not match any known engine.
**Likely Cause:**
- Leftover process from a previous deployment or test.
- Process from another system or service temporarily using the port.
- Engine process changed its name (unlikely).
**Investigation Steps:**
- Get full command line: `sudo ps -fp <PID>`.
- Check if the process belongs to a known service outside the DS ecosystem.
- If safe to do so, terminate the process and observe if the port frees up.
- Consider changing the engine's port if conflicts are frequent with external services.

### 5. "Failed to bind to port after multiple attempts"
**Where it appears:** Engine startup logs showing retry attempts.
**Likely Cause:**
- Port is rapidly being taken and released (e.g., by a test script or unstable service).
- Engine is attempting to bind to a range of ports and none are free.
- Permission issue (e.g., trying to bind to port <1024 without root).
**Investigation Steps:**
- Increase verbosity of engine logs to see bind attempt details.
- Check if engine is configured for port range instead of specific port.
- Verify user has permission to bind to the port (ports <1024 require root).
- Use `sudo lsof -iTCP:<port> -sTCP:LISTEN -nP` in a loop to see occupancy pattern.

## Ecosystem-Specific Notes for the specialist engine
- **Health check endpoint:** All engines should respond to `GET /health` with JSON containing `"status":"ok"` when healthy.
- **Binding address:** Engines typically bind to `127.0.0.1` only; external access is not expected.
- **Port reuse:** Engines should set `SO_REUSEADDR` to allow quick restarts, but this does not prevent two services from binding simultaneously.
- **Configuration sources:** Ports are typically set in:
  - `*_engine/run_server.py` (hardcoded or from config)
  - `*_engine/VERSION.md` (documented canonical port)
  - `*_engine/projects/PROJECT_REGISTRY.md` (cross-engine dependencies)
  - Environment variables or external config files (if used)
- **Common misconfiguration:** Confusing similar port numbers (e.g., 8090 vs 8098) or mistyping in configuration files.

## Quick Reference: the specialist engine and Common Errors
| Port | Engine | Typical Error if Misconfigured |
|------|--------|--------------------------------|
| 8010 | Wave Coaching | "Connection refused" from Quartz or CLI tools |
| 8089 | Quartz (Crystal) | "Address already in use" if Seed or another engine binds here |
| 8090 | Reproductive | "Connection refused" from Clinical or Scanner engines |
| 8091 | Allostasis | "Address already in use" if Harvey or another engine binds here |
| 8092 | Harvey | "Connection refused" from Allostasis or seed scanning |
| 8093 | Morphogen | "Address already in use" if Quartz or another engine binds here |
| 8094 | Beaumont | "Connection refused" from seed or other engines |
| 8095 | Seed | "Address already in use" if Reproductive or another engine binds here (common conflict) |
| 8096 | Bright | "Connection refused" from user-facing tools |
| 8097 | Unna | "Address already in use" if Bright or another engine binds here |
| 8099 | Clinical (Bernard) | "Connection refused" from Allostasis or other engines scanning it |

**Note:** The most frequent conflict observed is between Seed (8095) and Reproductive (8090) due to similar numbering and mutual dependencies.