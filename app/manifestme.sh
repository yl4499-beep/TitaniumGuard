#!/usr/bin/env bash
set -euo pipefail
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$APP_DIR")"
RUN_PY="${TITANIUM_PYTHON:-$PROJECT_DIR/.venv/bin/python}"
if [ ! -x "$RUN_PY" ]; then printf 'Run bash app/testme.sh first to create the environment.\n' >&2; exit 1; fi
"$RUN_PY" -m pip install rsconnect-python==1.27.0
cd "$APP_DIR"
"$(dirname "$RUN_PY")/rsconnect" write-manifest fastapi . --entrypoint server:api --overwrite --exclude '__pycache__/**' --exclude '.pytest_cache/**' --exclude 'test_api.py' --exclude 'requirements-dev.txt' --exclude '.env' --exclude '.env.*' --exclude '.rsconnect-python/**' --exclude 'rsconnect-python/**'
