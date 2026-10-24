#!/usr/bin/env bash
# Smoke test suite for adversarial panel review — runs 8+ endpoint checks
# Usage: ./scripts/smoke-test.sh <BASE_URL> (default: http://localhost:port)
set -euo pipefail

BASE_URL="${1:-http://localhost:port}"
PASS=0
FAIL=0

echo ""
echo "=== SMOKE TEST SUITE: $BASE_URL ==="
echo ""

# 1. Main health
echo "1. MAIN HEALTH"
HTTP=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/health")
if [[ "$HTTP" == "200" ]]; then
  ORG=$(curl -s "$BASE_URL/api/health" | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get("organism","-"))' 2>/dev/null || echo "-")
  echo "  ✅ HTTP 200 | organism: $ORG"
  ((PASS++))
else
  echo "  ❌ HTTP $HTTP"
  ((FAIL++))
fi

# 2. /you page loads
echo "2. /YOU PAGE LOADS"
HTTP=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/you")
if [[ "$HTTP" == "200" ]]; then
  echo "  ✅ HTTP 200"
  ((PASS++))
else
  echo "  ❌ HTTP $HTTP"
  ((FAIL++))
fi

# 3. /integrations-adaptive loads
echo "3. /INTEGRATIONS-ADAPTIVE LOADS"
HTTP=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/integrations-adaptive")
if [[ "$HTTP" == "200" ]]; then
  echo "  ✅ HTTP 200"
  ((PASS++))
else
  echo "  ❌ HTTP $HTTP"
  ((FAIL++))
fi

# 4. Health-check API (full TWC)
echo "4. HEALTH-CHECK API (full TWC)"
PAYLOAD='{"stress_level":"medium","energy_level":"high","sleep_quality":"good","mental_state":"focused"}'
RESPONSE=$(curl -s -X POST "$BASE_URL/api/user/health-check" -H 'Content-Type: application/json' -d "$PAYLOAD")
TWC=$(echo "$RESPONSE" | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get("twc_100","-"))' 2>/dev/null || echo "-")
ENGINE=$(echo "$RESPONSE" | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get("engine","-"))' 2>/dev/null || echo "-")
if [[ "$TWC" != "-" && "$ENGINE" != "-" ]]; then
  echo "  ✅ TWC: $TWC | Engine: $ENGINE"
  ((PASS++))
else
  echo "  ❌ Invalid response: $RESPONSE"
  ((FAIL++))
fi

# 5. Tech recommendations
echo "5. TECH RECOMMENDATIONS"
PAYLOAD='{"category":"databases"}'
RESPONSE=$(curl -s -X POST "$BASE_URL/api/integrations/recommend" -H 'Content-Type: application/json' -d "$PAYLOAD")
COUNT=$(echo "$RESPONSE" | python3 -c 'import sys,json; d=json.load(sys.stdin); print(len(d.get("recommendations",[])))' 2>/dev/null || echo "-")
if [[ "$COUNT" -ge 1 ]]; then
  ITEMS=$(echo "$RESPONSE" | python3 -c 'import sys,json; d=json.load(sys.stdin); recs=d.get("recommendations",[]); print(", ".join([r["name"] for r in recs[:3]]))' 2>/dev/null || echo "-")
  echo "  ✅ Count: $COUNT | Items: $ITEMS"
  ((PASS++))
else
  echo "  ❌ No recommendations: $RESPONSE"
  ((FAIL++))
fi

# 6. User summary
echo "6. USER SUMMARY"
RESPONSE=$(curl -s "$BASE_URL/api/user/summary")
LEVEL=$(echo "$RESPONSE" | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get("technical_level","-"))' 2>/dev/null || echo "-")
BURNOUT=$(echo "$RESPONSE" | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get("burnout_risk","-"))' 2>/dev/null || echo "-")
if [[ "$LEVEL" != "-" ]]; then
  echo "  ✅ Level: $LEVEL | Burnout: $BURNOUT"
  ((PASS++))
else
  echo "  ❌ Invalid response: $RESPONSE"
  ((FAIL++))
fi

# 7. CSS loads
echo "7. CSS LOADS"
HTTP=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/gg-styles.css")
if [[ "$HTTP" == "200" ]]; then
  echo "  ✅ HTTP 200"
  ((PASS++))
else
  echo "  ❌ HTTP $HTTP (page will be unstyled)"
  ((FAIL++))
fi

# 8. Ops loads
echo "8. OPS LOADS"
HTTP=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/ops")
if [[ "$HTTP" == "200" ]]; then
  echo "  ✅ HTTP 200"
  ((PASS++))
else
  echo "  ❌ HTTP $HTTP"
  ((FAIL++))
fi

echo ""
echo "=== SUMMARY ==="
echo "  PASS: $PASS"
echo "  FAIL: $FAIL"
if [[ "$FAIL" -eq 0 ]]; then
  echo "  ✅ ALL CHECKS PASSED"
  exit 0
else
  echo "  ❌ $FAIL CHECK(S) FAILED"
  exit 1
fi
