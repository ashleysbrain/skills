# PIML Prototype Build — Session Reference (2026-06-09)

## What Was Built
A Physics-Informed Neural ODE prototype for the 8D360 wellness system, built as a handoff artifact for the Rice/UTSA astrophysicist advisor.

## Location
`/<workspace>`

## Files
- `synthetic_data.py` — generates 90-day trajectories using actual ODEs (Process S, Process C, thermoregulation) with the κ coupling matrix
- `neural_ode_8d.py` — PhysicsInformedODE + UnconstrainedODE models (torchdiffeq)
- `train.py` — training, evaluation, visualization, metrics export
- `ADVISOR-REVIEW.md` — the document for the advisor (dark-themed PDF also generated)
- `results/` — plots, metrics.json, saved model weights

## Advisor Questions Embedded in the Review
1. Should κ be static or evolve over time?
2. Is graph diffusion the right framework, or should it be Hamiltonian?
3. Are there true conserved quantities (Noether symmetries)?
4. Should mean-reversion include overshoot (inertial dynamics)?
5. Is the system Hamiltonian, gradient, or mixed?
6. Are there bifurcation points?
7. What's the right noise model — Langevin, Lévy, or jump processes?
8. Can the system be reduced to a lower-dimensional manifold?

## Key Technical Decisions
- torchdiffeq with RK4 solver (step_size=0.25 for next-day, 0.5 for extrapolation)
- Physics loss weight = 0.1 (data loss dominates, physics regularizes)
- Residual network initialized with Xavier gain=0.01 (physics dominates early)
- Gradient clipping at 1.0 for training stability
- Batch size 32, Adam optimizer, StepLR (gamma=0.5 every 50 epochs)

## Environment Fix
- NumPy 2.x incompatible with torch 2.2.2 (compiled against NumPy 1.x)
- Fix: `pip install numpy==1.26.4`

## Build Approach
- First attempt: delegate_task subagent — timed out at 600s with 16 API calls
- Second attempt: built directly in main session — completed successfully, faster
- Lesson: for multi-file code generation with known structure, direct writes beat subagent delegation (confirms subagent-anti-timeout-patterns Pattern 18)
