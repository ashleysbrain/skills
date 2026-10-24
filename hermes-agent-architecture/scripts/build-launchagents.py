#!/usr/bin/env python3
"""
Build and install LaunchAgent plists for all DS organism engines.

This is the AUTONOMIC NERVOUS SYSTEM of the organism.
Like the medulla oblongata keeping your heart beating during sleep,
these plists keep engines alive across reboots and crashes.

Biological analog:
  - RunAtLoad=true   -> automaticity (SA node fires without brain input)
  - KeepAlive=true   -> medullary reflex (restart on failure)
  - Throttle 10s     -> refractory period (prevents fibrillation)

Reads FLEET_REGISTRY dynamically — new engines automatically get plists.

Usage:
  python3 build-launchagents.py          # generate plists
  python3 build-launchagents.py --install # generate + load into launchd
  python3 build-launchagents.py --unload  # unload all
"""
import os
import sys
import plistlib
import subprocess

WORKSPACE = os.environ.get("DS_WORKSPACE", "/<workspace>")
LAUNCH_DIR = os.path.expanduser("~/Library/LaunchAgents")
PYTHON = sys.executable or "/usr/local/bin/python3"

# Import the living registry
sys.path.insert(0, f"{WORKSPACE}/ds-engine-registry")
from ecs import FLEET_REGISTRY

LABEL_PREFIX = "com.divinityscience"

def get_engine_dir(key):
    """Find the actual directory for an engine key."""
    candidates = [key, key + "-engine"]
    for c in candidates:
        if os.path.isdir(os.path.join(WORKSPACE, c)):
            return c
    return None

def build_plist(key, entry):
    """Build a LaunchAgent plist dict for one engine."""
    name = entry.get("engine_name", key)
    engine_dir = get_engine_dir(key)
    
    if not engine_dir:
        return None, f"No directory found for {key}"
    
    server_file = os.path.join(WORKSPACE, engine_dir, "run_server.py")
    if not os.path.exists(server_file):
        return None, f"No run_server.py in {engine_dir}"
    
    label = f"{LABEL_PREFIX}.{key.replace('ds-', '').replace('-engine', '').replace('-', '.')}"
    
    plist = {
        "Label": label,
        "ProgramArguments": [
            PYTHON,
            server_file,
        ],
        "WorkingDirectory": os.path.join(WORKSPACE, engine_dir),
        "EnvironmentVariables": {
            "PYTHONPATH": f"{WORKSPACE}/ds-engine-registry:{WORKSPACE}/{engine_dir}/src",
            "DS_WORKSPACE": WORKSPACE,
        },
        "RunAtLoad": True,
        "KeepAlive": {
            "SuccessfulExit": False,
            "Crashed": True,
        },
        "ThrottleInterval": 10,
        "StandardOutPath": os.path.join(WORKSPACE, engine_dir, "logs", "launchd-stdout.log"),
        "StandardErrorPath": os.path.join(WORKSPACE, engine_dir, "logs", "launchd-stderr.log"),
        "ProcessType": "Background",
    }
    
    return plist, label

def ensure_log_dirs():
    """Create logs/ directories in each engine."""
    for key, entry in FLEET_REGISTRY.items():
        if entry.get("renamed_to"):
            continue
        engine_dir = get_engine_dir(key)
        if engine_dir:
            log_dir = os.path.join(WORKSPACE, engine_dir, "logs")
            os.makedirs(log_dir, exist_ok=True)

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "generate"
    
    ensure_log_dirs()
    os.makedirs(LAUNCH_DIR, exist_ok=True)
    
    plists = {}
    errors = []
    
    for key, entry in sorted(FLEET_REGISTRY.items()):
        if entry.get("renamed_to"):
            continue
        
        plist, result = build_plist(key, entry)
        if plist:
            plists[key] = (plist, result)
        else:
            errors.append(f"  SKIP  {key}: {result}")
    
    # Write plist files
    for key, (plist, label) in plists.items():
        plist_path = os.path.join(LAUNCH_DIR, f"{label}.plist")
        with open(plist_path, "wb") as f:
            plistlib.dump(plist, f)
    
    print(f"Generated {len(plists)} LaunchAgent plists in {LAUNCH_DIR}")
    if errors:
        print(f"\nSkipped {len(errors)} engines:")
        for e in errors:
            print(e)
    
    if action == "--install":
        print("\nLoading into launchd...")
        loaded = 0
        for key, (plist, label) in plists.items():
            plist_path = os.path.join(LAUNCH_DIR, f"{label}.plist")
            result = subprocess.run(
                ["launchctl", "load", plist_path],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                loaded += 1
                print(f"  OK  {label}")
            else:
                if "already" in result.stderr.lower():
                    print(f"  SKIP  {label} (already loaded)")
                    loaded += 1
                else:
                    print(f"  FAIL  {label}: {result.stderr.strip()}")
        print(f"\n{loaded}/{len(plists)} engines under autonomic supervision")
    
    elif action == "--unload":
        print("\nUnloading from launchd...")
        unloaded = 0
        for key, (plist, label) in plists.items():
            plist_path = os.path.join(LAUNCH_DIR, f"{label}.plist")
            result = subprocess.run(
                ["launchctl", "unload", plist_path],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                unloaded += 1
        print(f"Unloaded {unloaded} agents")
    
    elif action == "generate":
        print("\nTo install (start autonomic supervision):")
        print(f"  python3 {__file__} --install")
        print("\nTo uninstall:")
        print(f"  python3 {__file__} --unload")

if __name__ == "__main__":
    main()
