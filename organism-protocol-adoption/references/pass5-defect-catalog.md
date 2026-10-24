# Pass 4/5 adversarial QA defect catalog — MCP adoption chain

Context: principal directive "do another thorough QA pass... different adversarial
brains... find your gaps and half done work. i don't want talk." Executed as
rotated-brain adversarial passes over the MCP 2026-07-28 adoption work
(server `mosaic_mcp_server.py`, prober `mcp_discover_probe.py`, sensor
`real_sensors.sense_mcp`). Read this before the NEXT adversarial pass so old
defect classes are re-checked, not re-discovered.

## Brain rotation used

- Pass 3 (builds): the specialist engine (protocol surface), the specialist engine (probing),
  the specialist engine (sensing).
- Pass 4: the specialist engine (falsification vs primary-source spec) + the specialist engine
  (temporal/flow hazards).
- Pass 5: DS Gödel (self-reference/completeness), the specialist engine (invariants
  conserved across surfaces), the specialist engine (don't fool yourself — live A/B).
- Rule: the adversary brain must NEVER be the brain that built the code.

## Defects found and fixed

| # | Brain | Defect | Fix | Live proof |
|---|---|---|---|---|
| F1 | Popper | discover advertised `extensions` as top-level list (spec: map inside capabilities) + "planned" tasks ext = capability lie | removed; advertise only implemented | top-level `extensions` absent from response |
| F2 | Popper | `_meta.protocolVersion` ignored; stateless claim half-true | `_request_version()` reads both forms, echoes | echo verified top-level + nested |
| F3 | Lamport | sensor could block self-healing tick 120s on probes | fire-and-forget Popen | stale read 14ms, refresh lands ≤60s |
| F4 | Lamport | SUBSCRIPTIONS dict unbounded | prune oldest past 256 | boundary code |
| F5 | Noether | initialize said 1.2.0, discover said 1.2.1 — identity contradicted itself | one SERVER_IDENTITY/SERVER_CAPABILITIES source | init==discover version (1.2.2), caps match |
| F6 | Noether | `_meta` echo only on tools/call — half-done conformance | `_meta_echo()` helper on every surface | all 4 surfaces echo 2026-07-28 |
| F7 | Gödel | unknown method WITH id → silence = client hang | -32601; notifications stay silent | live zero-bytes reproduced before fix |
| F8 | Gödel | JSON array line crashed stdio loop (AttributeError) | -32600 per id'd entry; loop survives | array line + subsequent line both answered |
| F10 | Feynman | **prober lied: "context7 dead" was probe-fabricated** — hardcoded `MCP-Protocol-Version: 2026-07-28` pre-negotiation gets spec-permitted 400 | headerless first, then advertised-version only | A/B: 2026-07-28→400, 2025-06-18→200, none→200; fleet 10/10 after |
| G1 | Feynman | stale-path re-read snapshot right after async kick = same stale bytes (dead code) | removed; serve stale honestly with age | age 11214s reported honestly |
| G4 | Lamport | one-file-per-probe snapshot series grows forever | keep newest 48; `-current` regenerated never pruned | 60→48 scratch test |

## Reproduction commands (the adversarial battery)

```bash
cd ~/your-org/your-stack/adapters/mcp
python3 - <<'EOF'
import subprocess, json, sys
def send(lines, label):
    p = subprocess.run([sys.executable, "mosaic_mcp_server.py"],
        input="\n".join(lines)+"\n", capture_output=True, text=True, timeout=15)
    out = [json.loads(l) for l in p.stdout.splitlines() if l.strip()]
    print(label, "exit=", p.returncode, "responses=", len(out)); return out, p

V='"_meta":{"protocolVersion":"2026-07-28"}'
# identity invariant + echo everywhere
out,_=send(['{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"q","version":"0"}}}',
            f'{{"jsonrpc":"2.0","id":2,{V},"method":"server/discover"}}',
            f'{{"jsonrpc":"2.0","id":3,{V},"method":"tools/list"}}',
            f'{{"jsonrpc":"2.0","id":4,{V},"method":"subscriptions/listen","params":{{"events":["toolsListChanged"]}}}}'],"battery")
# unknown method with id / array line
out,_=send(['{"jsonrpc":"2.0","id":9,"method":"bogus/method"}'],"F7")
p=subprocess.run([sys.executable,"mosaic_mcp_server.py"],
    input='[{"jsonrpc":"2.0","id":1,"method":"tools/list"}]\n{"jsonrpc":"2.0","id":2,"method":"tools/list"}\n',
    capture_output=True,text=True,timeout=15)
print("F8 exit=",p.returncode)
EOF
# prober header A/B (never trust a death verdict without it)
for V in "2026-07-28" "2025-06-18" ""; do
  curl -s -o /dev/null -w "%{http_code}" -X POST https://mcp.context7.com/mcp \
    -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
    ${V:+-H "MCP-Protocol-Version: $V"} \
    -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"q","version":"0"}}}'
done
```

## Meta-lessons (recorded in run-record Pass 5)

1. Two patches corrupted the file mid-pass (typo'd identifiers:
   `regiustered_at`, a sliced-string jsonrpc). LSP caught both instantly.
   Read the diff after EVERY patch.
2. The happy-path battery passed a server that would hang/crash real
   clients (F7/F8). Adversarial inputs are not optional.
3. The worst defect was in the INSTRUMENT, not the system (F10). When a
   probe reports failure, A/B the probe itself before believing the drift.
4. Disclosed limits are part of the deliverable: live harness instance
   runs boot-time code until next restart (adiabatic — never kill your own
   tool bridge mid-session).
