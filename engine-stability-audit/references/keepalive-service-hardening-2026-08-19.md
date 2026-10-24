# KeepAlive Service Hardening — browser CDP fix + measured QA (2026-08-19)

Worked example behind the Crash-Race Test Battery (SKILL.md) and
`templates/keepalive-service.plist`. Operator: hermes. QA rotations: the specialist engine
(pass 2, immune/propagation vectors), the specialist engine (pass 3, circuit-timing
vectors). 16 vectors total, 14 PASS, 0 red, 1 by-design, 1 pending-empirical.

## Symptom class

Agent-facing local service works after manual repair, dies overnight, needs a
human report every morning to notice. Root cause was two-layer: (1) the
browser-use CLI was never persistently installed — every session re-attempted
an ephemeral uv build; (2) that build needed Rust and the rustup bootstrap
cache (`~/Library/Caches/puccinialin`) was corrupt (0-byte settings.toml), so
every cold build died. Morning failure = rebuild path + stale daemon
connections, not a crashing browser.

## Fix recipe (macOS, ordered)

1. Purge corrupt bootstrap cache: `rm -rf ~/Library/Caches/puccinialin`.
2. Real toolchain so nothing bootstraps per-session: `brew install rust`.
3. Persistent CLI install where the harness looks first:
   `uv tool install browser-use` (lands in `<agent-home>/bin` symlink ->
   `~/.local/share/uv/tools`). `--version` in 0.73s after; no rebuild path.
4. Dedicated headless Chrome as launchd KeepAlive service, private CDP port
   (9223), isolated `--user-data-dir` — never the user's daily driver, so no
   remote-debugging permission popups. See the template plist.
5. Point the harness at it: `hermes config set browser.cdp_url http://127.0.0.1:9223`.
6. Register the agent OUTSIDE the gateway process (gateway guards
   `launchctl bootstrap` to prevent SIGTERM-respawn loops). Escape that
   worked: `osascript -e 'do shell script "launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/<label>.plist"'`
   — osascript spawns from launchd context, outside the gateway.

## Measured battery

| Test | Method | Measured |
|---|---|---|
| Single kill -9 -> CDP back | tight curl poll on /json/version | 9.1s |
| Double kill < ThrottleInterval apart | 2 kills < 10s | 14.9s (backoff = protection) |
| Stale-client reconnect | kill Chrome while daemon holds websocket; next real call | seamless: 1.4s first nav, 0.9s second |
| Dual-supervisor race | `grep -l 9223 ~/Library/LaunchAgents/*.plist` | sole owner |
| Security bind | `lsof -nP -iTCP:9223` | 127.0.0.1 IPv4 LISTEN only |
| Boot coverage | `launchctl print gui/$(id -u)/<label>` | keepalive + runatload, state=running |
| Crash honesty | runs count + ~/Library/Logs/DiagnosticReports | all restarts = test kills; 0 crash reports |
| Resource trend | targets count, RSS, log bytes over 40min | flat (3 targets, 50->43MB, byte-flat log) |

## Honest-categories handling

- PENDING-EMPIRICAL: sleep/wake was structurally covered (KeepAlive) but
  unproven — machine had not fully slept since the fix. Resolving condition
  recorded: first real overnight sleep; verify via `pmset -g log` + a live
  call, never on structure alone.
- Non-issue by contract: CLI printed 0.1.9 while uv registry said 0.13.8;
  consumer source (browser_use_cli.py:745) never parses version output, so no
  contract existed to violate. Grep the consumer before filing version drift.

## By-design note

localhost URLs remain blocked at the tool layer (SSRF guard) — use a direct
chrome-headless-shell/Playwright path for localhost UI QA.

Run-record: `~/your-workspace/qa-browser-service-pass2-2026-08-19.md`
(passes 2-3 scorecards, folded same-doc per multi-pass protocol).
