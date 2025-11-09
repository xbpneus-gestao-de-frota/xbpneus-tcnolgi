#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
PYTHON_BIN=${PYTHON_BIN:-${PYTHON:-python3}}

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python interpreter '$PYTHON_BIN' is not available" >&2
  exit 1
fi

"$PYTHON_BIN" -m pip install --upgrade pip
"$PYTHON_BIN" -m pip install -r requirements.txt

export DJANGO_SETTINGS_MODULE=config.render_production
# Collect static files
"$PYTHON_BIN" manage.py collectstatic --no-input

# Ensure the static manifest contains the Django admin assets so deploys fail fast
"$PYTHON_BIN" <<'PY'
import json
import sys
from pathlib import Path

manifest_path = Path("staticfiles/staticfiles.json")

if not manifest_path.exists():
    sys.exit("collectstatic did not produce staticfiles/staticfiles.json")

data = json.loads(manifest_path.read_text())
paths = data.get("paths") or {}

if "admin/css/base.css" not in paths:
    sys.exit("Missing admin/css/base.css entry in staticfiles manifest; collectstatic may have failed")
PY

# Run migrations
"$PYTHON_BIN" manage.py migrate

# Note: Removed automatic creation of admin and test users for security.
