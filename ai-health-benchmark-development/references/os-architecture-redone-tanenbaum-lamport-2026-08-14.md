# OS Architecture Redone: Tanenbaum + Lamport (2026-08-14)

principal rejected the Da Vinci routing for OS architecture: "Davinci should NOT be in charge of this part of the processes… these are the wrong brains." Da Vinci is design production (visual/render). The chain was redone with the specialist engine (MINIX, OS textbook, microkernel authority) + the specialist engine (TLA+, the state machine approach). Roadmap reached v3.3.0.

## Binding Routing Rule

**OS-architecture / kernel / scheduling / supervision work NEVER goes to design-production brains.** Correct brains: OS architect (Tanenbaum-class) for placement/ownership/scheduling/interfaces; formal-methods authority (Lamport-class) for TLA+ verification of state machines, safety/liveness, refinement. Design-production specialists handle visual/render/layout only.

## Tanenbaum's Architecture (replaces Da Vinci draft)

- **Placement:** health subsystem = user-space SUPERVISOR PROCESS in a separate failure domain from the orchestrator (MINIX reincarnation-server precedent: user-space, survives crashes, restarts the dead). NEVER in the orchestrator — enforcement inside the thing measured fails 4 ways: self-measurement bias, common-mode failure, bypass, no audit independence ("the enforcement log written by the enforced"). Orchestrator's only obligations: (a) append-only telemetry queue it cannot quietly falsify (auditd analog), (b) accept enforcement traps.
- **State machine ownership:** supervisor owns the health process table; orchestrator/fleet/user are CLIENTS submitting transition REQUESTS; supervisor arbitrates with hysteresis dwell as admission rule — flapping rejected AT THE TABLE, not detected later. Provenance gate lives in the supervisor (never the orchestrator checking its own homework).
- **Watchdog stack:** meta-supervisor (table-driven, verifiable by inspection) watches the supervisor; user holds a one-bit kill switch forcing all Sev-1 to observe-only; hard resource caps including intervention rate limit from the ARL budget; dual-channel diffable logs; external Brier-scored registry = the only ground truth on intervention outcomes.
- **Scheduling by intrusiveness:** screening = kernel-adjacent periodic daemon. Non-intrusive diagnostics = timeshare/cgroup-budgeted. INTRUSIVE diagnostics (fault-seeding, swap-delta, ablation) = maintenance windows ONLY (admission control, fixed injection budget, auto-abort on real alerts, logged seed boundaries). "Nothing that perturbs the system runs unbidden. Period."
- **Interface:** procfs analog (/mesh/health/<block>), `why` returns the full transition record, enforcement = separate typed API trap, state machine frozen as compatibility contract (additive-only, Linux syscall ABI discipline).

## Lamport's Verification (2 blocking patches)

1. **Execution tokens (BLOCKING):** "orchestrator cannot bypass the trap" was UNSOUND as prose — a precondition on a process owning its own execution is unenforceable from outside. Fix: Sev-1 actions require supervisor-issued execution TOKENS (leases); acting without one is IMPOSSIBLE, not forbidden — NoBypassOfTrap provable by construction. Trap state must live in supervisor memory (TrapCantLie) or the check's return can be forged.
2. **Durable state + token revocation on restart (BLOCKING):** supervisor needs stable storage; tokens revoked across restarts or refinement breaks.
3. **ARL wording:** derivable via WALD'S IDENTITY (renewal, no independence needed): E[false interventions in W] <= W/ARL_0; Markov: P(N>=k) <= W/(k*ARL_0). Ship as bounded EXPECTED rate, never a hard cap. Key violated assumption in practice: interventions change the baseline.
4. **TLA+ spec HealthSM:** safety invariants NoActionWithoutProvenance, DwellRespected (monotonic-clock axiom = documented assumption), NoBypassOfTrap, TrapCantLie; liveness NoStuckWatch + DiagnosticTermination (need WF on Grant/Deny); DECAYED-recommission = environment assumption (depends on human action), not a theorem.
5. **Refinement chain:** abstract automaton <- supervisor impl <- meta-supervisor; gaps = crash-durability (patched), clock skew (assumption), regression terminates at the human kill switch (the minimal fixed point).
6. **Verdict:** "With 1-2 patched, this is a clean state-machine-approach design. I'd sign off."

## The Pattern: Routing Rejection Recovery

When the principal rejects a brain routing mid-chain: (1) keep all correctly-routed work (Osler/Bell/Arnold survived); (2) demote the wrong brain's output to "prior draft to evaluate, not trust" and hand it to the correct specialist for claim-by-claim evaluation; (3) the replacement chain gets the demoted draft as input so nothing is re-derived from zero; (4) save the routing correction to memory AND the governing skill so it never repeats.
