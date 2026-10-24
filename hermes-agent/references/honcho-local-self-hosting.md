# Honcho local self-hosting notes

## What worked in this session
- Honcho local setup on macOS used Homebrew PostgreSQL + pgvector, then the repo's manual setup path.
- `uv sync` on Intel macOS can fail on `lancedb` wheel resolution even though the rest of the environment is fine.
- Workaround used successfully: `uv sync --no-install-package lancedb`
- Then run migrations with `uv run --no-sync alembic upgrade head`
- Start the API with `uv run --no-sync --env-file .env fastapi dev src/main.py`
- Start the deriver with `uv run --no-sync --env-file .env python -m src.deriver`

## Verification pattern
- `curl http://127.0.0.1:port/health` should return `{"status":"ok"}`
- `hermes honcho status` should show the active profile and connection state
- `hermes honcho identity <profile-md>` seeds the AI peer identity from a profile file

## Notes
- Local Honcho expects PostgreSQL with the `vector` extension.
- The manual setup path can work without Docker if PostgreSQL is available locally.
- Keep the `.env` focused on the database URI, auth toggle, log level, and LLM provider keys.