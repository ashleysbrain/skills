---
name: service-port-conflict-resolution
category: devops
description: Diagnose and resolve port conflicts in a distributed engine or microservice ecosystem.
trigger_conditions:
  - One or more services fail to start or health checks fail
  - Suspected port conflict after deployment or configuration change
  - Error messages indicating "address already in use" or "connection refused"
  - Unexpected service behavior suggesting wrong port binding
  - Need to bring the full DS engine fleet online (fleet boot/recovery)
  - Preparing for a working session and need to verify all engines are up
  - Telegram gateway or GG3 stack needs readiness verification
  - Engines have crashed and need to be restarted
---

## Overview
This skill covers fleet-wide port management for the Divinity Science AI Organism: diagnosing conflicts, bringing engines online, verifying fleet health, and recovering from partial outages. Use it whenever the DS engine fleet needs to be up and verified.

## When to Use
- Services fail to start with bind errors
- Health checks fail unexpectedly after configuration changes
- Suspected port collisions during ecosystem expansion or reconfiguration
- After automated deployment scripts that may have assigned conflicting ports
- Fleet boot: bringing all engines online after reboot or partial outage
- Pre-session readiness check: verifying all critical specialists are ON CALL
- Starting engines that are NOT in the FLEET_REGISTRY (manual start required)

## Step-by-Step Procedure

### 1. Determine Expected Port Assignments
Consult ecosystem documentation, specification files, or version manifests to establish the canonical port mapping for each service.

**Commands:**
```bash
# Example for the specialist engine: check VERSION.md or PROJECT_REGISTRY.md
grep -r "Port:" /path/to/ecosystem/docs/
cat /path/to/ecosystem/PROJECT_REGISTRY.md | grep -E "(Port|PORT)"
# Look for explicit port assignments in config files or startup scripts
```

### 2. Check Current Port Usage
Identify which processes are currently bound to which ports.

**Commands:**
```bash
# Listen for TCP ports (adjust range as needed)
sudo lsof -iTCP -sTCP:LISTEN -nP | grep LISTEN
# Or for a specific port range
sudo lsof -iTCP:port-8100 -sTCP:LISTEN -nP
# Alternative using ss or netstat
ss -tlnp | grep :809[0-9]
```

### 3. Identify Conflicts
Compare expected vs. actual port usage to find:
- **Port in use by wrong service**: Expected port X for Service A, but found bound to Service B
- **Port not in use when expected**: Expected port X for Service A, but no process bound
- **Port in use by multiple services**: Two services bound to same port (should not happen with proper SO_REUSEADDR, but indicates misconfiguration)

**Check for launchd-managed services (macOS DS organism):**
```bash
# List all your-org launchd agents
launchctl list | grep divinityscience
# Check a specific plist for KeepAlive behavior
cat ~/Library/LaunchAgents/com.divinityscience.<service>.plist | grep -A1 KeepAlive
```
If `KeepAlive=true`, the service is managed by launchd and will auto-restart. Repeated `EADDRINUSE` errors are likely orphaned background launches hitting the already-bound port, NOT a real conflict. Verify the launchd-managed PID is healthy with `curl http://127.0.0.1:<port>/health`.

### 4. Resolve Each Conflict
For each conflict, determine the corrective action:

#### Case A: Service bound to wrong port
1. Identify why the service is bound incorrectly (check its config/startup script)
2. Stop the erroneous process: `kill <PID>` or use service manager
3. Revert the service's configuration to bind to correct port
4. Restart the service on the correct port

#### Case B: Expected port free but service not running
1. Verify service is supposed to be running (check deployment status)
2. Start the service: ensure it's configured for correct port
3. If service fails to start, check logs for other errors

#### Case C: Two services bound to same port (rare)
1. Determine which service should rightfully occupy the port (based on docs)
2. Stop the incorrect service
3. Reconfigure the incorrect service to use its proper port (if different) or investigate why it's binding elsewhere

### 5. Verify Resolution
After making changes, confirm all services are healthy on their expected ports.

**Commands:**
```bash
# For each service, check health endpoint
curl -s http://127.0.0.1:<expected_port>/health | python3 -m json.tool
# Or use a script to check all
for port in 8010 8089 8090 8091 8092 8093 8094 8095 8096 8097 8099; do
  echo "Checking port $port:"
  curl -s --max-time 2 http://127.0.0.1:$port/health 2>/dev/null | 
    python3 -c "import sys,json;print(json.load(sys.stdin).get('status','DOWN'))" 2>/dev/null || echo "DOWN"
done
```

## Pitfalls & Anti-Patterns
- **Assuming without verifying**: Never guess which service uses which port; always consult documentation.
- **Partial fixes**: Resolving one conflict may reveal another; always verify the entire ecosystem.
- **Ignoring dependent services**: Changing a service's port may require updating clients or service discovery.
- **Killing wrong process**: Double-check PID and service name before killing.
- **Not persisting changes**: Ensure configuration changes are saved to survive restarts.
- **Overlooking ephemeral ports**: Distinguish between service listening ports and client ephemeral ports in diagnostics.
- **Mistaking launchd relaunch noise for a real conflict**: When a service is managed by macOS launchd with `KeepAlive=true`, orphaned background launches hit `EADDRINUSE` and exit clean. Diagnose with `launchctl list | grep <service>`. Do NOT kill the launchd-managed PID to "resolve" harmless noise.
- **Host process steals Docker organism port (GG3 2026-08-02)**: Host listener wins user curls while container is healthy. Classic: `hydra-os/gg_metrics_v2.py --serve` on :port reports **the operator agent Live/Tubman** while `docker exec` vitals say **GG3**. Always dual-check host curl vs `docker exec … curl 127.0.0.1:<port>`. Unload GG3 LaunchAgents for Docker path.
- **Wrong identity string is a port-ownership symptom**: If `/vitals` organism name is a peer org (Live vs GG3 vs Cyber), treat as bind/ownership failure first, not a YAML typo.

## Verification
- All services report healthy status on their expected ports
- No error logs indicating bind failures or connection refusals
- Ecosystem-level functionality restored (e.g., cross-service communication works)

## Tools Used
- `lsof` or `ss`: To list listening ports and associated processes
- `curl` or `wget`: To test service health endpoints
- `kill`: To terminate errant processes
- Text editors (`nano`, `vim`, `sed`): To revert configuration files
- `ps` or `pgrep`: To find processes by name
- `grep`: To search documentation for port assignments

## Dynamic Port Allocation (binding — user requirement 2026-08-02)

Ports MUST be able to evolve if the person spinning up the organism already has those ports in use. Hardcoded ports that block deployment on a new machine are a critical bug.

**Rule:** Every service must read its port from config (ports.yaml) with environment variable override. No service may hardcode a port number as its only source. The priority chain:

```
ENV_VAR > ports.yaml > hardcoded fallback default
```

**Pattern for every service script:**
```python
port = 8400  # hardcoded fallback ONLY
try:
    import yaml
    cfg_path = Path(__file__).parent.parent / "config" / "ports.yaml"
    cfg = yaml.safe_load(cfg_path.read_text()) or {}
    primary = cfg.get("telemetry", {}).get("primary", "")
    if ":" in primary:
        port = int(primary.rsplit(":", 1)[1])
except Exception:
    pass
port = int(os.environ.get("CYBER_GG_METRICS_PORT", port))
```

**The auto-find-next-available pattern (from cyber_gg_server.py):**
```python
def is_port_available(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) != 0

def find_available_port(preferred, max_offset=20):
    for offset in range(max_offset):
        candidate = preferred + offset
        if is_port_available(candidate):
            return candidate
    return None  # caller must handle
```

**Adversarial verification after any organism deploy:**
```bash
# Grep every service script for hardcoded ports — any hit that isn't a fallback default is a bug
grep -rn 'port.*=.*8[0-9][0-9][0-9]' organism/ops/ organism/sherman_router.py organism/start_engines.py
# Check engine registry ports match the target block
python3 -c "
import sys; sys.path.insert(0, 'organism/engines')
from ecs import FLEET_REGISTRY
ports = [v['port'] for v in FLEET_REGISTRY.values() if isinstance(v,dict) and v.get('port')]
print(f'Port range: {min(ports)}-{max(ports)}')
# Check for cross-organism conflicts
conflicts = [p for p in ports if 8200 <= p <= 8210 or 8300 <= p <= 8320]
print(f'Cross-organism conflicts: {len(conflicts)}')
"
```

**Known port-shift bugs found in Cyber the operator agent 2026-08-02:**
1. `sherman_router.py` had hardcoded GG3/the operator agent Live tissue ports (8097, 8001, 8137, 8092, 8264) instead of shifted Cyber the operator agent ports
2. `cyber_gg_medical_records.py` had `COLLECTOR_URL = "http://0.0.0.0:port"` (GG3's port)
3. `ports.yaml` coaching endpoint pointed to GG3's Kuramoto (8010) not Cyber the operator agent's (9010)
4. Federation URL pointed to :port which was occupied by the specialist engine, not the federation server
5. `physics_compliance.py` had hardcoded `WORKSPACE = Path("/<workspace>")`

These are the class of bugs that happen when files are copied from one organism without port-shifting ALL references. The grep verification above catches them.

The complete canonical port mapping lives in `references/ds-engine-port-mapping.md`
(60+ engines verified July 2026). The machine source of truth for engine
definitions is `agent-organism/ecs.py` FLEET_REGISTRY, not `ENGINE_REGISTRY.yaml`
(which is documentation and can drift).

**Fleet boot/recovery procedure:** see `references/fleet-boot-procedure.md`
for the full step-by-step: health sweep, starting down engines (including
those NOT in FLEET_REGISTRY like the operator agent Live telemetry/medical), the terminal
backgrounding workaround, and sibling-agent coordination.

**Key infrastructure layers:**
- DS engines (8089-8265): registered in `agent-organism/ecs.py`, auto-managed by fleet autonomic supervisor
- the operator agent Live infra (8200-8201): manually started, NOT auto-restarted on crash
- GG3 product path (2026-08-02): **Docker** `gg3-8300` from `gg3-blueprint`, ports **8300–8306**. Host LaunchAgents `com.your-org-research-lab.gg3-launcher` and `com.your-org.gg3-metrics-keepalive` are **disabled** for isolation — do not treat launchd GG3 as canonical. If :port returns organism "the operator agent Live", host `gg_metrics_v2` (or similar) stole the port; kill host listener and dual-check `docker exec gg3-8300 curl 127.0.0.1:port/vitals`.
- the operator agent gateway: launchd-managed via `ai.hermes.gateway` (KeepAlive)
- Fleet supervisor: launchd `com.your-org.fleet-autonomic` (StartInterval=30s)

## Support Files
This skill includes the following support files for practical implementation:

- `references/ds-engine-port-mapping.md`: Complete canonical port assignments for ALL DS engines (60+ ports, July 2026), the operator agent Live/GG3 infrastructure, source-ready engines, and the 6 critical diagnostic specialists that must always be ON CALL
- `references/fleet-boot-procedure.md`: Step-by-step fleet boot and recovery procedure — health sweep, starting down engines, terminal backgrounding guard workaround, GG3 proxy Tailscale binding, and sibling-agent coordination protocol
- `scripts/check_ds_ports.sh`: Bash script to verify health of all engines on canonical ports
- `references/common_port_conflict_errors.md`: Common error messages and their meanings for port conflicts
- `templates/port_config_example.yaml`: Example configuration snippet for defining engine port mappings
- `scripts/detect_port_conflicts.sh`: Automated script to detect and report port conflicts with suggested fixes

## Terminal Backgrounding Constraint
The the operator agent terminal tool rejects foreground commands containing shell `&` (backgrounding operator), even inside heredocs or bash scripts. To start server processes, use Python `subprocess.Popen()` via `execute_code` or `terminal(background=true)` with a Python script. See `references/fleet-boot-procedure.md` for the exact pattern.

## Critical Diagnostic Specialists
Six specialists MUST always be ON CALL per binding user rule: the specialist engine/Bernard (:port), DS Röntgen (:port), the specialist engine (:port), the specialist engine (:port), the specialist engine (:port), the specialist engine/Cannon (:port). If any are down, repair immediately.

## Related Skills
- `hermes-agent`: For configuring the operator agent Agent itself
- `sibling-agent-fleet-analytics-troubleshooting`: For broader fleet health issues
- `devops/gateway-startup-hooks`: For gateway-specific startup issues

---