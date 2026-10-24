# Image Concept Re-Evaluation Results (2026-08-13)

**Context:** principal sent 30 physics/math images. Initial evaluation rejected several as "decorative." principal corrected: the Bloch sphere was wrongly rejected. Full re-evaluation of ALL rejected/noted concepts followed, each evaluated on its MATH not its LABEL.

**Specialists:** the specialist engine (Caltech/Santa Fe) + the specialist engine (Kyoto)

## The Bloch Sphere Lesson (binding)

A concept's LABEL ("quantum," "mystical," "philosophical") tells you nothing about its math content. The Bloch sphere survived because underneath the quantum label is genuine Riemannian geometry. Apply the same test to every concept.

## Results: 8 Adopted, 1 Partial, 1 Aspirational, 3 Confirmed Rejected

### TIER 1 — ADOPTED (genuine utility)

#### 1. Cymatics → Spectral/Frequency-Domain Drift Detection (THE NEXT BLOCH SPHERE)
- **Label:** "Vibration creates pattern" (mystical)
- **Actual math:** Fourier analysis / Welch power spectral density
- **Why it matters:** All 4 existing drift detectors are time-domain. Zero frequency-domain. A model degrading on a 7-day cycle (weekly retraining) is invisible to CUSUM/changepoint until damage accumulates. Welch PSD catches it from the first full cycle.
- **Resonance amplification:** Agent perturbed at characteristic frequency degrades 9x faster than off-resonance. Enables accelerated degradation testing.
- **Cost:** ~10 lines of scipy.signal.welch. Zero new telemetry. Needs 30+ daily snapshots.
- **Computed evidence:** FFT of simulated health time series cleanly recovered 7-day (47.2% power), 30-day (10.8%), 91-day (23.8%) cycles.

#### 2. Bloch Sphere → State Geometry (Rank 4)
- **Label:** "Quantum" 
- **Actual math:** Spherical coordinates on probability distribution. Classical geometry.
- **theta** = JS distance from baseline (drift magnitude). phi = drift direction (WHICH competing well). r = decisiveness (committed vs mixed). t_c = time-to-collapse (rigid vs exploratory).
- **Key equations:** theta = (pi/2) * d_JS / d_JS_max. phi = atan2(d_JS_persona, d_JS_shortcut). r = 1 - H_decision/log2(K). Composite H_Bloch = (theta_H, phi_H, r_H, t_c).
- **Why it matters:** Scalar score is a projection R^7 -> R. Preimage is 6-dimensional level surface. Two agents with same score can have completely different failure modes.

#### 3. 11D Brain Geometry + Adaptive Qudit → Participation Ratio
- **Label:** "11-dimensional neuroscience" + "quantum dimension selection"
- **Actual math:** Participation Ratio PR = (sum lambda_i)^2 / sum(lambda_i^2)
- **Why it matters:** Different agents need different numbers of scoring dimensions. PR tells us empirically. BIC/AIC overfit (select ambient dimension). PR is robust.
- **Implementation:** SVD on centered telemetry matrix, 20 lines of numpy.
- **Tested:** PR=3.07 for true d=4 low noise, 4.40 with realistic noise. BIC selected d=10 (wrong).

#### 4. ARIA 6-Layer Memory → Multi-Scale EMA (Wavelet Decomposition)
- **Label:** "Neurobiologically-inspired hierarchical memory stack"
- **Actual math:** 5-tier exponential moving average = discrete wavelet decomposition
- **Tiers:** Working(1d), Short-term(7d), Medium(30d), Long-term(90d), Archival(365d)
- **Why it matters:** Regime shifts detected when short-term EMA crosses below long-term EMA. ~20 bytes state per agent. Near-zero cost.

#### 5. SDQN → Ring Topology for Distributed Endpoints
- **Label:** "Software-Defined Quantum Network"
- **Actual math:** Spectral graph theory. Ring topology for distributed benchmark endpoints.
- **Why it matters:** Ring is 2-edge-connected (no SPOF), 6 edges (vs 15 for full mesh), synchronizability ratio 4.0.

#### 6. Representation Shifts → Gauge Invariance
- **Label:** "History of physics representation shifts"
- **Actual math:** Spearman rho = 1.000 across raw/z-score/percentile/rank gauges. Ordering is invariant.
- **Design principle:** Benchmark scores should be invariant under prompt reparameterization.

### TIER 2 — PARTIAL

#### 7. Fibonacci / Golden Ratio
- **What works:** Fibonacci-spaced RG block sizes [1,2,3,5,8,13,21,34,55,89,144] eliminate aliasing (phi = most irrational = zero resonance). Zeckendorf logarithmic scoring scale.
- **What FAILED:** phi-Kronecker sampling for contamination resistance. Discrepancy 0.0208 vs uniform 0.0100. The "most irrational = contamination resistant" argument does not hold in 1D.

### TIER 3 — ASPIRATIONAL

#### 8. TDA / Persistent Homology
- Rigorous math (Betti numbers, Vietoris-Rips complexes). But heavy compute. Park for v2.0.

### TIER 4 — CONFIRMED REJECTED (with math justification)

#### 9. Quantum Gates (Hadamard, CNOT, Pauli)
- Hadamard = FIM eigenbasis rotation (already have it). CNOT = coupling constants (already have it). Pauli = scoring updates (already have it). No new math.

#### 10. Quantum Memory
- Standard DB hierarchy. No quantum hardware. No decoherence physics at room temperature.

#### 11. Brain-Heart Model
- Already implemented as COG + ALIGN coupling. System 1/System 2 encoded in dimension architecture.

#### 12. Self-Trust Framework
- Extract one concept: detection SLA ("given drift magnitude delta, detect with probability p within T days" = Neyman-Pearson detection theory). Discard the rest.

## Image OCR Fallback

When vision_analyze fails on non-vision providers:
```bash
# Upscale 3x with PIL, then tesseract
python3 -c "from PIL import Image; img=Image.open('img.jpg'); w,h=img.size; img.resize((w*3,h*3),Image.LANCZOS).save('img_3x.png')"
tesseract img_3x.png stdout --psm 6  # uniform block
tesseract img_3x.png stdout --psm 11 # sparse text
tesseract img_3x.png stdout --psm 4  # column detection for math
```
Process in terminal batches to avoid per-image timeout. For batches of 10+ images, use a shell loop with individual PIL resize per image (shared /tmp output path fails silently).
