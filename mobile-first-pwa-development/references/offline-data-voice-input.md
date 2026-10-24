# Offline Data Layer + Voice Input Patterns

IndexedDB local-first storage, Web Speech API integration, and offline
sentiment analysis. All patterns proven in the 8D Sleep PWA (2026-06-19).

## IndexedDB — Multi-Store Local-First Storage

### Schema with Version Bump

```typescript
const DB_NAME = "app-db";
const DB_VERSION = 2;  // Bump when adding stores

const STORE_SESSIONS = "sessions";
const STORE_SCORES = "scores";
const STORE_JOURNALS = "journals";     // Added in v2
const STORE_MEDS = "medications";      // Added in v2

function initDB(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);

    request.onupgradeneeded = () => {
      const db = request.result;
      if (!db.objectStoreNames.contains(STORE_SESSIONS)) {
        db.createObjectStore(STORE_SESSIONS, { keyPath: "date" });
      }
      if (!db.objectStoreNames.contains(STORE_JOURNALS)) {
        // Auto-increment ID + date index for range queries
        const store = db.createObjectStore(STORE_JOURNALS, {
          keyPath: "id", autoIncrement: true,
        });
        store.createIndex("date", "date", { unique: false });
      }
      // ... other stores
    };

    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}
```

### The withStore Wrapper (Eliminates Callback Boilerplate)

```typescript
function withStore<T>(
  storeName: string,
  mode: IDBTransactionMode,
  run: (store: IDBObjectStore) => IDBRequest,
): Promise<T | null> {
  return new Promise((resolve, reject) => {
    if (typeof indexedDB === "undefined") { resolve(null); return; }
    initDB().then((db) => {
      const tx = db.transaction(storeName, mode);
      const store = tx.objectStore(storeName);
      const request = run(store);
      request.onsuccess = () => resolve(request.result as T);
      request.onerror = () => reject(request.error);
      tx.oncomplete = () => db.close();
      tx.onerror = () => reject(tx.error);
    }).catch(reject);
  });
}
```

### CRUD Functions (Each Degrades Gracefully)

```typescript
export interface JournalEntry {
  id?: number;
  date: string;
  timestamp: number;
  source: "voice" | "text";
  transcript: string;
  sentimentScore: number;
  sentimentLabel: "positive" | "neutral" | "negative";
  keywords: string[];
}

export async function saveJournal(entry: Omit<JournalEntry, "id">): Promise<void> {
  if (typeof indexedDB === "undefined") return;
  await withStore(STORE_JOURNALS, "readwrite", (s) => s.put(entry));
}

export async function getJournals(limit = 90): Promise<JournalEntry[]> {
  if (typeof indexedDB === "undefined") return [];
  const all = await withStore<JournalEntry[]>(STORE_JOURNALS, "readonly",
    (s) => s.getAll());
  return (all ?? []).sort((a, b) => b.timestamp - a.timestamp).slice(0, limit);
}
```

### Atomic Wipe (User "Erase My Data")

```typescript
export async function clearAllData(): Promise<void> {
  if (typeof indexedDB === "undefined") return;
  try {
    const db = await initDB();
    const stores = [STORE_SESSIONS, STORE_SCORES, STORE_JOURNALS, STORE_MEDS];
    await new Promise<void>((resolve, reject) => {
      const tx = db.transaction(stores, "readwrite");
      for (const name of stores) tx.objectStore(name).clear();
      tx.oncomplete = () => resolve();
      tx.onerror = () => reject(tx.error);
    });
    db.close();
  } catch { /* best-effort, never throw */ }
}
```

### Verification via Browser Console

```javascript
// Read all journal entries from IndexedDB in browser
new Promise(function(resolve) {
  var req = indexedDB.open('app-db');
  req.onsuccess = function() {
    var db = req.result;
    var tx = db.transaction(['journals'], 'readonly');
    var r = tx.objectStore('journals').getAll();
    r.onsuccess = function() { resolve(JSON.stringify(r.result)); };
  };
})
```

---

## Web Speech API — Voice Transcription

### TypeScript Shims

The `SpeechRecognition` API is not in standard TS DOM types. Declare
minimal interfaces matching the real API surface:

```typescript
interface SpeechRecognitionEventLike {
  resultIndex: number;
  results: {
    length: number;
    [index: number]: { 0: { transcript: string }; isFinal: boolean };
  };
}

interface SpeechRecognitionLike {
  lang: string;
  continuous: boolean;
  interimResults: boolean;
  start: () => void;
  stop: () => void;
  onresult: ((e: SpeechRecognitionEventLike) => void) | null;
  onerror: (() => void) | null;
  onend: (() => void) | null;
}

declare global {
  interface Window {
    SpeechRecognition?: { new (): SpeechRecognitionLike };
    webkitSpeechRecognition?: { new (): SpeechRecognitionLike };
  }
}
```

### Recording Component Pattern

```tsx
const [transcript, setTranscript] = useState("");
const [isRecording, setIsRecording] = useState(false);
const recognitionRef = useRef<SpeechRecognitionLike | null>(null);

const startRecording = useCallback(() => {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) return;

  const recognition = new SR();
  recognition.lang = "en-US";
  recognition.continuous = true;      // true = journaling, false = command
  recognition.interimResults = true;

  recognition.onresult = (e) => {
    let final = "";
    for (let i = e.resultIndex; i < e.results.length; i++) {
      if (e.results[i].isFinal) {
        final += e.results[i][0].transcript + " ";
      }
    }
    if (final) {
      setTranscript((prev) => (prev + " " + final).trim());
    }
  };

  recognition.onerror = () => setIsRecording(false);
  recognition.onend = () => setIsRecording(false);

  recognition.start();
  recognitionRef.current = recognition;
  setIsRecording(true);
}, []);

const stopRecording = useCallback(() => {
  recognitionRef.current?.stop();
  setIsRecording(false);
}, []);
```

**Key points**:
- Must create on user gesture (click), NOT page load — browser requires permission
- `continuous: true` for long-form journaling; `false` for short medication commands
- Accumulate `isFinal` segments into state; interim results are for live display
- `onend` fires when the browser stops listening (silence timeout, manual stop)
- Safari requires `webkit` prefix

---

## Offline Sentiment Analysis (Lexicon-Based)

### Compact AFINN-Style Lexicon

```typescript
const LEXICON: Record<string, number> = {
  // Positive (+1 to +3)
  good: 2, great: 3, calm: 2, peaceful: 3, grateful: 3,
  rested: 3, refreshed: 3, happy: 3, content: 2,
  // Negative (-1 to -3)
  bad: -2, terrible: -3, anxious: -3, stressed: -3,
  tired: -2, exhausted: -3, overwhelmed: -3, lonely: -3,
  // Modifiers (used as multipliers, not sentiment)
  very: 1.5, really: 1.3, extremely: 2, so: 1.2,
  // Negators (valence 0, detected separately)
  not: 0, never: 0, no: 0,
};

const NEGATORS = new Set(["not", "never", "no", "n't", "without", "hardly", "barely"]);
```

### Scoring Algorithm

```typescript
export function analyzeSentiment(text: string): SentimentResult {
  const words = text.toLowerCase().replace(/[^\w\s']/g, " ").split(/\s+/).filter(Boolean);
  let totalScore = 0, scoredCount = 0;
  const foundKeywords = new Set<string>();

  for (let i = 0; i < words.length; i++) {
    const word = words[i];
    const isNegated = i > 0 && NEGATORS.has(words[i - 1]);

    if (word in LEXICON) {
      let valence = LEXICON[word];
      if (isNegated) valence = -valence;        // "not good" → flip
      // Intensifier check on previous word...
      totalScore += valence;
      scoredCount++;
    }

    // Dimensional keyword detection
    for (const [dim, dimWords] of Object.entries(DIMENSION_KEYWORDS)) {
      if (dimWords.includes(word)) foundKeywords.add(word);
    }
  }

  // Normalize: average valence per scored word, clamped to [-1, 1]
  const rawAvg = scoredCount > 0 ? totalScore / scoredCount : 0;
  const normalized = Math.max(-1, Math.min(1, rawAvg / 3));

  return { score: normalized, label: /* ... */, keywords: [...foundKeywords] };
}
```

### Dimensional Keyword Groups

Map free-text keywords to scoring dimensions for future quantitative scoring:

```typescript
const DIMENSION_KEYWORDS: Record<string, string[]> = {
  physical: ["tired", "exhausted", "energy", "body", "pain", "rested", ...],
  psychological: ["anxious", "worried", "stressed", "calm", "happy", ...],
  social: ["family", "friend", "partner", "alone", "lonely", ...],
  environmental: ["noise", "light", "dark", "cold", "room", ...],
  // Extend per application domain
};
```

### Medication Extraction from Free Text

```typescript
const COMMON_MEDS = ["melatonin", "magnesium", "ibuprofen", "ashwagandha", ...];
const DOSE_PATTERN = /(\d+)\s*(mg|ml|mcg|g|ug|iu)\b/gi;

export function extractMedications(text: string): ExtractedMedication[] {
  const lower = text.toLowerCase();
  const found = [];
  for (const med of COMMON_MEDS) {
    const idx = lower.indexOf(med);
    if (idx >= 0) {
      const context = lower.substring(idx - 20, idx + med.length + 30);
      const doseMatch = context.match(DOSE_PATTERN);
      found.push({ name: med, dose: doseMatch?.[0] });
    }
  }
  return found;
}
```

**Proven result** (8D Sleep PWA, 2026-06-19): "I took 3mg of melatonin" →
`{name: "melatonin", dose: "3mg"}`. Sentiment on a mixed journal entry
(anxious + grateful + exhausted + hopeful) correctly scored as neutral
(-0.03), with 9 keywords extracted across psychological, social, and
physical dimensions.

---

## End-to-End Verification Pattern

After building, verify the full pipeline in the browser:

1. `npx tsc --noEmit` — zero errors
2. Start dev server (`npx vite --port 3000 --host`)
3. Navigate to the app, click through each view
4. Type/save a journal entry with mixed sentiment
5. Query IndexedDB via `browser_console(expression=...)` to verify:
   - Entry saved with correct sentiment score
   - Keywords extracted
   - Dimensions populated
6. Quick-add a medication, verify it saved
7. Kill the dev server after verification
