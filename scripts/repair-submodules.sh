#!/usr/bin/env bash
# Reset broken submodule checkouts (e.g. "not our ref"). Run from repo root: ./scripts/repair-submodules.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

git submodule sync --recursive

for name in qwen-code-api nanobot-websocket-channel; do
  echo "==> Resetting submodule: $name"
  git submodule deinit -f "$name" 2>/dev/null || true
  rm -rf "$name" ".git/modules/$name"
done

git submodule update --init --recursive --force
echo "OK"
git submodule status
