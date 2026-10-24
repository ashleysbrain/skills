# Architecture Term Definitions — Quick Reference

Condensed definitions for systems-engineering terms that are frequently used
loosely. All verified from primary sources via direct curl/urllib retrieval.

---

## Harness vs Mesh (the core confusion)

| Dimension | Harness | Mesh |
|---|---|---|
| Scope | Single artifact (model, agent, test) | Many artifacts (services, agents, nodes) |
| Role | Drives execution of ONE thing | Routes communication BETWEEN many things |
| Topology | Wrapper around one subject | Peer-to-peer fabric across many subjects |
| Control | Active: owns the run loop | Passive fabric: enables routing, does not direct |
| Direction | Vertical (wraps) | Horizontal (connects peers) |

**They are complementary, not interchangeable.** An agent sits IN a harness and
is CONNECTED BY a mesh.

## Harness — active execution driver

Wraps around and drives something: controls execution flow, supplies inputs,
captures outputs, provides infrastructure the wrapped artifact needs.

| Variant | Definition | Source |
|---|---|---|
| Test harness | Stubs + drivers for testing; imitation infrastructure | Wikipedia: Test harness |
| Evaluation harness | Unified framework testing LLMs on standardized benchmarks | EleutherAI lm-evaluation-harness |
| Model harness | Execution wrapper managing model lifecycle (load, infer, batch) | Industry: vLLM/TGI/Triton |

```
Harness  → CONTROLS execution lifecycle (active driver)
Wrapper  → TRANSLATES interface only (passive, no control)
Scaffold → GENERATES initial structure (disposable)
```

---

## MESH — software architecture view (LOGICAL layer only)

Decentralized infrastructure layer where peer nodes communicate laterally.
Control plane configures but does NOT mediate every call.

| Variant | Definition | Source |
|---|---|---|
| Service mesh | Dedicated infrastructure layer for service-to-service comms via proxy. Data plane (sidecars) + control plane. | Wikipedia, Istio docs |
| Data mesh | Sociotechnical approach: domain ownership, data as product, self-serve platform, federated governance | Dehghani, martinfowler.com |
| Agent mesh | (Emerging) P2P agent coordination fabric with discovery, routing, policy | By analogy; no canonical impl |
| Compute mesh | Distributed execution fabric with pooled resources | Ray, Dask |

```
Mesh         → DECENTRALIZED P2P fabric (horizontal)
Bus/Hub      → CENTRALIZED mediator
Orchestrator → CENTRALIZED director (schedules, delegates)
```

> **⚠ NARROW VIEW ALERT**: The table above covers only the LOGICAL/software
> layer. For a composable OS that meshes physical devices AND software agents,
> see the Three-Layer Mesh Model below.

---

## MESH — cross-discipline view (ALL layers)

"Mesh" means **"rich interconnection among autonomous nodes"** at its core,
but every field specializes it differently. The through-line: many autonomous
nodes cooperate by relaying/transforming/exchanging something directly
peer-to-peer, without a single point of failure or strict hierarchy.

### Mesh networking protocols (physical devices forming meshes)

| Protocol | Physical Layer | Mesh Type | Key Trait |
|---|---|---|---|
| Wi-Fi Mesh (EasyMesh) | 802.11 | Self-healing partial mesh | Multi-node blanket coverage; auto path selection |
| Zigbee | IEEE 802.15.4 (2.4 GHz) | Full routed mesh | Low-power, 250 kbit/s; 10-100m/hop; 128-bit encryption |
| Bluetooth Mesh | BLE | Flood mesh (every relay retransmits) | Jul 2017; many-to-many; lighting/IoT; TTL-limited hops |
| Thread | IEEE 802.15.4 + 6LoWPAN | IPv6 mesh | Every device individually IP-addressable; Nest origin; transport for Matter |
| Matter | IP (over Thread/Wi-Fi) | Uses transport mesh | App-layer standard; Apple+Google+Amazon+CSA; vendor-neutral; PKI attestation |

### Mesh topology (network engineering)

**Defining properties:** (1) Non-hierarchical, (2) Multi-path routing,
(3) Self-healing, (4) Cooperative forwarding (every node can relay),
(5) Fault-tolerant (no single point of failure).

| Topology | Failure Mode | Scalability |
|---|---|---|
| Bus | Entire network fails on backbone break | Poor |
| Star | Single point of failure (hub) | Good |
| Ring | Break isolates nodes | Moderate |
| Mesh (Full) | No single point of failure | Poor (O(n²) links) |
| Mesh (Partial) | Graceful degradation | Excellent |

### Mesh in computational geometry

- **Polygon mesh:** Vertices + edges + faces defining 3D surface. Render edges only → wireframe.
- **Finite Element Mesh (FEM):** Discretizes continuous domain into elements (triangles, tetrahedra) to solve differential equations. Finer = more accuracy but more compute.

### Mesh in physics

- **Causal Dynamical Triangulations (CDT):** Spacetime emerges from mesh of 4-simplices.
- **Lattice gauge theory:** Quantum fields on a discrete lattice.
- **Spin networks (Loop Quantum Gravity):** Space itself modeled as mesh of graphs.

### Mesh in biology

- **Extracellular Matrix (ECM):** Network of macromolecules (collagen, glycoproteins) providing structural + biochemical support to cells. NOT a channel — a **fabric that provides context and signaling**.
- **Cytoskeletal mesh:** Dynamic protein filaments (actin, microtubules) capable of **rapid growth/disassembly**.
- **Neural mesh / connectome:** ~86B neurons, ~100T synapses — dense information-processing mesh.

### Mesh in hardware

- **AMD Infinity Fabric:** Interconnect linking cores, CCXs, CCDs, I/O die. Enables multi-chiplet architectures.
- **Intel Mesh Interconnect:** 2D mesh grid for multi-core Xeon; beats ring at scale.
- **Switched fabric:** Nodes interconnect via crossbar switches. Higher throughput than broadcast networks. "Multiple switches in a fabric usually form a mesh internally."

### Physical device mesh (phones, computers, tablets)

| System | Mesh Type | Key Characteristic |
|---|---|---|
| Apple Continuity | Proximity cluster | BLE discovery + Wi-Fi transfer + iCloud identity; NOT routed mesh |
| Universal Control | Input mesh | Single kb/mouse across Mac + iPad |
| Samsung DeX | Role transformation | Phone → desktop when docked; device assumes new role |
| Folding@home | Star-distributed compute | Central coordinator + independent compute nodes; exceeded 1 exaflop |
| Matter/Thread | Vendor-neutral device mesh | IP-addressable, locally controllable, PKI-verified |

---

## Mesh NETWORK vs Mesh TOPOLOGY vs Mesh FABRIC

| Concept | Abstraction Level | Emphasis | Key Property |
|---|---|---|---|
| **Mesh Topology** | Mathematical/graph | Connection SHAPE | Multiple peer links per node |
| **Mesh Network** | System/operational | Cooperative BEHAVIOR | Self-organizing, self-healing routing |
| **Mesh Fabric** | Hardware/infrastructure | Throughput CAPACITY | Switched, multi-path, high bandwidth |

**Analogy — Highway system:** Topology = map of city connections. Network = traffic rules + emergency response. Fabric = road infrastructure, lanes, interchanges.

---

## Three-Layer Mesh Model for composable OS

A composable OS where physical devices AND software agents are meshed requires
three interlocking layers:

| Layer | Name | What It Does | Biological Analogy |
|---|---|---|---|
| Layer 1 | **Physical Mesh** | Devices connected via Matter/Thread/BLE/Wi-Fi | Cytoskeleton (dynamic scaffold) |
| Layer 2 | **Logical Mesh** | Software agents, models, services in P2P routing topology (service mesh) | Neural network |
| Layer 3 | **Semantic Mesh** | Shared context/state fabric — state, intent, context flow between all nodes | Extracellular matrix |

**Physical devices are first-class mesh nodes** with compute, sensors,
displays, identity, and role plasticity. They participate in all three layers.

**Broadened definition:** A composable OS mesh is a self-organizing,
self-healing cooperative structure of heterogeneous nodes (physical devices +
software agents + models + services) that communicate laterally across three
interlocking layers — physical interconnect, logical routing, and semantic
context — with no single point of failure and no mandatory hierarchy.

---

## Cross-discipline mapping (composable OS concept → mesh analogy)

| Composable OS Concept | Closest Mesh Analogy | Why |
|---|---|---|
| Device discovery & pairing | Apple Continuity / Matter commissioning | Proximity-based, identity-verified node joining |
| Agent-to-agent messaging | Service mesh (data plane) + Neural network | P2P routing with observability and security |
| Shared state / context | Extracellular matrix | Fabric provides context + signaling to embedded nodes |
| Dynamic agent scaling | Cytoskeletal assembly/disassembly | Rapid growth/reconfiguration |
| Compute distribution | Folding@home work-unit model | Split computation across nodes |
| Fault tolerance | Mesh network self-healing (TRILL, SPB) | Route around failed nodes |
| Role transformation | Samsung DeX | Device assumes new role based on context |
| Cross-vendor interop | Matter protocol | PKI-verified, standard-based participation |
| Performance at scale | Hardware mesh interconnect (Intel/AMD) | Mesh beats star/ring at high node count |
| Problem decomposition | Finite element mesh | Continuous problem → discrete cooperating elements |

---

## Platform / Framework / Runtime / Orchestrator / Registry / Connector / Adapter

| Term | Owns execution? | Inversion of control? |
|---|---|---|
| Platform | Yes (provides environment) | N/A — IS the environment |
| Framework | Yes (calls your code) | Yes (framework calls you) |
| Runtime | Yes (executes running code) | N/A — IS the execution env |
| Orchestrator | Yes (directs others) | Directs (centralized) |
| Registry | No (passive lookup) | No |
| Connector | No (pass-through conduit) | No |
| Adapter | No (interface translation) | No |

## Composable-OS layer patterns (comparison)

All composable systems share: **minimal core + extension points + communication fabric**.

| Framework | Core layer | Extension mechanism |
|---|---|---|
| Microkernel | μ-kernel (IPC, threads, address space) | User-space servers via IPC |
| Erlang/OTP | Runtime + OTP behaviors | gen_server, supervisor, application |
| Kubernetes Operator | Custom Resource + control loop | CRDs + reconciling controller |
| LangGraph | Stateful graph of nodes | Nodes (callables), edges, state schema |
| AutoGen | Multi-agent conversation | AssistantAgent, GroupChat, tools |

---

## Sources

### Software architecture sources
- Wikipedia: Test harness, Service mesh, Data mesh, Microkernel, Runtime system, Software framework, Orchestration, Computing platform, Erlang, Adapter pattern, Wrapper library, Service locator pattern
- Kubernetes docs: Operator pattern (kubernetes.io/docs/concepts/extend-kubernetes/operator/)
- Istio docs: The Istio service mesh (istio.io/latest/about/service-mesh/)
- Dehghani: Data Mesh Principles (martinfowler.com/articles/data-mesh-principles.html, Dec 2020)
- EleutherAI: lm-evaluation-harness (github.com/EleutherAI/lm-evaluation-harness)
- Microsoft: AutoGen (github.com/microsoft/autogen)

### Cross-discipline sources (added 2026-08-08)
- Wikipedia: Mesh networking, Network topology, Wireless mesh network
- Wikipedia: Bluetooth mesh networking, Zigbee, Thread (network protocol), Matter (standard)
- Wikipedia: Polygon mesh, Finite element method
- Wikipedia: Extracellular matrix, Cytoskeleton
- Wikipedia: HyperTransport/Infinity Fabric, Switched fabric
- Wikipedia: Samsung DeX, Folding@home, OS X Yosemite (Continuity), macOS Monterey (Universal Control)
