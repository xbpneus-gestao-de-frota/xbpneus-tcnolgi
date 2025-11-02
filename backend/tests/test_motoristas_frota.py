
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from xbpneus.backend.transportador.motorista_interno.models import Motorista
from xbpneus.backend.transportador.empresas.models import Empresa, Filial

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def _create_user(email, password, is_staff=False, is_active=True):
        return User.objects.create_user(email=email, password=password, is_staff=is_staff, is_active=is_active)
    return _create_user

@pytest.fixture
def auth_client(api_client, create_user):
    user = create_user("test@example.com", "password123")
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def setup_motorista_dependencies():
    empresa, _ = Empresa.objects.get_or_create(nome="Empresa Teste", cnpj="12.345.678/0001-90", tipo="TRANSPORTADOR")
    filial, _ = Filial.objects.get_or_create(nome="Filial Teste", codigo="001", empresa=empresa)
    return empresa, filial

@pytest.mark.django_db
def test_motorista_list_endpoint(auth_client, setup_motorista_dependencies):
    empresa, filial = setup_motorista_dependencies
    Motorista.objects.create(
        empresa=empresa, filial=filial, nome="Motorista Teste",
        cpf="12345678901", cnh="123456789", categoria_cnh="D",
        data_nascimento="1980-01-01", telefone="(11)98765-4321",
        email="motorista@teste.com"
    )
    url = reverse("motorista-list")
    response = auth_client.get(url)
    assert response.status_code == 200, response.data
    assert len(response.data) == 1
    assert response.data[0]["nome"] == "Motorista Teste"

@pytest.mark.django_db
def test_motorista_create_endpoint(auth_client, setup_motorista_dependencies):
    empresa, filial = setup_motorista_dependencies
    url = reverse("motorista-list")
    data = {
        "empresa": empresa.id,
        "filial": filial.id,
        "nome": "Novo Motorista",
        "cpf": "10987654321",
        "cnh": "987654321",
        "categoria_cnh": "E",
        "data_nascimento": "1990-05-15",
        "telefone": "(21)91234-5678",
        "email": "novo.motorista@teste.com"
    }
    response = auth_client.post(url, data, format="json")
    assert response.status_code == 201, response.data
    assert Motorista.objects.count() == 1
    assert Motorista.objects.first().nome == "Novo Motorista"


