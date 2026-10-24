# Docker Endpoint Smoke Test

## Purpose
Systematic verification that every API endpoint works correctly inside a
Docker container. Run after every build, never claim "done" without it.

## Setup

```bash
# Build and boot the container
docker build -f <deploy-dir>/Dockerfile -t <service>:test <context-dir>
docker run -d --name ws-test -p 8311:port \
  -e DATABASE_URL="sqlite+aiosqlite:///data/test.db" \
  -e SECRET_KEY="test_secret_minimum_32_chars_aaaaaaa" \
  -e ADMIN_EMAIL="admin@example.com" \
  -e ADMIN_PASSWORD="testpassword123" \
  -e ENVIRONMENT="development" \
  <service>:test

sleep 6
docker ps --filter name=ws-test --format "{{.Status}}"
# Must show "Up X seconds (healthy)"
```

## Test Pattern

Run tests via `docker exec` (avoids Colima port forwarding issues):

```python
import urllib.request, json, urllib.error

BASE = 'http://localhost:port'

def req(method, path, token=None, body=None):
    url = BASE + path
    headers = {'Content-Type': 'application/json'}
    if token: headers['Authorization'] = 'Bearer ' + token
    data = json.dumps(body).encode() if body else None
    r = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        resp = urllib.request.urlopen(r)
        return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

tests = []

# 1. Health (public)
code, d = req('GET', '/api/pipelines/health')
tests.append(('Health', code == 200 and d.get('status') == 'ok'))

# 2. HTML page (public)
code, d = req('GET', '/')
tests.append(('HTML page', code == 200))

# 3. Unauthenticated blocked
code, d = req('GET', '/api/drafts')
tests.append(('Unauth blocked', code == 401))

# 4. Signup
code, d = req('POST', '/api/auth/signup',
    body={'email':'qa@example.com','name':'QA','password':'testpassword123'})
token = d.get('token', '')
tests.append(('Signup', bool(token)))

# 5. Auth/me
code, d = req('GET', '/api/auth/me', token=token)
tests.append(('Auth/me', d.get('user',{}).get('email') == 'qa@example.com'))

# 6. CRUD: create
code, d = req('POST', '/api/drafts', token=token,
    body={'title':'Test Draft','content':'Hello'})
did = d.get('draft',{}).get('id','')
tests.append(('Create', bool(did)))

# 7. CRUD: read
code, d = req('GET', f'/api/drafts/{did}', token=token)
tests.append(('Read', d.get('draft',{}).get('title') == 'Test Draft'))

# 8. CRUD: update
code, d = req('PATCH', f'/api/drafts/{did}', token=token, body={'content':'Updated'})
tests.append(('Update', code == 200))

# 9. Cross-user isolation
code2, d2 = req('POST', '/api/auth/signup',
    body={'email':'user2@example.com','name':'U2','password':'testpassword123'})
token2 = d2.get('token','')
code, d = req('GET', f'/api/drafts/{did}', token=token2)
tests.append(('Isolation', code == 404))

# 10. Wrong password
code, d = req('POST', '/api/auth/login',
    body={'email':'qa@example.com','password':'wrong'})
tests.append(('Wrong pass', code == 401))

# 11. Duplicate signup
code, d = req('POST', '/api/auth/signup',
    body={'email':'qa@example.com','name':'D','password':'testpassword123'})
tests.append(('Duplicate', code == 409))

# Report
for name, passed in tests:
    print(f"  {'PASS' if passed else 'FAIL'}  {name}")
fails = [t for t in tests if not t[1]]
print(f"\n{'ALL PASSED' if not fails else f'{len(fails)} FAILURES'}")
```

## Colima Note
On macOS with Colima, `curl localhost:<mapped-port>` from the host may fail
even though the container is healthy. Always run tests via `docker exec`
from inside the container.

## Cleanup
```bash
docker rm -f ws-test
```
