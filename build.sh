#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
python3.11 -m pip install --upgrade pip
python3.11 -m pip install -r requirements.txt

export DJANGO_SETTINGS_MODULE=config.render_production
# Collect static files
python3.11 manage.py collectstatic --no-input

# Run migrations
python3.11 manage.py migrate

# Note: Removed automatic creation of admin and test users for security.
