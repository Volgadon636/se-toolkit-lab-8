#!/usr/bin/env bash
# Fill Flutter volume and restart Caddy (fixes empty /flutter). Repo root: ./scripts/task2-flutter-volume.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
ENV_FILE="${ENV_FILE:-.env.docker.secret}"
docker compose --env-file "$ENV_FILE" run --rm client-web-flutter
docker compose --env-file "$ENV_FILE" restart caddy
sleep 2
GATEWAY_PORT="$(grep -E '^GATEWAY_HOST_PORT=' "$ENV_FILE" | cut -d= -f2- | tr -d '\r' | head -1)"
GATEWAY_PORT="${GATEWAY_PORT:-42002}"
curl -sS -o /dev/null -w "HTTP %{http_code} main.dart.js\n" "http://127.0.0.1:${GATEWAY_PORT}/flutter/main.dart.js"
