#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Bootstrap admin user when credentials are provided
if { [ -n "${ADMIN_EMAIL}" ] && [ -n "${ADMIN_PASSWORD}" ]; } || \
   { [ -n "${DJANGO_SUPERUSER_EMAIL}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD}" ]; }; then
  python manage.py bootstrap_admin
else
  echo "[build] Variáveis ADMIN_EMAIL/DJANGO_SUPERUSER_EMAIL não configuradas. Pulando bootstrap_admin." >&2
fi


# Create or update superuser and test users
python manage.py criar_usuarios_teste
