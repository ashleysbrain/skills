# Body Analog Mappings for Project Physics Primitives

This document maps each physics primitive in the project management layer to its biological analog, providing intuitive interpretation for project health signals.

## 1. Free Energy Landscape → Cellular Metabolism / FEP
**Mapping**: Project free energy (F = ⟨E⟩ - TS) ↔ Cellular free energy
- **Internal Energy (⟨E⟩)** ↔ Chemical potential energy stored in molecular bonds
- **Entropy (S)** ↔ Conformational entropy / disorder in molecular states  
- **Temperature (T)** ↔ Thermal energy driving molecular motion
- **Free Energy Minimization** ↔ System seeks lowest energy state (completed project)
- **Forks as Local Minima** ↔ Metastable states requiring activation energy to escape
- **Fork-Queue as Thermal Energy** ↔ Brownian motion providing escape energy

**Interpretation Guide**:
- High F: Project far from completion (high uncertainty + much work remaining)
- Low F: Near completion (work done, low uncertainty)
- Rising F: Project accumulating work faster than completing it
- Forks increasing F: Local decision traps increasing project energy

## 2. Critical Path → Cardiovascular Perfusion System
**Mapping**: Dependency DAG ↔ Blood vessel network
- **Critical Path** ↔ Aorta and major arteries (must stay open for survival)
- **Parallelizable Tasks** ↔ Collateral circulation (nice to have but not critical)
- **Feasibility (Largest Component)** ↔ Percentage of tissue receiving adequate perfusion
- **Bottleneck Task** ↔ Occlusion point in vascular network
- **Dependency Resolution** ↔ Vasodilation/angiogenesis improving flow

**Interpretation Guide**:
- Feasibility < 0.7: Significant portion of project at risk of stalling
- Bottleneck on critical path: Focus unblocking efforts here first
- High parallelizability: Opportunity to accelerate with additional resources
- Changing critical path: Dependency structure evolving (re-plan needed)

## 3. Stress & Strain → Mechanotransduction System
**Mapping**: Project timeline stress/strain ↔ Mechanical load on cells
- **Stress (σ)** ↔ Force per unit area (pressure applied to material)
- **Strain (ε)** ↔ Deformation from original shape (stretch/compression)
- **Yield Strength** ↔ Point where elastic deformation becomes permanent
- **Safety Factor** ↔ Engineering margin before failure
- **Verdict (ELASTIC/PLASTIC/FRACTURE)** ↔ Material failure modes

**Interpretation Guide**:
- σ > σ_yield: Permanent timeline deformation (scope creep, quality loss)
- ε > 0.3: Significantly behind schedule (>30% delay)
- Safety Factor < 1.5: Operating close to failure threshold
- Cyclic loading: Repeated stress cycles causing fatigue damage

## 4. Critical Slowing Down → Allostatic Load / Early Warning System
**Mapping**: Fork recovery dynamics ↔ Physiological stress response
- **Recovery Time** ↔ Time to return to baseline after stressor
- **Recovery Trend** ↔ Increasing recovery time = allostatic load accumulation
- **Variance Trend** ↔ Growing fluctuations = loss of homeostatic control
- **Autocorrelation** ↔ High memory = system state persisting longer
- **Early Warning Signal** ↔ Pre-symptomatic detection of impending failure

**Interpretation Guide**:
- Rising recovery times: Project taking longer to resolve decisions
- Increasing variance: Unpredictable decision resolution times
- High autocorrelation: Today's fork status predicts tomorrow's (stuck state)
- Combined signals: Strong indication of approaching tipping point

## Usage in Project Health Assessment

When interpreting physics reports, consider the body analog first:

1. **Cellular Metabolism Lens**: "Is the project metabolizing work efficiently or getting stuck in local energy minima?"
2. **Cardiovascular Lens**: "Is the main perfusion pathway clear or are we risking ischemia in critical regions?"
3. **Mechanotransduction Lens**: "Are we applying sustainable mechanical load or causing microfractures in the timeline?"
4. **Allostatic Load Lens**: "Are we seeing the early warning signs of systemic overload before overt failure?"

This biological framing makes abstract physics signals immediately interpretable for project leaders familiar with basic physiology concepts.

---

## Quantum Layer Body Analogs

The quantum layer maps real quantum biology (proven in living systems) to
PM problems where quantum solutions are strictly more powerful than classical
ones.

### Q1. Superposition Forks → Photosynthetic Energy Transfer
**Mapping**: Fork in superposition ↔ Exciton coherence in photosynthesis
- **Superposition (psi = alpha|A> + beta|B>)** ↔ Exciton exists in multiple paths simultaneously
- **Measurement (collapse)** ↔ Exciton arrives at reaction center (one path confirmed)
- **Pre-computation** ↔ 95% energy transfer efficiency (vs 35% classical limit)

**Interpretation**: When a fork is in superposition, both branches are pre-computed.
When the answer arrives, the work is already done — like a photosynthetic complex
that explores all paths and collapses on the one that reaches the target fastest.

### Q2. Entanglement Dependencies → Bird Navigation (Cryptochrome)
**Mapping**: Dependency entanglement ↔ Quantum entanglement in avian cryptochrome
- **Entangled pair** ↔ Two subtasks linked by dependency (Bell pair analog)
- **Collapse propagation** ↔ Measuring one particle determines the other instantly
- **Zero-message propagation** ↔ Completing A instantly makes B "ready" — no polling

**Interpretation**: Classical PM polls dependent tasks ("is A done yet?").
Entangled PM knows instantly — the dependency graph IS the entanglement graph.

### Q3. Tunneling Barriers → Enzyme Catalysis
**Mapping**: Fork bypass ↔ Proton/electron tunneling in enzymes
- **Barrier (V)** ↔ Fork question complexity
- **Worker energy (E)** ↔ Worker expertise
- **Barrier width (L)** ↔ Number of affected subtasks
- **P(tunnel) = exp(-2*kappa*L)** ↔ Probability of discovering an alternative path

**Interpretation**: A worker with high expertise (E close to V) has a real chance
of bypassing a fork entirely by finding a creative alternative. Low expertise
workers must wait classically.

### Q4. Quantum Annealing → Protein Folding
**Mapping**: Lattice optimization ↔ Protein finding native conformation
- **Transverse field Gamma** ↔ Quantum fluctuations exploring configuration space
- **Tunneling through barriers** ↔ Escaping shallow local minima in the energy landscape
- **Annealing schedule** ↔ Gamma decays from high (explore) to low (exploit)

**Interpretation**: Classical annealing must thermally climb over energy barriers
(slow for wide barriers). Quantum annealing tunnels through them — faster when
the landscape has many shallow local minima (typical for complex project lattices).

### Q5. Coherence Flow → Organism-wide Information Transfer
**Mapping**: Multi-engine state sync ↔ Coherent energy transfer in photosynthesis
- **Coherence time (tau)** ↔ How long engine states stay synchronized without resync
- **Decoherence rate (gamma)** ↔ How fast engines drift apart
- **O(N^2) → O(1)** ↔ Classical polling vs coherent propagation

**Interpretation**: In a classical organism, N engines need N*(N-1) messages to
sync state. In a coherent organism, one state change propagates to all entangled
engines instantly. The organism's information flows at "coherence speed" rather
than serial round-trip speed — the same physics that lets photosynthesis achieve
near-perfect energy transfer.