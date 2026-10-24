# Crash Forensics and Load Lightening (macOS mesh nodes)

Depth for the "what is killing this machine" trigger in the parent skill.
Applies when crashes, not just load, are the question.

## Forensic hierarchy — mechanism before blame

1. **`/Library/Logs/DiagnosticReports/` FIRST.** The newest files name the
   crash mechanism directly: `Kernel_*gpuRestart` storms (driver resets;
   read the uptime in the header — 40h+ uptime at reset time is itself a
   finding), `WindowServer*spin` (display-server watchdog kill — the crash
   the user actually sees), panic files. `head -30` per file suffices.
2. **`pmset -g log`** — sleep/DarkWake/wake lines. Repeated "Entering Sleep
   … Using Batt" interrupted by maintenance wakes = scheduled work fighting
   sleep on battery; the machine never truly rests.
3. **`log show` LAST, with tight predicates only** — broad sweeps run past
   3-4 minute timeouts and return nothing; file-based sources answer faster.
4. **Attribute workloads only after the mechanism is known.** A GPU-reset
   storm on a 40h-uptime machine under sustained baseline load is a
   reboot-hygiene + load-floor failure — do not let the loudest scheduled
   job take the blame for a driver storm it merely fed.

## Same-day lightening moves (no new hardware)

- **Cap unbounded Docker containers.** `HostConfig.Memory == 0` means a
  container can balloon until the Docker VM swaps, which feeds exactly the
  memory pressure that precedes GPU/userland crashes. Measure steady usage
  (`docker stats --no-stream`), then `docker update --memory <X>m
  --memory-swap <X>m <name>` slightly above it — swap equal to memory so
  there is no spillover. Verify with `docker inspect -f '{{.HostConfig.Memory}}'`.
  Worst case becomes a contained container restart, not a host kill.
- **Move scheduled jobs out of the sleep window** — see the sibling skill
  `hermes-cron-scheduling` for the edit + verification commands.
- **Scheduled nightly reboot is the insurance when uptime feeds the crash
  class** (`sudo pmset repeat restart MTWRFSU 04:00:00`) — needs admin, so
  stage it as an explicit operator manual step rather than attempting it.

## Bootstrapping a remote batch lane over the tailnet

Standard path once a placement verdict names a remote node:

1. **`whoami` and stale-mirror check first** — the node's username may
   differ from the local one, and nodes often hold OLD mirrors (bare repos,
   month-old clones) from earlier attempts; supersede them explicitly so a
   stale mirror never silently serves old code.
2. **Rsync the working tree, not git clone.** Fresh nodes have no GitHub
   credentials: https clone fails non-interactively ("could not read
   Username") and ssh keys are absent. `rsync -az <repo>/ user@100.x:~/lane/`
   moves gigabytes in minutes over the tailnet and needs nothing but ssh.
3. **venv on the node's own Python, then compile there.** Node interpreters
   can be years older than local; `./venv/bin/python -m py_compile <scripts>`
   ON THE NODE is the compatibility check — local compile success proves
   nothing. Finish with one real script run, not just compile.
