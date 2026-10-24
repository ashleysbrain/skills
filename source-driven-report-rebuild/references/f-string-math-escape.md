# F-string math escape notes

When generating HTML/PDF source with Python f-strings, any literal braces used for math notation or set notation must be escaped as doubled braces (`{{` and `}}`). Otherwise Python treats the content as an f-string expression and `py_compile` fails before the build even runs.

## Symptoms
- `SyntaxError` pointing at math-like text inside a triple-quoted f-string
- The error caret may appear near Unicode set symbols or subscripts even though the real issue is unescaped `{...}`

## Fix pattern
- Escape all literal braces in the generated source string
- Prefer ASCII-safe or escaped forms in the builder when the content includes:
  - set notation
  - summation bounds
  - subscripts that use braces
  - formula fragments copied from LaTeX/Markdown
- Re-run `python3 -m py_compile <builder.py>` before rebuilding
- Then regenerate the artifact and verify the rendered output

## Example
- Bad: `Σ_{d∈𝒟} w_d = 1`
- Good inside an f-string: `Σ_{{d∈𝒟}} w_d = 1`
