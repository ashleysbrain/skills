# Image Editing / Inpainting Provider Landscape

When the user needs to EDIT an existing image (watermark removal, object removal,
background swap, text removal) rather than generate from scratch, the provider
landscape is DIFFERENT from text-to-image generation.

## When to Use This Reference

- User asks to remove watermarks, text, objects from an image
- User asks to edit, modify, or alter an existing image
- User asks to inpaint, heal, or fill regions of an image
- `image_generate` with `image_url` returns 403 (FAL edit endpoint blocked)

## Provider Priority for Image EDITING

1. **xAI Grok** — best quality editor per user experience. Needs credits
   (spending limit at grok.com/?_s=usage or console.x.ai). Returns 403 when
   `personal-team-blocked:spending-limit`. The spending limit does NOT
   auto-reset — it requires manual intervention (raise limit or add payment).

2. **OpenRouter image models** — `text+image -> text+image` chat completions.
   Needs $5 minimum credits. Cheapest viable option:
   - `google/gemini-2.5-flash-image` ($0.30/M tokens, ~$0.02/image)
   - `openai/gpt-5-image-mini` ($2.50/M tokens)
   - `openai/gpt-5-image` ($10/M tokens)
   
   API format (verified working, blocked only on credits):
   ```python
   payload = {
       "model": "google/gemini-2.5-flash-image",
       "messages": [{
           "role": "user",
           "content": [
               {"type": "text", "text": "Remove all watermark text from this image"},
               {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
           ]
       }]
   }
   # POST to https://openrouter.ai/api/v1/chat/completions
   ```

3. **FAL.ai direct key** — set `FAL_KEY` in `<agent-home>/.env`. Free tier has
   credits. Unblocks FLUX edit models through the operator agent `image_generate` tool.
   The Nous-managed FAL gateway returns 403 on the edit endpoint; a direct
   key bypasses this.

4. **IOPaint / LaMa (self-hosted, FREE, no API)** — gold standard for
   watermark/object removal. This is what cleanup.pictures runs under the
   hood. VERIFIED WORKING 2026-08-06.
   - Install: `uv venv <agent-home>/image-tools-venv --python 3.11 && uv pip install iopaint opencv-python-headless "numpy<2"`
   - **PITFALL:** `iopaint download --model=lama` CLI HANGS (timeouts after 120s+).
     Download directly via curl instead:
     ```bash
     mkdir -p ~/.cache/torch/hub/checkpoints
     curl -L -o ~/.cache/torch/hub/checkpoints/big-lama.pt \
       "https://github.com/Sanster/models/releases/download/add_big_lama/big-lama.pt"
     ```
     Model is ~196MB.
   - **PITFALL (numpy version conflict):** opencv-python-headless installs
     numpy 2.x, but torch 2.2.2 was compiled against numpy 1.x →
     `RuntimeError: Numpy is not available`. Fix: pin `numpy<2` during install.
   - **PITFALL (pytesseract hangs):** `import pytesseract` hangs in some venv
     configs (env scanning). Call the binary directly:
     `subprocess.run(["/usr/local/bin/tesseract", img_path, "-", "tsv"], ...)`
   - Working LaMa script: `scripts/watermark_removal_lama.py`

5. **ComfyUI** — local inpainting workflows. Heavy setup but full control.

## CRITICAL: Semi-Transparent Watermark Detection (Hard-Won Lesson)

**THE PROBLEM:** Semi-transparent watermarks (like "aarzoo" text overlaid at
~11% opacity) are nearly INVISIBLE to pixel-level detection methods because
they are indistinguishable from natural image texture (skin highlights, fabric
folds, hair sheen). The following approaches ALL FAILED on a real headshot:

| Approach | Result | Why It Failed |
|----------|--------|---------------|
| Tesseract OCR | 0 regions detected | Semi-transparent text has confidence < 15 |
| Top-hat morphology (k=5,7,9,11,15,21) | Catches natural features | Skin/hair/fabric all create similar local contrast |
| LaMa with loose mask (29% coverage) | Destroyed the person | Over-smoothed everything in mask |
| LaMa with tight mask (6.7% coverage) | Missed the watermark | Mask only caught the most extreme pixels |
| FFT notch filter | Changed 89% of pixels | Destroyed the image |
| PIL/Pillow median fill | Blurry, smeared | User rejected as "didn't work" |

**THE SOLUTION (refined 2026-08-07, 10+ iterations): Template Matching + LaMa.**

The alpha inversion formula is mathematically correct but produces INCOMPLETE masks
(tiled extraction caught only 14,522 of ~147,981 actual watermark pixels — the watermark
is NOT uniformly tiled, it scatters in different densities). The winning pipeline:

### Step 1: Extract watermark template from clean background
```python
bg_region = gray[0:100, 0:200]  # Top-left corner (adjust per image)
bg_clean = cv2.medianBlur(bg_region.astype(np.uint8), 15).astype(float)
watermark_template = np.clip(bg_region - bg_clean, 0, 50)
template = watermark_template[0:40, 0:80].astype(np.uint8)
template_norm = cv2.normalize(template, None, 0, 255, cv2.NORM_MINMAX)
```

### Step 2: Template match across full image
```python
match = cv2.matchTemplate(gray.astype(np.uint8), template_norm, cv2.TM_CCOEFF_NORMED)
# match.shape = (H - template_h + 1, W - template_w + 1)
```

### Step 3: Build mask from matched locations
```python
wm_mask = np.zeros((h, w), dtype=bool)
for y in range(match.shape[0]):
    for x in range(match.shape[1]):
        if match[y, x] > 0.35:
            wm_mask[y:y+40, x:x+80] = True
```

### Step 4: Refine with local shift verification
```python
local_med = cv2.medianBlur(gray.astype(np.uint8), 31).astype(float)
shift = gray - local_med
wm_mask = wm_mask & (shift > 1)  # Remove false positives on flat areas
```

### Step 5: Add opaque elements (heart icon, logo)
```python
heart = np.zeros((h, w), dtype=bool)
heart[40:125, 970:1060] = gray[40:125, 970:1060] > 170  # Adjust per image
```

### Step 6: MANDATORY face box protection (for portraits)
```python
face_y0, face_y1 = 340, 540  # Adjust per portrait
face_x0, face_x1 = 390, 710
mask_u8[face_y0-10:face_y1+10, face_x0-10:face_x1+10] = 0  # FORCE ZERO after dilation
```

### Step 7: Run LaMa
```python
# pad to mod-8, run LaMa JIT model, crop back
```

### Results comparison (same image, real headshot):
| Method | Mask coverage | Face damage | Watermark removed |
|--------|:---:|:---:|:---:|
| Top-hat k=9 + LaMa | 11.7% | No (but missed WM) | Partial |
| Alpha inversion + LaMa | 10.5% | No | Partial (14K of 148K) |
| Shift>3 threshold + LaMa | 17.1% | YES (eyes/teeth) | Yes |
| Shift>3 + face box + LaMa | 11.7% | No | Yes (best balance) |
| **Template matching + LaMa** | **16.5%** | **No (face locked)** | **Best** |

### Key pitfalls discovered:
1. **Background is NOT uniform gray.** Headshot backgrounds have gradients (150 at top-left
   to 131 at top-right to 115 at mid-right). Single-range detection misses half the image.
2. **LaMa destroys bright facial features.** Teeth, eye whites, and fingernails all have
   the same pixel signature as watermark text (bright relative to surroundings). A face box
   MUST be hard-locked to zero after all mask processing.
3. **Alpha inversion is necessary but not sufficient.** The formula correctly removes
   watermark brightness where it is detected, but tiled mask extraction misses non-uniform
   watermark distribution. Use template matching instead for comprehensive coverage.
4. **pytesseract import hangs** in some venv configs. Call the binary directly via subprocess.

## Grok Spending Limit (Common Blocker)

The error `personal-team-blocked:spending-limit` does NOT auto-reset monthly.
It is a spending cap on the xAI account that requires manual intervention:
raise the limit or add a payment method at grok.com/?_s=usage or console.x.ai.
This is a 2-minute fix on the user's end.

## Decision Framework

| Situation | Best Path |
|-----------|-----------|
| Grok credits available | Use Grok (best quality, surgical precision) |
| Need immediate result, no credits | Add $5 to OpenRouter, use Gemini Flash Image |
| Semi-transparent repeating watermark (portrait) | Template matching + LaMa + face box lock |
| Semi-transparent repeating watermark (no faces) | Template matching + LaMa |
| Opaque watermark / logo / icon | LaMa inpainting alone (local, free) |
| Recurring watermark removal (process flow) | Install IOPaint/LaMa locally |
| Need FLUX editing via the operator agent tool | Set FAL_KEY in .env (free tier) |
| Scientific diagram label fix | PIL/SVG code approach (see labeled-anatomy-diagram-pipeline.md) |

## User Preferences for Image Editing (from 2026-08-07 session)

1. **Surgical precision required.** The user rejects any approach that damages the
   subject (eyes, teeth, fingernails, hair). LaMa masks MUST protect facial features.
2. **Research before iterating.** When threshold tuning fails after 2-3 attempts, STOP
   and research alternative approaches. The user explicitly demanded this: "go do
   research and figure out a different way."
3. **Deliver JPEG, not PNG.** Some PNG paths fail to deliver on Telegram. JPEG is reliable.
4. **Send via `MEDIA:/path.jpg`.** Copy to a clean filename if the path is complex or if
   a previous delivery of the same path may have been cached.
5. **Never settle for "close enough."** If watermarks remain on any area (background,
   hair, clothing), keep iterating until clean. The user accepted "closest yet" but
   immediately pushed for the remaining gap to be closed.
