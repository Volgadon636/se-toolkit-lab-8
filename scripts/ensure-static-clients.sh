#!/usr/bin/env bash
# Fill client-web-react and client-web-flutter named volumes, then ensure Caddy is up.
# Run from repo root after build: ENV_FILE=.env.docker.secret ./scripts/ensure-static-clients.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
ENV_FILE="${ENV_FILE:-.env.docker.secret}"
DC=(docker compose --env-file "$ENV_FILE")

echo "==> Building static client images..."
"${DC[@]}" build client-web-react client-web-flutter

echo "==> Copying React build into volume..."
"${DC[@]}" run --rm --no-deps client-web-react

echo "==> Copying Flutter build into volume..."
"${DC[@]}" run --rm --no-deps client-web-flutter

echo "==> Starting full stack (Caddy will mount volumes)..."
"${DC[@]}" up -d --remove-orphans

echo "==> Restarting Caddy so it picks up volume content..."
sleep 2
"${DC[@]}" restart caddy

GATEWAY_PORT="$(grep -E '^GATEWAY_HOST_PORT=' "$ENV_FILE" | cut -d= -f2- | tr -d '\r' | head -1)"
GATEWAY_PORT="${GATEWAY_PORT:-42002}"
echo "==> Check Flutter JS (expect HTTP 200)..."
curl -sS -o /dev/null -w "HTTP %{http_code}\n" "http://127.0.0.1:${GATEWAY_PORT}/flutter/main.dart.js" || true

echo "==> Done. Run: ENV_FILE=$ENV_FILE ./scripts/verify-task2.sh"
