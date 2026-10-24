# Gemini Image Generation API Reference

## Endpoint

```
POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}
```

## Image-Capable Models

| Model | Speed | Quality | Cost |
|-------|-------|---------|------|
| `gemini-3.1-flash-image` | Fast | Good | Free tier (limited) or paid |
| `gemini-3-pro` | Slower | Best | 2x flash pricing |

## Request Format

```json
{
  "contents": [
    {
      "parts": [
        {"text": "your prompt here"}
      ]
    }
  ],
  "generationConfig": {
    "responseModalities": ["image", "text"]
  }
}
```

## Response Format

```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "inlineData": {
              "mimeType": "image/png",
              "data": "<base64-encoded-image>"
            }
          }
        ]
      }
    }
  ]
}
```

## Image Generation with Reference Image

```json
{
  "contents": [
    {
      "parts": [
        {
          "inlineData": {
            "mimeType": "image/png",
            "data": "<base64-reference-image>"
          }
        },
        {"text": "make it darker and more dramatic"}
      ]
    }
  ],
  "generationConfig": {
    "responseModalities": ["image", "text"]
  }
}
```

## Error Responses

| Status | Meaning | Fix |
|--------|---------|-----|
| 429 | Quota exhausted | Enable billing or wait for daily reset |
| 400 | Bad request (bad model name, missing modalities) | Check model name and config |
| 403 | API key invalid or wrong project | Use real Google AI Studio key |

## Key Requirement

The key MUST be a Google AI Studio key starting with `AIzaSy`. OpenRouter
keys (`sk-or-v1...`) do NOT work with this endpoint. They only proxy text
completion endpoints.

Get a key at: https://aistudio.google.com/apikey
