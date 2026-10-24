#!/usr/bin/env python3
"""Registry census for the Living Research Hub — run before any site-structure
or public-copy decision. Machine source of truth: agent-organism/ecs.py FLEET_REGISTRY."""
import sys
from collections import Counter

sys.path.insert(0, '/<workspace>')
import ecs  # noqa: E402

reg = ecs.FLEET_REGISTRY
bodies = Counter()
ports = set()
rows = []
for key, v in reg.items():
    if isinstance(v, dict):
        bodies[v.get('body_system') or v.get('body') or '?'] += 1
        p = v.get('port')
        if p:
            ports.add(p)
        rows.append((v.get('engine_name') or v.get('name') or key,
                     p, v.get('ds_ecs_code') or v.get('code'),
                     v.get('body_system') or v.get('body')))

print(f"engines: {len(reg)} | unique ports: {len(ports)}")
print("\nby body system:")
for b, c in bodies.most_common():
    print(f"  {b}: {c}")
skew = bodies.most_common(1)[0][1] / len(reg) if reg else 0
print(f"\nmax-bucket share: {skew:.0%} (if >40%, flat body-system taxonomy will bury the visitor — use function-first halls)")
if "--all" in sys.argv:
    print("\nfull roster:")
    for name, port, code, body in sorted(rows, key=lambda r: (r[3] or '', r[0])):
        print(f"  {name} | {port} | {code} | {body}")
