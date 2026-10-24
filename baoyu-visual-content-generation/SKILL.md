---
name: baoyu-visual-content-generation
description: "Use when turning articles, topics, or source notes into Baoyu-style comics, infographics, or article illustrations with prompt-driven image generation."
version: 1.0.0
author: the operator agent Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [creative, image-generation, comic, infographic, article-illustration, visual-storytelling]
---

# Baoyu Visual Content Generation

## Overview

Use this umbrella when a user wants a source document or topic turned into a visual artifact: a knowledge comic, an infographic, or article illustrations. The shared workflow is the same across the family:

1. analyze the source and extract structure
2. choose a visual format, tone, and aspect ratio
3. write reproducible prompt files before generating images
4. use `image_generate` for rendering
5. download the returned image URLs to local files
6. verify the final artifact path and regenerate only the changed parts when needed

These skills are prompt-driven. They do not feed reference images directly into the model; any reference image must be converted into textual traits first.

## When to Use

- turning a topic or article into a multi-panel knowledge comic
- generating an infographic or dense visual summary from structured content
- creating article illustrations from prose, notes, or a source file
- producing multiple pages, panels, or prompt variants from one source
- revising a previous visual artifact by regenerating only selected pieces

## Shared Workflow

### 1. Read and analyze the source

Identify:
- topic or thesis
- target audience
- key facts, quotes, or sequence of events
- visual density and narrative structure
- language to use in the final artifact

Preserve important source data exactly. Do not invent new facts or metrics.

### 2. Choose the right visual mode

Use the mode that fits the source:

- **Comic mode** for narrative, biography, tutorial, or teaching sequences
- **Infographic mode** for dense structure, comparison, timelines, or dashboards
- **Illustration mode** for placing visuals into an existing article or document

Pick an aspect ratio that matches the composition instead of forcing one universal canvas.

### 3. Write prompts before generating

Each image or page needs a saved prompt file first.

Common rules:
- write the full, final prompt to disk before calling `image_generate`
- keep the prompt reproducible and self-contained
- embed the text descriptions that drive consistency
- if using a reference image, convert it to traits in text and include those traits in the prompt

### 4. Generate and download

For AI image generation, load the `ai-image-generation` skill for the current
tooling landscape (Nano Banana, Gemini API, OpenAI, etc.).

`image_generate` returns a URL, not a local file.

After each generation:
1. capture the returned URL
2. download it to the correct output directory with an absolute path
3. verify the file exists and is non-empty before moving on

### 5. Regenerate carefully

If the user wants edits:
- update the prompt file first
- regenerate only the affected page / panel / illustration
- keep earlier outputs when they are still valid
- rename or back up old outputs if the workflow calls for it

## Mode Notes

### Comic Mode

Best for stepwise teaching, biographies, and explanatory sequences.

Keep the sequence clear:
- opening premise
- setup or context
- conflict / explanation / transformation
- closing takeaway

Make character consistency explicit in text. If there are recurring characters, describe them once and reuse the same descriptions in every page prompt.

### Infographic Mode

Best for structured comparisons, timelines, and high-density explanations.

Priorities:
- faithful data handling
- clear hierarchy
- one message per section
- visual structure that matches the content type

Do not summarize away the details that make the infographic useful.

### Illustration Mode

Best for article support images and inline visuals.

Priorities:
- visualize the underlying concept, not a literal metaphor
- reuse the article's actual data, terminology, and labels
- keep the illustration aligned with the surrounding text

## Common Pitfalls

- skipping the prompt file and going straight to image generation
- treating reference images as if `image_generate` could ingest them directly
- losing source fidelity by paraphrasing away numbers or named terms
- forgetting to download the returned URL to a local file
- using one aspect ratio for every composition even when the source wants another
- leaving regenerated outputs undocumented

## Verification

- prompt files exist before generation
- each generated image has been downloaded to the correct absolute path
- the output directory matches the requested mode and topic
- the final prompt and final artifact agree on language, aspect ratio, and content focus
