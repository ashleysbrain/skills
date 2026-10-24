---
name: prototype-production-deployment
category: devops
description: Deploy local single-user web apps to multi-user production.
---

# Prototype to Production Deployment

## When to Use
When a local single-user web application (FastAPI, Flask, etc.) needs to become
a multi-user production service running 24/7 behind TLS on a cloud VM. This
covers the full transition: containerization, database migration, auth upgrade,
task queue extraction, and deployment automation.

## Diagnosis: Why Local Apps Break at Scale

Before building anything, diagnose what will break. Run these checks FIRST:

### Check 0: Is the service auto-starting? (THE most common gap)
Before anything else, verify the service survives a reboot:
- On macOS: `launchctl list | grep <service-name>` and check for a plist in `~/Library/LaunchAgents/`
- Check the process tree: `ps -o ppid,command -p <PID>` — if the parent is a dev server (e.g., `hermes serve`, `npm run dev`, VS Code), the service dies when the parent dies
- If no launchd plist / systemd unit / Docker restart policy exists, the service is vulnerable to reboot

**This is the #1 cause of "it works after I wake you up but not cold."** The service is a child of an interactive process (desktop app, dev server, terminal session). When that parent exits, the service dies.

**Fix pattern (macOS):** Create a launchd LaunchAgent with `RunAtLoad=true` and `KeepAlive=true`. Test crash recovery with `kill -9 <PID>` and verify launchd restarts it within 10 seconds.

### Check 1: What will break at scale?

| Local Pattern | Breaks At | Production Fix |
|--------------|-----------|----------------|
| SQLite file locking | 2+ concurrent writes | PostgreSQL |
| In-process background threads | Web process blocks for all users | Celery + Redis task queue |
| Static shared token | Immediately on public exposure | JWT auth with per-user accounts |
| No auto-start (child of dev server) | Reboot / crash = dead service | systemd/launchd or Docker restart policy |
| CORS locked to localhost | Can't access remotely | Reverse proxy (Caddy/nginx) with TLS |
| No per-user cost tracking | Financial exposure | Redis-backed rate limiting + cost metering |
| Hardcoded local paths (`/<workspace>`) | Container or new machine | Env-var driven path resolution |

## The Deployment Stack

```
User -> Caddy (TLS, auto-HTTPS) -> web container (FastAPI/uvicorn)
                                     |
                                     +-- PostgreSQL (data persistence)
                                     +-- Redis (task queue + rate limiting)
                                     +-- worker container (Celery background execution)
```

## Key Steps (in dependency order)

### 1. Fix Auto-Start FIRST
Before any production work, ensure the local service survives reboots.
On macOS: create a launchd plist with `RunAtLoad` + `KeepAlive`. See
`references/macos-autostart-fix.md` for the plist template.

### 2. Database Abstraction Layer
Replace raw `sqlite3.connect()` calls with SQLAlchemy models. Design for
dual-mode: PostgreSQL in production, SQLite for local dev/testing.

CRITICAL: SQLite does not support `pool_size` / `max_overflow` engine params.
Make them conditional:
```python
if IS_POSTGRES:
    async_engine = create_async_engine(url, pool_size=10, max_overflow=20)
else:
    async_engine = create_async_engine(url)  # no pool params for sqlite
```

### 3. Multi-User Auth
Replace static tokens with JWT auth (bcrypt password hashing, per-user
accounts). Add `user_id` foreign key to every content table for data isolation.

CRITICAL TRAP: see Pitfalls section below about backward compatibility.

### 4. Task Queue Extraction
Move long-running work (pipeline runs, LLM calls) out of the web process
into a Celery worker. The web server submits jobs and polls status. The
worker executes with a time limit (`task_time_limit=1800`).

### 5. Containerize
Dockerfile with: pip install layer BEFORE code copy (cached deps),
non-root user, healthcheck, unbuffered output.

### 6. One-Command Deploy
`deploy.sh` that: generates `.env` secrets if missing, builds images,
starts all services, runs health checks, prints connection info.

## Pitfalls

### BREAKING LIVE ACCESS: The #1 Frontend Auth Migration Bug

**Scenario:** You change the frontend to use a new JWT login system, but the
user's local server still runs the OLD backend. The login form appears but
no endpoint receives it. User is LOCKED OUT.

**This happened.** The user's exact words: "I need to get into the writing
studio and you just kicked me out."

**Prevention:** When modifying frontend auth for a production deploy, ALWAYS
make the frontend detect which backend is running and fall back gracefully.

The CORRECT probe is to test for the LEGACY endpoint (`/api/auth/local-token`)
which returns 200 on the old server but 404 on the new one. Do NOT probe
`/api/auth/me` and check for 404 — the legacy auth guard intercepts all API
routes and returns 401 (not 404), so the detection never fires. See
`references/auth-dual-mode-detection.md` for the full corrected pattern.

**Rule:** Never push auth frontend changes to a live server unless the
backend change is already deployed, OR the frontend supports both auth modes.

### Missing Dependencies in Docker

Each time you build for the first time, expect missing deps. Common ones:
- `aiosqlite` (async SQLite driver: not included with sqlalchemy)
- `email-validator` (required by Pydantic `EmailStr`)
- `bcrypt==4.0.1` (passlib needs a compatible bcrypt version; 4.2+ rejects >72 byte passwords even when passlib truncates)

Fix: add to requirements.txt and rebuild. The build cache means only the
pip layer re-runs.

### SQLAlchemy AsyncSession as FastAPI Dependency

The `db: AsyncSession = Depends(get_db)` pattern requires the dependency
function to be imported properly. If `get_current_user` takes `db` as a
parameter, it MUST also use `Depends(get_db)`, otherwise FastAPI tries to
parse `AsyncSession` as a request body field and fails at startup.

### Docker Build Context Paths

When the Dockerfile lives in a subdirectory (`writing-studio-deploy/Dockerfile`)
but the build context is the parent directory, all COPY paths must be relative
to the parent. `COPY requirements.txt` fails; `COPY writing-studio-deploy/requirements.txt` works.

### Colima Port Forwarding

On macOS with Colima (not Docker Desktop), `docker run -p 8311:port` maps
correctly but host-side `curl localhost:port` may fail. Test from INSIDE
the container with `docker exec <container> curl localhost:port`.

### bcrypt 72-byte Limit

bcrypt silently truncates passwords at 72 bytes. With bcrypt 4.x, passlib's
truncation flag can raise `ValueError` instead. Truncate explicitly before
hashing: `password[:72].encode('utf-8')`.

## QA Discipline (Binding)

Never claim deployment is done without running a systematic endpoint test
suite. See `references/endpoint-smoke-test.md` for the pattern.

Minimum tests:
1. Health endpoint (public)
2. HTML page loads
3. Unauthenticated access returns 401
4. Signup creates a user + returns JWT
5. Login works for admin
6. Auth/me returns current user
7. CRUD on primary entity (create, read, update)
8. Cross-user data isolation (user A can't see user B's data -> 404)
9. Wrong password -> 401
10. Duplicate signup -> 409

## References

- `references/macos-autostart-fix.md` -- launchd plist template for service auto-start
- `references/sqlite-to-postgresql-migration.md` -- migration script pattern + checklist
- `references/endpoint-smoke-test.md` -- reusable Docker endpoint QA suite
- `references/auth-dual-mode-detection.md` -- frontend backward-compatibility pattern for auth migrations
