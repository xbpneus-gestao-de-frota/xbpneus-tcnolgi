import os

import django
import pytest


# Garante que o Django está configurado para os testes
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
except RuntimeError:
    # O Django já pode ter sido inicializado por outro processo de testes
    pass

from rest_framework.test import APIClient  # noqa: E402
from django.contrib.auth import get_user_model  # noqa: E402


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(
        email="tester@xbpneus.com",
        password="pass123",
        nome_razao_social="Tester User",
        cnpj="12345678000100",
        telefone="(11) 99999-9999",
        is_active=True,
        aprovado=True,
    )


@pytest.fixture
def client_auth(user):
    client = APIClient()
    from rest_framework_simplejwt.tokens import RefreshToken

    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    return client
