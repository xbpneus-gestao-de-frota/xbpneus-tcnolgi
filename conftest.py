import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from backend.tests.conftest import *  # noqa: F401,F403
