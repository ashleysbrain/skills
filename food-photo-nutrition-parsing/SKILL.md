---
name: food-photo-nutrition-parsing
description: Parse food photos sent via Telegram into nutrition data, log to DB, and trigger rescore
trigger: the principal sends a photo of food, a meal, a nutrition label, or mentions a food photo
version: 2.0
---

# Food Photo Nutrition Parsing

## When to Use
- the principal sends a photo of food, a meal, a nutrition label, or a supplement in Telegram
- the principal references a food photo that wasn't processed
- Any image containing food or nutrition information that should be logged

## The Pipeline

### Step 1: Receive the Image

When the principal sends a photo in Telegram:
1. The image arrives as a file path (MEDIA:/path/to/file) or is already visible in the conversation
2. If the image is already attached and visible, use it directly
3. If referenced by path, use that path

### Step 2: Vision Analysis

Use `vision_analyze` with this exact prompt:

```
Analyze this food photo. Extract ALL of the following as JSON:

1. "food_name": Descriptive name of the food/meal
2. "brand": Brand name if visible (null if not)
3. "is_label": true if a nutrition facts label is clearly visible, false if estimating
4. "nutrition": {
     "calories": number (total for portion shown),
     "protein_g": number,
     "carbs_g": number,
     "fat_g": number,
     "fiber_g": number or null,
     "sugar_g": number or null,
     "sodium_mg": number or null
   }
5. "serving_description": What portion is shown (e.g. "full tray", "half bowl", "1 cup")
6. "confidence": "high" (label readable), "medium" (food clearly identifiable), "low" (unclear)
7. "notes": Any additional context (ingredients visible, preparation method, etc.)

If a nutrition label is visible, READ THE EXACT NUMBERS from it. Do not estimate when the label provides the data.
If no label, estimate macros based on the food identified and the apparent portion size.
Be conservative with estimates - underestimate rather than overestimate protein.

Return ONLY valid JSON, no markdown fences.
```

### Step 3: Validate the Output

- Must have food_name and at least protein_g and calories
- If confidence is "low", note it and ask the principal to confirm
- If protein_g seems unreasonable (>100g for a single meal), flag it

### Step 4: Write to Database

Run the helper script:
```bash
python3 ~/your-workspace/health-private/daily/food_photo_to_nutrition.py \
  --date YYYY-MM-DD \
  --food-name "Food Name" \
  --protein PROTEIN_G \
  --calories CALORIES \
  --carbs CARBS_G \
  --fat FAT_G \
  --fiber FIBER_G \
  --sugar SUGAR_G \
  --sodium SODIUM_MG \
  --hydration-oz HYDRATION_OZ \
  --confidence high|medium|low
```

The script handles:
- Incrementing meals_count for the date
- Adding protein_grams to the daily total
- Recalculating the composite and modifier USING THE CANONICAL ENGINE
- Updating the scorecard nutrition_composite
- **Partial-day scoring**: automatically adjusts targets by time of day so mid-afternoon meals aren't penalized against end-of-day targets

### Step 5: Report Back to the principal

Send a concise confirmation:
```
📸 Logged: [Food Name]
Protein: [X]g | Calories: [X] | Carbs: [X]g | Fat: [X]g
Daily total: [Y]g protein / [Z] meals | Nutrition composite: [score]
```

### Step 6: Trigger Rescore (if applicable)

If the day already has a scorecard with a TWC score:
1. Load the `rescore-engine-usage` skill
2. Build a rescore input with the new nutrition as evidence
3. Run the engine and update the scorecard

## Known Foods Reference

These foods appear regularly and have known values:

| Food | Protein | Calories | Notes |
|------|---------|----------|-------|
| Spinach & artichoke chicken | ~35g | ~400 | Meal, estimate |
| Bone broth (1 cup) | ~10g | ~40 | Per cup, varies by brand |
| Factor meals (various) | varies | varies | READ LABEL - always has one |
| Oikos Triple Zero yogurt | 17g | 100 | Per serving |
| Protein shake (30g scoop) | ~30g | ~200 | Vanilla standard |
| AG1/Athletic Greens | ~2g | ~50 | Supplement baseline |
| 10g collagen | ~10g | ~35 | Unflavored |

## 🚨 CANONICAL ENGINE MANDATE

**NEVER duplicate nutrition scoring formulas in any script or inline calculation.** The canonical engine is at:
```
/<workspace> (FORGE-audited v1.1+)
```

Import and call it for ALL scoring math. The helper script `food_photo_to_nutrition.py` v2.0+ does this correctly via `importlib`. If you ever see a script computing protein_score, meal_frequency_score, hydration_score, composite, or modifier with inline formulas, it is DRIFT and must be fixed.

**The 5 mismatches found on 2026-05-27** (food_photo_to_nutrition.py v1 vs canonical engine):
1. Protein target: script used 114g, canonical is 100g with PIECEWISE curve (not linear)
2. Meal frequency: script used pure linear (meals/3)*100, canonical uses piecewise (1=30, 2=60, 3=85, 4=90)
3. Hydration target: script used 70oz, canonical is 80oz
4. Composite weights: script used 7 different weights (protein 0.35), canonical uses protein 0.22, meal_timing 0.18, glycemic 0.15, etc.
5. Label thresholds: script had adequate=65/gaps=50, canonical has adequate=70/gaps=60

**Impact:** At 110g protein + 3 meals, the buggy script scored composite 77.1 "adequate". The canonical engine scored 54.57 "concerning". A 22-point inflation from formula drift.

## 🕐 Partial-Day Scoring (added 2026-05-27)

The canonical engine now has `compute_nutrition_composite_partial(hour_of_day, **kwargs)` which scales targets by time of day:

- Eating window: 5 AM to 11 PM (18 hours)
- At 3 PM (hour 15): day_fraction = 0.556
- Scaled targets: protein 55.6g (not 100g), meals 2 (not 3), hydration 44.4oz (not 80oz)
- Floor at 0.3 so early morning doesn't get zero targets

**Why this exists:** Scoring 55g protein at 2:30 PM as "concerning" (54.6 composite) is wrong when the user is on pace. With partial-day adjustment, that same 55g scores 69.2 composite at 3 PM because they've hit 99% of their scaled protein target. The helper script uses partial scoring automatically.

**CRITICAL:** End-of-day final scoring (e.g. the rescore engine, nightly cron) should use `compute_nutrition_composite()` (full-day), NOT partial. Partial is only for midday check-ins and real-time food logging.

## Pitfalls

1. **Don't double-log.** Check if a meal was already logged for that date before adding.
2. **Bone broth counts.** 2x bone broth = ~20g protein. This is real nutrition, not zero.
3. **Drinks count for hydration.** Strawberry lemonade, apple juice, etc. add to water_oz. Pass via `--hydration-oz` flag.
4. **Labels beat estimates.** Always read the label first. Only estimate when no label is present.
5. **Partial days.** If it's still early, don't flag the composite as low - it will improve.
6. **Confidence matters.** If vision returns "low" confidence, tell the principal and ask for confirmation rather than logging bad data.
7. **Formula drift.** NEVER re-implement nutrition math inline. Always import the canonical engine. The moment you copy a formula, it starts drifting.
