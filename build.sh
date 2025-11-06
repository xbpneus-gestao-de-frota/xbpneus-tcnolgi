#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

export DJANGO_SETTINGS_MODULE=config.render_production
# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Note: Removed automatic creation of admin and test users for security.
