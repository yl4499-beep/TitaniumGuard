#!/usr/bin/env bash
set -euo pipefail
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$APP_DIR")"
PY_CMD="${PYTHON:-python3}"
if [ -n "${TITANIUM_PYTHON:-}" ]; then
  RUN_PY="$TITANIUM_PYTHON"
else
  if [ ! -x "$PROJECT_DIR/.venv/bin/python" ]; then "$PY_CMD" -m venv "$PROJECT_DIR/.venv"; fi
  RUN_PY="$PROJECT_DIR/.venv/bin/python"
  if ! cmp -s "$APP_DIR/requirements.txt" "$PROJECT_DIR/.venv/.titanium-requirements"; then
    "$RUN_PY" -m pip install -r "$APP_DIR/requirements.txt"
    cp "$APP_DIR/requirements.txt" "$PROJECT_DIR/.venv/.titanium-requirements"
  fi
fi
cd "$APP_DIR"
printf 'TitaniumGuard: open http://127.0.0.1:%s\n' "${PORT:-8000}"
exec "$RUN_PY" -m uvicorn server:api --host 127.0.0.1 --port "${PORT:-8000}"
