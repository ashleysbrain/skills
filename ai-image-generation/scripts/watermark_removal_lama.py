#!/usr/bin/env python3
"""
Watermark removal via template matching + LaMa inpainting.

WINNING approach discovered through 10+ iterations (2026-08-07):
  Phase 1: Extract watermark pattern from clean background corner.
  Phase 2: Template match (cv2.matchTemplate) to find ALL watermark locations.
  Phase 3: Refine mask with local-shift verification (remove false positives).
  Phase 4: Hard-lock face box to protect eyes/teeth/nails.
  Phase 5: LaMa inpainting on the final mask.

This replaces the earlier alpha-inversion-only approach which caught only 14K
of ~148K actual watermark pixels.

PREREQUISITES:
  uv venv <agent-home>/image-tools-venv --python 3.11
  uv pip install --python <agent-home>/image-tools-venv/bin/python3.11 \
      iopaint opencv-python-headless "numpy<2"
  mkdir -p ~/.cache/torch/hub/checkpoints
  curl -L -o ~/.cache/torch/hub/checkpoints/big-lama.pt \
    "https://github.com/Sanster/models/releases/download/add_big_lama/big-lama.pt"

USAGE:
  <agent-home>/image-tools-venv/bin/python3.11 scripts/watermark_removal_lama.py \
      input.jpg output.png

APPROACHES THAT FAILED (do not retry):
  - Tesseract OCR: returns 0 regions on semi-transparent watermarks (conf < 15)
  - Top-hat morphological filter (any kernel size): catches natural features
  - Alpha inversion alone: mathematically correct but mask only catches 14K of 148K pixels
  - Shift threshold >3 without face protection: destroys eyes/teeth/nails
  - Shift threshold >3 with face box but too narrow background range: misses gradient BG
  - FFT notch filter: changes 89% of pixels, destroys image
  - PIL/Pillow median fill: blurry, smeared, user rejected
  - GrabCut person segmentation: classifies watermark-on-background as person (47% area)

TUNING PER IMAGE:
  - FACE_BOX: adjust to cover the subject's face. Default is for a centered portrait.
  - TEMPLATE_REGION: adjust to a clean background area (corner without subject).
  - TEMPLATE_SIZE: 40x80 worked for "aarzoo" word watermark. Adjust for different text.
  - MATCH_THRESHOLD: 0.35 catches most. Lower to 0.25 for fainter watermarks (more false+).
  - HEART_REGION: set coordinates of any opaque icon/logo. Set to None if none present.
"""
import sys, os
import numpy as np
from PIL import Image
import cv2
import torch

INPUT = sys.argv[1] if len(sys.argv) > 1 else sys.exit("Usage: script.py <input> <output> [face_y0 face_y1 face_x0 face_x1]")
OUTPUT = sys.argv[2] if len(sys.argv) > 2 else sys.exit("Usage: script.py <input> <output> [face_y0 face_y1 face_x0 face_x1]")

# Optional face box override via CLI args
if len(sys.argv) >= 6:
    FACE_Y0, FACE_Y1, FACE_X0, FACE_X1 = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
else:
    # Default for centered portrait (adjust per image)
    FACE_Y0, FACE_Y1 = 340, 540
    FACE_X0, FACE_X1 = 390, 710

# Template extraction region (clean background corner)
TEMPLATE_Y0, TEMPLATE_Y1 = 0, 100
TEMPLATE_X0, TEMPLATE_X1 = 0, 200

# Template size (matches the watermark word width)
TEMPLATE_H, TEMPLATE_W = 40, 80

# Match threshold (lower = more sensitive, more false positives)
MATCH_THRESHOLD = 0.35

# Heart/icon region (set to None or adjust coordinates)
HEART_REGION = (40, 125, 970, 1060)  # (y0, y1, x0, x1)
HEART_THRESHOLD = 170  # gray brightness

img = np.array(Image.open(INPUT).convert("RGB"))
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY).astype(float)
h, w = gray.shape
print(f"Image: {w}x{h}")

# === STEP 1: Extract watermark template from clean background ===
bg_region = gray[TEMPLATE_Y0:TEMPLATE_Y1, TEMPLATE_X0:TEMPLATE_X1]
bg_clean = cv2.medianBlur(bg_region.astype(np.uint8), 15).astype(float)
watermark_template = np.clip(bg_region - bg_clean, 0, 50)
template = watermark_template[0:TEMPLATE_H, 0:TEMPLATE_W].astype(np.uint8)
template_norm = cv2.normalize(template, None, 0, 255, cv2.NORM_MINMAX)
print(f"Template: {template.shape}, nonzero pixels: {(template > 2).sum()}")

# === STEP 2: Template match across full image ===
match = cv2.matchTemplate(gray.astype(np.uint8), template_norm, cv2.TM_CCOEFF_NORMED)
print(f"Template match: best={match.max():.3f}, >0.35: {(match > 0.35).sum()} locations")

# === STEP 3: Build mask from matched locations ===
wm_mask = np.zeros((h, w), dtype=bool)
for y in range(match.shape[0]):
    for x in range(match.shape[1]):
        if match[y, x] > MATCH_THRESHOLD:
            wm_mask[y:y+TEMPLATE_H, x:x+TEMPLATE_W] = True

# === STEP 4: Refine with local shift verification ===
local_med = cv2.medianBlur(gray.astype(np.uint8), 31).astype(float)
shift = gray - local_med
wm_mask = wm_mask & (shift > 1)

# === STEP 5: Add opaque elements (heart icon, logo) ===
if HEART_REGION:
    hy0, hy1, hx0, hx1 = HEART_REGION
    heart = np.zeros((h, w), dtype=bool)
    heart[hy0:hy1, hx0:hx1] = gray[hy0:hy1, hx0:hx1] > HEART_THRESHOLD
    wm_mask = wm_mask | heart

# === STEP 6: Build and dilate mask ===
mask_u8 = (wm_mask.astype(np.uint8)) * 255
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
mask_u8 = cv2.dilate(mask_u8, kernel, iterations=2)

# MANDATORY: Force-zero the face box AFTER dilation
mask_u8[max(0, FACE_Y0-10):FACE_Y1+10, max(0, FACE_X0-10):FACE_X1+10] = 0

wm_count = (mask_u8 > 127).sum()
face_check = mask_u8[FACE_Y0-10:FACE_Y1+10, FACE_X0-10:FACE_X1+10]
print(f"Final mask: {wm_count} ({wm_count/(h*w)*100:.1f}%)")
print(f"Face box pixels in mask: {(face_check > 127).sum()} (must be 0)")

if wm_count == 0:
    print("WARNING: No watermark detected. Saving original.")
    Image.fromarray(img).save(OUTPUT)
    sys.exit(0)

# === STEP 7: Run LaMa inpainting ===
def pad_mod(arr, mod=8):
    hh, ww = arr.shape[:2]
    ph = (mod - hh % mod) % mod
    pw = (mod - ww % mod) % mod
    if len(arr.shape) == 3:
        return np.pad(arr, ((0, ph), (0, pw), (0, 0)), mode="reflect")
    return np.pad(arr, ((0, ph), (0, pw)), mode="constant")

LAMA_PATH = os.path.expanduser("~/.cache/torch/hub/checkpoints/big-lama.pt")
print(f"Loading LaMa from {LAMA_PATH}...")
img_p = pad_mod(img, 8)
mask_p = pad_mod(mask_u8, 8)
model = torch.jit.load(LAMA_PATH, map_location="cpu")
model.eval()
it = torch.from_numpy(np.transpose(img_p, (2, 0, 1)).astype("float32") / 255.0).unsqueeze(0)
mt = torch.from_numpy((mask_p > 127).astype("float32")).unsqueeze(0).unsqueeze(0)

print("Running LaMa inpainting...")
with torch.no_grad():
    out = model(it, mt)

result = (out.squeeze(0).numpy().transpose(1, 2, 0) * 255).astype("uint8")[:h, :w]

# Save as JPEG for reliable Telegram delivery
if OUTPUT.endswith(".png"):
    OUTPUT_JPG = OUTPUT.rsplit(".", 1)[0] + ".jpg"
else:
    OUTPUT_JPG = OUTPUT

Image.fromarray(result).save(OUTPUT, quality=95)
Image.fromarray(result).save(OUTPUT_JPG, "JPEG", quality=95)
print(f"\nSaved: {OUTPUT}")
print(f"Saved: {OUTPUT_JPG}")
