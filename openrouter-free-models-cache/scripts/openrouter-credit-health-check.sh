#!/usr/bin/env bash
# OpenRouter Credit + Service Health Check (Watchdog)
# Monitors any LLM-dependent service for OpenRouter credit exhaustion (402)
# and rate-limiting (429). Silent when healthy — only outputs on problems.
#
# Adapt the CONFIG section for your specific service.
# Schedule via cron every 4-6 hours.

# ============= CONFIG (adapt for your service) =============
SERVICE_PROCESS_PATTERN="src.deriver"        # pgrep pattern for the service process
SERVICE_LAUNCHCTL_LABEL="ai.honcho.deriver"  # launchctl label (if launchd-managed)
SERVICE_HEALTH_URL="http://127.0.0.1:port/health"  # HTTP health endpoint (if any)
SERVICE_ENV_FILE="/<workspace>"     # .env file containing model config
SERVICE_ERROR_LOG="/<workspace>"  # error log path
PAID_MODEL="google/gemini-2.5-flash"         # the paid model to test for credit restoration
# ============================================================

ALERTS=""
WARNINGS=""
TMP_BODY="/tmp/_or_health_body"

add_alert() { ALERTS="${ALERTS}
  CRITICAL: $1"; }
add_warning() { WARNINGS="${WARNINGS}
  WARNING: $1"; }

# === 1. Service process alive ===
if [ -n "$SERVICE_PROCESS_PATTERN" ]; then
    if ! pgrep -f "$SERVICE_PROCESS_PATTERN" >/dev/null 2>&1; then
        if [ -n "$SERVICE_LAUNCHCTL_LABEL" ]; then
            add_alert "Service ($SERVICE_PROCESS_PATTERN) is NOT running. Fix: launchctl start $SERVICE_LAUNCHCTL_LABEL"
        else
            add_alert "Service ($SERVICE_PROCESS_PATTERN) is NOT running."
        fi
    fi
fi

# === 2. HTTP health endpoint ===
if [ -n "$SERVICE_HEALTH_URL" ]; then
    API_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$SERVICE_HEALTH_URL" 2>/dev/null || echo "000")
    if [ "$API_STATUS" != "200" ]; then
        add_alert "Service health endpoint unreachable (HTTP $API_STATUS) at $SERVICE_HEALTH_URL"
    fi
fi

# === 3. OpenRouter credit check ===
OR_KEY=$(grep '^OPENROUTER_API_KEY=' "$SERVICE_ENV_FILE" 2>/dev/null | cut -d= -f2- || echo "")
if [ -n "$OR_KEY" ]; then
    # Determine current model from the service config
    CURRENT_MODEL=$(grep '^.*MODEL_CONFIG__MODEL=' "$SERVICE_ENV_FILE" 2>/dev/null | head -1 | cut -d= -f2- || echo "unknown")

    # Test with 1-token completion on current model
    HTTP_CODE=$(curl -s -o "$TMP_BODY" -w "%{http_code}" \
        -H "Authorization: Bearer $OR_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"model\":\"${CURRENT_MODEL}\",\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}],\"max_tokens\":1}" \
        "https://openrouter.ai/api/v1/chat/completions" 2>/dev/null || echo "000")

    case "$HTTP_CODE" in
        *402*)
            add_alert "OpenRouter credits exhausted (402) on $CURRENT_MODEL. Action: add credits or switch to free model."
            ;;
        *429*)
            add_warning "Free model rate-limited (429) on $CURRENT_MODEL. Service slow but functional."
            ;;
        *200*)
            # If currently on a free model, check if paid credits restored
            if echo "$CURRENT_MODEL" | grep -q ":free"; then
                PAID_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
                    -H "Authorization: Bearer $OR_KEY" \
                    -H "Content-Type: application/json" \
                    -d "{\"model\":\"${PAID_MODEL}\",\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}],\"max_tokens\":1}" \
                    "https://openrouter.ai/api/v1/chat/completions" 2>/dev/null || echo "000")
                case "$PAID_CODE" in
                    *200*)
                        add_warning "CREDITS RESTORED. Currently on free model ($CURRENT_MODEL). Switch back: sed -i '' 's|$CURRENT_MODEL|$PAID_MODEL|g' $SERVICE_ENV_FILE"
                        ;;
                esac
            fi
            ;;
        *)
            BODY_PREVIEW=$(cat "$TMP_BODY" 2>/dev/null | head -c 200 || echo "")
            add_warning "OpenRouter returned HTTP $HTTP_CODE. Body: $BODY_PREVIEW"
            ;;
    esac
fi
rm -f "$TMP_BODY" 2>/dev/null

# === 4. Log error pattern analysis ===
if [ -f "$SERVICE_ERROR_LOG" ]; then
    RECENT_402=$(tail -100 "$SERVICE_ERROR_LOG" 2>/dev/null | grep -c "402" || true)
    RECENT_429=$(tail -100 "$SERVICE_ERROR_LOG" 2>/dev/null | grep -c "429" || true)
    RECENT_402=${RECENT_402:-0}
    RECENT_429=${RECENT_429:-0}
    if [ "$RECENT_402" -gt 3 ] 2>/dev/null; then
        add_alert "Service hitting 402 errors ($RECENT_402 in last 100 log lines). Credits exhausted."
    fi
    if [ "$RECENT_429" -gt 10 ] 2>/dev/null; then
        add_warning "Service hitting heavy rate limits ($RECENT_429 429s in last 100 lines). Processing slow."
    fi
fi

# === Output (silent when healthy) ===
if [ -z "$ALERTS" ] && [ -z "$WARNINGS" ]; then
    exit 0
fi

echo "OpenRouter Health Check — $(date '+%Y-%m-%d %H:%M')"
echo "==============================================="
[ -n "$ALERTS" ] && echo -e "$ALERTS"
[ -n "$WARNINGS" ] && echo -e "$WARNINGS"
echo "==============================================="
