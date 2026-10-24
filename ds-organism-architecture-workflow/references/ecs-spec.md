# the specialist engine System (ECS) Specification

## Current Format (Legacy)
```
DS-ECS-DD.SS.NN-vX.Y.Z
```
Where:
- DD = Domain (Organ System, 01-12)
- SS = Subsystem (01-99)
- NN = Specific engine (01-99)
- vX.Y.Z = Semantic version

### Current Domain Mapping
1. Integumentary
2. Skeletal  
3. Muscular
4. Nervous
5. Endocrine
6. Cardiovascular
7. Lymphatic
8. Respiratory
9. Digestive
10. Urinary
11. Reproductive
12. Diagnostic (external tools)

## Enhanced Format Proposal
```
DS-ECS-L.F.D.SS.NN-P.D.vX.Y.Z
```
Where:
- L = Layer (0=Genome, 1=Organism, 2=Product)
- F = Faculty (C=Creative, D=Diagnostic, H=Homeostatic, R=Reproductive, S=Signal)
- D = Development Phase (0=Concept, 1=Prototype, 2=Production, 3=Deprecated)
- SS = Subsystem (01-99)
- NN = Specific engine (01-99)
- P = Platform/Deployment (0=Source, 1=Binary, 2=Container, 3=Service)
- vX.Y.Z = Semantic version

### Example Codes
- DS-ECS-1C0.01.01.01.0.0-v1.0.0 
  (Layer 1=Organism, Faculty C=Creative, DevPhase 0=Concept, Subsys 01, Engine 01, Platform 0=Source)
- DS-ECS-1H1.04.02.01.1.0-v2.1.0
  (Layer 1=Organism, Faculty H=Homeostatic, DevPhase 1=Prototype, Subsys 04=Nervous, Engine 02, Platform 1=Binary)

## Implementation Guidelines
1. Maintain backward compatibility with existing codes where possible
2. All new engines should use enhanced format
3. Create mapping documentation for legacy to enhanced codes
4. Update ecs.py to support both formats during transition
5. Regenerate all documentation and charts when ECS spec changes