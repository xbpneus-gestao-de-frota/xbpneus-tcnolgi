import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_create_empresa():
    client = APIClient()
    user = User.objects.create_user(username="admin", password="1234", role="transportador")
    client.force_authenticate(user=user)
    response = client.post("/api/empresas/", {"nome": "XPTO", "tipo": "transportador", "cnpj": "123456789"})
    assert response.status_code == 201
