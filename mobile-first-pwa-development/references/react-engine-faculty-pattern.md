# React Engine-Class Faculty Pattern

When adding capabilities to a DS organism product (8D Sleep, etc.), implement
them as **faculties**: pure TypeScript engine modules + thin React UI wrappers.
This keeps engines testable, framework-agnostic, and reusable.

## Engine Module Pattern (`src/engine/FacultyName.ts`)

The engine is a plain class with NO React/DOM dependencies. It holds internal
state, exposes methods, and returns immutable snapshots.

```typescript
export class FacultyEngine {
  private state: FacultyState;

  constructor() {
    this.state = { /* initial state */ };
  }

  /** Mutate state. Called by the UI on user interaction. */
  performAction(input: SomeInput): void {
    this.state.someField = computeThing(input);
  }

  /** Return an immutable snapshot for React to store in useState. */
  getState(): FacultyState {
    return { ...this.state, items: this.state.items.map(i => ({ ...i })) };
  }
}

export function createFaculty(): FacultyEngine {
  return new FacultyEngine();
}
```

Key rules:
- State is private. External code reads via `getState()` only.
- `getState()` returns deep copies (spread + map for arrays) so React sees
  new object references and re-renders correctly.
- Factory function (`createFaculty`) for clean instantiation in `useRef`.

## React Component Pattern (`src/components/FacultyView.tsx`)

The component owns the engine instance via `useRef`, stores the engine's state
snapshot in `useState`, and calls engine methods on user interaction.

```typescript
export const FacultyView: FC<Props> = ({ engine, sessions, onBack }) => {
  // Engine instance — stable across re-renders
  const facultyRef = useRef<FacultyEngine | null>(null);
  if (!facultyRef.current) {
    facultyRef.current = createFaculty();
  }
  const faculty = facultyRef.current;

  // React state — snapshot of engine state
  const [fState, setFState] = useState<FacultyState>(() => faculty.getState());

  // One-time setup (rebuild plan, etc.)
  const initDone = useRef(false);
  useEffect(() => {
    if (initDone.current || sessions.length === 0) return;
    initDone.current = true;
    faculty.buildFromData(sessions);
    setFState(faculty.getState());
  }, [faculty, sessions]);

  // Action handler — mutate engine, snapshot state
  const handleAction = useCallback(() => {
    faculty.performAction(/* input */);
    setFState(faculty.getState());
  }, [faculty]);

  return (
    <div>
      {/* Render from fState, NOT from faculty.getState() directly */}
      <span>{fState.someField}</span>
      <button onClick={handleAction}>Do Thing</button>
    </div>
  );
};
```

## Timer/Interval Pattern (the bug that caused hours of debugging)

When the engine has a timer (countdown, tick, etc.), manage the interval via
a ref and tie it to the React state value:

```typescript
const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

useEffect(() => {
  if (fState.timerActive && !intervalRef.current) {
    intervalRef.current = setInterval(() => {
      faculty.tick();
      setFState(faculty.getState());
    }, 1000);
  } else if (!fState.timerActive && intervalRef.current) {
    clearInterval(intervalRef.current);
    intervalRef.current = null;
  }

  return () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };
}, [fState.timerActive, faculty]);
```

### Why NOT to use `forceRender`

```typescript
// BROKEN — stale closures in useEffect dependencies
const [, forceRender] = useState(0);
const state = faculty.getState(); // read during render

const tickTimer = useCallback(() => {
  if (state.timerActive) {  // ← STALE: captures this render's value
    faculty.tick();
    forceRender(n => n + 1);
  }
}, [faculty, state.timerActive]); // ← state.timerActive from THIS render
```

The `state.timerActive` in the callback is captured at render time. After
`faculty.startTimer()` mutates the engine's internal state, the callback's
closure still sees the old `false` value. The interval never starts.

React StrictMode makes this worse: every effect runs twice (run → cleanup →
run again). The cleanup clears the interval that was just created, and the
re-run creates a new one — but if the state value in the dependency array
is stale, the re-run sees `false` and skips interval creation entirely.

### The fix

Always snapshot engine state into React state immediately after mutation:

```typescript
const toggleTimer = useCallback(() => {
  if (fState.timerActive) {
    faculty.stopTimer();
  } else {
    faculty.startTimer();
  }
  setFState(faculty.getState()); // ← React state updated
}, [faculty, fState.timerActive]); // ← React state in deps, not engine field
```

## Integration with Scoring Engine

When a faculty needs scoring data (like the Wave Coach reading dimension scores),
add a `getResult()` method to the scoring engine that returns a full snapshot:

```typescript
// In SleepScoringEngine.ts
getResult(): ScoringResult {
  return {
    dimensionScores: new Map(this.dimensionScores),
    twcScore: this.twcScore,
    twcTrend: this.twcTrend,
    phaseCoherence: this.phaseCoherence,
    sleepQualityScore: this.sleepQualityScore,
    dimensionHistory: new Map(this.dimensionHistory),
    twcHistory: [...this.twcHistory],
  };
}
```

The faculty calls `engine.getResult()` to build its context — no direct field
access needed. This keeps the scoring engine's internals private and gives the
faculty a stable snapshot to work with.

## Session Reference

Pattern derived from the 8D Sleep Wave Coach + Quartz Task Engine build
(2026-06-19). The WaveCoach engine has 8 query patterns, contextual greetings,
and cross-faculty action dispatch. The QuartzTaskEngine has a PID-controlled
wind-down planner with 6 timed steps that auto-personalize to the weakest
sleep dimension.
