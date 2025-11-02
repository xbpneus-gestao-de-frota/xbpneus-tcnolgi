
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from xbpneus.backend.transportador.estoque.models import PecasEstoque, MovimentacaoEstoque
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
def setup_estoque_dependencies():
    empresa, _ = Empresa.objects.get_or_create(nome="Empresa Estoque", cnpj="99.888.777/0001-11", tipo="TRANSPORTADOR")
    filial, _ = Filial.objects.get_or_create(nome="Filial Estoque", codigo="003", empresa=empresa)
    return empresa, filial

@pytest.mark.django_db
def test_pecas_estoque_creation(auth_client, setup_estoque_dependencies):
    empresa, filial = setup_estoque_dependencies
    url = reverse("pecasestoque-list")
    data = {
        "empresa": empresa.id,
        "filial": filial.id,
        "codigo": "PEC001",
        "descricao": "Filtro de Óleo",
        "quantidade": 10,
        "unidade_medida": "UN",
        "valor_unitario": "50.00",
        "localizacao": "Prateleira A",
        "estoque_minimo": 5,
        "observacoes": "Peça para manutenção"
    }
    response = auth_client.post(url, data, format="json")
    assert response.status_code == 201, response.data
    assert PecasEstoque.objects.count() == 1
    peca = PecasEstoque.objects.first()
    assert peca.codigo == "PEC001"

@pytest.mark.django_db
def test_movimentacao_estoque_creation(auth_client, setup_estoque_dependencies):
    empresa, filial = setup_estoque_dependencies
    peca = PecasEstoque.objects.create(
        empresa=empresa, filial=filial, codigo="PEC002",
        descricao="Pastilha de Freio", quantidade=5,
        unidade_medida="UN", valor_unitario="120.00",
        localizacao="Prateleira B", estoque_minimo=2
    )
    url = reverse("movimentacaoestoque-list")
    data = {
        "peca": peca.id,
        "tipo_movimentacao": "ENTRADA",
        "quantidade": 3,
        "observacoes": "Recebimento de fornecedor"
    }
    response = auth_client.post(url, data, format="json")
    assert response.status_code == 201, response.data
    assert MovimentacaoEstoque.objects.count() == 1
    mov = MovimentacaoEstoque.objects.first()
    assert mov.peca == peca
    peca.refresh_from_db()
    assert peca.quantidade == 8

@pytest.mark.django_db
def test_movimentacao_estoque_saida(auth_client, setup_estoque_dependencies):
    empresa, filial = setup_estoque_dependencies
    peca = PecasEstoque.objects.create(
        empresa=empresa, filial=filial, codigo="PEC003",
        descricao="Lâmpada Farol", quantidade=10,
        unidade_medida="UN", valor_unitario="25.00",
        localizacao="Prateleira C", estoque_minimo=3
    )
    url = reverse("movimentacaoestoque-list")
    data = {
        "peca": peca.id,
        "tipo_movimentacao": "SAIDA",
        "quantidade": 4,
        "observacoes": "Uso em manutenção"
    }
    response = auth_client.post(url, data, format="json")
    assert response.status_code == 201, response.data
    assert MovimentacaoEstoque.objects.count() == 1
    mov = MovimentacaoEstoque.objects.first()
    assert mov.peca == peca
    peca.refresh_from_db()
    assert peca.quantidade == 6


