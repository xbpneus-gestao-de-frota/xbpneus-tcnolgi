#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies using Python 3.11 explicitly
python3.11 -m pip install --upgrade pip
python3.11 -m pip install -r requirements.txt

# Collect static files
python3.11 manage.py collectstatic --no-input

# Run migrations
python3.11 manage.py migrate

# Create superuser if it doesn't exist
python3.11 manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()

email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@xbpneus.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "Teste@2025")

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(email=email, password=password)
EOF

