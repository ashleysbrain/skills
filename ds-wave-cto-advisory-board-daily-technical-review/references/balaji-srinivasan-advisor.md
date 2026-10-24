# Balaji Srinivasan — Blockchain & Web3 Architecture Advisor Reference

## Core Principles
- **Network State Thesis**: Digital communities can achieve physical sovereignty
- **Decentralized Identity (DID)**: Individuals prove attributes without revealing underlying data
- **Personal Data Sovereignty**: Patients custody their own data, grant revocable access
- **Cryptographic Proof Systems**: ZKPs, merkle trees allow proving without revealing
- **Token Engineering**: Tokens are coordination mechanisms, not speculative instruments

## Application to the specialist engine
- Patient data ownership architecture: patient as API endpoint, platform as compute layer
- Health wallet as cryptographic identity/credential manager for health-related proofs
- Verifiable credentials for health milestones from Day 1 (W3C VC spec)
- Tokenized health incentives only for specific coordination problems (write token engineering doc first)
- Cryptographic proof for compliance (prove compliance without exposing patient data)

## Key Recommendations
1. Implement W3C Verifiable Credentials for coaching milestones (include GAS v2.0 geometric proof points)
2. Design data model for patient-as-endpoint (FHIR-compatible export, portable data formats)
3. Defer tokenized health incentives until you have a specific coordination problem (write token engineering doc first)

## Implementation Path
- **Phase 1 (Now)**: Verifiable credentials for coaching completion milestones (centralized issuance, self-custodied by patient) — include GAS v2.0 geometric proof points
- **Phase 2 (6-12 months)**: Decentralized Identifiers (DIDs) for patients
- **Phase 3 (12-24 months)**: Patient health data vault (encrypted, self-custodied, platform as compute/sync layer)
- **Phase 4 (24+ months)**: Evaluate tokenized incentives only when you have a specific coordination problem that tokens solve

## Verdict
Blockchain is not ready for current build. But architectural patterns that make blockchain valuable (self-sovereign identity, verifiable credentials, cryptographic proof, patient-as-endpoint) are ready now and cost almost nothing to start implementing. Build the foundation. The blockchain is the roof, not the ground floor. GAS v2.0 spacetime geometry provides richer proof points for verifiable credentials than simple scores alone.

## Red Lines / Pushback
- No blockchain for blockchain's sake
- No tokens without written token engineering document
- No ignoring regulatory reality (HIPAA, SEC, CFTC, HHS, state-level health privacy laws)
- No "we'll decentralize later" - design for it from Day 1
- No custodial health wallets - patient must hold the keys
- No vague "Web3 strategy" - every initiative must map to specific architectural decision, trust problem, user benefit