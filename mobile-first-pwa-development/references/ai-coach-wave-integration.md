# AI Coach + Wave Engine Integration in PWAs

## Overview
This reference documents the pattern for integrating AI-powered chat coaches with scientific wave engines (like Kuramoto models) in Progressive Web Apps, based on the 8D Sleep implementation.

## Integration Pattern

### Data Flow
```
[User Input] 
    → [Coach UI Layer] 
    → [Context Preparation] 
    → [Wave Engine Interface] 
    → [Scientific Computation] 
    → [Result Interpretation] 
    → [Coach Response Generation] 
    → [UI Update]
```

### Context Preparation
Before sending data to the wave engine:
1. Select relevant sleep metrics from recent NIGHTS data
2. Map dimension scores to algorithm-appropriate inputs (e.g., 0-100 scores → natural frequencies)
3. Package contextual information (recent trends, influences, user profile)
4. Apply any necessary normalization or scaling

### Wave Engine Interface
Keep the wave engine interface clean and dependency-free:
```javascript
// Pure function interface - no DOM/browser dependencies
interface WaveEngine {
  setDimensions(scores: number[]): void;
  setCouplingMatrix(matrix: number[][]): void;
  runSimulation(steps: number, dt: number): void;
  getOrderParameter(): number;
  getPhaseCoherence(): number;
  getFrequencySync(): number[];
}
```

### Result Interpretation Layer
Convert raw algorithm outputs to user-friendly insights:
- Order Parameter (r) → Sleep Coherence Score (0-100)
- Phase differences → Dimension synchronization insights
- Frequency distributions → Internal rhythm alignment metrics
- Apply domain-specific thresholds for insight generation

### Coach Response Generation
Template-based responses with dynamic insertion:
```javascript
const responses = {
  highCoherence: `Your sleep dimensions are highly synchronized (coherence: ${coherence}%). 
                  This indicates your biological systems are working in harmony. 
                  Maintain your current routines for optimal recovery.`,
  
  lowCoherence: `Your sleep shows reduced synchronization (coherence: ${coherence}%). 
                 Consider focusing on ${weakestDimension} to improve overall system harmony.`,
                 
  // ... other templates
};
```

## Implementation Details from 8D Sleep Session

### File Structure Additions
```
src/
├── services/
│   ├── wave-engine.js          # Kuramoto model implementation (pure JS)
│   ├── coach-service.js        # AI conversation logic
│   └── integration-service.js  # Context prep + result interpretation
├── components/
│   ├── CoachChat.js            # Chat UI component
│   └── CoachDataCard.js        # Metrics display component
└── utils/
    └── sleep-mappers.js        # Domain-specific data translation
```

### Key Implementation Files

#### services/wave-engine.js
- Pure JavaScript implementation of Kuramoto model
- No dependencies on DOM, window, or browser APIs
- Exportable functions for setting dimensions, coupling matrix, running simulation
- Returns raw numerical outputs (order parameter, phase coherence, etc.)

#### services/coach-service.js
- Manages conversation state and history
- Formats prompts for AI backend with sleep context
- Handles action button callbacks from coach responses
- Manages typing indicators and message timing

#### services/integration-service.js
- Prepares context from app state for wave engine
- Interprets wave engine outputs into coaching insights
- Caches expensive computations when inputs unchanged
- Coordinates timing between user input, processing, and response display

#### utils/sleep-mappers.js
- Mapsleep dimension scores (0-100) → Kuramoto natural frequencies (0.5-2.5 Hz range)
- Converts sleep session objects to algorithm-compatible formats
- Translates wave engine outputs back to domain-specific insights

## Performance Considerations

### Computation Caching
Cache wave engine runs when input dimensions haven't changed significantly:
```javascript
let lastDimensions = null;
let lastResult = null;
const DIMENSION_CHANGE_THRESHOLD = 5; // percent

function getWaveEngineCoherence(currentDimensions) {
  const hasChangedSignificantly = lastDimensions && 
    currentDimensions.some((dim, i) => 
      Math.abs(dim - lastDimensions[i]) / Math.max(lastDimensions[i], 1) * 100 > 
      DIMENSION_CHANGE_THRESHOLD);
      
  if (!hasChangedSignificantly && lastResult) {
    return lastResult.coherence;
  }
  
  // Run fresh computation
  waveEngine.setDimensions(currentDimensions);
  waveEngine.runSimulation(SIMULATION_STEPS, DT);
  const coherence = waveEngine.getOrderParameter() * 100;
  
  lastDimensions = [...currentDimensions];
  lastResult = { coherence, timestamp: Date.now() };
  
  return coherence;
}
```

### Web Worker Evaluation
For simulations requiring >50ms on main thread:
1. Profile typical computation time with realistic data
2. If >16ms (risking dropped frames), consider web worker
3. Transfer only essential data (dimensions matrix, not full sleep objects)
4. Transfer results back via postMessage for UI update

## Testing Strategy

### Unit Testing Wave Engine
- Test mathematical properties (order parameter bounds 0-1)
- Verify symmetry and expected behaviors
- Test edge cases (all same frequencies, extreme differences)
- Compare against known mathematical results where available

### Integration Testing
- Mock AI backend responses for consistent testing
- Verify context preparation produces expected inputs
- Check that coach responses include expected insights based on algorithm outputs
- Test action button callbacks trigger appropriate UI changes

### End-to-End Scenarios
- High coherence state → positive reinforcement responses
- Low coherence state → constructive improvement suggestions
- Rapid state changes → appropriate coaching adaptations
- Action button clicks → expected UI state transitions

## Common Pitfalls and Solutions

### Pitfall: Algorithm Contamination with UI Code
**Symptom:** Wave engine functions accidentally accessing document or window
**Solution:** Keep wave engine in pure JS module; test in Node.js environment to confirm no browser dependencies

### Pitfall: Inappropriate Data Mapping
**Symptom:** Coherence scores don't correlate with user experience
**Solution:** Validate mapping with domain expertise; adjust frequency ranges based on empirical data

### Pitfall: Over-Coaching
**Symptom:** Coach provides too frequent or irrelevant suggestions
**Solution:** Implement coaching frequency limits; use significance thresholds for insight generation

### Pitfall: Performance Degradation
**Symptom:** UI becomes unresponsive during coach interactions
**Solution:** Profile computation time; implement caching; evaluate web worker offloading

## References
- Kuramoto Model: https://en.wikipedia.org/wiki/Kuramoto_model
- Coupled Oscillators in Biology: Strogatz, S. H. (2000). From Kuramoto to Crawford: exploring the onset of synchronization in populations of coupled oscillators.
- 8D Sleep Wave Engine: Divinity Science proprietary implementation (refer to physics-informed-engine-development skill)