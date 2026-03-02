#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec op run --env-file="$SCRIPT_DIR/.env" -- uv run python "$SCRIPT_DIR/detect.py" "$@"
