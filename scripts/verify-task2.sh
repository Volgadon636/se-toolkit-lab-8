#!/usr/bin/env bash
# Task 2 acceptance-style checks (Flutter JS, nanobot Up, WebSocket optional).
# Usage: from repo root — ./scripts/verify-task2.sh
# Requires: docker compose, curl; optional: websocat for WS check.

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

ENV_FILE="${ENV_FILE:-.env.docker.secret}"
if [[ ! -f "$ENV_FILE" ]]; then
  echo "FAIL: missing ${ENV_FILE} (copy from .env.docker.example and fill secrets)"
  exit 1
fi

GATEWAY_PORT="$(grep -E '^GATEWAY_HOST_PORT=' "$ENV_FILE" | cut -d= -f2- | tr -d '\r' | head -1)"
GATEWAY_PORT="${GATEWAY_PORT:-42002}"
ACCESS_KEY="$(grep -E '^NANOBOT_ACCESS_KEY=' "$ENV_FILE" | cut -d= -f2- | tr -d '\r' | sed 's/^"\(.*\)"$/\1/')"
if [[ -z "${ACCESS_KEY// }" ]]; then
  echo "FAIL: NANOBOT_ACCESS_KEY is empty in ${ENV_FILE}"
  exit 1
fi

if ! docker compose --env-file "$ENV_FILE" ps -a 2>/dev/null | grep -qE 'nanobot.*\sUp\s'; then
  echo "FAIL: nanobot not running (start with: docker compose --env-file ${ENV_FILE} up -d)"
  exit 1
fi

if ! out="$(curl -sf "http://127.0.0.1:${GATEWAY_PORT}/flutter/main.dart.js" 2>/dev/null | head -c 20)" || [[ ${#out} -lt 10 ]]; then
  echo "FAIL: Flutter bundle missing at http://127.0.0.1:${GATEWAY_PORT}/flutter/main.dart.js"
  exit 1
fi

if command -v websocat >/dev/null 2>&1; then
  if ! echo '{"content":"ping"}' | timeout 60 websocat "ws://127.0.0.1:${GATEWAY_PORT}/ws/chat?access_key=${ACCESS_KEY}" 2>/dev/null | grep -q .; then
    echo "FAIL: WebSocket did not return data (check Caddy /ws/chat, NANOBOT_ACCESS_KEY, qwen-code-api)"
    exit 1
  fi
else
  echo "SKIP: websocat not installed — install to validate WebSocket (optional on some CI)"
fi

echo "PASS"
