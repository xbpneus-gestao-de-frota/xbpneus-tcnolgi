import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse

@pytest.mark.django_db
def test_create_empresa():
    client = APIClient()
    user_model = get_user_model()
    user = user_model.objects.create_user(
        email="admin@example.com",
        password="1234",
        nome_razao_social="Admin Test",
        cnpj="12345678000199",
        telefone="11999990000",
        aprovado=True,
        is_active=True,
        is_staff=True,
    )
    client.force_authenticate(user=user)
    url = reverse("empresa-list")
    response = client.post(url, {"nome": "XPTO", "tipo": "transportador", "cnpj": "12345678000123"})
    assert response.status_code == 201
