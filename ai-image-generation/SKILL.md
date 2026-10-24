---
name: ai-image-generation
description: "Generate images using AI models via CLI tools and APIs. Covers Nano Banana (Gemini), OpenAI DALL-E/gpt-image, inference.sh, and direct Gemini API calls. Includes provider landscape, setup steps, and the user's workflow preferences."
version: 1.0.0
author: the operator agent Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [creative, image-generation, nano-banana, gemini, dall-e, gpt-image, inference-sh, visual-assets]
    category: creative
---

# AI Image Generation

Generate production-quality images using AI models. This skill covers the tools
available in this environment, how to choose between them, and the user's
workflow preferences for image generation tasks.

## When to Use

- User needs images for social media posts, LinkedIn, marketing, or branding
- User asks to generate, create, or produce visual assets
- User says "make an image", "generate a picture", "design a graphic"
- Any task that requires turning a text prompt into a visual output

## CRITICAL: Tool Selection Priority

**DO NOT hand-code HTML/CSS/SVG/Puppeteer images when AI image generation is
available.** The user has explicitly corrected this: "Why aren't we using nano
banana for this?" Hand-coded programmatic images look amateur ("middle school
PowerPoint") and waste turns going back and forth.

Priority order:

1. **xAI Grok Imagine** — when `xai-oauth` is logged in or `XAI_API_KEY` is set; prefer `grok-imagine-image-quality` for brand heroes / LinkedIn (see `references/grok-xai-image-path.md`)
2. **Nano Banana** (Gemini-powered CLI) — strong quality-to-speed when Gemini key is billed
3. **the operator agent `image_generate` tool** — only after confirming backend (FAL vs xAI); on Nous/FAL HTTP 402, fall through to xAI plugin immediately
4. **Gemini API direct** — fallback if Nano Banana CLI has issues
5. **OpenAI DALL-E/gpt-image** — if a direct OpenAI API key is available
6. **ComfyUI** — for batch/local workflows requiring fine control
7. **inference.sh** — if authenticated (`infsh login`)

**Never use PIL/Pillow programmatic drawing for ordinary production images** (brand heroes, mood art, product shots). Exception: multi-leader **scientific anatomy diagrams** where diffusion fails label geometry — see "Labeled science diagrams" below and skill `physiomorphic-ai-public-field-teaching`.

### HTML/CSS Fallback (when ALL diffusion is down AND user requests local build)

When FAL=402, xAI=403, Nano Banana unavailable, AND the user explicitly asks to
"build it here" or "try to build it locally," HTML/CSS rendering is the correct
fallback — NOT Pillow. Pillow cannot do anti-aliased typography and produces
output the user rejects as "programmer art" (rejected 6x in one session).

HTML/CSS fallback pipeline (verified 2026-08-03):
1. Write HTML file with real web fonts (Google Fonts: Cormorant Garamond, Inter)
2. SVG for any constellation/network/illustration elements with glow filters
3. Golden ratio composition (text zone = 38.2%, visual zone = 61.8%)
4. Serve: `cd assets_dir && python3 -m http.server 8753 &`
5. Navigate browser to localhost, screenshot via `browser_vision`
6. Deliver via `MEDIA:/path/to/screenshot.png`

Quality requirements for HTML fallback (user-validated):
- Golden ratio / Da Vinci composition REQUIRED. No flat text zones.
- Graphics must COMMUNICATE a message (announcement, comparison, architecture).
  Quote cards that just display a sentence are rejected as "just copying words."
- Cormorant Garamond for serif elegance, Inter for labels/meta.
- Navy gradient background, gold nodes, film grain, vignette, gold border corners.
- Text must be fully readable: solid dark veil behind text zone, pure white type.
- Body constellation should form an organic silhouette with multi-tier node glow.

IMPORTANT: This fallback is for when the user says "build it here." If the user
hasn't explicitly asked for local generation and diffusion is down, still TELL
them and offer NanoBanana as the primary path. The skill's "no code-rendered
art" rule applies to shipping publicly — HTML/CSS output is for internal
review and iteration, not final public delivery unless the user accepts it.

## Provider Landscape

| Provider | Tool | Image Gen? | Image EDIT? | Status |
|----------|------|-----------|-------------|--------|
| xAI Grok Imagine | `plugins/image_gen/xai` | YES | YES (best editor) | Prefer when OAuth live; quality model for brand work |
| Google Gemini | Nano Banana CLI | YES | YES (reference image) | Installed, needs billing-enabled key |
| Google Gemini | Direct API | YES | YES (reference image) | Free tier has daily quota limits |
| the operator agent gateway | `image_generate` → often Nous/FAL | YES | 403 on edit endpoint | Generation works; edit blocked by Nous gateway |
| OpenAI | DALL-E 3 / gpt-image-1 | YES | YES (gpt-image edit) | Needs direct OpenAI API key |
| OpenRouter | Chat completions | YES (9 models!) | YES (GPT-5-image, Gemini Flash Image) | **HAS image models** — needs credits ($5 min). See `references/image-editing-providers.md` |
| Perplexity | Search | NO | NO | Search/reasoning only |
| LLM / z.ai | Chat completions | NO | NO | Text only |
| inference.sh | infsh CLI | YES | NO | Needs `infsh login` first |
| ComfyUI | Local/cloud | YES | YES (inpainting) | Heavy setup, best for batch |
| IOPaint/LaMa | Local Python | NO | YES (self-hosted inpainting) | Free, no API. Gold standard for watermark removal. See `references/image-editing-providers.md` |

**CORRECTION (2026-08-06):** OpenRouter DOES support image generation AND editing.
It has 9 image-capable models including `openai/gpt-5-image`, `openai/gpt-5-image-mini`,
`google/gemini-2.5-flash-image`, `google/gemini-3.1-flash-image`, and more.
Architecture: `text+image -> text+image`. The previous "NO / text only" entry was wrong.
The blocker is credits ($0 balance = 402 error), not capability. Add $5 at
openrouter.ai/settings/credits to unlock.

## Nano Banana (Primary Tool)

### Location

```
~/tools/nano-banana-2/
```

### Setup (one-time)

```bash
# Bun must be installed
curl -fsSL https://bun.sh/install | bash
export PATH="$HOME/.bun/bin:$PATH"

# Clone and install
git clone https://github.com/kingbootoshi/nano-banana-2-skill.git ~/tools/nano-banana-2
cd ~/tools/nano-banana-2
bun install
bun link

# Configure API key
mkdir -p ~/.nano-banana
echo "GEMINI_API_KEY=AIzaSy..." > ~/.nano-banana/.env
```

### Usage

```bash
export PATH="$HOME/.bun/bin:$PATH"

# Basic generation
nano-banana "your prompt" -o output-name -d /path/to/output/

# High quality LinkedIn/social images (9:16 portrait at 2K)
nano-banana "your prompt" -o post1 -s 2K -a 4:5 -d ~/your-workspace/...

# With reference image (style transfer)
nano-banana "make it darker and more dramatic" -r reference.png -o output

# Transparent background (green screen removal)
nano-banana "product icon" -t -o icon

# Model selection
nano-banana "prompt" -m flash    # Gemini 3.1 Flash (default, fast, cheap)
nano-banana "prompt" -m pro      # Gemini 3 Pro (highest quality, 2x cost)
```

### Sizes and Aspect Ratios

```
Sizes:   512, 1K, 2K, 4K
Ratios:  1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 4:5, 5:4, 21:9
```

### Key Pitfall: Gemini API Key

The Gemini API key MUST be a real Google AI Studio key (starts with `AIzaSy`).
An OpenRouter key (`sk-or-v1...`) will NOT work with Nano Banana or the Gemini
API directly — it is a text-only proxy.

The key lives at `~/.nano-banana/.env`. If Nano Banana returns 429 quota errors,
the key is on the free tier. Either:
- Enable billing on the Google AI Studio project
- Wait for daily quota reset (midnight Pacific / 2 AM CT)
- Use a different key with paid quota

## Gemini API Direct (Fallback)

If Nano Banana CLI has issues, call the Gemini API directly:

```python
import urllib.request, json, base64, os

key = "AIzaSy..."  # from ~/.nano-banana/.env
model = "gemini-3.1-flash-image"
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"

payload = {
    "contents": [{"parts": [{"text": "your prompt here"}]}],
    "generationConfig": {"responseModalities": ["image", "text"]}
}

data = json.dumps(payload).encode()
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
resp = urllib.request.urlopen(req, timeout=120)
result = json.loads(resp.read())

for part in result["candidates"][0]["content"]["parts"]:
    if "inlineData" in part:
        img = base64.b64decode(part["inlineData"]["data"])
        with open("output.png", "wb") as f:
            f.write(img)
```

## User Workflow Preferences

1. **One-shot generation.** The user does NOT want to go back and forth
   iterating on images. Write a strong prompt, generate, deliver. If the user
   wants changes, they will say so.

2. **Professional quality only.** The user has rejected PIL-generated,
   hand-coded HTML/CSS, and "middle school PowerPoint" outputs. If the
   primary tool is down due to quota, SAY SO directly rather than falling
   back to low-quality programmatic generation.

3. **Prompt quality matters.** Before generating, craft a detailed prompt that
   captures the visual concept, style, colors, and composition. Brand canvas
   for DS: navy-teal void `#0a1e2e`–`#062323`, gold `#c9a227`/`#ffd700`, teal
   breath, phi composition, grain. LinkedIn heroes default **landscape 16:9**.

4. **Deliver files, not descriptions.** Download CDN URLs to a local assets
   path and deliver via `MEDIA:/abs/path`.

5. **Be honest about blockers.** If quota is exhausted or a key is missing,
   tell the user immediately. Do not substitute low-quality workarounds
   without disclosure.

6. **DS / Physiomorphic social heroes must TEACH first (2026-08-02, rev J).** Abstract gold organism nets can look premium and still fail. the principal rejected v1/v2 decorative webs as lead visuals. Body organ charts also fail for tech audiences. Current concept lock: neuron left + body right labeled with **technology analogs** (SPECIALISTS/COORDINATION/REGULATION/RECOVERY/DEFENSE/TIMING), not organ systems. Frame: "Biology inspires the shape. Labels are technology."

   **Ship carousel target (pending diffusion restoration):**
   - Slide 1: neuron + body with tech-analog labels
   - Slide 2: three I/O paths (MODEL-CENTRIC, COMMON MULTI-AGENT, PHYSIOMORPHIC AI) with arrows + diagnostics
   - **Blocked on:** xAI credit top-up (403 spending-limit as of 2026-08-02)
   - **Code-rendered drafts (v3k) were REJECTED by the principal as "not good at all" — programmer art is not ship art.**
   - Keep: `...-v3f-split.png` (left anatomy source), `...-hero-v1.png` (right craft reference), `...-v3j-body-tech-analogs-pre.png` (cleanest body diffusion for tech-analog concept)

   Full lock: `physiomorphic-ai-public-field-teaching`. When diffusion providers are down, BLOCK and tell the principal — do not ship code-rendered art as a substitute.

7. **Labeled science diagrams (anatomy exception, 2026-08-02).** Diffusion repeatedly misplaces multi-leader labels (soma on axon; "Ranvier" on myelin; duplicate systems). For neuron/body teaching figures:
   1. Lock leaders in code (Pillow/SVG) — especially left neuron half
   2. Optional xAI edit / right-panel hybrid (human + hero ref) with unique system labels
   3. Composite; heal garbled captions with **navy-matched** fills — never solid black rectangles
   4. Vision QA fail-closed on every leader (no duplicate IMMUNE)
   Recipe: `physiomorphic-ai-public-field-teaching/references/labeled-anatomy-diagram-pipeline.md`
   Do NOT use bare PIL for non-scientific brand art — that amateur ban still stands.


## Grok Imagine prompt budget

Keep the **primary prompt under ~900 tokens / ~3,500 chars**. One concept, one
composition, one mood, one reject block. Full invoke path + skeleton:
`references/grok-xai-image-path.md`. Canonical pack:
`your-org-marketing/02-social-posts/DIVINITY-SCIENCE-LINKEDIN-the operator agent-PHYSIOMORPHIC.md`
(section **LinkedIn hero image — Grok prompt pack**).

## Common Pitfalls

- **Using the wrong API key.** OpenRouter keys don't work with Gemini image
  generation. The key must be a Google AI Studio key (`AIzaSy...`).

- **Free tier daily quota.** Gemini free tier has limited daily requests for
  image models. If you hit 429 errors, the quota resets at midnight Pacific.

- **Hand-coding images.** Never use PIL/HTML/CSS/SVG/Puppeteer for ordinary brand/mood production images. Exception: multi-leader scientific anatomy where diffusion fails — lock labels in code, then beautify; see preference #7 and `physiomorphic-ai-public-field-teaching`.

- **Diffusion anatomy confidence.** (2026-08-02) Do not trust Grok/FAL alone for node of Ranvier / soma / multi-system body leaders. Vision-QA or use the labeled-science pipeline.

- **Inline Python with heredocs.** The `terminal` tool masks sensitive-looking
  strings (like API keys) in inline Python. Use a file-based approach
  (`write_file` + `python3 /tmp/script.py`) when working with API keys.

- **OpenRouter image generation.** OpenRouter DOES support image editing/generation.
  It has 9 image models (GPT-5-image, Gemini Flash Image, etc.) with `text+image -> text+image`
  architecture. The blocker is credits ($0 balance = 402), not capability. Add credits at
  openrouter.ai/settings/credits. Cheapest option: Gemini 2.5 Flash Image at $0.30/M tokens.
  See `references/image-editing-providers.md` for the full provider comparison and API format.

- **Semi-transparent watermark removal (HARD-WON, refined 2026-08-07).** This problem
  went through 10+ iterations. Pixel-level detection (OCR, top-hat, contrast thresholding)
  ALL FAIL. Alpha inversion is mathematically correct but produces incomplete masks (caught
  only 14K of ~148K watermark pixels). The WINNING approach is **template matching**:
  extract the watermark pattern from a clean background corner, use `cv2.matchTemplate`
  with normalized cross-correlation to find ALL occurrences across the image, then run
  LaMa on the matched mask. **MANDATORY for portraits:** hard-lock a face box (zero mask
  pixels) to protect eyes/teeth/nails from LaMa. When stuck iterating on thresholds, STOP
  and research alternative approaches — the user explicitly demands research over blind
  iteration. Full technique, failed-approach table, and decision framework in
  `references/image-editing-providers.md`. Working script: `scripts/watermark_removal_lama.py`.

- **Stopping at FAL 402.** (2026-08-02) `image_generate` → Nous/FAL 402 is a
  routing miss. Fall through to `XAIImageGenProvider` when xAI OAuth is live.
  Do not harden "image gen broken" as a durable fact.

- **Fleet Atlas clone on social heroes.** (2026-08-02) PDF/report layout is
  wrong for LinkedIn field-intro art. Build on coupling/cascade as fine art.

## Reference Files

- `references/gemini-image-api.md` — Gemini image API formats and key requirements
- `references/grok-xai-image-path.md` — xAI Grok Imagine invoke, models, prompt budget, DS social-hero rejects
- `references/image-editing-providers.md` — Image EDITING/inpainting provider landscape (watermark removal, object removal). Different from generation. Includes OpenRouter image models, FAL direct key, IOPaint/LaMa self-hosted setup.

## Verification

- Nano Banana installed: `which nano-banana && nano-banana --help`
- API key configured: `cat ~/.nano-banana/.env | grep AIzaSy | wc -c`
- Test generation: `nano-banana "test blue circle" -o test -s 512 -d /tmp`
- xAI available: `cd <agent-home>/hermes-agent && ./venv/bin/python3.11 -c "import sys; sys.path.insert(0,'.'); from plugins.image_gen.xai import XAIImageGenProvider; print(XAIImageGenProvider().is_available())"`
